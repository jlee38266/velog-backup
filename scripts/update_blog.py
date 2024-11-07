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
        # 환경변수 확인
        self.username = os.getenv('VELOG_USERNAME')
        self.git_username = os.getenv('GIT_USERNAME')
        self.git_email = os.getenv('GIT_EMAIL')

        if not self.username:
            raise ValueError("VELOG_USERNAME 환경 변수가 설정되지 않았습니다.")
        if not self.git_username or not self.git_email:
            raise ValueError("Git 사용자 정보가 설정되지 않았습니다.")

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

    def get_series_info(self, post_url: str) -> Dict[str, any]:
        """
        Velog 게시글의 시리즈 정보를 가져오는 함수
        """
        try:
            response = requests.get(post_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 시리즈 정보 찾기
            series_section = soup.find('div', class_='sc-jIkXHa')
            if series_section:
                # 시리즈 제목
                series_name = series_section.find('h2').find('a').text.strip()
                
                # 시리즈 번호
                series_number = series_section.find('div', class_='series-number')
                if series_number:
                    # 현재 포스트 번호와 총 포스트 수 찾기
                    numbers = series_number.text.strip().split('/')
                    current_number = numbers[0].strip()
                    total_posts = numbers[1].strip()
                    
                    return {
                        "series_name": series_name,
                        "series_order": f"{current_number}/{total_posts}",
                        "total_in_series": total_posts
                    }
        except Exception as e:
            print(f"시리즈 정보 가져오기 실패: {str(e)}")
        return {}

    def get_tags(self, soup: BeautifulSoup) -> List[str]:
        """
        게시글의 태그 정보를 가져오는 함수
        """
        tags = []
        try:
            tag_list = soup.find('div', class_='sc-cZMNgc')
            if tag_list:
                tags = [tag.text.strip() for tag in tag_list.find_all('a', class_='sc-dtMgUX')]
        except Exception as e:
            print(f"태그 정보 가져오기 실패: {str(e)}")
        return tags

    def get_content_hash(self, content: str) -> str:
        """컨텐츠의 해시값 계산"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def convert_html_to_markdown(self, html_content: str) -> str:
        """HTML 컨텐츠를 마크다운으로 변환"""
        return self.h2t.handle(html_content)

    def create_or_update_post(self, entry: feedparser.FeedParserDict) -> bool:
        """게시글 생성 또는 업데이트"""
        try:
            # 파일명 처리
            title = entry.title.replace('/', '-').replace('\\', '-')
            date_str = datetime.strptime(
                entry.published, 
                '%a, %d %b %Y %H:%M:%S %Z'
            ).strftime('%Y-%m-%d')
            
            # 현재 날짜를 last_modified로 사용 (시간 제외)
            current_date = datetime.now().strftime('%Y-%m-%d')
            
            filename = f"{date_str}-{title}.md"
            filepath = os.path.join(self.posts_dir, filename)

            # 게시글 페이지에서 추가 정보 가져오기
            response = requests.get(entry.link)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 태그와 시리즈 정보 가져오기
            tags = self.get_tags(soup)
            series_info = self.get_series_info(entry.link)

            # 메타데이터 설정
            post_metadata = {
                'title': entry.title,
                'date': date_str,
                'link': entry.link,
                'tags': tags,
                'last_modified': current_date  # 기본값으로 현재 날짜 설정
            }

            # 시리즈 정보가 있으면 메타데이터에 추가
            if series_info:
                post_metadata.update(series_info)

            # HTML을 마크다운으로 변환
            markdown_content = self.convert_html_to_markdown(entry.description)
            content_hash = self.get_content_hash(markdown_content)

            # 업데이트 필요성 체크
            update_needed = True
            is_new_post = not os.path.exists(filepath)

            if not is_new_post:
                try:
                    existing_post = frontmatter.load(filepath)
                    existing_hash = self.get_content_hash(existing_post.content)
                    if existing_hash == content_hash:
                        update_needed = False
                        # 기존 메타데이터에서 last_modified 필드 유지
                        if 'last_modified' in existing_post.metadata:
                            post_metadata['last_modified'] = existing_post.metadata['last_modified']
                    else:
                        # 내용이 변경되었으므로 last_modified 업데이트
                        post_metadata['last_modified'] = current_date
                except Exception as e:
                    print(f"기존 파일 읽기 실패: {str(e)}")

            # 업데이트 처리
            if update_needed:
                post_content = frontmatter.Post(markdown_content, **post_metadata)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(frontmatter.dumps(post_content))

                # Git에 변경사항 추가
                self.repo.index.add([filepath])
                action = "Add" if is_new_post else "Update"
                commit_message = f"{action} post: {entry.title} ({current_date})"
                
                # Author 정보를 포함하여 커밋
                self.repo.index.commit(
                    commit_message,
                    author=git.Actor(self.git_username, self.git_email),
                    committer=git.Actor(self.git_username, self.git_email)
                )

                action_str = "추가됨" if is_new_post else "업데이트됨"
                print(f"게시글 {action_str}: {entry.title}")
                return True

            return False

        except Exception as e:
            print(f"게시글 처리 중 오류 발생: {str(e)}")
            return False

    def sync(self):
        """메인 동기화 함수"""
        try:
            feed = feedparser.parse(self.rss_url)
            
            if feed.bozo:
                print(f"RSS 피드 파싱 오류: {feed.bozo_exception}")
                return

            changes_made = False
            
            for entry in feed.entries:
                if self.create_or_update_post(entry):
                    changes_made = True

            if changes_made:
                print("변경사항 푸시 중...")
                origin = self.repo.remote(name='origin')
                origin.push()
                print("모든 변경사항이 GitHub에 푸시되었습니다.")
            else:
                print("변경사항이 없습니다.")

        except Exception as e:
            print(f"동기화 중 오류 발생: {str(e)}")

if __name__ == "__main__":
    syncer = VelogSync()
    syncer.sync()