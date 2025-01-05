---
_id: bce9cc4e-49bd-4481-b5cd-0dd958261e79
date: '2024-08-02'
title: Docker를 이용한 Terraform 환경 설정 및 AWS 리소스 관리
url: https://velog.io/@jlee38266/Docker를-이용한-Terraform-환경-설정-및-AWS-리소스-관리
---

```bash
# zshell 스크립트 수정 에디터 열기
nano ~/.zshrc

# 해당 세션에 적용시키기
source ~/.zshrc
```
### Neovim 활용시 (선택사항)
이 가이드에서는 Neovim(nvim)을 텍스트 에디터로 사용. 설치되어 있지 않다면 다음 방법으로 설치:


```bash
# Ubuntu/Debian
sudo apt update
sudo apt install neovim

## 설치 확인
nvim --version

nvim ~/.zshrc

####### 다른 OS 활용 시#######
# macOS(Homebrew 사용)
brew install neovim

# windows(Chocolatey 사용)
choco install neovim
#############################

```

### Neovim 사용 팁

1. 입력 모드로 전환: `i` 키
2. 명령 모드로 돌아가기: `Esc` 키
3. 저장하고 종료하기: 명령 모드에서 `:wq`를 입력하고 Enter
4. 저장하지 않고 종료하기: 명령 모드에서 `:q!`를 입력하고 Enter
(Neovim에 익숙하지 않다면, `vimtutor` 명령어로 기본적인 사용법을 배울 수 있음)

## 0. AWS CLI 설정
새로운 AWS 프로필을 설정하거나 기존 프로필을 수정:

```bash
# 해당 명령어와 함께 profile 이름을 넣어면 이걸 기반으로 새롭게 profile을 만들 수 있음
# 이 명령어 이후 aws credencials를 입력하는 프롬프트가 표시됨
aws configure --profile samsamohoh-infra-terraform

# 이후 표시되는 옵션들:
# AWS Access Key ID: (AWS에 액세스하기 위한 access key를 입력)

# AWS Secret Access Key: (access key와 함께 사용되는 비밀 키를 입력)

# Default region name: (사용하고자 하는 기본 리전 - 예: us-west-2, ap-northeast-2을 입력)

# Default output format: (AWS CLI 명령어의 출력 형식을 설정 - 예: json, text, table)
#
```

## 1. Terraform Docker Alias 설정

`.zshrc` 파일에 다음 alias를 추가. 이를 통해 로컬에 Terraform을 설치하지 않고도 Docker를 통해 Terraform을 실행 가능.

### AWS_PROFILE 환경변수만으로 자격 증명이 안됨 🤔
> 
- --rm 옵션 때문에 terraform 명령이 종료되면 컨테이너가 즉시 삭제됨
- hashicorp/terraform 도커 이미지는 aws cli를 포함한 이미지가 아님
- aws cli가 없기 때문에 ~/.aws/credentials 을 volume에 마운트 하더라도 직접 읽어 오지 못함

_이것 때문에 aws cli 포함된 terraform image를 쓸까 고민하다가 설정 관리에 피로함을 느낌._
```bash
# profile만 활용해서 자격증명까지 되기를 기대했으나...도커는 호락호락 하지 않음
alias terraform='docker run --rm -it \
  -v "$(pwd):/workspace" \
  -v "${HOME}/.aws:/root/.aws" \
  -e AWS_PROFILE \
  -w /workspace \
  hashicorp/terraform:${TF_VERSION}'
```

그래서 아래와 같이 자격 증명 및 프로필 관련 코드를 하드코딩:

```bash
# 현재는 하드코딩으로 access key & secret access key를 각각 등록
# Terraform 버전 설정
export TF_VERSION=1.9.3

# AWS Profile 설정
export AWS_PROFILE=samsamohoh-infra-terraform

# Profile에서 AWS credentials(자격 증명)을 환경 변수로 가져오기
# - AWS CLI가 지정된 프로파일(AWS_PROFILE)에서 credentials를 읽어옴
# - 자격 증명을 Docker 컨테이너에 전달하기 위해 환경 변수로 설정
export AWS_ACCESS_KEY_ID=$(aws configure get ${AWS_PROFILE}.aws_access_key_id)
export AWS_SECRET_ACCESS_KEY=$(aws configure get ${AWS_PROFILE}.aws_secret_access_key)
export AWS_DEFAULT_REGION=$(aws configure get ${AWS_PROFILE}.region)

# Terraform alias 설정
alias terraform='docker run --rm -it \
  -v "$(pwd):/workspace" \                 # 현재 디렉토리를 컨테이너의 /workspace에 마운트
  -v "${HOME}/.aws:/root/.aws" \           # 로컬 ~/.aws 디렉토리를 컨테이너의 /root/.aws에 마운트
  -e AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \          # AWS Access Key 환경 변수 전달
  -e AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \  # AWS Secret Access Key 환경 변수 전달
  -e AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION}" \        # AWS Region 환경 변수 전달
  -w /workspace \                                        # 작업 디렉토리를 /workspace로 설정
  --user "$(id -u):$(id -g)" \                      # 컨테이너를 현재 호스트 사용자의 UID:GID로 실행 (설정하지 않으면 root로 되어 Permission denied 때문에 미리 방지)
  hashicorp/terraform:${TF_VERSION}'
```  

## 2. 유용한 함수 추가
AWS 프로필과 Terraform 버전을 쉽게 전환할 수 있는 함수를 .zshrc 파일에 추가

```bash
# Terraform 버전 전환 함수
tf_version() {
    if [ $# -eq 0 ]
        then
            echo "Current Terraform version: $TF_VERSION"
        else
            export TF_VERSION=$1
            echo "Terraform version set to $TF_VERSION"
    fi
}
```

## 3. 설정 확인 및 테스트
설정이 올바르게 되었는지 확인:
```bash
# AWS 설정 확인
aws configure list

# AWS 자격 증명 테스트
aws sts get-caller-identity

# 환경 변수 확인
echo $AWS_PROFILE

# 자격 증명 파일 직접 확인
cat ~/.aws/credentials

# alias 설정 확인
alias terraform
```

## 4. Terraform 프로젝트 구조 예시
프로젝트 디렉토리에 다음 파일들을 생성:
- main.tf: 주요 리소스 정의
- variables.tf: 변수 정의
- outputs.tf: 출력 정의
- versions.tf: Terraform 및 provider 버전 정의

main.tf 예시
```bash
hclCopyprovider "aws" {
  region  = var.region
  profile = "samsamohoh-infra-terraform"
}

# 나머지 리소스 정의...
```

versions.tf 예시
```bash
hclCopyterraform {
  required_version = ">= 1.3"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.30"
    }
  }
}
```
## 5. Terraform 명령어 실행
프로젝트 디렉토리에서 다음 명령어를 실행:
```bash
# 초기화
terraform init

# 계획 생성
terraform plan

# 변경 사항 적용
terraform apply
```

> ⚠️ 주의사항
- 해당 설정을 쓰게 되는 경우 Docker를 사용하므로 local에 Terraform을 설치하면 docker와 local 중 어디를 기준으로 명령어가 전달되는지 명확하지 않을 수 있음 (물론 alias을 바꾸면 해결되긴 함)
- WSL2를 사용하는 경우 경로 문제에 주의 필요.

## 6. 결론
- 처음 terraform을 설치하는 것보다 docker를 쓰면 편하지 않을까 했지만, 생각보다 명령어에 관련된 설정을 만들지 않으면 굉장히 불편하다는 점
- 실제 prod 환경인 aws 같은 서비스를 이용할 때는 자격 증명과 더불어 고려해야 하는 부분들이 많아짐 (docker image를 처음부터 aws cli가 탑재된 것 활용하거나, 하드 코딩으로 자격 증명이 될 수 있도록 신경써야 하는점)
- terraform의 버전 차이에 따른 테스트를 한다던지, 팀원간의 버전을 모두 통일해야 하는 상황이라면 써봄직 한 것 같음
- terraform의 버전 차이로 호환성 검증을 진행하는게 아니라면 docker로 terraform을 쓰는건 불편함

### 로컬에 terraform 설치
- [Terraform Install](https://developer.hashicorp.com/terraform/install)
- [Terraform CLI로만 다운받는 tutorial](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)