from pathlib import Path
import json
import os
from collections import defaultdict


INPUT = Path("data/contributions.json")
OUTPUT = Path("info-card.svg")


USERNAME = "haseebarshad17"

EMAIL = "haseebarshad1712@gmail.com"
PHONE = "3295339588"

ROLE = "Senior Software Engineer"
COMPANY = "Spadatsoft"

PRIMARY = "TypeScript / JavaScript"
FRONTEND = "Next.js / React / React Native"
BACKEND = "NestJS / Node.js / Express"
DATA_CLOUD = "Supabase / Firebase / MongoDB"


WIDTH = 490
HEIGHT = 370


BG = "#0d1117"
BORDER = "#30363d"
CARD = "#161b22"
GREEN = "#39d353"
TEXT = "#c9d1d9"
MUTED = "#8b949e"


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
        INPUT.read_text(
            encoding="utf-8"
        )
    )


def get_monthly_data(days):

    monthly = defaultdict(int)

    for day in days:

        month = day["date"][:7]

        monthly[month] += (
            day.get("count", 0)
        )

    months = sorted(
        monthly.keys()
    )[-12:]

    return [
        (
            month,
            monthly.get(month, 0)
        )
        for month in months
    ]


def main():

    data = load_data()

    static = (
        os.getenv("STATIC") == "1"
    )

    days = sorted(
        data["days"],
        key=lambda item: item["date"]
    )

    monthly = get_monthly_data(days)

    total = data.get(
        "total",
        0
    )

    current_streak = data.get(
        "current_streak",
        0
    )

    longest_streak = data.get(
        "longest_streak",
        0
    )

    active_days = sum(
        1
        for day in days
        if day.get("count", 0) > 0
    )

    # ---------------------------------------------------------
    # SVG ROOT
    # ---------------------------------------------------------

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

        # Identity.
        (
            f'<text '
            f'x="22" '
            f'y="64" '
            f'font-family="monospace" '
            f'font-size="8" '
            f'letter-spacing="1.6" '
            f'fill="{GREEN}">'
            f'SENIOR SOFTWARE ENGINEER'
            f'</text>'
        ),

        (
            f'<text '
            f'x="22" '
            f'y="83" '
            f'font-family="monospace" '
            f'font-size="10" '
            f'fill="{TEXT}">'
            f'Building scalable web &amp; mobile systems'
            f'</text>'
        ),
    ]

    # ---------------------------------------------------------
    # SIX PROFESSIONAL STAT CARDS
    # ---------------------------------------------------------

    stats = [

        (
            "ROLE",
            "Senior Developer",
            "software engineering",
        ),

        (
            "COMPANY",
            "Spadatsoft",
            "professional role",
        ),

        (
            "PRIMARY",
            "TypeScript",
            "JavaScript / ES6",
        ),

        (
            "FRONTEND",
            "Next.js",
            "React / React Native",
        ),

        (
            "BACKEND",
            "NestJS",
            "Node.js / Express",
        ),

        (
            "DATA / CLOUD",
            "Supabase",
            "Firebase / MongoDB",
        ),
    ]

    card_width = 214
    card_height = 47

    left_x = 22
    right_x = 254

    start_y = 94
    row_gap = 6

    for index, (
        eyebrow,
        title,
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
            + row
            * (
                card_height
                + row_gap
            )
        )

        if static:

            opacity = "1"
            animation = ""

        else:

            opacity = "0"

            delay = (
                0.1
                + index * 0.08
            )

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
                f'y="{y + 13}" '
                f'font-family="monospace" '
                f'font-size="6.5" '
                f'letter-spacing="1" '
                f'fill="{GREEN}">'
                f'{escape(eyebrow)}'
                f'</text>'

                # Main title.
                f'<text '
                f'x="{x + 12}" '
                f'y="{y + 31}" '
                f'font-family="monospace" '
                f'font-size="14" '
                f'font-weight="bold" '
                f'fill="{TEXT}">'
                f'{escape(title)}'
                f'</text>'

                # Subtitle.
                f'<text '
                f'x="{x + 12}" '
                f'y="{y + 42}" '
                f'font-family="monospace" '
                f'font-size="6.5" '
                f'fill="{MUTED}">'
                f'{escape(subtitle)}'
                f'</text>'

                f'{animation}'

                f'</g>'
            )
        )

    # ---------------------------------------------------------
    # CONTRIBUTION PILLAR CHART
    # ---------------------------------------------------------

    chart_title_y = 257

    svg.append(

        (
            f'<text '
            f'x="22" '
            f'y="{chart_title_y}" '
            f'font-family="monospace" '
            f'font-size="7.5" '
            f'letter-spacing="1.3" '
            f'fill="{GREEN}">'
            f'CONTRIBUTION ACTIVITY'
            f'</text>'
        )
    )

    chart_x = 22
    chart_y = 264

    chart_width = 446
    chart_height = 42

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

            delay = (
                0.65
                + index * 0.04
            )

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

        # Month.
        svg.append(

            (
                f'<text '
                f'x="{x + pillar_width / 2:.2f}" '
                f'y="318" '
                f'text-anchor="middle" '
                f'font-family="monospace" '
                f'font-size="6" '
                f'fill="{MUTED}">'
                f'{escape(month[5:7])}'
                f'</text>'
            )
        )

    # ---------------------------------------------------------
    # ACTIVITY SUMMARY
    # ---------------------------------------------------------

    svg.append(

        (
            f'<text '
            f'x="22" '
            f'y="337" '
            f'font-family="monospace" '
            f'font-size="7" '
            f'fill="{MUTED}">'
            f'{total:,} contributions'
            f' · {active_days:,} active days'
            f' · streak {current_streak}'
            f'</text>'
        )
    )

    # ---------------------------------------------------------
    # CONTACT
    # ---------------------------------------------------------

    svg.append(

        (
            f'<line '
            f'x1="22" '
            f'y1="345" '
            f'x2="468" '
            f'y2="345" '
            f'stroke="{BORDER}"/>'
        )
    )

    svg.append(

        (
            f'<text '
            f'x="22" '
            f'y="360" '
            f'font-family="monospace" '
            f'font-size="6.5" '
            f'fill="{TEXT}">'
            f'✉ {escape(EMAIL)}'
            f'</text>'
        )
    )

    svg.append(

        (
            f'<text '
            f'x="330" '
            f'y="360" '
            f'font-family="monospace" '
            f'font-size="6.5" '
            f'fill="{TEXT}">'
            f'☎ {escape(PHONE)}'
            f'</text>'
        )
    )

    svg.append("</svg>")

    OUTPUT.write_text(
        "\n".join(svg),
        encoding="utf-8"
    )

    print(
        f"Created: {OUTPUT}"
    )


if __name__ == "__main__":
    main()