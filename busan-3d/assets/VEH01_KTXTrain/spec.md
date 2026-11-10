# VEH01 KTX 고속열차 (선두차+객차2) 설계도

버전: v1.0 — 2026-11-10 — 설계도·블록아웃·참고 이미지 최초 작성
상태: 초안
폴더: `busan-3d/assets/VEH01_KTXTrain/`

문서의 ID·버전·날짜·섹션 번호·파일명은 식별자다. 표의 숫자는 해당 행의 근거 태그를 적용한다. 스크립트의 좌표·분할·PBR 수치는 모두 [설정]이다. 실제 차종을 혼합 복제하지 않는 가상 디자인이며, 사진 미제공 상태에서 실측을 주장하지 않는다.

## 1. 개요
| 항목 | 내용 |
|---|---|
| 등장 장면 | 1일차 [확인] 10:30 [확인] 부산역 도착 / 3일차 [확인] 16:30 [확인] 출발. 출처: FACTS.md 여행 일정 |
| 화면에서의 역할 | 길고 낮은 유선형 열차와 문 개폐로 부산 여행의 시작·끝을 전달 |
| 등급 | H |
| 가장 가까운 카메라 거리 | 문에서 1.5 m [설정]; 선두 실루엣은 12 m [설정] 이상 |
| 화면 점유율 | 선두 또는 승차문 최대 80% [설정]; 전체 편성은 측면 와이드 |

## 2. 핵심 특징
- **지켜야 할 것**
  - 긴 차체와 낮고 둥근 유선형 선두, 짙은 운전실 창.
  - 밝은 차체, 바다 딥 하부 띠, 끊기지 않는 측면 창 리듬.
  - 선두차 1량 [설정]과 객차 2량 [설정], 연결부와 분리된 바퀴.
  - 승강장 높이와 맞출 수 있는 출입문 하단 및 문 슬라이딩 여유.
- **생략·단순화할 것**
  - 실제 운행사 로고·띠 도색·제조사 문양을 가상 배색으로 대체.
  - 팬터그래프·고압 설비·정밀 하부 배관은 생략; 높이는 팬터그래프 제외.
  - 실내는 문 안쪽 가림막과 바닥만 후속 제작, 실제 좌석 배열은 미재현.
  - 차륜 플랜지·대차 스프링은 덩어리와 노멀로 축약.

## 3. 치수표
| 부위 | 가로 X (m) | 깊이 Y (m) | 높이 Z (m) | 근거 태그 | 근거·계산식 |
|---|---|---|---|---|---|
| 조립 블록아웃 전체 | 3.0 | 70.0 | 3.9 | [설정] | 22 + 23.5 × 2 + 0.5 × 2 = 70; 실제 편성의 축소 비율 아님 |
| 선두차 외피 영역 | 3.0 | 22.0 | 3.9 | [설정] | Y=-35~−13; 지붕·차륜 포함 |
| 객차 각각 | 3.0 | 23.5 | 3.9 | [설정] | 반복 가능하게 동일 길이 |
| 차량 사이 간격 | – | 0.5 | – | [설정] | 차체 끝면 간 여유, 연결 고무는 간격 내부 |
| 차체 폭 참고 범위 | 2.9~3.0 | – | – | [추정] | FACTS.md VEH01의 미확정 범위; 사진 계산은 아직 불가 |
| 레일 면~지붕 참고 범위 | – | – | 3.5~4.0 | [추정] | FACTS.md VEH01; 팬터그래프 제외 |
| 출입문 외피 판 | 0.02 | 0.90 | 2.10 | [설정] | 두께·개구 폭은 가상 설계, 높이는 지시서 기준 문 치수 채택 |
| 차륜 원형 단면 | 0.18 | 0.92 | 0.92 | [설정] | 월드 좌표 치수, 지름 0.92; 스크립트 원형 Z축을 Y회전해 X축 차축 구성 |
| 문 하단 | – | – | 1.00 | [설정] | 중심 2.05 − 높이 2.10/2; ENV01 승강장과 후속 검수 필요 |
| KTX-청룡 실제 편성 길이(참고) | – | 199.1 | – | [확인] | FACTS.md VEH01; https://www.ajunews.com/view/20240422151706070 |
| KTX-산천 실제 편성 길이(참고) | – | 201 | – | [확인] | FACTS.md VEH01; 10량 [확인], 객차 8량 [확인]; https://www.segye.com/view/20240401515589 |

사람 1.70 m [설정: INSTRUCTIONS.md 스케일 기준] 대비 높이 3.9 / 1.70 = 2.294배 [설정]. 실제 편성 길이로 개별 차량 길이를 역산하지 않는다. 전체 차량 수·차종이 정해지기 전에는 이 조립 블록을 실제 전체 편성으로 표기하지 않는다.

## 4. 정면·측면·윗면 도면
### 4-1. 주요 점 좌표 (에셋 원점 = 바닥 중앙, 단위 m)
표의 좌표는 전부 [설정]. +X는 진행 방향 기준 우측, 정면은 −Y, Z는 위. 바닥은 레일 접촉면.

| 점 이름 | x | y | z | 설명 |
|---|---|---|---|---|
| 에셋 원점 | 0 | 0 | 0 | Root Empty, 조립 AABB 바닥 중앙 |
| 코 끝 | 0 | −35 | 2.05 | LeadNose 전단 |
| 선두차 후단 | 0 | −13 | 2.3 | 선두 외피 끝 |
| 객차 A 전단 / 후단 | 0 | −12.5 / 11 | 2.3 | CoachA 외피 |
| 객차 B 전단 / 후단 | 0 | 11.5 / 35 | 2.3 | CoachB 외피 |
| 폭 양끝 | −1.5 / 1.5 | 0 | 3.8 | 지붕 최대 폭 |
| 최고점 | 0 | 0 | 3.9 | 지붕 상단 |
| 선두 우측 문 중심 | 1.49 | −15 | 2.05 | LeadDoorR0 |
| 선두 우측 앞 바퀴 축 | 1 | −31.1 | 0.46 | LeadWheelFFR |

### 4-2. 텍스트 실루엣 (가로세로 비율 유지)
ASCII는 한 칸의 가로 폭 약 0.5 m [설정], 세로 약 1 m [설정]인 문자 셀을 가정한다. 측면·윗면은 차체만 표시하며 대차·틈은 도식 생략. 정확한 비율은 좌표와 Blender 직교 뷰로 확인한다.

```
정면 (-Y에서 본 모습)      측면 (+X에서 본 모습; 왼쪽=선두)
  ____                         ______________________________________________________________________________________________________________________________________
 /####\                       /########################################################################################################################################|
|      |                    /__________________________________________________________________________________________________________________________________________|
 \_oo_/                       o o                          o o          o o                         o o          o o                         o o

윗면 (+Z에서 본 모습; 왼쪽=선두, 가로 방향으로 회전하여 표기)
    _____________________________________________________________________________________________________________________________________
  /                                                                                                                                       |
 (                                                                                                                                        |
  \______________________________________________________________________________________________________________________________________|
```

### 4-3. 치수선
좌표·길이는 모두 [설정].

| 치수선 | 시작점 → 끝점 | 길이 (m) |
|---|---|---|
| 전체 길이 | (0,−35,0) → (0,35,0) | 70 |
| 전체 폭 | (−1.5,0,0) → (1.5,0,0) | 3 |
| 전체 높이 | (0,0,0) → (0,0,3.9) | 3.9 |
| 객차 피치 | (0,−0.75,0) → (0,23.25,0) | 24 |
| 문 높이 | (1.49,−15,1) → (1.49,−15,3.1) | 2.1 |

## 5. 부품 목록
PARTS와 행별 일치. 크기·위치·회전·베벨·분할은 각 행의 [설정] 태그를 적용한다. sphere 크기는 축별 지름, cylinder 크기는 회전 전 로컬 X·Y 지름과 Z 두께다. cylinder만 로컬 Y회전 90° [설정]; 원점은 축 중심. Empty 크기는 표시용이며 실물 외곽 치수에서 제외한다. 이름은 `VEH01_KTXTrain_{부품명}_L0` [설정: 이름 규칙]로 생성한다.

| 부품명 | 도형 | 크기 X×Y×Z (m) | 위치 x,y,z (부모 기준) | 회전 x,y,z (°) | 원점(pivot) | 부모 | 재질 | 반복·대칭 | 근거 |
|---|---|---|---|---|---|---|---|---|---|
| Root | empty | (0.2, 0.2, 0.2) | (0, 0, 0) | (0, 0, 0) | center | – | – | 없음 | [설정] |
| LeadRoot | empty | (0.2, 0.2, 0.2) | (0, -24, 0) | (0, 0, 0) | center | Root | – | 없음 | [설정] |
| LeadBody | cube | (2.96, 19, 2.8) | (0, 1.5, 2.3) | (0, 0, 0) | center | LeadRoot | Body | bevel 0.12 m / 3 seg | [설정] |
| LeadRoof | cube | (3, 17, 0.2) | (0, 2.5, 3.8) | (0, 0, 0) | center | LeadRoot | Roof | bevel 0.08 m / 3 seg | [설정] |
| LeadSill | cube | (2.8, 19, 0.35) | (0, 1.5, 1.025) | (0, 0, 0) | center | LeadRoot | Sill | bevel 0.06 m / 2 seg | [설정] |
| LeadWindowsR | cube | (0.02, 14, 0.75) | (1.49, 1, 2.7) | (0, 0, 0) | center | LeadRoot | Glass | bevel 0.008 m / 2 seg | [설정] |
| LeadDoorR0 | cube | (0.02, 0.9, 2.1) | (1.49, 9, 2.05) | (0, 0, 0) | center | LeadRoot | Body | bevel 0.008 m / 2 seg | [설정] |
| LeadWindowsL | cube | (0.02, 14, 0.75) | (-1.49, 1, 2.7) | (0, 0, 0) | center | LeadRoot | Glass | bevel 0.008 m / 2 seg | [설정] |
| LeadDoorL0 | cube | (0.02, 0.9, 2.1) | (-1.49, 9, 2.05) | (0, 0, 0) | center | LeadRoot | Body | bevel 0.008 m / 2 seg | [설정] |
| LeadBogieF | cube | (1.9, 3.2, 0.35) | (0, -6, 0.6) | (0, 0, 0) | center | LeadRoot | Rubber | bevel 0.05 m / 2 seg | [설정] |
| LeadWheelFFR | cylinder | (0.92, 0.92, 0.18) | (1, -7.1, 0.46) | (0, 90, 0) | center | LeadRoot | Steel | 24 radial seg | [설정] |
| LeadWheelFFL | cylinder | (0.92, 0.92, 0.18) | (-1, -7.1, 0.46) | (0, 90, 0) | center | LeadRoot | Steel | 24 radial seg | [설정] |
| LeadWheelFBR | cylinder | (0.92, 0.92, 0.18) | (1, -4.9, 0.46) | (0, 90, 0) | center | LeadRoot | Steel | 24 radial seg | [설정] |
| LeadWheelFBL | cylinder | (0.92, 0.92, 0.18) | (-1, -4.9, 0.46) | (0, 90, 0) | center | LeadRoot | Steel | 24 radial seg | [설정] |
| LeadBogieB | cube | (1.9, 3.2, 0.35) | (0, 8, 0.6) | (0, 0, 0) | center | LeadRoot | Rubber | bevel 0.05 m / 2 seg | [설정] |
| LeadWheelBFR | cylinder | (0.92, 0.92, 0.18) | (1, 6.9, 0.46) | (0, 90, 0) | center | LeadRoot | Steel | 24 radial seg | [설정] |
| LeadWheelBFL | cylinder | (0.92, 0.92, 0.18) | (-1, 6.9, 0.46) | (0, 90, 0) | center | LeadRoot | Steel | 24 radial seg | [설정] |
| LeadWheelBBR | cylinder | (0.92, 0.92, 0.18) | (1, 9.1, 0.46) | (0, 90, 0) | center | LeadRoot | Steel | 24 radial seg | [설정] |
| LeadWheelBBL | cylinder | (0.92, 0.92, 0.18) | (-1, 9.1, 0.46) | (0, 90, 0) | center | LeadRoot | Steel | 24 radial seg | [설정] |
| CoachARoot | empty | (0.2, 0.2, 0.2) | (0, -0.75, 0) | (0, 0, 0) | center | Root | – | 없음 | [설정] |
| CoachABody | cube | (2.96, 23.5, 2.8) | (0, 0, 2.3) | (0, 0, 0) | center | CoachARoot | Body | bevel 0.12 m / 3 seg | [설정] |
| CoachARoof | cube | (3, 23.5, 0.2) | (0, 0, 3.8) | (0, 0, 0) | center | CoachARoot | Roof | bevel 0.08 m / 3 seg | [설정] |
| CoachASill | cube | (2.8, 23.5, 0.35) | (0, 0, 1.025) | (0, 0, 0) | center | CoachARoot | Sill | bevel 0.06 m / 2 seg | [설정] |
| CoachAWindowsR | cube | (0.02, 18, 0.75) | (1.49, 0, 2.7) | (0, 0, 0) | center | CoachARoot | Glass | bevel 0.008 m / 2 seg | [설정] |
| CoachADoorR0 | cube | (0.02, 0.9, 2.1) | (1.49, -10.3, 2.05) | (0, 0, 0) | center | CoachARoot | Body | bevel 0.008 m / 2 seg | [설정] |
| CoachADoorR1 | cube | (0.02, 0.9, 2.1) | (1.49, 10.3, 2.05) | (0, 0, 0) | center | CoachARoot | Body | bevel 0.008 m / 2 seg | [설정] |
| CoachAWindowsL | cube | (0.02, 18, 0.75) | (-1.49, 0, 2.7) | (0, 0, 0) | center | CoachARoot | Glass | bevel 0.008 m / 2 seg | [설정] |
| CoachADoorL0 | cube | (0.02, 0.9, 2.1) | (-1.49, -10.3, 2.05) | (0, 0, 0) | center | CoachARoot | Body | bevel 0.008 m / 2 seg | [설정] |
| CoachADoorL1 | cube | (0.02, 0.9, 2.1) | (-1.49, 10.3, 2.05) | (0, 0, 0) | center | CoachARoot | Body | bevel 0.008 m / 2 seg | [설정] |
| CoachABogieF | cube | (1.9, 3.2, 0.35) | (0, -8, 0.6) | (0, 0, 0) | center | CoachARoot | Rubber | bevel 0.05 m / 2 seg | [설정] |
| CoachAWheelFFR | cylinder | (0.92, 0.92, 0.18) | (1, -9.1, 0.46) | (0, 90, 0) | center | CoachARoot | Steel | 24 radial seg | [설정] |
| CoachAWheelFFL | cylinder | (0.92, 0.92, 0.18) | (-1, -9.1, 0.46) | (0, 90, 0) | center | CoachARoot | Steel | 24 radial seg | [설정] |
| CoachAWheelFBR | cylinder | (0.92, 0.92, 0.18) | (1, -6.9, 0.46) | (0, 90, 0) | center | CoachARoot | Steel | 24 radial seg | [설정] |
| CoachAWheelFBL | cylinder | (0.92, 0.92, 0.18) | (-1, -6.9, 0.46) | (0, 90, 0) | center | CoachARoot | Steel | 24 radial seg | [설정] |
| CoachABogieB | cube | (1.9, 3.2, 0.35) | (0, 8, 0.6) | (0, 0, 0) | center | CoachARoot | Rubber | bevel 0.05 m / 2 seg | [설정] |
| CoachAWheelBFR | cylinder | (0.92, 0.92, 0.18) | (1, 6.9, 0.46) | (0, 90, 0) | center | CoachARoot | Steel | 24 radial seg | [설정] |
| CoachAWheelBFL | cylinder | (0.92, 0.92, 0.18) | (-1, 6.9, 0.46) | (0, 90, 0) | center | CoachARoot | Steel | 24 radial seg | [설정] |
| CoachAWheelBBR | cylinder | (0.92, 0.92, 0.18) | (1, 9.1, 0.46) | (0, 90, 0) | center | CoachARoot | Steel | 24 radial seg | [설정] |
| CoachAWheelBBL | cylinder | (0.92, 0.92, 0.18) | (-1, 9.1, 0.46) | (0, 90, 0) | center | CoachARoot | Steel | 24 radial seg | [설정] |
| CoachBRoot | empty | (0.2, 0.2, 0.2) | (0, 23.25, 0) | (0, 0, 0) | center | Root | – | 없음 | [설정] |
| CoachBBody | cube | (2.96, 23.5, 2.8) | (0, 0, 2.3) | (0, 0, 0) | center | CoachBRoot | Body | bevel 0.12 m / 3 seg | [설정] |
| CoachBRoof | cube | (3, 23.5, 0.2) | (0, 0, 3.8) | (0, 0, 0) | center | CoachBRoot | Roof | bevel 0.08 m / 3 seg | [설정] |
| CoachBSill | cube | (2.8, 23.5, 0.35) | (0, 0, 1.025) | (0, 0, 0) | center | CoachBRoot | Sill | bevel 0.06 m / 2 seg | [설정] |
| CoachBWindowsR | cube | (0.02, 18, 0.75) | (1.49, 0, 2.7) | (0, 0, 0) | center | CoachBRoot | Glass | bevel 0.008 m / 2 seg | [설정] |
| CoachBDoorR0 | cube | (0.02, 0.9, 2.1) | (1.49, -10.3, 2.05) | (0, 0, 0) | center | CoachBRoot | Body | bevel 0.008 m / 2 seg | [설정] |
| CoachBDoorR1 | cube | (0.02, 0.9, 2.1) | (1.49, 10.3, 2.05) | (0, 0, 0) | center | CoachBRoot | Body | bevel 0.008 m / 2 seg | [설정] |
| CoachBWindowsL | cube | (0.02, 18, 0.75) | (-1.49, 0, 2.7) | (0, 0, 0) | center | CoachBRoot | Glass | bevel 0.008 m / 2 seg | [설정] |
| CoachBDoorL0 | cube | (0.02, 0.9, 2.1) | (-1.49, -10.3, 2.05) | (0, 0, 0) | center | CoachBRoot | Body | bevel 0.008 m / 2 seg | [설정] |
| CoachBDoorL1 | cube | (0.02, 0.9, 2.1) | (-1.49, 10.3, 2.05) | (0, 0, 0) | center | CoachBRoot | Body | bevel 0.008 m / 2 seg | [설정] |
| CoachBBogieF | cube | (1.9, 3.2, 0.35) | (0, -8, 0.6) | (0, 0, 0) | center | CoachBRoot | Rubber | bevel 0.05 m / 2 seg | [설정] |
| CoachBWheelFFR | cylinder | (0.92, 0.92, 0.18) | (1, -9.1, 0.46) | (0, 90, 0) | center | CoachBRoot | Steel | 24 radial seg | [설정] |
| CoachBWheelFFL | cylinder | (0.92, 0.92, 0.18) | (-1, -9.1, 0.46) | (0, 90, 0) | center | CoachBRoot | Steel | 24 radial seg | [설정] |
| CoachBWheelFBR | cylinder | (0.92, 0.92, 0.18) | (1, -6.9, 0.46) | (0, 90, 0) | center | CoachBRoot | Steel | 24 radial seg | [설정] |
| CoachBWheelFBL | cylinder | (0.92, 0.92, 0.18) | (-1, -6.9, 0.46) | (0, 90, 0) | center | CoachBRoot | Steel | 24 radial seg | [설정] |
| CoachBBogieB | cube | (1.9, 3.2, 0.35) | (0, 8, 0.6) | (0, 0, 0) | center | CoachBRoot | Rubber | bevel 0.05 m / 2 seg | [설정] |
| CoachBWheelBFR | cylinder | (0.92, 0.92, 0.18) | (1, 6.9, 0.46) | (0, 90, 0) | center | CoachBRoot | Steel | 24 radial seg | [설정] |
| CoachBWheelBFL | cylinder | (0.92, 0.92, 0.18) | (-1, 6.9, 0.46) | (0, 90, 0) | center | CoachBRoot | Steel | 24 radial seg | [설정] |
| CoachBWheelBBR | cylinder | (0.92, 0.92, 0.18) | (1, 9.1, 0.46) | (0, 90, 0) | center | CoachBRoot | Steel | 24 radial seg | [설정] |
| CoachBWheelBBL | cylinder | (0.92, 0.92, 0.18) | (-1, 9.1, 0.46) | (0, 90, 0) | center | CoachBRoot | Steel | 24 radial seg | [설정] |
| LeadNose | sphere | (2.96, 6, 2.3) | (0, -8, 2.05) | (0, 0, 0) | center | LeadRoot | Body | 32 radial seg | [설정] |
| LeadCockpit | sphere | (2.3, 2, 1) | (0, -8, 2.9) | (0, 0, 0) | center | LeadRoot | Glass | 24 radial seg | [설정] |
| HeadlightR | sphere | (0.25, 0.18, 0.18) | (0.75, -10.4, 1.6) | (0, 0, 0) | center | LeadRoot | Light | 16 radial seg | [설정] |
| HeadlightL | sphere | (0.25, 0.18, 0.18) | (-0.75, -10.4, 1.6) | (0, 0, 0) | center | LeadRoot | Light | 16 radial seg | [설정] |
| CouplerA | cube | (1.8, 0.5, 2.5) | (0, -12.75, 2.2) | (0, 0, 0) | center | Root | Rubber | bevel 0.05 m / 2 seg | [설정] |
| CouplerB | cube | (1.8, 0.5, 2.5) | (0, 11.25, 2.2) | (0, 0, 0) | center | Root | Rubber | bevel 0.05 m / 2 seg | [설정] |

## 6. 모델링 순서
| 단계 | 작업 | 쓸 모디파이어·설정값 |
|---|---|---|
| 블록아웃 | 실행 후 REPORT를 확인, Root 아래 차량별 분리 유지 | 모든 형상은 PARTS 표 기준 [설정] |
| 1차 형태 | LeadNose와 LeadBody의 겹침을 연결하고 선두 지붕을 코 쪽으로 낮춤; 최외곽은 유지 | 선두 길이 22 m [설정], 폭 3 m [설정], 최고점 3.9 m [설정]; 대칭 X |
| 디테일 | 창 띠에 창 분할을 텍스처로 추가; 문 개구부를 실제로 뚫고 문틀·후면 가림막·바닥 추가; 객차 후단은 평평한 연결면 | 창 분할 피치 1.8 m [설정], 기둥 폭 0.08 m [설정], 문 여유 0.02 m [설정]; 창과 문 겹침 부분 삭제 |
| 베벨·웨이티드 노멀 | 외피 베벨은 표 값 유지, 문은 표면 노멀 정리, 최종 export 복제본에서 Apply | 차체 0.12 m / 3 seg [설정], 지붕 0.08 m / 3 seg [설정]; Weighted Normal 사용 |
| UV | 차체·지붕은 타일 재질, 문·창 테두리 트림, 가상 그래픽만 데칼 | H 1024 px/m [설정: 지시서], 트림 2048² px [설정], 전체 차량을 단일 고유 UV로 펴지 않음 |

블록아웃에서는 외피가 닫혀 있고 문 판이 외피에 겹쳐 있다. 문 개폐를 보이는 최종 모델에서는 위 개구부 작업을 반드시 완료한다. 구형 코와 상자 외피의 겹침은 볼륨 확인용이며 최종 곡면은 리토폴로지한다.

## 7. 폴리곤 예산
완성 에셋 목표값으로 모두 [설정]. 블록아웃을 예산 하한까지 불필요하게 세분하지 않는다.

| 부품 | 삼각형 목표 | 베벨 폭·세그먼트 | 서브디비전 | 비고 |
|---|---|---|---|---|
| 차체 외피 | 9,000 [설정] | 0.12 m / 3 [설정] | 없음 | 문 구멍 포함 |
| 선두 코 | 5,000 [설정] | 접합부 수동 정리 | 최대 1단 [설정], Apply 후 계수 | 외피 접합 포함 |
| 지붕 | 3,000 [설정] | 0.08 m / 3 [설정] | 없음 | 팬터그래프 생략 |
| 차륜·대차 | 8,000 [설정] | 최대 0.02 m / 2 [설정] | 없음 | 좌우 바퀴 독립 |
| 유리 | 3,000 [설정] | 테두리 0.008 m / 2 [설정] | 없음 | 불투명 스타일 유리 |
| 문·문틀 | 4,000 [설정] | 0.008 m / 2 [설정] | 없음 | 후속 개구부 작업 |
| 하부·실내 가림 | 5,000 [설정] | 0.06 m / 2 [설정] | 없음 | 좌석 생략 |
| 연결부 | 2,000 [설정] | 0.05 m / 2 [설정] | 없음 | 고무 주름 노멀 |
| 등·그래픽 | 1,000 [설정] | 메시 최소화 | 없음 | 전조등만 발광 |
| 합계 | 40,000 [설정] | 위 합계 | – | H 범위 20,000~80,000 [설정: 지시서] 내부 |

## 8. 재질표
색은 INSTRUCTIONS.md 전역 팔레트 [설정], 실제 열차 도색을 복제하지 않는다. 아래 노멀 강도는 블록아웃 기준이며 텍스처 없는 단순 Principled BSDF다. Alpha는 불투명도이며 Glass도 불투명으로 처리해 실내 미제작 상태를 가린다.

| 재질 이름 | 색 hex (팔레트 이름) | 거칠기 | 금속성 | 노멀 강도 | 야간 발광 색·강도 | 투명도·IOR |
|---|---|---|---|---|---|---|
| M_KTXTrain_Body | #F2EFE6 | 0.38 [설정] | 0.15 [설정] | 0 [설정] | 없음 / 0 [설정] | Alpha 1 [설정]; IOR 1.5 [설정] |
| M_KTXTrain_Sill | #0E4C77 | 0.42 [설정] | 0.2 [설정] | 0 [설정] | 없음 / 0 [설정] | Alpha 1 [설정]; IOR 1.5 [설정] |
| M_KTXTrain_Roof | #A9D6F0 | 0.45 [설정] | 0.15 [설정] | 0 [설정] | 없음 / 0 [설정] | Alpha 1 [설정]; IOR 1.5 [설정] |
| M_KTXTrain_Glass | #3A3D42 | 0.18 [설정] | 0.1 [설정] | 0 [설정] | 없음 / 0 [설정] | Alpha 1 [설정]; IOR 1.45 [설정] |
| M_KTXTrain_Steel | #B9B6AE | 0.5 [설정] | 0.8 [설정] | 0 [설정] | 없음 / 0 [설정] | Alpha 1 [설정]; IOR 1.5 [설정] |
| M_KTXTrain_Rubber | #3A3D42 | 0.8 [설정] | 0 [설정] | 0 [설정] | 없음 / 0 [설정] | Alpha 1 [설정]; IOR 1.5 [설정] |
| M_KTXTrain_Light | #DDEBFF | 0.3 [설정] | 0 [설정] | 0 [설정] | #DDEBFF / 2 [설정] | Alpha 1 [설정]; IOR 1.5 [설정] |

Body=오프화이트, Sill=바다 딥, Roof=하늘 낮, Glass·Rubber=아스팔트, Steel=콘크리트, Light=쿨 화이트. 색 외 예외 없음.
텍스처: `T_KTXTrain_BaseColor`, `T_KTXTrain_Normal`, `T_KTXTrain_ORM`, `T_KTXTrain_Emission`. 해상도 2048² px [설정] 트림·타일; ORM은 R=AO, G=Roughness, B=Metallic [설정]. 근접 문 그래픽은 필요 시 4096² px [설정] 별도 아틀라스; 패딩 16 px [설정]. 트림을 반복하여 1024 px/m [설정]을 확보하고 긴 차체 전체를 단일 저밀도 고유 맵에 넣지 않는다. 블록아웃에는 이미지 텍스처가 없다.

## 9. 글자·그래픽
| 위치 | 내용 | 처리 방법 (텍스처 교체 / 가상 디자인) | 글꼴 성격 |
|---|---|---|---|
| 측면 문 옆 | 가상 서비스명 BLUE HARBOR | 최종 모델에서 데칼, 실제 회사명·로고 금지 | 단정한 산세리프 |
| 객차 표식 | A / B | 텍스처 교체, 실제 차량번호 생략 | 굵은 산세리프 |
| 화면 자막 | KTX 부산 도착 / 출발 | 편집 UI에만 표시, 운행사 로고 미사용 | 읽기 쉬운 고딕 |

## 10. 움직임
표의 수치는 전부 [설정]. 애니메이션은 블록아웃 스크립트에 자동 생성되지 않으며 다음 규약으로 후속 제작한다.

| 부품 | 움직임 | 원점(회전 중심) 좌표 | 축 | 범위 | 속도·식 |
|---|---|---|---|---|---|
| Root | 직선 주행 | (0,0,0) | −Y | 샷별 경로 | 역내 2 m/s, 정지 진입은 72 frames 감속, 24 fps |
| 모든 Wheel | 바퀴 회전 | PARTS의 각 wheel.location + 해당 차량 Root 위치 | 부모 X축; 로컬은 Z축 | 연속 회전 | 부호 포함 거리 s를 −Y 주행 양수로 두면 θX=−s/0.46 rad; 회전 0 적용 후 부모 X로 구동 |
| LeadDoorR0 | 외측 플러그 후 뒤로 슬라이드 | 로컬 (1.49,9,2.05), 월드 (1.49,−15,2.05) | +X 후 +Y | X +0.08 m, Y +1.0 m | 6 frames 플러그, 이어 18 frames 슬라이드 |
| 우측 객차 문 | 위와 같음 | PARTS 각 DoorR 중심 | +X 후 +Y | 위와 동일 | 개방 24 frames, 닫기 역순 |
| 좌측 문 | 반대쪽 승강장 샷에만 사용 | PARTS 각 DoorL 중심 | −X 후 +Y | X −0.08 m, Y +1.0 m | 반대편 문 동시 개방 금지 |
| 차량 Root | 커브 이동 | 각 차량 Root 접촉면 | 경로 접선 Z 회전 | 샷에서 별도 계산 | 객차 중심 경로 간격 24 m, 바퀴-레일 정합 우선 |

선두 Root의 Y 위치 −24 m [설정]는 대차 배치를 위한 로컬 기준이며 차체 상자 중심과 다르다. 곡선 주행은 단순한 전체 Root 회전만으로 처리하지 않는다. 로컬 축을 유지한 리그 원본과 회전 0° [설정]·스케일 1 [설정]인 정적 납품 복제본을 분리한다.

## 11. 변형
| 종류 | 내용 |
|---|---|
| 낮 / 밤 | 낮은 기본 재질, 밤은 Light 발광 2 [설정] 유지; 실내 미제작 창은 외부 조명 반사로만 처리 |
| 색상 변형 | 기본안만 제작, 예비안은 Roof를 민트 #8FC9B9 [설정]로 변경 가능 |
| LOD1 (약 50%) / LOD2 (약 15%) | 완성 목표 기준 20,000 / 6,000 tris [설정]; LOD1 하부 축약, LOD2 창·문을 데칼로 합침 |
| 객차 재사용 | CoachA 계층 링크 복제 후 +Y 24 m [설정] 이동. CoachB는 독립 이름의 동일 규격 예시. 곡선은 차량별 배치 |

실제 전체 편성 재현은 보류한다. 목표 길이 199.1 m [확인] 또는 201 m [확인] 중 어느 차종인지 정하고 개별 차량 길이·연결 구조를 확인해야 하며, 현재 24 m [설정] 피치를 그대로 반복해 실측 편성이라고 주장하지 않는다.

## 12. 참고 이미지 프롬프트 (영어)
`reference_prompt.txt`와 동일. 프롬프트의 숫자 전체는 [설정]; 사람 기준은 지시서의 스케일 기준이다.

```
Create an orthographic model reference sheet for a 3D modeler.
Subject: a fictional Korean high-speed train inspired only by a recognizable streamlined silhouette, one lead car followed by two passenger coaches. No actual manufacturer, operator or train livery. Model-design dimensions (all artistic settings, not measurements): assembled length 70 m, width 3 m, rail-contact-to-roof height 3.9 m, lead car 22 m long, each coach 23.5 m long, two coupling gaps 0.5 m. Front is negative Y, up is Z. Long low tapered rounded nose, dark cockpit glazing, continuous dark side window strips, simplified steel wheel bogies, flush passenger sliding doors. Off-white body, deep ocean blue lower sill, pale sky blue roof, charcoal glazing.
Layout: four views in a two-by-two grid: FRONT, RIGHT SIDE, BACK, TOP, true orthographic, no perspective. Keep train length undistorted. The long side and top views use the same scale; short end views may occupy blank space but must not be enlarged. A faint one-meter grid and a 1.7 m human silhouette beside each view communicate scale. Any dimensions shown are design settings.
Style: stylized miniature diorama, soft bevels, simplified forms, clean dark outlines, flat even lighting, no cast shadows, light gray background.
Include a row of flat color swatches: #F2EFE6 #0E4C77 #A9D6F0 #3A3D42 #B9B6AE #DDEBFF.
Exclude brand logos, actual livery graphics, readable signage, watermarks, scenery backgrounds.
This is an illustrative shape reference; the written specification and executable blockout determine exact geometry.
```

이미지: `images/reference.png`. 생성 이미지의 정면·후면은 측면과 스케일이 다를 수 있고 후면을 선두처럼 둥글게 묘사할 수 있다. 후면은 객차의 평평한 연결면으로 만든다. 이미지의 표기·비율은 실측 근거로 쓰지 않으며 치수표·좌표·블록아웃이 우선한다.

## 13. 확실하지 않은 값과 필요한 사진
| 값 | 현재 값 | 태그 | 영향도 (상·중·하) | 확정에 필요한 사진 (대상·각도) |
|---|---|---|---|---|
| 차종과 개별 길이 | 가상 선두 22 m, 객차 23.5 m | [설정] | 상 | 사용할 열차의 전체 측면, 차종 식별 가능한 선두와 객차 연결부 사진 |
| 폭·높이 | 3.0 / 3.9 m 채택; 참고 범위 2.9~3.0 / 3.5~4.0 m | [설정] / [추정] | 상 | 동일 차종 정면·측면, 옆에 선 성인 또는 치수 알려진 기준물 포함 |
| 선두 곡률·운전실 창 | 코 길이 6 m, 창 2.3×2×1 m | [설정] | 상 | 선두 정면·직측면·위쪽 사선, 렌즈 왜곡 적은 사진 |
| 출입문·승강장 정합 | 문 하단 Z=1.00 m, 높이 2.10 m | [설정] | 상 | 부산역 해당 승강장에서 문 열린 측면, 승강장과 레일·문 하단이 함께 보이는 사진 |
| 차륜·대차 | 지름 0.92 m, 객차 대차 중심 간격 16 m | [설정] | 중 | 차륜 수와 대차 위치가 드러나는 수평 측면 사진 |
| 창·문 배열 | 창 띠와 간략 문 판 | [설정] | 중 | 객차 전체 측면 및 출입문 근접 사진, 실제 글자는 복제하지 않음 |
| 종단면·연결 구조 | 고무 직육면체 연결부, 객차 평면 후단 | [설정] | 중 | 객차 연결부 정측면·후면 사선 사진 |

위 사진이 있으면 제공 요청. 제공 전까지 이 초안 설정으로 모델링 가능하며 FACTS.md의 확인값은 변경하지 않는다.

## 14. 블록아웃 스크립트
- 파일: `blockout.py` (`templates/blockout_template.py` 복사본).
- 채운 블록: `1. 에셋 정보`, `2. 재질`, `3. 부품`; 버전 헤더도 동기화. 공용 함수는 원문 그대로 유지.
- `python blockout.py --self-test` 입력 검사 후 `blender --background --factory-startup --python blockout.py` 실행.
- 목표 로그: `[REPORT] dims_m=3.000x70.000x3.900 expected_m=3.000x70.000x3.900 max_err_m=0.0000` [설정]; 허용 오차 0.01 m [설정]. 삼각형 상한 40,000 [설정], min_z=0 [설정].
- `KTXTrain_blockout.blend`와 `KTXTrain_blockout.glb`는 이 초안의 생성 결과이며 완성 H 에셋이 아니다. 텍스처·문 개구부·리그·애니메이션은 위 제작 순서로 완성한다. 정적 출력은 모디파이어 Apply, scale=1 [설정], rotation=0 [설정], 미터 단위. glTF는 표준 Y-up으로 내보내고 Blender 재가져오기 후 Z-up 외곽을 검사한다.
- Blender 실행 및 export 검증 결과는 `validation.md`에 기록한다.

## (종류별 추가 섹션)
탈것 단일 에셋으로 키트·캐릭터·음식 추가 섹션은 적용하지 않는다.

---

## Changelog
- v1.0 — 2026-11-10 — 설계도·블록아웃·참고 프롬프트·참고 이미지 최초 작성. 실측 미확정 항목은 설정으로 분리.
