from pathlib import Path
import json
import os
from collections import defaultdict


INPUT = Path("data/contributions.json")
OUTPUT = Path("info-card.svg")

USERNAME = "haseebarshad17"

WIDTH = 490
HEIGHT = 370

BG = "#0d1117"
BORDER = "#30363d"
CARD = "#161b22"
GREEN = "#39d353"
TEXT = "#c9d1d9"
MUTED = "#8b949e"

PALETTE = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
    "#69f0a0",
]


def escape(value):
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def load_data():
    if not INPUT.exists():
        raise FileNotFoundError(
            "data/contributions.json not found. "
            "Run fetch_contributions.py first."
        )

    return json.loads(
        INPUT.read_text(encoding="utf-8")
    )


def get_monthly_data(days):
    monthly = defaultdict(int)

    for day in days:
        month = day["date"][:7]
        monthly[month] += day.get("count", 0)

    months = sorted(monthly.keys())[-12:]

    return [
        (
            month,
            monthly.get(month, 0),
        )
        for month in months
    ]


def get_active_days(days):
    return sum(
        1
        for day in days
        if day.get("count", 0) > 0
    )


def get_best_day(days):
    if not days:
        return None

    return max(
        days,
        key=lambda day: day.get("count", 0),
    )


def main():
    data = load_data()

    static = os.getenv("STATIC") == "1"

    days = sorted(
        data["days"],
        key=lambda item: item["date"],
    )

    total = data.get("total", 0)

    current_streak = data.get(
        "current_streak",
        0,
    )

    longest_streak = data.get(
        "longest_streak",
        0,
    )

    active_days = get_active_days(days)

    best_day = get_best_day(days)

    best_day_count = (
        best_day.get("count", 0)
        if best_day
        else 0
    )

    monthly = get_monthly_data(days)

    active_months = sum(
        1
        for _, value in monthly
        if value > 0
    )

    svg = [
        '<?xml version="1.0" encoding="UTF-8"?>',

        (
            f'<svg '
            f'xmlns="http://www.w3.org/2000/svg" '
            f'width="{WIDTH}" '
            f'height="{HEIGHT}" '
            f'viewBox="0 0 {WIDTH} {HEIGHT}">'
        ),

        (
            f'<rect '
            f'x="0" '
            f'y="0" '
            f'width="{WIDTH}" '
            f'height="{HEIGHT}" '
            f'rx="12" '
            f'fill="{BG}" '
            f'stroke="{BORDER}"/>'
        ),

        # Terminal dots.
        '<circle cx="20" cy="20" r="5" fill="#ff5f56"/>',
        '<circle cx="38" cy="20" r="5" fill="#ffbd2e"/>',
        '<circle cx="56" cy="20" r="5" fill="#27c93f"/>',

        (
            f'<text '
            f'x="78" '
            f'y="25" '
            f'font-family="monospace" '
            f'font-size="12" '
            f'fill="{MUTED}">'
            f'{escape(USERNAME)}@github'
            f'</text>'
        ),

        (
            f'<line '
            f'x1="20" '
            f'y1="42" '
            f'x2="470" '
            f'y2="42" '
            f'stroke="{BORDER}"/>'
        ),
    ]

    # ---------------------------------------------------------
    # HEADER
    # ---------------------------------------------------------

    svg.append(
        (
            f'<text '
            f'x="22" '
            f'y="70" '
            f'font-family="monospace" '
            f'font-size="10" '
            f'letter-spacing="1.5" '
            f'fill="{GREEN}">'
            f'GITHUB ANALYTICS'
            f'</text>'
        )
    )

    svg.append(
        (
            f'<text '
            f'x="22" '
            f'y="98" '
            f'font-family="monospace" '
            f'font-size="30" '
            f'font-weight="bold" '
            f'fill="{TEXT}">'
            f'{total:,}'
            f'</text>'
        )
    )

    svg.append(
        (
            f'<text '
            f'x="112" '
            f'y="98" '
            f'font-family="monospace" '
            f'font-size="10" '
            f'fill="{MUTED}">'
            f'total contributions'
            f'</text>'
        )
    )

    # ---------------------------------------------------------
    # SIX STAT CARDS
    # ---------------------------------------------------------

    stats = [
        (
            "CURRENT STREAK",
            str(current_streak),
            "consecutive days",
        ),
        (
            "LONGEST STREAK",
            str(longest_streak),
            "best run",
        ),
        (
            "ACTIVE DAYS",
            str(active_days),
            "days with activity",
        ),
        (
            "BEST DAY",
            str(best_day_count),
            "contributions",
        ),
        (
            "ACTIVE MONTHS",
            str(active_months),
            "of last 12",
        ),
        (
            "YEAR TOTAL",
            f"{total:,}",
            "last 12 months",
        ),
    ]

    card_width = 214
    card_height = 52

    left_x = 22
    right_x = 254

    start_y = 112
    row_gap = 8

    for index, (
        eyebrow,
        value,
        subtitle,
    ) in enumerate(stats):

        column = index % 2
        row = index // 2

        x = (
            left_x
            if column == 0
            else right_x
        )

        y = (
            start_y
            + row * (
                card_height
                + row_gap
            )
        )

        if static:
            opacity = "1"
            animation = ""
        else:
            opacity = "0"
            delay = 0.15 + index * 0.08

            animation = (
                f'<animate '
                f'attributeName="opacity" '
                f'values="0;1" '
                f'begin="{delay:.2f}s" '
                f'dur="0.3s" '
                f'fill="freeze"/>'
            )

        svg.append(
            (
                f'<g opacity="{opacity}">'
                f'<rect '
                f'x="{x}" '
                f'y="{y}" '
                f'width="{card_width}" '
                f'height="{card_height}" '
                f'rx="7" '
                f'fill="{CARD}" '
                f'stroke="{BORDER}"/>'

                # Eyebrow.
                f'<text '
                f'x="{x + 12}" '
                f'y="{y + 15}" '
                f'font-family="monospace" '
                f'font-size="7" '
                f'letter-spacing="1" '
                f'fill="{GREEN}">'
                f'{escape(eyebrow)}'
                f'</text>'

                # Big value.
                f'<text '
                f'x="{x + 12}" '
                f'y="{y + 36}" '
                f'font-family="monospace" '
                f'font-size="18" '
                f'font-weight="bold" '
                f'fill="{TEXT}">'
                f'{escape(value)}'
                f'</text>'

                # Subtitle.
                f'<text '
                f'x="{x + 85}" '
                f'y="{y + 34}" '
                f'font-family="monospace" '
                f'font-size="7" '
                f'fill="{MUTED}">'
                f'{escape(subtitle)}'
                f'</text>'

                f'{animation}'
                f'</g>'
            )
        )

    # ---------------------------------------------------------
    # PILLAR CHART
    # ---------------------------------------------------------

    chart_title_y = 294

    svg.append(
        (
            f'<text '
            f'x="22" '
            f'y="{chart_title_y}" '
            f'font-family="monospace" '
            f'font-size="8" '
            f'letter-spacing="1.2" '
            f'fill="{GREEN}">'
            f'CONTRIBUTION ACTIVITY'
            f'</text>'
        )
    )

    chart_x = 22
    chart_y = 302
    chart_width = 446
    chart_height = 45

    if monthly:
        max_value = max(
            value
            for _, value in monthly
        )
    else:
        max_value = 1

    if max_value <= 0:
        max_value = 1

    pillar_gap = 5

    pillar_width = (
        chart_width
        / max(len(monthly), 1)
    ) - pillar_gap

    for index, (
        month,
        value,
    ) in enumerate(monthly):

        height = (
            value
            / max_value
            * chart_height
        )

        x = (
            chart_x
            + index
            * (
                pillar_width
                + pillar_gap
            )
        )

        y = (
            chart_y
            + chart_height
            - height
        )

        if static:
            opacity = "1"
            animation = ""
        else:
            opacity = "0"
            delay = 0.7 + index * 0.04

            animation = (
                f'<animate '
                f'attributeName="opacity" '
                f'values="0;1" '
                f'begin="{delay:.2f}s" '
                f'dur="0.25s" '
                f'fill="freeze"/>'
            )

        svg.append(
            (
                f'<rect '
                f'x="{x:.2f}" '
                f'y="{y:.2f}" '
                f'width="{pillar_width:.2f}" '
                f'height="{height:.2f}" '
                f'rx="2" '
                f'fill="{GREEN}" '
                f'opacity="{opacity}">'
                f'{animation}'
                f'</rect>'
            )
        )

        label = month[5:7]

        svg.append(
            (
                f'<text '
                f'x="{x + pillar_width / 2:.2f}" '
                f'y="359" '
                f'text-anchor="middle" '
                f'font-family="monospace" '
                f'font-size="6" '
                f'fill="{MUTED}">'
                f'{escape(label)}'
                f'</text>'
            )
        )

    svg.append("</svg>")

    OUTPUT.write_text(
        "\n".join(svg),
        encoding="utf-8",
    )

    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    main()