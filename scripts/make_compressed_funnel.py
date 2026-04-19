# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "matplotlib>=3.8",
#   "numpy>=1.26",
# ]
# ///
"""Render traditional vs short-form compressed funnel comparison.

§1.1.3 '압축 구매 퍼널(compressed funnel)' 개념을 두 퍼널의 시각적
비교로 설명한다. 왼쪽은 전통 다단계 퍼널, 오른쪽은 숏폼 내 완결되는
압축 퍼널.

Run:
    uv run scripts/make_compressed_funnel.py

Output:
    assets/diagrams/compressed_funnel.png
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyBboxPatch


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


def draw_funnel_stage(ax, cx, top_y, bottom_y, top_w, bottom_w, color,
                      stage_label, stage_value, text_color="white"):
    """Draw a trapezoid section of a funnel."""
    pts = [
        (cx - top_w / 2, top_y),
        (cx + top_w / 2, top_y),
        (cx + bottom_w / 2, bottom_y),
        (cx - bottom_w / 2, bottom_y),
    ]
    poly = Polygon(pts, closed=True, facecolor=color,
                   edgecolor="white", linewidth=2, zorder=2)
    ax.add_patch(poly)
    mid_y = (top_y + bottom_y) / 2
    ax.text(cx, mid_y + 0.25, stage_label,
            ha="center", va="center",
            fontsize=12, fontweight="bold",
            color=text_color, zorder=3)
    ax.text(cx, mid_y - 0.22, stage_value,
            ha="center", va="center",
            fontsize=9, color=text_color, alpha=0.9, zorder=3)


def main() -> None:
    font = pick_korean_font()
    plt.rcParams["font.family"] = font
    plt.rcParams["axes.unicode_minus"] = False

    fig, ax = plt.subplots(figsize=(14, 9), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    # --- Left: Traditional multi-stage funnel ---
    left_cx = -3.8
    trad_stages = [
        ("상품 발견",         "포털 검색 · 광고 클릭",       "#93C5FD", 5.5),
        ("상품 정보 확인",     "쇼핑몰 상세 페이지",          "#60A5FA", 3.5),
        ("비교·검증",          "리뷰 · 커뮤니티 탐색",        "#3B82F6", 1.5),
        ("결제",              "장바구니 → 결제 완료",         "#1E3A8A", -0.5),
    ]

    top_y = 6.0
    widths = [5.4, 5.0, 4.6, 4.4, 4.4]
    for i, (label, value, color, _) in enumerate(trad_stages):
        draw_funnel_stage(
            ax, left_cx,
            top_y=top_y - i * 1.5,
            bottom_y=top_y - (i + 1) * 1.5,
            top_w=widths[i],
            bottom_w=widths[i + 1],
            color=color,
            stage_label=label,
            stage_value=value,
        )

    ax.text(left_cx, 6.7, "전통 이커머스 퍼널",
            ha="center", va="center",
            fontsize=15, fontweight="bold",
            color="#0F172A")
    ax.text(left_cx, -1.0, "수 분 ~ 수 시간",
            ha="center", va="center",
            fontsize=13, fontweight="bold",
            color="#1E3A8A",
            bbox=dict(boxstyle="round,pad=0.4",
                      facecolor="#EFF6FF",
                      edgecolor="#1E3A8A",
                      linewidth=1.3))
    ax.text(left_cx, -1.9, "소비자가 여러 단계에서 '검증'할 수 있다",
            ha="center", va="center",
            fontsize=10, color="#64748B", style="italic")

    # --- Right: Compressed single-stage "funnel" ---
    right_cx = 3.8

    ax.text(right_cx, 6.7, "숏폼 이커머스 퍼널 (압축)",
            ha="center", va="center",
            fontsize=15, fontweight="bold",
            color="#BE185D")

    # Phone-like single rounded box
    phone = FancyBboxPatch(
        (right_cx - 2.2, -0.5),
        4.4, 6.0,
        boxstyle="round,pad=0.06,rounding_size=0.4",
        facecolor="#BE185D",
        edgecolor="#9D174D",
        linewidth=2.5,
        zorder=2,
    )
    ax.add_patch(phone)

    stages_right = [
        ("인지",   "영상 자동재생"),
        ("관심",   "15~60초 자막·연출"),
        ("결정",   "효능 주장·긴박감 조성"),
        ("결제",   "커머스 핀 · in-bio · 바로결제"),
    ]
    for i, (label, value) in enumerate(stages_right):
        y = 5.1 - i * 1.35
        ax.text(right_cx - 1.85, y + 0.15,
                f"• {label}",
                ha="left", va="center",
                fontsize=12, fontweight="bold",
                color="white", zorder=3)
        ax.text(right_cx - 1.85, y - 0.28,
                value,
                ha="left", va="center",
                fontsize=10, color="#FCE7F3", zorder=3)

    # Label inside bottom
    ax.text(right_cx, 0.2,
            "→ 한 영상 안에서 모두 완결",
            ha="center", va="center",
            fontsize=11, fontweight="bold", style="italic",
            color="white", zorder=3)

    ax.text(right_cx, -1.0, "수 초 ~ 수 분",
            ha="center", va="center",
            fontsize=13, fontweight="bold",
            color="#BE185D",
            bbox=dict(boxstyle="round,pad=0.4",
                      facecolor="#FCE7F3",
                      edgecolor="#BE185D",
                      linewidth=1.3))
    ax.text(right_cx, -1.9, "검증 단계가 사실상 사라진다",
            ha="center", va="center",
            fontsize=10, color="#64748B", style="italic")

    # --- Center compression arrow ---
    ax.annotate(
        "",
        xy=(right_cx - 2.6, 3.0),
        xytext=(left_cx + 2.6, 3.0),
        arrowprops=dict(arrowstyle="-|>", color="#B45309", lw=3.5,
                        mutation_scale=26),
        zorder=3,
    )
    ax.text(
        0, 3.5,
        "압축",
        ha="center", va="center",
        fontsize=16, fontweight="bold",
        color="#B45309",
        bbox=dict(boxstyle="round,pad=0.4",
                  facecolor="#FEF3C7",
                  edgecolor="#B45309", linewidth=1.8),
        zorder=4,
    )

    # Title
    ax.text(0, 7.6,
            "전통 vs 숏폼 — '압축 구매 퍼널' 비교",
            ha="center", va="center",
            fontsize=17, fontweight="bold",
            color="#0F172A")

    ax.set_xlim(-8, 8)
    ax.set_ylim(-2.7, 8.2)
    ax.set_aspect("equal")
    ax.axis("off")

    out_path = (
        Path(__file__).resolve().parents[1]
        / "assets" / "diagrams" / "compressed_funnel.png"
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
