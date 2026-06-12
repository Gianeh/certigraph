#!/usr/bin/env python3
"""Generate the CertiGraph demo video.

This script is intentionally kept outside the runtime package. It requires
Pillow and ffmpeg, but CertiGraph itself remains dependency-free.

Usage:
    python scripts/generate_demo_video.py

Outputs:
    docs/assets/certigraph-demo.mp4
    docs/assets/certigraph-demo-thumbnail.png
    docs/assets/certigraph-demo.srt
"""
from __future__ import annotations

import math
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Sequence

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs" / "assets"
OUT_MP4 = OUT_DIR / "certigraph-demo.mp4"
OUT_THUMB = OUT_DIR / "certigraph-demo-thumbnail.png"
OUT_SRT = OUT_DIR / "certigraph-demo.srt"

W, H = 1920, 1080
FPS = 24
DURATION = 57.0

BG0 = (7, 11, 24)
BG1 = (13, 19, 42)
PANEL = (16, 26, 48)
PANEL2 = (21, 33, 58)
TEXT = (236, 245, 255)
MUTED = (149, 164, 189)
GREEN = (74, 242, 166)
GREEN_DARK = (22, 148, 102)
VIOLET = (139, 92, 246)
BLUE = (56, 189, 248)
RED = (255, 94, 115)
AMBER = (245, 197, 66)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def _first_font(paths: Sequence[str], size: int) -> ImageFont.FreeTypeFont:
    for p in paths:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)


def font(size: int, weight: str = "regular") -> ImageFont.FreeTypeFont:
    base = {
        "regular": [
            "/usr/share/fonts/opentype/inter/Inter-Regular.otf",
            "/usr/share/fonts/truetype/lato/Lato-Regular.ttf",
        ],
        "medium": [
            "/usr/share/fonts/opentype/inter/Inter-Medium.otf",
            "/usr/share/fonts/truetype/lato/Lato-Medium.ttf",
        ],
        "semibold": [
            "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf",
            "/usr/share/fonts/truetype/lato/Lato-Semibold.ttf",
        ],
        "bold": [
            "/usr/share/fonts/opentype/inter/Inter-Bold.otf",
            "/usr/share/fonts/truetype/lato/Lato-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ],
        "mono": [
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        ],
    }
    return _first_font(base.get(weight, base["regular"]), size)

F_REG_28 = font(28)
F_REG_32 = font(32)
F_REG_36 = font(36)
F_MED_30 = font(30, "medium")
F_MED_36 = font(36, "medium")
F_MED_42 = font(42, "medium")
F_BOLD_44 = font(44, "bold")
F_BOLD_52 = font(52, "bold")
F_BOLD_64 = font(64, "bold")
F_BOLD_86 = font(86, "bold")
F_BOLD_112 = font(112, "bold")
F_MONO_24 = font(24, "mono")
F_MONO_28 = font(28, "mono")
F_MONO_32 = font(32, "mono")
F_MONO_36 = font(36, "mono")


def clamp(x: float, a: float = 0.0, b: float = 1.0) -> float:
    return max(a, min(b, x))


def ease(x: float) -> float:
    x = clamp(x)
    return x * x * (3 - 2 * x)


def ease_out(x: float) -> float:
    x = clamp(x)
    return 1 - (1 - x) ** 3


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def mix(c1: tuple[int, int, int], c2: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return tuple(int(lerp(c1[i], c2[i], t)) for i in range(3))


def alpha_composite(base: Image.Image, overlay: Image.Image) -> Image.Image:
    if base.mode != "RGBA":
        base = base.convert("RGBA")
    return Image.alpha_composite(base, overlay)


def make_background() -> Image.Image:
    img = Image.new("RGB", (W, H), BG0)
    draw = ImageDraw.Draw(img)
    for y in range(H):
        ty = y / H
        c = mix(BG0, BG1, ty)
        draw.line([(0, y), (W, y)], fill=c)
    # soft aurora glows
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((-220, -260, 760, 600), fill=(74, 242, 166, 34))
    gd.ellipse((1160, -180, 2200, 650), fill=(139, 92, 246, 44))
    gd.ellipse((930, 620, 2280, 1430), fill=(56, 189, 248, 18))
    glow = glow.filter(ImageFilter.GaussianBlur(80))
    img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
    draw = ImageDraw.Draw(img)
    for x in range(60, W, 90):
        for y in range(60, H, 90):
            a = 20 if (x + y) % 180 == 0 else 11
            draw.ellipse((x - 1, y - 1, x + 1, y + 1), fill=(90, 113, 142))
    return img.convert("RGBA")

BASE_BG = make_background()


def rounded(img: Image.Image, box: tuple[int, int, int, int], radius: int, fill, outline=None, width: int = 1):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def overlay_round(img: Image.Image, box: tuple[int, int, int, int], radius: int, fill, outline=None, width: int = 1):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)
    return alpha_composite(img, ov)


def text_size(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont) -> tuple[int, int]:
    b = draw.textbbox((0, 0), text, font=fnt)
    return b[2] - b[0], b[3] - b[1]


def draw_shadow_text(
    img: Image.Image,
    xy: tuple[int, int],
    text: str,
    fnt: ImageFont.ImageFont,
    fill=TEXT,
    anchor: str | None = None,
    shadow=(0, 0, 0, 90),
    spacing: int = 4,
):
    d = ImageDraw.Draw(img)
    x, y = xy
    d.multiline_text((x + 3, y + 5), text, font=fnt, fill=shadow, anchor=anchor, spacing=spacing)
    d.multiline_text((x, y), text, font=fnt, fill=fill, anchor=anchor, spacing=spacing)


def wrap_text(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for w in words:
        trial = " ".join(current + [w])
        if text_size(draw, trial, fnt)[0] <= max_width or not current:
            current.append(w)
        else:
            lines.append(" ".join(current))
            current = [w]
    if current:
        lines.append(" ".join(current))
    return lines


def draw_wrapped(
    img: Image.Image,
    xy: tuple[int, int],
    text: str,
    fnt: ImageFont.ImageFont,
    max_width: int,
    fill=MUTED,
    line_gap: int = 12,
):
    d = ImageDraw.Draw(img)
    x, y = xy
    for line in wrap_text(d, text, fnt, max_width):
        d.text((x, y), line, font=fnt, fill=fill)
        y += text_size(d, line, fnt)[1] + line_gap


def draw_mini_logo(img: Image.Image, x: int, y: int, s: float = 1.0):
    d = ImageDraw.Draw(img)
    pts = [(x, y + 32 * s), (x + 52 * s, y), (x + 112 * s, y + 26 * s), (x + 92 * s, y + 84 * s), (x + 28 * s, y + 82 * s)]
    edges = [(0, 1, GREEN), (1, 2, VIOLET), (2, 3, BLUE), (3, 4, GREEN), (4, 0, VIOLET), (1, 3, GREEN)]
    for i, j, color in edges:
        d.line([pts[i], pts[j]], fill=color + (210,), width=max(2, int(5 * s)))
    for idx, p in enumerate(pts):
        r = 10 * s
        fill = GREEN if idx in (0, 3) else (VIOLET if idx in (1, 4) else BLUE)
        d.ellipse((p[0] - r, p[1] - r, p[0] + r, p[1] + r), fill=fill + (255,), outline=WHITE + (40,), width=2)


def draw_top_brand(img: Image.Image, alpha: int = 255):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_mini_logo(ov, 64, 48, 0.55)
    d = ImageDraw.Draw(ov)
    d.text((148, 54), "CertiGraph", font=F_BOLD_44, fill=TEXT + (alpha,))
    d.text((150, 105), "proof-carrying graph results", font=F_REG_28, fill=MUTED + (alpha,))
    return alpha_composite(img, ov)


def draw_progress(img: Image.Image, t: float):
    d = ImageDraw.Draw(img)
    rounded(img, (90, H - 48, W - 90, H - 36), 6, (255, 255, 255, 28))
    rounded(img, (90, H - 48, int(90 + (W - 180) * t / DURATION), H - 36), 6, GREEN + (180,))


def draw_badge(img: Image.Image, xy: tuple[int, int], label: str, color: tuple[int, int, int], icon: str = ""):
    d = ImageDraw.Draw(img)
    x, y = xy
    label_full = (icon + "  " if icon else "") + label
    tw, th = text_size(d, label_full, F_MED_30)
    box = (x, y, x + tw + 44, y + th + 30)
    rounded(img, box, 22, color + (38,), outline=color + (180,), width=2)
    d.text((x + 22, y + 14), label_full, font=F_MED_30, fill=WHITE + (255,))


def arrowhead_points(p1: tuple[float, float], p2: tuple[float, float], size: float = 18.0):
    x1, y1 = p1
    x2, y2 = p2
    ang = math.atan2(y2 - y1, x2 - x1)
    return [
        (x2, y2),
        (x2 - size * math.cos(ang - math.pi / 6), y2 - size * math.sin(ang - math.pi / 6)),
        (x2 - size * math.cos(ang + math.pi / 6), y2 - size * math.sin(ang + math.pi / 6)),
    ]


def shorten(p1: tuple[int, int], p2: tuple[int, int], amount: float):
    x1, y1 = p1
    x2, y2 = p2
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1
    return (x1 + dx / L * amount, y1 + dy / L * amount), (x2 - dx / L * amount, y2 - dy / L * amount)


def draw_arrow(
    img: Image.Image,
    p1: tuple[int, int],
    p2: tuple[int, int],
    label: str,
    color: tuple[int, int, int],
    width: int = 6,
    highlight: float = 0.0,
):
    d = ImageDraw.Draw(img)
    a, b = shorten(p1, p2, 42)
    if highlight:
        d.line([a, b], fill=color + (60,), width=width + int(16 * highlight))
    d.line([a, b], fill=color + (225,), width=width)
    d.polygon(arrowhead_points(a, b, 22), fill=color + (240,))
    mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    tw, th = text_size(d, label, F_MED_30)
    rounded(img, (int(mid[0] - tw / 2 - 12), int(mid[1] - th / 2 - 10), int(mid[0] + tw / 2 + 12), int(mid[1] + th / 2 + 10)), 12, (8, 13, 28, 230))
    d.text((mid[0] - tw / 2, mid[1] - th / 2 - 1), label, font=F_MED_30, fill=TEXT + (240,))


def draw_node(img: Image.Image, xy: tuple[int, int], label: str, fill: tuple[int, int, int], subtitle: str | None = None):
    d = ImageDraw.Draw(img)
    x, y = xy
    r = 42
    # glow
    d.ellipse((x - r - 14, y - r - 14, x + r + 14, y + r + 14), fill=fill + (40,))
    d.ellipse((x - r, y - r, x + r, y + r), fill=(12, 18, 33, 255), outline=fill + (250,), width=5)
    tw, th = text_size(d, label, F_BOLD_44)
    d.text((x - tw / 2, y - th / 2 - 3), label, font=F_BOLD_44, fill=TEXT + (255,))
    if subtitle:
        sw, sh = text_size(d, subtitle, F_REG_28)
        d.text((x - sw / 2, y + r + 16), subtitle, font=F_REG_28, fill=fill + (255,))


def draw_terminal(img: Image.Image, box: tuple[int, int, int, int], lines: Sequence[tuple[str, tuple[int, int, int]]], reveal: float = 1.0, title: str = "terminal"):
    x1, y1, x2, y2 = box
    d = ImageDraw.Draw(img)
    # shadow
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((x1 + 12, y1 + 18, x2 + 12, y2 + 18), radius=26, fill=(0, 0, 0, 90))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    img.alpha_composite(shadow)
    rounded(img, box, 26, (5, 9, 20, 242), outline=(95, 115, 150, 85), width=2)
    rounded(img, (x1, y1, x2, y1 + 62), 26, (15, 23, 42, 250))
    # flatten top bottom artifacts by header overlay not worth fixing
    for i, c in enumerate([RED, AMBER, GREEN]):
        d.ellipse((x1 + 28 + i * 28, y1 + 22, x1 + 44 + i * 28, y1 + 38), fill=c + (230,))
    d.text((x1 + 130, y1 + 18), title, font=F_MONO_24, fill=MUTED + (240,))
    all_text = "\n".join(line for line, _ in lines)
    total_chars = len(all_text)
    visible = int(total_chars * clamp(reveal))
    used = 0
    y = y1 + 88
    max_text_width = x2 - x1 - 68
    for line, color in lines:
        n = max(0, min(len(line), visible - used))
        if n > 0:
            shown = line[:n]
            # Marketing/demo terminals must never bleed outside their cards.
            while shown and text_size(d, shown, F_MONO_28)[0] > max_text_width:
                shown = shown[:-1]
            if len(shown) < n and shown:
                while shown and text_size(d, shown + "...", F_MONO_28)[0] > max_text_width:
                    shown = shown[:-1]
                shown = shown + "..."
            d.text((x1 + 34, y), shown, font=F_MONO_28, fill=color + (255,))
        used += len(line) + 1
        y += 38
        if y > y2 - 40:
            break
    # cursor
    if reveal < 1:
        d.rectangle((x1 + 34 + (visible % 42) * 16, y - 38, x1 + 46 + (visible % 42) * 16, y - 8), fill=GREEN + (180,))


def draw_code_panel(img: Image.Image, box: tuple[int, int, int, int], lines: Sequence[str], title: str):
    x1, y1, x2, y2 = box
    d = ImageDraw.Draw(img)
    rounded(img, box, 26, (9, 16, 30, 230), outline=(100, 117, 150, 85), width=2)
    d.text((x1 + 28, y1 + 22), title, font=F_MED_30, fill=BLUE + (255,))
    y = y1 + 72
    for line in lines:
        color = TEXT if not line.strip().startswith("#") else MUTED
        d.text((x1 + 28, y), line, font=F_MONO_28, fill=color + (245,))
        y += 38


@dataclass(frozen=True)
class Scene:
    start: float
    end: float
    draw: Callable[[Image.Image, float, float], Image.Image]


def title_scene(img: Image.Image, lt: float, gt: float) -> Image.Image:
    p = ease_out(lt / 1.4)
    img = draw_top_brand(img, int(255 * p))
    d = ImageDraw.Draw(img)
    # big logo graph
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_mini_logo(ov, int(830 - 30 * (1 - p)), 202, 2.0)
    img = alpha_composite(img, ov)
    draw_shadow_text(img, (W // 2, 438), "CertiGraph", F_BOLD_112, fill=TEXT, anchor="mm")
    draw_shadow_text(img, (W // 2, 536), "Proof-carrying graph results", F_BOLD_52, fill=GREEN, anchor="mm")
    draw_shadow_text(img, (W // 2, 610), "Let any solver compute the answer. Trust only a tiny checker.", F_REG_36, fill=MUTED, anchor="mm")
    badges = [("zero deps", GREEN), ("AI/untrusted solvers", VIOLET), ("small auditable core", BLUE)]
    x = 524
    for i, (label, color) in enumerate(badges):
        draw_badge(img, (x, 700), label, color, "")
        x += [255, 418, 0][i]
    draw_wrapped(img, (650, 830), "Do not trust the solver. Verify the result.", F_BOLD_44, 700, fill=TEXT, line_gap=8)
    return img


def pain_scene(img: Image.Image, lt: float, gt: float) -> Image.Image:
    img = draw_top_brand(img)
    d = ImageDraw.Draw(img)
    draw_shadow_text(img, (120, 220), "Modern graph answers\ncome from black boxes.", F_BOLD_64, fill=TEXT)
    draw_wrapped(img, (124, 390), "AI agents, remote APIs, distributed jobs, GPU kernels, vendor solvers, cached pipelines — any of them can be wrong while still looking plausible.", F_REG_36, 720, fill=MUTED, line_gap=14)
    # solver boxes
    cards = [
        ("LLM agent", "writes code", VIOLET),
        ("Remote API", "black box", BLUE),
        ("GPU job", "fast + opaque", AMBER),
        ("Distributed solver", "hard to audit", GREEN),
    ]
    for i, (a, b, c) in enumerate(cards):
        x = 1040 + (i % 2) * 340
        y = 245 + (i // 2) * 220
        appear = ease_out((lt - i * 0.25) / 1.0)
        yy = int(y + 40 * (1 - appear))
        rounded(img, (x, yy, x + 286, yy + 150), 28, c + (30,), outline=c + (170,), width=2)
        d.text((x + 26, yy + 28), a, font=F_BOLD_44, fill=TEXT + (int(255 * appear),))
        d.text((x + 28, yy + 88), b, font=F_REG_32, fill=MUTED + (int(255 * appear),))
    # arrows converge
    center = (1385, 725)
    for p0, c in [((1183, 395), VIOLET), ((1523, 395), BLUE), ((1183, 615), AMBER), ((1523, 615), GREEN)]:
        progress = ease_out((lt - 1.7) / 2.1)
        p1 = (int(lerp(p0[0], center[0], progress)), int(lerp(p0[1], center[1], progress)))
        d.line([p0, p1], fill=c + (190,), width=5)
    warn_t = 0.5 + 0.5 * math.sin(gt * 4)
    rounded(img, (1198, 692, 1572, 802), 26, RED + (30 + int(20 * warn_t),), outline=RED + (210,), width=3)
    d.text((1232, 718), "claimed answer?", font=F_BOLD_44, fill=TEXT + (255,))
    d.text((1236, 768), "plausible ≠ verified", font=F_REG_30 if False else F_REG_28, fill=RED + (255,))
    draw_badge(img, (122, 770), "The fix: verify the result, not the whole solver", GREEN, "✓")
    return img


def contract_scene(img: Image.Image, lt: float, gt: float) -> Image.Image:
    img = draw_top_brand(img)
    d = ImageDraw.Draw(img)
    draw_shadow_text(img, (120, 190), "The CertiGraph contract", F_BOLD_64, fill=TEXT)
    draw_wrapped(img, (123, 272), "A producer can be huge, clever, stochastic or untrusted. The certificate checker stays small, deterministic and boring.", F_REG_36, 820, fill=MUTED, line_gap=14)
    # pipeline
    items = [
        (140, 500, 360, 685, "instance", "graph + query", BLUE),
        (470, 500, 720, 685, "solver", "any implementation", VIOLET),
        (845, 450, 1175, 735, "result +\ncertificate", "witness object", AMBER),
        (1305, 500, 1600, 685, "tiny checker", "trusted core", GREEN),
    ]
    for i, (x1, y1, x2, y2, title, sub, c) in enumerate(items):
        a = ease_out((lt - i * 0.35) / 1.0)
        yy1 = int(y1 + 40 * (1 - a)); yy2 = int(y2 + 40 * (1 - a))
        rounded(img, (x1, yy1, x2, yy2), 30, c + (30,), outline=c + (185,), width=3)
        d.multiline_text(((x1 + x2) // 2, yy1 + 50), title, font=F_BOLD_44, fill=TEXT + (int(255 * a),), anchor="ma", align="center", spacing=3)
        d.text(((x1 + x2) // 2, yy2 - 52), sub, font=F_REG_28, fill=MUTED + (int(255 * a),), anchor="mm")
    arrow_y = 592
    for x0, x1, c in [(362, 466, BLUE), (724, 840, VIOLET), (1178, 1302, AMBER)]:
        prog = ease_out((lt - 1.1) / 2.0)
        d.line([(x0, arrow_y), (int(lerp(x0, x1, prog)), arrow_y)], fill=c + (220,), width=8)
        if prog > 0.9:
            d.polygon(arrowhead_points((x0, arrow_y), (x1, arrow_y), 24), fill=c + (240,))
    # final accept/reject
    a = ease_out((lt - 3.2) / 1.0)
    rounded(img, (1650, 515, 1810, 585), 24, GREEN + (int(42 * a),), outline=GREEN + (int(200 * a),), width=3)
    rounded(img, (1650, 625, 1810, 695), 24, RED + (int(30 * a),), outline=RED + (int(160 * a),), width=3)
    d.text((1730, 550), "ACCEPT", font=F_MED_30, fill=GREEN + (int(255 * a),), anchor="mm")
    d.text((1730, 660), "REJECT", font=F_MED_30, fill=RED + (int(255 * a),), anchor="mm")
    # little invariant card
    rounded(img, (560, 815, 1360, 930), 28, (255, 255, 255, 18), outline=(255, 255, 255, 55), width=1)
    d.text((602, 843), "Invariant", font=F_MED_36, fill=BLUE + (255,))
    d.text((602, 890), "If the checker accepts, the claimed graph result satisfies a mathematical certificate.", font=F_REG_32, fill=TEXT + (240,))
    return img


def bad_solver_scene(img: Image.Image, lt: float, gt: float) -> Image.Image:
    img = draw_top_brand(img)
    d = ImageDraw.Draw(img)
    draw_shadow_text(img, (95, 165), "Demo: catch a wrong\nAI-generated shortest path", F_BOLD_52, fill=TEXT)
    draw_wrapped(img, (98, 305), "The solver claims dist(b)=5. But edge a→b with weight -1 improves it to 1.", F_REG_32, 720, fill=MUTED, line_gap=10)
    # left terminal
    lines = [
        ("$ python demo_bad_sssp.py", GREEN),
        ("Untrusted solver result:", TEXT),
        ("{", MUTED),
        ('  "ok": false,', RED),
        ('  "message": "relaxation violation",', RED),
        ('  "edge": ["a", "b", -1.0],', MUTED),
        ('  "candidate": 1.0', MUTED),
        ("}", MUTED),
    ]
    draw_terminal(img, (92, 430, 900, 890), lines, reveal=ease_out((lt - 0.6) / 5.0), title="bad solver demo")
    # graph
    box = (990, 200, 1810, 820)
    rounded(img, box, 34, (9, 16, 30, 215), outline=(95, 115, 150, 80), width=2)
    d.text((1030, 230), "SSSP instance", font=F_MED_36, fill=BLUE + (255,))
    pts = {"s": (1115, 420), "a": (1360, 330), "b": (1360, 605), "c": (1620, 470)}
    pulse = 0.5 + 0.5 * math.sin(gt * 5)
    draw_arrow(img, pts["s"], pts["a"], "2", GREEN, width=6, highlight=0.4 * pulse)
    draw_arrow(img, pts["s"], pts["b"], "5", VIOLET, width=5, highlight=0.1)
    draw_arrow(img, pts["a"], pts["b"], "-1", RED, width=7, highlight=0.8 * pulse)
    draw_arrow(img, pts["b"], pts["c"], "2", BLUE, width=5, highlight=0.0)
    draw_arrow(img, pts["a"], pts["c"], "5", VIOLET, width=5, highlight=0.0)
    draw_node(img, pts["s"], "s", GREEN, "0")
    draw_node(img, pts["a"], "a", GREEN, "2")
    draw_node(img, pts["b"], "b", RED, "claimed 5")
    draw_node(img, pts["c"], "c", BLUE, "?")
    # math box
    rounded(img, (1040, 715, 1760, 790), 20, RED + (35,), outline=RED + (180,), width=2)
    d.text((1070, 735), "2 + (-1) = 1  <  claimed 5", font=F_BOLD_44, fill=TEXT + (255,))
    if lt > 5.2:
        draw_badge(img, (1090, 860), "REJECTED before downstream code can act", RED, "")
    return img


def valid_cert_scene(img: Image.Image, lt: float, gt: float) -> Image.Image:
    img = draw_top_brand(img)
    d = ImageDraw.Draw(img)
    draw_shadow_text(img, (96, 185), "Now verify a proof-carrying answer", F_BOLD_52, fill=TEXT)
    draw_wrapped(img, (98, 250), "A valid SSSP certificate gives distances and parent edges. The checker proves every path exists and no edge can improve the result.", F_REG_32, 790, fill=MUTED, line_gap=10)
    # terminal right
    lines = [
        ("$ certigraph verify sssp examples/sssp_valid.json", GREEN),
        ("{", MUTED),
        ('  "message": "valid SSSP certificate",', GREEN),
        ('  "details": {', MUTED),
        ('    "vertices": 5, "edges": 5,', MUTED),
        ('    "reachable": 4', MUTED),
        ('  },', MUTED),
        ('  "ok": true', GREEN),
        ("}", MUTED),
    ]
    draw_terminal(img, (900, 300, 1818, 748), lines, reveal=ease_out((lt - 0.6) / 4.0), title="certigraph verify")
    # certificate envelope
    rounded(img, (105, 390, 790, 830), 30, (9, 16, 30, 225), outline=GREEN + (125,), width=2)
    d.text((145, 425), "certificate.json", font=F_MED_36, fill=GREEN + (255,))
    code = [
        '{',
        '  "kind": "sssp",',
        '  "source": "s",',
        '  "distance": {"s": 0, "a": 2,',
        '               "b": 1, "c": 3},',
        '  "parent": {"a": 0, "b": 2,',
        '             "c": 3}',
        '}',
    ]
    y = 485
    for line in code:
        color = GREEN if '"b": 1' in line or '"ok"' in line else (TEXT if line.strip().startswith('"') or ':' in line else MUTED)
        d.text((145, y), line, font=F_MONO_28, fill=color + (245,))
        y += 38
    if lt > 4.8:
        draw_badge(img, (925, 780), "ACCEPTED: valid shortest-path certificate", GREEN, "✓")
        rounded(img, (925, 870, 1760, 950), 26, GREEN + (28,), outline=GREEN + (120,), width=2)
        d.text((960, 892), "Trust moves from producer to witness + checker.", font=F_REG_36, fill=TEXT + (245,))
    return img


def checkers_scene(img: Image.Image, lt: float, gt: float) -> Image.Image:
    img = draw_top_brand(img)
    d = ImageDraw.Draw(img)
    draw_shadow_text(img, (W // 2, 175), "Small checkers. Concrete guarantees.", F_BOLD_64, fill=TEXT, anchor="mm")
    draw_shadow_text(img, (W // 2, 250), "Each result carries the evidence needed to verify it independently.", F_REG_36, fill=MUTED, anchor="mm")
    cards = [
        ("SSSP", "distances + parents", "no relaxation improves", GREEN),
        ("MSF / MST", "selected edge indices", "spans + cycle optimality", AMBER),
        ("Max-flow", "flow + s-t cut", "equal flow and cut", BLUE),
        ("Topo order", "vertex ordering", "every edge goes forward", VIOLET),
        ("Bipartition", "two-coloring", "every edge crosses", GREEN),
    ]
    start_x = 155
    for i, (name, cert, guarantee, c) in enumerate(cards):
        a = ease_out((lt - i * 0.25) / 0.9)
        x = start_x + i * 345
        y = int(365 + 45 * (1 - a))
        rounded(img, (x, y, x + 300, y + 405), 32, c + (28,), outline=c + (165,), width=2)
        d.text((x + 30, y + 42), name, font=F_BOLD_44, fill=TEXT + (int(255 * a),))
        d.text((x + 30, y + 112), "certificate", font=F_REG_28, fill=MUTED + (int(255 * a),))
        draw_wrapped(img, (x + 30, y + 150), cert, F_MED_30, 240, fill=c, line_gap=8)
        d.line((x + 30, y + 240, x + 270, y + 240), fill=(255, 255, 255, int(45 * a)), width=2)
        d.text((x + 30, y + 266), "checker proves", font=F_REG_28, fill=MUTED + (int(255 * a),))
        draw_wrapped(img, (x + 30, y + 306), guarantee, F_MED_30, 240, fill=TEXT, line_gap=8)
    rounded(img, (300, 850, 1620, 940), 30, (255, 255, 255, 18), outline=(255, 255, 255, 55), width=1)
    d.text((W // 2, 895), "The solver can be optimized. The checker should be boring.", font=F_BOLD_44, fill=GREEN + (255,), anchor="mm")
    return img


def contribution_scene(img: Image.Image, lt: float, gt: float) -> Image.Image:
    img = draw_top_brand(img)
    d = ImageDraw.Draw(img)
    draw_shadow_text(img, (W // 2, 170), "Make graph computation more trustworthy", F_BOLD_64, fill=TEXT, anchor="mm")
    draw_shadow_text(img, (W // 2, 246), "CertiGraph is a small layer with a big surface for contributions.", F_REG_36, fill=MUTED, anchor="mm")
    bullets = [
        ("Add checkers", "matching, SCC, dominators, min-cost flow", GREEN),
        ("Integrate solvers", "NetworkX, OR-Tools, cuGraph, Spark, Rust/WASM", BLUE),
        ("Harden the core", "fuzzing, exact numerics, formal verification", VIOLET),
    ]
    for i, (title, sub, c) in enumerate(bullets):
        a = ease_out((lt - 0.4 - i * 0.35) / 1.0)
        x = 285
        y = int(360 + i * 150 + 36 * (1 - a))
        rounded(img, (x, y, W - x, y + 108), 28, c + (25,), outline=c + (150,), width=2)
        d.text((x + 44, y + 25), title, font=F_BOLD_44, fill=TEXT + (int(255 * a),))
        d.text((x + 430, y + 34), sub, font=F_REG_32, fill=MUTED + (int(255 * a),))
    # final claim
    if lt > 3.2:
        y0 = 845
        rounded(img, (280, y0, W - 280, y0 + 110), 35, GREEN + (34,), outline=GREEN + (170,), width=3)
        draw_shadow_text(img, (W // 2, y0 + 54), "Do not trust the solver. Verify the result.", F_BOLD_52, fill=TEXT, anchor="mm")
    d.text((W // 2, 980), "Star CertiGraph on GitHub", font=F_MED_36, fill=BLUE + (240,), anchor="mm")
    return img



@dataclass(frozen=True)
class Slide:
    name: str
    draw: Callable[[Image.Image, float, float], Image.Image]
    local_time: float
    duration: float


SLIDES: list[Slide] = [
    Slide("00_title", title_scene, 3.8, 6.0),
    Slide("01_pain", pain_scene, 6.8, 8.0),
    Slide("02_contract", contract_scene, 6.5, 8.0),
    Slide("03_bad_solver", bad_solver_scene, 8.8, 10.0),
    Slide("04_valid_certificate", valid_cert_scene, 8.6, 9.0),
    Slide("05_checkers", checkers_scene, 6.5, 8.0),
    Slide("06_contribute", contribution_scene, 6.6, 8.0),
]


def make_slide(slide: Slide, cumulative_t: float) -> Image.Image:
    img = BASE_BG.copy()
    img = slide.draw(img, slide.local_time, cumulative_t)
    draw_progress(img, cumulative_t)
    return Image.alpha_composite(BASE_BG.copy(), img).convert("RGB")


def write_srt() -> None:
    captions = [
        (0.0, 6.0, "CertiGraph: proof-carrying graph results for untrusted and AI-generated solvers."),
        (6.0, 14.0, "Modern graph answers can come from black boxes: agents, APIs, GPU jobs, distributed systems."),
        (14.0, 22.0, "The producer may be complex. The checker stays small, deterministic and auditable."),
        (22.0, 32.0, "Here a plausible shortest-path answer is wrong. The checker rejects it immediately."),
        (32.0, 41.0, "Now the result carries a valid certificate. The independent checker accepts."),
        (41.0, 49.0, "CertiGraph ships checkers for SSSP, MSF, max-flow, topological order and bipartition."),
        (49.0, 57.0, "Contribute more checkers, integrations, fuzzing and formal verification. Do not trust the solver. Verify the result."),
    ]

    def fmt(x: float) -> str:
        ms = int(round(x * 1000))
        h, rem = divmod(ms, 3600_000)
        m, rem = divmod(rem, 60_000)
        s, ms = divmod(rem, 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    lines: list[str] = []
    for idx, (a, b, text) in enumerate(captions, 1):
        lines.extend([str(idx), f"{fmt(a)} --> {fmt(b)}", text, ""])
    OUT_SRT.write_text("\n".join(lines), encoding="utf-8")


def render_mp4() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    slides_dir = OUT_DIR / "demo_slides"
    slides_dir.mkdir(exist_ok=True)
    cumulative = 0.0
    list_lines: list[str] = []
    for idx, slide in enumerate(SLIDES):
        path = slides_dir / f"{slide.name}.png"
        frame = make_slide(slide, cumulative)
        frame.save(path, optimize=True)
        if slide.name == "04_valid_certificate":
            frame.save(OUT_THUMB, optimize=True)
        list_lines.append(f"file '{path.as_posix()}'")
        list_lines.append(f"duration {slide.duration:.3f}")
        cumulative += slide.duration
    # Concat demuxer requires the last image repeated.
    last_path = slides_dir / f"{SLIDES[-1].name}.png"
    list_lines.append(f"file '{last_path.as_posix()}'")
    concat_file = slides_dir / "concat.txt"
    concat_file.write_text("\n".join(list_lines) + "\n", encoding="utf-8")
    total = sum(s.duration for s in SLIDES)
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-t", f"{total:.3f}",
        "-vf", f"fps={FPS},format=yuv420p,fade=t=in:st=0:d=0.35,fade=t=out:st={total-0.6:.2f}:d=0.6",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "18", "-movflags", "+faststart",
        str(OUT_MP4),
    ]
    subprocess.run(cmd, check=True)


def make_teaser_gif() -> None:
    out = OUT_DIR / "certigraph-demo-teaser.gif"
    cmd = [
        "ffmpeg", "-y", "-ss", "22", "-t", "19", "-i", str(OUT_MP4),
        "-vf", "fps=10,scale=960:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=96[p];[s1][p]paletteuse=dither=bayer:bayer_scale=5",
        str(out),
    ]
    subprocess.run(cmd, check=True)


def main() -> None:
    write_srt()
    render_mp4()
    make_teaser_gif()
    print(f"wrote {OUT_MP4}")
    print(f"wrote {OUT_THUMB}")
    print(f"wrote {OUT_SRT}")
    print(f"wrote {OUT_DIR / 'certigraph-demo-teaser.gif'}")


if __name__ == "__main__":
    main()
