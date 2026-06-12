#!/usr/bin/env python3
"""Generate CertiGraph visual assets.

Runtime package code has zero dependencies. This script is only for repository
branding/docs assets and requires Pillow.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
DOC_ASSETS = ROOT / "docs" / "assets"
ROOT_ASSETS = ROOT / "assets"
DOC_ASSETS.mkdir(parents=True, exist_ok=True)
ROOT_ASSETS.mkdir(parents=True, exist_ok=True)


def write_svg(path: str, text: str) -> None:
    (DOC_ASSETS / path).write_text(text.strip() + "\n", encoding="utf-8")


logo_svg = r'''
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="260" viewBox="0 0 1200 260" role="img" aria-labelledby="title desc">
  <title id="title">CertiGraph logo</title>
  <desc id="desc">A graph inside a verification shield next to the CertiGraph wordmark.</desc>
  <defs>
    <linearGradient id="g" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0" stop-color="#7c3aed"/>
      <stop offset="1" stop-color="#10b981"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="260" rx="38" fill="#0b1020"/>
  <g transform="translate(58 32)">
    <path d="M99 0 L185 36 V101 C185 155 151 190 99 207 C47 190 13 155 13 101 V36 Z" fill="url(#g)" opacity="0.98"/>
    <path d="M99 19 L166 48 V101 C166 143 141 169 99 185 C57 169 32 143 32 101 V48 Z" fill="#0b1020" opacity="0.92"/>
    <g stroke="#a7f3d0" stroke-width="6" stroke-linecap="round">
      <line x1="72" y1="76" x2="122" y2="58"/>
      <line x1="122" y1="58" x2="139" y2="112"/>
      <line x1="72" y1="76" x2="91" y2="138"/>
      <line x1="91" y1="138" x2="139" y2="112"/>
    </g>
    <g fill="#ecfdf5" stroke="#10b981" stroke-width="4">
      <circle cx="72" cy="76" r="13"/>
      <circle cx="122" cy="58" r="13"/>
      <circle cx="139" cy="112" r="13"/>
      <circle cx="91" cy="138" r="13"/>
    </g>
    <path d="M64 111 L91 139 L146 80" fill="none" stroke="#f8fafc" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <g transform="translate(300 72)">
    <text x="0" y="66" font-family="Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, sans-serif" font-size="74" font-weight="850" fill="#f8fafc">CertiGraph</text>
    <text x="4" y="120" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="29" fill="#a7f3d0">proof-carrying graph results</text>
  </g>
  <text x="302" y="218" font-family="ui-sans-serif, system-ui" font-size="24" fill="#cbd5e1">Do not trust the solver. Verify the result.</text>
</svg>
'''
write_svg("certigraph-logo.svg", logo_svg)

icon_svg = r'''
<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512" role="img" aria-labelledby="title">
  <title id="title">CertiGraph icon</title>
  <defs><linearGradient id="g" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#7c3aed"/><stop offset="1" stop-color="#10b981"/></linearGradient></defs>
  <rect width="512" height="512" rx="92" fill="#0b1020"/>
  <path d="M256 54 L414 122 V246 C414 346 351 413 256 456 C161 413 98 346 98 246 V122 Z" fill="url(#g)"/>
  <path d="M256 93 L374 144 V247 C374 326 326 377 256 413 C186 377 138 326 138 247 V144 Z" fill="#0b1020" opacity="0.92"/>
  <g stroke="#a7f3d0" stroke-width="14" stroke-linecap="round">
    <line x1="202" y1="202" x2="284" y2="166"/>
    <line x1="284" y1="166" x2="322" y2="256"/>
    <line x1="202" y1="202" x2="226" y2="312"/>
    <line x1="226" y1="312" x2="322" y2="256"/>
  </g>
  <g fill="#ecfdf5" stroke="#10b981" stroke-width="8">
    <circle cx="202" cy="202" r="25"/>
    <circle cx="284" cy="166" r="25"/>
    <circle cx="322" cy="256" r="25"/>
    <circle cx="226" cy="312" r="25"/>
  </g>
  <path d="M176 264 L232 320 L342 192" fill="none" stroke="#f8fafc" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
'''
write_svg("certigraph-icon.svg", icon_svg)

certificate_flow_svg = r'''
<svg xmlns="http://www.w3.org/2000/svg" width="980" height="360" viewBox="0 0 980 360" role="img" aria-labelledby="title desc">
  <title id="title">CertiGraph certificate flow</title>
  <desc id="desc">An untrusted solver emits a result and certificate, then a small checker accepts or rejects it.</desc>
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#94a3b8"/></marker>
  </defs>
  <rect width="980" height="360" rx="28" fill="#0b1020"/>
  <g font-family="ui-sans-serif, system-ui, -apple-system, Segoe UI, sans-serif">
    <rect x="40" y="86" width="230" height="150" rx="24" fill="#1e1b4b" stroke="#7c3aed" stroke-width="3"/>
    <text x="70" y="136" fill="#f8fafc" font-size="28" font-weight="800">Producer</text>
    <text x="70" y="174" fill="#c4b5fd" font-size="18">fast / remote / AI</text>
    <text x="70" y="204" fill="#c4b5fd" font-size="18">not trusted</text>
    <line x1="278" y1="160" x2="405" y2="160" stroke="#94a3b8" stroke-width="5" marker-end="url(#arrow)"/>
    <rect x="415" y="60" width="210" height="88" rx="18" fill="#172554" stroke="#38bdf8" stroke-width="3"/>
    <text x="445" y="112" fill="#e0f2fe" font-size="25" font-weight="800">result</text>
    <rect x="415" y="178" width="210" height="88" rx="18" fill="#064e3b" stroke="#10b981" stroke-width="3"/>
    <text x="445" y="232" fill="#d1fae5" font-size="25" font-weight="800">certificate</text>
    <line x1="634" y1="105" x2="730" y2="150" stroke="#94a3b8" stroke-width="5" marker-end="url(#arrow)"/>
    <line x1="634" y1="222" x2="730" y2="174" stroke="#94a3b8" stroke-width="5" marker-end="url(#arrow)"/>
    <rect x="740" y="86" width="200" height="150" rx="24" fill="#022c22" stroke="#34d399" stroke-width="3"/>
    <text x="775" y="134" fill="#f8fafc" font-size="28" font-weight="800">Checker</text>
    <text x="775" y="174" fill="#a7f3d0" font-size="18">small / boring</text>
    <text x="775" y="204" fill="#a7f3d0" font-size="18">trusted core</text>
    <text x="340" y="318" fill="#cbd5e1" font-size="22">Accept only results whose evidence checks out.</text>
  </g>
</svg>
'''
write_svg("certificate-flow.svg", certificate_flow_svg)
write_svg("architecture.svg", certificate_flow_svg)

terminal_svg = r'''
<svg xmlns="http://www.w3.org/2000/svg" width="980" height="390" viewBox="0 0 980 390" role="img" aria-labelledby="title">
  <title id="title">CertiGraph terminal demo</title>
  <rect width="980" height="390" rx="24" fill="#020617"/>
  <rect x="18" y="18" width="944" height="354" rx="18" fill="#0f172a" stroke="#334155"/>
  <circle cx="48" cy="46" r="8" fill="#ef4444"/>
  <circle cx="76" cy="46" r="8" fill="#f59e0b"/>
  <circle cx="104" cy="46" r="8" fill="#22c55e"/>
  <g font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="22">
    <text x="42" y="96" fill="#93c5fd">$ python examples/ai_solver_wrong_answer_demo.py</text>
    <text x="42" y="136" fill="#f8fafc">Untrusted solver result:</text>
    <text x="42" y="176" fill="#fca5a5">{ "ok": false,</text>
    <text x="70" y="210" fill="#fca5a5">"message": "edge relaxation would improve distance" }</text>
    <text x="42" y="260" fill="#93c5fd">$ python -m certigraph verify sssp examples/sssp_valid.json</text>
    <text x="42" y="304" fill="#86efac">{ "ok": true, "message": "valid SSSP certificate" }</text>
    <text x="42" y="344" fill="#cbd5e1">Do not trust the solver. Verify the result.</text>
  </g>
</svg>
'''
write_svg("terminal-demo.svg", terminal_svg)

sssp_svg = r'''
<svg xmlns="http://www.w3.org/2000/svg" width="860" height="420" viewBox="0 0 860 420" role="img" aria-labelledby="title desc">
  <title id="title">Shortest-path certificate diagram</title>
  <desc id="desc">A small graph where parent edges and edge inequalities certify shortest-path distances.</desc>
  <defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="#64748b"/></marker></defs>
  <rect width="860" height="420" rx="24" fill="#0b1020"/>
  <g stroke="#64748b" stroke-width="4" fill="none" marker-end="url(#arrow)">
    <path d="M160 210 C260 100 370 100 470 205"/>
    <path d="M160 210 C270 260 360 260 470 205"/>
    <path d="M470 205 C560 120 650 120 735 200"/>
    <path d="M330 100 C475 60 610 90 735 200" stroke="#7c3aed"/>
  </g>
  <g fill="#ecfdf5" stroke="#10b981" stroke-width="5">
    <circle cx="160" cy="210" r="38"/>
    <circle cx="330" cy="100" r="38"/>
    <circle cx="470" cy="205" r="38"/>
    <circle cx="735" cy="200" r="38"/>
  </g>
  <g font-family="ui-sans-serif, system-ui" font-size="26" font-weight="800" fill="#0f172a" stroke="none" text-anchor="middle" dominant-baseline="middle">
    <text x="160" y="210">s</text>
    <text x="330" y="100">a</text>
    <text x="470" y="205">b</text>
    <text x="735" y="200">c</text>
  </g>
  <g font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="20" fill="#cbd5e1">
    <text x="188" y="128">2</text><text x="308" y="248">5</text><text x="565" y="126">2</text><text x="520" y="82">5</text>
    <text x="385" y="143" fill="#a7f3d0">-1</text>
  </g>
  <text x="42" y="365" font-family="ui-sans-serif, system-ui" font-size="24" fill="#f8fafc">Parent edges prove attainability; edge inequalities prove optimality.</text>
</svg>
'''
write_svg("sssp-certificate.svg", sssp_svg)

maxflow_svg = r'''
<svg xmlns="http://www.w3.org/2000/svg" width="860" height="420" viewBox="0 0 860 420" role="img" aria-labelledby="title desc">
  <title id="title">Max-flow min-cut certificate diagram</title>
  <desc id="desc">A feasible flow and an equal-value s-t cut certify maximum-flow optimality.</desc>
  <defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="#94a3b8"/></marker></defs>
  <rect width="860" height="420" rx="24" fill="#0b1020"/>
  <rect x="70" y="60" width="330" height="260" rx="26" fill="#052e2b" stroke="#10b981" stroke-width="3" stroke-dasharray="10 8"/>
  <text x="96" y="98" font-family="ui-sans-serif, system-ui" font-size="24" fill="#a7f3d0" font-weight="800">cut S</text>
  <g stroke="#94a3b8" stroke-width="5" fill="none" marker-end="url(#arrow)">
    <path d="M190 210 L340 130"/>
    <path d="M190 210 L340 290"/>
    <path d="M340 130 L620 210" stroke="#fbbf24"/>
    <path d="M340 290 L620 210" stroke="#fbbf24"/>
    <path d="M340 130 L340 290"/>
  </g>
  <g fill="#ecfdf5" stroke="#10b981" stroke-width="5">
    <circle cx="190" cy="210" r="40"/>
    <circle cx="340" cy="130" r="40"/>
    <circle cx="340" cy="290" r="40"/>
    <circle cx="620" cy="210" r="40"/>
  </g>
  <g font-family="ui-sans-serif, system-ui" font-size="26" font-weight="800" fill="#0f172a" stroke="none" text-anchor="middle" dominant-baseline="middle">
    <text x="190" y="210">s</text>
    <text x="340" y="130">a</text>
    <text x="340" y="290">b</text>
    <text x="620" y="210">t</text>
  </g>
  <text x="450" y="118" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="21" fill="#fde68a">cut capacity = flow value</text>
  <text x="70" y="365" font-family="ui-sans-serif, system-ui" font-size="24" fill="#f8fafc">Feasible flow + equal s-t cut certifies optimality.</text>
</svg>
'''
write_svg("maxflow-certificate.svg", maxflow_svg)


def load_font(paths: list[str], size: int) -> ImageFont.ImageFont:
    for p in paths:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


font_bold_paths = [
    "/usr/share/fonts/opentype/inter/Inter-Bold.otf",
    "/usr/share/fonts/truetype/lato/Lato-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
font_regular_paths = [
    "/usr/share/fonts/opentype/inter/Inter-Regular.otf",
    "/usr/share/fonts/truetype/lato/Lato-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]
mono_paths = ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"]
font_big = load_font(font_bold_paths, 98)
font_med = load_font(font_bold_paths, 42)
font_reg = load_font(font_regular_paths, 30)
font_mono = load_font(mono_paths, 30)
font_mono_small = load_font(mono_paths, 26)

# Social preview PNG, 1280x640.
W, H = 1280, 640
img = Image.new("RGB", (W, H), "#0b1020")
d = ImageDraw.Draw(img)
for y in range(H):
    r = int(9 + 20 * y / H)
    g = int(14 + 12 * y / H)
    b = int(28 + 48 * y / H)
    d.line([(0, y), (W, y)], fill=(r, g, b))
# Subtle graph motif kept away from the main text.
nodes = [(1040, 85), (1160, 120), (1205, 230), (1125, 300), (1005, 245), (980, 150)]
for a, b in [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (0, 4)]:
    d.line([nodes[a], nodes[b]], fill=(76, 44, 142), width=4)
for x, y in nodes:
    d.ellipse((x - 15, y - 15, x + 15, y + 15), fill=(20, 32, 54), outline=(74, 242, 166), width=4)
# Shield/logo at left.
shield = [(135, 105), (242, 150), (242, 258), (188, 318), (135, 340), (82, 318), (28, 258), (28, 150)]
d.polygon(shield, fill=(16, 185, 129), outline=(167, 243, 208))
d.line([(86, 235), (122, 271), (194, 178)], fill=(248, 250, 252), width=16)
# Copy.
d.text((300, 105), "CertiGraph", font=font_big, fill=(248, 250, 252))
d.text((306, 240), "Proof-carrying graph results", font=font_med, fill=(167, 243, 208))
d.text((308, 308), "Do not trust the solver. Verify the result.", font=font_reg, fill=(203, 213, 225))
# Terminal card.
d.rounded_rectangle((308, 386, 1000, 506), radius=18, fill=(15, 23, 42), outline=(51, 65, 85), width=2)
d.text((336, 414), "$ certigraph verify result.json", font=font_mono, fill=(134, 239, 172))
d.text((336, 456), "✓ accepted: certificate valid", font=font_mono_small, fill=(167, 243, 208))
d.rounded_rectangle((1018, 406, 1188, 486), radius=24, fill=(6, 78, 59), outline=(74, 242, 166), width=3)
d.text((1060, 430), "OK", font=font_med, fill=(236, 253, 245))
img.save(DOC_ASSETS / "social-preview.png", optimize=True)

# Small animated GIF for social posts / docs.
frames = []
commands = [
    "$ certigraph verify sssp bad.json",
    "✗ rejected: edge relaxation improves distance",
    "$ certigraph verify sssp good.json",
    "✓ accepted: valid SSSP certificate",
]
for i in range(1, len(commands) + 1):
    frame = Image.new("RGB", (900, 420), "#020617")
    dr = ImageDraw.Draw(frame)
    dr.rounded_rectangle((20, 20, 880, 400), radius=20, fill="#0f172a", outline="#334155", width=2)
    dr.ellipse((45, 43, 61, 59), fill="#ef4444")
    dr.ellipse((74, 43, 90, 59), fill="#f59e0b")
    dr.ellipse((103, 43, 119, 59), fill="#22c55e")
    y = 105
    for line in commands[:i]:
        fill = "#93c5fd" if line.startswith("$") else ("#fca5a5" if line.startswith("✗") else "#86efac")
        dr.text((58, y), line, font=font_mono_small, fill=fill)
        y += 64
    frames.append(frame)
frames[0].save(DOC_ASSETS / "terminal-demo.gif", save_all=True, append_images=frames[1:], duration=850, loop=0, optimize=True)

# Keep root-level assets in sync for repository settings and quick browsing.
for name in ["certigraph-logo.svg", "certigraph-icon.svg", "social-preview.png"]:
    shutil.copy2(DOC_ASSETS / name, ROOT_ASSETS / name)

print(f"Wrote assets to {DOC_ASSETS} and synced root assets to {ROOT_ASSETS}")
