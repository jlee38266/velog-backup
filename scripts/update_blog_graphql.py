# scripts/update_blog_graphql.py

import frontmatter  # markdown 파일의 메타데이터를 처리하기 위한 라이브러리
import git  # Git 작업을 위한 라이브러리
import os  # 파일/디렉토리 작업을 위한 라이브러리
import requests  # HTTP 요청을 위한 라이브러리
from datetime import datetime  # 날짜/시간 처리를 위한 라이브러리
from typing import Dict, List  # 타입 힌트를 위한 라이브러리

class VelogSync:
    def __init__(self):
        """클래스 초기화 - 프로그램 시작시 필요한 기본 설정을 합니다"""
        # 환경 변수에서 필요한 정보를 가져옵니다
        self.username = os.getenv('VELOG_USERNAME')
        self.git_username = os.getenv('GIT_USERNAME')
        self.git_email = os.getenv('GIT_EMAIL')

        # 필수 환경 변수가 없으면 오류를 발생시킵니다
        if not self.username:
            raise ValueError("VELOG_USERNAME 환경 변수가 설정되지 않았습니다.")
        if not self.git_username or not self.git_email:
            raise ValueError("Git 사용자 정보가 설정되지 않았습니다.")

        # Velog API 주소 설정
        self.graphql_url = 'https://api.velog.io/graphql'

        # 게시글이 저장될 디렉토리 설정
        self.posts_dir = 'velog-posts'
        if not os.path.exists(self.posts_dir):
            os.makedirs(self.posts_dir)

        # Git 저장소 초기화
        self.repo = git.Repo('.')

        # URL을 키로 하는 파일 경로 인덱스
        self.posts_index = {}
        self.load_existing_posts()

    def load_existing_posts(self):
        """기존에 저장된 게시물들의 정보를 불러옵니다"""
        for filepath in glob.glob(os.path.join(self.posts_dir, '*.md')):
            try:
                post = frontmatter.load(filepath)
                if 'url' in post.metadata:
                    self.posts_index[post.metadata['url']] = filepath
            except Exception as e:
                print(f"파일 로딩 중 오류 발생: {filepath}, {str(e)}")

    def sanitize_filename(self, filename: str) -> str:
        """파일 이름에 사용할 수 없는 문자들을 처리합니다"""
        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        for char in invalid_chars:
            filename = filename.replace(char, '-')
        return filename

    def get_all_posts(self) -> List[Dict]:
        """Velog에서 모든 게시물 정보를 가져옵니다"""
        posts = []
        after = None

        while True:
            # GraphQL 쿼리 정의
            query = """
            query Posts($username: String!, $after: ID) {
                posts(username: $username, after: $after) {
                    title
                    body
                    url_slug
                    released_at
                    updated_at
                    is_private
                }
            }
            """

            # 쿼리 변수 설정
            variables = {
                "username": self.username,
                "after": after
            }

            # API 요청 보내기
            response = requests.post(
                self.graphql_url,
                json={'query': query, 'variables': variables}
            )

            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'posts' in data['data']:
                    current_posts = data['data']['posts']
                    if not current_posts:  # 더 이상 게시물이 없으면 종료
                        break

                    # private이 아닌 게시물만 필터링
                    public_posts = [post for post in current_posts if not post['is_private']]
                    posts.extend(public_posts)

                    # 마지막 게시물의 ID를 다음 페이지 요청에 사용
                    if current_posts:
                        after = current_posts[-1]['id']
                    else:
                        break
                else:
                    print("GraphQL 응답 형식이 올바르지 않습니다.")
                    break
            else:
                print(f"GraphQL 요청 실패: {response.status_code}")
                break

        return posts

    def create_or_update_post(self, post: Dict) -> bool:
        """게시글을 생성하거나 업데이트합니다"""
        try:
            # Velog URL 생성
            post_url = f"https://velog.io/@{self.username}/{post['url_slug']}"
            existing_filepath = self.posts_index.get(post_url)

            # 날짜 정보 변환
            date_str = datetime.fromisoformat(post['released_at'].replace('Z', '+00:00')).strftime('%Y-%m-%d')
            current_date = datetime.now().strftime('%Y-%m-%d')
            last_modified = datetime.fromisoformat(post['updated_at'].replace('Z', '+00:00')).strftime('%Y-%m-%d')

            # 변경사항 확인
            is_new_post = not existing_filepath or not os.path.exists(existing_filepath)
            changes = []

            if not is_new_post:
                existing_post = frontmatter.load(existing_filepath)
                # 각종 변경사항 체크
                if existing_post.content.strip() != post['body'].strip():
                    changes.append("content")
                if existing_post.metadata.get('title') != post['title']:
                    changes.append("title")
                if existing_post.metadata.get('url') != post_url:
                    changes.append("url")
                    old_url = existing_post.metadata.get('url')
                    if old_url in self.posts_index:
                        del self.posts_index[old_url]
                if existing_post.metadata.get('last_modified') != last_modified:
                    changes.append("last_modified")

            # 파일명 설정
            filename = f"{date_str}-{self.sanitize_filename(post['title'])}.md"
            filepath = os.path.join(self.posts_dir, filename)

            # 메타데이터 설정
            metadata = {
                'title': post['title'],
                'date': date_str,
                'url': post_url,
                'last_modified': last_modified
            }

            # 변경사항이 있거나 새 게시물인 경우 저장
            if changes or is_new_post:
                print(f"{'새 게시물 추가' if is_new_post else '게시물 업데이트'}: {post['title']}")
                print(f"변경사항: {', '.join(changes) if changes else '없음'}")

                # 파일명 변경이 필요한 경우
                if not is_new_post and existing_filepath != filepath:
                    if os.path.exists(existing_filepath):
                        self.repo.index.remove([existing_filepath])
                        os.rename(existing_filepath, filepath)
                        print(f"파일명 변경: {os.path.basename(existing_filepath)} -> {os.path.basename(filepath)}")

                # 포스트 저장
                post = frontmatter.Post(post['body'], **metadata)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(frontmatter.dumps(post))

                # Git 커밋
                self.repo.index.add([filepath])
                commit_message = "Add post: " if is_new_post else f"Update {', '.join(changes)} in: "
                commit_message += f"{post['title']} ({current_date})"

                self.repo.index.commit(
                    commit_message,
                    author=git.Actor(self.git_username, self.git_email),
                    committer=git.Actor(self.git_username, self.git_email)
                )

                # 인덱스 업데이트
                self.posts_index[post_url] = filepath
                return True

            return False

        except Exception as e:
            print(f"게시글 처리 중 오류 발생: {str(e)}")
            return False

    def sync(self):
        """전체 동기화 프로세스를 실행합니다"""
        try:
            print("Velog에서 게시물 가져오는 중...")
            posts = self.get_all_posts()

            changes_made = False
            for post in posts:
                if self.create_or_update_post(post):
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