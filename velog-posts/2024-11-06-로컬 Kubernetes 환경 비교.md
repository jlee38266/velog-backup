---
date: '2024-11-06'
last_modified: '2024-11-07'
link: https://velog.io/@jlee38266/%EB%A1%9C%EC%BB%AC-Kubernetes-%ED%99%98%EA%B2%BD-%EB%B9%84%EA%B5%90
series_name: GitHub Actions
series_order: 2/2
tags:
- kubernetes
title: 로컬 Kubernetes 환경 비교
---

로컬 Kubernetes 환경을 선택할 때 고려할 주요 요소들을 정리했습니다. Docker Desktop Kubernetes, Minikube, k3d의 주요 차이점은 다음과 같습니다.

항목 | Docker Desktop Kubernetes | Minikube | k3d  
---|---|---|---  
**구성 방식** | Docker 내장 Kubernetes | VM 또는 Docker 컨테이너 | Docker 컨테이너 기반 K3s  
**설정 편의성** | 매우 간단 | 다소 복잡 | 간단  
**리소스 사용** | 보통 | 높음 | 낮음  
**클러스터 속도** | 빠름 | 비교적 느림 | 매우 빠름  
**Kubernetes 완전성** | 표준 Kubernetes | 표준 Kubernetes | 경량화된 Kubernetes  
  
## 각 로컬 Kubernetes 환경의 특징

### Docker Desktop Kubernetes

  * **구성 방식** : Docker Desktop에 내장된 Kubernetes를 사용하여 별도 설치 과정 없이 바로 Kubernetes를 활성화할 수 있습니다.
  * **설정 편의성** : 매우 간단하게 설정 가능하며, Docker Desktop UI에서 쉽게 Kubernetes 기능을 활성화할 수 있습니다.
  * **적합한 경우** : 빠르게 Kubernetes 환경을 시작하고 싶은 경우나 가벼운 개발 환경에 적합합니다.



### Minikube

  * **구성 방식** : Minikube는 VM 또는 Docker 컨테이너를 이용해 Kubernetes 클러스터를 생성합니다.
  * **리소스 사용** : VM 기반으로 동작하는 경우가 많아 상대적으로 높은 리소스를 소비합니다.
  * **적합한 경우** : Kubernetes 클러스터와 동일한 VM 기반의 환경에서 네트워크와 스토리지를 보다 유사하게 테스트하고자 할 때 적합합니다.



### k3d

  * **구성 방식** : Docker 컨테이너 기반으로, 경량화된 Kubernetes 배포판인 K3s를 사용합니다.
  * **설정 편의성** : 가볍고 설치가 간편하며, 멀티 노드를 빠르게 구성할 수 있어 반복적인 테스트에 유리합니다.
  * **적합한 경우** : 빠른 배포 및 테스트가 필요한 CI/CD 환경, ArgoCD와 연동하여 GitOps 파이프라인을 테스트하고자 할 때 특히 유용합니다.