---
_id: 641c6bd2-6074-49b2-b57e-bbf24e5fc556
date: '2024-11-16'
last_modified: '2024-11-23'
title: WSL and python Env Conflicts in Pycharm (제목 변경)
url: https://velog.io/@jlee38266/WSL-and-python-Env-Conflicts-in-Pycharm-제목-변경
---

# 테스트용 내용 추가

![](https://velog.velcdn.com/images/jlee38266/post/9053f329-8c2a-4347-969e-d34bceb883d2/image.png)

![](https://velog.velcdn.com/images/jlee38266/post/ca093ed4-10ec-4ebd-aded-454ea7ca19fd/image.png)

1. `can't change option: zle`
- 주 원인: Oh My Zsh와 관련 플러그인들의 셸 확장 기능
- 특히 다음 플러그인들이 관련됨:
```
zshCopyplugins=(
    zsh-autosuggestions     # 자동 완성 기능
    zsh-syntax-highlighting # 문법 강조 기능
)
```

2. `can't change option: monitor`
- 주 원인: Zsh의 job control 기능 설정
- .zshrc에서 기본적으로 설정되는 interactive 셸 옵션

3. `gitstatus failed to initialize`
- 주 원인: Powerlevel10k의 git 상태 표시 기능
```
zshCopyZSH_THEME="powerlevel10k/powerlevel10k"
```

따라서 맞습니다. p10k와 Oh My Zsh 관련 설정들이 없었다면 이러한 오류들은 발생하지 않았을 것입니다. 하지만 이는 트레이드오프입니다:
```
bashCopy# 장점 있는 설정들
- p10k: 강력한 프롬프트 기능
- zsh-autosuggestions: 편리한 자동 완성
- zsh-syntax-highlighting: 가독성 높은 문법 강조

# VS

# 발생하는 문제
- IDE 통합 시 non-interactive 셸 관련 오류
- 초기화 과정에서의 경고 메시지
실제 개발 생산성 측면에서는 이러한 도구들의 이점이 훨씬 크기 때문에, 앞서 제안된 non-interactive 셸 관련 설정을 추가하는 것이 좋은 해결책입니다.
```

```
1단계: PyCharm → WSL Python 인터프리터 설정 시도
├── PyCharm: "WSL의 Python 경로가 필요하네. which python3를 실행해야겠다"
└── 명령 실행: /usr/bin/which python3

2단계: WSL에서 명령 실행
├── 기본 셸(zsh)로 명령 실행 시도
└── .zshrc 로드 시작

3단계: .zshrc 설정 로드 시도
├── Powerlevel10k instant prompt 초기화
├── Oh My Zsh 로드
└── 플러그인 초기화 시도

4단계: 여기서 문제 발생!
├── zsh-autosuggestions가 ZLE(Zsh Line Editor) 초기화 시도
│   └── ERROR: can't change option: zle
│       (이유: non-interactive 환경에서는 라인 편집 기능 불가능)
│
├── Oh My Zsh가 job control 설정 시도
│   └── ERROR: can't change option: monitor
│       (이유: non-interactive 환경에서는 작업 제어 불가능)
│
└── Powerlevel10k가 gitstatus 초기화 시도
    └── ERROR: gitstatus failed to initialize
        (이유: git 상태 모니터링은 interactive 환경 필요)

5단계: 그럼에도 불구하고 명령은 실행됨
├── which python3 명령 실행 성공
└── 결과: /usr/bin/python3 반환
```

문제가 발생하는 핵심 이유:
```
pythonCopy# 일반적인 터미널 사용 시 (Interactive)
터미널 → zsh 시작 → .zshrc 로드 → 모든 기능 정상 작동
                                   (프롬프트, 자동완성, git 상태 등)

# IDE에서 명령 실행 시 (Non-interactive)
IDE → zsh 시작 → .zshrc 로드 시도 → 터미널 기능 초기화 실패
                                   (터미널이 필요없는데 초기화하려 함)
```

이를 방지하기 위한 코드의 동작:
```
zshCopy# .zshrc 최상단
[[ $- != *i* ]] && return

# 의미: 
# 1. $-: 현재 셸의 옵션 플래그 확인
# 2. *i*: interactive 플래그 찾기
# 3. !=: interactive 플래그가 없으면
# 4. return: 더 이상의 .zshrc 실행을 중단
```
이렇게 하면 non-interactive 모드에서는 불필요한 초기화를 시도하지 않게 됩니다.


Interactive 셸과 Non-interactive 셸의 차이를 실제 예시로 설명드리겠습니다:

1. Interactive 셸 상황:

```
Copy# 터미널을 열고 직접 명령어를 입력하는 상황
$ ls
Documents  Downloads  
$ pwd
/home/user

# 이때 작동하는 interactive 셸 기능들:
- 명령어 자동완성 (Tab키)
- 명령어 프롬프트 표시 (Powerlevel10k)
- 문법 강조 표시
- 명령어 히스토리 (위/아래 화살표)
```

2. Non-interactive 셸 상황:

```
Copy# PyCharm이 Python 경로를 찾기 위해 실행하는 명령
$ which python3

# 이때는 필요하지 않은 것들:
- 프롬프트 표시 ❌
- 자동완성 ❌
- 문법 강조 ❌
```

문제가 발생하는 상황을 예시로 들면:
```bash
Copy# .zshrc에서 interactive 셸 기능을 설정
zle-line-init() {
    echo "새 명령줄 시작!"
}
zle -N zle-line-init

# PyCharm이 which python3를 실행할 때:
ERROR: can't change option: zle
# → "명령줄 시작 알림" 같은 interactive 기능이 
#   필요없는 상황인데 설정하려고 해서 오류 발생
```

쉽게 비유하면:
- Interactive 셸 = 레스토랑에서 직접 주문하고 서비스 받기
  - 메뉴판 필요
  - 웨이터 서비스 필요
  - 테이블 세팅 필요

- Non-interactive 셸 = 배달 주문
  - 메뉴판 불필요 ❌
  - 웨이터 서비스 불필요 ❌
  - 테이블 세팅 불필요 ❌
  - 음식만 있으면 됨

따라서 "배달"인 상황에서 "웨이터 서비스"를 설정하려고 할 때 오류가 발생하는 것과 같습니다.