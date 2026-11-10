# ENV11 해동용궁사 설계도

버전: v1.0 — 2026-11-10 — 일괄 제작 초안 최초 작성
상태: 초안
폴더: `busan-3d/assets/ENV11_YonggungsaTemple/`

ID·버전·날짜·섹션 번호·파일명은 식별자. 표의 근거 태그는 해당 행의 모든 수치에 적용한다. 확인된 실제 시설 수치와 제작용 부품 치수를 아래에서 분리한다. 이 납품은 모델러용 설계·비례 블록아웃이며 최종 리토폴로지·텍스처·리그·애니메이션 확정본이 아니다.

## 1. 개요
| 항목 | 내용 |
|---|---|
| 등장 장면 | 2일차 아침 [설정: 레지스트리 장면 계획], 세부 일정 FACTS.md |
| 화면에서의 역할 | stylized coastal Buddhist temple with stair approach and ten-meter generic stone bodhisattva |
| 등급 | H |
| 가장 가까운 카메라 거리 | 25.5m [설정] |
| 화면 점유율 | 최대 80% [설정], 상세 컷 95% [설정] |

- 진입 108계단 [확인], 해수관음대불 높이 10 m [확인], 십이지신 석상 [확인]. 출처: FACTS.md ENV11. 계단 한 단 .17×.30 m [설정: 지시서 기준].

확인·추정 구분을 보존한 원자료 발췌(출처 FACTS.md, 아래 [확인]/[추정]/[설정] 표기는 해당 원문 값에 적용):

### ENV11 해동용궁사
- **[확인]** 바닷가 바위 위의 사찰, 진입로 108계단, 입구 쪽 십이지신 석상, 단일 석재로 만든 높이 10 m 해수관음대불(대웅전 옆 계단 위). 04:30부터 개방, 무료.
- **[추정]** 십이지신 석상 각 약 2 m(자료 1건). 전각 배치·크기는 사진과 위성지도로 산정.


## 2. 핵심 특징
- **지켜야 할 것**
- 바위 위 전각
- 108계단
- 십이지 동물 대용 석상
- 해수관음
- **생략·단순화할 것**
  - 실제 상호·로고·상표·앱 화면은 가상 그래픽으로 대체.
  - 안 보이는 하부·내부는 삭제, 주요 실루엣과 접합부 우선.
  - 미세 반복 패턴은 노멀·트림시트로 처리.
  - 사진 미제공 치수는 실측으로 주장하지 않음.

전각 배치와 석상 세부는 일반화. 관음상 높이와 계단 수는 확인값, 계단 치수는 설정.

## 3. 치수표
| 부위 | 가로 X (m) | 깊이 Y (m) | 높이 Z (m) | 근거 태그 | 근거·계산식 |
|---|---|---|---|---|---|
| 전체 | 30 | 60.15 | 28.36 | [설정] | PARTS 회전·피벗 포함 AABB 사전 계산, minZ=0 [설정] |
| ApproachStep0 (로컬) | 3 | 0.3 | 0.17 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep1 (로컬) | 3 | 0.3 | 0.34 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep2 (로컬) | 3 | 0.3 | 0.51 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep3 (로컬) | 3 | 0.3 | 0.68 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep4 (로컬) | 3 | 0.3 | 0.85 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep5 (로컬) | 3 | 0.3 | 1.02 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep6 (로컬) | 3 | 0.3 | 1.19 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep7 (로컬) | 3 | 0.3 | 1.36 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep8 (로컬) | 3 | 0.3 | 1.53 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep9 (로컬) | 3 | 0.3 | 1.7 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep10 (로컬) | 3 | 0.3 | 1.87 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep11 (로컬) | 3 | 0.3 | 2.04 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep12 (로컬) | 3 | 0.3 | 2.21 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep13 (로컬) | 3 | 0.3 | 2.38 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep14 (로컬) | 3 | 0.3 | 2.55 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep15 (로컬) | 3 | 0.3 | 2.72 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep16 (로컬) | 3 | 0.3 | 2.89 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep17 (로컬) | 3 | 0.3 | 3.06 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep18 (로컬) | 3 | 0.3 | 3.23 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep19 (로컬) | 3 | 0.3 | 3.4 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep20 (로컬) | 3 | 0.3 | 3.57 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep21 (로컬) | 3 | 0.3 | 3.74 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep22 (로컬) | 3 | 0.3 | 3.91 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep23 (로컬) | 3 | 0.3 | 4.08 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep24 (로컬) | 3 | 0.3 | 4.25 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep25 (로컬) | 3 | 0.3 | 4.42 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep26 (로컬) | 3 | 0.3 | 4.59 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep27 (로컬) | 3 | 0.3 | 4.76 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep28 (로컬) | 3 | 0.3 | 4.93 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep29 (로컬) | 3 | 0.3 | 5.1 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep30 (로컬) | 3 | 0.3 | 5.27 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep31 (로컬) | 3 | 0.3 | 5.44 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep32 (로컬) | 3 | 0.3 | 5.61 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep33 (로컬) | 3 | 0.3 | 5.78 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep34 (로컬) | 3 | 0.3 | 5.95 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep35 (로컬) | 3 | 0.3 | 6.12 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep36 (로컬) | 3 | 0.3 | 6.29 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep37 (로컬) | 3 | 0.3 | 6.46 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep38 (로컬) | 3 | 0.3 | 6.63 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep39 (로컬) | 3 | 0.3 | 6.8 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep40 (로컬) | 3 | 0.3 | 6.97 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep41 (로컬) | 3 | 0.3 | 7.14 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep42 (로컬) | 3 | 0.3 | 7.31 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep43 (로컬) | 3 | 0.3 | 7.48 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep44 (로컬) | 3 | 0.3 | 7.65 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep45 (로컬) | 3 | 0.3 | 7.82 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep46 (로컬) | 3 | 0.3 | 7.99 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep47 (로컬) | 3 | 0.3 | 8.16 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep48 (로컬) | 3 | 0.3 | 8.33 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep49 (로컬) | 3 | 0.3 | 8.5 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep50 (로컬) | 3 | 0.3 | 8.67 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep51 (로컬) | 3 | 0.3 | 8.84 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep52 (로컬) | 3 | 0.3 | 9.01 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep53 (로컬) | 3 | 0.3 | 9.18 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep54 (로컬) | 3 | 0.3 | 9.35 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep55 (로컬) | 3 | 0.3 | 9.52 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep56 (로컬) | 3 | 0.3 | 9.69 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep57 (로컬) | 3 | 0.3 | 9.86 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep58 (로컬) | 3 | 0.3 | 10.03 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep59 (로컬) | 3 | 0.3 | 10.2 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep60 (로컬) | 3 | 0.3 | 10.37 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep61 (로컬) | 3 | 0.3 | 10.54 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep62 (로컬) | 3 | 0.3 | 10.71 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep63 (로컬) | 3 | 0.3 | 10.88 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep64 (로컬) | 3 | 0.3 | 11.05 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep65 (로컬) | 3 | 0.3 | 11.22 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep66 (로컬) | 3 | 0.3 | 11.39 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep67 (로컬) | 3 | 0.3 | 11.56 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep68 (로컬) | 3 | 0.3 | 11.73 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep69 (로컬) | 3 | 0.3 | 11.9 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep70 (로컬) | 3 | 0.3 | 12.07 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep71 (로컬) | 3 | 0.3 | 12.24 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep72 (로컬) | 3 | 0.3 | 12.41 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep73 (로컬) | 3 | 0.3 | 12.58 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep74 (로컬) | 3 | 0.3 | 12.75 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep75 (로컬) | 3 | 0.3 | 12.92 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep76 (로컬) | 3 | 0.3 | 13.09 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep77 (로컬) | 3 | 0.3 | 13.26 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep78 (로컬) | 3 | 0.3 | 13.43 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep79 (로컬) | 3 | 0.3 | 13.6 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep80 (로컬) | 3 | 0.3 | 13.77 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep81 (로컬) | 3 | 0.3 | 13.94 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep82 (로컬) | 3 | 0.3 | 14.11 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep83 (로컬) | 3 | 0.3 | 14.28 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep84 (로컬) | 3 | 0.3 | 14.45 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep85 (로컬) | 3 | 0.3 | 14.62 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep86 (로컬) | 3 | 0.3 | 14.79 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep87 (로컬) | 3 | 0.3 | 14.96 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep88 (로컬) | 3 | 0.3 | 15.13 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep89 (로컬) | 3 | 0.3 | 15.3 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep90 (로컬) | 3 | 0.3 | 15.47 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep91 (로컬) | 3 | 0.3 | 15.64 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep92 (로컬) | 3 | 0.3 | 15.81 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep93 (로컬) | 3 | 0.3 | 15.98 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep94 (로컬) | 3 | 0.3 | 16.15 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep95 (로컬) | 3 | 0.3 | 16.32 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep96 (로컬) | 3 | 0.3 | 16.49 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep97 (로컬) | 3 | 0.3 | 16.66 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep98 (로컬) | 3 | 0.3 | 16.83 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep99 (로컬) | 3 | 0.3 | 17 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep100 (로컬) | 3 | 0.3 | 17.17 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep101 (로컬) | 3 | 0.3 | 17.34 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep102 (로컬) | 3 | 0.3 | 17.51 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep103 (로컬) | 3 | 0.3 | 17.68 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep104 (로컬) | 3 | 0.3 | 17.85 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep105 (로컬) | 3 | 0.3 | 18.02 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep106 (로컬) | 3 | 0.3 | 18.19 | [설정] | PARTS; 회전 전 전체 크기 |
| ApproachStep107 (로컬) | 3 | 0.3 | 18.36 | [설정] | PARTS; 회전 전 전체 크기 |
| TemplePlatform (로컬) | 30 | 28 | 0.5 | [설정] | PARTS; 회전 전 전체 크기 |
| HallWall (로컬) | 10 | 7 | 4 | [설정] | PARTS; 회전 전 전체 크기 |
| HallRoof (로컬) | 10.12 | 7.12 | 0.15 | [설정] | PARTS; 회전 전 전체 크기 |
| HallDoor (로컬) | 0.9 | 0.04 | 2.1 | [설정] | PARTS; 회전 전 전체 크기 |
| HallWindow (로컬) | 1 | 0.05 | 0.85 | [설정] | PARTS; 회전 전 전체 크기 |
| HallEaves (로컬) | 13 | 9 | 0.8 | [설정] | PARTS; 회전 전 전체 크기 |
| HallRidge (로컬) | 8 | 1 | 0.7 | [설정] | PARTS; 회전 전 전체 크기 |
| BodhisattvaRobe (로컬) | 3.5 | 3.5 | 8 | [설정] | PARTS; 회전 전 전체 크기 |
| BodhisattvaHead (로컬) | 2 | 2 | 2 | [설정] | PARTS; 회전 전 전체 크기 |
| ZodiacPlinth0 (로컬) | 1 | 1 | 0.3 | [설정] | PARTS; 회전 전 전체 크기 |
| GenericAnimal0 (로컬) | 1 | 1 | 1.6 | [설정] | PARTS; 회전 전 전체 크기 |
| ZodiacPlinth1 (로컬) | 1 | 1 | 0.3 | [설정] | PARTS; 회전 전 전체 크기 |
| GenericAnimal1 (로컬) | 1 | 1 | 1.6 | [설정] | PARTS; 회전 전 전체 크기 |
| ZodiacPlinth2 (로컬) | 1 | 1 | 0.3 | [설정] | PARTS; 회전 전 전체 크기 |
| GenericAnimal2 (로컬) | 1 | 1 | 1.6 | [설정] | PARTS; 회전 전 전체 크기 |
| ZodiacPlinth3 (로컬) | 1 | 1 | 0.3 | [설정] | PARTS; 회전 전 전체 크기 |
| GenericAnimal3 (로컬) | 1 | 1 | 1.6 | [설정] | PARTS; 회전 전 전체 크기 |
| ZodiacPlinth4 (로컬) | 1 | 1 | 0.3 | [설정] | PARTS; 회전 전 전체 크기 |
| GenericAnimal4 (로컬) | 1 | 1 | 1.6 | [설정] | PARTS; 회전 전 전체 크기 |
| ZodiacPlinth5 (로컬) | 1 | 1 | 0.3 | [설정] | PARTS; 회전 전 전체 크기 |
| GenericAnimal5 (로컬) | 1 | 1 | 1.6 | [설정] | PARTS; 회전 전 전체 크기 |
| ZodiacPlinth6 (로컬) | 1 | 1 | 0.3 | [설정] | PARTS; 회전 전 전체 크기 |
| GenericAnimal6 (로컬) | 1 | 1 | 1.6 | [설정] | PARTS; 회전 전 전체 크기 |
| ZodiacPlinth7 (로컬) | 1 | 1 | 0.3 | [설정] | PARTS; 회전 전 전체 크기 |
| GenericAnimal7 (로컬) | 1 | 1 | 1.6 | [설정] | PARTS; 회전 전 전체 크기 |
| ZodiacPlinth8 (로컬) | 1 | 1 | 0.3 | [설정] | PARTS; 회전 전 전체 크기 |
| GenericAnimal8 (로컬) | 1 | 1 | 1.6 | [설정] | PARTS; 회전 전 전체 크기 |
| ZodiacPlinth9 (로컬) | 1 | 1 | 0.3 | [설정] | PARTS; 회전 전 전체 크기 |
| GenericAnimal9 (로컬) | 1 | 1 | 1.6 | [설정] | PARTS; 회전 전 전체 크기 |
| ZodiacPlinth10 (로컬) | 1 | 1 | 0.3 | [설정] | PARTS; 회전 전 전체 크기 |
| GenericAnimal10 (로컬) | 1 | 1 | 1.6 | [설정] | PARTS; 회전 전 전체 크기 |
| ZodiacPlinth11 (로컬) | 1 | 1 | 0.3 | [설정] | PARTS; 회전 전 전체 크기 |
| GenericAnimal11 (로컬) | 1 | 1 | 1.6 | [설정] | PARTS; 회전 전 전체 크기 |

사람 1.70m [설정: 지시서 스케일 기준] 대비 높이 16.68배 [설정]. 복합 전시본은 시설·모듈 전체 경계이며 개별 부품 실측으로 오해하지 않는다. 확인값은 개요 원자료에 별도 표기.

## 4. 정면·측면·윗면 도면
### 4-1. 주요 점 좌표 (에셋 원점 = 바닥 중앙, 단위 m)
| 점 이름 | x | y | z | 설명 |
|---|---|---|---|---|
| 원점 | 0 | 0 | 0 | [설정] Root, AABB 바닥 중앙 |
| 최저 좌전 | -15 | -30.075 | 0 | [설정] 경계 |
| 최고 우후 | 15 | 30.075 | 28.36 | [설정] 경계 |
| 부품·회전축 | PARTS | PARTS | PARTS | [설정] 아래 각 부모 기준 location·pivot을 조합 |

### 4-2. 텍스트 실루엣 (가로세로 비율 유지)
다음은 부품 AABB 투영의 ASCII 요약이다. 문자 셀 가로:세로 약 1:2 [설정]로 보정하되 극단적으로 긴 시설은 높이 표시 최소 줄수 때문에 왜곡될 수 있다. 정확한 비율은 동일 배율 직교 PNG를 기준으로 한다.

```
정면 (-Y에서 본 모습)
                                        #####
                                        #####
                                       #######
                  ###############      #######
              #######################  #######
                 ##################    #######
####################################################
####################################################
                      #######
                      #######
                      #######
                      #######
                      #######
                      #######
                      #######
                      #######
           ##         #######         ##
           ##         #######         ##

측면 (+X에서 본 모습)
                                     ###
                                    ####
                                    ####
                                   ########
                          ##########################
                      ##############################
                   #########
               #############
           #################
       #####################
   #########################
############################

윗면 (+Z에서 본 모습)
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
                      #######
                      #######
           ##         #######         ##
           ##         #######         ##
           ##         #######         ##
           ##         #######         ##
           ##         #######         ##
           ##         #######         ##
           ##         #######         ##
```

### 4-3. 치수선
| 치수선 | 시작점 → 끝점 | 길이 (m) |
|---|---|---|
| X | (-15,0,0) → (15,0,0) | 30 [설정] |
| Y | (0,-30.075,0) → (0,30.075,0) | 60.15 [설정] |
| Z | (0,0,0) → (0,0,28.36) | 28.36 [설정] |

## 5. 부품 목록
PARTS와 행별 일치. 최종 이름은 `ENV11_YonggungsaTemple_{부품}_L0`. 크기는 로컬 전체 치수, sphere는 축별 지름, cylinder/cone는 로컬 지름X·Y와 Z높이. 위치는 부모 기준. pivot 튜플은 도형 중심에서 회전축까지의 오프셋. 원형 부품의 회전은 메시로 베이크한 정적 복제본에서 회전 0°·스케일 1 [설정] 납품. 모든 치수·좌표·회전·분할은 행의 [설정] 적용. Empty 크기는 표시 전용.

| 부품명 | 도형 | 크기 X×Y×Z (m) | 위치 x,y,z (부모 기준) | 회전 x,y,z (°) | 원점(pivot) | 부모 | 재질 | 반복·대칭 | 근거 |
|---|---|---|---|---|---|---|---|---|---|
| Root | empty | (0.1, 0.1, 0.1) | (0, 0, 0) | (0, 0, 0) | center | – | – | 없음 | [설정] |
| ApproachStep0 | cube | (3, 0.3, 0.17) | (0, -29.925, 0.085) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep1 | cube | (3, 0.3, 0.34) | (0, -29.625, 0.17) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep2 | cube | (3, 0.3, 0.51) | (0, -29.325, 0.255) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep3 | cube | (3, 0.3, 0.68) | (0, -29.025, 0.34) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep4 | cube | (3, 0.3, 0.85) | (0, -28.725, 0.425) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep5 | cube | (3, 0.3, 1.02) | (0, -28.425, 0.51) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep6 | cube | (3, 0.3, 1.19) | (0, -28.125, 0.595) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep7 | cube | (3, 0.3, 1.36) | (0, -27.825, 0.68) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep8 | cube | (3, 0.3, 1.53) | (0, -27.525, 0.765) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep9 | cube | (3, 0.3, 1.7) | (0, -27.225, 0.85) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep10 | cube | (3, 0.3, 1.87) | (0, -26.925, 0.935) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep11 | cube | (3, 0.3, 2.04) | (0, -26.625, 1.02) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep12 | cube | (3, 0.3, 2.21) | (0, -26.325, 1.105) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep13 | cube | (3, 0.3, 2.38) | (0, -26.025, 1.19) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep14 | cube | (3, 0.3, 2.55) | (0, -25.725, 1.275) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep15 | cube | (3, 0.3, 2.72) | (0, -25.425, 1.36) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep16 | cube | (3, 0.3, 2.89) | (0, -25.125, 1.445) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep17 | cube | (3, 0.3, 3.06) | (0, -24.825, 1.53) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep18 | cube | (3, 0.3, 3.23) | (0, -24.525, 1.615) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep19 | cube | (3, 0.3, 3.4) | (0, -24.225, 1.7) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep20 | cube | (3, 0.3, 3.57) | (0, -23.925, 1.785) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep21 | cube | (3, 0.3, 3.74) | (0, -23.625, 1.87) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep22 | cube | (3, 0.3, 3.91) | (0, -23.325, 1.955) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep23 | cube | (3, 0.3, 4.08) | (0, -23.025, 2.04) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep24 | cube | (3, 0.3, 4.25) | (0, -22.725, 2.125) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep25 | cube | (3, 0.3, 4.42) | (0, -22.425, 2.21) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep26 | cube | (3, 0.3, 4.59) | (0, -22.125, 2.295) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep27 | cube | (3, 0.3, 4.76) | (0, -21.825, 2.38) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep28 | cube | (3, 0.3, 4.93) | (0, -21.525, 2.465) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep29 | cube | (3, 0.3, 5.1) | (0, -21.225, 2.55) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep30 | cube | (3, 0.3, 5.27) | (0, -20.925, 2.635) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep31 | cube | (3, 0.3, 5.44) | (0, -20.625, 2.72) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep32 | cube | (3, 0.3, 5.61) | (0, -20.325, 2.805) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep33 | cube | (3, 0.3, 5.78) | (0, -20.025, 2.89) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep34 | cube | (3, 0.3, 5.95) | (0, -19.725, 2.975) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep35 | cube | (3, 0.3, 6.12) | (0, -19.425, 3.06) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep36 | cube | (3, 0.3, 6.29) | (0, -19.125, 3.145) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep37 | cube | (3, 0.3, 6.46) | (0, -18.825, 3.23) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep38 | cube | (3, 0.3, 6.63) | (0, -18.525, 3.315) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep39 | cube | (3, 0.3, 6.8) | (0, -18.225, 3.4) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep40 | cube | (3, 0.3, 6.97) | (0, -17.925, 3.485) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep41 | cube | (3, 0.3, 7.14) | (0, -17.625, 3.57) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep42 | cube | (3, 0.3, 7.31) | (0, -17.325, 3.655) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep43 | cube | (3, 0.3, 7.48) | (0, -17.025, 3.74) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep44 | cube | (3, 0.3, 7.65) | (0, -16.725, 3.825) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep45 | cube | (3, 0.3, 7.82) | (0, -16.425, 3.91) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep46 | cube | (3, 0.3, 7.99) | (0, -16.125, 3.995) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep47 | cube | (3, 0.3, 8.16) | (0, -15.825, 4.08) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep48 | cube | (3, 0.3, 8.33) | (0, -15.525, 4.165) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep49 | cube | (3, 0.3, 8.5) | (0, -15.225, 4.25) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep50 | cube | (3, 0.3, 8.67) | (0, -14.925, 4.335) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep51 | cube | (3, 0.3, 8.84) | (0, -14.625, 4.42) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep52 | cube | (3, 0.3, 9.01) | (0, -14.325, 4.505) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep53 | cube | (3, 0.3, 9.18) | (0, -14.025, 4.59) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep54 | cube | (3, 0.3, 9.35) | (0, -13.725, 4.675) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep55 | cube | (3, 0.3, 9.52) | (0, -13.425, 4.76) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep56 | cube | (3, 0.3, 9.69) | (0, -13.125, 4.845) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep57 | cube | (3, 0.3, 9.86) | (0, -12.825, 4.93) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep58 | cube | (3, 0.3, 10.03) | (0, -12.525, 5.015) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep59 | cube | (3, 0.3, 10.2) | (0, -12.225, 5.1) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep60 | cube | (3, 0.3, 10.37) | (0, -11.925, 5.185) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep61 | cube | (3, 0.3, 10.54) | (0, -11.625, 5.27) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep62 | cube | (3, 0.3, 10.71) | (0, -11.325, 5.355) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep63 | cube | (3, 0.3, 10.88) | (0, -11.025, 5.44) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep64 | cube | (3, 0.3, 11.05) | (0, -10.725, 5.525) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep65 | cube | (3, 0.3, 11.22) | (0, -10.425, 5.61) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep66 | cube | (3, 0.3, 11.39) | (0, -10.125, 5.695) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep67 | cube | (3, 0.3, 11.56) | (0, -9.825, 5.78) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep68 | cube | (3, 0.3, 11.73) | (0, -9.525, 5.865) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep69 | cube | (3, 0.3, 11.9) | (0, -9.225, 5.95) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep70 | cube | (3, 0.3, 12.07) | (0, -8.925, 6.035) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep71 | cube | (3, 0.3, 12.24) | (0, -8.625, 6.12) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep72 | cube | (3, 0.3, 12.41) | (0, -8.325, 6.205) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep73 | cube | (3, 0.3, 12.58) | (0, -8.025, 6.29) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep74 | cube | (3, 0.3, 12.75) | (0, -7.725, 6.375) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep75 | cube | (3, 0.3, 12.92) | (0, -7.425, 6.46) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep76 | cube | (3, 0.3, 13.09) | (0, -7.125, 6.545) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep77 | cube | (3, 0.3, 13.26) | (0, -6.825, 6.63) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep78 | cube | (3, 0.3, 13.43) | (0, -6.525, 6.715) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep79 | cube | (3, 0.3, 13.6) | (0, -6.225, 6.8) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep80 | cube | (3, 0.3, 13.77) | (0, -5.925, 6.885) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep81 | cube | (3, 0.3, 13.94) | (0, -5.625, 6.97) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep82 | cube | (3, 0.3, 14.11) | (0, -5.325, 7.055) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep83 | cube | (3, 0.3, 14.28) | (0, -5.025, 7.14) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep84 | cube | (3, 0.3, 14.45) | (0, -4.725, 7.225) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep85 | cube | (3, 0.3, 14.62) | (0, -4.425, 7.31) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep86 | cube | (3, 0.3, 14.79) | (0, -4.125, 7.395) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep87 | cube | (3, 0.3, 14.96) | (0, -3.825, 7.48) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep88 | cube | (3, 0.3, 15.13) | (0, -3.525, 7.565) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep89 | cube | (3, 0.3, 15.3) | (0, -3.225, 7.65) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep90 | cube | (3, 0.3, 15.47) | (0, -2.925, 7.735) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep91 | cube | (3, 0.3, 15.64) | (0, -2.625, 7.82) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep92 | cube | (3, 0.3, 15.81) | (0, -2.325, 7.905) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep93 | cube | (3, 0.3, 15.98) | (0, -2.025, 7.99) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep94 | cube | (3, 0.3, 16.15) | (0, -1.725, 8.075) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep95 | cube | (3, 0.3, 16.32) | (0, -1.425, 8.16) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep96 | cube | (3, 0.3, 16.49) | (0, -1.125, 8.245) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep97 | cube | (3, 0.3, 16.66) | (0, -0.825, 8.33) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep98 | cube | (3, 0.3, 16.83) | (0, -0.525, 8.415) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep99 | cube | (3, 0.3, 17) | (0, -0.225, 8.5) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep100 | cube | (3, 0.3, 17.17) | (0, 0.075, 8.585) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep101 | cube | (3, 0.3, 17.34) | (0, 0.375, 8.67) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep102 | cube | (3, 0.3, 17.51) | (0, 0.675, 8.755) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep103 | cube | (3, 0.3, 17.68) | (0, 0.975, 8.84) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep104 | cube | (3, 0.3, 17.85) | (0, 1.275, 8.925) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep105 | cube | (3, 0.3, 18.02) | (0, 1.575, 9.01) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep106 | cube | (3, 0.3, 18.19) | (0, 1.875, 9.095) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| ApproachStep107 | cube | (3, 0.3, 18.36) | (0, 2.175, 9.18) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| TemplePlatform | cube | (30, 28, 0.5) | (0, 16.075, 18.11) | (0, 0, 0) | center | Root | Rock | bevel 0.2m/2seg | [설정] |
| HallWall | cube | (10, 7, 4) | (0, 16.075, 20.36) | (0, 0, 0) | center | Root | White | bevel 0.06m/2seg | [설정] |
| HallRoof | cube | (10.12, 7.12, 0.15) | (0, 16.075, 22.435) | (0, 0, 0) | center | Root | White | bevel 0.03m/2seg | [설정] |
| HallDoor | cube | (0.9, 0.04, 2.1) | (-2.5, 12.555, 19.41) | (0, 0, 0) | center | Root | Wood | bevel 0.01m/2seg | [설정] |
| HallWindow | cube | (1, 0.05, 0.85) | (2.2, 12.545, 20.01) | (0, 0, 0) | center | Root | Sky | bevel 0.015m/2seg | [설정] |
| HallEaves | cube | (13, 9, 0.8) | (0, 16.075, 22.76) | (0, 0, 0) | center | Root | Night | bevel 0.2m/2seg | [설정] |
| HallRidge | cube | (8, 1, 0.7) | (0, 16.075, 23.5) | (0, 0, 0) | center | Root | BusGreen | bevel 0.1m/2seg | [설정] |
| BodhisattvaRobe | cone | (3.5, 3.5, 8) | (10, 15.075, 22.36) | (0, 0, 0) | center | Root | Concrete | radial 16 | [설정] |
| BodhisattvaHead | sphere | (2, 2, 2) | (10, 15.075, 27.36) | (0, 0, 0) | center | Root | Concrete | radial 16 | [설정] |
| ZodiacPlinth0 | cube | (1, 1, 0.3) | (-8, -26.925, 0.15) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| GenericAnimal0 | sphere | (1, 1, 1.6) | (-8, -26.925, 1.1) | (0, 0, 0) | center | Root | Concrete | radial 12 | [설정] |
| ZodiacPlinth1 | cube | (1, 1, 0.3) | (-8, -22.925, 0.15) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| GenericAnimal1 | sphere | (1, 1, 1.6) | (-8, -22.925, 1.1) | (0, 0, 0) | center | Root | Concrete | radial 12 | [설정] |
| ZodiacPlinth2 | cube | (1, 1, 0.3) | (-8, -18.925, 0.15) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| GenericAnimal2 | sphere | (1, 1, 1.6) | (-8, -18.925, 1.1) | (0, 0, 0) | center | Root | Concrete | radial 12 | [설정] |
| ZodiacPlinth3 | cube | (1, 1, 0.3) | (-8, -14.925, 0.15) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| GenericAnimal3 | sphere | (1, 1, 1.6) | (-8, -14.925, 1.1) | (0, 0, 0) | center | Root | Concrete | radial 12 | [설정] |
| ZodiacPlinth4 | cube | (1, 1, 0.3) | (-8, -10.925, 0.15) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| GenericAnimal4 | sphere | (1, 1, 1.6) | (-8, -10.925, 1.1) | (0, 0, 0) | center | Root | Concrete | radial 12 | [설정] |
| ZodiacPlinth5 | cube | (1, 1, 0.3) | (-8, -6.925, 0.15) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| GenericAnimal5 | sphere | (1, 1, 1.6) | (-8, -6.925, 1.1) | (0, 0, 0) | center | Root | Concrete | radial 12 | [설정] |
| ZodiacPlinth6 | cube | (1, 1, 0.3) | (8, -26.925, 0.15) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| GenericAnimal6 | sphere | (1, 1, 1.6) | (8, -26.925, 1.1) | (0, 0, 0) | center | Root | Concrete | radial 12 | [설정] |
| ZodiacPlinth7 | cube | (1, 1, 0.3) | (8, -22.925, 0.15) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| GenericAnimal7 | sphere | (1, 1, 1.6) | (8, -22.925, 1.1) | (0, 0, 0) | center | Root | Concrete | radial 12 | [설정] |
| ZodiacPlinth8 | cube | (1, 1, 0.3) | (8, -18.925, 0.15) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| GenericAnimal8 | sphere | (1, 1, 1.6) | (8, -18.925, 1.1) | (0, 0, 0) | center | Root | Concrete | radial 12 | [설정] |
| ZodiacPlinth9 | cube | (1, 1, 0.3) | (8, -14.925, 0.15) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| GenericAnimal9 | sphere | (1, 1, 1.6) | (8, -14.925, 1.1) | (0, 0, 0) | center | Root | Concrete | radial 12 | [설정] |
| ZodiacPlinth10 | cube | (1, 1, 0.3) | (8, -10.925, 0.15) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| GenericAnimal10 | sphere | (1, 1, 1.6) | (8, -10.925, 1.1) | (0, 0, 0) | center | Root | Concrete | radial 12 | [설정] |
| ZodiacPlinth11 | cube | (1, 1, 0.3) | (8, -6.925, 0.15) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| GenericAnimal11 | sphere | (1, 1, 1.6) | (8, -6.925, 1.1) | (0, 0, 0) | center | Root | Concrete | radial 12 | [설정] |

## 6. 모델링 순서
| 단계 | 작업 | 쓸 모디파이어·설정값 |
|---|---|---|
| 1 | blockout.py 실행 후 치수·원점·접합 확인 | 허용 오차 .01m [설정] |
| 2 | 주요 실루엣을 부품별 리토폴로지, 중복·겹친 비가시 면 삭제 | X 대칭 가능 부품만 Mirror; 석상·음식은 불규칙성 유지 |
| 3 | 창·문 개구부·접합·하부·세부 형상 제작, 회전축 원점 유지 | 프레임과 문 스윙·손 그립·보행폭은 실제 사진과 최종 씬에서 검사 |
| 4 | 베벨·웨이티드 노멀, 메시 크기에 맞게 폭 조정 | PARTS 베벨 우선, 최소 치수 2% 이하 [설정], segments 2 [설정] |
| 5 | 반복 표면 트림·타일 UV, 가상 그래픽은 별도 데칼 | H/M/B 각각 1024/512/256px/m [설정: 지시서], 아틀라스 2048²px [설정], padding 16px [설정] |

복합 전시본은 구성 확인용. 각 모듈·음식·소품은 부품 그룹을 묶어 바닥 중앙으로 다시 추출하되 회전 부품의 축은 유지. 의도된 겹침은 최종 토폴로지 단계에서 연결하고 물리·인물 접촉면은 별도로 검사한다.

## 7. 폴리곤 예산
| 부품 | 삼각형 목표 | 베벨 폭·세그먼트 | 서브디비전 | 비고 |
|---|---|---|---|---|
| ApproachStep0 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep1 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep2 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep3 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep4 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep5 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep6 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep7 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep8 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep9 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep10 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep11 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep12 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep13 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep14 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep15 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep16 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep17 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep18 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep19 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep20 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep21 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep22 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep23 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep24 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep25 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep26 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep27 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep28 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep29 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep30 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep31 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep32 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep33 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep34 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep35 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep36 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep37 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep38 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep39 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep40 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep41 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep42 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep43 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep44 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep45 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep46 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep47 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep48 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep49 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep50 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep51 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep52 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep53 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep54 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep55 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep56 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep57 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep58 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep59 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep60 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep61 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep62 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep63 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep64 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep65 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep66 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep67 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep68 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep69 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep70 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep71 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep72 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep73 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep74 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep75 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep76 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep77 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep78 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep79 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep80 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep81 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep82 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep83 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep84 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep85 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep86 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep87 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep88 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep89 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep90 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep91 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep92 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep93 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep94 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep95 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep96 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep97 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep98 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep99 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep100 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep101 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep102 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep103 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep104 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep105 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep106 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ApproachStep107 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| TemplePlatform | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| HallWall | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| HallRoof | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| HallDoor | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| HallWindow | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| HallEaves | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| HallRidge | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| BodhisattvaRobe | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| BodhisattvaHead | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ZodiacPlinth0 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| GenericAnimal0 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ZodiacPlinth1 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| GenericAnimal1 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ZodiacPlinth2 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| GenericAnimal2 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ZodiacPlinth3 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| GenericAnimal3 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ZodiacPlinth4 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| GenericAnimal4 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ZodiacPlinth5 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| GenericAnimal5 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ZodiacPlinth6 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| GenericAnimal6 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ZodiacPlinth7 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| GenericAnimal7 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ZodiacPlinth8 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| GenericAnimal8 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ZodiacPlinth9 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| GenericAnimal9 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ZodiacPlinth10 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| GenericAnimal10 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ZodiacPlinth11 | 283 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| GenericAnimal11 | 380 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| 합계 | 40,000 [설정] | 위 합계 | 없음 | 등급 H, 완성 목표 예산 |

블록아웃은 예산 하한까지 의미 없이 세분하지 않는다. 키트는 K2/K5의 모듈 예산과 시설 전체 전시본을 구분. 군중 한 캐릭터는 300tris 이하 [설정: 지시서]. 최종 평가 메시·glTF 삼각형은 validation.md.

## 8. 재질표
| 재질 이름 | 색 hex (팔레트 이름) | 거칠기 | 금속성 | 노멀 강도 | 야간 발광 색·강도 | 투명도·IOR |
|---|---|---|---|---|---|---|
| M_YonggungsaTemple_Concrete | #B9B6AE (전역 팔레트) | 0.65 | 0 | 0 | 없음 / 0 | Alpha 1, IOR 1.5 [설정: 행 전체] |
| M_YonggungsaTemple_Rock | #6E6A64 (전역 팔레트) | 0.65 | 0 | 0 | 없음 / 0 | Alpha 1, IOR 1.5 [설정: 행 전체] |
| M_YonggungsaTemple_White | #F2EFE6 (전역 팔레트) | 0.65 | 0 | 0 | 없음 / 0 | Alpha 1, IOR 1.5 [설정: 행 전체] |
| M_YonggungsaTemple_Wood | #9A7350 (전역 팔레트) | 0.65 | 0 | 0 | 없음 / 0 | Alpha 1, IOR 1.5 [설정: 행 전체] |
| M_YonggungsaTemple_Sky | #A9D6F0 (전역 팔레트) | 0.65 | 0 | 0 | 없음 / 0 | Alpha 1, IOR 1.5 [설정: 행 전체] |
| M_YonggungsaTemple_Night | #121A33 (전역 팔레트) | 0.65 | 0 | 0 | 없음 / 0 | Alpha 1, IOR 1.5 [설정: 행 전체] |
| M_YonggungsaTemple_BusGreen | #4E9A5B (전역 팔레트) | 0.65 | 0 | 0 | 없음 / 0 | Alpha 1, IOR 1.5 [설정: 행 전체] |

색은 INSTRUCTIONS.md 전역 팔레트, 수치는 측색값이 아닌 [설정]. 텍스처 `T_YonggungsaTemple_BaseColor`, `T_YonggungsaTemple_Normal`, `T_YonggungsaTemple_ORM`, `T_YonggungsaTemple_Emission`. ORM R=AO/G=Roughness/B=Metallic [설정]. 현재 블록아웃은 단순 PBR 색, 고유 텍스처 미포함. 반복 재질은 트림·타일, 가상 표시는 별도 UV 아틀라스. 텍셀 밀도는 등급별 위 값, 긴 시설은 고유 한 장으로 펴지 않는다.

## 9. 글자·그래픽
| 위치 | 내용 | 처리 방법 (텍스처 교체 / 가상 디자인) | 글꼴 성격 |
|---|---|---|---|
| 표지·포장·간판·화면(해당 시) | BLUE COAST 가상 브랜드, 정류장·버스 번호는 FACTS 목록 | 실제 로고·상표·앱·캐릭터 조형물 복제 금지, 데칼 교체 | 단순 산세리프·픽토그램 |
| 숫자·정보(해당 시) | 확인된 노선·정류장·시간만 사용 | 모르는 주소·번호·가격 생성 금지 | 읽기 쉬운 고딕 |

## 10. 움직임
| 부품 | 움직임 | 원점(회전 중심) 좌표 | 축 | 범위 | 속도·식 |
|---|---|---|---|---|---|
| Root | 정적 배치 | (0,0,0) [설정] | – | 변형 없음 | 씬 이동은 Root 전체 이동 |

숫자는 별도 [확인] 표기가 없는 한 [설정]. 이 표는 리그·애니메이션 제작 사양이며 자동 생성된 키프레임 납품을 뜻하지 않는다. 정적 복제본 .blend/.glb에는 정지 상태만 저장. 부모 위치가 정규화되었으므로 회전축은 PARTS의 현재 location을 기준으로 사용한다.

## 11. 변형
| 종류 | 내용 |
|---|---|
| 낮 / 밤 | 낮 기본 팔레트, 밤 Warm·Cool 발광과 FX02 조명. 재질이 없는 발광을 사실처럼 추가하지 않음 |
| 색상 변형 | 전역 팔레트 내 색만, 실제 브랜드 배색·패턴 미복제 |
| LOD1 (약 50%) / LOD2 (약 15%) | 20,000 / 6,000tris [설정], 반복·하부·실내 세부 축약; 실루엣 유지 |

## 12. 참고 이미지 프롬프트 (영어)
`reference_prompt.txt`와 동일. 프롬프트 치수는 제작용 [설정].

```
Create an orthographic model reference sheet for a 3D modeler.
Subject: stylized coastal Buddhist temple with stair approach and ten-meter generic stone bodhisattva.
Model-design bounds, not surveyed measurements: X 30 m, Y 60.15 m, Z 28.36 m. Z up, front negative Y; floor-center origin. All unspecified details are fictional artistic settings. Preserve confirmed facts listed in spec.md.
Layout: 4 views in a 2x2 grid — FRONT, RIGHT SIDE, BACK, TOP — all at exactly the same scale, aligned to a faint 1-meter grid, true orthographic projection, no perspective.
Style: stylized miniature diorama, soft bevels, simplified forms, clean dark outlines, flat even lighting, no cast shadows, light gray background.
Include: a 1.7 m human silhouette beside each view for scale; palette swatches: #121A33, #4E9A5B, #6E6A64, #9A7350, #A9D6F0, #B9B6AE, #F2EFE6.
Exclude: brand logos, readable commercial signage, copied application screens, watermarks, scenery backgrounds. Use generic brands and original sculpture designs. Written dimensions and executable blockout take precedence over any illustration.
```

images/front.png, right.png, back.png, top.png는 실제 블록아웃의 동일 배율 직교 렌더. 작은 소품은 detail.png에 별도 확대, 실측 근거로 사용하지 않음. 성인 1.70m [설정] 비교용 실루엣은 프리뷰 전용이며 저장 에셋에서 제외. 렌더 투영의 겹침이나 의도된 임시 형상은 최종 메시 품질을 보장하지 않는다.

## 13. 확실하지 않은 값과 필요한 사진
| 값 | 현재 값 | 태그 | 영향도 (상·중·하) | 확정에 필요한 사진 (대상·각도) |
|---|---|---|---|---|
| 실측 외곽·세부 비례 | (30, 60.15, 28.36) m [설정] | [설정] 또는 위 원자료의 [추정] | 상 | 전체 정면·정측면·배면·높은 사선, 성인 또는 규격 기준물과 함께 |
| 재질·그래픽·접합 | 전역 팔레트·가상 디자인 [설정] | [설정] 또는 위 원자료의 [추정] | 중 | 재료 근접·연결부·사용 장면 사진; 실제 로고는 재현하지 않음 |

사진 제공 전에는 위 제작 설정으로 진행하되 [확인]으로 격상하지 않는다. 사진·좌표·실측 제공 시 버전을 올려 보정한다. 사용자 요청에 따라 전체 항목을 일괄 초안 작성하므로 개별 사진 요청으로 작업을 중단하지 않는다.

## 14. 블록아웃 스크립트
- 파일: `blockout.py`, templates/blockout_template.py에서 에셋 정보·재질·부품만 채우고 공용 함수는 동일하게 유지. VERSION과 SPEC_VERSION=v1.0 동기화.
- 외부 검사: `python blockout.py --self-test`.
- Blender 실행: `blender --background --factory-startup --python blockout.py`.
- REPORT 목표 dims_m=30.000x60.150x28.360, 허용 .01m [설정], triangles≤40000 [설정], 바닥 min_z=0 [설정].
- `YonggungsaTemple_blockout.blend`와 `YonggungsaTemple_blockout.glb`는 초안 정적 형상. 최종 외피·디테일·UV·리그·키프레임·LOD 변형은 명시된 후속 모델링 작업. 변환 Apply, 미터 단위. GLB는 표준 Y-up 저장 후 Blender 재가져오기에서 Z-up 치수 확인.
- 실행·중복·외곽·예산·이름·변환·GLB 검사 결과는 validation.md. 참고 렌더는 실제 GLB 재가져오기 메시로 생성.

## (종류별 추가 섹션)
해당 분류는 키트·캐릭터·음식이 아니므로 추가 섹션 없음.

---

## Changelog
- v1.0 — 2026-11-10 — 설계도·블록아웃·참고 프롬프트·직교 참고 이미지·정적 blend/GLB·검증 기록 최초 작성, 실측 미확정 항목 분리.
