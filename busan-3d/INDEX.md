# 부산 3D 에셋 초안 라이브러리

> **2026-11-10 방식 변경 (v2.0.0):** 이 목록은 v1(모든 것을 3D로 모델링) 초안이다. v2부터 3D는 지도·지형·단순 소품만 만들고, 관광지·음식·실제 교통수단은 실제 사진, 캐릭터·아이콘은 일러스트로 바뀌었다. 현재 작업 목록은 [REGISTRY.md](REGISTRY.md), 규칙은 [INSTRUCTIONS.md](INSTRUCTIONS.md)를 본다.

2026-11-10 · 전체 61개 초안. 3D 모델 57개와 FX 설정 4개. 모두 완성 모델·실측 확정본 전 단계의 설계·블록아웃이다.

- [전체 검수](REVIEW_2026-11-10.md)
- [진행 레지스트리](REGISTRY.md)
- [확인·추정 원자료](FACTS.md)
- [작업 기록](CHANGELOG.md)

설계도에는 치수·부품·재질·제작 순서·움직임·미확정 값과 사진 요청이 있다. 블록아웃은 Blender에서 실행 가능하며 `.blend`와 `.glb`는 정적 형태. 리그·표정 키·동작 클립은 제작 사양이며 완성 애니메이션 납품이 아니다. FX는 setup.py와 설정 .blend, 노드 참고도를 제공한다.

신규 참고 이미지는 실제 메시의 동일 배율 정면·우측·배면·상면 렌더를 `images/reference.svg`에 모았다. 개별 PNG와 소품 확대 detail.png도 포함. 기존 VEH01·VEH02는 해당 폴더의 참고 이미지와 직교 렌더를 사용한다.

| ID | 이름 | 설계도 | 실행·블록아웃 | 참고도 | 검증 |
|---|---|---|---|---|---|
| VEH01 | KTX 고속열차 (선두차+객차2) | [spec](assets/VEH01_KTXTrain/spec.md) | [blockout.py](assets/VEH01_KTXTrain/blockout.py) | [참고도](assets/VEH01_KTXTrain/images/reference.png) | [검증](assets/VEH01_KTXTrain/validation.md) |
| VEH02 | 부산 시내버스 (일반) | [spec](assets/VEH02_CityBus/spec.md) | [blockout.py](assets/VEH02_CityBus/blockout.py) | [참고도](assets/VEH02_CityBus/images/reference.png) | [검증](assets/VEH02_CityBus/validation.md) |
| VEH03 | 급행 좌석버스 1003 | [spec](assets/VEH03_ExpressBus/spec.md) | [blockout.py](assets/VEH03_ExpressBus/blockout.py) | [참고도](assets/VEH03_ExpressBus/images/reference.svg) | [검증](assets/VEH03_ExpressBus/validation.md) |
| VEH04 | 마을버스 서구2-2 | [spec](assets/VEH04_VillageBus/spec.md) | [blockout.py](assets/VEH04_VillageBus/blockout.py) | [참고도](assets/VEH04_VillageBus/images/reference.svg) | [검증](assets/VEH04_VillageBus/validation.md) |
| VEH05 | 해변열차 | [spec](assets/VEH05_BeachTrain/spec.md) | [blockout.py](assets/VEH05_BeachTrain/blockout.py) | [참고도](assets/VEH05_BeachTrain/images/reference.svg) | [검증](assets/VEH05_BeachTrain/validation.md) |
| VEH06 | 스카이캡슐 + 고가 레일 키트 | [spec](assets/VEH06_SkyCapsule/spec.md) | [blockout.py](assets/VEH06_SkyCapsule/blockout.py) | [참고도](assets/VEH06_SkyCapsule/images/reference.svg) | [검증](assets/VEH06_SkyCapsule/validation.md) |
| VEH07 | 배경 차량 (승용·트럭) | [spec](assets/VEH07_BackgroundCar/spec.md) | [blockout.py](assets/VEH07_BackgroundCar/blockout.py) | [참고도](assets/VEH07_BackgroundCar/images/reference.svg) | [검증](assets/VEH07_BackgroundCar/validation.md) |
| VEH08 | 어선·대형 정박 선박 | [spec](assets/VEH08_Boats/spec.md) | [blockout.py](assets/VEH08_Boats/blockout.py) | [참고도](assets/VEH08_Boats/images/reference.svg) | [검증](assets/VEH08_Boats/validation.md) |
| ENV01 | 부산역 역사 + 광장 + 승강장 | [spec](assets/ENV01_BusanStation/spec.md) | [blockout.py](assets/ENV01_BusanStation/blockout.py) | [참고도](assets/ENV01_BusanStation/images/reference.svg) | [검증](assets/ENV01_BusanStation/validation.md) |
| ENV02 | 감천문화마을 주택 모듈 | [spec](assets/ENV02_GamcheonHouseKit/spec.md) | [blockout.py](assets/ENV02_GamcheonHouseKit/blockout.py) | [참고도](assets/ENV02_GamcheonHouseKit/images/reference.svg) | [검증](assets/ENV02_GamcheonHouseKit/validation.md) |
| ENV03 | 감천 전망대 + 오리지널 조형물 | [spec](assets/ENV03_GamcheonObservatory/spec.md) | [blockout.py](assets/ENV03_GamcheonObservatory/blockout.py) | [참고도](assets/ENV03_GamcheonObservatory/images/reference.svg) | [검증](assets/ENV03_GamcheonObservatory/validation.md) |
| ENV04 | BIFF광장 거리 + 호떡 노점 | [spec](assets/ENV04_BiffSquareStall/spec.md) | [blockout.py](assets/ENV04_BiffSquareStall/blockout.py) | [참고도](assets/ENV04_BiffSquareStall/images/reference.svg) | [검증](assets/ENV04_BiffSquareStall/validation.md) |
| ENV05 | 국제시장·깡통시장 골목 상점 | [spec](assets/ENV05_MarketAlleyKit/spec.md) | [blockout.py](assets/ENV05_MarketAlleyKit/blockout.py) | [참고도](assets/ENV05_MarketAlleyKit/images/reference.svg) | [검증](assets/ENV05_MarketAlleyKit/validation.md) |
| ENV06 | 영도대교 (도개교) | [spec](assets/ENV06_YeongdoBridge/spec.md) | [blockout.py](assets/ENV06_YeongdoBridge/blockout.py) | [참고도](assets/ENV06_YeongdoBridge/images/reference.svg) | [검증](assets/ENV06_YeongdoBridge/validation.md) |
| ENV07 | 흰여울 절벽 마을 + 해안 산책로 + 터널 | [spec](assets/ENV07_HuinnyeoulVillage/spec.md) | [blockout.py](assets/ENV07_HuinnyeoulVillage/blockout.py) | [참고도](assets/ENV07_HuinnyeoulVillage/images/reference.svg) | [검증](assets/ENV07_HuinnyeoulVillage/validation.md) |
| ENV08 | 자갈치시장 건물 + 꼼장어 골목 | [spec](assets/ENV08_JagalchiMarket/spec.md) | [blockout.py](assets/ENV08_JagalchiMarket/blockout.py) | [참고도](assets/ENV08_JagalchiMarket/images/reference.svg) | [검증](assets/ENV08_JagalchiMarket/validation.md) |
| ENV09 | 해운대 해변 + 구남로 + 가상 호텔 | [spec](assets/ENV09_HaeundaeBeach/spec.md) | [blockout.py](assets/ENV09_HaeundaeBeach/blockout.py) | [참고도](assets/ENV09_HaeundaeBeach/images/reference.svg) | [검증](assets/ENV09_HaeundaeBeach/validation.md) |
| ENV10 | 해운대 고층 스카이라인 (엘시티·마린시티) | [spec](assets/ENV10_HaeundaeSkyline/spec.md) | [blockout.py](assets/ENV10_HaeundaeSkyline/blockout.py) | [참고도](assets/ENV10_HaeundaeSkyline/images/reference.svg) | [검증](assets/ENV10_HaeundaeSkyline/validation.md) |
| ENV11 | 해동용궁사 | [spec](assets/ENV11_YonggungsaTemple/spec.md) | [blockout.py](assets/ENV11_YonggungsaTemple/blockout.py) | [참고도](assets/ENV11_YonggungsaTemple/images/reference.svg) | [검증](assets/ENV11_YonggungsaTemple/validation.md) |
| ENV12 | 연화리 포구 + 해녀촌 천막 | [spec](assets/ENV12_YeonhwariHarbor/spec.md) | [blockout.py](assets/ENV12_YeonhwariHarbor/blockout.py) | [참고도](assets/ENV12_YeonhwariHarbor/images/reference.svg) | [검증](assets/ENV12_YeonhwariHarbor/validation.md) |
| ENV13 | 송정정거장 (옛 송정역) | [spec](assets/ENV13_SongjeongStation/spec.md) | [blockout.py](assets/ENV13_SongjeongStation/blockout.py) | [참고도](assets/ENV13_SongjeongStation/images/reference.svg) | [검증](assets/ENV13_SongjeongStation/validation.md) |
| ENV14 | 해안 철로 키트 + 다릿돌전망대 | [spec](assets/ENV14_CoastalRailDaritdol/spec.md) | [blockout.py](assets/ENV14_CoastalRailDaritdol/blockout.py) | [참고도](assets/ENV14_CoastalRailDaritdol/images/reference.svg) | [검증](assets/ENV14_CoastalRailDaritdol/validation.md) |
| ENV15 | 청사포 포구 + 쌍둥이 등대 | [spec](assets/ENV15_CheongsapoLighthouse/spec.md) | [blockout.py](assets/ENV15_CheongsapoLighthouse/blockout.py) | [참고도](assets/ENV15_CheongsapoLighthouse/images/reference.svg) | [검증](assets/ENV15_CheongsapoLighthouse/validation.md) |
| ENV16 | 동백섬 (누리마루·등대·해안 데크) | [spec](assets/ENV16_DongbaekIsland/spec.md) | [blockout.py](assets/ENV16_DongbaekIsland/blockout.py) | [참고도](assets/ENV16_DongbaekIsland/images/reference.svg) | [검증](assets/ENV16_DongbaekIsland/validation.md) |
| ENV17 | 광안대교 | [spec](assets/ENV17_GwanganBridge/spec.md) | [blockout.py](assets/ENV17_GwanganBridge/blockout.py) | [참고도](assets/ENV17_GwanganBridge/images/reference.svg) | [검증](assets/ENV17_GwanganBridge/validation.md) |
| ENV18 | 광안리 해변 + 회센터 건물 | [spec](assets/ENV18_GwangalliMillak/spec.md) | [blockout.py](assets/ENV18_GwangalliMillak/blockout.py) | [참고도](assets/ENV18_GwangalliMillak/images/reference.svg) | [검증](assets/ENV18_GwangalliMillak/validation.md) |
| ENV19 | 드론 라이트쇼 (드론 1기 + 편대 배치) | [spec](assets/ENV19_DroneShow/spec.md) | [blockout.py](assets/ENV19_DroneShow/blockout.py) | [참고도](assets/ENV19_DroneShow/images/reference.svg) | [검증](assets/ENV19_DroneShow/validation.md) |
| ENV20 | 오륙도 + 스카이워크 + 해맞이공원 | [spec](assets/ENV20_OryukdoSkywalk/spec.md) | [blockout.py](assets/ENV20_OryukdoSkywalk/blockout.py) | [참고도](assets/ENV20_OryukdoSkywalk/images/reference.svg) | [검증](assets/ENV20_OryukdoSkywalk/validation.md) |
| ENV21 | 이기대 해안 데크·계단·구름다리 | [spec](assets/ENV21_IgidaeTrailKit/spec.md) | [blockout.py](assets/ENV21_IgidaeTrailKit/blockout.py) | [참고도](assets/ENV21_IgidaeTrailKit/images/reference.svg) | [검증](assets/ENV21_IgidaeTrailKit/validation.md) |
| ENV22 | 차이나타운 거리 (가상 간판) | [spec](assets/ENV22_Chinatown/spec.md) | [blockout.py](assets/ENV22_Chinatown/blockout.py) | [참고도](assets/ENV22_Chinatown/images/reference.svg) | [검증](assets/ENV22_Chinatown/validation.md) |
| ENV23 | 장면 전환용 부산 3D 지도 + 루트 + 핀 | [spec](assets/ENV23_BusanMap3D/spec.md) | [blockout.py](assets/ENV23_BusanMap3D/blockout.py) | [참고도](assets/ENV23_BusanMap3D/images/reference.svg) | [검증](assets/ENV23_BusanMap3D/validation.md) |
| SF01 | 버스정류장 (쉘터·도착 안내 전광판·정류장명 판) | [spec](assets/SF01_BusStop/spec.md) | [blockout.py](assets/SF01_BusStop/blockout.py) | [참고도](assets/SF01_BusStop/images/reference.svg) | [검증](assets/SF01_BusStop/validation.md) |
| SF02 | 버스 실내 (교통카드 단말기·하차벨·손잡이·좌석) | [spec](assets/SF02_BusInterior/spec.md) | [blockout.py](assets/SF02_BusInterior/blockout.py) | [참고도](assets/SF02_BusInterior/images/reference.svg) | [검증](assets/SF02_BusInterior/validation.md) |
| SF03 | 가로등·벤치·볼라드·해변 난간·쓰레기통 | [spec](assets/SF03_StreetFurnitureKit/spec.md) | [blockout.py](assets/SF03_StreetFurnitureKit/blockout.py) | [참고도](assets/SF03_StreetFurnitureKit/images/reference.svg) | [검증](assets/SF03_StreetFurnitureKit/validation.md) |
| SF04 | 짐 배송 카운터 (가상 브랜드) | [spec](assets/SF04_LuggageCounter/spec.md) | [blockout.py](assets/SF04_LuggageCounter/blockout.py) | [참고도](assets/SF04_LuggageCounter/images/reference.svg) | [검증](assets/SF04_LuggageCounter/validation.md) |
| CHR01 | 여행자 A (1.70 m) | [spec](assets/CHR01_TravelerA/spec.md) | [blockout.py](assets/CHR01_TravelerA/blockout.py) | [참고도](assets/CHR01_TravelerA/images/reference.svg) | [검증](assets/CHR01_TravelerA/validation.md) |
| CHR02 | 여행자 B (1.62 m) | [spec](assets/CHR02_TravelerB/spec.md) | [blockout.py](assets/CHR02_TravelerB/blockout.py) | [참고도](assets/CHR02_TravelerB/images/reference.svg) | [검증](assets/CHR02_TravelerB/validation.md) |
| CHR03 | 행인·관광객 군중 | [spec](assets/CHR03_Crowd/spec.md) | [blockout.py](assets/CHR03_Crowd/blockout.py) | [참고도](assets/CHR03_Crowd/images/reference.svg) | [검증](assets/CHR03_Crowd/validation.md) |
| CHR04 | 갈매기 | [spec](assets/CHR04_Seagull/spec.md) | [blockout.py](assets/CHR04_Seagull/blockout.py) | [참고도](assets/CHR04_Seagull/images/reference.svg) | [검증](assets/CHR04_Seagull/validation.md) |
| PRP01 | 캐리어 + 배송 태그 | [spec](assets/PRP01_Suitcase/spec.md) | [blockout.py](assets/PRP01_Suitcase/blockout.py) | [참고도](assets/PRP01_Suitcase/images/reference.svg) | [검증](assets/PRP01_Suitcase/validation.md) |
| PRP02 | 백팩·크로스백 | [spec](assets/PRP02_Bags/spec.md) | [blockout.py](assets/PRP02_Bags/blockout.py) | [참고도](assets/PRP02_Bags/images/reference.svg) | [검증](assets/PRP02_Bags/validation.md) |
| PRP03 | 스마트폰 (가상 지도 앱 화면) | [spec](assets/PRP03_Smartphone/spec.md) | [blockout.py](assets/PRP03_Smartphone/blockout.py) | [참고도](assets/PRP03_Smartphone/images/reference.svg) | [검증](assets/PRP03_Smartphone/validation.md) |
| PRP04 | 교통카드 | [spec](assets/PRP04_TransitCard/spec.md) | [blockout.py](assets/PRP04_TransitCard/blockout.py) | [참고도](assets/PRP04_TransitCard/images/reference.svg) | [검증](assets/PRP04_TransitCard/validation.md) |
| PRP05 | 감천 스탬프 지도 | [spec](assets/PRP05_StampMap/spec.md) | [blockout.py](assets/PRP05_StampMap/blockout.py) | [참고도](assets/PRP05_StampMap/images/reference.svg) | [검증](assets/PRP05_StampMap/validation.md) |
| PRP06 | 카메라 | [spec](assets/PRP06_Camera/spec.md) | [blockout.py](assets/PRP06_Camera/blockout.py) | [참고도](assets/PRP06_Camera/images/reference.svg) | [검증](assets/PRP06_Camera/validation.md) |
| PRP07 | 스카이워크 덧신 | [spec](assets/PRP07_ShoeCovers/spec.md) | [blockout.py](assets/PRP07_ShoeCovers/blockout.py) | [참고도](assets/PRP07_ShoeCovers/images/reference.svg) | [검증](assets/PRP07_ShoeCovers/validation.md) |
| FOOD01 | 밀면 + 왕만두 | [spec](assets/FOOD01_Milmyeon/spec.md) | [blockout.py](assets/FOOD01_Milmyeon/blockout.py) | [참고도](assets/FOOD01_Milmyeon/images/reference.svg) | [검증](assets/FOOD01_Milmyeon/validation.md) |
| FOOD02 | 씨앗호떡 (종이컵) | [spec](assets/FOOD02_SeedHotteok/spec.md) | [blockout.py](assets/FOOD02_SeedHotteok/blockout.py) | [참고도](assets/FOOD02_SeedHotteok/images/reference.svg) | [검증](assets/FOOD02_SeedHotteok/validation.md) |
| FOOD03 | 유부비빔당면 | [spec](assets/FOOD03_YubuGlassNoodle/spec.md) | [blockout.py](assets/FOOD03_YubuGlassNoodle/blockout.py) | [참고도](assets/FOOD03_YubuGlassNoodle/images/reference.svg) | [검증](assets/FOOD03_YubuGlassNoodle/validation.md) |
| FOOD04 | 꼼장어 반반 + 불판 | [spec](assets/FOOD04_Gomjangeo/spec.md) | [blockout.py](assets/FOOD04_Gomjangeo/blockout.py) | [참고도](assets/FOOD04_Gomjangeo/images/reference.svg) | [검증](assets/FOOD04_Gomjangeo/validation.md) |
| FOOD05 | 복국 | [spec](assets/FOOD05_Bokguk/spec.md) | [blockout.py](assets/FOOD05_Bokguk/blockout.py) | [참고도](assets/FOOD05_Bokguk/images/reference.svg) | [검증](assets/FOOD05_Bokguk/validation.md) |
| FOOD06 | 전복죽 + 해물모둠 | [spec](assets/FOOD06_AbaloneJukSeafood/spec.md) | [blockout.py](assets/FOOD06_AbaloneJukSeafood/blockout.py) | [참고도](assets/FOOD06_AbaloneJukSeafood/images/reference.svg) | [검증](assets/FOOD06_AbaloneJukSeafood/validation.md) |
| FOOD07 | 방어회 상차림 | [spec](assets/FOOD07_BangeoSashimi/spec.md) | [blockout.py](assets/FOOD07_BangeoSashimi/blockout.py) | [참고도](assets/FOOD07_BangeoSashimi/images/reference.svg) | [검증](assets/FOOD07_BangeoSashimi/validation.md) |
| FOOD08 | 대구탕 | [spec](assets/FOOD08_Daegutang/spec.md) | [blockout.py](assets/FOOD08_Daegutang/blockout.py) | [참고도](assets/FOOD08_Daegutang/images/reference.svg) | [검증](assets/FOOD08_Daegutang/validation.md) |
| FOOD09 | 돼지국밥 상차림 | [spec](assets/FOOD09_DwaejiGukbap/spec.md) | [blockout.py](assets/FOOD09_DwaejiGukbap/blockout.py) | [참고도](assets/FOOD09_DwaejiGukbap/images/reference.svg) | [검증](assets/FOOD09_DwaejiGukbap/validation.md) |
| FOOD10 | 고기만두 포장·어묵 | [spec](assets/FOOD10_DumplingFishcake/spec.md) | [blockout.py](assets/FOOD10_DumplingFishcake/blockout.py) | [참고도](assets/FOOD10_DumplingFishcake/images/reference.svg) | [검증](assets/FOOD10_DumplingFishcake/validation.md) |
| FOOD11 | 커피잔 | [spec](assets/FOOD11_Coffee/spec.md) | [blockout.py](assets/FOOD11_Coffee/blockout.py) | [참고도](assets/FOOD11_Coffee/images/reference.svg) | [검증](assets/FOOD11_Coffee/validation.md) |
| FX01 | 바다·파도 셰이더 | [spec](assets/FX01_SeaShader/spec.md) | [setup.py](assets/FX01_SeaShader/setup.py) | [참고도](assets/FX01_SeaShader/images/reference.svg) | [검증](assets/FX01_SeaShader/validation.md) |
| FX02 | 시간대 조명 프리셋 (아침·정오·일몰·밤) | [spec](assets/FX02_LightingPresets/spec.md) | [setup.py](assets/FX02_LightingPresets/setup.py) | [참고도](assets/FX02_LightingPresets/images/reference.svg) | [검증](assets/FX02_LightingPresets/validation.md) |
| FX03 | 김·연기 | [spec](assets/FX03_SteamSmoke/spec.md) | [setup.py](assets/FX03_SteamSmoke/setup.py) | [참고도](assets/FX03_SteamSmoke/images/reference.svg) | [검증](assets/FX03_SteamSmoke/validation.md) |
| FX04 | 자막·정보 카드 (시간·버스 번호·정류장) | [spec](assets/FX04_InfoCards/spec.md) | [setup.py](assets/FX04_InfoCards/setup.py) | [참고도](assets/FX04_InfoCards/images/reference.svg) | [검증](assets/FX04_InfoCards/validation.md) |

지도 핀은 ENV23/pins.json에 사용자 좌표가 들어오기 전까지 비어 있다. 실제 해안선·고도 데이터가 없는 중립 지도판을 부산 실측 지도라고 표시하지 않는다. 다른 모든 미확정 실측도 각 설계도의 사진 요구사항으로 남겨 두었다.
