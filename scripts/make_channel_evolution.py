# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "matplotlib>=3.8",
#   "numpy>=1.26",
# ]
# ///
"""Render Korean e-commerce advertising channel evolution as 4-column card timeline.

각 전환의 공통 동인(사용자 체류 시간의 이동)과 주요 사건을 4 시기로 시각화한다.
SEO·검색광고 이력과 숏폼·AI 단계의 생성형 광고까지 포괄한다.

Run:
    uv run scripts/make_channel_evolution.py

Output:
    assets/diagrams/channel_evolution.png
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

    eras = [
        {
            "title": "포털 · 검색광고",
            "period": "1997 ~ 2000년대 중반",
            "color": "#475569",
            "bg": "#F1F5F9",
            "events": [
                ("1997", "국내 인터넷 광고\n210억 원 규모"),
                ("2000", "1,360억 원으로\n6배 성장 (배너)"),
                ("2001", "네이버 첫 검색광고\n도입 (CPC 경매)"),
                ("2000년대", "SEO 유기 검색\n블로그 상위 노출"),
            ],
            "driver": '"내가 찾는다"\n의도 검색',
        },
        {
            "title": "소셜 · UCC",
            "period": "2001 ~ 2010",
            "color": "#0891B2",
            "bg": "#E0F2FE",
            "events": [
                ("2001", "싸이월드 미니홈피\n소셜 광고 시초"),
                ("2003", "네이버 블로그·카페\n커뮤니티 마케팅"),
                ("2005 이후", "파워블로거·지식iN\n바이럴 마케팅 확산"),
                ("2008 이후", "페이스북 등 SNS\n네트워크 광고 본격화"),
            ],
            "driver": '"지인이 추천"\n관계·바이럴',
        },
        {
            "title": "모바일 피드",
            "period": "2010 ~ 2019",
            "color": "#7C3AED",
            "bg": "#F3E8FF",
            "events": [
                ("2010 이후", "스마트폰 보급\n모바일 광고 급증"),
                ("2012 이후", "네이버 디스플레이\n→ 모바일 광고 전환"),
                ("2014 이후", "페이스북·인스타\n피드 네이티브 광고"),
                ("2015 이후", "앱스토어 최적화\n(ASO) 확산"),
            ],
            "driver": '"피드에서 만난다"\n무한 스크롤',
        },
        {
            "title": "숏폼 · AI",
            "period": "2020 ~ 현재",
            "color": "#DB2777",
            "bg": "#FCE7F3",
            "events": [
                ("2020~2021", "COVID-19 비대면\n라이브커머스 급성장"),
                ("2022 이후", "YouTube Shorts·\nReels·TikTok 주류"),
                ("2022 이후", "커머스 핀·in-bio link\n바로결제 통합"),
                ("2024 이후", "생성형 AI 광고\n대량 생산"),
            ],
            "driver": '"광고가 덮친다"\n알고리즘 주도',
        },
    ]

    n = len(eras)
    col_w = 3.5
    col_gap = 0.35
    total_w = n * col_w + (n - 1) * col_gap

    fig, ax = plt.subplots(figsize=(17.5, 9.5), dpi=170)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    header_h = 0.95
    header_y = 8.7
    body_top = 8.0
    body_bottom = 1.8
    footer_y = 1.1
    body_h = body_top - body_bottom

    for i, era in enumerate(eras):
        x = i * (col_w + col_gap)

        # Header
        hdr = FancyBboxPatch(
            (x, header_y),
            col_w,
            header_h,
            boxstyle="round,pad=0.02,rounding_size=0.12",
            facecolor=era["color"],
            edgecolor="none",
            zorder=2,
        )
        ax.add_patch(hdr)
        ax.text(
            x + col_w / 2,
            header_y + header_h - 0.32,
            era["title"],
            ha="center",
            va="center",
            fontsize=14,
            fontweight="bold",
            color="white",
            zorder=3,
        )
        ax.text(
            x + col_w / 2,
            header_y + 0.28,
            era["period"],
            ha="center",
            va="center",
            fontsize=10,
            color="white",
            alpha=0.9,
            zorder=3,
        )

        # Body
        body = FancyBboxPatch(
            (x, body_bottom),
            col_w,
            body_h,
            boxstyle="round,pad=0.02,rounding_size=0.1",
            facecolor=era["bg"],
            edgecolor=era["color"],
            linewidth=1.3,
            zorder=1,
        )
        ax.add_patch(body)

        # Events
        event_count = len(era["events"])
        slot_h = body_h / event_count
        for j, (year, desc) in enumerate(era["events"]):
            center_y = body_top - (j + 0.5) * slot_h

            ax.text(
                x + 0.25,
                center_y + 0.28,
                year,
                fontsize=11,
                fontweight="bold",
                color=era["color"],
                ha="left",
                va="center",
                zorder=3,
            )
            ax.text(
                x + 0.25,
                center_y - 0.22,
                desc,
                fontsize=10,
                color="#0F172A",
                ha="left",
                va="center",
                zorder=3,
            )

            # Separator line between events (except last)
            if j < event_count - 1:
                sep_y = body_top - (j + 1) * slot_h
                ax.plot(
                    [x + 0.2, x + col_w - 0.2],
                    [sep_y, sep_y],
                    color=era["color"],
                    alpha=0.25,
                    linewidth=0.8,
                    zorder=2,
                )

        # Driver footer
        ax.text(
            x + col_w / 2,
            footer_y,
            era["driver"],
            ha="center",
            va="center",
            fontsize=11,
            fontweight="bold",
            color=era["color"],
            style="italic",
        )

        # Arrow to next
        if i < n - 1:
            arrow_x = x + col_w + 0.04
            arrow_end = x + col_w + col_gap - 0.04
            arrow_y = (body_top + body_bottom) / 2
            ax.annotate(
                "",
                xy=(arrow_end, arrow_y),
                xytext=(arrow_x, arrow_y),
                arrowprops=dict(arrowstyle="->", color="#94A3B8", lw=2.2),
                zorder=4,
            )

    # Title
    ax.text(
        total_w / 2,
        9.95,
        "국내 이커머스 광고 채널의 진화 — 4시기",
        ha="center",
        va="center",
        fontsize=18,
        fontweight="bold",
        color="#0F172A",
    )

    # Bottom insight
    ax.text(
        total_w / 2,
        0.25,
        "공통 동인: 사용자 체류 시간의 이동 — 포털 검색 → 소셜 피드 → 모바일 스크롤 → 숏폼·AI 알고리즘 주도",
        ha="center",
        va="center",
        fontsize=11,
        color="#334155",
        style="italic",
    )

    ax.set_xlim(-0.4, total_w + 0.4)
    ax.set_ylim(-0.1, 10.4)
    ax.axis("off")
    ax.set_aspect("auto")

    out_path = (
        Path(__file__).resolve().parents[1]
        / "assets" / "diagrams" / "channel_evolution.png"
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
