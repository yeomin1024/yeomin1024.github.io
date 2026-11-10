# VEH02 부산 시내버스 (일반) 설계도

버전: v1.0 — 2026-11-10 — 설계도·블록아웃·참고 이미지 최초 작성
상태: 초안
폴더: `busan-3d/assets/VEH02_CityBus/`

ID·버전·날짜·섹션·파일명은 식별자다. 표의 근거 태그는 해당 행의 모든 숫자에 적용한다. 스크립트의 모든 치수·좌표·각도·분할·PBR 수치는 [설정]이다. 사진이 없으므로 실측 모델이 아닌 가상 저상버스 제작안이다.

## 1. 개요
| 항목 | 내용 |
|---|---|
| 등장 장면 | FACTS.md 전체 일정의 일반버스 이동: 61·7·71·508·181·38·27·131번 [확인: FACTS.md 일정]; 급행·마을버스는 별도 에셋 |
| 화면에서의 역할 | 버스만 이용하는 여행임을 청색 버스·교체 가능한 행선판·승하차 동작으로 전달 |
| 등급 | H |
| 가장 가까운 카메라 거리 | 문 1.2 m [설정], 외관 4 m [설정], 실내 카메라는 SF02 조립 후 설정 |
| 화면 점유율 | 외관 최대 85% [설정], 문·단말기 컷 최대 100% [설정] |

## 2. 핵심 특징
- **지켜야 할 것**
  - 둥근 상자형 차체, 큰 전면 유리, 저상 출입구.
  - 앞·가운데 승객 출입문은 모두 진행 우측인 −X 면에 배치. 운전석은 +X 면.
  - 청색 하부와 오프화이트 상부의 가상 배색, 실제 도색·로고 미복제.
  - 앞·옆·뒤 행선판을 독립 부품으로 분리하여 노선 번호 교체.
  - 문은 경첩축, 바퀴는 차축 중심 원점. 앞바퀴 조향 Empty와 휠 회전 메시 분리.
- **생략·단순화할 것**
  - 제조사 외형 세부, 실제 운수회사 문구·BIG BUS 로고는 복제하지 않음.
  - 하부 배관·엔진·서스펜션은 그림자와 대형 덩어리로 축약.
  - 와이퍼·창 고무 패킹·휠 볼트는 최종 모델에서 실루엣 영향만 남김.
  - 블록아웃 실내 좌석은 공간 확인용, 실제 좌석 수·배열로 주장하지 않음.

## 3. 치수표
| 부위 | 가로 X (m) | 깊이 Y (m) | 높이 Z (m) | 근거 태그 | 근거·계산식 |
|---|---|---|---|---|---|
| 전체(미러·지붕 냉방기 포함) | 2.89 | 11.00 | 3.30 | [설정] | 폭: 2 × (1.365 + 0.16/2); 전고: 3.225 + 0.15/2 |
| 차체 외피(미러 제외) | 2.49 | 11.00 | 2.81 | [설정] | 외피 바닥 Z=0.34~지붕 Z=3.15. 실제 차체 폭은 미확정 |
| FACTS 참고 범위 | 약 2.49 | 약 11.0 | 약 3.2~3.4 | [추정] | FACTS.md VEH02; 사진 미제공이므로 현재 추가 비율 계산 불가 |
| 휠베이스 | – | 5.70 | – | [설정] | 후륜 Y=2.20 − 전륜 Y=−3.50; FACTS 미확정 범위 5.5~5.9 m [추정] 내 선택 |
| 앞 / 뒤 오버행 | – | 2.00 / 3.30 | – | [설정] | −3.5−(−5.5), 5.5−2.2; 합계 2+5.7+3.3=11 |
| 타이어(월드 치수, 전륜) | 0.26 | 0.94 | 0.94 | [설정] | 차축 X 방향, 반지름 0.47 |
| 타이어(월드 치수, 후륜) | 0.42 | 0.94 | 0.94 | [설정] | 복륜은 블록아웃에서 두꺼운 단일 실린더로 축약 |
| 앞문 개구부 | 0.08 | 1.10 | 2.10 | [설정] | −X 면, Y=−5.40~−4.30, Z=0.34~2.44 |
| 가운데문 개구부 | 0.08 | 1.20 | 2.10 | [설정] | −X 면, Y=−0.50~0.70, Z=0.34~2.44 |
| 입구 바닥 상면 | – | – | 0.34 | [설정] | Floor 중심 0.30 + 두께 0.08/2; 실측 저상 높이 아님 |
| 후부 단상 상면 | 2.30 | 2.20 | 0.80 | [설정] | RearDeck 중심 0.57 + 높이 0.46/2; 접근은 후속 계단 제작 |
| 단일 좌석 방석 | 0.46 | 0.48 | 0.12 | [설정] | 460 × 480 × 120 mm [설정], 실내 공간 대용 |
| 문 잎 간 틈 | – | 0.02 | – | [설정] | 개구 폭에서 빼고 남은 폭을 두 잎에 균등 배분 |

사람 1.70 m [설정: 지시서 기준] 대비 전체 높이 3.30/1.70 = 1.941배 [설정]. 차체 폭과 미러 포함 전체 폭을 구분한다. 차로 폭 3.25 m [설정: 지시서 기준]에서 미러 여유는 양쪽 각각 (3.25−2.89)/2 = 0.18 m [설정]; 곡선·정차 간격은 씬에서 별도 검수한다.

## 4. 정면·측면·윗면 도면
### 4-1. 주요 점 좌표 (에셋 원점 = 바닥 중앙, 단위 m)
모든 좌표 [설정]. 정면 −Y, 위 +Z, 진행 우측 −X, 운전석 쪽 +X. 사람을 기준으로 좌우를 명시해 미러링 실수를 방지한다.

| 점 이름 | x | y | z | 설명 |
|---|---|---|---|---|
| 원점 | 0 | 0 | 0 | Root, 타이어 접지면 중앙 |
| 차체 전단 / 후단 | 0 | −5.50 / 5.50 | 1.75 | 외곽 기준 |
| 미러 폭 끝 | −1.445 / 1.445 | −5.10 | 2.48 | 좌우 대칭 |
| 최고점 | 0 | 1.60 | 3.30 | RoofAC 상단 |
| 앞문 앞 / 뒤 경첩 | −1.225 | −5.40 / −4.30 | 1.39 | DoorFrontA/B |
| 가운데문 앞 / 뒤 경첩 | −1.225 | −0.50 / 0.70 | 1.39 | DoorMiddleA/B |
| 우측 앞 / 뒤 차축 | −1.08 / −0.98 | −3.50 / 2.20 | 0.47 | FrontAxleR / RearAxleR |
| 실내 소켓 | 0 | 0 | 0.34 | InteriorSocket, SF02 기준 |
| 카드 단말기 소켓 | −0.62 | −4.65 | 1.35 | ValidatorSocket, SF02 연결 |

### 4-2. 텍스트 실루엣 (가로세로 비율 유지)
셀 가로 약 0.25 m [설정], 줄 높이 약 0.50 m [설정] 가정. 측면은 −X에서 본 우측이며 오른쪽이 앞. ASCII는 패널·창·바퀴 식별용이며 치수는 좌표가 우선한다.

```
정면 (-Y)                  우측면 (-X)
   ______                      ________________________________
  | [LED]|                 ___|________________________________|___
  |======|                 |==========================|D|========|D|
  |      |                 |==========================|D|========|D|
  |______|                 |                          |D|        |D|
  |o____o|                 |        __                |D|    __  |D|
    O  O                   |___( O)_____________________( O)_______|

윗면 (+Z, 왼쪽=앞; 긴 축을 가로로 회전 표기)
  ____________________________________________
 | driver +X             roof A/C              |
 |                                            |
 |                                            |
 | front door -X         middle door -X        |
 |____________________________________________|
```

### 4-3. 치수선
좌표·길이 모두 [설정].

| 치수선 | 시작점 → 끝점 | 길이 (m) |
|---|---|---|
| 전장 | (0,−5.5,0) → (0,5.5,0) | 11 |
| 미러 포함 폭 | (−1.445,−5.1,2.48) → (1.445,−5.1,2.48) | 2.89 |
| 차체 폭 | (−1.245,0,3.025) → (1.245,0,3.025) | 2.49 |
| 전고 | (0,1.6,0) → (0,1.6,3.30) | 3.30 |
| 휠베이스 | (0,−3.5,.47) → (0,2.2,.47) | 5.70 |
| 앞문 폭 | (−1.225,−5.4,1.39) → (−1.225,−4.3,1.39) | 1.10 |

## 5. 부품 목록
PARTS와 행별 일치. 해당 행 [설정]은 모든 숫자·베벨·분할에 적용한다. cube/sphere 크기는 전체 치수. cylinder는 회전 전 지름 X·Y와 로컬 Z 두께, 로컬 Y회전으로 차축을 X에 맞춘다. pivot 튜플은 도형 중심에서 회전축까지의 오프셋이다. 문은 수직 경첩축 중심 원점, 차륜은 차축 중심. Empty 크기는 표시용으로 외곽에서 제외한다. 최종 이름은 `VEH02_CityBus_{부품명}_L0`.

| 부품명 | 도형 | 크기 X×Y×Z (m) | 위치 x,y,z (부모 기준) | 회전 x,y,z (°) | 원점(pivot) | 부모 | 재질 | 반복·대칭 | 근거 |
|---|---|---|---|---|---|---|---|---|---|
| Root | empty | (0.2, 0.2, 0.2) | (0, 0, 0) | (0, 0, 0) | center | – | – | 없음 | [설정] |
| Floor | cube | (2.4, 11, 0.08) | (0, 0, 0.3) | (0, 0, 0) | center | Root | Floor | bevel 0.01 m / 2 seg | [설정] |
| Roof | cube | (2.49, 11, 0.25) | (0, 0, 3.025) | (0, 0, 0) | center | Root | Frame | bevel 0.1 m / 2 seg | [설정] |
| RoofAC | cube | (1.8, 2, 0.15) | (0, 1.6, 3.225) | (0, 0, 0) | center | Root | Frame | bevel 0.05 m / 2 seg | [설정] |
| SideRBand0 | cube | (0.08, 0.1, 0.37) | (-1.205, -5.45, 1.175) | (0, 0, 0) | center | Root | Paint | bevel 0.02 m / 2 seg | [설정] |
| SideRLower0S0 | cube | (0.08, 0.1, 0.65) | (-1.205, -5.45, 0.665) | (0, 0, 0) | center | Root | Paint | bevel 0.015 m / 2 seg | [설정] |
| SideRCorner0 | cube | (0.08, 0.1, 1.54) | (-1.205, -5.45, 2.13) | (0, 0, 0) | center | Root | Frame | bevel 0.015 m / 2 seg | [설정] |
| SideRBand1 | cube | (0.08, 3.8, 0.37) | (-1.205, -2.4, 1.175) | (0, 0, 0) | center | Root | Paint | bevel 0.02 m / 2 seg | [설정] |
| SideRLower1S0 | cube | (0.08, 0.28, 0.65) | (-1.205, -4.16, 0.665) | (0, 0, 0) | center | Root | Paint | bevel 0.015 m / 2 seg | [설정] |
| SideRLower1S2 | cube | (0.08, 2.48, 0.65) | (-1.205, -1.74, 0.665) | (0, 0, 0) | center | Root | Paint | bevel 0.015 m / 2 seg | [설정] |
| SideRGlass1 | cube | (0.04, 3.8, 1.43) | (-1.205, -2.4, 2.105) | (0, 0, 0) | center | Root | Glass | bevel 0.015 m / 2 seg | [설정] |
| SideRBand2 | cube | (0.08, 4.8, 0.37) | (-1.205, 3.1, 1.175) | (0, 0, 0) | center | Root | Paint | bevel 0.02 m / 2 seg | [설정] |
| SideRLower2S0 | cube | (0.08, 0.98, 0.65) | (-1.205, 1.19, 0.665) | (0, 0, 0) | center | Root | Paint | bevel 0.015 m / 2 seg | [설정] |
| SideRLower2S2 | cube | (0.08, 2.78, 0.65) | (-1.205, 4.11, 0.665) | (0, 0, 0) | center | Root | Paint | bevel 0.015 m / 2 seg | [설정] |
| SideRGlass2 | cube | (0.04, 4.8, 1.43) | (-1.205, 3.1, 2.105) | (0, 0, 0) | center | Root | Glass | bevel 0.015 m / 2 seg | [설정] |
| PillarR0 | cube | (0.09, 0.08, 1.54) | (-1.205, -4.3, 2.13) | (0, 0, 0) | center | Root | Frame | bevel 0.01 m / 2 seg | [설정] |
| PillarR1 | cube | (0.09, 0.08, 1.54) | (-1.205, -2.8, 2.13) | (0, 0, 0) | center | Root | Frame | bevel 0.01 m / 2 seg | [설정] |
| PillarR2 | cube | (0.09, 0.08, 1.54) | (-1.205, -1.3, 2.13) | (0, 0, 0) | center | Root | Frame | bevel 0.01 m / 2 seg | [설정] |
| PillarR3 | cube | (0.09, 0.08, 1.54) | (-1.205, 0.7, 2.13) | (0, 0, 0) | center | Root | Frame | bevel 0.01 m / 2 seg | [설정] |
| PillarR4 | cube | (0.09, 0.08, 1.54) | (-1.205, 2, 2.13) | (0, 0, 0) | center | Root | Frame | bevel 0.01 m / 2 seg | [설정] |
| PillarR5 | cube | (0.09, 0.08, 1.54) | (-1.205, 3.5, 2.13) | (0, 0, 0) | center | Root | Frame | bevel 0.01 m / 2 seg | [설정] |
| PillarR6 | cube | (0.09, 0.08, 1.54) | (-1.205, 5.4, 2.13) | (0, 0, 0) | center | Root | Frame | bevel 0.01 m / 2 seg | [설정] |
| SideLBand0 | cube | (0.08, 11, 0.37) | (1.205, 0, 1.175) | (0, 0, 0) | center | Root | Paint | bevel 0.02 m / 2 seg | [설정] |
| SideLLower0S0 | cube | (0.08, 1.48, 0.65) | (1.205, -4.76, 0.665) | (0, 0, 0) | center | Root | Paint | bevel 0.015 m / 2 seg | [설정] |
| SideLLower0S2 | cube | (0.08, 4.66, 0.65) | (1.205, -0.65, 0.665) | (0, 0, 0) | center | Root | Paint | bevel 0.015 m / 2 seg | [설정] |
| SideLLower0S4 | cube | (0.08, 2.78, 0.65) | (1.205, 4.11, 0.665) | (0, 0, 0) | center | Root | Paint | bevel 0.015 m / 2 seg | [설정] |
| SideLGlass0 | cube | (0.04, 11, 1.43) | (1.205, 0, 2.105) | (0, 0, 0) | center | Root | Glass | bevel 0.015 m / 2 seg | [설정] |
| PillarL0 | cube | (0.09, 0.08, 1.54) | (1.205, -5.4, 2.13) | (0, 0, 0) | center | Root | Frame | bevel 0.01 m / 2 seg | [설정] |
| PillarL1 | cube | (0.09, 0.08, 1.54) | (1.205, -3.9, 2.13) | (0, 0, 0) | center | Root | Frame | bevel 0.01 m / 2 seg | [설정] |
| PillarL2 | cube | (0.09, 0.08, 1.54) | (1.205, -2.3, 2.13) | (0, 0, 0) | center | Root | Frame | bevel 0.01 m / 2 seg | [설정] |
| PillarL3 | cube | (0.09, 0.08, 1.54) | (1.205, -0.7, 2.13) | (0, 0, 0) | center | Root | Frame | bevel 0.01 m / 2 seg | [설정] |
| PillarL4 | cube | (0.09, 0.08, 1.54) | (1.205, 0.9, 2.13) | (0, 0, 0) | center | Root | Frame | bevel 0.01 m / 2 seg | [설정] |
| PillarL5 | cube | (0.09, 0.08, 1.54) | (1.205, 2.5, 2.13) | (0, 0, 0) | center | Root | Frame | bevel 0.01 m / 2 seg | [설정] |
| PillarL6 | cube | (0.09, 0.08, 1.54) | (1.205, 4.1, 2.13) | (0, 0, 0) | center | Root | Frame | bevel 0.01 m / 2 seg | [설정] |
| PillarL7 | cube | (0.09, 0.08, 1.54) | (1.205, 5.4, 2.13) | (0, 0, 0) | center | Root | Frame | bevel 0.01 m / 2 seg | [설정] |
| FrontLower | cube | (2.49, 0.08, 0.92) | (0, -5.46, 0.8) | (0, 0, 0) | center | Root | Paint | bevel 0.035 m / 2 seg | [설정] |
| FrontGlass | cube | (2.3, 0.06, 1.4) | (0, -5.46, 2.01) | (0, 0, 0) | center | Root | Glass | bevel 0.025 m / 2 seg | [설정] |
| FrontHeader | cube | (2.49, 0.08, 0.19) | (0, -5.46, 2.805) | (0, 0, 0) | center | Root | Frame | bevel 0.025 m / 2 seg | [설정] |
| FrontLED | cube | (1.7, 0.085, 0.25) | (0, -5.455, 2.94) | (0, 0, 0) | center | Root | LED | bevel 0.02 m / 2 seg | [설정] |
| FrontLampR | cube | (0.4, 0.1, 0.2) | (-0.87, -5.45, 0.82) | (0, 0, 0) | center | Root | Headlight | bevel 0.035 m / 2 seg | [설정] |
| FrontLampL | cube | (0.4, 0.1, 0.2) | (0.87, -5.45, 0.82) | (0, 0, 0) | center | Root | Headlight | bevel 0.035 m / 2 seg | [설정] |
| RearLower | cube | (2.49, 0.08, 0.92) | (0, 5.46, 0.8) | (0, 0, 0) | center | Root | Paint | bevel 0.035 m / 2 seg | [설정] |
| RearGlass | cube | (2.3, 0.06, 1.4) | (0, 5.46, 2.01) | (0, 0, 0) | center | Root | Glass | bevel 0.025 m / 2 seg | [설정] |
| RearHeader | cube | (2.49, 0.08, 0.19) | (0, 5.46, 2.805) | (0, 0, 0) | center | Root | Frame | bevel 0.025 m / 2 seg | [설정] |
| RearLED | cube | (1.7, 0.085, 0.25) | (0, 5.455, 2.94) | (0, 0, 0) | center | Root | LED | bevel 0.02 m / 2 seg | [설정] |
| RearLampR | cube | (0.4, 0.1, 0.2) | (-0.87, 5.45, 0.82) | (0, 0, 0) | center | Root | TailLight | bevel 0.035 m / 2 seg | [설정] |
| RearLampL | cube | (0.4, 0.1, 0.2) | (0.87, 5.45, 0.82) | (0, 0, 0) | center | Root | TailLight | bevel 0.035 m / 2 seg | [설정] |
| SideLED | cube | (0.09, 1.5, 0.26) | (-1.2, -3.2, 2.67) | (0, 0, 0) | center | Root | LED | bevel 0.02 m / 2 seg | [설정] |
| DoorFrontHeader | cube | (0.08, 1.1, 0.46) | (-1.205, -4.85, 2.67) | (0, 0, 0) | center | Root | Frame | bevel 0.015 m / 2 seg | [설정] |
| DoorFrontA | cube | (0.04, 0.54, 2.1) | (-1.225, -5.4, 1.39) | (0, 0, 0) | (0, -0.27, 0) | Root | Glass | bevel 0.008 m / 2 seg | [설정] |
| DoorFrontALower | cube | (0.044, 0.54, 0.78) | (0, 0.27, -0.66) | (0, 0, 0) | center | DoorFrontA | Paint | bevel 0.008 m / 2 seg | [설정] |
| DoorFrontB | cube | (0.04, 0.54, 2.1) | (-1.225, -4.3, 1.39) | (0, 0, 0) | (0, 0.27, 0) | Root | Glass | bevel 0.008 m / 2 seg | [설정] |
| DoorFrontBLower | cube | (0.044, 0.54, 0.78) | (0, -0.27, -0.66) | (0, 0, 0) | center | DoorFrontB | Paint | bevel 0.008 m / 2 seg | [설정] |
| DoorMiddleHeader | cube | (0.08, 1.2, 0.46) | (-1.205, 0.1, 2.67) | (0, 0, 0) | center | Root | Frame | bevel 0.015 m / 2 seg | [설정] |
| DoorMiddleA | cube | (0.04, 0.59, 2.1) | (-1.225, -0.5, 1.39) | (0, 0, 0) | (0, -0.295, 0) | Root | Glass | bevel 0.008 m / 2 seg | [설정] |
| DoorMiddleALower | cube | (0.044, 0.59, 0.78) | (0, 0.295, -0.66) | (0, 0, 0) | center | DoorMiddleA | Paint | bevel 0.008 m / 2 seg | [설정] |
| DoorMiddleB | cube | (0.04, 0.59, 2.1) | (-1.225, 0.7, 1.39) | (0, 0, 0) | (0, 0.295, 0) | Root | Glass | bevel 0.008 m / 2 seg | [설정] |
| DoorMiddleBLower | cube | (0.044, 0.59, 0.78) | (0, -0.295, -0.66) | (0, 0, 0) | center | DoorMiddleB | Paint | bevel 0.008 m / 2 seg | [설정] |
| MirrorArmR | cube | (0.22, 0.06, 0.06) | (-1.305, -5.1, 2.48) | (0, 0, 0) | center | Root | Rubber | bevel 0.015 m / 2 seg | [설정] |
| MirrorR | cube | (0.16, 0.34, 0.5) | (-1.365, -5.1, 2.48) | (0, 0, 0) | center | Root | Rubber | bevel 0.035 m / 2 seg | [설정] |
| MirrorArmL | cube | (0.22, 0.06, 0.06) | (1.305, -5.1, 2.48) | (0, 0, 0) | center | Root | Rubber | bevel 0.015 m / 2 seg | [설정] |
| MirrorL | cube | (0.16, 0.34, 0.5) | (1.365, -5.1, 2.48) | (0, 0, 0) | center | Root | Rubber | bevel 0.035 m / 2 seg | [설정] |
| FrontAxleR | empty | (0.15, 0.15, 0.15) | (-1.08, -3.5, 0.47) | (0, 0, 0) | center | Root | – | 없음 | [설정] |
| WheelFrontR | cylinder | (0.94, 0.94, 0.26) | (0, 0, 0) | (0, 90, 0) | center | FrontAxleR | Rubber | 32 radial seg | [설정] |
| HubFrontR | cylinder | (0.48, 0.48, 0.028) | (-0.145, 0, 0) | (0, 90, 0) | center | FrontAxleR | Steel | 24 radial seg | [설정] |
| FrontAxleL | empty | (0.15, 0.15, 0.15) | (1.08, -3.5, 0.47) | (0, 0, 0) | center | Root | – | 없음 | [설정] |
| WheelFrontL | cylinder | (0.94, 0.94, 0.26) | (0, 0, 0) | (0, 90, 0) | center | FrontAxleL | Rubber | 32 radial seg | [설정] |
| HubFrontL | cylinder | (0.48, 0.48, 0.028) | (0.145, 0, 0) | (0, 90, 0) | center | FrontAxleL | Steel | 24 radial seg | [설정] |
| RearAxleR | empty | (0.15, 0.15, 0.15) | (-0.98, 2.2, 0.47) | (0, 0, 0) | center | Root | – | 없음 | [설정] |
| WheelRearR | cylinder | (0.94, 0.94, 0.42) | (0, 0, 0) | (0, 90, 0) | center | RearAxleR | Rubber | 32 radial seg | [설정] |
| HubRearR | cylinder | (0.48, 0.48, 0.028) | (-0.225, 0, 0) | (0, 90, 0) | center | RearAxleR | Steel | 24 radial seg | [설정] |
| RearAxleL | empty | (0.15, 0.15, 0.15) | (0.98, 2.2, 0.47) | (0, 0, 0) | center | Root | – | 없음 | [설정] |
| WheelRearL | cylinder | (0.94, 0.94, 0.42) | (0, 0, 0) | (0, 90, 0) | center | RearAxleL | Rubber | 32 radial seg | [설정] |
| HubRearL | cylinder | (0.48, 0.48, 0.028) | (0.225, 0, 0) | (0, 90, 0) | center | RearAxleL | Steel | 24 radial seg | [설정] |
| InteriorSocket | empty | (0.2, 0.2, 0.2) | (0, 0, 0.34) | (0, 0, 0) | center | Root | – | 없음 | [설정] |
| ValidatorSocket | empty | (0.15, 0.15, 0.15) | (-0.62, -4.65, 1.35) | (0, 0, 0) | center | Root | – | 없음 | [설정] |
| RearDeck | cube | (2.3, 2.2, 0.46) | (0, 4.2, 0.57) | (0, 0, 0) | center | Root | Floor | bevel 0.01 m / 2 seg | [설정] |
| DriverSeat | cube | (0.46, 0.5, 0.12) | (0.65, -4.55, 0.78) | (0, 0, 0) | center | Root | Seat | bevel 0.01 m / 2 seg | [설정] |
| DriverBack | cube | (0.46, 0.12, 0.65) | (0.65, -4.31, 1.045) | (0, 0, 0) | center | Root | Seat | bevel 0.01 m / 2 seg | [설정] |
| Dashboard | cube | (1.1, 0.5, 0.48) | (0.47, -5.03, 1.1) | (0, 0, 0) | center | Root | Rubber | bevel 0.06 m / 2 seg | [설정] |
| Seat0 | cube | (0.46, 0.48, 0.12) | (0.78, -2.2, 0.8) | (0, 0, 0) | center | Root | Seat | bevel 0.01 m / 2 seg | [설정] |
| SeatBack0 | cube | (0.46, 0.12, 0.62) | (0.78, -1.98, 1.05) | (0, 0, 0) | center | Root | Seat | bevel 0.01 m / 2 seg | [설정] |
| Seat1 | cube | (0.46, 0.48, 0.12) | (0.78, -1.25, 0.8) | (0, 0, 0) | center | Root | Seat | bevel 0.01 m / 2 seg | [설정] |
| SeatBack1 | cube | (0.46, 0.12, 0.62) | (0.78, -1.03, 1.05) | (0, 0, 0) | center | Root | Seat | bevel 0.01 m / 2 seg | [설정] |
| Seat2 | cube | (0.46, 0.48, 0.12) | (0.78, -0.3, 0.8) | (0, 0, 0) | center | Root | Seat | bevel 0.01 m / 2 seg | [설정] |
| SeatBack2 | cube | (0.46, 0.12, 0.62) | (0.78, -0.08, 1.05) | (0, 0, 0) | center | Root | Seat | bevel 0.01 m / 2 seg | [설정] |
| Seat3 | cube | (0.46, 0.48, 0.12) | (0.78, 0.65, 0.8) | (0, 0, 0) | center | Root | Seat | bevel 0.01 m / 2 seg | [설정] |
| SeatBack3 | cube | (0.46, 0.12, 0.62) | (0.78, 0.87, 1.05) | (0, 0, 0) | center | Root | Seat | bevel 0.01 m / 2 seg | [설정] |
| Seat4 | cube | (0.46, 0.48, 0.12) | (-0.78, 1.35, 0.8) | (0, 0, 0) | center | Root | Seat | bevel 0.01 m / 2 seg | [설정] |
| SeatBack4 | cube | (0.46, 0.12, 0.62) | (-0.78, 1.57, 1.05) | (0, 0, 0) | center | Root | Seat | bevel 0.01 m / 2 seg | [설정] |
| Seat5 | cube | (0.46, 0.48, 0.12) | (0.78, 1.6, 0.8) | (0, 0, 0) | center | Root | Seat | bevel 0.01 m / 2 seg | [설정] |
| SeatBack5 | cube | (0.46, 0.12, 0.62) | (0.78, 1.82, 1.05) | (0, 0, 0) | center | Root | Seat | bevel 0.01 m / 2 seg | [설정] |
| Seat6 | cube | (0.46, 0.48, 0.12) | (-0.78, 3.9, 1.26) | (0, 0, 0) | center | Root | Seat | bevel 0.01 m / 2 seg | [설정] |
| SeatBack6 | cube | (0.46, 0.12, 0.62) | (-0.78, 4.12, 1.51) | (0, 0, 0) | center | Root | Seat | bevel 0.01 m / 2 seg | [설정] |
| Seat7 | cube | (0.46, 0.48, 0.12) | (0.78, 3.9, 1.26) | (0, 0, 0) | center | Root | Seat | bevel 0.01 m / 2 seg | [설정] |
| SeatBack7 | cube | (0.46, 0.12, 0.62) | (0.78, 4.12, 1.51) | (0, 0, 0) | center | Root | Seat | bevel 0.01 m / 2 seg | [설정] |
| LightStripR | cube | (0.08, 8.5, 0.04) | (-0.7, 0, 2.88) | (0, 0, 0) | center | Root | InteriorLight | bevel 0.015 m / 2 seg | [설정] |
| LightStripL | cube | (0.08, 8.5, 0.04) | (0.7, 0, 2.88) | (0, 0, 0) | center | Root | InteriorLight | bevel 0.015 m / 2 seg | [설정] |

## 6. 모델링 순서
| 단계 | 작업 | 쓸 모디파이어·설정값 |
|---|---|---|
| 블록아웃 | 실행·REPORT 확인, 문 경첩과 조향 Empty·소켓 확인 | 치수 허용 오차 0.01 m [설정]; 부품 표와 동일 |
| 1차 형태 | 측면 하부 사각 휠 개구를 원호로 정리; 앞뒤 모서리를 둥글게 연결; 출입구는 실제 빈 공간으로 유지 | 차륜 주변 여유 최소 0.05 m [설정], 외곽 폭은 유지 |
| 디테일 | 창 프레임·범퍼·와이퍼·바퀴 허브 추가, 전륜 휠하우스와 후부 단상 계단 제작; SF02 연결 시 임시 실내 제거 | 후부 계단 높이 0.1533 m × 3단 [설정], 깊이 0.30 m [설정], 단상 높이 차 0.46 m [설정] |
| 베벨·웨이티드 노멀 | 부품별 표 베벨 유지, 문틀·유리 노멀 정리, 정적 납품 복제본 모디파이어 Apply | 지붕 0.10 m / 2 seg [설정], 최종 외피 0.04 m / 3 seg [설정]; Subdivision 불필요 |
| UV | 창틀·좌석 반복 트림, 차체 타일 PBR, 노선·그래픽만 별도 아틀라스 | H 1024 px/m [설정: 지시서], 트림 2048² px [설정], 그래픽 2048² px [설정], 패딩 16 px [설정] |

문은 차체 측면 패널을 끊은 구간에 배치되어 개방 시 외피가 남지 않는다. 문 폭은 벽체 구간 사이 명목치이며, 문틀·경첩을 반영한 유효 통과폭은 최종 제작 시 별도 검수한다. 휠하우스·가림판·단상 계단은 최종 단계에서 정리한다. 블록아웃 실내는 좌석 수를 고증한 결과가 아니며 단말기·손잡이·벨·최종 좌석은 SF02가 담당한다. SF02 연결 시 DriverSeat·DriverBack·Dashboard·Seat 접두사 부품·LightStrip을 제거하고 소켓 기준을 유지한다. Floor·RearDeck은 차량 구조로 유지한다.

## 7. 폴리곤 예산
완성 외관+임시 실내 기준이며 SF02 본체는 별도 예산. 모두 [설정].

| 부품 | 삼각형 목표 | 베벨 폭·세그먼트 | 서브디비전 | 비고 |
|---|---|---|---|---|
| 외피·지붕·휠하우스 | 16,000 [설정] | 0.04 m / 3 [설정] | 없음 | 실루엣 우선 |
| 창·프레임 | 6,000 [설정] | 0.01 m / 2 [설정] | 없음 | 유리 단면화 |
| 문·문틀 | 6,000 [설정] | 0.008 m / 2 [설정] | 없음 | 경첩 독립 |
| 바퀴·허브·조향 | 8,000 [설정] | 0.01 m / 2 [설정] | 없음 | 반복 공유 메시 |
| 미러·등·행선판·가상 그래픽 | 4,000 [설정] | 0.02 m / 2 [설정] | 없음 | 글자는 텍스처 |
| 실내 가림·바닥·임시 좌석 | 8,000 [설정] | 0.01 m / 2 [설정] | 없음 | SF02 조립 시 교체 |
| 합계 | 48,000 [설정] | – | 없음 | H 20,000~80,000 [설정: 지시서] 범위 |

블록아웃은 형상·축·치수 검증용이므로 완성 모델 예산 하한까지 세분하지 않는다. SF02 조립 씬은 임시 좌석 제거 후 실제 합계를 다시 계산한다.

## 8. 재질표
색은 INSTRUCTIONS.md 전역 팔레트 [설정]. 블록아웃 노멀 강도는 입력 텍스처가 없으므로 영값. Alpha는 불투명도이며 Glass는 단순 알파 합성, 실제 굴절 유리가 아니다.

| 재질 이름 | 색 hex (팔레트 이름) | 거칠기 | 금속성 | 노멀 강도 | 야간 발광 색·강도 | 투명도·IOR |
|---|---|---|---|---|---|---|
| M_CityBus_Paint | #2E6FB7 | 0.4 [설정] | 0.15 [설정] | 0 [설정] | 없음 / 0 [설정] | Alpha 1 / IOR 1.5 [설정] |
| M_CityBus_Frame | #F2EFE6 | 0.45 [설정] | 0.1 [설정] | 0 [설정] | 없음 / 0 [설정] | Alpha 1 / IOR 1.5 [설정] |
| M_CityBus_Glass | #A9D6F0 | 0.2 [설정] | 0 [설정] | 0 [설정] | 없음 / 0 [설정] | Alpha 0.35 / IOR 1.45 [설정] |
| M_CityBus_Rubber | #3A3D42 | 0.8 [설정] | 0 [설정] | 0 [설정] | 없음 / 0 [설정] | Alpha 1 / IOR 1.5 [설정] |
| M_CityBus_Steel | #B9B6AE | 0.45 [설정] | 0.8 [설정] | 0 [설정] | 없음 / 0 [설정] | Alpha 1 / IOR 1.5 [설정] |
| M_CityBus_Floor | #6E6A64 | 0.85 [설정] | 0 [설정] | 0 [설정] | 없음 / 0 [설정] | Alpha 1 / IOR 1.5 [설정] |
| M_CityBus_Seat | #9DB7E0 | 0.75 [설정] | 0 [설정] | 0 [설정] | 없음 / 0 [설정] | Alpha 1 / IOR 1.5 [설정] |
| M_CityBus_LED | #3A3D42 | 0.4 [설정] | 0 [설정] | 0 [설정] | 없음 / 0 [설정] | Alpha 1 / IOR 1.5 [설정] |
| M_CityBus_Headlight | #DDEBFF | 0.3 [설정] | 0 [설정] | 0 [설정] | #DDEBFF / 2 [설정] | Alpha 1 / IOR 1.5 [설정] |
| M_CityBus_TailLight | #C8423B | 0.3 [설정] | 0 [설정] | 0 [설정] | #C8423B / 1 [설정] | Alpha 1 / IOR 1.5 [설정] |
| M_CityBus_InteriorLight | #FFD9A0 | 0.5 [설정] | 0 [설정] | 0 [설정] | #FFD9A0 / 1.5 [설정] | Alpha 1 / IOR 1.5 [설정] |

팔레트 대응: Paint=일반버스 청색, Frame=오프화이트, Glass=하늘 낮, Rubber·LED=아스팔트, Steel=콘크리트, Floor=바위, Seat=감천 하늘, Headlight=쿨 화이트, TailLight=교통 적색, InteriorLight=웜 화이트. 적색을 제동등에 재사용하되 실제 차량 렌즈 색 실측으로 주장하지 않는다. 팔레트 외 색 없음.
텍스처: `T_CityBus_BaseColor`, `T_CityBus_Normal`, `T_CityBus_ORM`, `T_CityBus_Emission`. 반복 트림 2048² px [설정]와 타일 재질로 1024 px/m [설정]을 유지. 행선판·가상 그래픽은 별도 2048² px [설정] 아틀라스의 UV 영역을 교체하며 노선마다 새 메시를 만들지 않는다. ORM R=AO / G=Roughness / B=Metallic [설정]. 유리는 최종 엔진에서 정렬 오류를 확인하고 실내 컷에는 해당 유리 숨김 변형 사용.

## 9. 글자·그래픽
| 위치 | 내용 | 처리 방법 (텍스처 교체 / 가상 디자인) | 글꼴 성격 |
|---|---|---|---|
| FrontLED / SideLED / RearLED | 기본 61번 [확인: FACTS.md 일정], 변형 7·71·508·181·38·27·131번 [확인: 동일 자료] | BaseColor·Emission 교체; 블록아웃은 빈 판, 최종 제작 시 숫자 텍스처 추가 | 단순 도트 LED, 숫자 식별 우선 |
| 측면 차체 | 가상 브랜드 BLUE COAST | 가상 문자 데칼, 실운수사 로고·BIG BUS 문양 미복제 | 둥근 산세리프 |
| 정류장 안내 | 부산역 / 흰여울문화마을 / 해운대해수욕장 등 | FACTS.md SF01의 정류장명 그대로 텍스처 사용 가능 | 읽기 쉬운 고딕 |
| 실내 단말기 화면 | 가상 카드 인식 아이콘 | SF02에서 제작, 실제 앱·결제 브랜드 화면 미복제 | 픽토그램 중심 |

색 근거: 예전 부산 일반버스는 파랑, 좌석은 빨강 [확인: FACTS.md, https://www.busan.com/view/busan/view.php?code=20160923000099]. 새 디자인은 2024년 12월 [확인] 공개, 매년 200~300대 [확인] 교체, 2033년 [확인] 전체 교체 계획 [확인: FACTS.md, https://www.kukinews.com/article/view/kuk202412030032]. 따라서 기존·신규 도색 혼재를 전제로 실제 도색을 복제하지 않는 청색 가상안을 사용한다. FACTS의 내용은 수정하지 않는다.

## 10. 움직임
모든 동작 수치 [설정]. 블록아웃 스크립트는 키프레임을 자동 생성하지 않으며 검증 스크립트는 문 개방·조향·차륜 축을 시험한다.

| 부품 | 움직임 | 원점(회전 중심) 좌표 | 축 | 범위 | 속도·식 |
|---|---|---|---|---|---|
| Root | 차체 주행 | (0,0,0) | −Y, 경로 접선 | 씬 경로 | 도심 예시 8 m/s, 정류장 접근 3 m/s→0, 48 frames 감속 @24 fps |
| DoorFrontA / DoorMiddleA | 앞쪽 잎 실내 방향 회전 | (−1.225,−5.4,1.39) / (−1.225,−0.5,1.39) | 로컬 Z | 0→−90° | 24 frames, smoothstep t²(3−2t), 닫기는 역순 |
| DoorFrontB / DoorMiddleB | 뒤쪽 잎 실내 방향 회전 | (−1.225,−4.3,1.39) / (−1.225,0.7,1.39) | 로컬 Z | 0→+90° | 위와 동일; 문 잎은 +X 방향 실내로 들어옴 |
| FrontAxleR/L | 조향 | (±1.08,−3.5,.47) | 부모 Z | ±25° | 블록아웃은 평행 조향; 최종은 아래 Ackermann 식 |
| WheelFrontR/L, WheelRearR/L 및 각 Hub | 타이어·허브 함께 회전 | 각 Axle Empty의 월드 위치 | 베이크 후 로컬 X | 연속 | −Y 방향 양의 거리 s에 대해 θX=−s/0.47 rad; Hub와 Wheel에 같은 값 |
| InteriorLight / Headlight | 밤 발광 | 해당 위치 | – | 강도 표 기준 | 야간 프리셋으로 노출 정합 |
| LED 판 | 노선 교체 | 고정 | – | 메모리 내 텍스처 교체 | 외관 샷 시작 전에 교체, 주행 중 임의 변경 금지 |

최종 조향: L=5.70 m [설정], 전륜 트랙 T=2.16 m [설정]. 조향 반경 R=L/tan(|δ|), 안쪽 각 atan(L/(R−T/2)), 바깥쪽 각 atan(L/(R+T/2)); δ=0° [설정]이면 직진 처리. 핸들 최대 중앙각은 25° [설정]. −Y 주행에서 +Z 회전은 +X 쪽으로 차체가 선회하므로 +Z 조향에서 +X 바퀴를 안쪽으로 설정한다. 주행 중 문은 닫고 정차 후 개방하며 개방 시 인물·단말기를 문 스윙 영역 밖으로 둔다.

## 11. 변형
| 종류 | 내용 |
|---|---|
| 낮 / 밤 | 낮 기본 PBR, 밤은 실내 웜 화이트·전조등 쿨 화이트, 행선판은 최종 Emission 텍스처 사용 |
| 색상 변형 | 기본 청색만 제작. VEH03은 적색 도장 후보이며 좌석형·출입문·실내 구조를 별도 검증. VEH04는 축거·폭·길이·문 위치 재설계 필요 |
| LOD1 (약 50%) / LOD2 (약 15%) | 완성 목표 24,000 / 7,200 tris [설정]. LOD1 하부·실내 축약, LOD2 유리 불투명화·실내 제거·행선판 데칼 유지 |
| 행선판 | 기본 61 [설정: 현재 표시 선택], 다른 일반버스 번호는 위 목록에서 교체. 급행 1003 [확인: FACTS.md]은 VEH03에서 처리 |
| 내부 카메라 | 실내 샷에서 카메라 앞 유리를 렌더 제외, SF02 최종 부품으로 임시 좌석 교체 |

## 12. 참고 이미지 프롬프트 (영어)
`reference_prompt.txt`와 동일. 숫자는 모두 제작용 [설정], 노선 번호는 FACTS.md 목록 [확인].

```
Create an orthographic model reference sheet for a 3D modeler.
Subject: fictional Busan-style full-size low-floor city bus, rounded box silhouette, two axles, passenger entrance doors at the front and middle ON THE SAME RIGHT-HAND SIDE, driver on the left. Front points toward negative Y, Z up, vehicle passenger-right is negative X; driver-left is positive X. No manufacturer logos or real operator livery.
Design settings, not verified measurements: body length 11.00 m, body width 2.49 m, full width including mirrors 2.89 m, height including roof air conditioner 3.30 m; wheelbase 5.70 m; wheel diameter 0.94 m. Front overhang 2.00 m, rear overhang 3.30 m. Floor entry 0.34 m above ground. Front door clear opening 1.10 m wide and middle door 1.20 m wide, both 2.10 m high. Door layouts are artistic settings.
Palette: blue lower panels #2E6FB7, off-white roof and window posts #F2EFE6, pale blue glass #A9D6F0, charcoal tires and LED housings #3A3D42, concrete-colored wheel hubs #B9B6AE, warm-white interior light #FFD9A0, cool-white headlights #DDEBFF. Simplified large windshield, side glazing, blank replaceable destination LED boards at front, passenger side and rear, small paired exterior mirrors, compact rooftop air conditioner. Only route number 61 may appear, with no brand signage.
Layout: 4 views in a 2x2 grid: FRONT, RIGHT SIDE (door side), BACK, TOP. True orthographic, no perspective. All views at exactly the same scale, each inside a same-size panel large enough for the full bus. A faint 1-meter grid, aligned ground lines, and a 1.7 m human silhouette beside each view. In the right side view from negative X with Z up, the front is on the RIGHT; passenger doors are clearly visible. Top view reveals driver's position and seats through a roof-outline cutaway, clearly a conceptual interior, no real seat layout asserted.
Style: stylized miniature diorama, soft bevels, simplified forms, clean dark outlines, flat even lighting, no cast shadows, light gray background. Include a row of flat palette swatches.
Exclude actual brand logos, copied livery, actual app screens, readable commercial signage, watermarks, scenery backgrounds.
Any dimensions are artistic modeling settings. Written specification and executable blockout take precedence over this illustration.
```

이미지: `images/reference.png`. 생성 이미지의 길이·높이·축 안내·문 구조·좌석 배열·후미등 색·뷰별 배율은 실측 근거가 아니다. 프롬프트의 clear opening 표기는 형상 참고용 명목 폭이며 최종 유효 통과폭을 보증하지 않는다. 실제 치수와 문 경첩은 본 문서·PARTS가 우선한다. 이미지가 문을 접이식처럼 보여도 이 초안은 경첩축이 양 끝에 있는 독립 잎 회전으로 제작한다. 상면도는 실내 개념 컷이며 지붕 메시 제거 지시가 아니다.

## 13. 확실하지 않은 값과 필요한 사진
| 값 | 현재 값 | 태그 | 영향도 (상·중·하) | 확정에 필요한 사진 (대상·각도) |
|---|---|---|---|---|
| 차종·차체 길이·폭·높이 | 11.0 / 2.49 / 3.30 m | [설정], FACTS 범위는 [추정] | 상 | 같은 일반 저상버스 정면·정측면·후면, 옆에 성인 또는 규격 기준물 포함 |
| 축거·오버행·차륜 | 5.70 m / 2.0·3.3 m / 지름 .94 m | [설정] | 상 | 바퀴 중심과 차체 양 끝이 한 화면에 보이는 긴 거리 정측면 |
| 문 폭·힌지·개폐 방식 | 앞 1.10 m, 중간 1.20 m, 안쪽 회전 잎 | [설정] | 상 | 앞문·가운데문 닫힘 및 완전 개방, 실내에서 경첩과 문 스윙이 보이는 사진 |
| 저상 바닥·승강장 정합 | 입구 Z=.34 m, 후부 단상 .80 m | [설정] | 상 | 정류장 보도·차륜·문턱이 함께 보이는 측면과 실내 바닥 사진 |
| 미러·냉방기 | 미러 포함 폭 2.89 m, 최고점 3.30 m | [설정] | 중 | 정면 미러 양끝, 높은 위치에서 본 지붕 사선 |
| 실내 통로·좌석·단말기 | 임시 방석 .46×.48 m, 소켓 위치 표 참고 | [설정] | 상: SF02 연동 | 문 안쪽에서 운전석·단말기·통로·뒤쪽 단상이 보이는 광각 왜곡 적은 사진 |
| LED 위치·비율 | 앞 1.70×.25 m, 옆 1.50×.26 m | [설정] | 중 | 전면·우측·후면을 수평으로 찍은 사진. 회사명·로고는 복제하지 않음 |

사진이 있으면 위 각도로 제공 요청. 사진 전까지는 가상 제작안으로 진행 가능하다. 미확정값을 [확인]으로 바꾸지 않으며 FACTS.md는 유지한다.

## 14. 블록아웃 스크립트
- 파일: `blockout.py` (`templates/blockout_template.py` 복사본).
- 채운 블록: `1. 에셋 정보`, `2. 재질`, `3. 부품`; 맨 위 VERSION과 SPEC_VERSION은 v1.0으로 동기화. 공용 함수는 수정하지 않음.
- 외부 검사: `python blockout.py --self-test`. Blender 실행: `blender --background --factory-startup --python blockout.py`.
- 목표 REPORT: `dims_m=2.890x11.000x3.300 expected_m=2.890x11.000x3.300` [설정], `max_err_m` 허용 0.01 m [설정], 바닥 Z=0 [설정], 삼각형 상한 48,000 [설정].
- `CityBus_blockout.blend` / `CityBus_blockout.glb`는 이 초안의 정적 LOD0 이름 블록아웃. 완성 H 에셋은 리토폴로지·실내·텍스처·동작 제작 후 별도 검토 필요. 모디파이어 적용, 회전 0° [설정], 스케일 1 [설정], 미터 단위로 출력. GLB는 표준 Y-up 내보내기 후 Blender 재가져오기에서 Z-up 치수 확인.
- 검증 기록: `validation.md`; 블록아웃 정면·우측면 렌더는 `images/blockout_front.png`, `images/blockout_right.png`.

## (종류별 추가 섹션)
분류는 탈것. 키트·캐릭터·음식의 추가 섹션은 적용하지 않는다.

---

## Changelog
- v1.0 — 2026-11-10 — 시내버스 설계도·블록아웃·참고 이미지 최초 작성. 출입구·회전축·SF02 연결 기준 명시.
