#!/usr/bin/env python3
# Контактные листы: 20 кадров с таймкодами на каждое видео (5x4)
import os, subprocess, sys, json
from PIL import Image, ImageDraw, ImageFont

MEDIA = "/Users/aleksandrnarodetskii/Downloads/hand-marketing-react/media"
SCRATCH = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SCRATCH, "sheets")
TMP = os.path.join(SCRATCH, "frames_tmp")
os.makedirs(OUT, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

FONT = ImageFont.truetype("/Users/aleksandrnarodetskii/Downloads/hand-marketing-react/scripts/fonts/Montserrat.ttf", 22)

VIDEOS = [
    "hm-showreel.mp4", "stavropol-3dmapping.mp4", "stavropol-vdnh-nakedeye.mp4",
    "stavropol-vdnh-main.mp4", "samara-vdnh-30.mp4", "samara-vdnh-history.mp4",
    "samara-vdnh-1.mp4", "samara-vdnh-2.mp4", "samara-vdnh-3.mp4", "samara-vdnh-8.mp4",
    "samara-pres-content.mp4", "content-mapping-curved.mp4", "content-infopanels.mp4",
    "content-mapping-arch.mp4", "content-graphics.mp4", "gazelle-transformer.mp4",
    "changan.mp4", "samsung-2020.mp4", "salaris-2.mp4", "salaris-event-fin180416.mp4",
    "marie-claire-event.mp4", "event-riviera.mp4", "lingerie.mp4", "mozaika.mp4",
    "interplastika.mp4", "izotek-brand-video.mp4", "mmg-paveleckaya.mp4",
    "technopark-zubovo.mp4", "transrzhd.mp4", "vivax-samburskaya.mp4",
    "eaton-almaty.mp4", "pt-film-short.mp4", "bekabad-hd.mp4", "eaton-yaz.mp4",
    "samara-vdnh-4.mp4", "samara-vdnh-5.mp4", "samara-vdnh-6.mp4", "samara-vdnh-7.mp4",
    "samara-pres-5spirits.mp4",
]

COLS, ROWS = 5, 4
TW, TH = 384, 216

def duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", path], capture_output=True, text=True)
    return float(r.stdout.strip())

for vid in VIDEOS:
    path = os.path.join(MEDIA, vid)
    if not os.path.exists(path):
        print("SKIP missing", vid); continue
    name = os.path.splitext(vid)[0]
    out_sheet = os.path.join(OUT, name + ".jpg")
    if os.path.exists(out_sheet):
        continue
    dur = duration(path)
    n = COLS * ROWS
    # кадры равномерно, с отступом от краёв
    stamps = [dur * (i + 0.5) / n for i in range(n)]
    sheet = Image.new("RGB", (COLS * TW, ROWS * TH + 40), (10, 10, 10))
    d = ImageDraw.Draw(sheet)
    d.text((10, 6), name, font=FONT, fill=(255, 255, 100))
    for i, ts in enumerate(stamps):
        fp = os.path.join(TMP, f"f{i}.jpg")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{ts:.2f}", "-i", path,
                        "-frames:v", "1", "-vf", f"scale={TW}:{TH}:force_original_aspect_ratio=decrease,pad={TW}:{TH}:(ow-iw)/2:(oh-ih)/2",
                        fp], capture_output=True)
        try:
            img = Image.open(fp)
        except Exception:
            continue
        x, y = (i % COLS) * TW, 40 + (i // COLS) * TH
        sheet.paste(img, (x, y))
        label = f"{int(ts//60)}:{ts%60:04.1f}"
        d.rectangle([x, y, x + 92, y + 28], fill=(0, 0, 0))
        d.text((x + 6, y + 2), label, font=FONT, fill=(0, 255, 180))
    sheet.save(out_sheet, quality=82)
    print("OK", name)
print("DONE")
