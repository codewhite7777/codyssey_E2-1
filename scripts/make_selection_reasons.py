# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "matplotlib>=3.8",
#   "numpy>=1.26",
# ]
# ///
"""Render §1.4 five selection reasons as a 5-pillar summary card visualization.

Run:
    uv run scripts/make_selection_reasons.py

Output:
    assets/diagrams/selection_reasons.png
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

    reasons = [
        {
            "num": "1",
            "title": "시급성 · 시의성",
            "subtitle": "2025년 전형적 사회 문제",
            "body": [
                "숏폼 광고 침투율 급증",
                "+ 생성형 AI 광고 폭증",
                "= AI가 만든 문제는",
                "   AI로 풀어야 한다",
            ],
            "ref": "§1.1.2 · §1.1.4",
            "color": "#DC2626",
            "bg": "#FEE2E2",
        },
        {
            "num": "2",
            "title": "다면 가치",
            "subtitle": "4주체 모두에게 가치",
            "body": [
                "• 소비자: 피해 방지",
                "• 플랫폼: 운영 리스크 저감",
                "• 규제기관: 모니터링 자동화",
                "• 정직한 셀러: 공정경쟁",
            ],
            "ref": "§1.1.4 · §1.4 #2",
            "color": "#0891B2",
            "bg": "#CFFAFE",
        },
        {
            "num": "3",
            "title": "AI 기술 정당성",
            "subtitle": "본질적으로 멀티모달 문제",
            "body": [
                "• Vision / Video",
                "  (Before·After · 딥페이크)",
                "• NLP / LLM (Claim 추출)",
                "• 멀티모달 교차검증",
            ],
            "ref": "§1.4 #3",
            "color": "#7C3AED",
            "bg": "#EDE9FE",
        },
        {
            "num": "4",
            "title": "도메인 좌표",
            "subtitle": "L4 × L6 교차점",
            "body": [
                "• L4 광고·마케팅",
                "   (공급 측 콘텐츠 분석)",
                "• L6 의사결정 지원",
                "   (수요 측 판별 근거)",
            ],
            "ref": "§1.4.1",
            "color": "#DB2777",
            "bg": "#FCE7F3",
        },
        {
            "num": "5",
            "title": "학습 프로젝트 적합성",
            "subtitle": "데이터·데모 조달 가능",
            "body": [
                "• 공개 데이터 + 자체 수집",
                "• 공정위·식약처 시정내역",
                "• 앱·확장 프로토타입",
                "• 발표 데모 임팩트 강",
            ],
            "ref": "§1.5 · §4",
            "color": "#059669",
            "bg": "#D1FAE5",
        },
    ]

    n = len(reasons)
    card_w = 3.3
    card_gap = 0.3
    total_w = n * card_w + (n - 1) * card_gap

    fig, ax = plt.subplots(figsize=(18, 8.5), dpi=170)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    header_h = 1.45
    body_top = 5.8
    body_bottom = 0.4

    for i, r in enumerate(reasons):
        x = i * (card_w + card_gap)

        # Header
        hdr = FancyBboxPatch(
            (x, body_top),
            card_w, header_h,
            boxstyle="round,pad=0.02,rounding_size=0.12",
            facecolor=r["color"], edgecolor="none",
            zorder=2,
        )
        ax.add_patch(hdr)

        # Number badge
        badge_x = x + 0.45
        badge_y = body_top + header_h - 0.55
        badge = Circle(
            (badge_x, badge_y), 0.27,
            facecolor="white", edgecolor="white", linewidth=1.5,
            zorder=3,
        )
        ax.add_patch(badge)
        ax.text(
            badge_x, badge_y,
            r["num"],
            ha="center", va="center",
            fontsize=16, fontweight="bold",
            color=r["color"],
            zorder=4,
        )

        # Title
        ax.text(
            x + 0.9, body_top + header_h - 0.55,
            r["title"],
            ha="left", va="center",
            fontsize=14, fontweight="bold",
            color="white",
            zorder=4,
        )
        # Subtitle
        ax.text(
            x + card_w / 2, body_top + 0.3,
            r["subtitle"],
            ha="center", va="center",
            fontsize=10.5,
            color="white", alpha=0.92,
            zorder=4,
        )

        # Body
        body = FancyBboxPatch(
            (x, body_bottom),
            card_w, body_top - body_bottom - 0.02,
            boxstyle="round,pad=0.02,rounding_size=0.1",
            facecolor=r["bg"], edgecolor=r["color"],
            linewidth=1.3, zorder=1,
        )
        ax.add_patch(body)

        # Body lines
        line_count = len(r["body"])
        line_start = body_top - 0.45
        line_step = (body_top - body_bottom - 0.9) / (line_count + 0.5)
        for j, line in enumerate(r["body"]):
            ax.text(
                x + 0.25,
                line_start - j * line_step,
                line,
                ha="left", va="top",
                fontsize=11,
                color="#0F172A",
                zorder=3,
            )

        # Reference badge
        ax.text(
            x + card_w / 2,
            body_bottom + 0.2,
            r["ref"],
            ha="center", va="center",
            fontsize=10, fontweight="bold",
            color=r["color"],
            style="italic",
            zorder=3,
        )

    # Title
    ax.text(
        total_w / 2,
        8.0,
        "본 프로젝트 선택 5 이유 — 한눈에 보기",
        ha="center", va="center",
        fontsize=18, fontweight="bold",
        color="#0F172A",
    )
    ax.text(
        total_w / 2,
        7.5,
        "시급성 × 다면 가치 × AI 정당성 × 도메인 좌표 × 학습 적합성 — 다섯 축이 모두 충족되는 과제",
        ha="center", va="center",
        fontsize=11,
        color="#475569",
        style="italic",
    )

    ax.set_xlim(-0.4, total_w + 0.4)
    ax.set_ylim(-0.1, 8.4)
    ax.set_aspect("auto")
    ax.axis("off")

    out_path = (
        Path(__file__).resolve().parents[1]
        / "assets" / "diagrams" / "selection_reasons.png"
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
