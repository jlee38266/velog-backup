---
date: '2024-11-07'
last_modified: '2024-11-19'
link: https://velog.io/@jlee38266/Local-Monitoring-System-Setup
tags:
- devops
- monitoring
---

WSL2 환경에서 k3d와 Tilt를 활용하여 구현된 애플리케이션의 모니터링 시스템을 구축하는 과정을 기록합니다.

목표

  * k3d, Tilt, Prometheus, Grafana를 활용한 모니터링 시스템 구축
  * springboot로 구현한 코드를 테스트베드로 활용
  * 간단한 모니터링 시스템 구축에 초점



개발 환경

  * OS: WSL2(Ubuntu-24.04)
  * Container: Window Docker Desktop과 통합
  * 기타 도구: k3d, Tilt, kubectl


  1. 사전 준비 및 환경 확인 윈도우 환경에서 리눅스를 쓰기위한 환경이 설정되어 있는지 확인합니다 ![](https://velog.velcdn.com/images/jlee38266/post/0e78c2e2-d5eb-4e26-ac12-b7871df18b15/image.png)