---
_id: 443c368a-c428-454a-b321-39e7e0992658
date: '2025-03-16'
title: Mechanical Properties of Metals (ch.6)
url: https://velog.io/@jlee38266/Mechanical-Properties-of-Materials
---

# 1. Mechanical Properties
1. **Stiffness(강성)**: The ability of a material to resist deformation under load. Material with high stiffness undergo small deformations when subjected to loads. It is measured by Young's moduldus; the higher the value, the greater the stiffness. (변형에 저항하는 재료의 능력입니다. 강성이 높은 재료는 하중을 받을 때 변형이 적습니다. 영률(Young's modulus)로 측정되며, 값이 클수록 강성이 높습니다.)

2. **Strength(강도)**: The maximum stress a material can withstand before failure. Yield strength refers to the point where permanent deformation begins, while tensile strength is the maximum stress a material can withstand before fracture. (재료가 파괴되기 전에 견딜 수 있는 최대 응력입니다. 항복 강도는 영구 변형이 시작되는 지점을, 인장 강도는 재료가 파단되기 전 견딜 수 있는 최대 응력을 의미합니다.)

3. **Hardness(경도)**: The resistance of material's surface to scratching, indentation, and wear. It is measured through hardness tests such as Brinell, Rockwell, and Vickers. (재료의 표면이 긁힘, 압입, 마모에 저항하는 능력입니다. 브리넬, 로크웰, 비커스 등의 경도 시험으로 측정됩니다.)

4. **Ductility(연성)**: The ability of a material to undergo plastic deformation without breaking. Highly ductile materials fracture only after signigicant deformation when stretched. It is measured as percent elongation. (재료가 파괴 없이 소성 변형할 수 있는 능력입니다. 연성이 높은 재료는 인장 시 상당한 변형 후에 파단됩니다. 연신율(%)로 측정됩니다.)

5. **Toughness(인성)**: The ability of a material to absorb energy before fractrue. It is a combination of strength and ductility, and is crucial for resisting impact loads. Toughness is measured through impact tests or as the area under the stress-strain curve. (재료가 파괴 전에 에너지를 흡수할 수 있는 능력입니다. 강도와 연성의 조합으로, 충격 하중에 저항하는 중요한 특성입니다. 충격 시험이나 응력-변형률 곡선의 면적으로 측정됩니다.)

These properties are critical for material selection and design, with different applications requiring different property combinations.

# 2. Elongation
신장률(elongation)은 재료가 인장 응력을 받을 때 발생하는 길이 증가를 나타내는 중요한 기계적 특성입니다. 일반적으로 백분율로 표시하며, 다음과 같이 계산합니다:

% 신장률 = [(최종 길이 - 원래 길이) / 원래 길이] × 100%

항공 엔지니어링 관점에서 신장률은 다음과 같은 중요한 의미를 가집니다:

1. 연성의 지표: 높은 신장률은 재료가 파단 전에 상당한 소성 변형을 견딜 수 있음을 의미합니다. 항공 구조물에서는 재료가 갑작스럽게 파단되기보다 눈에 보이는 변형을 통해 경고 신호를 제공하는 것이 안전성 측면에서 중요합니다.
2. 재료 선택: 항공기 부품은 사용 위치에 따라 다른 신장률 요구사항을 가질 수 있습니다. 예를 들어, 주요 구조 부재는 일정 수준의 연성(따라서 적절한 신장률)이 필요한 반면, 일부 비구조적 부품은 다른 특성이 더 중요할 수 있습니다.
3. 피로 특성과의 관계: 신장률과 같은 연성 특성은 종종 재료의 피로 거동과 관련이 있습니다. 적절한 연성을 가진 재료는 응력 집중을 더 잘 완화시킬 수 있어 피로 수명이 향상될 수 있습니다.

실제 항공 재료의 예시 신장률:

- 항공용 알루미늄 합금 2024-T3: 약 10-15%
- 항공용 티타늄 합금 Ti-6Al-4V: 약 10-14%
- 고강도 강철 AISI 4340: 약 12-17%
- 탄소 섬유 복합재: 일반적으로 1-2% 미만(매우 낮음)

이러한 신장률 값은 재료의 처리 상태, 시험 조건, 그리고 정확한 합금 조성에 따라 달라질 수 있습니다

# 3. 공학적 응력과 변형률의 이해

## 공학적 응력(Engineering Stress)

재료가 받는 힘을 단면적으로 나눈 값으로, 재료가 견디는 단위 면적당 힘을 의미합니다.

```
σ = F/A₀
```

여기서:
- σ (시그마): 공학적 응력
- F: 가해지는 힘(하중)
- A₀: 원래 단면적(변형 전)

**단위**: 
- SI: MPa (메가파스칼, 1 MPa = 10⁶ Pa)
- 미국식: psi (pounds per square inch)

## 공학적 변형률(Engineering Strain)

재료의 길이 변화를 원래 길이로 나눈 값으로, 상대적인 길이 변화를 나타냅니다.

```
ε = (l - l₀)/l₀ = Δl/l₀
```

여기서:
- ε (엡실론): 공학적 변형률
- l: 현재 길이
- l₀: 원래 길이
- Δl: 길이 변화량

**특징**:
- 무차원 값(단위 없음)
- 보통 % 단위로도 표현 (값에 100을 곱함)

## 왜 중요한가?

1. **크기 독립성**: 시편 크기에 관계없이 재료 특성을 비교할 수 있음
2. **설계 기준**: 구조물 설계 시 기준이 되는 수치
3. **재료 특성 파악**: 항복 강도, 탄성 계수 등을 결정하는 기본 데이터

## 항공 엔지니어가 알아야 할 점

- 항공 구조물은 다양한 응력 상태(인장, 압축, 전단, 비틀림)를 경험함
- 재료의 응력-변형률 관계를 이해하는 것은 안전한 구조물 설계의 기본
- 특히 피로 하중을 받는 항공 구조물의 경우, 재료의 응력 반응 이해가 필수적
- 응력-변형률 데이터는 유한요소해석(FEA)과 같은 컴퓨터 시뮬레이션의 기본 입력값

> 💡 **참고**: 실제 항공기 구조 설계에서는 공학적 응력/변형률뿐 아니라 진응력(true stress)과 진변형률(true strain)도 중요합니다. 큰 변형이 발생하는 경우 더 정확한 분석이 필요할 때 사용됩니다.


## 압축 시험 (Compression Tests)

압축 시험은 인장 시험과 유사하지만 재료가 압축력을 받아 수축하는 차이가 있습니다.

- **압축 응력**: 인장 응력과 동일한 방식으로 계산 (σ = F/A₀)
- **압축 변형률**: 인장 변형률과 동일한 공식 사용 (ε = (l - l₀)/l₀)
- **특징**: 관례적으로 압축력과 변형률은 음수(-)로 표시

**주요 용도**:
- 큰 소성 변형 하에서의 재료 거동 연구
- 제조 공정에서의 재료 특성 파악
- 압축 하중을 받는 구조물 설계 시 (기둥, 압축 부재 등)

## 전단 시험 (Shear Tests)

전단 시험은 재료의 평행한 면에 반대 방향으로 힘을 가하는 방식으로 수행됩니다.

- **전단 응력**: τ = F/A₀
  - F: 전단력
  - A₀: 전단력이 작용하는 면의 면적

- **전단 변형률**: γ = tan φ
  - φ: 전단 변형 각도

## 비틀림 시험 (Torsional Tests)

비틀림은 구조물이 길이 방향 축을 중심으로 회전하도록 하는 전단력의 변형입니다.

- **주요 특징**: 원통형 시편에 토크를 가하여 수행
- **전단 응력**: 가해진 토크 T와 관련됨
- **전단 변형률**: 비틀림 각도 φ와 관련됨

**응용 예**:
- 기계 축, 구동축
- 드릴, 나사와 같은 회전 부품
- 항공기 프로펠러 축, 엔진 부품

## 응력 상태의 기하학적 고려사항

실제 구조물에서는 단일 방향의 응력만 발생하지 않고, 복합적인 응력 상태가 발생합니다.

- 임의의 각도 θ를 가진 평면에서의 응력:
  - 수직 응력: σ' = σ cos²θ = σ((1 + cos 2θ)/2)
  - 전단 응력: τ' = σ sin θ cos θ = σ((sin 2θ)/2)

> 💡 **항공 구조 설계에서의 중요성**: 항공기 구조물은 비행 중 복합적인 하중(인장, 압축, 전단, 비틀림)을 동시에 경험합니다. 이러한 복합 하중 상태에서의 재료 거동을 이해하는 것은 안전한 설계의 핵심입니다. 특히 날개, 동체 연결부, 랜딩기어 마운트 등의 부분에서는 다양한 응력이 복합적으로 작용합니다.

# 4. 탄성 변형(Elastic Deformation)과 응력-변형률 거동(STRESS–STRAIN BEHAVIOR)의 이해

## 응력-변형률 관계

구조물이 변형되거나 늘어나는 정도는 가해진 응력의 크기에 따라 달라집니다. 대부분의 금속에서 상대적으로 낮은 응력 수준에서는 응력과 변형률이 서로 비례합니다:

```
σ = E·ε
```

이것이 바로 **후크의 법칙(Hooke's law)** 이며, 비례 상수 E는 **탄성 계수(modulus of elasticity)** 또는 **영률(Young's modulus)** 이라고 합니다.

## 탄성 계수(Elastic Modulus)

- 응력-변형률 선도에서 선형 부분의 기울기
- 재료의 강성(stiffness)을 나타냄
- 단위: GPa 또는 psi
- 물리적 의미: 재료가 탄성 변형에 저항하는 정도

### 주요 금속의 탄성 계수 (실온)

| 금속 | 탄성 계수(GPa) | 전단 계수(GPa) | 포아송 비 |
|------|--------------|--------------|----------|
| 알루미늄 | 69 | 25 | 0.33 |
| 구리 | 110 | 46 | 0.34 |
| 마그네슘 | 45 | 17 | 0.29 |
| 강철 | 207 | 83 | 0.30 |
| 티타늄 | 107 | 45 | 0.34 |
| 텅스텐 | 407 | 160 | 0.28 |

## 탄성 변형의 특성

1. **비영구성(Nonpermanent)**: 하중을 제거하면 재료는 원래 형태로 완전히 돌아감
2. **가역성(Reversible)**: 하중 제거 시 응력-변형률 경로를 반대 방향으로 그대로 따라감
3. **원자적 관점**: 원자 간 거리와 원자 간 결합의 신장에 작은 변화로 나타남

## 비선형 탄성 거동

일부 재료(주철, 콘크리트, 많은 폴리머)의 응력-변형률 곡선은 선형이 아닙니다:

- **접선 계수(tangent modulus)**: 응력-변형률 곡선의 특정 지점에서의 기울기
- **할선 계수(secant modulus)**: 원점에서 응력-변형률 곡선의 특정 지점까지 그은 선의 기울기

## 전단 응력-변형률 관계

전단 응력과 전단 변형률도 낮은 응력 수준에서는 비례 관계를 가집니다:

```
τ = G·γ
```

여기서 G는 **전단 계수(shear modulus)** 로, 전단 응력-변형률 곡선의 선형 탄성 영역의 기울기입니다.

## 온도 영향

온도가 증가함에 따라 탄성 계수는 감소하는 경향이 있습니다.

## 항공 엔지니어가 알아야 할 핵심 사항

- 탄성 계수는 설계 매개변수로서 구조물의 처짐(deflection)을 계산하는 데 중요함
- 알루미늄 합금(항공기 구조에 일반적으로 사용)은 강철에 비해 탄성 계수가 약 1/3 수준으로 낮음
- 티타늄은 알루미늄보다 높은 탄성 계수를 갖지만 여전히 강철보다는 낮음
- 탄성 계수는 온도에 따라 변화하므로 고온 환경(엔진 주변)에서 작동하는
  항공기 부품 설계 시 이 점을 고려해야 함
- 복합재료는 방향에 따라 탄성 계수가 달라질 수 있음 (이방성 특성)

# 5. 비탄성과 재료의 탄성 특성 (Anelasticity and Elastic Properties of Materials)

## 비탄성(Anelasticity)

지금까지는 탄성 변형(elastic deformation)이 시간에 독립적(time-independent)이라고 가정했습니다. 즉, 응력(stress)을 가하면 즉각적인 탄성 변형이 발생하고 응력이 유지되는 동안 변형률(strain)도 일정하게 유지되며, 응력을 제거하면 변형률이 즉시 0으로 돌아간다고 생각했습니다.

그러나 대부분의 공학 재료(engineering materials)에서는 **시간 의존적 탄성 변형 요소(time-dependent elastic strain component)**도 존재합니다:
- 응력을 제거한 후에도 탄성 변형이 계속됨
- 완전한 회복(complete recovery)을 위해서는 일정 시간이 필요함

이러한 시간 의존적 탄성 거동을 **비탄성(anelasticity)**이라고 합니다. 이는 변형에 수반되는 시간 의존적 미시적(microscopic), 원자적(atomic) 과정 때문에 발생합니다.

- **금속(metals)**: 비탄성 성분이 일반적으로 작아서 무시됨
- **폴리머 재료(polymeric materials)**: 비탄성 성분이 상당히 크며, 이를 **점탄성 거동(viscoelastic behavior)**이라고 함

## 포아송 비(Poisson's Ratio)

금속 시편(metal specimen)에 인장 응력(tensile stress)을 가하면, 응력 방향(z 방향)으로 탄성 신장(elastic elongation)과 그에 따른 변형률 ε<sub>z</sub>가 발생합니다. 이 신장의 결과로, 가해진 응력에 수직인 방향(x, y 방향)으로 수축(constriction)이 일어납니다.

**포아송 비(Poisson's ratio, ν)**는 측면 변형률(lateral strain)과 축 방향 변형률(axial strain)의 비율로 정의됩니다:

```
ν = -ε_x/ε_z = -ε_y/ε_z
```

여기서:
- ε<sub>x</sub>, ε<sub>y</sub>: 측면(lateral) 변형률 (보통 음수, 수축을 나타냄)
- ε<sub>z</sub>: 축 방향(axial) 변형률 (보통 양수, 신장을 나타냄)

### 포아송 비의 특징

- 거의 모든 구조 재료(structural materials)에서 ε<sub>x</sub>와 ε<sub>z</sub>는 부호가 반대임
- 등방성 재료(isotropic materials)의 이론적 포아송 비는 0.5임 (부피 변화 없음, no volume change)
- 대부분의 금속(metals)과 합금(alloys)의 포아송 비는 0.25와 0.35 사이임

### 탄성 계수 간의 관계 (Relationship between Elastic Parameters)

등방성 재료에서 전단 계수와 탄성 계수는 포아송 비를 통해 서로 관련됩니다:

```
E = 2G(1 + ν)
```

여기서:
- E: 탄성 계수(Young's modulus)
- G: 전단 계수(shear modulus)
- ν: 포아송 비(Poisson's ratio)

이 관계식을 통해 한 계수를 알면 다른 계수를 근사적으로 계산할 수 있습니다(approximation).

## 재료의 이방성 (Anisotropy in Materials)

많은 재료들은 탄성적으로 이방성(elastically anisotropic)을 가집니다. 즉, 탄성 거동(E의 크기)이 결정학적 방향(crystallographic direction)에 따라 달라집니다:

- **이방성 재료(anisotropic materials)**: 탄성 특성(elastic properties)이 방향에 따라 완전히 다름
- **등방성 재료(isotropic materials)**: 모든 방향에서 탄성 특성이 동일함

대부분의 다결정질 금속(polycrystalline metals)은 결정립 방향(grain orientation)이 무작위로 분포되어 있어 등방성으로 간주됩니다. 그러나 비정질 세라믹 유리(amorphous ceramic glasses)는 진정한 등방성(truly isotropic)을 가집니다.

## 항공 엔지니어가 알아야 할 핵심 사항 (Key Points for Aerospace Engineers)

1. **비탄성 영향(Anelastic Effects)**: 항공기 구조(aircraft structures)에서 급격한 하중 변화(sudden load changes)나 진동(vibration)이 있을 때, 비탄성 효과가 미세하게 나타날 수 있음 (대부분 무시 가능)

2. **포아송 비의 중요성(Importance of Poisson's Ratio)**: 
   - 복잡한 응력 상태(complex stress states)에서의 재료 거동 예측에 필요
   - 유한요소 해석(Finite Element Analysis, FEA)에서 필수적인 입력 매개변수
   - 압축/인장 하중(compressive/tensile loads)이 복합적으로 작용하는 복잡한 항공 구조물 설계 시 중요

3. **이방성 고려(Anisotropy Considerations)**:
   - 탄소 섬유 복합재료(carbon fiber composites)와 같은 이방성 재료를 사용할 때 특히 중요
   - 방향에 따라 탄성 계수가 크게 달라질 수 있음(directional properties)
   - 하중 방향에 따른 설계 최적화(design optimization) 가능성

4. **실제 응용(Practical Applications)**: 
   - 날개 휨(wing deflection) 및 비틀림(torsion) 계산
   - 압력 격벽(pressure bulkhead) 설계
   - 랜딩 기어 구조 해석(landing gear structural analysis)

# 6. 소성 변형과 기계적 특성 (Plastic Deformation and Mechanical Properties)

## 소성 변형 (Plastic Deformation)

대부분의 금속 재료에서 탄성 변형은 약 0.005 정도의 변형률까지만 지속됩니다. 이 지점을 넘어서면 응력과 변형률이 더 이상 비례하지 않으며(후크의 법칙이 적용되지 않음), **소성 변형(plastic deformation)**이 발생합니다.

소성 변형의 특징:
- 영구적인 변형(permanent deformation)
- 하중 제거 후에도 원래 형태로 돌아가지 않음
- 대부분의 금속에서 초기에는 완만한 곡선 형태를 보이다가 응력이 증가함에 따라 더 급격하게 변형

### 소성 변형의 미시적 메커니즘:
- **결정질 고체(crystalline solids)**: 원자들의 미끄러짐(slip) 현상과 전위(dislocation) 이동에 의해 발생
- **비결정질 재료(amorphous materials)**: 점성 유동(viscous flow) 메커니즘으로 변형

## 항복 및 항복 강도 (Yielding and Yield Strength)

대부분의 구조물은 탄성 변형만 발생하도록 설계됩니다. 소성 변형이 발생하면 구조물이 의도된 대로 기능하지 못할 수 있습니다. 따라서 **항복(yielding)**이 발생하는 지점을 아는 것이 중요합니다.

### 항복 강도 (Yield Strength, σy)
- 소성 변형이 시작되는 응력 수준
- 응력-변형률 곡선에서 선형성에서 벗어나는 초기 지점
- 때로는 **비례 한계(proportional limit)**라고도 함
- 정확한 측정이 어려워 0.002(0.2%) 변형률 오프셋 방법으로 결정됨

**0.002 변형률 오프셋 방법**:
1. 응력-변형률 곡선의 탄성 영역에 평행하게 0.002 변형률 지점에서 직선을 그림
2. 이 직선과 응력-변형률 곡선이 만나는 지점의 응력이 항복 강도

비선형 탄성 영역을 가진 재료의 경우, 변형률 오프셋 방법이 불가능하며 **상/하부 항복점(upper/lower yield point)** 현상을 보이는 재료들도 있음:
- **상부 항복점(upper yield point)**: 소성 변형 초기의 최대 응력
- **하부 항복점(lower yield point)**: 소성 변형이 진행될 때의 일정한 응력

## 인장 강도 (Tensile Strength)

항복 이후, 금속의 소성 변형에 필요한 응력은 계속 증가합니다. 이는 **변형 경화(strain hardening)** 또는 **가공 경화(work hardening)**라고 합니다.

**인장 강도(tensile strength, TS)** 또는 **극한 인장 강도(ultimate tensile strength, UTS)**:
- 응력-변형률 곡선에서 최대 응력 값
- 재료가 인장에서 견딜 수 있는 최대 응력

특징:
- 인장 강도에 도달하면 시편에 **네킹(necking)** 현상 발생 (단면적 감소)
- 모든 후속 변형은 네킹 부위에 집중됨
- 최종적으로 해당 부위에서 파단(fracture) 발생

### 인장 강도 범위
- 알루미늄: 90 MPa(저강도) ~ 550 MPa(고강도)
- 강철: 260 MPa(저강도) ~ 3000 MPa(고강도)
- 티타늄: 520 MPa

## 연성 (Ductility)

**연성(ductility)**은 파단 전 재료가 견딜 수 있는 소성 변형의 정도를 나타내는 중요한 기계적 특성입니다. 파단 시 거의 소성 변형이 없는 재료는 **취성(brittle)** 재료라고 합니다.

연성은 두 가지 방법으로 표현:
1. **백분율 신장률(percent elongation, %EL)**:
   ```
   %EL = ((lf - l0)/l0) × 100
   ```
   여기서:
   - lf: 파단 길이
   - l0: 원래 게이지 길이

2. **단면적 감소율(percent reduction in area, %RA)**:
   ```
   %RA = ((A0 - Af)/A0) × 100
   ```
   여기서:
   - A0: 원래 단면적
   - Af: 파단 지점의 단면적

연성과 관련된 중요 사항:
- 연성 값은 게이지 길이에 따라 달라지므로 명시 필요
- 일반적으로 50mm(2인치) 게이지 길이 사용
- 대부분의 금속은 실온에서 적당한 연성 보유
- 일부 금속은 저온에서 취성으로 변함

## 탄성 (Resilience)

**탄성(resilience)**은 재료가 탄성적으로 변형될 때 에너지를 흡수하고 하중 제거 시 이 에너지를 회복하는 능력입니다. 관련 특성은 **탄성 계수(modulus of resilience, Ur)**입니다.

```
Ur = ∫(0 to εy) σdε
```

선형 탄성 영역에서:
```
Ur = (1/2)σyεy = (1/2)(σy²/E)
```

여기서:
- σy: 항복 강도
- εy: 항복 변형률
- E: 탄성 계수

**단위**: J/m³ (SI) 또는 in-lb/in³ (미국식)

## 인성 (Toughness)

**인성(toughness)**은 재료가 파단 전까지 에너지를 흡수하는 능력을 나타냅니다. 특히 **파괴 인성(fracture toughness)**은 균열이 존재할 때 재료의 파괴 저항성을 나타냅니다.

정적(낮은 변형률 속도) 상황에서의 인성은 응력-변형률 곡선 아래 전체 면적으로 측정됩니다. 따라서 인성이 높은 재료는:
- 높은 강도와 높은 연성을 동시에 가짐
- 파단 전 많은 에너지를 흡수 가능

취성 재료는 높은 항복 및 인장 강도를 가질 수 있지만, 연성 재료보다 낮은 인성을 가짐

## 주요 금속의 기계적 특성 비교

| 금속 합금 | 항복 강도(MPa) | 인장 강도(MPa) | 연성(%EL) |
|---------|--------------|--------------|---------|
| 알루미늄 | 35 | 90 | 40 |
| 구리 | 69 | 200 | 45 |
| 황동 | 75 | 300 | 68 |
| 철 | 130 | 262 | 45 |
| 니켈 | 138 | 480 | 40 |
| 강철(1020) | 180 | 380 | 25 |
| 티타늄 | 450 | 520 | 25 |
| 몰리브덴 | 565 | 655 | 35 |

## 항공 엔지니어가 알아야 할 핵심 사항

1. **설계 고려사항**:
   - 항공 구조물은 대부분 항복 강도 이하에서 운용되도록 설계됨
   - 안전율(safety factor)을 적용하여 예상치 못한 하중에 대비
   - 피로(fatigue)와 응력 집중(stress concentration)이 소성 변형 시작에 영향

2. **재료 선택**:
   - 알루미늄 합금: 가볍고 적절한 강도, 높은 연성(부품 제작 용이)
   - 티타늄 합금: 중간 정도의 밀도, 높은 강도, 우수한 내열성과 내식성
   - 강철: 높은 강도가 필요한 랜딩 기어 등의 부품에 사용

3. **환경 영향**:
   - 온도 증가에 따라 항복 강도와 인장 강도는 감소하는 경향
   - 연성은 온도가 상승함에 따라 일반적으로 증가
   - 극저온 환경에서는 일부 금속이 취성으로 변할 수 있음

4. **실제 적용**:
   - 연성은 제작 공정(forming, bending)에서 허용 가능한 변형을 결정
   - 탄성은 충격이나 진동 흡수에 중요 (랜딩 기어, 마운트)
   - 인성은 손상 허용 설계(damage tolerant design)에 중요한 요소
   
# 7. 진응력, 진변형률, 경도 및 기타 기계적 특성 (True Stress, True Strain, Hardness and Other Mechanical Properties)

## 진응력과 진변형률 (True Stress and True Strain)

### 진응력 (True Stress)

인장 시험에서 최대 응력 이후의 응력 감소(응력-변형률 곡선의 M점 이후)는 재료가 약해진다는 것을 의미하는 것처럼 보이지만, 실제로는 그렇지 않습니다. 이는 네킹(necking) 영역에서 단면적이 급격히 감소하기 때문입니다.

**공학적 응력(engineering stress)**은 원래 단면적을 기준으로 계산되므로 이러한 단면적 감소를 고려하지 않습니다. 이에 따라 **진응력(true stress)**을 사용하는 것이 더 의미가 있을 수 있습니다.

진응력(σₜ)은 다음과 같이 정의됩니다:
```
σₜ = F/Aᵢ
```

여기서:
- F: 하중
- Aᵢ: 변형이 발생하는 순간의 실제 단면적(즉, 네킹 부위)

### 진변형률 (True Strain)

마찬가지로, **진변형률(true strain, εₜ)**을 다음과 같이 정의할 수 있습니다:
```
εₜ = ln(lᵢ/l₀)
```

여기서:
- lᵢ: 순간 길이
- l₀: 원래 길이

### 공학적 값과 진값 간의 변환

변형 중에 부피 변화가 없다면(대부분의 금속에서 가정할 수 있음):
```
Aᵢlᵢ = A₀l₀
```

이러한 조건에서 공학적 응력(σ)과 변형률(ε)에서 진응력과 진변형률로의 변환은 다음과 같습니다:
```
σₜ = σ(1 + ε)
εₜ = ln(1 + ε)
```

이 식들은 네킹이 시작되기 전까지만 유효합니다. 네킹 이후에는 실제 하중, 단면적, 길이 측정을 통해 계산해야 합니다.

### 진응력-진변형률 관계

소성 영역에서 네킹이 시작되는 지점까지의 진응력-진변형률 곡선은 다음과 같이 근사할 수 있습니다:
```
σₜ = Kεₜⁿ
```

여기서:
- K: 강도 계수(strength coefficient)
- n: 변형 경화 지수(strain hardening exponent), 항상 1보다 작은 값

주요 합금의 K 및 n 값:

| 재료 | n | K (MPa) |
|------|---|---------|
| 저탄소강(어닐링) | 0.21 | 600 |
| 4340강(315°C에서 템퍼링) | 0.12 | 2650 |
| 304 스테인리스강(어닐링) | 0.44 | 1400 |
| 구리(어닐링) | 0.44 | 530 |
| 황동(어닐링) | 0.21 | 585 |
| 2024 알루미늄 합금(열처리-T3) | 0.17 | 780 |
| AZ-31B 마그네슘 합금(어닐링) | 0.16 | 450 |

## 소성 변형 후의 탄성 회복 (Elastic Recovery after Plastic Deformation)

응력-변형률 시험 중 하중을 제거하면, 총 변형의 일부가 탄성 변형으로 회복됩니다. 이 거동은 다음과 같은 특징을 가집니다:

- 하중 제거(unloading) 시 곡선은 하중 제거 지점(D)에서 시작하여 거의 직선으로 내려옴
- 이 직선의 기울기는 탄성 계수와 거의 동일하거나 초기 탄성 부분과 평행함
- 회복되는 탄성 변형의 크기는 하중 제거 후 최종 변형률과 관련됨
- 하중이 다시 가해지면(reapply), 곡선은 동일한 선형 부분을 역방향으로 따라가며, 하중 제거가 시작된 응력 수준에 다시 도달하면 소성 변형이 다시 시작됨

### 항복 강도 변화

- σ₀: 초기 항복 강도
- σ'₀: 하중 제거 후 재하중 시 새로운 항복 강도

소성 변형 후 재하중 시의 항복 강도는 일반적으로 초기 항복 강도보다 높습니다. 이것은 **변형 경화(strain hardening)** 또는 **가공 경화(work hardening)** 효과라고 합니다.

## 압축, 전단, 비틀림 변형 (Compressive, Shear, and Torsional Deformations)

금속은 압축, 전단, 비틀림 하중 하에서도 소성 변형을 경험할 수 있습니다:

- **압축(compression)**: 소성 영역에서의 응력-변형률 거동은 인장과 유사(항복과 관련된 곡률)하지만, 최대점(necking)이 발생하지 않음. 파괴 모드도 인장과 다름
- **전단(shear)**: 응력-변형률 거동이 소성 영역에서 인장과 유사한 패턴을 보임
- **비틀림(torsion)**: 전단 변형의 한 형태로, 응력-변형률 특성은 전단과 유사함

## 경도 (Hardness)

경도는 재료의 국부적인 소성 변형(작은 압입이나 긁힘)에 대한 저항을 측정하는 특성입니다.

### 경도 시험의 장점
1. 간단하고 저렴함 - 특별한 시편 준비가 필요 없음
2. 비파괴적 - 시편이 파손되거나 과도하게 변형되지 않음
3. 다른 기계적 특성(예: 인장 강도)을 경도 데이터에서 추정 가능

### 주요 경도 시험 방법

#### 1. 로크웰 경도 시험(Rockwell Hardness Tests)
- 가장 일반적인 방법
- 초기 소하중 적용 후 대하중 적용 시 압입 깊이 차이로 측정
- 다양한 압입자(구형 및 경화 강철 볼, 원뿔형 다이아몬드)와 하중 조합
- 주요 스케일: A, B, C, D, E, F, G, H, K(일반 로크웰) 및 15N, 30N, 45N 등(표면 로크웰)
- 표기 예: 80 HRB(B 스케일에서 80), 60 HR15W(15W 스케일에서 60)

#### 2. 브리넬 경도 시험(Brinell Hardness Tests)
- 경화 강철/텅스텐 카바이드 구형 압입자(10mm/0.394인치)를 사용
- 500-3000kg 하중을 10-30초간 유지
- 압입 자국의 지름을 측정하여 브리넬 경도 수치로 변환
- 표기 예: 240 HB

#### 3. 미세압입 경도 시험(Microindentation Hardness Tests)
- **누프 경도 시험(Knoop)**: 작은 피라미드형 압입자, 1-1000g 하중
- **비커스 경도 시험(Vickers)**: 작은 다이아몬드 피라미드, 1-1000g 하중
- 작은 영역이나 선택된 미세 조직의 경도 측정에 적합
- 세라믹과 같은 취성 재료 시험에도 적합
- 표기 예: HK(누프), HV(비커스)

### 경도와 인장 강도의 상관관계

경도와 인장 강도는 둘 다 재료의 소성 변형에 대한 저항을 나타내므로, 일반적으로 비례 관계가 있습니다:

- 주철, 강철, 황동의 경우: TS(MPa) = 3.45 × HB
- 대부분의 강철: TS(psi) = 500 × HB

## 항공 엔지니어가 알아야 할 핵심 사항

1. **진응력과 진변형률의 중요성**:
   - 대변형 해석(large deformation analysis)에서 진응력과 진변형률을 사용해야 더 정확한 결과를 얻을 수 있음
   - 형성 공정(forming processes)이나 충돌 해석(crash analysis)에서 특히 중요

2. **변형 경화 현상의 활용**:
   - 소성 변형 후 탄성 회복의 이해는 성형 및 가공 공정 설계에 중요
   - 항공기 부품은 종종 변형 경화를 이용해 강도를 높임(예: 냉간 가공, cold working)

3. **경도 측정의 실용적 측면**:
   - 현장에서 빠르게 재료 특성을 확인할 수 있는 비파괴 방법
   - 용접부, 열영향부(heat-affected zones) 등의 국부적 특성 평가에 유용
   - 마모 저항성이 중요한 부품(랜딩 기어, 베어링 표면 등)의 품질 관리에 활용

4. **다양한 하중 상태에서의 소성 변형 이해**:
   - 항공 구조물은 복합적인 하중 상태(인장, 압축, 전단, 비틀림의 조합)를 경험함
   - 이러한 복합 하중 상태에서의 재료 거동 이해는 정확한 구조 해석에 필수적
   
   
# 8. 재료 특성의 변동성과 설계/안전 계수 (Property Variability and Design/Safety Factors)

## 재료 특성의 변동성 (Variability of Material Properties)

재료 특성은 단순한 결정론적 값이 아닌 통계적 수치입니다. 정밀한 측정 장비와 엄격하게 통제된 시험 절차를 사용하더라도, 수집된 데이터에는 항상 어느 정도의 산포(scatter)나 변동성이 존재합니다.

예를 들어, 동일한 금속 합금에서 제작된 여러 개의 인장 시편을 동일한 장비로 시험하더라도, 각 시편의 응력-변형률 곡선이 서로 약간씩 다르게 나타납니다. 이로 인해 탄성 계수, 항복 강도, 인장 강도 값에 변동이 생깁니다.

### 변동성의 원인

1. **측정 데이터의 불확실성**: 시험 방법, 장비 검교정
2. **시편 제작 과정의 차이**: 제작자, 제작 과정의 변동
3. **재료 자체의 불균질성**: 동일한 배치의 재료 내에서도 미세 조성과 구조적 차이가 존재

재료의 밀도, 전기 전도도, 열팽창 계수 등 다른 특성들도 유사한 산포를 보입니다.

### 평균과 표준편차의 계산 (Computation of Average and Standard Deviation Values)

**평균값**:
```
x̄ = (Σxi)/n
```
여기서:
- n: 관측 또는 측정 횟수
- xi: 개별 측정값

**표준편차**:
```
s = [(Σ(xi - x̄)²)/(n-1)]^(1/2)
```

표준편차 값이 클수록 산포도가 높음을 의미합니다.

## 설계/안전 계수 (Design/Safety Factors)

실제 서비스 조건에서의 하중 크기와 응력 분포를 특성화하는 데는 항상 불확실성이 존재합니다. 보통 하중 계산은 근사치에 불과합니다. 또한 앞서 언급했듯이, 모든 공학 재료는 측정된 기계적 특성에 변동성을 보입니다.

### 설계 접근 방식의 변화

- **20세기**: 설계 안전 계수(design safety factor)로 적용 응력을 줄이는 방식
- **현대적 접근**: 충분한 인성을 가진 재료 사용, 구조적 중복성(redundancy) 제공, 정기 검사로 균열 감지, 필요 시 안전하게 구성 요소 제거/수리

### 설계 응력 (Design Stress)

중요 응용 분야에서는 **설계 응력(design stress, σ_d)**이 사용됩니다:
```
σ_d = N'σ_c
```
여기서:
- σ_c: 계산된 응력 수준(최대 예상 하중 기준)
- N': 설계 계수(1보다 큰 값)

이를 통해 재료 선택 시 적어도 이 값만큼의 항복 강도를 가져야 함을 보장합니다.

### 안전 응력 (Safe Stress)

대안으로, **안전 응력(safe stress)** 또는 **작업 응력(working stress, σ_w)**이 사용되기도 합니다:
```
σ_w = σ_y/N
```
여기서:
- σ_y: 재료의 항복 강도
- N: 안전 계수(factor of safety)

### 설계 응력 vs 안전 응력

설계 응력(Equation 6.23) 사용은 일반적으로 재료의 항복 강도보다 최대 예상 응력 예측에 더 큰 불확실성이 있을 때 선호됩니다.

### 안전 계수 선택

적절한 N 값의 선택은 중요합니다:
- N이 너무 크면 과다 설계: 너무 많은 재료 사용 또는 필요 이상의 강도를 가진 합금 사용
- 일반적인 N 값 범위: 1.2-4.0

N 값 선택 시 고려 사항:
1. **경제성**: 재료 비용, 제작 비용
2. **이전 경험**: 유사 설계의 성공/실패 사례
3. **측정 정확도**: 기계적 물성 측정 및 재료 특성 결정의 정확도
4. **실패 결과**: 생명, 재산 손실, 운영 중단 등의 관점에서 결과의 심각성

따라서 구조 설계자들은 경제적으로 가능한 범위 내에서 중복성을 갖춘 튼튼한 재료를 사용하는 방향으로 움직이고 있습니다.

## 항공 엔지니어가 알아야 할 핵심 사항

1. **통계적 접근의 중요성**:
   - 재료 특성의 통계적 특성(평균, 표준편차, 분포)을 이해하고 활용
   - "이 합금의 파단 강도는 얼마인가?"보다 "이 조건에서 이 합금의 파단 확률은 얼마인가?"를 질문하는 습관

2. **항공기 구조물의 안전 계수**:
   - 상업용 항공기의 일반적인 안전 계수: 1.5
   - 특수 하중 조건에서는 더 높은 값(~1.8) 사용 가능
   - 우주 발사체에서는 효율성을 위해 더 낮은 안전 계수(~1.2-1.4) 사용 가능

3. **중요 설계 고려사항**:
   - 정적 강도뿐만 아니라 피로 수명도 고려
   - 손상 허용 설계(damage tolerant design) 원칙 적용
   - 파괴 인성과 균열 성장률 고려

4. **재료 선택과 품질 관리**:
   - 항공기 구조물에 사용되는 재료는 일반적으로 더 엄격한 품질 관리와 검사 기준 적용
   - 일관된 특성을 보장하기 위한 정밀한 공정 제어
   - 통계적 공정 관리(SPC) 및 품질 보증 방법 활용

5. **실제 응용 예시**:
   - 항공기 날개 구조: 하중 불확실성, 재료 변동성, 제작 공차를 고려한 설계
   - 착륙 장치: 충격 하중의 확률적 특성을 고려한 안전 계수 설정
   - 엔진 마운트: 극한 온도와 진동 환경을 견디기 위한 재료 선택과 안전 계수 결정
   
# 참고 문헌 (References)

본 내용은 다음 자료를 참고하여 정리되었습니다:

Callister, W. D., Jr., & Rethwisch, D. G. (2019). *Materials Science and Engineering: An Introduction* (10th ed.). Wiley.

> **참고**: 본 정리 내용은 교육 및 학습 목적으로 작성되었으며, 실제 엔지니어링 설계에 적용하기 전에는 해당 분야의 최신 표준, 규정 및 전문가의 조언을 참고하시기 바랍니다.