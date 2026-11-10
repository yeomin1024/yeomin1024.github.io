# SF02 버스 실내 (교통카드 단말기·하차벨·손잡이·좌석) 설계도

버전: v1.0 — 2026-11-10 — 일괄 제작 초안 최초 작성
상태: 초안
폴더: `busan-3d/assets/SF02_BusInterior/`

ID·버전·날짜·섹션 번호·파일명은 식별자. 표의 근거 태그는 해당 행의 모든 수치에 적용한다. 확인된 실제 시설 수치와 제작용 부품 치수를 아래에서 분리한다. 이 납품은 모델러용 설계·비례 블록아웃이며 최종 리토폴로지·텍스처·리그·애니메이션 확정본이 아니다.

## 1. 개요
| 항목 | 내용 |
|---|---|
| 등장 장면 | 버스 탑승 컷 [설정: 레지스트리 장면 계획], 세부 일정 FACTS.md |
| 화면에서의 역할 | bus interior modules: card validator, stop bell, strap, seat and pole |
| 등급 | H |
| 가장 가까운 카메라 거리 | 1.98m [설정] |
| 화면 점유율 | 최대 80% [설정], 상세 컷 95% [설정] |

- 대상과 등장 장면은 REGISTRY.md·FACTS.md의 제작 계획. 이 초안의 개별 실측값은 확인되지 않았으며 치수는 [설정].

## 2. 핵심 특징
- **지켜야 할 것**
- 카드 단말기
- 하차벨
- 손잡이
- 좌석
- 소켓
- **생략·단순화할 것**
  - 실제 상호·로고·상표·앱 화면은 가상 그래픽으로 대체.
  - 안 보이는 하부·내부는 삭제, 주요 실루엣과 접합부 우선.
  - 미세 반복 패턴은 노멀·트림시트로 처리.
  - 사진 미제공 치수는 실측으로 주장하지 않음.

VEH02의 InteriorSocket=(0,0,.34)m [설정], ValidatorSocket=(−.62,−4.65,1.35)m [설정]에 맞춰 개별 모듈 연결. 여기서는 모듈별 전시 배치.

## 3. 치수표
| 부위 | 가로 X (m) | 깊이 Y (m) | 높이 Z (m) | 근거 태그 | 근거·계산식 |
|---|---|---|---|---|---|
| 전체 | 1.84 | 0.7625 | 2.2 | [설정] | PARTS 회전·피벗 포함 AABB 사전 계산, minZ=0 [설정] |
| SeatBase (로컬) | 0.46 | 0.48 | 0.12 | [설정] | PARTS; 회전 전 전체 크기 |
| SeatBack (로컬) | 0.46 | 0.12 | 0.65 | [설정] | PARTS; 회전 전 전체 크기 |
| Pole (로컬) | 0.035 | 0.035 | 2.2 | [설정] | PARTS; 회전 전 전체 크기 |
| StopBell (로컬) | 0.07 | 0.04 | 0.06 | [설정] | PARTS; 회전 전 전체 크기 |
| Validator (로컬) | 0.22 | 0.16 | 0.3 | [설정] | PARTS; 회전 전 전체 크기 |
| ValidatorScreen (로컬) | 0.15 | 0.015 | 0.12 | [설정] | PARTS; 회전 전 전체 크기 |
| TapZone (로컬) | 0.14 | 0.02 | 0.07 | [설정] | PARTS; 회전 전 전체 크기 |
| StrapStem (로컬) | 0.035 | 0.035 | 0.24 | [설정] | PARTS; 회전 전 전체 크기 |
| StrapGrip (로컬) | 0.16 | 0.045 | 0.045 | [설정] | PARTS; 회전 전 전체 크기 |

사람 1.70m [설정: 지시서 스케일 기준] 대비 높이 1.294배 [설정]. 복합 전시본은 시설·모듈 전체 경계이며 개별 부품 실측으로 오해하지 않는다. 확인값은 개요 원자료에 별도 표기.

소품·식기 치수 mm 병기: 각 표의 m 값 × 1000 [설정].

| 부품 | X×Y×Z (mm) | 근거 |
|---|---|---|
| SeatBase | (460, 480, 120) | [설정] |
| SeatBack | (460, 120, 650) | [설정] |
| Pole | (35, 35, 2200) | [설정] |
| StopBell | (70, 40, 60) | [설정] |
| Validator | (220, 160, 300) | [설정] |
| ValidatorScreen | (150, 15, 120) | [설정] |
| TapZone | (140, 20, 70) | [설정] |
| StrapStem | (35, 35, 240) | [설정] |
| StrapGrip | (160, 45, 45) | [설정] |
## 4. 정면·측면·윗면 도면
### 4-1. 주요 점 좌표 (에셋 원점 = 바닥 중앙, 단위 m)
| 점 이름 | x | y | z | 설명 |
|---|---|---|---|---|
| 원점 | 0 | 0 | 0 | [설정] Root, AABB 바닥 중앙 |
| 최저 좌전 | -0.92 | -0.38125 | 0 | [설정] 경계 |
| 최고 우후 | 0.92 | 0.38125 | 2.2 | [설정] 경계 |
| 부품·회전축 | PARTS | PARTS | PARTS | [설정] 아래 각 부모 기준 location·pivot을 조합 |

### 4-2. 텍스트 실루엣 (가로세로 비율 유지)
다음은 부품 AABB 투영의 ASCII 요약이다. 문자 셀 가로:세로 약 1:2 [설정]로 보정하되 극단적으로 긴 시설은 높이 표시 최소 줄수 때문에 왜곡될 수 있다. 정확한 비율은 동일 배율 직교 PNG를 기준으로 한다.

```
정면 (-Y에서 본 모습)
                            ##
                            ##
                            ##
                          #####
                          #####
                            ##
                            ##
                           ###              ########
                            ##              ########
#############               ##              ########
#############               ##
#############               ##
#############               ##
#############               ##
#############               ##
                            ##
                            ##
                            ##

측면 (+X에서 본 모습)
              ####
              ####                              ###
              ####                              ###
              ####                             #####
              ####                             #####
              ####
              ####
         #############
         #############
         #############   #########
              ####       #########
              ####       #########
              ####       #########
##################################
##################################
              ####
              ####
              ####

윗면 (+Z에서 본 모습)
                          #####
                          #####


#############
#############
#############                               ########
#############               ##              ########
#############              ###              ########
#############                                ######
#############
```

### 4-3. 치수선
| 치수선 | 시작점 → 끝점 | 길이 (m) |
|---|---|---|
| X | (-0.92,0,0) → (0.92,0,0) | 1.84 [설정] |
| Y | (0,-0.38125,0) → (0,0.38125,0) | 0.7625 [설정] |
| Z | (0,0,0) → (0,0,2.2) | 2.2 [설정] |

## 5. 부품 목록
PARTS와 행별 일치. 최종 이름은 `SF02_BusInterior_{부품}_L0`. 크기는 로컬 전체 치수, sphere는 축별 지름, cylinder/cone는 로컬 지름X·Y와 Z높이. 위치는 부모 기준. pivot 튜플은 도형 중심에서 회전축까지의 오프셋. 원형 부품의 회전은 메시로 베이크한 정적 복제본에서 회전 0°·스케일 1 [설정] 납품. 모든 치수·좌표·회전·분할은 행의 [설정] 적용. Empty 크기는 표시 전용.

| 부품명 | 도형 | 크기 X×Y×Z (m) | 위치 x,y,z (부모 기준) | 회전 x,y,z (°) | 원점(pivot) | 부모 | 재질 | 반복·대칭 | 근거 |
|---|---|---|---|---|---|---|---|---|---|
| Root | empty | (0.1, 0.1, 0.1) | (0, 0, 0) | (0, 0, 0) | center | – | – | 없음 | [설정] |
| SeatBase | cube | (0.46, 0.48, 0.12) | (-0.69, -0.14125, 0.46) | (0, 0, 0) | center | Root | Blue | bevel 0.02m/2seg | [설정] |
| SeatBack | cube | (0.46, 0.12, 0.65) | (-0.69, 0.05875, 0.75) | (0, 0, 0) | center | Root | Blue | bevel 0.02m/2seg | [설정] |
| Pole | cylinder | (0.035, 0.035, 2.2) | (0.11, -0.14125, 1.1) | (0, 0, 0) | center | Root | Yellow | radial 12 | [설정] |
| StopBell | cube | (0.07, 0.04, 0.06) | (0.11, -0.18125, 1.35) | (0, 0, 0) | center | Root | BusRed | bevel 0.01m/2seg | [설정] |
| Validator | cube | (0.22, 0.16, 0.3) | (0.81, -0.14125, 1.2) | (0, 0, 0) | center | Root | Asphalt | bevel 0.02m/2seg | [설정] |
| ValidatorScreen | cube | (0.15, 0.015, 0.12) | (0.81, -0.23125, 1.26) | (0, 0, 0) | center | Root | Cool | bevel 0.008m/2seg | [설정] |
| TapZone | cube | (0.14, 0.02, 0.07) | (0.81, -0.23125, 1.1) | (0, 0, 0) | center | Root | Mint | bevel 0.008m/2seg | [설정] |
| StrapPivot | empty | (0.08, 0.08, 0.08) | (0.11, 0.35875, 2.1) | (0, 0, 0) | center | Root | – | 없음 | [설정] |
| StrapStem | cube | (0.035, 0.035, 0.24) | (0, 0, -0.12) | (0, 0, 0) | center | StrapPivot | Concrete | 없음 | [설정] |
| StrapGrip | cube | (0.16, 0.045, 0.045) | (0, 0, -0.27) | (0, 0, 0) | center | StrapPivot | Yellow | 없음 | [설정] |

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
| SeatBase | 4444 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| SeatBack | 4444 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| Pole | 4444 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| StopBell | 4444 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| Validator | 4444 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| ValidatorScreen | 4444 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| TapZone | 4444 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| StrapStem | 4444 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| StrapGrip | 4448 [설정] | PARTS 표; 최종 모서리 .01m/2seg [설정], 소품은 최소 치수의 2% 이내 [설정] | 없음 | 완성 에셋 배분, 블록아웃 실측과 구분 |
| 합계 | 40,000 [설정] | 위 합계 | 없음 | 등급 H, 완성 목표 예산 |

블록아웃은 예산 하한까지 의미 없이 세분하지 않는다. 키트는 K2/K5의 모듈 예산과 시설 전체 전시본을 구분. 군중 한 캐릭터는 300tris 이하 [설정: 지시서]. 최종 평가 메시·glTF 삼각형은 validation.md.

## 8. 재질표
| 재질 이름 | 색 hex (팔레트 이름) | 거칠기 | 금속성 | 노멀 강도 | 야간 발광 색·강도 | 투명도·IOR |
|---|---|---|---|---|---|---|
| M_BusInterior_Blue | #9DB7E0 (전역 팔레트) | 0.65 | 0 | 0 | 없음 / 0 | Alpha 1, IOR 1.5 [설정: 행 전체] |
| M_BusInterior_Yellow | #F7D57A (전역 팔레트) | 0.65 | 0 | 0 | 없음 / 0 | Alpha 1, IOR 1.5 [설정: 행 전체] |
| M_BusInterior_BusRed | #C8423B (전역 팔레트) | 0.65 | 0 | 0 | 없음 / 0 | Alpha 1, IOR 1.5 [설정: 행 전체] |
| M_BusInterior_Asphalt | #3A3D42 (전역 팔레트) | 0.65 | 0 | 0 | 없음 / 0 | Alpha 1, IOR 1.5 [설정: 행 전체] |
| M_BusInterior_Cool | #DDEBFF (전역 팔레트) | 0.65 | 0 | 0 | #DDEBFF / 2 | Alpha 1, IOR 1.5 [설정: 행 전체] |
| M_BusInterior_Mint | #8FC9B9 (전역 팔레트) | 0.65 | 0 | 0 | 없음 / 0 | Alpha 1, IOR 1.5 [설정: 행 전체] |
| M_BusInterior_Concrete | #B9B6AE (전역 팔레트) | 0.65 | 0 | 0 | 없음 / 0 | Alpha 1, IOR 1.5 [설정: 행 전체] |

색은 INSTRUCTIONS.md 전역 팔레트, 수치는 측색값이 아닌 [설정]. 텍스처 `T_BusInterior_BaseColor`, `T_BusInterior_Normal`, `T_BusInterior_ORM`, `T_BusInterior_Emission`. ORM R=AO/G=Roughness/B=Metallic [설정]. 현재 블록아웃은 단순 PBR 색, 고유 텍스처 미포함. 반복 재질은 트림·타일, 가상 표시는 별도 UV 아틀라스. 텍셀 밀도는 등급별 위 값, 긴 시설은 고유 한 장으로 펴지 않는다.

## 9. 글자·그래픽
| 위치 | 내용 | 처리 방법 (텍스처 교체 / 가상 디자인) | 글꼴 성격 |
|---|---|---|---|
| 표지·포장·간판·화면(해당 시) | BLUE COAST 가상 브랜드, 정류장·버스 번호는 FACTS 목록 | 실제 로고·상표·앱·캐릭터 조형물 복제 금지, 데칼 교체 | 단순 산세리프·픽토그램 |
| 숫자·정보(해당 시) | 확인된 노선·정류장·시간만 사용 | 모르는 주소·번호·가격 생성 금지 | 읽기 쉬운 고딕 |

## 10. 움직임
| 부품 | 움직임 | 원점(회전 중심) 좌표 | 축 | 범위 | 속도·식 |
|---|---|---|---|---|---|
| StrapPivot | X/Y 변환 | PARTS의 pivot·location | X/Y | ±8° [설정] | sin(2πt/1.5) [설정] |
| StopBell | Y 변환 | PARTS의 pivot·location | Y | −.004 m [설정] | 4 frames 누름·복귀 [설정] |
| ValidatorScreen | Emission 변환 | PARTS의 pivot·location | Emission | 기본→수락 [설정] | 12 frames @24fps [설정] |

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
Subject: bus interior modules: card validator, stop bell, strap, seat and pole.
Model-design bounds, not surveyed measurements: X 1.84 m, Y 0.7625 m, Z 2.2 m. Z up, front negative Y; floor-center origin. All unspecified details are fictional artistic settings. Preserve confirmed facts listed in spec.md.
Layout: 4 views in a 2x2 grid — FRONT, RIGHT SIDE, BACK, TOP — all at exactly the same scale, aligned to a faint 1-meter grid, true orthographic projection, no perspective.
Style: stylized miniature diorama, soft bevels, simplified forms, clean dark outlines, flat even lighting, no cast shadows, light gray background.
Include: a 1.7 m human silhouette beside each view for scale; palette swatches: #3A3D42, #8FC9B9, #9DB7E0, #B9B6AE, #C8423B, #DDEBFF, #F7D57A.
Exclude: brand logos, readable commercial signage, copied application screens, watermarks, scenery backgrounds. Use generic brands and original sculpture designs. Written dimensions and executable blockout take precedence over any illustration.
```

images/front.png, right.png, back.png, top.png는 실제 블록아웃의 동일 배율 직교 렌더. 작은 소품은 detail.png에 별도 확대, 실측 근거로 사용하지 않음. 성인 1.70m [설정] 비교용 실루엣은 프리뷰 전용이며 저장 에셋에서 제외. 렌더 투영의 겹침이나 의도된 임시 형상은 최종 메시 품질을 보장하지 않는다.

## 13. 확실하지 않은 값과 필요한 사진
| 값 | 현재 값 | 태그 | 영향도 (상·중·하) | 확정에 필요한 사진 (대상·각도) |
|---|---|---|---|---|
| 실측 외곽·세부 비례 | (1.84, 0.7625, 2.2) m [설정] | [설정] 또는 위 원자료의 [추정] | 상 | 전체 정면·정측면·배면·높은 사선, 성인 또는 규격 기준물과 함께 |
| 재질·그래픽·접합 | 전역 팔레트·가상 디자인 [설정] | [설정] 또는 위 원자료의 [추정] | 중 | 재료 근접·연결부·사용 장면 사진; 실제 로고는 재현하지 않음 |

사진 제공 전에는 위 제작 설정으로 진행하되 [확인]으로 격상하지 않는다. 사진·좌표·실측 제공 시 버전을 올려 보정한다. 사용자 요청에 따라 전체 항목을 일괄 초안 작성하므로 개별 사진 요청으로 작업을 중단하지 않는다.

## 14. 블록아웃 스크립트
- 파일: `blockout.py`, templates/blockout_template.py에서 에셋 정보·재질·부품만 채우고 공용 함수는 동일하게 유지. VERSION과 SPEC_VERSION=v1.0 동기화.
- 외부 검사: `python blockout.py --self-test`.
- Blender 실행: `blender --background --factory-startup --python blockout.py`.
- REPORT 목표 dims_m=1.840x0.762x2.200, 허용 .01m [설정], triangles≤40000 [설정], 바닥 min_z=0 [설정].
- `BusInterior_blockout.blend`와 `BusInterior_blockout.glb`는 초안 정적 형상. 최종 외피·디테일·UV·리그·키프레임·LOD 변형은 명시된 후속 모델링 작업. 변환 Apply, 미터 단위. GLB는 표준 Y-up 저장 후 Blender 재가져오기에서 Z-up 치수 확인.
- 실행·중복·외곽·예산·이름·변환·GLB 검사 결과는 validation.md. 참고 렌더는 실제 GLB 재가져오기 메시로 생성.

## (종류별 추가 섹션)
해당 분류는 키트·캐릭터·음식이 아니므로 추가 섹션 없음.

---

## Changelog
- v1.0 — 2026-11-10 — 설계도·블록아웃·참고 프롬프트·직교 참고 이미지·정적 blend/GLB·검증 기록 최초 작성, 실측 미확정 항목 분리.
