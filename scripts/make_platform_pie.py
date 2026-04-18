# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "matplotlib>=3.8",
#   "numpy>=1.26",
# ]
# ///
"""Render 2024 SNS 뒷광고 platform distribution donut chart.

Source:
    공정거래위원회 「2024년 SNS 부당광고(뒷광고) 모니터링 결과 발표」(2025-03-16)
    https://www.korea.kr/briefing/pressReleaseView.do?newsId=156679064

Run:
    uv run scripts/make_platform_pie.py

Output:
    assets/diagrams/platform_distribution_2024.png
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np


KOREAN_FONT_CANDIDATES = (
    "Apple SD Gothic Neo",
    "AppleSDGothicNeo",
    "AppleGothic",
    "Noto Sans CJK KR",
    "Noto Sans KR",
    "NanumGothic",
    "Nanum Gothic",
    "Malgun Gothic",
)


def pick_korean_font() -> str:
    available = {f.name for f in fm.fontManager.ttflist}
    for name in KOREAN_FONT_CANDIDATES:
        if name in available:
            return name
    return "DejaVu Sans"


def main() -> None:
    font = pick_korean_font()
    plt.rcParams["font.family"] = font
    plt.rcParams["axes.unicode_minus"] = False

    labels = ["인스타그램", "네이버 블로그", "유튜브", "기타\n(틱톡 · 네이버 카페 등)"]
    sizes = [10195, 9423, 1409, 984]
    colors = ["#7C3AED", "#F97316", "#DB2777", "#2563EB"]
    total = sum(sizes)

    fig, ax = plt.subplots(figsize=(13, 7.5), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    wedges, _ = ax.pie(
        sizes,
        colors=colors,
        startangle=90,
        counterclock=False,
        wedgeprops=dict(width=0.38, edgecolor="white", linewidth=3),
    )

    centre = plt.Circle(
        (0, 0),
        0.54,
        facecolor="#1E293B",
        edgecolor="white",
        linewidth=2,
        zorder=5,
    )
    ax.add_artist(centre)
    ax.text(
        0, 0.10,
        f"{total:,}",
        ha="center", va="center",
        fontsize=26, fontweight="bold",
        color="white",
        zorder=6,
    )
    ax.text(
        0, -0.05,
        "건",
        ha="center", va="center",
        fontsize=13,
        color="#CBD5E1",
        zorder=6,
    )
    ax.text(
        0, -0.22,
        "2024 총 적발",
        ha="center", va="center",
        fontsize=10,
        color="#94A3B8",
        zorder=6,
    )

    for i, wedge in enumerate(wedges):
        theta = np.deg2rad((wedge.theta1 + wedge.theta2) / 2)
        x = np.cos(theta)
        y = np.sin(theta)
        anchor = (x * 0.82, y * 0.82)
        elbow = (x * 1.15, y * 1.15)
        label_x = 1.55 if x >= 0 else -1.55
        horiz_align = "left" if x >= 0 else "right"

        ax.plot(
            [anchor[0], elbow[0], label_x],
            [anchor[1], elbow[1], elbow[1]],
            color=colors[i],
            linewidth=1.6,
            solid_capstyle="round",
            zorder=3,
        )
        ax.plot(
            label_x, elbow[1],
            marker="o", markersize=6,
            color=colors[i], zorder=4,
        )

        pct = sizes[i] / total * 100
        ax.text(
            label_x + (0.04 if x >= 0 else -0.04),
            elbow[1] + 0.08,
            labels[i],
            ha=horiz_align, va="bottom",
            fontsize=12, fontweight="bold",
            color="#0F172A",
            zorder=5,
        )
        ax.text(
            label_x + (0.04 if x >= 0 else -0.04),
            elbow[1] - 0.06,
            f"{sizes[i]:,}건  ·  {pct:.1f}%",
            ha=horiz_align, va="top",
            fontsize=11,
            color=colors[i],
            fontweight="semibold" if hasattr(plt, "semibold") else "bold",
            zorder=5,
        )

    ax.set_title(
        "2024년 SNS 뒷광고 의심 게시물 플랫폼별 분포",
        fontsize=17, fontweight="bold",
        color="#0F172A",
        pad=24,
    )
    ax.text(
        0, -1.55,
        "출처: 공정거래위원회 「2024년 SNS 부당광고(뒷광고) 모니터링 결과」 (2025-03-16)",
        ha="center", va="center",
        fontsize=9, color="#64748B",
    )

    ax.set_xlim(-2.15, 2.15)
    ax.set_ylim(-1.75, 1.45)
    ax.set_aspect("equal")
    ax.axis("off")

    out_path = (
        Path(__file__).resolve().parents[1]
        / "assets" / "diagrams" / "platform_distribution_2024.png"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        out_path,
        facecolor="white",
        bbox_inches="tight",
        pad_inches=0.35,
    )
    plt.close(fig)
    print(f"saved: {out_path.relative_to(Path.cwd())}  ({out_path.stat().st_size / 1024:.0f} KB)  font={font}")


if __name__ == "__main__":
    main()
