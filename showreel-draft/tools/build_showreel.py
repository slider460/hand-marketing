#!/usr/bin/env python3
# Сборка 2-минутного шоурила Hand Marketing
# Все склейки привязаны к сетке битов трека (BPM ~70.8, бит ~0.8475с)
import json, os, subprocess, sys

SC = os.path.dirname(os.path.abspath(__file__))
MEDIA = "/Users/aleksandrnarodetskii/Downloads/hand-marketing-react/media"
SEG = os.path.join(SC, "segs")
os.makedirs(SEG, exist_ok=True)
FPS = 25

a = json.load(open(os.path.join(SC, "audio/analysis.json")))
beats = a["beats"]
PERIOD = (beats[-1] - beats[0]) / (len(beats) - 1)
B0 = beats[0]
def beat_t(i): return B0 + i * PERIOD

INTRO_BEATS = 9           # заставка-анимация сборки куба: 0 → beat 9 (~8.21s)
OUTRO_END = 123.5         # конец ролика

# EDL: (файл, старт в источнике, длина в битах)
EDL = [
    # ── Секция 1 · УДАР (открытие) ──
    ("content-mapping-arch.mp4",      1.5,  2),   # неоновый контур здания
    ("content-mapping-arch.mp4",      4.0,  2),   # глитч-пиксели по фасаду
    ("samara-vdnh-8.mp4",            49.8,  3),   # ракета над Землёй на экране
    ("stavropol-vdnh-nakedeye.mp4", 126.6,  2),   # naked-eye 3D куб
    ("gazelle-transformer.mp4",      33.0,  2),   # трансформация ГАЗели
    # ── Секция 2 · ИВЕНТЫ ──
    ("samsung-2020.mp4",             31.6,  2),   # красная сетка-мэппинг в зале
    ("samsung-2020.mp4",             38.8,  2),   # барабанщики на сцене Samsung
    ("event-riviera.mp4",           164.8,  2),   # барабан + луч света
    ("event-riviera.mp4",           174.8,  2),   # драмлайн
    ("changan.mp4",                  57.8,  2),   # барабанщицы в зелёном свете
    ("changan.mp4",                  73.9,  2),   # проекция на автомобиль
    ("lingerie.mp4",                 74.6,  2),   # подиум, корсет
    ("marie-claire-event.mp4",      121.9,  2),   # рэп-группа
    ("salaris-event-fin180416.mp4", 160.7,  1),   # азотный дым
    # ── Секция 3 · ЭКСПО / МУЛЬТИМЕДИА ──
    ("stavropol-vdnh-main.mp4",       2.6,  2),   # павильон ВДНХ
    ("samara-vdnh-1.mp4",             5.0,  2),   # капсула на экране
    ("samara-vdnh-8.mp4",            15.2,  2),   # ракета на вертикальном экране
    ("samara-vdnh-8.mp4",            41.4,  2),   # отделение ступеней
    ("stavropol-vdnh-nakedeye.mp4", 104.9,  2),   # водопад на экране
    ("samara-vdnh-7.mp4",            13.2,  2),   # ребёнок и виртуальный мяч
    ("content-infopanels.mp4",       19.3,  1),   # палец по тач-панели
    ("stavropol-vdnh-main.mp4",      44.2,  2),   # лес POV (VR-заезд)
    ("stavropol-vdnh-main.mp4",      33.8,  2),   # VR-велосипед
    ("content-mapping-curved.mp4",   53.3,  2),   # Lada на изогнутом экране
    ("samara-pres-5spirits.mp4",     71.5,  2),   # AI-богиня воды
    ("samara-pres-5spirits.mp4",     51.5,  2),   # VR-девушка
    ("transrzhd.mp4",               109.8,  2),   # контейнеры сверху
    ("samara-vdnh-30.mp4",          381.5,  2),   # стенд Самарской области
    ("technopark-zubovo.mp4",        69.1,  2),   # сварка, искры
    ("transrzhd.mp4",               169.5,  2),   # флешмоб «10» сверху
    # ── Секция 4 · ВИДЕОПРОДАКШН ──
    ("vivax-samburskaya.mp4",         8.5,  2),   # Самбурская
    ("vivax-samburskaya.mp4",        18.4,  1),   # ноги, бег
    ("vivax-samburskaya.mp4",        28.2,  1),   # прыжок на степ
    ("gazelle-transformer.mp4",      47.6,  2),   # робот летит над полем
    ("gazelle-transformer.mp4",      58.0,  2),   # трансформация крупно
    ("changan.mp4",                   5.9,  2),   # приборная панель
    ("hm-showreel.mp4",              60.4,  2),   # SilkWay 3D-логотип
    ("samara-vdnh-7.mp4",            62.5,  2),   # хоккеист на льду
    # ── Секция 5 · БОЛЬШИЕ ШОУ ──
    ("stavropol-3dmapping.mp4",      49.0,  2),   # световое шоу над сценой
    ("content-mapping-arch.mp4",      7.7,  2),   # золотой каркас здания
    ("stavropol-3dmapping.mp4",      94.2,  2),   # зелёные лазеры по зданию
    ("stavropol-3dmapping.mp4",     101.7,  2),   # лазерная ёлка
    ("pt-film-short.mp4",            18.8,  2),   # тоннель стадиона
    ("hm-showreel.mp4",              93.0,  2),   # поле стадиона
    ("samsung-2020.mp4",             95.0,  2),   # воздушная гимнастка
    ("samsung-2020.mp4",            124.1,  2),   # концерт, пиро
    ("content-graphics.mp4",         14.3,  2),   # зал с экранами
    ("stavropol-3dmapping.mp4",     116.8,  2),   # лучи над толпой
    ("mozaika.mp4",                   6.8,  2),   # город с воздуха
    ("salaris-2.mp4",                57.3,  2),   # шоссе с воздуха
    ("hm-showreel.mp4",             106.5,  2),   # новогодняя толпа
    ("stavropol-3dmapping.mp4",     124.3,  2),   # ёлка + толпа панорама
    ("changan.mp4",                  49.6,  1),   # руки диджея
    # ── Секция 6 · ФИНАЛЬНЫЙ РАЗГОН (1 бит) ──
    ("gazelle-transformer.mp4",      34.0,  1),
    ("content-mapping-arch.mp4",      4.4,  1),
    ("samara-vdnh-8.mp4",            50.6,  1),
    ("samsung-2020.mp4",             32.3,  1),
    ("vivax-samburskaya.mp4",        16.0,  1),
    ("stavropol-vdnh-nakedeye.mp4", 127.8,  1),
    ("event-riviera.mp4",           175.8,  1),
    ("changan.mp4",                  74.8,  1),
    ("stavropol-3dmapping.mp4",     110.0,  1),
    ("lingerie.mp4",                160.8,  1),
    ("transrzhd.mp4",               227.3,  1),
    ("samara-vdnh-8.mp4",            16.0,  1),
    ("content-mapping-arch.mp4",      5.4,  1),
    ("gazelle-transformer.mp4",      48.4,  1),
    ("samsung-2020.mp4",            124.8,  1),
    ("stavropol-3dmapping.mp4",      95.0,  1),
    ("vivax-samburskaya.mp4",        28.4,  1),
    ("samara-vdnh-7.mp4",            63.0,  1),
    ("content-graphics.mp4",        128.2,  1),
    ("salaris-2.mp4",                12.0,  1),
    ("marie-claire-event.mp4",      122.5,  1),
    ("hm-showreel.mp4",              48.2,  1),   # ч/б робот — эхо
    # финальные аккорды (2 бита)
    ("stavropol-3dmapping.mp4",     109.0,  2),   # фейерверк панорама
    ("gazelle-transformer.mp4",      33.2,  2),   # трансформация
    ("hm-showreel.mp4",              16.1,  2),   # конфетти над сценой
]

VF = ("scale=1280:720:force_original_aspect_ratio=increase:flags=bicubic,"
      "crop=1280:720,fps=25,setsar=1,format=yuv420p")
X264 = ["-c:v", "libx264", "-crf", "16", "-preset", "veryfast",
        "-pix_fmt", "yuv420p", "-profile:v", "high", "-level", "4.0",
        "-x264-params", "keyint=50:min-keyint=25", "-an"]

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FFMPEG FAIL:", " ".join(cmd)); print(r.stderr[-1500:]); sys.exit(1)

segments = []

# ── Заставка: анимация сборки куба (секвенция из intro_frames/) ──
intro_frames = round(beat_t(INTRO_BEATS) * FPS)  # 0 → бит 9 (205 кадров)
intro = os.path.join(SEG, "seg_000_intro.ts")
run(["ffmpeg", "-y", "-v", "error", "-framerate", "25",
     "-i", os.path.join(SC, "intro_frames/f%04d.jpg"),
     "-vf", (f"fade=t=in:st=0:d=0.35:color=white,"
             f"fade=t=out:st={intro_frames/FPS-0.12}:d=0.12:color=white,"
             "setsar=1,format=yuv420p"),
     "-frames:v", str(intro_frames), *X264, "-f", "mpegts", intro])
segments.append(intro)
print(f"intro: {intro_frames} frames ({intro_frames/FPS:.2f}s)")

# ── Монтаж ──
beat_cursor = INTRO_BEATS
frame_cursor = intro_frames
for i, (src, start, nb) in enumerate(EDL, 1):
    beat_cursor += nb
    end_frame = round(beat_t(beat_cursor) * FPS)
    nframes = end_frame - frame_cursor
    frame_cursor = end_frame
    path = os.path.join(MEDIA, src)
    if not os.path.exists(path):
        print("MISSING:", src); sys.exit(1)
    out = os.path.join(SEG, f"seg_{i:03d}.ts")
    if not os.path.exists(out):
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{start:.3f}", "-i", path,
             "-frames:v", str(nframes), "-vf", VF, *X264, "-f", "mpegts", out])
    segments.append(out)
    print(f"{i:3d}. {src:32s} @{start:7.1f}s  {nb}b {nframes}f  -> t={end_frame/FPS:7.2f}")

# ── Финальная карточка ──
outro_frames = round(OUTRO_END * FPS) - frame_cursor
outro = os.path.join(SEG, "seg_999_outro.ts")
run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", "25",
     "-i", os.path.join(SC, "card_outro.png"),
     "-vf", (f"zoompan=z='1.05-0.0004*on':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2'"
             f":d={outro_frames}:s=1280x720:fps=25,"
             "fade=t=in:st=0:d=0.4:color=white,"
             f"fade=t=out:st={outro_frames/FPS-0.8}:d=0.8:color=white,"
             "setsar=1,format=yuv420p"),
     "-frames:v", str(outro_frames), *X264, "-f", "mpegts", outro])
segments.append(outro)
print(f"outro: {outro_frames} frames, конец = {OUTRO_END}s")

# ── Склейка + звук ──
listfile = os.path.join(SEG, "concat.txt")
with open(listfile, "w") as f:
    for s in segments:
        f.write(f"file '{s}'\n")

concat_ts = os.path.join(SEG, "full.ts")
run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
     "-i", listfile, "-c", "copy", concat_ts])

final = os.path.join(SC, "showreel-2min-v1.mp4")
run(["ffmpeg", "-y", "-v", "error", "-i", concat_ts,
     "-i", os.path.join(SC, "audio/showreel.wav"),
     "-filter_complex",
     f"[1:a]atrim=0:{OUTRO_END},afade=t=out:st={OUTRO_END-3}:d=3,"
     "loudnorm=I=-14:TP=-1.0:LRA=11[a]",
     "-map", "0:v", "-map", "[a]",
     "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
     "-movflags", "+faststart", final])
print("DONE:", final)
r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                    "format=duration,size", "-of", "csv=p=0", final],
                   capture_output=True, text=True)
print("duration,size:", r.stdout.strip())
