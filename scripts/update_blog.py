# scripts/update_blog.py

import feedparser
import frontmatter
import git
import os
import hashlib
import requests
import html2text
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Dict, List, Optional

class VelogSync:
    def __init__(self):
        """
        VelogSync 클래스 초기화
        - 환경변수 확인
        - 기본 디렉토리 생성
        - Git 저장소 초기화
        """
        # Velog 사용자명 가져오기
        self.username = os.getenv('VELOG_USERNAME')
        if not self.username:
            raise ValueError("VELOG_USERNAME 환경 변수가 설정되지 않았습니다.")

        # 게시글이 저장될 디렉토리 설정
        self.posts_dir = 'velog-posts'
        self.ensure_directory_exists(self.posts_dir)

        # Git 저장소 초기화
        self.repo = git.Repo('.')
        
        # RSS 피드 URL 설정
        self.rss_url = f'https://api.velog.io/rss/@{self.username}'
        
        # HTML to Markdown 변환기 초기화
        self.h2t = html2text.HTML2Text()
        self.h2t.body_width = 0  # 줄 바꿈 비활성화

    def ensure_directory_exists(self, directory: str):
        """지정된 디렉토리가 없으면 생성"""
        if not os.path.exists(directory):
            os.makedirs(directory)

    def get_series_info(self, post_url: str) -> Dict[str, str]:
        """
        Velog 게시글의 시리즈 정보를 가져오는 함수
        
        Args:
            post_url: 게시글 URL
            
        Returns:
            시리즈 정보를 담은 딕셔너리:
            - series_name: 시리즈 이름
            - series_order: 현재 포스트의 시리즈 내 순서
            - total_in_series: 시리즈의 총 포스트 수
            - series_list: 시리즈에 속한 모든 포스트 정보
        """
        try:
            response = requests.get(post_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            series_section = soup.select_one('.series-card')
            if series_section:
                # 시리즈 제목 추출
                series_name = series_section.select_one('.series-name').text.strip()
                
                # 시리즈 내 순서 정보 추출
                series_order_element = soup.select_one('.series-number')
                current_number = series_order_element.text.strip() if series_order_element else "1"
                
                # 시리즈의 모든 포스트 정보 수집
                series_list = []
                series_items = series_section.select('.series-list-item')
                total_posts = len(series_items)
                
                for item in series_items:
                    series_list.append({
                        'title': item.select_one('.series-item-title').text.strip(),
                        'link': item.get('href', ''),
                        'current': 'current' in item.get('class', [])
                    })
                
                return {
                    "series_name": series_name,
                    "series_order": current_number,
                    "total_in_series": total_posts,
                    "series_list": series_list
                }
                
        except Exception as e:
            print(f"시리즈 정보 가져오기 실패: {str(e)}")
        return {}

    def get_content_hash(self, content: str) -> str:
        """
        컨텐츠의 해시값 계산
        
        Args:
            content: 해시를 계산할 컨텐츠
            
        Returns:
            컨텐츠의 SHA-256 해시값
        """
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def convert_html_to_markdown(self, html_content: str) -> str:
        """
        HTML 컨텐츠를 마크다운으로 변환
        
        Args:
            html_content: 변환할 HTML 컨텐츠
            
        Returns:
            변환된 마크다운 텍스트
        """
        return self.h2t.handle(html_content)

    def create_or_update_post(self, entry: feedparser.FeedParserDict) -> bool:
        """
        게시글 생성 또는 업데이트
        
        Args:
            entry: RSS 피드에서 가져온 게시글 정보
            
        Returns:
            bool: 변경사항이 있으면 True, 없으면 False
        """
        try:
            # 파일명에서 사용할 수 없는 문자 처리
            title = entry.title.replace('/', '-').replace('\\', '-')
            date_str = datetime.strptime(
                entry.published, 
                '%a, %d %b %Y %H:%M:%S %Z'
            ).strftime('%Y-%m-%d')
            
            # 현재 시간을 last_modified로 사용
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # 파일명 생성 (날짜-제목.md 형식)
            filename = f"{date_str}-{title}.md"
            filepath = os.path.join(self.posts_dir, filename)

            # 태그 처리
            tags = []
            if hasattr(entry, 'tags'):
                tags = [tag.term for tag in entry.tags]
            elif hasattr(entry, 'category'):
                tags = [entry.category]

            # 시리즈 정보 가져오기
            series_info = self.get_series_info(entry.link)

            # 메타데이터 설정
            post_metadata = {
                'title': entry.title,
                'date': date_str,
                'link': entry.link,
                'tags': tags,
                'last_modified': current_time
            }

            # 시리즈 정보가 있으면 메타데이터에 추가
            if series_info:
                post_metadata.update(series_info)

            # HTML을 마크다운으로 변환
            markdown_content = self.convert_html_to_markdown(entry.description)
            content_hash = self.get_content_hash(markdown_content)

            # 파일 존재 여부 확인과 업데이트 필요성 체크
            update_needed = True
            is_new_post = not os.path.exists(filepath)

            # 기존 파일이 있는 경우 내용 비교
            if not is_new_post:
                try:
                    existing_post = frontmatter.load(filepath)
                    existing_hash = self.get_content_hash(existing_post.content)
                    if existing_hash == content_hash and existing_post.metadata.get('last_modified') == current_time:
                        update_needed = False
                except Exception as e:
                    print(f"기존 파일 읽기 실패: {str(e)}")

            # 업데이트가 필요한 경우 처리
            if update_needed:
                # frontmatter와 내용을 합쳐서 마크다운 파일 생성
                post_content = frontmatter.Post(markdown_content, **post_metadata)
                
                # 파일 저장
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(frontmatter.dumps(post_content))

                # Git에 변경사항 추가
                self.repo.index.add([filepath])
                action = "Add" if is_new_post else "Update"
                commit_message = f"{action} post: {entry.title} ({current_time})"
                self.repo.index.commit(commit_message)

                action_str = "추가됨" if is_new_post else "업데이트됨"
                print(f"게시글 {action_str}: {entry.title}")
                return True

            return False

        except Exception as e:
            print(f"게시글 처리 중 오류 발생: {str(e)}")
            return False

    def sync(self):
        """
        메인 동기화 함수
        - RSS 피드를 가져와서 각 게시글을 처리
        - 변경사항이 있으면 GitHub에 push
        """
        try:
            # RSS 피드 파싱
            feed = feedparser.parse(self.rss_url)
            
            if feed.bozo:  # RSS 파싱 에러 체크
                print(f"RSS 피드 파싱 오류: {feed.bozo_exception}")
                return

            changes_made = False
            
            # 각 게시글 처리
            for entry in feed.entries:
                if self.create_or_update_post(entry):
                    changes_made = True

            # 변경사항이 있으면 Git push
            if changes_made:
                print("변경사항 반영하는중...")
                origin = self.repo.remote(name='origin')
                origin.push()
                print("모든 변경사항이 GitHub에 push 되었습니다.")
            else:
                print("변경사항이 없습니다.")

        except Exception as e:
            print(f"동기화 중 오류 발생: {str(e)}")

if __name__ == "__main__":
    syncer = VelogSync()
    syncer.sync()