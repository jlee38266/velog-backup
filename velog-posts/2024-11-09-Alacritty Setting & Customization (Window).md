---
date: '2024-11-09'
last_modified: '2024-11-09'
link: https://velog.io/@jlee38266/Alacritty-Setting-Customization-Window
tags:
- alacritty
---

> _Alacritty는 v0.13.0부터 TOML 설정 파일을 기본으로 사용하도록 변경되었습니다. 여전히 YAML 파일을 지원은 합니다만, 권장 방식을 따라 TOML로 설정 파일을 설정합니다. TOML 파일의 유효성 검증이 필요한 경우 아래의 링크에 통해 검사할 수도 있습니다._

<https://www.toml-lint.com/>

## 현재 구축된 계층적 도구 체인
    
    
    Alacritty (터미널 에뮬레이터)
        └── tmux (터미널 멀티플렉서)
            └── shell (zsh/bash)
                └── 애플리케이션 (vim, git 등)

CLI 환경에서 여러 설정 값을 추가 하고 제외하다 보면 한 번쯤 고민하게 되는 부분이 있었습니다.

*** "도대체 어디에 뭘 쓰고 제외해야 하는거지?"***

제가 이러한 고민이 떠오른 이유는 그냥 몰라서 그런거죠! 🫠🫠. 그래서 알아봤습니다.

  * 이런 조사와 비교가 필요한 이유는 _Alacritty_와 _tmux_를 그냥 쓰면 **키바인딩 충돌이 발생** 하기 때문입니다. 즉 두 프로그램이 비슷한 기능(예: 복사/붙여넣기, 창 분할)을 제공할 때 키바인딩이 충돌할 수 있습니다. 따라서 각 도구의 역할을 명확히 구분할 필요가 있었습니다. 다만 개인적으로는 일단 _tmux_의 기능을 우선적으로 사용하는 것이 더 좋을 것 같네요.

  * _Alacritty_의 메인 기능을 기반으로 _tmux_의 기능을 비교하면서 어느 부분을 쓸지를 결정했습니다. <https://alacritty.org/index.html> ![](https://velog.velcdn.com/images/jlee38266/post/95cc98ad-23f1-43a9-8204-61adc98d7526/image.png)




## 기능 비교
    
    
    Alacritty              tmux
    -------------------------------
    Alt+Enter (전체화면)  | Ctrl+b z (창 확대/축소)
    Ctrl+Shift+c (복사)  | Ctrl+b [ (복사 모드)
    Alt+방향키 (탭 이동)  | Ctrl+b 방향키 (패널 이동)

### 1\. Vi Mode

Alacritty:

  * GPU 가속으로 더 부드러운 스크롤링과 선택
  * 터미널 자체 수준에서의 빠른 반응성
  * 시스템 클립보드와의 직접적인 통합



tmux:

  * Vi copy mode가 있지만 약간 덜 부드러움
  * 클립보드 통합이 시스템에 따라 추가 설정 필요



➡️ Alacritty의 Vi Mode로 선택 (Alacritty의 가장 매력적인 부분!)

### 2\. Search

Alacritty:

  * 현재 창에서만 동작
  * 세션 종료시 히스토리 손실



tmux:

  * 세션 간 검색 내용 유지
  * 검색 히스토리 관리
  * 정규식 검색 지원
  * 하이라이팅 기능



➡️ tmux 검색 기능을 쓸 듯?

### 3\. Regex Hints

Alacritty:

  * URL, IP 주소 등 실시간 감지
  * 마우스 호버 시 시각적 피드백
  * 키보드 기반 빠른 접근



tmux:

  * 기본적인 URL 선택 기능은 있음
  * 하지만 덜 직관적이고 설정이 복잡



➡️ Alacritty로 결정

### 4\. Multi-Window

Alacritty Multi-Window:

  * 단일 프로세스로 리소스 효율적
  * 하지만 세션 관리 기능 부족



tmux 장점:

  * 세션 유지 및 복구
  * 더 풍부한 창 관리 기능
  * 원격 접속시에도 안정적
  * 세션 공유 가능



➡️ tmux로 결정

### 기능 활용 정리 요약

> Vi Mode와 Regex Hints는 Alacritty의 기능을 사용

  * 더 부드럽고 반응성 좋은 사용자 경험
  * 시스템 통합이 더 자연스러움



> Search와 Multi-Window는 tmux 기능을 사용

  * 더 안정적인 세션 관리
  * 더 풍부한 검색 기능
  * 원격 작업시 안정성



### window 환경에서 alacritty setup
    
    
    # 1. %APPDATA% 경로로 이동 (보통 C:\Users\[사용자명]\AppData\Roaming)
    # Windows: %APPDATA%\alacritty\alacritty.toml
    cd $env:APPDATA
    
    # 2. alacritty 디렉토리가 있는지 확인
    dir alacritty
    
    # 3. alacritty 디렉토리 없다면 생성
    mkdir alacritty
    
    # 4. alacritty 디렉토리로 이동
    cd alacritty
    
    # 5. 현재 상태 확인 (alacritty.toml 파일 있는지)
    dir
    
    nvim alacritty.toml (없으면 생성하면서 편집기 열기, 선호하는 에디터 사용 ex: code, notepad)
    
    # 6. themes 디렉토리 클론
    git clone https://github.com/alacritty/alacritty-theme themes
    
    # 6-1.테마 저장소 업데이트하여 최신 테마 유지를 원할 때 (alacritty 디렉토리에 있을 때 & 어느 위치든 상관 없이 업데이트를 원할 때)
    cd themes && git pull && cd ..
    cd $env:APPDATA/alacritty/themes && git pull

#### directory structure

기본적인 디렉토리 및 파일 셋업이 끝나면 다음과 같은 구조를 갖게 됩니다.
    
    
    C:\Users\[사용자명]\AppData\Roaming\alacritty\
    ├── alacritty.toml
    └── themes\
        └── themes\
            ├── everforest_dark.toml
            └── [다른 테마 파일들...]