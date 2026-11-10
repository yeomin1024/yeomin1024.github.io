# FX03 김·연기 효과 설계도

버전: v1.0 — 2026-11-10 — 효과 노드·수치·프리셋 최초 작성
상태: 초안
폴더: `busan-3d/assets/FX03_SteamSmoke/`

INSTRUCTIONS.md 8장의 FX 예외 적용. 3D 모델이 아니므로 일반 모델링 양식·삼각형·GLB 납품 대신 노드 라이브러리와 설정 스크립트로 제공한다. 숫자는 ID·버전·날짜·노드 식별자를 제외하고 아래 태그를 적용.

## 목적과 범위
reusable steam and smoke volume shader. 등장: 음식·불판 [설정: 레지스트리 씬 계획]. 음식 재료·버스 노선·정류장 정보는 FACTS.md를 따른다. 효과 수치는 실측값이 아닌 연출 설정.

## 셰이더·컴포지터 노드 구성
- Object coordinates + time [설정]
- Advection Z -.08 m/s [설정]
- Noise scale 12 [설정]
- Ramp .4 to .7 / density .08 [설정]
- Volume anisotropy .2 [설정]
- Volume output [설정]

노드 연결과 입력값의 실행 가능한 정의는 `setup.py`. material()은 노드를 재생성하여 중복 누적을 막고 setup()을 반복 호출해도 같은 이름의 재질·월드·태양을 재사용한다. FX01의 좌표와 FX03의 좌표는 Object를 사용하므로 효과 컨테이너의 scale=1 [설정], 단위 1m [설정]를 적용한다. 시간은 frame/24 [설정] 초 기준.

## 핵심 수치
| 항목 | 값 | 근거 |
|---|---|---|
| FPS | 24 | [설정: 영상 규격] |
| Sea IOR / Roughness / Bump | 1.33 / .22 / .18 | [설정] |
| 파도 이동 | .12m/s | [설정] |
| 김 상승 / 수명 / 개수 | .08m/s / 1.8s / 초당 8개 | [설정] |
| 볼륨 밀도 최대 / anisotropy | .08 / .2 | [설정] |
| 카드 페이드 / 홀드 / 아웃 | 6 / 96 / 6 frames | [설정] |
| 자막 기준 화면 / 최종 | 1920×1080 / 3840×2160 | [설정: 영상 규격] |
| UI 안전 여백 / 본문 글자 | 64px / 42px at 1080p | [설정] |

해당 효과에 해당하는 행만 적용. 파도는 노멀 효과이며 실제 지오메트리 파도·해안 충돌 시뮬레이션이 아니다. 김은 컨테이너 볼륨 재질이며 입자 방출기·컨테이너 위치는 음식 SteamSocket에서 후속 배치한다. 카드 SVG는 2D 그래픽, 실제 지도 앱 화면을 복제하지 않는다.

## 시간대별 프리셋
모든 값 [설정]. 태양 elevation/azimuth는 연출 각도, 공식 일조 방위 계산값이 아님.

| 시간대 | World hex | World strength | Sun strength | Elevation / Azimuth ° | Exposure |
|---|---|---|---|---|---|
| 아침 | #A9D6F0 | .55 | 2 | 25 / 110 | 0 |
| 정오 | #A9D6F0 | .8 | 3 | 60 / 180 | 0 |
| 일몰 | #F28C5B | .28 | 1.1 | 6 / 250 | −.3 |
| 밤 | #121A33 | .08 | .12 | 30 / 40 | −.5 |

바다·하늘·발광은 전역 팔레트만 사용. 밤 음식 김은 배경과 분리되는 웜 화이트 림 조명을 프리셋 외 개별 조명으로 추가하되 기본 밀도를 과도하게 올리지 않는다. 카드 낮/밤 색은 본문 오프화이트·배경 밤하늘, 대비는 실제 렌더에서 확인한다.

## 움직임과 합성
FX01: 좌표 Y에 −frame/24×.12 [설정] 더함. FX03: 좌표 Z에 −frame/24×.08 [설정] 더해 상승 패턴. FX04: alpha=smoothstep(0,6,frame−start)×(1−smoothstep(102,108,frame−start)) [설정]. 카드 텍스트는 버스 번호·정류장명·시간만 표시, 실제 브랜드명·앱 레이아웃 미복제. 입출력 알파는 premultiplied 기준으로 Alpha Over에서 가장자리 검수.

## 참고 이미지 프롬프트 (영어)
```
reusable steam and smoke volume shader; technical shader/compositor diagram; show node links, artistic parameter values and morning/noon/sunset/night palette swatches; no logos, no copied application screens. All numerical values are design settings. Clean light background and readable labels.
```
`images/reference.svg`는 실제 노드 사양을 요약한 벡터 참고도. 수치는 setup.py와 위 표가 우선한다.

## 미확정 값과 검증
파도 속도·카메라 노출·볼륨 밀도·UI 배치는 연출 설정. 최종 씬 수면 크기·태양 방향·배경 명도·음식 근접 컷 또는 화면 녹화가 있어야 최종 보정 가능. `validation.md`에 라이브러리 실행·중복·필수 노드·프리셋 검증 기록.
FX04는 컴포지터 Image 노드에 투명 PNG를 연결해야 한다. 제공된 cards.svg를 렌더 툴에서 PNG로 출력하여 연결한다. 입력 이미지 미연결 상태는 완성 합성으로 주장하지 않는다.

## Changelog
- v1.0 — 2026-11-10 — 효과·설정 초안 최초 작성, 실측값과 연출 수치 분리.
