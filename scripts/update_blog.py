# scripts/update_blog.py

import feedparser
import frontmatter
import git
import os
import requests
import html2text
import glob
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Dict, List

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

    def convert_html_to_markdown(self, html_content: str) -> str:
        """HTML 컨텐츠를 마크다운으로 변환"""
        return self.h2t.handle(html_content)

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
            markdown_content = self.convert_html_to_markdown(entry.description)

            # 변경사항 확인
            is_new_post = not existing_filepath or not os.path.exists(existing_filepath)
            changes = []
            
            if not is_new_post:
                existing_post = frontmatter.load(existing_filepath)
                # 변경사항 검사
                if existing_post.content.strip() != markdown_content.strip():
                    changes.append("content")
                if existing_post.metadata.get('tags') != tags:
                    changes.append("tags")

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

            # 변경사항이 있거나 새 게시물인 경우 저장
            if changes or is_new_post:
                print(f"{'새 게시물 추가' if is_new_post else '게시물 업데이트(제목)'}: {entry.title}")
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
                print("변경사항 반영 중...")
                origin = self.repo.remote(name='origin')
                origin.push()
                print("모든 변경사항이 GitHub에 반영되었습니다.")
            else:
                print("변경사항이 없습니다.")

        except Exception as e:
            print(f"동기화 중 오류 발생: {str(e)}")

if __name__ == "__main__":
    syncer = VelogSync()
    syncer.sync()