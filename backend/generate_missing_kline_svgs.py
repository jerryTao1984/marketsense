"""
Generate fallback SVG assets for K-line question images that are referenced by the
database seed data but were never committed to the repository.

The goal is not photorealism; it is to guarantee that every referenced asset exists
and conveys the intended pattern well enough for quiz usage in Docker deployments.
"""
from __future__ import annotations

from pathlib import Path


CANVAS_W = 240
CANVAS_H = 320


def svg_doc(body: str) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_W} {CANVAS_H}" width="{CANVAS_W}" height="{CANVAS_H}">
  <rect width="100%" height="100%" fill="#ffffff"/>
  <rect x="1" y="1" width="{CANVAS_W-2}" height="{CANVAS_H-2}" rx="20" fill="#f8fafc" stroke="#e2e8f0"/>
  <line x1="24" y1="36" x2="24" y2="248" stroke="#cbd5e1" stroke-width="1"/>
  <line x1="24" y1="248" x2="216" y2="248" stroke="#cbd5e1" stroke-width="1"/>
{body}
</svg>
"""


def candle(cx: int, open_y: int, close_y: int, high_y: int, low_y: int, width: int = 22) -> str:
    rising = close_y < open_y
    color = "#ef4444" if rising else "#22c55e"
    top = min(open_y, close_y)
    height = max(abs(close_y - open_y), 4)
    rect_y = top if abs(close_y - open_y) >= 4 else top - 2
    return (
        f'  <line x1="{cx}" y1="{high_y}" x2="{cx}" y2="{low_y}" stroke="{color}" stroke-width="4" stroke-linecap="round"/>\n'
        f'  <rect x="{cx-width//2}" y="{rect_y}" width="{width}" height="{height}" rx="3" fill="{color}" opacity="0.92"/>'
    )


def polyline(points: list[tuple[int, int]], color: str = "#2563eb", width: int = 6, dashed: bool = False) -> str:
    pts = " ".join(f"{x},{y}" for x, y in points)
    extra = ' stroke-dasharray="8 8"' if dashed else ""
    return f'  <polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"{extra}/>'


def bars(values: list[int], color: str) -> str:
    parts = []
    x = 42
    for v in values:
        parts.append(f'  <rect x="{x}" y="{292-v}" width="12" height="{v}" rx="3" fill="{color}" opacity="0.85"/>')
        x += 20
    return "\n".join(parts)


def single(pattern: str) -> str:
    configs = {
        "hammer2.svg": [(120, 132, 148, 126, 236)],
        "inverse-hammer.svg": [(120, 170, 154, 58, 192)],
        "t-line.svg": [(120, 144, 144, 144, 236)],
        "limit-line.svg": [(120, 164, 164, 164, 164)],
    }
    body = "\n".join(candle(*cfg) for cfg in configs[pattern])
    return svg_doc(body)


def multi_candles(pattern: str) -> str:
    configs = {
        "bullish-engulf.svg": [(88, 118, 176, 104, 194, 20), (140, 186, 96, 82, 202, 28)],
        "bearish-engulf.svg": [(88, 186, 104, 92, 202, 20), (140, 94, 184, 80, 200, 28)],
        "three-crows.svg": [(76, 104, 156, 92, 176, 18), (120, 120, 188, 108, 206, 18), (164, 140, 216, 128, 236, 18)],
        "three-soldiers.svg": [(76, 188, 132, 118, 202, 18), (120, 170, 108, 96, 184, 18), (164, 148, 84, 70, 160, 18)],
        "evening-star.svg": [(74, 184, 108, 96, 198, 18), (120, 96, 100, 80, 124, 14), (166, 112, 188, 98, 206, 22)],
        "morning-star.svg": [(74, 112, 186, 98, 202, 18), (120, 104, 100, 82, 122, 14), (166, 186, 112, 96, 202, 22)],
        "rising-three.svg": [(56, 194, 96, 84, 212, 20), (96, 118, 154, 108, 170, 14), (124, 126, 162, 116, 176, 14), (152, 132, 168, 120, 184, 14), (188, 178, 74, 62, 196, 22)],
        "falling-three.svg": [(56, 94, 198, 80, 214, 20), (96, 176, 142, 132, 190, 14), (124, 168, 136, 126, 184, 14), (152, 162, 130, 120, 178, 14), (188, 120, 216, 108, 232, 22)],
        "piercing.svg": [(88, 92, 194, 80, 210, 22), (144, 214, 136, 122, 226, 22)],
        "dark-cloud.svg": [(88, 196, 88, 74, 212, 22), (144, 72, 152, 58, 198, 22)],
    }
    body = "\n".join(candle(*cfg[:-1], width=cfg[-1]) for cfg in configs[pattern])
    return svg_doc(body)


def line_pattern(pattern: str) -> str:
    specs = {
        "head-shoulder.svg": {
            "line": [(42, 188), (70, 134), (100, 186), (124, 88), (152, 184), (180, 136), (206, 200)],
            "guides": ['  <line x1="42" y1="204" x2="206" y2="192" stroke="#94a3b8" stroke-width="3" stroke-dasharray="6 6"/>'],
        },
        "head-shoulder-bottom.svg": {
            "line": [(42, 110), (70, 176), (98, 116), (124, 226), (154, 118), (180, 176), (206, 106)],
            "guides": ['  <line x1="42" y1="118" x2="206" y2="126" stroke="#94a3b8" stroke-width="3" stroke-dasharray="6 6"/>'],
        },
        "double-top.svg": {
            "line": [(42, 200), (80, 114), (118, 182), (156, 116), (194, 204)],
            "guides": ['  <line x1="42" y1="182" x2="194" y2="182" stroke="#94a3b8" stroke-width="3" stroke-dasharray="6 6"/>'],
        },
        "double-bottom.svg": {
            "line": [(42, 118), (78, 206), (118, 132), (156, 210), (194, 116)],
            "guides": ['  <line x1="42" y1="132" x2="194" y2="132" stroke="#94a3b8" stroke-width="3" stroke-dasharray="6 6"/>'],
        },
        "sym-triangle.svg": {
            "line": [(54, 156), (82, 130), (108, 150), (132, 138), (156, 146), (184, 142)],
            "guides": [
                '  <line x1="44" y1="106" x2="188" y2="150" stroke="#94a3b8" stroke-width="3"/>',
                '  <line x1="44" y1="198" x2="188" y2="150" stroke="#94a3b8" stroke-width="3"/>',
            ],
        },
        "bull-flag.svg": {
            "line": [(46, 218), (88, 100), (112, 118), (132, 138), (152, 158), (176, 144), (206, 88)],
            "guides": [
                '  <line x1="100" y1="110" x2="174" y2="140" stroke="#94a3b8" stroke-width="3"/>',
                '  <line x1="96" y1="146" x2="170" y2="176" stroke="#94a3b8" stroke-width="3"/>',
            ],
        },
        "asc-triangle.svg": {
            "line": [(44, 196), (76, 170), (108, 146), (142, 124), (176, 122), (204, 104)],
            "guides": [
                '  <line x1="54" y1="122" x2="202" y2="122" stroke="#94a3b8" stroke-width="3"/>',
                '  <line x1="54" y1="204" x2="202" y2="122" stroke="#94a3b8" stroke-width="3"/>',
            ],
        },
        "desc-triangle.svg": {
            "line": [(44, 118), (78, 140), (112, 166), (146, 182), (180, 178), (204, 210)],
            "guides": [
                '  <line x1="54" y1="180" x2="202" y2="180" stroke="#94a3b8" stroke-width="3"/>',
                '  <line x1="54" y1="102" x2="202" y2="180" stroke="#94a3b8" stroke-width="3"/>',
            ],
        },
        "falling-wedge.svg": {
            "line": [(50, 108), (80, 146), (108, 132), (136, 168), (164, 156), (194, 198)],
            "guides": [
                '  <line x1="48" y1="88" x2="196" y2="168" stroke="#94a3b8" stroke-width="3"/>',
                '  <line x1="48" y1="152" x2="196" y2="210" stroke="#94a3b8" stroke-width="3"/>',
            ],
        },
        "rounding.svg": {
            "line": [(44, 106), (70, 140), (96, 170), (122, 188), (148, 170), (174, 136), (202, 102)],
            "guides": [],
        },
    }
    spec = specs[pattern]
    body = "\n".join(spec["guides"] + [polyline(spec["line"], color="#0f172a")])
    return svg_doc(body)


def volume_pattern(pattern: str) -> str:
    specs = {
        "vol-divergence.svg": {
            "line": [(42, 174), (74, 164), (106, 146), (138, 128), (170, 114), (202, 102)],
            "bars": [64, 58, 50, 40, 30, 22],
            "bar_color": "#94a3b8",
        },
        "vol-confirm.svg": {
            "line": [(42, 190), (74, 178), (106, 156), (138, 130), (170, 110), (202, 86)],
            "bars": [18, 28, 38, 50, 62, 76],
            "bar_color": "#ef4444",
        },
        "vol-sell.svg": {
            "line": [(42, 96), (74, 110), (106, 134), (138, 160), (170, 186), (202, 212)],
            "bars": [18, 28, 42, 58, 70, 82],
            "bar_color": "#22c55e",
        },
        "vol-bottom.svg": {
            "line": [(42, 126), (74, 154), (106, 186), (138, 176), (170, 132), (202, 96)],
            "bars": [14, 18, 24, 32, 64, 74],
            "bar_color": "#ef4444",
        },
        "vol-peak.svg": {
            "line": [(42, 208), (74, 178), (106, 142), (138, 112), (170, 132), (202, 176)],
            "bars": [18, 32, 52, 80, 58, 30],
            "bar_color": "#ef4444",
        },
        "vol-pullback.svg": {
            "line": [(42, 206), (74, 176), (106, 132), (138, 144), (170, 152), (202, 138)],
            "bars": [56, 44, 38, 28, 20, 18],
            "bar_color": "#94a3b8",
        },
        "obv.svg": {
            "line": [(42, 170), (74, 168), (106, 164), (138, 156), (170, 146), (202, 126)],
            "bars": [20, 26, 30, 34, 42, 48],
            "bar_color": "#3b82f6",
        },
        "turnover.svg": {
            "line": [(42, 162), (74, 154), (106, 148), (138, 140), (170, 132), (202, 120)],
            "bars": [16, 18, 22, 72, 24, 20],
            "bar_color": "#f59e0b",
        },
    }
    spec = specs[pattern]
    body = "\n".join([
        polyline(spec["line"], color="#0f172a"),
        bars(spec["bars"], spec["bar_color"]),
    ])
    return svg_doc(body)


def build_svg(filename: str) -> str:
    if filename in {"hammer2.svg", "inverse-hammer.svg", "t-line.svg", "limit-line.svg"}:
        return single(filename)
    if filename in {
        "bullish-engulf.svg", "bearish-engulf.svg", "three-crows.svg", "three-soldiers.svg",
        "evening-star.svg", "morning-star.svg", "rising-three.svg", "falling-three.svg",
        "piercing.svg", "dark-cloud.svg",
    }:
        return multi_candles(filename)
    if filename in {
        "head-shoulder.svg", "head-shoulder-bottom.svg", "double-top.svg", "double-bottom.svg",
        "sym-triangle.svg", "bull-flag.svg", "asc-triangle.svg", "desc-triangle.svg",
        "falling-wedge.svg", "rounding.svg",
    }:
        return line_pattern(filename)
    if filename in {
        "vol-divergence.svg", "vol-confirm.svg", "vol-sell.svg", "vol-bottom.svg",
        "vol-peak.svg", "vol-pullback.svg", "obv.svg", "turnover.svg",
    }:
        return volume_pattern(filename)
    raise KeyError(filename)


MISSING_ASSETS = [
    "asc-triangle.svg",
    "bearish-engulf.svg",
    "bull-flag.svg",
    "bullish-engulf.svg",
    "dark-cloud.svg",
    "desc-triangle.svg",
    "double-bottom.svg",
    "double-top.svg",
    "evening-star.svg",
    "falling-three.svg",
    "falling-wedge.svg",
    "hammer2.svg",
    "head-shoulder-bottom.svg",
    "head-shoulder.svg",
    "inverse-hammer.svg",
    "limit-line.svg",
    "morning-star.svg",
    "obv.svg",
    "piercing.svg",
    "rising-three.svg",
    "rounding.svg",
    "sym-triangle.svg",
    "t-line.svg",
    "three-crows.svg",
    "three-soldiers.svg",
    "turnover.svg",
    "vol-bottom.svg",
    "vol-confirm.svg",
    "vol-divergence.svg",
    "vol-peak.svg",
    "vol-pullback.svg",
    "vol-sell.svg",
]


def main() -> None:
    current_dir = Path(__file__).resolve().parent
    output_dirs = [
        current_dir / "public" / "assets" / "kline",
        current_dir.parent / "public" / "assets" / "kline",
    ]
    output_dirs = [p for p in output_dirs if p.parent.parent.exists()]
    generated = 0

    for output_dir in output_dirs:
        output_dir.mkdir(parents=True, exist_ok=True)
        for filename in MISSING_ASSETS:
            target = output_dir / filename
            if target.exists():
                continue
            target.write_text(build_svg(filename), encoding="utf-8")
            generated += 1

    print(f"Generated {generated} missing SVG assets")


if __name__ == "__main__":
    main()
