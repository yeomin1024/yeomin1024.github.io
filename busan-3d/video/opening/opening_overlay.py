# VERSION: v1.0.0 — 2026-11-10 — 오프닝 2D 글자·정보 패널·사진 자리·출처를 얹고 mp4 로 묶기
"""
실행:
  python opening_overlay.py --frames <opening_blender.py 출력 폴더> --comp <합성 프레임 폴더> --out opening_v1.mp4 [--only 40,110]
필요: Pillow, ffmpeg, Noto Sans CJK 글꼴(/usr/share/fonts/opentype/noto/NotoSansCJK-*.ttc)

- 모든 문구는 timeline.json 에서 읽는다(FACTS.md 1장과 같은 내용).
- 실제 사진은 아직 없으므로 사진 자리에는 "실제 사진 자리" 틀만 그린다. 사진을 만들어 넣지 않는다.
"""
import json
import logging
import os
import subprocess
import sys
import time

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
TL = json.load(open(os.path.join(HERE, "timeline.json"), encoding="utf-8"))
W, H = TL["resolution"]
FONT_DIR = "/usr/share/fonts/opentype/noto"
KR = 1   # .ttc 안의 Noto Sans CJK KR 번호

log_ = logging.getLogger("overlay")


def log(stage, level=logging.INFO, **kv):
    log_.log(level, "[%s] [%s] %s", stage, time.strftime("%Y-%m-%dT%H:%M:%S"), " ".join(f"{k}={v}" for k, v in kv.items()))


_fonts = {}


def font(size, bold=False):
    key = (size, bold)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(os.path.join(FONT_DIR, "NotoSansCJK-Bold.ttc" if bold else "NotoSansCJK-Regular.ttc"), size, index=KR)
    return _fonts[key]


def rgb(h, a=255):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def fade(f, start, end, n=8):
    """구간 안에서 0→1→0 로 서서히 나타나고 사라지는 값."""
    if f < start or f > end:
        return 0.0
    return max(0.0, min(1.0, (f - start + 1) / n, (end - f + 1) / n))


def text(d, xy, s, fnt, fill, anchor="la"):
    d.text(xy, s, font=fnt, fill=fill, anchor=anchor)


def draw_title(d, f):
    t = TL["title"]
    a = fade(f, t["start"], t["end"], 12)
    if not a:
        return
    k = int(255 * a)
    d.rectangle((0, H * 0.34, W, H * 0.66), fill=(18, 26, 51, int(150 * a)))
    text(d, (W / 2, H * 0.47), t["text"], font(64, True), (255, 255, 255, k), "mm")
    text(d, (W / 2, H * 0.57), t["sub"], font(26), (242, 239, 230, k), "mm")


def draw_day(d, f):
    c = TL["day_card"]
    a = fade(f, c["start"], c["end"], 8)
    if not a:
        return
    k = int(255 * a)
    fnt = font(28, True)
    x0, y0 = 40, 36
    tw = d.textbbox((0, 0), c["text"], font=fnt)[2]
    d.rounded_rectangle((x0, y0, x0 + tw + 40, y0 + 52), radius=26, fill=rgb(c["color"], int(235 * a)))
    text(d, (x0 + 20, y0 + 26), c["text"], fnt, (255, 255, 255, k), "lm")


def draw_panel(d, f):
    for p in TL["panels"]:
        a = fade(f, p["start"], p["end"], 8)
        if not a:
            continue
        k = int(255 * a)
        x0, y1 = 40, H - 40
        lines = [(p["time"], font(40, True), rgb("#F28C5B", k)), (p["title"], font(28, True), (255, 255, 255, k)),
                 (p["sub"], font(20), (225, 230, 240, k))]
        if p.get("note"):
            lines.append((p["note"], font(16), (170, 180, 200, k)))
        widths = [d.textbbox((0, 0), s, font=fn)[2] for s, fn, _ in lines]
        heights = [52, 40, 30, 26][:len(lines)]
        bw, bh = max(widths) + 48, sum(heights) + 28
        d.rounded_rectangle((x0, y1 - bh, x0 + bw, y1), radius=18, fill=(18, 26, 51, int(210 * a)))
        y = y1 - bh + 14
        for (s, fn, col), hgt in zip(lines, heights):
            text(d, (x0 + 24, y), s, fn, col)
            y += hgt


def dashed_rect(d, box, col, dash=14, gap=9, width=3):
    x0, y0, x1, y1 = box
    for (ax, ay, bx, by) in ((x0, y0, x1, y0), (x1, y0, x1, y1), (x1, y1, x0, y1), (x0, y1, x0, y0)):
        length = ((bx - ax) ** 2 + (by - ay) ** 2) ** 0.5
        n = int(length // (dash + gap)) + 1
        for i in range(n):
            s = i * (dash + gap) / length
            e = min(1.0, (i * (dash + gap) + dash) / length)
            d.line((ax + (bx - ax) * s, ay + (by - ay) * s, ax + (bx - ax) * e, ay + (by - ay) * e), fill=col, width=width)


def draw_placeholder(d, f):
    for p in TL["photo_placeholders"]:
        a = fade(f, p["start"], p["end"], 8)
        if not a:
            continue
        k = int(255 * a)
        bw, bh = 400, 225
        x1, y0 = W - 40, 110
        box = (x1 - bw, y0, x1, y0 + bh)
        d.rectangle(box, fill=(18, 26, 51, int(150 * a)))
        dashed_rect(d, box, (242, 239, 230, k))
        cx = x1 - bw / 2
        text(d, (cx, y0 + 70), "실제 사진 자리", font(28, True), (255, 255, 255, k), "mm")
        text(d, (cx, y0 + 115), f"{p['id']} {p['name']}", font(24), (242, 239, 230, k), "mm")
        text(d, (cx, y0 + 160), "사용권이 확인된 실제 사진으로 교체 예정", font(17), (190, 198, 215, k), "mm")


def draw_labels(d, f, pts):
    row = pts.get(str(f))
    if not row:
        return
    for l in TL["labels"]:
        a = fade(f, l["start"], l["end"], 8)
        x, y, z = row.get(l["place"], (0, 0, -1))
        if not a or z <= 0 or not (0 <= x <= W and 0 <= y <= H):
            continue
        k = int(255 * a)
        fnt = font(20, True)
        tw = d.textbbox((0, 0), l["text"], font=fnt)[2]
        bx0, by0 = x - tw / 2 - 12, y - 46
        d.line((x, y - 10, x, by0 + 32), fill=(242, 239, 230, k), width=2)
        d.rounded_rectangle((bx0, by0, bx0 + tw + 24, by0 + 32), radius=16, fill=(18, 26, 51, int(220 * a)))
        text(d, (x, by0 + 16), l["text"], fnt, (255, 255, 255, k), "mm")
    b = TL["bus_token"]
    a = fade(f, b["start"], b["end"], 8)
    x, y, z = row.get("bus", (0, 0, -1))
    if a and z > 0 and 0 <= x <= W and 0 <= y <= H:
        k = int(255 * a)
        fnt = font(18, True)
        tw = d.textbbox((0, 0), b["label"], font=fnt)[2]
        d.rounded_rectangle((x - tw / 2 - 10, y - 40, x + tw / 2 + 10, y - 12), radius=14, fill=rgb(b["color"], int(235 * a)))
        text(d, (x, y - 26), b["label"], fnt, (255, 255, 255, k), "mm")


def draw_credits(d, f):
    c = TL["credits"]
    a = fade(f, c["start"], c["end"] + 8, 10)
    if not a:
        return
    k = int(255 * a)
    d.rectangle((0, 0, W, H), fill=(18, 26, 51, int(225 * a)))
    text(d, (W / 2, 220), "자료 출처", font(30, True), (255, 255, 255, k), "mm")
    y = 290
    for line in c["lines"]:
        text(d, (W / 2, y), line, font(15), (225, 230, 240, k), "mm")
        y += 34


def draw_tag(d, f):
    s = TL["draft_tag"]
    fnt = font(14)
    tw = d.textbbox((0, 0), s, font=fnt)[2]
    d.rounded_rectangle((W - tw - 40, 20, W - 16, 46), radius=13, fill=(18, 26, 51, 170))
    text(d, (W - 28, 33), s, fnt, (230, 230, 230, 255), "rm")


def compose(base_path, f, pts):
    im = Image.open(base_path).convert("RGBA")
    if im.size != (W, H):
        im = im.resize((W, H), Image.LANCZOS)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for fn in (draw_labels, draw_panel, draw_placeholder, draw_day, draw_title, draw_tag):
        fn(d, f, pts) if fn is draw_labels else fn(d, f)
    out = Image.alpha_composite(im, ov)
    cr = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_credits(ImageDraw.Draw(cr), f)
    return Image.alpha_composite(out, cr).convert("RGB")


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s", stream=sys.stdout)
    a = sys.argv[1:]
    get = lambda k, dflt=None: a[a.index(k) + 1] if k in a else dflt
    frames_dir, comp_dir, out = get("--frames"), get("--comp"), get("--out")
    only = [int(x) for x in get("--only", "").split(",") if x]
    os.makedirs(comp_dir, exist_ok=True)
    pts = json.load(open(os.path.join(frames_dir, "screen_points.json"), encoding="utf-8"))
    todo = only or list(range(TL["frame_start"], TL["frame_end"] + 1))
    missing = [f for f in todo if not os.path.exists(os.path.join(frames_dir, f"frame_{f:04d}.png"))]
    if missing:
        log("CHECK", logging.ERROR, missing_frames=len(missing), first=missing[0], next_step="opening_blender.py 렌더가 끝났는지 확인")
        sys.exit(1)
    t = time.time()
    for f in todo:
        compose(os.path.join(frames_dir, f"frame_{f:04d}.png"), f, pts).save(os.path.join(comp_dir, f"frame_{f:04d}.png"))
    log("COMPOSE", frames=len(todo), seconds=f"{time.time() - t:.1f}")
    if only or not out:
        return
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(TL["fps"]), "-start_number", str(TL["frame_start"]),
           "-i", os.path.join(comp_dir, "frame_%04d.png"), "-c:v", "libx264", "-preset", "medium", "-crf", "20",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        log("ENCODE", logging.ERROR, error=r.stderr.strip()[:300], next_step="ffmpeg 설치·경로 확인")
        sys.exit(1)
    log("ENCODE", out=out, size_MB=f"{os.path.getsize(out) / 1e6:.2f}", seconds=f"{len(todo) / TL['fps']:.1f}")


if __name__ == "__main__":
    main()

# CHANGELOG
# v1.0.0 — 2026-11-10 — 최초 작성
