# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "matplotlib>=3.8",
#   "numpy>=1.26",
# ]
# ///
"""Render e-commerce value chain (L1~L11) with project-scope layers highlighted.

본 프로젝트는 11개 레이어 가치사슬 중 L4(광고·마케팅)와 L6(의사결정 지원)에
개입한다. 본 다이어그램은 그 개입 좌표를 시각화한다.

Run:
    uv run scripts/make_value_chain.py

Output:
    assets/diagrams/value_chain_scope.png
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


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

    layers = [
        ("L1", "상품\n소싱·기획"),
        ("L2", "등록·\n콘텐츠"),
        ("L3", "검색·노출·\n랭킹"),
        ("L4", "광고·\n마케팅"),
        ("L5", "개인화\n추천"),
        ("L6", "의사결정\n지원"),
        ("L7", "결제·\n금융"),
        ("L8", "재고·\n풀필먼트"),
        ("L9", "배송·\n라스트마일"),
        ("L10", "CS·반품·\n교환"),
        ("L11", "리뷰·\n재구매"),
    ]
    focus_indices = {3, 5}  # L4, L6 (0-indexed)
    focus_colors = {3: "#7C3AED", 5: "#DB2777"}  # violet, pink
    focus_callouts = {
        3: "AI 광고 분석\n(허위·과장 탐지)",
        5: "소비자 판별 지원\n(리포트 제공)",
    }

    n = len(layers)
    box_w = 1.4
    box_h = 1.3
    gap = 0.22
    total_w = n * box_w + (n - 1) * gap
    x_start = 0

    fig, ax = plt.subplots(figsize=(17, 6.2), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    for i, (code, name) in enumerate(layers):
        x = x_start + i * (box_w + gap)
        is_focus = i in focus_indices

        if is_focus:
            face = focus_colors[i]
            edge = face
            code_color = "white"
            name_color = "white"
            lw = 2.6
        else:
            face = "#F1F5F9"
            edge = "#CBD5E1"
            code_color = "#64748B"
            name_color = "#475569"
            lw = 1.0

        box = FancyBboxPatch(
            (x, -box_h / 2),
            box_w,
            box_h,
            boxstyle="round,pad=0.02,rounding_size=0.14",
            facecolor=face,
            edgecolor=edge,
            linewidth=lw,
            zorder=2,
        )
        ax.add_patch(box)

        ax.text(
            x + box_w / 2,
            box_h / 2 - 0.28,
            code,
            ha="center",
            va="center",
            fontsize=14,
            fontweight="bold",
            color=code_color,
            zorder=3,
        )
        ax.text(
            x + box_w / 2,
            -0.18,
            name,
            ha="center",
            va="center",
            fontsize=10,
            color=name_color,
            zorder=3,
        )

        if i < n - 1:
            arrow_start = x + box_w + 0.03
            arrow_end = x + box_w + gap - 0.03
            ax.annotate(
                "",
                xy=(arrow_end, 0),
                xytext=(arrow_start, 0),
                arrowprops=dict(arrowstyle="->", color="#94A3B8", lw=1.5),
                zorder=1,
            )

    for i in focus_indices:
        x = x_start + i * (box_w + gap) + box_w / 2
        color = focus_colors[i]
        callout = focus_callouts[i]

        ax.annotate(
            callout,
            xy=(x, -box_h / 2 - 0.02),
            xytext=(x, -box_h / 2 - 1.05),
            ha="center",
            va="center",
            fontsize=11,
            fontweight="bold",
            color=color,
            arrowprops=dict(
                arrowstyle="-|>",
                color=color,
                lw=1.8,
                connectionstyle="arc3,rad=0.0",
            ),
            bbox=dict(
                boxstyle="round,pad=0.45",
                facecolor="white",
                edgecolor=color,
                linewidth=1.4,
            ),
            zorder=4,
        )

    ax.text(
        x_start + total_w / 2,
        box_h / 2 + 0.55,
        "이커머스 가치사슬 11개 레이어 — 본 프로젝트 개입 영역 (L4 × L6)",
        ha="center",
        va="center",
        fontsize=16,
        fontweight="bold",
        color="#0F172A",
    )

    ax.text(
        x_start + total_w / 2,
        -box_h / 2 - 2.0,
        "본 프로젝트는 L4(광고·마케팅)에서 허위·과장 광고를 포착하고, "
        "L6(의사결정 지원) 지점에서 소비자에게 판별 근거를 제공한다.",
        ha="center",
        va="center",
        fontsize=11,
        color="#334155",
        style="italic",
    )

    ax.set_xlim(x_start - 0.5, x_start + total_w + 0.5)
    ax.set_ylim(-box_h / 2 - 2.4, box_h / 2 + 1.1)
    ax.set_aspect("auto")
    ax.axis("off")

    out_path = (
        Path(__file__).resolve().parents[1]
        / "assets" / "diagrams" / "value_chain_scope.png"
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
