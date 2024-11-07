# scripts/update_blog.py

import feedparser
import frontmatter
import git
import os
import hashlib
import requests
import html2text
import glob
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Dict, List, Optional

class VelogSync:
    def __init__(self):
        """VelogSync 클래스 초기화"""
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
        if not os.path.exists(self.posts_dir):
            os.makedirs(self.posts_dir)

        # Git 저장소 초기화
        self.repo = git.Repo('.')
        
        # RSS 피드 URL 설정
        self.rss_url = f'https://api.velog.io/rss/@{self.username}'
        
        # HTML to Markdown 변환기 초기화
        self.h2t = html2text.HTML2Text()
        self.h2t.body_width = 0

        # URL을 키로 하는 파일 경로 인덱스
        self.posts_index = {}
        self.load_existing_posts()

    def load_existing_posts(self):
        """기존 게시물들의 URL과 파일 경로를 인덱싱"""
        for filepath in glob.glob(os.path.join(self.posts_dir, '*.md')):
            try:
                post = frontmatter.load(filepath)
                if 'link' in post.metadata:
                    self.posts_index[post.metadata['link']] = filepath
            except Exception as e:
                print(f"파일 로딩 중 오류 발생: {filepath}, {str(e)}")

    def get_series_info(self, post_url: str) -> Dict[str, any]:
        """Velog 게시글의 시리즈 정보를 가져오는 함수"""
        try:
            response = requests.get(post_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            series_selectors = [
                'div.sc-jIkXHa',
                'div.series-info',
                'div[class*="series"]',
                'h2[class*="series"]'
            ]
            
            for selector in series_selectors:
                series_section = soup.select_one(selector)
                if series_section:
                    # 시리즈 제목 찾기
                    series_title = series_section.find('h2')
                    if series_title and series_title.find('a'):
                        series_name = series_title.find('a').text.strip()
                    elif series_title:
                        series_name = series_title.text.strip()
                    else:
                        series_link = series_section.find('a')
                        if series_link:
                            series_name = series_link.text.strip()
                        else:
                            continue

                    # 시리즈 번호 찾기
                    number_selectors = [
                        'div.series-number',
                        'div[class*="number"]',
                        'span[class*="number"]'
                    ]
                    
                    for num_selector in number_selectors:
                        number_element = series_section.select_one(num_selector)
                        if number_element:
                            numbers = number_element.text.strip().split('/')
                            return {
                                "series_name": series_name,
                                "series_order": f"{numbers[0].strip()}/{numbers[1].strip()}"
                            }
                    
                    return {"series_name": series_name}
            
        except Exception as e:
            print(f"시리즈 정보 가져오기 실패: {str(e)}")
        return {}

    def get_tags(self, soup: BeautifulSoup) -> List[str]:
        """게시글의 태그 정보를 가져오는 함수"""
        tags = []
        try:
            tag_list = soup.find('div', class_='sc-cZMNgc')
            if tag_list:
                tags = [tag.text.strip() for tag in tag_list.find_all('a', class_='sc-dtMgUX')]
            else:
                tag_elements = soup.find_all('a', attrs={'data-tag': True})
                if tag_elements:
                    tags = [tag.text.strip() for tag in tag_elements]
        except Exception as e:
            print(f"태그 정보 가져오기 실패: {str(e)}")
        return tags

    def sanitize_filename(self, filename: str) -> str:
        """파일 이름에 사용할 수 없는 문자들을 처리"""
        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        for char in invalid_chars:
            filename = filename.replace(char, '-')
        return filename

    def create_or_update_post(self, entry: feedparser.FeedParserDict) -> bool:
        """게시글 생성 또는 업데이트"""
        try:
            # 기본 정보 설정
            existing_filepath = self.posts_index.get(entry.link)
            date_str = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %Z').strftime('%Y-%m-%d')
            current_date = datetime.now().strftime('%Y-%m-%d')
    
            # Velog에서 최신 정보 가져오기
            response = requests.get(entry.link)
            soup = BeautifulSoup(response.text, 'html.parser')
            tags = self.get_tags(soup)
            series_info = self.get_series_info(entry.link)
            markdown_content = self.convert_html_to_markdown(entry.description)
    
            # 변경사항 확인
            is_new_post = not existing_filepath or not os.path.exists(existing_filepath)
            changes = []
            
            if not is_new_post:
                try:
                    existing_post = frontmatter.load(existing_filepath)
                    
                    # 내용 변경 확인 (공백 무시)
                    if existing_post.content.strip() != markdown_content.strip():
                        changes.append("content")
                        print(f"내용 변경 감지")
                    
                    # 시리즈 변경 확인
                    existing_series = existing_post.metadata.get('series_name')
                    new_series = series_info.get('series_name')
                    if existing_series != new_series:
                        changes.append("series")
                        print(f"시리즈 변경 감지: {existing_series} -> {new_series}")
                    
                    # 태그 변경 확인
                    existing_tags = set(existing_post.metadata.get('tags', []))
                    new_tags = set(tags)
                    if existing_tags != new_tags:
                        changes.append("tags")
                        print(f"태그 변경 감지: {existing_tags} -> {new_tags}")
                
                except Exception as e:
                    print(f"기존 포스트 읽기 실패, 새 포스트로 처리: {str(e)}")
                    is_new_post = True
                    changes = ["content", "metadata"]  # 전체 변경으로 처리
    
            # 파일명 설정
            filename = f"{date_str}-{self.sanitize_filename(entry.title)}.md"
            filepath = os.path.join(self.posts_dir, filename)
    
            # 메타데이터 설정
            metadata = {
                'date': date_str,
                'link': entry.link,
                'tags': tags,
                'last_modified': current_date if changes else (
                    existing_post.metadata.get('last_modified', date_str) if not is_new_post else date_str
                )
            }
            if series_info:
                metadata.update(series_info)
    
            # 변경사항이 있거나 새 게시물인 경우 저장
            if changes or is_new_post:
                print(f"{'새 게시물 추가' if is_new_post else '게시물 업데이트'}: {entry.title}")
                print(f"변경사항: {', '.join(changes) if changes else '없음'}")
                
                # 파일명 변경이 필요한 경우
                if not is_new_post and existing_filepath != filepath:
                    self.repo.index.remove([existing_filepath])
                    os.rename(existing_filepath, filepath)
                    print(f"파일명 변경: {os.path.basename(existing_filepath)} -> {os.path.basename(filepath)}")
    
                # 포스트 저장
                post = frontmatter.Post(markdown_content, **metadata)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(frontmatter.dumps(post))
    
                # Git 커밋
                self.repo.index.add([filepath])
                commit_message = "Add post: " if is_new_post else f"Update {', '.join(changes)} in: "
                commit_message += f"{entry.title} ({current_date})"
                
                self.repo.index.commit(
                    commit_message,
                    author=git.Actor(self.git_username, self.git_email),
                    committer=git.Actor(self.git_username, self.git_email)
                )
    
                # 인덱스 업데이트
                self.posts_index[entry.link] = filepath
                return True
    
            return False
    
        except Exception as e:
            print(f"게시글 처리 중 오류 발생: {str(e)}")
            return False

    def convert_html_to_markdown(self, html_content: str) -> str:
        """HTML 컨텐츠를 마크다운으로 변환"""
        return self.h2t.handle(html_content)

    def sync(self):
        """메인 동기화 함수"""
        try:
            feed = feedparser.parse(self.rss_url)
            
            if feed.bozo:
                print(f"RSS 피드 파싱 오류: {feed.bozo_exception}")
                return
    
            changes_made = False
            series_changes = {}  # 시리즈별 변경사항 추적
    
            # 첫번째 패스: 모든 게시물의 변경사항 확인 및 기본 업데이트
            for entry in feed.entries:
                try:
                    # 게시물의 시리즈 정보 가져오기
                    response = requests.get(entry.link)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    series_info = self.get_series_info(entry.link)
    
                    # 기존 게시물의 시리즈 정보와 비교
                    if entry.link in self.posts_index:
                        try:
                            existing_post = frontmatter.load(self.posts_index[entry.link])
                            old_series = existing_post.metadata.get('series_name')
                            new_series = series_info.get('series_name')
                            
                            # 시리즈 변경 감지
                            if old_series != new_series:
                                # 이전 시리즈와 새 시리즈 모두 업데이트 필요
                                if old_series:
                                    series_changes[old_series] = True
                                if new_series:
                                    series_changes[new_series] = True
                        except Exception as e:
                            print(f"시리즈 변경 감지 중 오류: {str(e)}")
    
                    # 일반 게시물 처리
                    if self.create_or_update_post(entry):
                        changes_made = True
                    
                    # 현재 게시물의 시리즈 정보 저장
                    if series_info.get('series_name'):
                        series_changes[series_info['series_name']] = True
                        
                except Exception as e:
                    print(f"게시물 처리 중 오류 발생: {str(e)}")
    
            # 두번째 패스: 변경된 시리즈의 모든 게시물 업데이트
            for series_name in series_changes:
                print(f"시리즈 '{series_name}' 전체 업데이트 중...")
                for filepath in glob.glob(os.path.join(self.posts_dir, '*.md')):
                    try:
                        post = frontmatter.load(filepath)
                        if post.metadata.get('series_name') == series_name:
                            post_url = post.metadata['link']
                            response = requests.get(post_url)
                            soup = BeautifulSoup(response.text, 'html.parser')
                            content = soup.find('div', class_='blog-post-content')
                            
                            if content:
                                # feedparser.FeedParserDict와 동일한 구조로 생성
                                mock_entry = feedparser.FeedParserDict({
                                    'title': post.metadata.get('title', ''),
                                    'link': post_url,
                                    'published': post.metadata.get('date', ''),
                                    'description': content.decode_contents()
                                })
                                
                                self.create_or_update_post(mock_entry)
                                changes_made = True
                    except Exception as e:
                        print(f"시리즈 게시물 업데이트 중 오류: {str(e)}")
    
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