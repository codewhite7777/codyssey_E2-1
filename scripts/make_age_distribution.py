# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "matplotlib>=3.8",
#   "numpy>=1.26",
# ]
# ///
"""Render age-wise distribution of 'YouTube as primary source for news & current affairs'.

Source (primary, WebFetch 직접 확인):
    한국언론진흥재단 「2024 소셜미디어 이용자 조사」 (2024년 10~11월,
    만 19세 이상 3,000명 대면 방문조사) — 뉴스·시사정보 1순위
    소셜미디어로 유튜브 선택 비율.
    19~29세 31.4% · 30대 39.9% · 40대 52.8% · 50대 70.0%
    · 60대 82.6% · 70대 이상 93.1%

Run:
    uv run scripts/make_age_distribution.py

Output:
    assets/diagrams/news_youtube_by_age.png
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt


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

    ages = ["19~29세", "30대", "40대", "50대", "60대", "70대 이상"]
    values = [31.4, 39.9, 52.8, 70.0, 82.6, 93.1]
    colors = ["#BFDBFE", "#93C5FD", "#60A5FA", "#3B82F6", "#1D4ED8", "#1E3A8A"]

    fig, ax = plt.subplots(figsize=(13, 7), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    bars = ax.bar(
        ages,
        values,
        color=colors,
        edgecolor="white",
        linewidth=1.6,
        width=0.62,
        zorder=3,
    )

    max_val = 100
    ax.set_ylim(0, max_val * 1.15)

    for bar, v in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            v + 1.8,
            f"{v}%",
            ha="center",
            va="bottom",
            fontsize=13,
            fontweight="bold",
            color="#0F172A",
        )

    # Trend arrow — 19~29세 -> 70대 이상 gap
    ax.annotate(
        "",
        xy=(5.05, 95),
        xytext=(0.15, 36),
        arrowprops=dict(
            arrowstyle="-|>",
            color="#059669",
            lw=2.2,
            connectionstyle="arc3,rad=-0.15",
            mutation_scale=20,
        ),
        zorder=2,
    )
    ax.text(
        2.5,
        85,
        "연령 상승 → +61.7%p",
        ha="center",
        va="center",
        fontsize=13,
        fontweight="bold",
        color="#059669",
        bbox=dict(
            boxstyle="round,pad=0.4",
            facecolor="white",
            edgecolor="#10B981",
            linewidth=1.3,
        ),
        zorder=4,
    )

    ax.set_title(
        "뉴스·시사 정보를 유튜브로 얻는 비율 — 연령이 올라갈수록 급상승",
        fontsize=15,
        fontweight="bold",
        color="#0F172A",
        pad=18,
    )
    ax.set_ylabel(
        "1순위 소셜미디어로 유튜브 선택 (%)",
        fontsize=11,
        color="#475569",
        labelpad=10,
    )
    ax.tick_params(axis="both", colors="#334155", labelsize=11)

    ax.yaxis.grid(True, linestyle="--", alpha=0.4, zorder=1)
    ax.set_axisbelow(True)

    for spine_name in ("top", "right"):
        ax.spines[spine_name].set_visible(False)
    ax.spines["left"].set_color("#CBD5E1")
    ax.spines["bottom"].set_color("#CBD5E1")

    fig.text(
        0.5,
        0.02,
        "출처: 한국언론진흥재단 「2024 소셜미디어 이용자 조사」 (2024년 10~11월, 만 19세 이상 3,000명 대면 방문조사)",
        ha="center",
        va="center",
        fontsize=9,
        color="#64748B",
    )

    out_path = (
        Path(__file__).resolve().parents[1]
        / "assets" / "diagrams" / "news_youtube_by_age.png"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, facecolor="white", bbox_inches="tight", pad_inches=0.35)
    plt.close(fig)
    print(
        f"saved: {out_path.relative_to(Path.cwd())}  "
        f"({out_path.stat().st_size / 1024:.0f} KB)  font={font}"
    )


if __name__ == "__main__":
    main()
