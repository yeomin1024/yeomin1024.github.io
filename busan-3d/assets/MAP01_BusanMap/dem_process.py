# VERSION: v1.0.0 — 2026-11-10 — Copernicus DEM GLO-30 타일 2장으로 MAP01 높이 이미지 생성
"""
MAP01 높이 이미지 만들기

사용법:
  python dem_process.py <N35_E128 타일.tif> <N35_E129 타일.tif> <출력 폴더>
  타일 내려받기 (공개, 무료):
    https://copernicus-dem-30m.s3.amazonaws.com/Copernicus_DSM_COG_10_N35_00_E128_00_DEM/Copernicus_DSM_COG_10_N35_00_E128_00_DEM.tif
    https://copernicus-dem-30m.s3.amazonaws.com/Copernicus_DSM_COG_10_N35_00_E129_00_DEM/Copernicus_DSM_COG_10_N35_00_E129_00_DEM.tif
  필요 패키지: numpy, tifffile, imagecodecs, pillow

처리 (모두 기록한다):
  1. 두 타일을 이어 붙이고 지도 범위(남 35.05, 서 128.98, 북 35.25, 동 129.26)만 자른다.
  2. 0 m 아래 값(해안 오차, 최소 약 -12.6 m)은 0 m 로 바꾼다.
  3. 0 ~ MAX_ELEV_M 를 0 ~ 65535 로 바꿔 16비트 흑백 PNG 로 저장한다 (위쪽 = 북쪽).
  건물 제거·평활화 같은 다른 가공은 하지 않는다 (확인 결과 건물 돌출 없음).
"""
import json
import logging
import sys
import time

import numpy as np
import tifffile
from PIL import Image

SOUTH, WEST, NORTH, EAST = 35.05, 128.98, 35.25, 129.26
STEP = 1.0 / 3600.0            # 1초 간격 (약 30 m)
MAX_ELEV_M = 640.0             # 16비트 값 65535 에 해당하는 높이
OUT_NAME = "dem_busan_cop30"
NOTICE = ("produced using Copernicus WorldDEM-30 © DLR e.V. 2010-2014 and © Airbus Defence and Space GmbH "
          "2014-2018 provided under COPERNICUS by the European Union and ESA; all rights reserved")
LIABILITY = ("The organisations in charge of the Copernicus programme by law or by delegation do not incur any "
             "liability for any use of the Copernicus WorldDEM-30")

log = logging.getLogger("dem")


def stage(name, **kv):
    log.info("[%s] [%s] %s", name, time.strftime("%Y-%m-%dT%H:%M:%S"), " ".join(f"{k}={v}" for k, v in kv.items()))


def read_tile(path, lon0):
    with tifffile.TiffFile(path) as t:
        p = t.pages[0]
        scale = p.tags["ModelPixelScaleTag"].value
        tie = p.tags["ModelTiepointTag"].value
        arr = p.asarray().astype(np.float32)
    if abs(scale[0] - STEP) > 1e-12 or abs(tie[3] - lon0) > 1e-9 or abs(tie[4] - 36.0) > 1e-9:
        raise ValueError(f"예상과 다른 타일 좌표: {path} scale={scale} tie={tie}")
    stage("LOAD", file=path.split("/")[-1], shape=arr.shape, min=f"{arr.min():.1f}", max=f"{arr.max():.1f}")
    return arr


def main(t128, t129, out_dir):
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s", stream=sys.stdout)
    a = read_tile(t128, 128.0)
    b = read_tile(t129, 129.0)
    r0, r1 = round((36.0 - NORTH) / STEP), round((36.0 - SOUTH) / STEP)
    c0, c1 = round((WEST - 128.0) / STEP), round((EAST - 129.0) / STEP)
    dem = np.hstack([a[r0:r1 + 1, c0:], b[r0:r1 + 1, :c1 + 1]])
    stage("CROP", rows=f"{r0}-{r1}", shape=dem.shape, bounds=f"{SOUTH},{WEST},{NORTH},{EAST}")
    neg = int((dem < 0).sum())
    dem = np.clip(dem, 0.0, None)
    top = float(dem.max())
    if top > MAX_ELEV_M:
        raise ValueError(f"최고 높이 {top:.1f} m 가 MAX_ELEV_M {MAX_ELEV_M} 보다 큼 → MAX_ELEV_M 를 올릴 것")
    sea = float((dem == 0).mean())
    stage("CLEAN", negative_to_zero=neg, max_m=f"{top:.1f}", sea_fraction=f"{sea:.3f}")
    u16 = np.round(dem / MAX_ELEV_M * 65535.0).astype(np.uint16)
    png = f"{out_dir}/{OUT_NAME}.png"
    Image.fromarray(u16).save(png)
    meta = {
        "file": f"{OUT_NAME}.png", "bounds_s_w_n_e": [SOUTH, WEST, NORTH, EAST], "pixel_deg": STEP,
        "size_px": [int(dem.shape[1]), int(dem.shape[0])], "value_65535_m": MAX_ELEV_M, "max_m": round(top, 1),
        "negative_pixels_set_to_0": neg, "sea_fraction": round(sea, 3),
        "source": "Copernicus DEM GLO-30 (WorldDEM-30), tiles N35_00_E128_00 & N35_00_E129_00",
        "source_urls": [
            "https://copernicus-dem-30m.s3.amazonaws.com/Copernicus_DSM_COG_10_N35_00_E128_00_DEM/Copernicus_DSM_COG_10_N35_00_E128_00_DEM.tif",
            "https://copernicus-dem-30m.s3.amazonaws.com/Copernicus_DSM_COG_10_N35_00_E129_00_DEM/Copernicus_DSM_COG_10_N35_00_E129_00_DEM.tif"],
        "processing": ["mosaic + crop to bounds", "values < 0 m set to 0 m", f"0..{MAX_ELEV_M} m scaled to 16-bit PNG (north up)"],
        "notice_modified": NOTICE, "liability_sentence": LIABILITY,
        "pixel_registration_note": "타일 좌표를 화소 중심 기준으로 처리. 기준 차이가 있어도 최대 반 화소(약 15 m) 이내",
    }
    with open(f"{out_dir}/{OUT_NAME}.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    stage("SAVE", png=png, size=f"{dem.shape[1]}x{dem.shape[0]}", max_m=f"{top:.1f}")
    return meta


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])

# CHANGELOG
# v1.0.0 — 2026-11-10 — 최초 작성
