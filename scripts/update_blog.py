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
from typing import Dict, List, Optional, Set, Tuple

class VelogSync:
    def __init__(self):
        """
        VelogSync 클래스 초기화
        - 환경변수 확인
        - 기본 디렉토리 생성
        - Git 저장소 초기화
        - 게시물 인덱스 초기화
        """
        # 환경변수 확인
        self.username = os.getenv('VELOG_USERNAME')
        self.git_username = os.getenv('GIT_USERNAME')
        self.git_email = os.getenv('GIT_EMAIL')
        self.series_posts = {}  # 시리즈별 게시물 추적을 위한 딕셔너리
        self.current_feed_urls = set()  # 현재 RSS 피드에 있는 URL들을 저장

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

        # URL을 키로 하는 파일 경로 인덱스
        self.posts_index = {}
        self.load_existing_posts()

    def ensure_directory_exists(self, directory: str):
        """지정된 디렉토리가 없으면 생성"""
        if not os.path.exists(directory):
            os.makedirs(directory)

    def load_existing_posts(self):
        """기존 게시물들의 URL과 파일 경로를 인덱싱"""
        for filepath in glob.glob(os.path.join(self.posts_dir, '*.md')):
            try:
                post = frontmatter.load(filepath)
                if 'link' in post.metadata:
                    self.posts_index[post.metadata['link']] = filepath
            except Exception as e:
                print(f"파일 로딩 중 오류 발생: {filepath}, {str(e)}")

    def collect_series_info(self):
        """모든 시리즈 정보 수집"""
        self.series_posts = {}
        for filepath in glob.glob(os.path.join(self.posts_dir, '*.md')):
            try:
                post = frontmatter.load(filepath)
                series_name = post.metadata.get('series_name')
                if series_name:
                    if series_name not in self.series_posts:
                        self.series_posts[series_name] = set()
                    self.series_posts[series_name].add(post.metadata['link'])
            except Exception as e:
                print(f"시리즈 정보 수집 중 오류: {str(e)}")

    def get_series_info(self, post_url: str) -> Dict[str, any]:
        """Velog 게시글의 시리즈 정보를 가져오는 함수"""
        try:
            response = requests.get(post_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 다양한 시리즈 관련 클래스 탐색
            series_selectors = [
                'div.sc-jIkXHa',  # 기존 선택자
                'div.series-info',
                'div[class*="series"]',  # series가 포함된 모든 클래스
                'h2[class*="series"]'    # 시리즈 제목을 포함할 수 있는 h2
            ]
            
            series_section = None
            for selector in series_selectors:
                series_section = soup.select_one(selector)
                if series_section:
                    break

            if series_section:
                print("시리즈 섹션 발견")
                
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
                        return {}

                # 시리즈 번호 찾기
                number_selectors = [
                    'div.series-number',
                    'div[class*="number"]',
                    'span[class*="number"]'
                ]
                
                series_number = None
                for selector in number_selectors:
                    number_element = series_section.select_one(selector)
                    if number_element:
                        series_number = number_element
                        break

                if series_number:
                    numbers = series_number.text.strip().split('/')
                    current_number = numbers[0].strip()
                    total_posts = numbers[1].strip()
                    
                    return {
                        "series_name": series_name,
                        "series_order": f"{current_number}/{total_posts}"
                    }
                else:
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

    def get_content_hash(self, content: str) -> str:
        """컨텐츠의 해시값 계산"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def convert_html_to_markdown(self, html_content: str) -> str:
        """HTML 컨텐츠를 마크다운으로 변환"""
        return self.h2t.handle(html_content)

    def check_changes(self, 
                     existing_post: frontmatter.Post, 
                     new_content: str,
                     new_title: str,
                     new_series_info: Dict) -> Tuple[bool, bool, bool, bool]:
        """
        게시물의 변경 사항을 확인하고 반환
        
        Returns:
            Tuple[bool, bool, bool, bool]: (content_changed, title_changed, series_changed, needs_update)
        """
        content_changed = self.get_content_hash(existing_post.content) != self.get_content_hash(new_content)
        title_changed = existing_post.metadata.get('title', '') != new_title
        
        # 시리즈 변경 확인
        old_series = existing_post.metadata.get('series_name')
        old_order = existing_post.metadata.get('series_order')
        new_series = new_series_info.get('series_name') if new_series_info else None
        new_order = new_series_info.get('series_order') if new_series_info else None
        
        series_changed = (old_series != new_series) or (old_order != new_order)
        
        # 전체적인 업데이트 필요 여부
        needs_update = content_changed or title_changed or series_changed
        
        return content_changed, title_changed, series_changed, needs_update

    def update_last_modified(self, 
                           metadata: Dict, 
                           content_changed: bool, 
                           title_changed: bool, 
                           series_changed: bool,
                           current_date: str,
                           original_date: str) -> str:
        """last_modified 값을 적절히 업데이트"""
        if content_changed or title_changed or series_changed:
            return current_date
        return metadata.get('last_modified', original_date)

    def update_series_order(self, series_name: str) -> None:
        """특정 시리즈의 모든 게시물의 순서를 업데이트"""
        if not series_name or series_name not in self.series_posts:
            return
    
        series_urls = self.series_posts[series_name]
        total_posts = len(series_urls)
        
        for i, post_url in enumerate(series_urls, 1):
            filepath = self.posts_index.get(post_url)
            if filepath and os.path.exists(filepath):
                try:
                    post = frontmatter.load(filepath)
                    if post.metadata.get('series_name') == series_name:
                        post.metadata['series_order'] = f"{i}/{total_posts}"
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(frontmatter.dumps(post))
                        print(f"시리즈 순서 업데이트: {os.path.basename(filepath)} -> {i}/{total_posts}")
                        self.repo.index.add([filepath])
                except Exception as e:
                    print(f"시리즈 순서 업데이트 실패: {str(e)}")

    def sanitize_filename(self, filename: str) -> str:
        """파일 이름에 사용할 수 없는 문자들을 처리"""
        # Windows와 Unix 모두에서 사용할 수 없는 문자들을 대체
        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        for char in invalid_chars:
            filename = filename.replace(char, '-')
        return filename

    def create_or_update_post(self, entry: feedparser.FeedParserDict) -> bool:
        """게시글 생성 또는 업데이트"""
        try:
            # 현재 피드에 있는 URL 추적
            self.current_feed_urls.add(entry.link)
            
            # 게시글 URL로 기존 파일 찾기
            existing_filepath = self.posts_index.get(entry.link)
            
            # 날짜 정보 추출
            date_str = datetime.strptime(
                entry.published, 
                '%a, %d %b %Y %H:%M:%S %Z'
            ).strftime('%Y-%m-%d')
            
            # 현재 날짜
            current_date = datetime.now().strftime('%Y-%m-%d')
            
            # 게시글 페이지에서 추가 정보 가져오기
            response = requests.get(entry.link)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 태그와 시리즈 정보 가져오기
            tags = self.get_tags(soup)
            series_info = self.get_series_info(entry.link)
    
            # HTML을 마크다운으로 변환
            markdown_content = self.convert_html_to_markdown(entry.description)
    
            # 초기값 설정
            is_new_post = True
            old_title = None
            changes = []  # 변경 사항 추적
            content_changed = False
            title_changed = False
            series_changed = False
            needs_update = False
            last_modified = current_date
    
            if existing_filepath and os.path.exists(existing_filepath):
                is_new_post = False
                try:
                    existing_post = frontmatter.load(existing_filepath)
                    old_title = existing_post.metadata.get('title')
                    
                    # 변경 사항 확인
                    content_changed, title_changed, series_changed, needs_update = self.check_changes(
                        existing_post, markdown_content, entry.title, series_info
                    )
                    
                    # last_modified 업데이트
                    last_modified = self.update_last_modified(
                        existing_post.metadata,
                        content_changed, 
                        title_changed,
                        series_changed,
                        current_date,
                        date_str
                    )
                    
                    # 변경 사항 추적
                    if content_changed:
                        changes.append("content")
                    if title_changed:
                        changes.append("title")
                    if series_changed:
                        changes.append("series")
                    
                except Exception as e:
                    print(f"기존 파일 읽기 실패: {str(e)}")
                    is_new_post = True
                    needs_update = True
                    last_modified = current_date
            else:
                needs_update = True
                last_modified = current_date
    
            # 메타데이터 설정
            post_metadata = {
                'date': date_str,
                'link': entry.link,
                'tags': tags,
                'last_modified': last_modified
            }
    
            # 시리즈 정보 처리
            if series_info:
                post_metadata.update(series_info)
                series_name = series_info['series_name']
                
                # 시리즈 게시물 목록 업데이트
                if series_name not in self.series_posts:
                    self.series_posts[series_name] = set()
                self.series_posts[series_name].add(entry.link)
            
                # 기존 시리즈에서 제거
                if not is_new_post:
                    try:
                        existing_post = frontmatter.load(existing_filepath)
                        old_series = existing_post.metadata.get('series_name')
                        if old_series and old_series != series_name:
                            if old_series in self.series_posts:
                                self.series_posts[old_series].discard(entry.link)
                                self.update_series_order(old_series)
                    except Exception as e:
                        print(f"기존 시리즈 정보 제거 중 오류: {str(e)}")
            else:
                # 기존 게시물이 시리즈에서 제거된 경우
                if not is_new_post:
                    try:
                        existing_post = frontmatter.load(existing_filepath)
                        old_series = existing_post.metadata.get('series_name')
                        if old_series and old_series in self.series_posts:
                            self.series_posts[old_series].discard(entry.link)
                            self.update_series_order(old_series)
                    except Exception as e:
                        print(f"기존 시리즈 정보 제거 중 오류: {str(e)}")
    
            # 파일 경로 및 이름 처리
            if is_new_post:
                filename = f"{date_str}-{self.sanitize_filename(entry.title)}.md"
                filepath = os.path.join(self.posts_dir, filename)
            else:
                if title_changed:
                    new_filename = f"{date_str}-{self.sanitize_filename(entry.title)}.md"
                    new_filepath = os.path.join(self.posts_dir, new_filename)
                    
                    try:
                        # 기존 파일 제거
                        self.repo.index.remove([existing_filepath])
                        # 파일 이름 변경
                        os.rename(existing_filepath, new_filepath)
                        # 새 파일 추가
                        self.repo.index.add([new_filepath])
                        
                        print(f"파일 이름 변경: {os.path.basename(existing_filepath)} -> {new_filename}")
                        filepath = new_filepath
                    except Exception as e:
                        print(f"파일 이름 변경 실패: {str(e)}")
                        filepath = existing_filepath
                else:
                    filepath = existing_filepath
    
            if needs_update:
                # 포스트 저장
                post_content = frontmatter.Post(markdown_content, **post_metadata)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(frontmatter.dumps(post_content))
    
                if not title_changed:  # 제목 변경 시에는 이미 add 되었음
                    self.repo.index.add([filepath])
    
                # 시리즈 정보가 있는 경우 다른 게시물들도 업데이트
                if series_info:
                    self.update_series_order(series_info['series_name'])
    
                # Git 커밋 메시지 설정
                if is_new_post:
                    commit_message = f"Add post: {entry.title} ({current_date})"
                else:
                    change_types = ' & '.join(changes) if changes else "general"
                    commit_message = f"Update {change_types} in: {entry.title} ({current_date})"
                
                # Git 커밋
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

    def sync(self):
        """메인 동기화 함수"""
        try:
            feed = feedparser.parse(self.rss_url)
            
            if feed.bozo:
                print(f"RSS 피드 파싱 오류: {feed.bozo_exception}")
                return

            # 현재 피드의 URL 집합 초기화
            self.current_feed_urls.clear()
            
            # 먼저 모든 시리즈 정보 수집
            self.collect_series_info()
            
            changes_made = False
            
            for entry in feed.entries:
                if self.create_or_update_post(entry):
                    changes_made = True

            # 이제 피드에는 없지만 로컬에 있는 파일들은 그대로 유지
            # (삭제된 게시물의 백업 유지)

            # 모든 게시물 처리 후 시리즈 순서 최종 업데이트
            for series_name in self.series_posts:
                self.update_series_order(series_name)

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