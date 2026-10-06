from pathlib import Path
from datetime import datetime

import json


INPUT = Path("data/contributions.json")
OUTPUT = Path("contrib-heatmap.svg")


PALETTE = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
]

BG = "#0d1117"
TEXT = "#c9d1d9"
MUTED = "#8b949e"

CELL = 11
GAP = 3

LEFT = 35
TOP = 35

WIDTH = 860
HEIGHT = 150


def main():
    if not INPUT.exists():
        raise FileNotFoundError(
            "data/contributions.json not found. "
            "Run fetch_contributions.py first."
        )

    data = json.loads(
        INPUT.read_text(encoding="utf-8")
    )

    days = data["days"]
    total = data["total"]
    username = data["username"]

    # GitHub calendar starts from the oldest date.
    days = sorted(
        days,
        key=lambda item: item["date"],
    )

    # Build 7-day columns.
    first_date = datetime.strptime(
        days[0]["date"],
        "%Y-%m-%d",
    )

    # Align first day to Sunday.
    start_offset = (first_date.weekday() + 1) % 7

    padded = ([None] * start_offset) + days

    columns = (len(padded) + 6) // 7

    svg = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{WIDTH}" height="{HEIGHT}" '
            f'viewBox="0 0 {WIDTH} {HEIGHT}">'
        ),

        f'<rect width="100%" height="100%" '
        f'rx="12" fill="{BG}"/>',

        # Terminal title
        f'<text x="20" y="22" '
        f'font-family="monospace" '
        f'font-size="11" fill="{MUTED}">'
        f'{escape(username)}@github ~ contributions'
        f'</text>',
    ]

    for index, day in enumerate(padded):
        if day is None:
            continue

        column = index // 7
        row = index % 7

        x = LEFT + column * (CELL + GAP)
        y = TOP + row * (CELL + GAP)

        level = max(
            0,
            min(4, int(day["level"])),
        )

        fill = PALETTE[level]

        delay = 0.01 + (column + row) * 0.025

        svg.append(
            f'<rect '
            f'x="{x}" '
            f'y="{y}" '
            f'width="{CELL}" '
            f'height="{CELL}" '
            f'rx="2" '
            f'fill="{fill}" '
            f'opacity="0">'
            f'<animate '
            f'attributeName="opacity" '
            f'values="0;1" '
            f'keyTimes="0;1" '
            f'begin="{delay:.3f}s" '
            f'dur="0.35s" '
            f'fill="freeze"/>'
            f'</rect>'
        )

    # Legend
    legend_x = 665
    legend_y = 125

    svg.append(
        f'<text x="{legend_x - 42}" y="{legend_y + 10}" '
        f'font-family="monospace" font-size="10" '
        f'fill="{MUTED}">Less</text>'
    )

    for i, color in enumerate(PALETTE):
        x = legend_x + i * 16

        svg.append(
            f'<rect x="{x}" y="{legend_y}" '
            f'width="11" height="11" rx="2" '
            f'fill="{color}"/>'
        )

    svg.append(
        f'<text x="{legend_x + 85}" y="{legend_y + 10}" '
        f'font-family="monospace" font-size="10" '
        f'fill="{MUTED}">More</text>'
    )

    # Stats
    svg.append(
        f'<text x="20" y="125" '
        f'font-family="monospace" font-size="11" '
        f'fill="{TEXT}">'
        f'{total:,} contributions in the last year'
        f'</text>'
    )

    svg.append("</svg>")

    OUTPUT.write_text(
        "\n".join(svg),
        encoding="utf-8",
    )

    print(f"Created: {OUTPUT}")


def escape(value):
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


if __name__ == "__main__":
    main()