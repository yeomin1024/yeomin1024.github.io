# VERSION: v1.0.0 — 2026-11-11 — 직교 3면 렌더 18장을 한 장의 확인 시트로 묶기 (Pillow)
import os, sys, shutil
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
tiles = os.path.join(HERE, "previews", "_tiles")
rows = [("BusStdRoot", "일반버스"), ("BusExpressRoot", "급행버스"), ("BusVillageRoot", "마을버스"),
        ("KTXRoot", "KTX"), ("BeachTrainRoot", "해변열차"), ("SkyCapsuleRoot", "스카이캡슐")]
cols = [("front", "정면 (-Y)"), ("side", "오른쪽 (+X)"), ("top", "윗면 (+Z)")]
f = lambda s, b=False: ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-" + ("Bold" if b else "Regular") + ".ttc", s, index=1)
TW, TH, LW, HH = 480, 300, 170, 50
sheet = Image.new("RGB", (LW + TW * 3, HH + TH * len(rows)), (245, 246, 248))
d = ImageDraw.Draw(sheet)
for j, (_, t) in enumerate(cols):
    d.text((LW + j * TW + TW / 2, HH / 2), t, font=f(22, True), fill=(30, 30, 40), anchor="mm")
for i, (r, name) in enumerate(rows):
    d.text((LW / 2, HH + i * TH + TH / 2), name, font=f(24, True), fill=(30, 30, 40), anchor="mm")
    for j, (v, _) in enumerate(cols):
        sheet.paste(Image.open(os.path.join(tiles, f"{r}_{v}.png")).convert("RGB"), (LW + j * TW, HH + i * TH))
d.text((8, HH / 2), "정면 칸 가로 1.9 m · 옆·윗면 칸 가로 3.2 m", font=f(13), fill=(90, 90, 100), anchor="lm")
sheet.save(os.path.join(HERE, "previews", "sheet.png"))
if "--keep-tiles" not in sys.argv:
    shutil.rmtree(tiles)
print("sheet", sheet.size)
