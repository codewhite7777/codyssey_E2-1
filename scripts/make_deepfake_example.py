# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "matplotlib>=3.8",
#   "numpy>=1.26",
# ]
# ///
"""Render an illustrative mockup of an AI deepfake short-form ad with red-flag annotations.

실제 언론 보도된 AI 딥페이크 가짜 의사 광고 패턴을 저작권 문제 없이
재현한 교육용 mockup. 4가지 red flag 를 번호·설명으로 표시한다.

Run:
    uv run scripts/make_deepfake_example.py

Output:
    assets/diagrams/deepfake_example.png
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle


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

    fig, ax = plt.subplots(figsize=(15, 9), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    # --- Phone frame (left side) ---
    phone_x, phone_y = 0.5, 0.3
    phone_w, phone_h = 4.2, 7.8

    phone_outer = FancyBboxPatch(
        (phone_x, phone_y),
        phone_w, phone_h,
        boxstyle="round,pad=0.02,rounding_size=0.4",
        facecolor="#1F2937",
        edgecolor="#111827",
        linewidth=2,
        zorder=2,
    )
    ax.add_patch(phone_outer)

    # Screen
    screen_margin = 0.18
    screen = FancyBboxPatch(
        (phone_x + screen_margin, phone_y + 0.35),
        phone_w - 2 * screen_margin, phone_h - 0.7,
        boxstyle="round,pad=0.01,rounding_size=0.25",
        facecolor="#0F172A",
        edgecolor="none",
        zorder=3,
    )
    ax.add_patch(screen)

    # Status bar text
    ax.text(
        phone_x + phone_w / 2,
        phone_y + phone_h - 0.22,
        "● ● ●        오전 10:30        |||| 85%",
        ha="center", va="center",
        fontsize=9, color="#94A3B8",
        zorder=4,
    )

    # AI Avatar (circular placeholder)
    avatar_cx = phone_x + phone_w / 2
    avatar_cy = phone_y + phone_h - 1.7
    avatar = Circle(
        (avatar_cx, avatar_cy), 0.75,
        facecolor="#475569", edgecolor="#E11D48", linewidth=2.5,
        zorder=4,
    )
    ax.add_patch(avatar)
    ax.text(
        avatar_cx, avatar_cy + 0.10,
        "[AI 생성]",
        ha="center", va="center",
        fontsize=9, color="#FCA5A5", fontweight="bold",
        zorder=5,
    )
    ax.text(
        avatar_cx, avatar_cy - 0.25,
        "허구 인물",
        ha="center", va="center",
        fontsize=10, color="#FECACA",
        zorder=5,
    )

    # Fake credentials
    ax.text(
        avatar_cx, phone_y + phone_h - 3.05,
        "Dr. 박○○",
        ha="center", va="center",
        fontsize=15, fontweight="bold", color="white",
        zorder=4,
    )
    ax.text(
        avatar_cx, phone_y + phone_h - 3.45,
        '"S대 치과 전문의 · 20년 경력"',
        ha="center", va="center",
        fontsize=10, color="#FDE68A", style="italic",
        zorder=4,
    )

    # Main claim
    claim_box = FancyBboxPatch(
        (phone_x + 0.4, phone_y + phone_h - 4.8),
        phone_w - 0.8, 0.9,
        boxstyle="round,pad=0.02,rounding_size=0.1",
        facecolor="#FEF3C7", edgecolor="#F59E0B", linewidth=1.3,
        zorder=4,
    )
    ax.add_patch(claim_box)
    ax.text(
        avatar_cx, phone_y + phone_h - 4.20,
        "이 구강 유산균만 먹으면",
        ha="center", va="center",
        fontsize=10, color="#78350F",
        zorder=5,
    )
    ax.text(
        avatar_cx, phone_y + phone_h - 4.55,
        "단 2주 만에 치석 제거!",
        ha="center", va="center",
        fontsize=13, fontweight="bold", color="#B91C1C",
        zorder=5,
    )

    # Countdown / urgency
    urgency_box = FancyBboxPatch(
        (phone_x + 0.5, phone_y + phone_h - 5.85),
        phone_w - 1.0, 0.55,
        boxstyle="round,pad=0.02,rounding_size=0.1",
        facecolor="#DC2626", edgecolor="none",
        zorder=4,
    )
    ax.add_patch(urgency_box)
    ax.text(
        avatar_cx, phone_y + phone_h - 5.58,
        "[ 마감 임박 ]  오늘 자정까지  ·  50% 특가",
        ha="center", va="center",
        fontsize=11, fontweight="bold", color="white",
        zorder=5,
    )

    # CTA Button
    cta = FancyBboxPatch(
        (phone_x + 0.55, phone_y + phone_h - 6.75),
        phone_w - 1.1, 0.65,
        boxstyle="round,pad=0.03,rounding_size=0.3",
        facecolor="#10B981", edgecolor="none",
        zorder=4,
    )
    ax.add_patch(cta)
    ax.text(
        avatar_cx, phone_y + phone_h - 6.42,
        "→  지금 바로 주문하기",
        ha="center", va="center",
        fontsize=12, fontweight="bold", color="white",
        zorder=5,
    )

    # Missing AI label note (intentionally missing)
    ax.text(
        avatar_cx, phone_y + 0.25,
        "( AI 생성 표시 없음 )",
        ha="center", va="center",
        fontsize=9, color="#64748B", style="italic",
        zorder=4,
    )

    # --- Red flag callouts (right side) ---
    callouts = [
        {
            "num": "①",
            "title": "출처 불명 '전문가' 자칭",
            "desc": "실존 여부 검증 불가 · 학·경력 과시\nAI 생성된 가공 인물 가능성",
            "target_y": phone_y + phone_h - 2.2,
        },
        {
            "num": "②",
            "title": "구체 효능·수치 과장",
            "desc": '"2주 만에 X 제거" — 임상·실증 없는\n극단적 주장. 표시광고법 위반 소지',
            "target_y": phone_y + phone_h - 4.4,
        },
        {
            "num": "③",
            "title": "긴박감·한정 심리 조작",
            "desc": '"오늘만" · "마감 임박" · "단 100개"\n비판적 판단을 서두르게 하는 패턴',
            "target_y": phone_y + phone_h - 5.58,
        },
        {
            "num": "④",
            "title": "AI 생성 표시 부재",
            "desc": "2025-12-10 표시 의무제 대상 —\n미표시 시 징벌적 손배 5배 가능",
            "target_y": phone_y + 0.25,
        },
    ]

    callout_x = 6.2
    callout_text_x = 6.6
    for i, co in enumerate(callouts):
        target_x = phone_x + phone_w + 0.02
        co_y = co["target_y"]

        # Arrow from phone edge to callout number
        ax.annotate(
            "",
            xy=(target_x, co_y),
            xytext=(callout_x, co_y),
            arrowprops=dict(
                arrowstyle="-|>",
                color="#DC2626",
                lw=2,
                mutation_scale=16,
            ),
            zorder=3,
        )

        # Numbered badge
        badge = Circle(
            (callout_x, co_y), 0.28,
            facecolor="#DC2626", edgecolor="#991B1B", linewidth=1.5,
            zorder=4,
        )
        ax.add_patch(badge)
        ax.text(
            callout_x, co_y,
            co["num"],
            ha="center", va="center",
            fontsize=13, fontweight="bold", color="white",
            zorder=5,
        )

        # Title + description
        ax.text(
            callout_text_x + 0.05, co_y + 0.18,
            co["title"],
            ha="left", va="center",
            fontsize=12.5, fontweight="bold", color="#0F172A",
            zorder=5,
        )
        ax.text(
            callout_text_x + 0.05, co_y - 0.28,
            co["desc"],
            ha="left", va="top",
            fontsize=10, color="#334155",
            zorder=5,
        )

    # Title
    ax.text(
        7.8, 8.55,
        "AI 딥페이크 숏폼 광고의 전형적 패턴",
        ha="center", va="center",
        fontsize=17, fontweight="bold",
        color="#0F172A",
    )
    ax.text(
        7.8, 8.18,
        "유튜브 · 인스타그램 · 틱톡에서 범람 중 — 소비자가 찾아야 할 4가지 red flag",
        ha="center", va="center",
        fontsize=11, color="#475569", style="italic",
    )

    # Footer note
    ax.text(
        7.5, 0.1,
        "※ 본 이미지는 저작권 보호를 위한 교육용 재현 mockup이며, 실제 광고 스크린샷이 아닙니다.",
        ha="center", va="center",
        fontsize=9, color="#94A3B8", style="italic",
    )

    ax.set_xlim(-0.3, 15.3)
    ax.set_ylim(-0.2, 9.0)
    ax.set_aspect("equal")
    ax.axis("off")

    out_path = (
        Path(__file__).resolve().parents[1]
        / "assets" / "diagrams" / "deepfake_example.png"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, facecolor="white", bbox_inches="tight", pad_inches=0.3)
    plt.close(fig)
    print(
        f"saved: {out_path.relative_to(Path.cwd())}  "
        f"({out_path.stat().st_size / 1024:.0f} KB)  font={font}"
    )


if __name__ == "__main__":
    main()
