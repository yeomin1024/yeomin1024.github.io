# MAP04 탈것 토큰 6종 3D 설계도

버전: v1.0 — 2026-11-11 — 지도용 탈것 토큰 6종 치수·재질·동작과 참고 이미지 최초 작성
상태: 설계도
폴더: `busan-3d/assets/MAP04_TransitTokens/`

> 이 문서의 치수와 좌표가 참고 이미지보다 우선한다. 모든 형상·치수는 실제 차량을 재현한 값이 아니라 지도 위에서 구분하기 위한 [설정]이다. 실제 로고·노선 번호·도색 패턴은 사용하지 않는다.

## 1. 개요
| 항목 | 내용 |
|---|---|
| 등장 장면 | [확인] FACTS.md 1장의 KTX·일반버스·급행버스·마을버스·해변열차·스카이캡슐 이동 구간 |
| 화면에서의 역할 | MAP01 위에서 이동 수단의 종류와 이동 방향을 즉시 구분하는 단순 3D 픽토그램 |
| 등급 | B [설정] |
| 가장 가까운 카메라 거리 | 지도 장면 카메라에서 0.45 map unit [설정] |
| 화면 점유율 | 토큰 1개가 프레임 너비의 최대 12% [설정] |

- 원본 에셋은 [설정] 1 unit = 1 m, Z-up, 정면 -Y, 각 토큰의 바닥 중앙이 원점이다.
- MAP01 장면에 배치할 때 각 Root에 [설정] 균일 배율 0.08을 적용하고 지형보다 [설정] 0.04 map unit 위에 둔다.
- 위 배율은 실물 축척이 아니라 가독성을 위한 표시 배율이다. 영상 자막에는 [설정] “이동 경로·탈것 아이콘은 개략”을 쓴다.

## 2. 핵심 특징
- **지켜야 할 것**
  1. 여섯 토큰은 같은 베벨·창·바퀴 언어를 쓰되 실루엣과 지정색만으로 구분된다 [설정].
  2. 일반·급행버스는 같은 길이, 마을버스는 25% 짧다 [설정].
  3. KTX 토큰은 길고 낮은 몸체와 둥근 쐐기형 코, 해변열차는 큰 직사각 창 띠, 스카이캡슐은 둥근 세로형 객실과 하부 썰매가 핵심이다 [설정].
  4. 지도에서 읽히도록 모든 창은 어두운 단일 덩어리, 바퀴·하부는 아스팔트색 단일 덩어리로 만든다 [설정].
- **생략·단순화할 것**
  1. 실제 제조사·운영사 로고, 노선 번호, 행선판, 실제 도색 패턴을 모두 생략한다.
  2. 문, 좌석, 와이퍼, 램프 내부, 대차·현가장치, 레일의 실제 구조를 생략한다.
  3. 실제 KTX·부산버스·블루라인파크 차량의 고유 외형을 복제하지 않는다.
  4. 텍스처를 쓰지 않고 재질색과 간단한 형상만 쓴다 [설정].

## 3. 치수표
| 부위 | 가로 X (m) | 깊이 Y (m) | 높이 Z (m) | 근거 태그 | 근거·계산식 |
|---|---:|---:|---:|---|---|
| 일반버스 토큰 전체 | 0.90 | 2.40 | 0.90 | [설정] | 지도용 정규화 크기 |
| 급행버스 토큰 전체 | 0.90 | 2.40 | 0.85 | [설정] | 일반버스보다 낮은 실루엣 |
| 마을버스 토큰 전체 | 0.90 | 1.80 | 0.85 | [설정] | 2.40 × 0.75 = 1.80 |
| KTX 토큰 전체 | 0.75 | 2.80 | 0.75 | [설정] | 버스보다 길고 낮게 정규화 |
| 해변열차 토큰 전체 | 0.90 | 2.10 | 0.85 | [설정] | 큰 창 띠가 보이는 중간 길이 |
| 스카이캡슐 토큰 전체 | 0.90 | 1.10 | 1.10 | [설정] | 짧고 높은 세로형 객실 |
| MAP01 표시 배율 | 0.08 | 0.08 | 0.08 | [설정] | 지도 너비의 약 7~9% 길이로 표시 |
| MAP01 바닥 오프셋 | – | – | 0.04 map unit | [설정] | 지형·루트와 겹치지 않게 띄움 |

사람(1.70 m) 대비 비율은 실물 비교에 쓰지 않는다. 여섯 토큰의 크기는 실제 차량 치수가 아닌 지도 아이콘 [설정]이다.

## 4. 정면·측면·윗면 도면
### 4-1. 주요 점 좌표 (에셋 원점 = 바닥 중앙, 단위 m)
각 토큰은 독립 Root를 가지며 아래 좌표는 모두 [설정]이다.

| 점 이름 | x | y | z | 설명 |
|---|---:|---:|---:|---|
| BusStd front / rear | 0 | -1.20 / 1.20 | 0.45 | 일반버스 앞·뒤 중심 |
| BusExpress front / rear | 0 | -1.20 / 1.20 | 0.425 | 급행버스 앞·뒤 중심 |
| BusVillage front / rear | 0 | -0.90 / 0.90 | 0.425 | 마을버스 앞·뒤 중심 |
| KTX nose / rear | 0 | -1.40 / 1.40 | 0.40 | KTX 코 끝·뒤 끝 |
| BeachTrain front / rear | 0 | -1.05 / 1.05 | 0.425 | 해변열차 앞·뒤 중심 |
| SkyCapsule front / rear | 0 | -0.55 / 0.55 | 0.58 | 캡슐 앞·뒤 중심 |
| 모든 토큰 좌우 끝 | -X/2 / X/2 | 0 | Z/2 | 3번 전체 치수의 X·Z 사용 |

### 4-2. 텍스트 실루엣 (가로세로 비율 유지)
```
정면(-Y)                 측면(+X)                         윗면(+Z)
일반/급행  ┌────┐        ┌──────────────────┐             ╭──────────────────╮
버스       │████│        │██████████████████│             ╰──────────────────╯
           └o──o┘        o                o

마을버스   ┌────┐        ┌─────────────┐                  ╭─────────────╮
           │████│        │█████████████│                  ╰─────────────╯
           └o──o┘        o           o

KTX        ╭────╮        ╭◀──────────────────╮            ◀──────────────────╮
           │████│        ╰──o──────────o─────╯            ◀──────────────────╯
           ╰o──o╯

해변열차   ╭────╮        ╭────────────────╮               ╭────────────────╮
           │████│        │████████████████│               ╰────────────────╯
           ╰o──o╯        o              o

캡슐       ╭────╮        ╭───────╮                       ╭───────╮
           │████│        │███████│                       │       │
           ╰─━━─╯        ╰──━━───╯                       ╰───────╯
```

### 4-3. 치수선
| 치수선 | 시작점 → 끝점 | 길이 (m) |
|---|---|---:|
| 일반·급행버스 길이 | (0,-1.20,0) → (0,1.20,0) | 2.40 |
| 마을버스 길이 | (0,-0.90,0) → (0,0.90,0) | 1.80 |
| KTX 길이 | (0,-1.40,0) → (0,1.40,0) | 2.80 |
| 해변열차 길이 | (0,-1.05,0) → (0,1.05,0) | 2.10 |
| 스카이캡슐 길이 | (0,-0.55,0) → (0,0.55,0) | 1.10 |
| 버스·해변열차 폭 | (-0.45,0,0) → (0.45,0,0) | 0.90 |
| KTX 폭 | (-0.375,0,0) → (0.375,0,0) | 0.75 |
| 스카이캡슐 높이 | (0,0,0) → (0,0,1.10) | 1.10 |

## 5. 부품 목록
각 Root는 독립 납품 단위다. 위치는 해당 Root 기준이며 모든 행은 [설정]이다. mirror X는 원본과 대칭 부품을 함께 만든다는 뜻이다.

| 부품명 | 도형 | 크기 X×Y×Z (m) | 위치 x,y,z (부모 기준) | 회전 x,y,z (°) | 원점(pivot) | 부모 | 재질 | 반복·대칭 | 근거 |
|---|---|---|---|---|---|---|---|---|---|
| BusStdRoot | empty | 0.10×0.10×0.10 | 0,0,0 | 0,0,0 | center | – | – | 없음 | [설정] |
| BusStdBody | cube | 0.86×2.40×0.62 | 0,0,0.53 | 0,0,0 | center | BusStdRoot | BusBlue | bevel 0.06/3 | [설정] |
| BusStdRoof | cube | 0.90×2.16×0.12 | 0,0.05,0.84 | 0,0,0 | center | BusStdRoot | BusBlue | bevel 0.05/3 | [설정] |
| BusStdFrontGlass | cube | 0.72×0.04×0.32 | 0,-1.17,0.64 | 0,0,0 | center | BusStdRoot | DarkGlass | bevel 0.02/2 | [설정] |
| BusStdSideGlassR | cube | 0.03×1.50×0.30 | 0.435,-0.10,0.65 | 0,0,0 | center | BusStdRoot | DarkGlass | mirror X | [설정] |
| BusStdWheelFR | cylinder | 0.30×0.30×0.10 | 0.40,-0.72,0.15 | 0,90,0 | center | BusStdRoot | Asphalt | mirror X, rear y=0.72 | [설정] |
| BusStdLampR | cube | 0.12×0.03×0.10 | 0.25,-1.18,0.36 | 0,0,0 | center | BusStdRoot | OffWhite | mirror X | [설정] |
| BusExpressRoot | empty | 0.10×0.10×0.10 | 0,0,0 | 0,0,0 | center | – | – | 없음 | [설정] |
| BusExpressBody | cube | 0.86×2.40×0.58 | 0,0,0.50 | 0,0,0 | center | BusExpressRoot | ExpressRed | bevel 0.06/3 | [설정] |
| BusExpressRoof | cube | 0.90×2.14×0.11 | 0,0.06,0.795 | 0,0,0 | center | BusExpressRoot | ExpressRed | bevel 0.05/3 | [설정] |
| BusExpressFrontGlass | cube | 0.72×0.05×0.30 | 0,-1.16,0.62 | -12,0,0 | center | BusExpressRoot | DarkGlass | bevel 0.02/2 | [설정] |
| BusExpressSideGlassR | cube | 0.03×1.62×0.29 | 0.435,-0.04,0.62 | 0,0,0 | center | BusExpressRoot | DarkGlass | mirror X | [설정] |
| BusExpressWheelFR | cylinder | 0.30×0.30×0.10 | 0.40,-0.72,0.15 | 0,90,0 | center | BusExpressRoot | Asphalt | mirror X, rear y=0.72 | [설정] |
| BusExpressLampR | cube | 0.12×0.03×0.09 | 0.25,-1.18,0.34 | 0,0,0 | center | BusExpressRoot | OffWhite | mirror X | [설정] |
| BusVillageRoot | empty | 0.10×0.10×0.10 | 0,0,0 | 0,0,0 | center | – | – | 없음 | [설정] |
| BusVillageBody | cube | 0.86×1.80×0.60 | 0,0,0.51 | 0,0,0 | center | BusVillageRoot | VillageGreen | bevel 0.06/3 | [설정] |
| BusVillageRoof | cube | 0.90×1.58×0.11 | 0,0.03,0.795 | 0,0,0 | center | BusVillageRoot | VillageGreen | bevel 0.05/3 | [설정] |
| BusVillageFrontGlass | cube | 0.72×0.04×0.31 | 0,-0.87,0.62 | 0,0,0 | center | BusVillageRoot | DarkGlass | bevel 0.02/2 | [설정] |
| BusVillageSideGlassR | cube | 0.03×1.02×0.29 | 0.435,-0.04,0.63 | 0,0,0 | center | BusVillageRoot | DarkGlass | mirror X | [설정] |
| BusVillageWheelFR | cylinder | 0.29×0.29×0.10 | 0.40,-0.51,0.145 | 0,90,0 | center | BusVillageRoot | Asphalt | mirror X, rear y=0.51 | [설정] |
| BusVillageLampR | cube | 0.12×0.03×0.09 | 0.25,-0.88,0.34 | 0,0,0 | center | BusVillageRoot | OffWhite | mirror X | [설정] |
| KTXRoot | empty | 0.10×0.10×0.10 | 0,0,0 | 0,0,0 | center | – | – | 없음 | [설정] |
| KTXBody | cube | 0.70×2.16×0.52 | 0,0.32,0.40 | 0,0,0 | center | KTXRoot | OffWhite | bevel 0.06/3 | [설정] |
| KTXNose | sphere | 0.74×0.95×0.68 | 0,-0.925,0.41 | 0,0,0 | center | KTXRoot | OffWhite | 앞쪽 Y<0 절반을 쐐기형으로 정리 | [설정] |
| KTXRoof | cube | 0.75×1.65×0.10 | 0,0.42,0.70 | 0,0,0 | center | KTXRoot | OffWhite | bevel 0.04/2 | [설정] |
| KTXCockpit | sphere | 0.56×0.40×0.28 | 0,-1.16,0.53 | 0,0,0 | center | KTXRoot | DarkGlass | 16 seg | [설정] |
| KTXAccentR | cube | 0.03×2.10×0.13 | 0.36,0.12,0.22 | 0,0,0 | center | KTXRoot | SeaDeep | mirror X | [설정] |
| KTXSideGlassR | cube | 0.03×1.10×0.22 | 0.35,0.40,0.50 | 0,0,0 | center | KTXRoot | DarkGlass | mirror X | [설정] |
| KTXBogieF | cube | 0.48×0.34×0.12 | 0,-0.36,0.06 | 0,0,0 | center | KTXRoot | Asphalt | rear y=0.78 | [설정] |
| BeachTrainRoot | empty | 0.10×0.10×0.10 | 0,0,0 | 0,0,0 | center | – | – | 없음 | [설정] |
| BeachTrainBody | cube | 0.86×2.10×0.58 | 0,0,0.50 | 0,0,0 | center | BeachTrainRoot | SeaShallow | bevel 0.06/3 | [설정] |
| BeachTrainRoof | cube | 0.90×1.90×0.12 | 0,0.02,0.79 | 0,0,0 | center | BeachTrainRoot | OffWhite | bevel 0.05/3 | [설정] |
| BeachTrainFrontGlass | cube | 0.72×0.04×0.34 | 0,-1.02,0.62 | 0,0,0 | center | BeachTrainRoot | DarkGlass | bevel 0.02/2 | [설정] |
| BeachTrainSideGlassR | cube | 0.03×1.64×0.34 | 0.435,-0.02,0.62 | 0,0,0 | center | BeachTrainRoot | DarkGlass | mirror X | [설정] |
| BeachTrainTrimR | cube | 0.03×1.94×0.08 | 0.438,0,0.34 | 0,0,0 | center | BeachTrainRoot | OffWhite | mirror X | [설정] |
| BeachTrainWheelFR | cylinder | 0.27×0.27×0.10 | 0.40,-0.62,0.135 | 0,90,0 | center | BeachTrainRoot | Asphalt | mirror X, rear y=0.62 | [설정] |
| BeachTrainLampR | cylinder | 0.13×0.13×0.03 | 0.23,-1.03,0.36 | 90,0,0 | center | BeachTrainRoot | OffWhite | mirror X | [설정] |
| SkyCapsuleRoot | empty | 0.10×0.10×0.10 | 0,0,0 | 0,0,0 | center | – | – | 없음 | [설정] |
| SkyCapsuleSled | cube | 0.70×1.10×0.08 | 0,0,0.04 | 0,0,0 | center | SkyCapsuleRoot | Asphalt | bevel 0.02/2 | [설정] |
| SkyCapsuleBody | cube | 0.90×1.04×0.82 | 0,0,0.59 | 0,0,0 | center | SkyCapsuleRoot | SunsetCoral | bevel 0.10/4 | [설정] |
| SkyCapsuleRoof | cube | 0.78×0.90×0.18 | 0,0.04,1.01 | 0,0,0 | center | SkyCapsuleRoot | SunsetCoral | bevel 0.08/4 | [설정] |
| SkyCapsuleFrontGlass | cube | 0.70×0.04×0.54 | 0,-0.53,0.66 | 0,0,0 | center | SkyCapsuleRoot | SkyGlass | bevel 0.04/3 | [설정] |
| SkyCapsuleSideGlassR | cube | 0.03×0.62×0.54 | 0.445,-0.03,0.66 | 0,0,0 | center | SkyCapsuleRoot | SkyGlass | mirror X | [설정] |
| SkyCapsuleFrame | cube | 0.06×1.06×0.10 | 0,0,0.18 | 0,0,0 | center | SkyCapsuleRoot | DarkGlass | bevel 0.02/2 | [설정] |

## 6. 모델링 순서
| 단계 | 작업 | 쓸 모디파이어·설정값 |
|---|---|---|
| 1 | 여섯 Root와 5번 기본 도형으로 블록아웃 | 치수 오차 ±0.01 m [설정] |
| 2 | 토큰별 실루엣 정리 | Cube 베벨 0.02~0.10 m, 2~4 segments [설정] |
| 3 | 창·바퀴·램프를 큰 덩어리로 정리 | 작은 디테일 추가 금지 [설정] |
| 4 | 베벨·웨이티드 노멀 | Auto Smooth 30°, Weighted Normal 50 [설정] |
| 5 | UV | 텍스처 없음; UV는 선택 사항 [설정] |

## 7. 폴리곤 예산
| 부품 | 삼각형 목표 | 베벨 폭·세그먼트 | 서브디비전 | 비고 |
|---|---:|---|---|---|
| 일반버스 | 450 이하 [설정] | 0.02~0.06 m / 2~3 | 없음 | L0 |
| 급행버스 | 450 이하 [설정] | 0.02~0.06 m / 2~3 | 없음 | L0 |
| 마을버스 | 420 이하 [설정] | 0.02~0.06 m / 2~3 | 없음 | L0 |
| KTX | 500 이하 [설정] | 0.02~0.06 m / 2~3 | 구형 16 seg | L0 |
| 해변열차 | 450 이하 [설정] | 0.02~0.06 m / 2~3 | 없음 | L0 |
| 스카이캡슐 | 500 이하 [설정] | 0.02~0.10 m / 2~4 | 없음 | L0 |
| 합계 | 2,770 이하 [설정] | – | – | 각 토큰 3천 이하 규칙 충족 |

## 8. 재질표
| 재질 이름 | 색 hex (팔레트 이름) | 거칠기 | 금속성 | 노멀 강도 | 야간 발광 색·강도 | 투명도·IOR |
|---|---|---:|---:|---:|---|---|
| M_TransitTokens_BusBlue | #2E6FB7 (일반버스) | 0.62 | 0.0 | 0 | 없음 | Alpha 1 |
| M_TransitTokens_ExpressRed | #C8423B (급행버스) | 0.62 | 0.0 | 0 | 없음 | Alpha 1 |
| M_TransitTokens_VillageGreen | #4E9A5B (마을버스) | 0.62 | 0.0 | 0 | 없음 | Alpha 1 |
| M_TransitTokens_OffWhite | #F2EFE6 (오프화이트) | 0.58 | 0.0 | 0 | 없음 | Alpha 1 |
| M_TransitTokens_SeaDeep | #0E4C77 (바다 딥) | 0.60 | 0.0 | 0 | 없음 | Alpha 1 |
| M_TransitTokens_SeaShallow | #3FA7B5 (바다 얕음) | 0.60 | 0.0 | 0 | 없음 | Alpha 1 |
| M_TransitTokens_SunsetCoral | #F28C5B (노을) | 0.60 | 0.0 | 0 | 없음 | Alpha 1 |
| M_TransitTokens_DarkGlass | #121A33 (밤하늘) | 0.25 | 0.0 | 0 | #121A33 / 0.2 [설정] | Alpha 1 |
| M_TransitTokens_SkyGlass | #A9D6F0 (하늘) | 0.25 | 0.0 | 0 | #A9D6F0 / 0.2 [설정] | Alpha 1 |
| M_TransitTokens_Asphalt | #3A3D42 (아스팔트) | 0.78 | 0.0 | 0 | 없음 | Alpha 1 |

텍스처: 없음 [설정]. 재질색만 사용하고 UV 아틀라스·노멀·ORM 텍스처를 만들지 않는다.

## 9. 글자·그래픽
| 위치 | 내용 | 처리 방법 (텍스처 교체 / 가상 디자인) | 글꼴 성격 |
|---|---|---|---|
| 모든 토큰 | 글자 없음 [설정] | 실제 로고·노선 번호·행선판 금지 | 해당 없음 |

## 10. 움직임
| 부품 | 움직임 | 원점(회전 중심) 좌표 | 축 | 범위 | 속도·식 |
|---|---|---|---|---|---|
| 각 Root | MAP02 루트 경로 추종 | 0,0,0 | XYZ | u=0→1 [설정] | 샷 길이에 맞춰 선형 이동 후 ease in/out 10% [설정] |
| 각 Root | 진행 방향 회전 | 0,0,0 | Z | -180°~180° | yaw = atan2(Δx, -Δy) [설정] |
| 버스 3종·해변열차 바퀴 | 이동에 따른 회전 | 각 바퀴 중심 | X | 누적 | 각도 = 이동거리 ÷ (2πr) × 360° [설정] |
| KTX | 차체 이동 | KTXRoot | XYZ | u=0→1 | 바퀴 회전은 생략 [설정] |
| 스카이캡슐 | 차체 이동 | SkyCapsuleRoot | XYZ | u=0→1 | 흔들림·진자 운동 없음 [설정] |

## 11. 변형
| 종류 | 내용 |
|---|---|
| 낮 / 밤 | 형상은 동일. 밤에는 창 재질 발광 강도만 0.2 [설정] |
| 색상 변형 | 지정된 6종 색만 사용. 실제 도색 변형은 만들지 않음 |
| LOD1 (약 50%) / LOD2 (약 15%) | LOD1은 램프·바퀴 절반 생략, LOD2는 Body+Glass+Undercarriage 최대 3덩어리 [설정] |

## 12. 참고 이미지 프롬프트 (영어)
`reference_prompt.txt`에도 같은 내용을 저장한다.

```
Create a clean 3D modeling reference sheet for a set of six generic transit map tokens, presented as stylized miniature pictograms rather than real vehicles. The six subjects are: (1) standard city bus, deep blue #2E6FB7; (2) express bus, muted red #C8423B; (3) compact village bus, green #4E9A5B; (4) generic high-speed train token, off-white #F2EFE6 with deep sea blue #0E4C77 accent; (5) generic beach train token, shallow-sea teal #3FA7B5 with off-white trim; (6) generic sky capsule token, sunset coral #F28C5B with pale sky glass #A9D6F0. All use dark glass #121A33 and asphalt wheels/undercarriage #3A3D42.

Arrange them in six clearly separated horizontal rows. For every token show three consistent views at the same scale within its row: FRONT orthographic, RIGHT SIDE orthographic, and TOP orthographic. Front faces negative Y. Use simple rounded cubes, cylinders, and low-poly forms, soft 0.04–0.06 m bevel language, flat even studio lighting, faint 0.25 m square grid, light gray background, no perspective distortion, no cast shadows.

Proportions must be deliberately icon-like and normalized: buses approximately 0.9 m wide and 0.85–0.9 m tall, standard/express 2.4 m long, village bus 1.8 m long; high-speed train 0.75 x 2.8 x 0.75 m with a simple tapered rounded nose; beach train 0.9 x 2.1 x 0.85 m with a broad window band; sky capsule 0.9 x 1.1 x 1.1 m with a rounded cabin and tiny rail sled. Emphasize silhouette differences.

No realistic branding, no real route numbers, no readable text, no logos, no scenery, no people, no photographs, no watermarks. This is an original concept reference; dimensions in the written spec take precedence.
```

참고 이미지: `images/reference.png`. 모양·색 참고용이며 치수 기준은 3번과 5번이다.

## 13. 확실하지 않은 값과 필요한 사진
| 값 | 현재 값 | 태그 | 영향도 (상·중·하) | 확정에 필요한 사진 (대상·각도) |
|---|---|---|---|---|
| MAP01 표시 배율 | 0.08 | [설정] | 중 | MAP01 위 여섯 토큰 동시 배치 미리보기 |
| 토큰별 창 비율 | 5번 수치 | [설정] | 하 | Claude 직교 미리보기에서 160 px 이하 축소 가독성 확인 |
| KTX 코 형상 | sphere를 정리한 둥근 쐐기 | [설정] | 중 | Claude 정면·측면 직교 미리보기 |
| 스카이캡슐 하부 썰매 두께 | 0.08 m | [설정] | 하 | Claude 측면 미리보기 |

실제 차량 사진은 필요하지 않다. 이 에셋은 실물 재현이 아닌 지도 픽토그램이며, 실제 사진을 형태 근거로 가져오지 않는다.

## 14. Claude에게 전달 (모델링 요청)
| 항목 | 내용 |
|---|---|
| 모델링 기준 | 5번 부품 목록 + 3번 치수표 + 8번 재질표 |
| 전체 크기 목표 | 일반 0.90×2.40×0.90, 급행 0.90×2.40×0.85, 마을 0.90×1.80×0.85, KTX 0.75×2.80×0.75, 해변열차 0.90×2.10×0.85, 캡슐 0.90×1.10×1.10 m — 1 cm 넘게 다르면 알림 |
| 삼각형 목표 | 여섯 토큰 합계 2,770 이하, 각 토큰 500 이하 [설정] |
| 참고 이미지 | `images/reference.png` (모양·색 참고용, 치수 기준 아님) |
| 꼭 지킬 것 | 각 토큰 독립 Root·바닥 중앙 원점·정면 -Y·실제 로고와 글자 없음·지정 hex 색 |
| Claude가 정해도 되는 것 | 베벨 세그먼트 수, KTX 코 메시 분할, LOD별 병합 방식 |
| 결과물 위치 | Claude가 `blockout.py`, `TransitTokens.blend`, `TransitTokens.glb`, `previews/`, `validation.md`를 이 폴더에 저장 |

## (종류별 추가 섹션)
해당 없음.

---

## Changelog
- v1.0 — 2026-11-11 — 탈것 토큰 6종 설계도와 AI 참고 이미지 최초 작성
