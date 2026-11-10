# ENV14 해안 철로 키트 + 다릿돌전망대 설계도

버전: v1.0 — 2026-11-10 — 일괄 제작 초안 최초 작성
상태: 초안
폴더: `busan-3d/assets/ENV14_CoastalRailDaritdol/`

ID·버전·날짜·섹션 번호·파일명은 식별자. 표의 근거 태그는 해당 행의 모든 수치에 적용한다. 확인된 실제 시설 수치와 제작용 부품 치수를 아래에서 분리한다. 이 납품은 모델러용 설계·비례 블록아웃이며 최종 리토폴로지·텍스처·리그·애니메이션 확정본이 아니다.

## 1. 개요
| 항목 | 내용 |
|---|---|
| 등장 장면 | 2일차 [설정: 레지스트리 장면 계획], 세부 일정 FACTS.md |
| 화면에서의 역할 | coastal rail kit and U-shaped Daritdol observation walkway |
| 등급 | H |
| 가장 가까운 카메라 거리 | 19m [설정] |
| 화면 점유율 | 최대 80% [설정], 상세 컷 95% [설정] |

- 다릿돌전망대 길이 191 m [확인], 폭 3 m [확인], 해수면 위 약 20 m [확인], U자 확장 [확인]. 출처: FACTS.md ENV14. 해월전망대 137 m [확인]와 구분.

확인·추정 구분을 보존한 원자료 발췌(출처 FACTS.md, 아래 [확인]/[추정]/[설정] 표기는 해당 원문 값에 적용):

### ENV14 다릿돌전망대 / ENV15 청사포
- **[확인]** 해수면 위 약 20 m. 2024년 확장 후 U자형, 길이 191 m(일부 기사는 192 m), 폭 3 m, 끝에 반달 모양 투명 유리 바닥.
- **[확인]** 앞바다 암초 다섯 개가 등대까지 이어진다(이름의 유래).
- **[확인]** 근처 해월전망대(길이 137 m)는 다른 시설이다.
- **[추정]** 청사포 방파제 끝 쌍둥이 등대 → 색·높이는 사진으로 확인.


## 2. 핵심 특징
- **지켜야 할 것**
- 해안 철로
- U자 전망 보행로
- 반달 투명 끝단
- **생략·단순화할 것**
  - 실제 상호·로고·상표·앱 화면은 가상 그래픽으로 대체.
  - 안 보이는 하부·내부는 삭제, 주요 실루엣과 접합부 우선.
  - 미세 반복 패턴은 노멀·트림시트로 처리.
  - 사진 미제공 치수는 실측으로 주장하지 않음.

191 m는 곡선 중심선 설계 길이로 유지. 실제 U자 비례·교각 배치는 사진 미확인 설정. 해수면 Z=0. 끝단의 Glass 접두사 패널은 반달 유리 바닥으로 후속 연결·리토폴로지. 실제 총길이 정의가 확인되기 전에는 중심선 해석을 설정으로 명시. 191 m [확인]를 임의 축소하지 않음. 일반 접근 바닥은 Concrete, U자 끝단 반달 구간은 WalkGlass20~27의 Sky 유리 [설정]로 분리. 실제 유리 경계·반달 패널 윤곽은 사진으로 보정. 유리 알파 .30·IOR1.45 [설정].

## 3. 치수표
| 부위 | 가로 X (m) | 깊이 Y (m) | 높이 Z (m) | 근거 태그 | 근거·계산식 |
|---|---|---|---|---|---|
| 전체 | 28.4975 | 92.4166 | 21.13 | [설정] | PARTS 회전·피벗 포함 AABB 사전 계산, minZ=0 [설정] |
| WalkGlass0 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail0S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail0S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass1 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail1S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail1S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass2 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail2S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail2S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass3 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail3S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail3S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass4 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail4S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail4S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass5 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail5S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail5S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass6 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail6S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail6S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass7 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail7S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail7S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass8 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail8S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail8S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass9 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail9S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail9S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass10 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail10S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail10S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass11 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail11S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail11S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass12 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail12S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail12S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass13 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail13S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail13S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass14 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail14S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail14S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass15 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail15S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail15S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass16 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail16S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail16S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass17 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail17S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail17S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass18 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail18S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail18S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass19 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail19S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail19S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass20 (로컬) | 3 | 3.9786 | 0.05549 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail20S0 (로컬) | 0.06 | 3.9786 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail20S2 (로컬) | 0.06 | 3.9786 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass21 (로컬) | 3 | 3.93827 | 0.05549 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail21S0 (로컬) | 0.06 | 3.93827 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail21S2 (로컬) | 0.06 | 3.93827 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass22 (로컬) | 3 | 3.93827 | 0.05549 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail22S0 (로컬) | 0.06 | 3.93827 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail22S2 (로컬) | 0.06 | 3.93827 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass23 (로컬) | 3 | 3.93827 | 0.05549 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail23S0 (로컬) | 0.06 | 3.93827 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail23S2 (로컬) | 0.06 | 3.93827 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass24 (로컬) | 3 | 3.93827 | 0.05549 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail24S0 (로컬) | 0.06 | 3.93827 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail24S2 (로컬) | 0.06 | 3.93827 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass25 (로컬) | 3 | 3.93827 | 0.05549 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail25S0 (로컬) | 0.06 | 3.93827 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail25S2 (로컬) | 0.06 | 3.93827 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass26 (로컬) | 3 | 3.93827 | 0.05549 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail26S0 (로컬) | 0.06 | 3.93827 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail26S2 (로컬) | 0.06 | 3.93827 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass27 (로컬) | 3 | 3.9786 | 0.05549 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail27S0 (로컬) | 0.06 | 3.9786 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail27S2 (로컬) | 0.06 | 3.9786 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass28 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail28S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail28S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass29 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail29S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail29S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass30 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail30S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail30S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass31 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail31S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail31S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass32 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail32S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail32S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass33 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail33S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail33S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass34 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail34S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail34S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass35 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail35S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail35S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass36 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail36S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail36S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass37 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail37S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail37S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass38 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail38S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail38S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass39 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail39S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail39S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass40 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail40S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail40S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass41 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail41S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail41S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass42 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail42S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail42S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass43 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail43S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail43S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass44 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail44S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail44S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass45 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail45S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail45S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass46 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail46S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail46S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkGlass47 (로컬) | 3 | 3.97917 | 0.18 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail47S0 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkRail47S2 (로컬) | 0.06 | 3.97917 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkPier0 (로컬) | 0.5 | 0.5 | 19.7 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkPier1 (로컬) | 0.5 | 0.5 | 19.7 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkPier2 (로컬) | 0.5 | 0.5 | 19.7 | [설정] | PARTS; 회전 전 전체 크기 |
| WalkPier3 (로컬) | 0.5 | 0.5 | 19.7 | [설정] | PARTS; 회전 전 전체 크기 |
| CoastalTrackRail0 (로컬) | 0.07 | 12 | 0.12 | [설정] | PARTS; 회전 전 전체 크기 |
| CoastalTrackRail2 (로컬) | 0.07 | 12 | 0.12 | [설정] | PARTS; 회전 전 전체 크기 |
| CoastalTrackSleeper0 (로컬) | 1.935 | 0.2 | 0.1 | [설정] | PARTS; 회전 전 전체 크기 |
| CoastalTrackSleeper1 (로컬) | 1.935 | 0.2 | 0.1 | [설정] | PARTS; 회전 전 전체 크기 |
| CoastalTrackSleeper2 (로컬) | 1.935 | 0.2 | 0.1 | [설정] | PARTS; 회전 전 전체 크기 |
| CoastalTrackSleeper3 (로컬) | 1.935 | 0.2 | 0.1 | [설정] | PARTS; 회전 전 전체 크기 |
| CoastalTrackSleeper4 (로컬) | 1.935 | 0.2 | 0.1 | [설정] | PARTS; 회전 전 전체 크기 |
| CoastalTrackSleeper5 (로컬) | 1.935 | 0.2 | 0.1 | [설정] | PARTS; 회전 전 전체 크기 |
| CoastalTrackSleeper6 (로컬) | 1.935 | 0.2 | 0.1 | [설정] | PARTS; 회전 전 전체 크기 |
| CoastalTrackSleeper7 (로컬) | 1.935 | 0.2 | 0.1 | [설정] | PARTS; 회전 전 전체 크기 |
| CoastalTrackSleeper8 (로컬) | 1.935 | 0.2 | 0.1 | [설정] | PARTS; 회전 전 전체 크기 |
| CoastalTrackSleeper9 (로컬) | 1.935 | 0.2 | 0.1 | [설정] | PARTS; 회전 전 전체 크기 |
| CoastalTrackSleeper10 (로컬) | 1.935 | 0.2 | 0.1 | [설정] | PARTS; 회전 전 전체 크기 |
| CoastalTrackSleeper11 (로컬) | 1.935 | 0.2 | 0.1 | [설정] | PARTS; 회전 전 전체 크기 |
| CoastalTrackSleeper12 (로컬) | 1.935 | 0.2 | 0.1 | [설정] | PARTS; 회전 전 전체 크기 |
| CoastalTrackSleeper13 (로컬) | 1.935 | 0.2 | 0.1 | [설정] | PARTS; 회전 전 전체 크기 |
| CoastalTrackSleeper14 (로컬) | 1.935 | 0.2 | 0.1 | [설정] | PARTS; 회전 전 전체 크기 |
| CoastalTrackSleeper15 (로컬) | 1.935 | 0.2 | 0.1 | [설정] | PARTS; 회전 전 전체 크기 |
| CoastalTrackSleeper16 (로컬) | 1.935 | 0.2 | 0.1 | [설정] | PARTS; 회전 전 전체 크기 |
| CoastalTrackSleeper17 (로컬) | 1.935 | 0.2 | 0.1 | [설정] | PARTS; 회전 전 전체 크기 |
| CoastalTrackSleeper18 (로컬) | 1.935 | 0.2 | 0.1 | [설정] | PARTS; 회전 전 전체 크기 |
| CoastalTrackSleeper19 (로컬) | 1.935 | 0.2 | 0.1 | [설정] | PARTS; 회전 전 전체 크기 |

사람 1.70m [설정: 지시서 스케일 기준] 대비 높이 12.43배 [설정]. 복합 전시본은 시설·모듈 전체 경계이며 개별 부품 실측으로 오해하지 않는다. 확인값은 개요 원자료에 별도 표기.

## 4. 정면·측면·윗면 도면
### 4-1. 주요 점 좌표 (에셋 원점 = 바닥 중앙, 단위 m)
| 점 이름 | x | y | z | 설명 |
|---|---|---|---|---|
| 원점 | 0 | 0 | 0 | [설정] Root, AABB 바닥 중앙 |
| 최저 좌전 | -14.2487 | -46.2083 | 0 | [설정] 경계 |
| 최고 우후 | 14.2487 | 46.2083 | 21.13 | [설정] 경계 |
| 부품·회전축 | PARTS | PARTS | PARTS | [설정] 아래 각 부모 기준 location·pivot을 조합 |

### 4-2. 텍스트 실루엣 (가로세로 비율 유지)
다음은 부품 AABB 투영의 ASCII 요약이다. 문자 셀 가로:세로 약 1:2 [설정]로 보정하되 극단적으로 긴 시설은 높이 표시 최소 줄수 때문에 왜곡될 수 있다. 정확한 비율은 동일 배율 직교 PNG를 기준으로 한다.

```
정면 (-Y에서 본 모습)
                ####################################
                ####################################
                #######                      ######
                   ##                          ##
                   ##                          ##
                   ##                          ##
                   ##                          ##
                   ##                          ##
                   ##                          ##
                   ##                          ##
                   ##                          ##
                   ##                          ##
                   ##                          ##
                   ##                          ##
                   ##                          ##
                   ##                          ##
                   ##                          ##
####               ##                          ##

측면 (+X에서 본 모습)
####################################################
####################################################
     #                          ##
     #                          ##
     #                          ##
     # ########                 ##

윗면 (+Z에서 본 모습)
                          ################
                 ##################################
                #############         #############
                #######                      #######
                #######                      #######
                #######                      #######
                #######                      #######
                #######                      #######
                #######                      #######
                #######                      #######
                #######                      #######
                #######                      #######
                #######                      #######
####            #######                      #######
####            #######                      #######
####            #######                      #######
                #######                      #######
                #######                      #######
```

### 4-3. 치수선
| 치수선 | 시작점 → 끝점 | 길이 (m) |
|---|---|---|
| X | (-14.2487,0,0) → (14.2487,0,0) | 28.4975 [설정] |
| Y | (0,-46.2083,0) → (0,46.2083,0) | 92.4166 [설정] |
| Z | (0,0,0) → (0,0,21.13) | 21.13 [설정] |

## 5. 부품 목록
PARTS와 행별 일치. 최종 이름은 `ENV14_CoastalRailDaritdol_{부품}_L0`. 크기는 로컬 전체 치수, sphere는 축별 지름, cylinder/cone는 로컬 지름X·Y와 Z높이. 위치는 부모 기준. pivot 튜플은 도형 중심에서 회전축까지의 오프셋. 원형 부품의 회전은 메시로 베이크한 정적 복제본에서 회전 0°·스케일 1 [설정] 납품. 모든 치수·좌표·회전·분할은 행의 [설정] 적용. Empty 크기는 표시 전용.

| 부품명 | 도형 | 크기 X×Y×Z (m) | 위치 x,y,z (부모 기준) | 회전 x,y,z (°) | 원점(pivot) | 부모 | 재질 | 반복·대칭 | 근거 |
|---|---|---|---|---|---|---|---|---|---|
| Root | empty | (0.1, 0.1, 0.1) | (0, 0, 0) | (0, 0, 0) | center | – | – | 없음 | [설정] |
| WalkGlass0 | cube | (3, 3.97917, 0.18) | (-3.28125, -44.2187, 19.91) | (0, 0, -0) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail0S0 | cube | (0.06, 3.97917, 0.06) | (-4.78125, -44.2187, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkRail0S2 | cube | (0.06, 3.97917, 0.06) | (-1.78125, -44.2187, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass1 | cube | (3, 3.97917, 0.18) | (-3.28125, -40.2395, 19.91) | (0, 0, -0) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail1S0 | cube | (0.06, 3.97917, 0.06) | (-4.78125, -40.2395, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkRail1S2 | cube | (0.06, 3.97917, 0.06) | (-1.78125, -40.2395, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass2 | cube | (3, 3.97917, 0.18) | (-3.28125, -36.2604, 19.91) | (0, 0, -0) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail2S0 | cube | (0.06, 3.97917, 0.06) | (-4.78125, -36.2604, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkRail2S2 | cube | (0.06, 3.97917, 0.06) | (-1.78125, -36.2604, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass3 | cube | (3, 3.97917, 0.18) | (-3.28125, -32.2812, 19.91) | (0, 0, -0) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail3S0 | cube | (0.06, 3.97917, 0.06) | (-4.78125, -32.2812, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkRail3S2 | cube | (0.06, 3.97917, 0.06) | (-1.78125, -32.2812, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass4 | cube | (3, 3.97917, 0.18) | (-3.28125, -28.302, 19.91) | (0, 0, -0) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail4S0 | cube | (0.06, 3.97917, 0.06) | (-4.78125, -28.302, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkRail4S2 | cube | (0.06, 3.97917, 0.06) | (-1.78125, -28.302, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass5 | cube | (3, 3.97917, 0.18) | (-3.28125, -24.3229, 19.91) | (0, 0, -0) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail5S0 | cube | (0.06, 3.97917, 0.06) | (-4.78125, -24.3229, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkRail5S2 | cube | (0.06, 3.97917, 0.06) | (-1.78125, -24.3229, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass6 | cube | (3, 3.97917, 0.18) | (-3.28125, -20.3437, 19.91) | (0, 0, -0) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail6S0 | cube | (0.06, 3.97917, 0.06) | (-4.78125, -20.3437, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkRail6S2 | cube | (0.06, 3.97917, 0.06) | (-1.78125, -20.3437, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass7 | cube | (3, 3.97917, 0.18) | (-3.28125, -16.3645, 19.91) | (0, 0, -0) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail7S0 | cube | (0.06, 3.97917, 0.06) | (-4.78125, -16.3645, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkRail7S2 | cube | (0.06, 3.97917, 0.06) | (-1.78125, -16.3645, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass8 | cube | (3, 3.97917, 0.18) | (-3.28125, -12.3854, 19.91) | (0, 0, -0) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail8S0 | cube | (0.06, 3.97917, 0.06) | (-4.78125, -12.3854, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkRail8S2 | cube | (0.06, 3.97917, 0.06) | (-1.78125, -12.3854, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass9 | cube | (3, 3.97917, 0.18) | (-3.28125, -8.4062, 19.91) | (0, 0, -0) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail9S0 | cube | (0.06, 3.97917, 0.06) | (-4.78125, -8.4062, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkRail9S2 | cube | (0.06, 3.97917, 0.06) | (-1.78125, -8.4062, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass10 | cube | (3, 3.97917, 0.18) | (-3.28125, -4.42703, 19.91) | (0, 0, -0) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail10S0 | cube | (0.06, 3.97917, 0.06) | (-4.78125, -4.42703, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkRail10S2 | cube | (0.06, 3.97917, 0.06) | (-1.78125, -4.42703, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass11 | cube | (3, 3.97917, 0.18) | (-3.28125, -0.447862, 19.91) | (0, 0, -0) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail11S0 | cube | (0.06, 3.97917, 0.06) | (-4.78125, -0.447862, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkRail11S2 | cube | (0.06, 3.97917, 0.06) | (-1.78125, -0.447862, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass12 | cube | (3, 3.97917, 0.18) | (-3.28125, 3.5313, 19.91) | (0, 0, -0) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail12S0 | cube | (0.06, 3.97917, 0.06) | (-4.78125, 3.5313, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkRail12S2 | cube | (0.06, 3.97917, 0.06) | (-1.78125, 3.5313, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass13 | cube | (3, 3.97917, 0.18) | (-3.28125, 7.51047, 19.91) | (0, 0, -0) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail13S0 | cube | (0.06, 3.97917, 0.06) | (-4.78125, 7.51047, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkRail13S2 | cube | (0.06, 3.97917, 0.06) | (-1.78125, 7.51047, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass14 | cube | (3, 3.97917, 0.18) | (-3.28125, 11.4896, 19.91) | (0, 0, -0) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail14S0 | cube | (0.06, 3.97917, 0.06) | (-4.78125, 11.4896, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkRail14S2 | cube | (0.06, 3.97917, 0.06) | (-1.78125, 11.4896, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass15 | cube | (3, 3.97917, 0.18) | (-3.28125, 15.4688, 19.91) | (0, 0, -0) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail15S0 | cube | (0.06, 3.97917, 0.06) | (-4.78125, 15.4688, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkRail15S2 | cube | (0.06, 3.97917, 0.06) | (-1.78125, 15.4688, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass16 | cube | (3, 3.97917, 0.18) | (-3.28125, 19.448, 19.91) | (0, 0, -0) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail16S0 | cube | (0.06, 3.97917, 0.06) | (-4.78125, 19.448, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkRail16S2 | cube | (0.06, 3.97917, 0.06) | (-1.78125, 19.448, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass17 | cube | (3, 3.97917, 0.18) | (-3.28125, 23.4271, 19.91) | (0, 0, -0) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail17S0 | cube | (0.06, 3.97917, 0.06) | (-4.78125, 23.4271, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkRail17S2 | cube | (0.06, 3.97917, 0.06) | (-1.78125, 23.4271, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass18 | cube | (3, 3.97917, 0.18) | (-3.28125, 27.4063, 19.91) | (0, 0, -0) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail18S0 | cube | (0.06, 3.97917, 0.06) | (-4.78125, 27.4063, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkRail18S2 | cube | (0.06, 3.97917, 0.06) | (-1.78125, 27.4063, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass19 | cube | (3, 3.97917, 0.18) | (-3.28125, 31.3855, 19.91) | (0, 0, -0) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail19S0 | cube | (0.06, 3.97917, 0.06) | (-4.78125, 31.3855, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkRail19S2 | cube | (0.06, 3.97917, 0.06) | (-1.78125, 31.3855, 21.1) | (0, 0, -0) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass20 | cube | (3, 3.9786, 0.05549) | (-3.2689, 35.3643, 19.9723) | (0, 0, -0.355774) | center | Root | Sky | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail20S0 | cube | (0.06, 3.9786, 0.06) | (-4.76887, 35.3736, 21.1) | (0, 0, -0.355774) | center | Root | Concrete | 없음 | [설정] |
| WalkRail20S2 | cube | (0.06, 3.9786, 0.06) | (-1.76893, 35.355, 21.1) | (0, 0, -0.355774) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass21 | cube | (3, 3.93827, 0.05549) | (-2.62348, 39.2182, 19.9723) | (0, 0, -18.7533) | center | Root | Sky | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail21S0 | cube | (0.06, 3.93827, 0.06) | (-4.04385, 39.7004, 21.1) | (0, 0, -18.7533) | center | Root | Concrete | 없음 | [설정] |
| WalkRail21S2 | cube | (0.06, 3.93827, 0.06) | (-1.20311, 38.7359, 21.1) | (0, 0, -18.7533) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass22 | cube | (3, 3.93827, 0.05549) | (-0.544386, 42.4194, 19.9723) | (0, 0, -47.252) | center | Root | Sky | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail22S0 | cube | (0.06, 3.93827, 0.06) | (-1.56255, 43.5209, 21.1) | (0, 0, -47.252) | center | Root | Concrete | 없음 | [설정] |
| WalkRail22S2 | cube | (0.06, 3.93827, 0.06) | (0.473777, 41.3179, 21.1) | (0, 0, -47.252) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass23 | cube | (3, 3.93827, 0.05549) | (2.8102, 44.2407, 19.9723) | (0, 0, -75.7507) | center | Root | Sky | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail23S0 | cube | (0.06, 3.93827, 0.06) | (2.44098, 45.6945, 21.1) | (0, 0, -75.7507) | center | Root | Concrete | 없음 | [설정] |
| WalkRail23S2 | cube | (0.06, 3.93827, 0.06) | (3.17941, 42.7868, 21.1) | (0, 0, -75.7507) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass24 | cube | (3, 3.93827, 0.05549) | (6.6273, 44.2407, 19.9723) | (0, 0, -104.249) | center | Root | Sky | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail24S0 | cube | (0.06, 3.93827, 0.06) | (6.99652, 45.6945, 21.1) | (0, 0, -104.249) | center | Root | Concrete | 없음 | [설정] |
| WalkRail24S2 | cube | (0.06, 3.93827, 0.06) | (6.25809, 42.7868, 21.1) | (0, 0, -104.249) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass25 | cube | (3, 3.93827, 0.05549) | (9.98189, 42.4194, 19.9723) | (0, 0, -132.748) | center | Root | Sky | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail25S0 | cube | (0.06, 3.93827, 0.06) | (11, 43.5209, 21.1) | (0, 0, -132.748) | center | Root | Concrete | 없음 | [설정] |
| WalkRail25S2 | cube | (0.06, 3.93827, 0.06) | (8.96372, 41.3179, 21.1) | (0, 0, -132.748) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass26 | cube | (3, 3.93827, 0.05549) | (12.061, 39.2182, 19.9723) | (0, 0, -161.247) | center | Root | Sky | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail26S0 | cube | (0.06, 3.93827, 0.06) | (13.4813, 39.7004, 21.1) | (0, 0, -161.247) | center | Root | Concrete | 없음 | [설정] |
| WalkRail26S2 | cube | (0.06, 3.93827, 0.06) | (10.6406, 38.7359, 21.1) | (0, 0, -161.247) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass27 | cube | (3, 3.9786, 0.05549) | (12.7064, 35.3643, 19.9723) | (0, 0, -179.644) | center | Root | Sky | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail27S0 | cube | (0.06, 3.9786, 0.06) | (14.2064, 35.3736, 21.1) | (0, 0, -179.644) | center | Root | Concrete | 없음 | [설정] |
| WalkRail27S2 | cube | (0.06, 3.9786, 0.06) | (11.2064, 35.355, 21.1) | (0, 0, -179.644) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass28 | cube | (3, 3.97917, 0.18) | (12.7188, 31.3855, 19.91) | (0, 0, -180) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail28S0 | cube | (0.06, 3.97917, 0.06) | (14.2188, 31.3855, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkRail28S2 | cube | (0.06, 3.97917, 0.06) | (11.2188, 31.3855, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass29 | cube | (3, 3.97917, 0.18) | (12.7188, 27.4063, 19.91) | (0, 0, -180) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail29S0 | cube | (0.06, 3.97917, 0.06) | (14.2188, 27.4063, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkRail29S2 | cube | (0.06, 3.97917, 0.06) | (11.2188, 27.4063, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass30 | cube | (3, 3.97917, 0.18) | (12.7188, 23.4271, 19.91) | (0, 0, -180) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail30S0 | cube | (0.06, 3.97917, 0.06) | (14.2188, 23.4271, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkRail30S2 | cube | (0.06, 3.97917, 0.06) | (11.2188, 23.4271, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass31 | cube | (3, 3.97917, 0.18) | (12.7188, 19.448, 19.91) | (0, 0, -180) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail31S0 | cube | (0.06, 3.97917, 0.06) | (14.2188, 19.448, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkRail31S2 | cube | (0.06, 3.97917, 0.06) | (11.2188, 19.448, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass32 | cube | (3, 3.97917, 0.18) | (12.7188, 15.4688, 19.91) | (0, 0, -180) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail32S0 | cube | (0.06, 3.97917, 0.06) | (14.2188, 15.4688, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkRail32S2 | cube | (0.06, 3.97917, 0.06) | (11.2188, 15.4688, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass33 | cube | (3, 3.97917, 0.18) | (12.7188, 11.4896, 19.91) | (0, 0, -180) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail33S0 | cube | (0.06, 3.97917, 0.06) | (14.2188, 11.4896, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkRail33S2 | cube | (0.06, 3.97917, 0.06) | (11.2188, 11.4896, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass34 | cube | (3, 3.97917, 0.18) | (12.7188, 7.51047, 19.91) | (0, 0, -180) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail34S0 | cube | (0.06, 3.97917, 0.06) | (14.2188, 7.51047, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkRail34S2 | cube | (0.06, 3.97917, 0.06) | (11.2188, 7.51047, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass35 | cube | (3, 3.97917, 0.18) | (12.7188, 3.5313, 19.91) | (0, 0, -180) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail35S0 | cube | (0.06, 3.97917, 0.06) | (14.2188, 3.5313, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkRail35S2 | cube | (0.06, 3.97917, 0.06) | (11.2188, 3.5313, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass36 | cube | (3, 3.97917, 0.18) | (12.7188, -0.447862, 19.91) | (0, 0, -180) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail36S0 | cube | (0.06, 3.97917, 0.06) | (14.2188, -0.447862, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkRail36S2 | cube | (0.06, 3.97917, 0.06) | (11.2188, -0.447862, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass37 | cube | (3, 3.97917, 0.18) | (12.7188, -4.42703, 19.91) | (0, 0, -180) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail37S0 | cube | (0.06, 3.97917, 0.06) | (14.2188, -4.42703, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkRail37S2 | cube | (0.06, 3.97917, 0.06) | (11.2188, -4.42703, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass38 | cube | (3, 3.97917, 0.18) | (12.7188, -8.4062, 19.91) | (0, 0, -180) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail38S0 | cube | (0.06, 3.97917, 0.06) | (14.2188, -8.4062, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkRail38S2 | cube | (0.06, 3.97917, 0.06) | (11.2188, -8.4062, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass39 | cube | (3, 3.97917, 0.18) | (12.7188, -12.3854, 19.91) | (0, 0, -180) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail39S0 | cube | (0.06, 3.97917, 0.06) | (14.2188, -12.3854, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkRail39S2 | cube | (0.06, 3.97917, 0.06) | (11.2188, -12.3854, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass40 | cube | (3, 3.97917, 0.18) | (12.7188, -16.3645, 19.91) | (0, 0, -180) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail40S0 | cube | (0.06, 3.97917, 0.06) | (14.2188, -16.3645, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkRail40S2 | cube | (0.06, 3.97917, 0.06) | (11.2188, -16.3645, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass41 | cube | (3, 3.97917, 0.18) | (12.7188, -20.3437, 19.91) | (0, 0, -180) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail41S0 | cube | (0.06, 3.97917, 0.06) | (14.2188, -20.3437, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkRail41S2 | cube | (0.06, 3.97917, 0.06) | (11.2188, -20.3437, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass42 | cube | (3, 3.97917, 0.18) | (12.7188, -24.3229, 19.91) | (0, 0, -180) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail42S0 | cube | (0.06, 3.97917, 0.06) | (14.2188, -24.3229, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkRail42S2 | cube | (0.06, 3.97917, 0.06) | (11.2188, -24.3229, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass43 | cube | (3, 3.97917, 0.18) | (12.7188, -28.302, 19.91) | (0, 0, -180) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail43S0 | cube | (0.06, 3.97917, 0.06) | (14.2188, -28.302, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkRail43S2 | cube | (0.06, 3.97917, 0.06) | (11.2188, -28.302, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass44 | cube | (3, 3.97917, 0.18) | (12.7188, -32.2812, 19.91) | (0, 0, -180) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail44S0 | cube | (0.06, 3.97917, 0.06) | (14.2188, -32.2812, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkRail44S2 | cube | (0.06, 3.97917, 0.06) | (11.2188, -32.2812, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass45 | cube | (3, 3.97917, 0.18) | (12.7188, -36.2604, 19.91) | (0, 0, -180) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail45S0 | cube | (0.06, 3.97917, 0.06) | (14.2188, -36.2604, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkRail45S2 | cube | (0.06, 3.97917, 0.06) | (11.2188, -36.2604, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass46 | cube | (3, 3.97917, 0.18) | (12.7188, -40.2395, 19.91) | (0, 0, -180) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail46S0 | cube | (0.06, 3.97917, 0.06) | (14.2188, -40.2395, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkRail46S2 | cube | (0.06, 3.97917, 0.06) | (11.2188, -40.2395, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkGlass47 | cube | (3, 3.97917, 0.18) | (12.7188, -44.2187, 19.91) | (0, 0, -180) | center | Root | Concrete | 없음 | X=3m [확인: FACTS.md ENV14], Y/Z [설정] |
| WalkRail47S0 | cube | (0.06, 3.97917, 0.06) | (14.2188, -44.2187, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkRail47S2 | cube | (0.06, 3.97917, 0.06) | (11.2188, -44.2187, 21.1) | (0, 0, -180) | center | Root | Concrete | 없음 | [설정] |
| WalkPier0 | cube | (0.5, 0.5, 19.7) | (-3.28125, -36.2083, 9.85) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| WalkPier1 | cube | (0.5, 0.5, 19.7) | (12.7188, -36.2083, 9.85) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| WalkPier2 | cube | (0.5, 0.5, 19.7) | (-3.28125, 13.7917, 9.85) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| WalkPier3 | cube | (0.5, 0.5, 19.7) | (12.7188, 13.7917, 9.85) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| CoastalTrackRail0 | cube | (0.07, 12, 0.12) | (-13.9988, -26.2083, 0.12) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| CoastalTrackRail2 | cube | (0.07, 12, 0.12) | (-12.5637, -26.2083, 0.12) | (0, 0, 0) | center | Root | Concrete | 없음 | [설정] |
| CoastalTrackSleeper0 | cube | (1.935, 0.2, 0.1) | (-13.2812, -31.9083, 0.05) | (0, 0, 0) | center | Root | Wood | 없음 | [설정] |
| CoastalTrackSleeper1 | cube | (1.935, 0.2, 0.1) | (-13.2812, -31.3083, 0.05) | (0, 0, 0) | center | Root | Wood | 없음 | [설정] |
| CoastalTrackSleeper2 | cube | (1.935, 0.2, 0.1) | (-13.2812, -30.7083, 0.05) | (0, 0, 0) | center | Root | Wood | 없음 | [설정] |
| CoastalTrackSleeper3 | cube | (1.935, 0.2, 0.1) | (-13.2812, -30.1083, 0.05) | (0, 0, 0) | center | Root | Wood | 없음 | [설정] |
| CoastalTrackSleeper4 | cube | (1.935, 0.2, 0.1) | (-13.2812, -29.5083, 0.05) | (0, 0, 0) | center | Root | Wood | 없음 | [설정] |
| CoastalTrackSleeper5 | cube | (1.935, 0.2, 0.1) | (-13.2812, -28.9083, 0.05) | (0, 0, 0) | center | Root | Wood | 없음 | [설정] |
| CoastalTrackSleeper6 | cube | (1.935, 0.2, 0.1) | (-13.2812, -28.3083, 0.05) | (0, 0, 0) | center | Root | Wood | 없음 | [설정] |
| CoastalTrackSleeper7 | cube | (1.935, 0.2, 0.1) | (-13.2812, -27.7083, 0.05) | (0, 0, 0) | center | Root | Wood | 없음 | [설정] |
| CoastalTrackSleeper8 | cube | (1.935, 0.2, 0.1) | (-13.2812, -27.1083, 0.05) | (0, 0, 0) | center | Root | Wood | 없음 | [설정] |
| CoastalTrackSleeper9 | cube | (1.935, 0.2, 0.1) | (-13.2812, -26.5083, 0.05) | (0, 0, 0) | center | Root | Wood | 없음 | [설정] |
| CoastalTrackSleeper10 | cube | (1.935, 0.2, 0.1) | (-13.2812, -25.9083, 0.05) | (0, 0, 0) | center | Root | Wood | 없음 | [설정] |
| CoastalTrackSleeper11 | cube | (1.935, 0.2, 0.1) | (-13.2812, -25.3083, 0.05) | (0, 0, 0) | center | Root | Wood | 없음 | [설정] |
| CoastalTrackSleeper12 | cube | (1.935, 0.2, 0.1) | (-13.2812, -24.7083, 0.05) | (0, 0, 0) | center | Root | Wood | 없음 | [설정] |
| CoastalTrackSleeper13 | cube | (1.935, 0.2, 0.1) | (-13.2812, -24.1083, 0.05) | (0, 0, 0) | center | Root | Wood | 없음 | [설정] |
| CoastalTrackSleeper14 | cube | (1.935, 0.2, 0.1) | (-13.2812, -23.5083, 0.05) | (0, 0, 0) | center | Root | Wood | 없음 | [설정] |
| CoastalTrackSleeper15 | cube | (1.935, 0.2, 0.1) | (-13.2812, -22.9083, 0.05) | (0, 0, 0) | center | Root | Wood | 없음 | [설정] |
| CoastalTrackSleeper16 | cube | (1.935, 0.2, 0.1) | (-13.2812, -22.3083, 0.05) | (0, 0, 0) | center | Root | Wood | 없음 | [설정] |
| CoastalTrackSleeper17 | cube | (1.935, 0.2, 0.1) | (-13.2812, -21.7083, 0.05) | (0, 0, 0) | center | Root | Wood | 없음 | [설정] |
| CoastalTrackSleeper18 | cube | (1.935, 0.2, 0.1) | (-13.2812, -21.1083, 0.05) | (0, 0, 0) | center | Root | Wood | 없음 | [설정] |
| CoastalTrackSleeper19 | cube | (1.935, 0.2, 0.1) | (-13.2812, -20.5083, 0.05) | (0, 0, 0) | center | Root | Wood | 없음 | [설정] |

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
| WalkGlass0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail0S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail0S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass1 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail1S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail1S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail2S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail2S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass3 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail3S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail3S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass4 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail4S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail4S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass5 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail5S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail5S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass6 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail6S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail6S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass7 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail7S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail7S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass8 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail8S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail8S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass9 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail9S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail9S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass10 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail10S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail10S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass11 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail11S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail11S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass12 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail12S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail12S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass13 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail13S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail13S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass14 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail14S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail14S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass15 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail15S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail15S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass16 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail16S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail16S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass17 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail17S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail17S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass18 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail18S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail18S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass19 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail19S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail19S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass20 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail20S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail20S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass21 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail21S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail21S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass22 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail22S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail22S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass23 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail23S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail23S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass24 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail24S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail24S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass25 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail25S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail25S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass26 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail26S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail26S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass27 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail27S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail27S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass28 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail28S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail28S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass29 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail29S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail29S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass30 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail30S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail30S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass31 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail31S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail31S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass32 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail32S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail32S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass33 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail33S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail33S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass34 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail34S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail34S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass35 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail35S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail35S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass36 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail36S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail36S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass37 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail37S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail37S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass38 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail38S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail38S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass39 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail39S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail39S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass40 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail40S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail40S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass41 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail41S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail41S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass42 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail42S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail42S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass43 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail43S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail43S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass44 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail44S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail44S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass45 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail45S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail45S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass46 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail46S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail46S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkGlass47 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail47S0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkRail47S2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkPier0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkPier1 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkPier2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| WalkPier3 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| CoastalTrackRail0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| CoastalTrackRail2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| CoastalTrackSleeper0 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| CoastalTrackSleeper1 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| CoastalTrackSleeper2 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| CoastalTrackSleeper3 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| CoastalTrackSleeper4 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| CoastalTrackSleeper5 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| CoastalTrackSleeper6 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| CoastalTrackSleeper7 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| CoastalTrackSleeper8 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| CoastalTrackSleeper9 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| CoastalTrackSleeper10 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| CoastalTrackSleeper11 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| CoastalTrackSleeper12 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| CoastalTrackSleeper13 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| CoastalTrackSleeper14 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| CoastalTrackSleeper15 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| CoastalTrackSleeper16 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| CoastalTrackSleeper17 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| CoastalTrackSleeper18 | 235 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| CoastalTrackSleeper19 | 285 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| 합계 | 40,000 [설정] | 위 합계 | 없음 | 등급 H, 완성 목표 예산 |

블록아웃은 예산 하한까지 의미 없이 세분하지 않는다. 키트는 K2/K5의 모듈 예산과 시설 전체 전시본을 구분. 군중 한 캐릭터는 300tris 이하 [설정: 지시서]. 최종 평가 메시·glTF 삼각형은 validation.md.

## 8. 재질표
| 재질 이름 | 색 hex (팔레트 이름) | 거칠기 | 금속성 | 노멀 강도 | 야간 발광 색·강도 | 투명도·IOR |
|---|---|---|---|---|---|---|
| M_CoastalRailDaritdol_Sky | #A9D6F0 (전역 팔레트) | 0.12 | 0 | 0 | 없음 / 0 | Alpha 0.3, IOR 1.45 [설정: 행 전체] |
| M_CoastalRailDaritdol_Concrete | #B9B6AE (전역 팔레트) | 0.65 | 0 | 0 | 없음 / 0 | Alpha 1, IOR 1.5 [설정: 행 전체] |
| M_CoastalRailDaritdol_Wood | #9A7350 (전역 팔레트) | 0.65 | 0 | 0 | 없음 / 0 | Alpha 1, IOR 1.5 [설정: 행 전체] |

색은 INSTRUCTIONS.md 전역 팔레트, 수치는 측색값이 아닌 [설정]. 텍스처 `T_CoastalRailDaritdol_BaseColor`, `T_CoastalRailDaritdol_Normal`, `T_CoastalRailDaritdol_ORM`, `T_CoastalRailDaritdol_Emission`. ORM R=AO/G=Roughness/B=Metallic [설정]. 현재 블록아웃은 단순 PBR 색, 고유 텍스처 미포함. 반복 재질은 트림·타일, 가상 표시는 별도 UV 아틀라스. 텍셀 밀도는 등급별 위 값, 긴 시설은 고유 한 장으로 펴지 않는다.

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
Subject: coastal rail kit and U-shaped Daritdol observation walkway.
Model-design bounds, not surveyed measurements: X 28.4975 m, Y 92.4166 m, Z 21.13 m. Z up, front negative Y; floor-center origin. All unspecified details are fictional artistic settings. Preserve confirmed facts listed in spec.md.
Layout: 4 views in a 2x2 grid — FRONT, RIGHT SIDE, BACK, TOP — all at exactly the same scale, aligned to a faint 1-meter grid, true orthographic projection, no perspective.
Style: stylized miniature diorama, soft bevels, simplified forms, clean dark outlines, flat even lighting, no cast shadows, light gray background.
Include: a 1.7 m human silhouette beside each view for scale; palette swatches: #9A7350, #A9D6F0, #B9B6AE.
Exclude: brand logos, readable commercial signage, copied application screens, watermarks, scenery backgrounds. Use generic brands and original sculpture designs. Written dimensions and executable blockout take precedence over any illustration.
```

images/front.png, right.png, back.png, top.png는 실제 블록아웃의 동일 배율 직교 렌더. 작은 소품은 detail.png에 별도 확대, 실측 근거로 사용하지 않음. 성인 1.70m [설정] 비교용 실루엣은 프리뷰 전용이며 저장 에셋에서 제외. 렌더 투영의 겹침이나 의도된 임시 형상은 최종 메시 품질을 보장하지 않는다.

## 13. 확실하지 않은 값과 필요한 사진
| 값 | 현재 값 | 태그 | 영향도 (상·중·하) | 확정에 필요한 사진 (대상·각도) |
|---|---|---|---|---|
| 실측 외곽·세부 비례 | (28.4975, 92.4166, 21.13) m [설정] | [설정] 또는 위 원자료의 [추정] | 상 | 전체 정면·정측면·배면·높은 사선, 성인 또는 규격 기준물과 함께 |
| 재질·그래픽·접합 | 전역 팔레트·가상 디자인 [설정] | [설정] 또는 위 원자료의 [추정] | 중 | 재료 근접·연결부·사용 장면 사진; 실제 로고는 재현하지 않음 |

사진 제공 전에는 위 제작 설정으로 진행하되 [확인]으로 격상하지 않는다. 사진·좌표·실측 제공 시 버전을 올려 보정한다. 사용자 요청에 따라 전체 항목을 일괄 초안 작성하므로 개별 사진 요청으로 작업을 중단하지 않는다.

## 14. 블록아웃 스크립트
- 파일: `blockout.py`, templates/blockout_template.py에서 에셋 정보·재질·부품만 채우고 공용 함수는 동일하게 유지. VERSION과 SPEC_VERSION=v1.0 동기화.
- 외부 검사: `python blockout.py --self-test`.
- Blender 실행: `blender --background --factory-startup --python blockout.py`.
- REPORT 목표 dims_m=28.497x92.417x21.130, 허용 .01m [설정], triangles≤40000 [설정], 바닥 min_z=0 [설정].
- `CoastalRailDaritdol_blockout.blend`와 `CoastalRailDaritdol_blockout.glb`는 초안 정적 형상. 최종 외피·디테일·UV·리그·키프레임·LOD 변형은 명시된 후속 모델링 작업. 변환 Apply, 미터 단위. GLB는 표준 Y-up 저장 후 Blender 재가져오기에서 Z-up 치수 확인.
- 실행·중복·외곽·예산·이름·변환·GLB 검사 결과는 validation.md. 참고 렌더는 실제 GLB 재가져오기 메시로 생성.

## (종류별 추가 섹션)

### K1 그리드
수평 스냅 0.5 m [설정], 연결 피벗은 모듈 끝면 중심. 감천 주택 수직 스냅은 2.7 m [설정: FACTS.md], 다른 모듈 층고는 PARTS의 명시 치수. 회전 스냅 90° [설정]. 시설 전체 전시본과 반복할 모듈을 구분한다.
- CoastalTrack 직선 12 m [설정], 궤간 1.435 m [설정: 실제 노선 실측 아님], Walk는 확인 치수 시설 전체 전시본.
### K2 모듈 목록
| 모듈 ID | 치수 X×Y×Z (m) | 연결 면 | 부품 수·변형 | 완성 예산 |
|---|---|---|---|---|
| Track12 | (1.935, 12, 0.18) [설정] | ±Y 또는 아래 규칙 | 22개 부품 [설정] | 1,000 triangles/module [설정] |
| WalkPanel | (3.06, 3.97917, 1.31) [설정] | ±Y 또는 아래 규칙 | 3개 부품 [설정] | 1,000 triangles/module [설정] |
| Pier | (0.5, 0.5, 19.7) [설정] | ±Y 또는 아래 규칙 | 1개 부품 [설정] | 1,000 triangles/module [설정] |
모듈별 실제 부품 이름 목록은 `modules.json`. 그 이름의 메시를 함께 복사하고 전체 바닥 중앙 피벗으로 재추출한다. 임의 부품 하나만 복제해 모듈이라고 부르지 않는다.

### K3 조합 규칙
보행로 유효 폭 2 m [설정] 미만을 금지, 출입문 앞 장애물 금지, 기둥·바닥 겹침 금지. 연결부 높이를 맞추고 공중에 뜬 바닥 금지. 팔레트 배분 Coral 20% / Yellow 15% / Mint 20% / Blue 15% / Lavender 10% / White 20% [설정, 합계 100%]. 토목 모듈은 Concrete·Wood 유지. 복제 주택은 같은 색 연속 3개 [설정] 금지, 수평 회전 0/90/180/270° [설정], 소품 위치 ±0.15 m [설정] 범위에서만 변형. 난간·레일은 회전 랜덤을 끄고 접선 방향 유지.

### K4 배치 자동화
`placement.py`의 `place(module_id, count, spacing, seed=20261110)` 사용. random.Random 지역 인스턴스, 시드 20261110 [설정] 고정. 원본을 변경하지 않고 모듈 부품별 mesh.data 공유 인스턴스를 새 컬렉션에 생성. 기준 배치는 선형이라 연결 오류를 점검하기 쉽다. 실제 지형 스냅은 사용자 사진·씬 지형 확인 후 적용한다.

### K5 화면 크기별(소·중·대) 예시 배치
| 화면 | 모듈 수 | 오브젝트 수 | 완성 삼각형 합계 |
|---|---|---|---|
| 소 | 4 [설정] | 88 [설정: 첫 모듈 22부품×4] | 4,000 [설정: 1,000×4] |
| 중 | 16 [설정] | 352 [설정: 첫 모듈 22부품×16] | 16,000 [설정: 1,000×16] |
| 대 | 48 [설정] | 1056 [설정: 첫 모듈 22부품×48] | 48,000 [설정: 1,000×48] |
블록아웃 실측 삼각형은 validation.md, 위 표는 완성 모듈 예산 기준. 큰 시설의 전체 전시본을 모듈 한 개로 가정한 수치가 아니다.

---

## Changelog
- v1.0 — 2026-11-10 — 설계도·블록아웃·참고 프롬프트·직교 참고 이미지·정적 blend/GLB·검증 기록 최초 작성, 실측 미확정 항목 분리.
