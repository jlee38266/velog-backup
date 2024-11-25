# scripts/update_blog_graphql.py

import glob  # 특정 패턴에 맞는 파일 이름 찾는 모듈 라이브러리
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
        self.id_index = {}  # post_id -> filepath

        for filepath in glob.glob(os.path.join(self.posts_dir, '*.md')):
            try:
                post = frontmatter.load(filepath)
                if '_id' in post.metadata:  # 내부적으로만 사용할 _id 저장
                    self.id_index[post.metadata['_id']] = filepath
            except Exception as e:
                print(f"파일 로딩 중 오류 발생: {filepath}, {str(e)}")

    def sanitize_filename(self, filename: str) -> str:
        """파일 이름에 사용할 수 없는 문자들을 처리합니다"""
        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        for char in invalid_chars:
            filename = filename.replace(char, '-')
        return filename

    def get_all_posts(self) -> List[Dict]:
        """GraphQL을 사용하여 모든 게시물 정보 가져오기"""
        # 1. 먼저 모든 게시물의 기본 정보를 가져옵니다
        posts_query = """
        query Posts($username: String!) { 
            posts(username: $username) { 
                title 
                url_slug 
            } 
        }
        """

        # username 변수 추가
        variables = {
            "username": self.username
        }

        response = requests.post(
            self.graphql_url,
            json={
                'query': posts_query,
                'variables': variables  # 변수 전달
            }
        )

        if response.status_code != 200:
            print(f"게시물 목록 가져오기 실패: {response.status_code}")
            return []

        posts_data = response.json()
        if 'data' not in posts_data or 'posts' not in posts_data['data']:
            print("게시물 목록 형식이 올바르지 않습니다.")
            return []

        posts_list = posts_data['data']['posts']
        complete_posts = []

        # 2. 각 게시물의 상세 정보를 가져옵니다
        for post in posts_list:
            post_query = """
            query Post($username: String!, $url_slug: String!) { 
                post(username: $username, url_slug: $url_slug) {
                    id 
                    title 
                    released_at 
                    updated_at 
                    body 
                    is_private 
                    url_slug 
                } 
            }
            """

            variables = {
                "username": self.username,
                "url_slug": post['url_slug']
            }

            post_response = requests.post(
                self.graphql_url,
                json={
                    'query': post_query,
                    'variables': variables
                }
            )

            if post_response.status_code == 200:
                post_data = post_response.json()
                if 'data' in post_data and 'post' in post_data['data'] and post_data['data']['post']:
                    post_detail = post_data['data']['post']
                    # private이 아닌 게시물만 추가
                    if not post_detail['is_private']:
                        complete_posts.append(post_detail)
                    print(f"게시물 가져오기 성공: {post_detail['title']}")
                else:
                    print(f"게시물 상세 정보를 가져올 수 없습니다: {post['title']}")
            else:
                print(f"게시물 상세 정보 가져오기 실패: {post['title']}")

        return complete_posts

    def create_or_update_post(self, post: Dict) -> bool:
        """게시글을 생성하거나 업데이트합니다"""
        try:
            # post_id로 기존 파일 찾기
            existing_filepath = self.id_index.get(post['id'])

            # Velog URL 생성
            post_url = f"https://velog.io/@{self.username}/{post['url_slug']}"

            # 날짜 정보 변환
            date_str = datetime.fromisoformat(post['released_at'].replace('Z', '+00:00')).strftime('%Y-%m-%d')
            current_date = datetime.now().strftime('%Y-%m-%d')
            last_modified = datetime.fromisoformat(post['updated_at'].replace('Z', '+00:00')).strftime('%Y-%m-%d')

            # 변경사항 확인
            is_new_post = not existing_filepath or not os.path.exists(existing_filepath)
            changes = []

            if not is_new_post:
                existing_post = frontmatter.load(existing_filepath)
                if existing_post.content.strip() != post['body'].strip():
                    changes.append("content")
                if existing_post.metadata.get('title') != post['title']:
                    changes.append("title")
                if existing_post.metadata.get('url') != post_url:
                    changes.append("url")
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
                'last_modified': last_modified,
                '_id': post['id']
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