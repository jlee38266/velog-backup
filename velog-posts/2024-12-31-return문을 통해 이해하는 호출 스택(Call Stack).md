---
_id: ed516d98-18a3-4da2-89a4-cd5bfad4d612
date: '2024-12-31'
title: return문을 통해 이해하는 호출 스택(Call Stack)
url: https://velog.io/@jlee38266/호출-스택Call-Stack-이해
---

## Call Stack
콜 스택은 프로그램이 함수 호출을 추적하고 관리하는 데이터 구조 (재귀 함수의 동작을 이해하는 데 매우 중요).

#### 콜 스택의 주요 기능
- 함수 호출의 순서 관리
- 각 함수의 지역 변수와 매개변수 저장
- 함수 종료 후 돌아갈 위치(반환 주소) 저장
- 함수의 실행 컨텍스트 유지

## 실제 예시로 확인하는 콜 스택

#### 스택 프레임의 구성요소
- 매개변수 값
- 지역 변수들
- 반환 주소 (돌아갈 위치)
- 반환값 저장 공간

#### 팩토리얼 계산에서의 호출 스택 활용
```python
def factorial(n):
    # 스택 프레임 생성 (매개변수 n, 반환 주소 저장)
    if n == 1:
        return 1  # 여기서 스택 프레임이 해제, 1 반환
    
    # 재귀 호출 (새로운 스택 프레임 생성)
    result = n * factorial(n - 1)  
    return result  # 현재 스택 프레임 해제, 계산 결과 반환
    
    """
    # 스택의 동작 설명
    
    factorial(3) 호출 시:
    [스택]
    +------------------+
    | n = 3           |  <- factorial(3) 프레임
    +------------------+
    
    factorial(2) 호출 시:    
    +------------------+
    | n = 2           |  <- factorial(2) 프레임
    +------------------+
    | n = 3           |  <- factorial(3) 프레임 (대기)
    +------------------+
    
    factorial(1) 호출 시:
    +------------------+
    | n = 1           |  <- factorial(1) 프레임
    +------------------+
    | n = 2           |  <- factorial(2) 프레임 (대기)
    +------------------+
    | n = 3           |  <- factorial(3) 프레임 (대기)
    +------------------+
    
    return 시작:
    1. factorial(1) 반환: 1
    2. factorial(2) 계산: 2 * 1 = 2
    3. factorial(3) 계산: 3 * 2 = 6
    """
```
이 예시에서 return을 만나면 해당 프레임이 제거 되면서 이전 호출로 결과값을 전달

## Java vs Python에서의 콜 스택
#### 1. Java의 특징
- 메소드 선언 시 반환 타입 명시 필수 (void, int, String 등)
- void 키워드로 반환값 없음을 명시
- 컴파일 시점에서의 엄격한 타입 체크 (초기에 많은 오류를 잡아낼 수 있음)
- 컴파일 시점에 메모리 크기 예측 가능
- 명시적인 스택 크기 제한 설정 가능

```java
public class RecursiveExample {
    public int factorial(int n) {
        if (n == 1) {
            return 1;  // 명시적 반환 필수
        }
        return n * factorial(n - 1);
    }
    
    public void printMessage() {  // void로 반환 없음 명시
        System.out.println("Hello");
        return;  // 생략 가능
    }
}
```

```java
public int mustReturnSomething() {
    if (condition) {
        return 42;
    }
    // 컴파일 에러, 모든 경로에서 반환값이 필요
}
```

```java
// Java의 return
public class ReturnExample {
    // 명시적 반환 타입 필수
    public int singleReturn() {
        int a = 1;
        int b = 2;
        return a + b;    // a, b 변수가 스택에서 해제되고
                        // 결과값 3이 호출자의 스택으로 복사
    }

    // 다중 반환을 위해선 객체나 배열 사용 필요
    public Pair<Integer, Integer> multipleReturn() {
        return new Pair<>(1, 2);
    }
}
```

#### 2. Python의 특징
- 반환 타입 명시 불필요 (선택사항)
- 동적 타입 시스템 (런타임에 타입이 결정됨)
- 유연한 반환값 처리
- 런타임에 메모리 할당 결정
- 스택 크기 자동 조절

```python
def factorial(n):
    if n == 1:
        return 1 # 타입 명시 불필요
    return n * factorial(n-1)
    
def flexible_return():
    if condition:
        return 42 # 숫자 반환
    return "Hello World!" # 문자열 반환도 가능
```

```python
# Python의 return
def single_return():
    a = 1
    b = 2
    return a + b    # Java와 동일한 스택 메모리 처리

def multiple_return():
    return 1, 2     # 튜플로 자동 패킹 (1,2) 되어 반환

# 암시적 return (Java에는 없음)
def implicit():
    pass    # return None 자동 추가

"""
# 참고
tuple은 java에는 없는 자료형으로 리스트 [] 와 다르게 () 형태로 저장되며 주요 차이점은
- 리스트는 mutable (수정 가능)
- 튜플은 immutable(수정 불가)

# 리스트는 수정 가능
list_ex[0] = 10  # OK

# 튜플은 수정 불가
tuple_ex[0] = 10  # TypeError 발생
"""
```

## return의 역할과 콜 스택
#### 실행 시 일어나는 일
- 현재 스택 프레임의 메모리 해제 (함수 종료)
- 반환값이 이전 스택 프레임으로 복사
- 프로그램 카운터가 반환 주소로 이동
- 제어권의 반환(이전 호출 지점으로 돌아가기 or 이전 함수의 실행 컨텍스트 복원)

```python
def get_all_ways_by_doing_plus_or_minus(array, current_index, current_sum):
    # 1️⃣ 첫 번째 호출
    # current_index=0, current_sum=0
    
    # 2️⃣ 두 번째 호출 (+2 케이스)
    # current_index=1, current_sum=2
    
    # 3️⃣ 세 번째 호출 (+3 케이스)
    # current_index=2, current_sum=5
    
    # 4️⃣ 네 번째 호출 (+1 케이스)
    # current_index=3, current_sum=6
    if current_index == len(array):  # True -> array = [2, 3, 1]
        all_ways.append(current_sum)  # 6을 추가
        return  # ⬅️ 여기서 return하면
               # 자동으로 3️⃣번 호출로 돌아감!
```

### 주의사항
- 재귀가 깊어지면 스택 오버플로우 발생 가능
- 각 언어별 스택 크기 제한 확인 필요
- 메모리 사용량 고려한 설계 필요

### 정리
- 콜 스택은 Java나 Python 등 언어에 관계없이 동일한 원리로 작동
- 차이점은 각 언어의 특성과 철학에 따른 구현 방식의 차이일 뿐, 기본 개념은 동일
  1. 함수 호출이 스택에 쌓임
  2. return을 만나면 현재 함수가 스택에서 제거
  3. 제어권이 이전 함수 호출로 돌아감
  4. 반환된 값을 이용해 계산을 계속 진행
- 재귀 함수는 호출 스택을 활용한 대표적인 예시 (DFS를 구현하는 핵심 메커니즘)