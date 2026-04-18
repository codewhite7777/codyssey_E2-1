# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "matplotlib>=3.8",
#   "numpy>=1.26",
# ]
# ///
"""Render Korean e-commerce annual transaction growth bar chart (2019-2025).

Source:
    통계청 「온라인쇼핑동향」 연간 보도자료 (2019~2025)
    https://kostat.go.kr/  (각 연도 12월 및 연간 발표)

Run:
    uv run scripts/make_ecommerce_growth.py

Output:
    assets/diagrams/ecommerce_growth.png
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

    years = ["2019", "2020", "2021", "2022", "2023", "2024", "2025"]
    values = [134.6, 161.1, 187.1, 206.5, 227.3, 259.0, 272.0]  # 단위: 조 원

    # 시간 흐름을 표현하는 블루 그라데이션 (soft → strong)
    colors = [
        "#BFDBFE", "#93C5FD", "#60A5FA",
        "#3B82F6", "#2563EB", "#1D4ED8", "#1E3A8A",
    ]

    fig, ax = plt.subplots(figsize=(13, 6.8), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    bars = ax.bar(
        years, values,
        color=colors,
        edgecolor="white", linewidth=1.6,
        width=0.62,
        zorder=3,
    )

    max_val = max(values)
    ax.set_ylim(0, max_val * 1.25)

    for i, (bar, v) in enumerate(zip(bars, values)):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            v + max_val * 0.015,
            f"{v:,.1f}조",
            ha="center", va="bottom",
            fontsize=12, fontweight="bold",
            color="#0F172A",
        )

        if i == 0:
            continue
        yoy = (values[i] - values[i - 1]) / values[i - 1] * 100
        accent = "#059669" if yoy >= 10 else ("#F59E0B" if yoy >= 5 else "#DC2626")
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            v + max_val * 0.085,
            f"▲ {yoy:.1f}%",
            ha="center", va="bottom",
            fontsize=10, fontweight="bold",
            color=accent,
        )

    # 코로나19 기간 강조
    ax.annotate(
        "COVID-19 비대면 소비 급증\n(2020~2021)",
        xy=(1.5, 175),
        xytext=(0.7, 280),
        ha="center", va="center",
        fontsize=10,
        color="#B91C1C",
        fontweight="bold",
        arrowprops=dict(
            arrowstyle="-|>",
            color="#B91C1C",
            connectionstyle="arc3,rad=0.25",
            lw=1.4,
        ),
    )

    # 성숙기 진입 주석
    ax.annotate(
        "성숙기 진입\n성장 둔화",
        xy=(6, 272),
        xytext=(6.5, 320),
        ha="center", va="center",
        fontsize=10,
        color="#1E3A8A",
        fontweight="bold",
        arrowprops=dict(
            arrowstyle="-|>",
            color="#1E3A8A",
            connectionstyle="arc3,rad=-0.2",
            lw=1.4,
        ),
    )

    ax.set_title(
        "국내 온라인쇼핑 연간 거래액 추이 (2019–2025)",
        fontsize=17, fontweight="bold",
        color="#0F172A", pad=18,
    )
    ax.set_ylabel("거래액 (조 원)", fontsize=11, color="#475569", labelpad=10)
    ax.tick_params(axis="both", colors="#334155", labelsize=11)

    ax.yaxis.grid(True, linestyle="--", alpha=0.4, zorder=1)
    ax.set_axisbelow(True)

    for spine_name in ("top", "right"):
        ax.spines[spine_name].set_visible(False)
    ax.spines["left"].set_color("#CBD5E1")
    ax.spines["bottom"].set_color("#CBD5E1")

    fig.text(
        0.5, 0.02,
        "출처: 통계청 「온라인쇼핑동향」 연간 보도자료 (2019~2025)",
        ha="center", va="center",
        fontsize=9, color="#64748B",
    )

    out_path = (
        Path(__file__).resolve().parents[1]
        / "assets" / "diagrams" / "ecommerce_growth.png"
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
