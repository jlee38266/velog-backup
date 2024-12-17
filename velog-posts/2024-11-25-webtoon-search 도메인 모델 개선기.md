---
_id: 66c1b094-9260-48e3-ba22-e1261a70cffd
date: '2024-11-25'
last_modified: '2024-12-17'
title: webtoon-search 도메인 모델 개선기
url: https://velog.io/@jlee38266/webtoon-search-도메인-모델-개선기
---

# 헥사고날 아키텍처와 팩토리 메소드 패턴 적용

_들어가며_

> 웹툰 검색 서비스를 토이 프로젝트를 개발하면서, 도메인 모델의 개선이 필요한 상황을 마주쳤습니다. 이 글에서는 기존 코드의 문제점을 파악하고, 헥사고날 아키텍처의 원칙에 맞춰 개선하는 과정을 공유하고자 합니다.

## 1. 기존 코드의 문제점

### 1.1 기존 도메엔 모델
```java
@Value
public class SearchableWebtoon {
    String id;
    String title;
    String provider;
    List<String> updateDays;
    String url;
    List<String> thumbnail;
    boolean isEnd;
    boolean isFree;
    boolean isUpdated;
    int ageGrade;
    Integer freeWaitHour;
    List<String> authors;

    // 비즈니스 메소드들
    public boolean isForAdults() {
        return ageGrade >= 19;
    }

    public boolean isFreeToRead() {
        return isFree || (freeWaitHour != null && freeWaitHour == 0);
    }

    public boolean isRecentlyUpdated() {
        return isUpdated && !isEnd;
    }
}
```

### 1.2 문제점들
1. 객체 생성 제어 부재
   - 누구나 새로운 `SearchableWebtoon` 객체를 자유롭게 생성할 수 있음
   - 객체 생성 시점에 유효성 검증이나 일관성 보장이 어려움
 2. 검색 성능 모니터링 메타데이터 부재
    - 검색 결과의 품질이나 성능을 측정할 수 있는 정보가 없음
    - 검색 점수, 응답 시간 등의 중요한 메트릭을 추적할 수 없음
    
## 2. 개선 방향
### 2.1 개선 목표
>  객체 생성 제어
> 검색 성능 모니터링 지원
> 헥사고날 아키텍처 원칙 준수

### 2.2 개선된 도메인 모델
```java
@Value
@Builder(access = AccessLevel.PRIVATE)  // 빌더 접근 제한
public class SearchableWebtoon {
    String id;
    String title;
    String provider;
    List<String> updateDays;
    String url;
    List<String> thumbnail;
    boolean isEnd;
    boolean isFree;
    boolean isUpdated;
    int ageGrade;
    Integer freeWaitHour;
    List<String> authors;
    
    // 검색 메타데이터 추가
    SearchMetadata searchMetadata;

    @Value
    @Builder
    public static class SearchMetadata {
        float score;         // 검색 점수
        long latency;        // 검색 소요시간 (ms)
        String matchedOn;    // 매칭된 필드
    }

    // 팩토리 메서드
    public static SearchableWebtoon createFrom(
            String id,
            String title,
            String provider,
            List<String> updateDays,
            String url,
            List<String> thumbnail,
            boolean isEnd,
            boolean isFree,
            boolean isUpdated,
            int ageGrade,
            Integer freeWaitHour,
            List<String> authors,
            float score,
            long latency,
            String matchedField) {
        // 객체 생성 로직
        return builder()
                .id(id)
                .title(title)
                // ... 필드 설정
                .searchMetadata(SearchMetadata.builder()
                        .score(score)
                        .latency(latency)
                        .matchedOn(matchedField)
                        .build())
                .build();
    }
}
````

## 3. 주요 개선 사항
### 3.1 팩토리 메소드 패턴 도입
- `@Builder(access = AccessLevel.PRIVATE`로 직접적인 빌더 사용 제한
- 팩토리 메소드를 통한 객체 생성으로 일관성 보장
- 객체 생성 로직을 한 곳에서 중앙 관리
  
### 3.2 검색 메타데이터 추가
- 검색 결과의 품질과 성능을 측정할 수 있는 메타데이터 도입
- `SearchMetaData` 내부 클래스로 관련 정보 캡슐화
- 검색 점수, 응담 시간, 매칭 필드 정보 포함

도메인 모델의 품질을 향상시키고, 검색 성능 모니터링을 위한 기반에 초점을 맞추기 위해, 과하지 않게 기능을 균형있게 구현하려고 합니다.