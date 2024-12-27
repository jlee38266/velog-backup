---
_id: 1389aac5-5a4b-4433-86f9-ef97096a1cf8
date: '2024-12-27'
last_modified: '2024-12-27'
title: (List vs Binary vs Hash)
url: https://velog.io/@jlee38266/List-vs-Binary-vs-Hash
---

# 파이썬 알고리즘: 검색 방식 비교 분석 

> 코딩 테스트나 실무에서 자주 사용되는 세 가지 검색 방식의 특징과 성능을 비교 분석

## 검색 방식별 특징 비교

각 검색 방식의 시간복잡도, 공간복잡도, 장단점을 비교

### List Search (순차 검색)
- **시간복잡도**: O(n*m)
- **공간복잡도**: O(1)
- **장점**
  - 구현이 매우 간단함
  - 작은 데이터셋에서 효율적
  - 추가 메모리가 필요 없음
- **단점**
  - 큰 데이터에서 매우 느림
  - 데이터가 증가하면 성능이 급격히 저하됨

### Binary Search (이진 검색)
- **시간복잡도**: O(m*log(m) + n*log(m))
- **공간복잡도**: O(1)
- **장점**
  - 중간 크기 데이터에서 효율적
  - 메모리 사용이 효율적
- **단점**
  - 정렬이 필요함
  - 구현이 비교적 복잡
  - 데이터 수정 시 재정렬 필요

### Hash Search (해시 테이블)
- **시간복잡도**: O(m + n)
- **공간복잡도**: O(m)
- **장점**
  - 대부분의 경우 가장 빠름
  - 구현이 간단
  - 데이터가 커져도 성능 유지
- **단점**
  - 추가 메모리 필요
  - 해시 충돌 가능성 있음

## 데이터 크기별 최적 구현

### 작은 데이터셋 (n < 100)
```python
def search_small_dataset(menus, orders):
    """리스트 검색이 가장 효율적"""
    for order in orders:
        if order not in menus:  # 단순하고 직관적
            return False
    return True
```

### 중간 데이터셋 (100 ≤ n < 10000)
```python
def search_medium_dataset(menus, orders):
    """상황에 따라 리스트 검색 또는 해시 검색"""
    # 메모리가 중요하다면 리스트 검색
    # 성능이 중요하다면 해시 검색
    menus_set = set(menus)  # 해시 검색 권장
    return all(order in menus_set for order in orders)
```

### 큰 데이터셋 (n ≥ 10000)
```python
def search_large_dataset(menus, orders):
    """해시 검색이 압도적으로 유리"""
    menus_set = set(menus)  # 필수적으로 해시 테이블 사용
    return all(order in menus_set for order in orders)
```

## 실제 성능 테스트

실제 데이터로 테스트해본 결과

### 작은 데이터셋 (메뉴 5개, 주문 3개)
```
List Search:   0.000308ms (가장 빠름)
Binary Search: 0.001237ms
Hash Search:   0.000398ms
```

### 큰 데이터셋 (메뉴 10000개, 주문 100개)
```
List Search:   7.252239ms
Binary Search: 1.871406ms
Hash Search:   0.630629ms (가장 빠름)
```

## 전체 구현 코드

각 검색 방식의 전체 구현 코드

```python
import time
import random
import string
from typing import List, Set


def generate_random_menu(length=8):
    """랜덤한 메뉴 이름 생성"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


# 테스트용 데이터
SMALL_MENU_COUNT = 5
SMALL_ORDER_COUNT = 3
LARGE_MENU_COUNT = 10000
LARGE_ORDER_COUNT = 100

# 작은 데이터셋
small_menus = [generate_random_menu() for _ in range(SMALL_MENU_COUNT)]
small_orders = random.sample(small_menus, SMALL_ORDER_COUNT)
small_orders_with_invalid = small_orders + [generate_random_menu()]


def search_list(menus: List[str], orders: List[str]) -> bool:
    """리스트 순차 검색을 사용한 주문 가능 여부 확인

    시간복잡도: O(n*m), 여기서 n은 orders의 길이, m은 menus의 길이
    공간복잡도: O(1), 추가 공간 필요 없음
    """
    for order in orders:
        if order not in menus:
            return False
    return True


def search_binary(menus: List[str], orders: List[str]) -> bool:
    """이진 검색을 사용한 주문 가능 여부 확인

    시간복잡도: O(m*log(m) + n*log(m)), 여기서 n은 orders의 길이, m은 menus의 길이
    공간복잡도: O(1), 정렬이 in-place로 수행된다고 가정
    """
    menus.sort()  # 이진 검색을 위한 정렬

    def binary_search(target: str, array: List[str]) -> bool:
        start = 0
        end = len(array) - 1

        while start <= end:
            mid = (start + end) // 2
            if array[mid] == target:
                return True
            elif array[mid] < target:
                start = mid + 1
            else:
                end = mid - 1
        return False

    for order in orders:
        if not binary_search(order, menus):
            return False
    return True


def search_hash(menus: List[str], orders: List[str]) -> bool:
    """해시 테이블(Set)을 사용한 주문 가능 여부 확인

    시간복잡도: O(m + n), 여기서 n은 orders의 길이, m은 menus의 길이
    공간복잡도: O(m), 메뉴 리스트를 저장할 추가 공간 필요
    """
    menus_set = set(menus)
    for order in orders:
        if order not in menus_set:
            return False
    return True


def measure_time(func, menus, orders, iterations=1000):
    """함수의 실행 시간을 측정"""
    total_time = 0
    for _ in range(iterations):
        # 매 반복마다 새로운 메뉴 리스트 복사 (원본 보존)
        menus_copy = menus.copy()
        start_time = time.time()
        func(menus_copy, orders)
        end_time = time.time()
        total_time += (end_time - start_time)
    return (total_time / iterations) * 1000  # 밀리초 단위 변환


def run_performance_test(menus: List[str], orders: List[str], dataset_name: str):
    """성능 테스트 실행 및 결과 출력"""
    print(f"\n=== {dataset_name} ===")
    print(f"메뉴 개수: {len(menus)}, 주문 개수: {len(orders)}")

    # 정확성 테스트
    print("\n정확성 테스트 (유효한 주문):")
    print(f"List Search:   {search_list(menus.copy(), orders)}")
    print(f"Binary Search: {search_binary(menus.copy(), orders)}")
    print(f"Hash Search:   {search_hash(menus.copy(), orders)}")

    # 잘못된 주문 테스트
    invalid_orders = orders + [generate_random_menu()]
    print("\n정확성 테스트 (잘못된 주문):")
    print(f"List Search:   {search_list(menus.copy(), invalid_orders)}")
    print(f"Binary Search: {search_binary(menus.copy(), invalid_orders)}")
    print(f"Hash Search:   {search_hash(menus.copy(), invalid_orders)}")

    # 성능 테스트
    print("\n성능 테스트 (평균 실행 시간):")
    list_time = measure_time(search_list, menus, orders)
    binary_time = measure_time(search_binary, menus, orders)
    hash_time = measure_time(search_hash, menus, orders)

    print(f"List Search:   {list_time:.6f}ms")
    print(f"Binary Search: {binary_time:.6f}ms")
    print(f"Hash Search:   {hash_time:.6f}ms")


if __name__ == "__main__":
    # 작은 데이터셋 테스트
    run_performance_test(small_menus, small_orders, "작은 데이터셋 테스트")

    # 큰 데이터셋 테스트
    large_menus = [generate_random_menu() for _ in range(LARGE_MENU_COUNT)]
    large_orders = random.sample(large_menus, LARGE_ORDER_COUNT)
    run_performance_test(large_menus, large_orders, "큰 데이터셋 테스트")
```

## 적용시 고려사항

### 1. 데이터 크기에 따른 선택
- 작은 데이터: 가장 단순한 방식 선택 (List Search)
- 큰 데이터: 최적화된 자료구조 사용 (Hash Search)
- 메모리 제약 있음: Binary Search 고려

### 2. 최적화 전략
1. 먼저 가장 단순한 해결책으로 시작
2. 성능 문제 발생 시 점진적 최적화
3. 실제 데이터로 반드시 테스트

### 3. 주의사항
- 과도한 최적화는 피하기
- 코드 가독성과 유지보수성 고려
- 실제 사용 패턴 분석 필요

## 결론

- 각 검색 방식은 상황에 따른 장단점이 있음
- 데이터 크기와 메모리 제약을 고려하여 선택
- 실제 환경에서는 해시 검색이 대부분 최적
- 단, 작은 데이터에서는 단순한 방식이 더 효율적