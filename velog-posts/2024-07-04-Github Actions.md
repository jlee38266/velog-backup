---
date: '2024-07-04'
last_modified: Thu, 04 Jul 2024 08:14:57 GMT
link: https://velog.io/@jlee38266/Github-Actions
tags: []
title: Github Actions
---

<h2 id="github-actions-프로젝트에-추가하기">Github Actions 프로젝트에 추가하기</h2>
<ul>
<li>현재 프로젝트를 진행하는 레포지토리에 깃허브 액션이 도입이 안되어 있다면 <code>Actions</code> 클릭을 통해 추가 가능.
<img alt="" src="https://velog.velcdn.com/images/jlee38266/post/4ddb169a-4b51-4faf-b8ca-27192028c281/image.png" /></li>
</ul>
<ul>
<li>직접 추가하지 않고 프로젝트에서 직접 추가하는 것도 가능
<img alt="" src="https://velog.velcdn.com/images/jlee38266/post/be8e5d32-0eb6-410a-8827-43aa083aca27/image.png" /></li>
</ul>
<p>root 디렉토리에서 <code>.github/workflows</code> (workflow에 s가 빠지면 안된다) 디렉토리 생성 후 <code>yml 파일</code>을 생성 하고 github에 코드가 <code>push</code>되면 포함되면 <strong>github action</strong>이 활성화</p>
<h2 id="github-action-구성-요소">Github Action 구성 요소</h2>
<p>Github action은 크게 세 가지 구성 요소를 가진다. - <strong>Workflow &gt; Job &gt; Step</strong></p>
<p><img alt="" src="https://velog.velcdn.com/images/jlee38266/post/b80eaf97-ade8-4db5-8026-7a2c70393b6d/image.png" />
<img alt="" src="https://velog.velcdn.com/images/jlee38266/post/cff01de9-d0be-42ab-8bca-4a5bdd9da1ee/image.png" /></p>
<p>On: 설정한 조건이 발동 하면 워크플로우를 실행
runs-on:  워크플로우를 실행하는 운영체제 환경</p>
<h2 id="java-기반으로-action-setup">Java 기반으로 action setup</h2>
<p><a href="https://github.com/actions/setup-java/blob/main/docs/advanced-usage.md#Amazon-Corretto">https://github.com/actions/setup-java/blob/main/docs/advanced-usage.md#Amazon-Corretto</a></p>
<p>(해당 Github Actions 공식 레포지토리를 통해 버전과 설정 예시 확인 가능)</p>
<p>깃허브 테스트를 위해서 글을 올려봅니다</p>