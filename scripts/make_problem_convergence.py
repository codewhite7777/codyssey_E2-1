# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "matplotlib>=3.8",
#   "numpy>=1.26",
# ]
# ///
"""Render the convergence diagram — 4 flows meeting at the project's problem point.

§1.2 문제 제기의 '네 흐름이 한 지점에서 교차하는 지점' 서사를 시각화한다.
각 흐름(시장 확대 / 채널 이동 / 소비 가속 / 공급 폭증)이 중앙의 문제로
모여드는 방사형 수렴 다이어그램.

Run:
    uv run scripts/make_problem_convergence.py

Output:
    assets/diagrams/problem_convergence.png
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

    flows = [
        {  # North
            "id": "①",
            "name": "시장 확대",
            "detail": "거래액 134조 → 272조\n(6년간 2배 팽창)",
            "ref": "§1.1.1",
            "color": "#0891B2",
            "pos": (0, 5.0),
            "direction": "N",
        },
        {  # East
            "id": "②",
            "name": "채널 이동",
            "detail": "포털 검색 → 숏폼 · AI\n(알고리즘 주도 피드)",
            "ref": "§1.1.2",
            "color": "#7C3AED",
            "pos": (7.5, 0),
            "direction": "E",
        },
        {  # South
            "id": "③",
            "name": "소비 가속",
            "detail": "21분 플로우 소비\n(수 초만에 결제 이동)",
            "ref": "§1.1.3",
            "color": "#DB2777",
            "pos": (0, -5.0),
            "direction": "S",
        },
        {  # West
            "id": "④",
            "name": "공급 폭증",
            "detail": "AI 생성 비용 극단 절감\n규제는 사후적",
            "ref": "§1.1.4",
            "color": "#DC2626",
            "pos": (-7.5, 0),
            "direction": "W",
        },
    ]

    fig, ax = plt.subplots(figsize=(14, 10), dpi=180)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    # Center problem box
    cx, cy = 0, 0
    cw, ch = 7.6, 3.2
    center_box = FancyBboxPatch(
        (cx - cw / 2, cy - ch / 2),
        cw, ch,
        boxstyle="round,pad=0.05,rounding_size=0.3",
        facecolor="#FEF3C7",
        edgecolor="#B45309",
        linewidth=3,
        zorder=5,
    )
    ax.add_patch(center_box)
    ax.text(
        cx, cy + 0.95,
        "본 프로젝트 문제",
        ha="center", va="center",
        fontsize=16, fontweight="bold",
        color="#B45309",
        zorder=6,
    )
    ax.text(
        cx, cy - 0.05,
        "일반 소비자는 숏폼 피드의",
        ha="center", va="center",
        fontsize=13,
        color="#0F172A",
        zorder=6,
    )
    ax.text(
        cx, cy - 0.60,
        "허위·과장 광고를 실시간 판별할 수단이 없다",
        ha="center", va="center",
        fontsize=13, fontweight="bold",
        color="#B91C1C",
        zorder=6,
    )

    # 4 flow boxes
    box_w = 4.8
    box_h = 1.85

    for flow in flows:
        px, py = flow["pos"]

        box = FancyBboxPatch(
            (px - box_w / 2, py - box_h / 2),
            box_w, box_h,
            boxstyle="round,pad=0.04,rounding_size=0.2",
            facecolor=flow["color"],
            edgecolor=flow["color"],
            linewidth=2,
            zorder=5,
        )
        ax.add_patch(box)

        ax.text(
            px, py + 0.55,
            f"{flow['id']}  {flow['name']}",
            ha="center", va="center",
            fontsize=14, fontweight="bold",
            color="white",
            zorder=6,
        )
        ax.text(
            px, py - 0.20,
            flow["detail"],
            ha="center", va="center",
            fontsize=10.5,
            color="white",
            zorder=6,
        )
        ax.text(
            px, py - 0.75,
            flow["ref"],
            ha="center", va="center",
            fontsize=9,
            color="white",
            alpha=0.75,
            style="italic",
            zorder=6,
        )

        # Arrow from box edge toward center box edge
        if flow["direction"] == "N":
            start = (px, py - box_h / 2)
            end = (cx, cy + ch / 2 + 0.05)
        elif flow["direction"] == "S":
            start = (px, py + box_h / 2)
            end = (cx, cy - ch / 2 - 0.05)
        elif flow["direction"] == "E":
            start = (px - box_w / 2, py)
            end = (cx + cw / 2 + 0.05, cy)
        else:  # W
            start = (px + box_w / 2, py)
            end = (cx - cw / 2 - 0.05, cy)

        ax.annotate(
            "",
            xy=end, xytext=start,
            arrowprops=dict(
                arrowstyle="-|>",
                color=flow["color"],
                lw=3,
                mutation_scale=22,
                alpha=0.85,
            ),
            zorder=3,
        )

    # Title
    ax.text(
        0, 7.4,
        "네 흐름이 한 지점에서 교차하며 문제가 드러난다",
        ha="center", va="center",
        fontsize=17, fontweight="bold",
        color="#0F172A",
    )
    ax.text(
        0, 6.65,
        "§1.1에서 추적한 네 흐름의 교차점 = 본 프로젝트의 문제 발생 지점",
        ha="center", va="center",
        fontsize=11,
        color="#475569",
        style="italic",
    )

    ax.set_xlim(-10.5, 10.5)
    ax.set_ylim(-7.0, 8.0)
    ax.set_aspect("equal")
    ax.axis("off")

    out_path = (
        Path(__file__).resolve().parents[1]
        / "assets" / "diagrams" / "problem_convergence.png"
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
