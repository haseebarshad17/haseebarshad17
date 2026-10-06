from pathlib import Path
import json


INPUT = Path("data/contributions.json")
OUTPUT = Path("contrib-heatmap.svg")


PALETTE = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
    "#69f0a0",
]


BG = "#0d1117"
TEXT = "#c9d1d9"
MUTED = "#8b949e"


WIDTH = 860
HEIGHT = 125

CELL = 10
GAP = 3

LEFT = 20
TOP = 28


def escape(value):
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def main():

    if not INPUT.exists():
        raise FileNotFoundError(
            "data/contributions.json not found."
        )

    data = json.loads(
        INPUT.read_text(
            encoding="utf-8"
        )
    )

    days = sorted(
        data["days"],
        key=lambda item: item["date"],
    )

    if not days:
        raise ValueError(
            "No contribution data found."
        )

    total = data.get("total", 0)
    username = data.get(
        "username",
        "github",
    )

    current_streak = data.get(
        "current_streak",
        0,
    )

    longest_streak = data.get(
        "longest_streak",
        0,
    )

    # Keep exactly the last 365 days.
    days = days[-365:]

    padded = (
        [None]
        * (
            (
                len(days)
                + 6
            )
            % 7
        )
        + days
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
            f'width="100%" '
            f'height="100%" '
            f'rx="12" '
            f'fill="{BG}"/>'
        ),

        (
            f'<text '
            f'x="20" '
            f'y="17" '
            f'font-family="monospace" '
            f'font-size="9" '
            f'fill="{MUTED}">'
            f'{escape(username)}@github ~ contributions'
            f'</text>'
        ),
    ]

    for index, day in enumerate(padded):

        if day is None:
            continue

        column = index // 7
        row = index % 7

        x = (
            LEFT
            + column * (CELL + GAP)
        )

        y = (
            TOP
            + row * (CELL + GAP)
        )

        level = max(
            0,
            min(
                5,
                int(day.get("level", 0)),
            ),
        )

        fill = PALETTE[level]

        delay = (
            0.01
            + (column + row)
            * 0.015
        )

        svg.append(
            (
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
                f'begin="{delay:.3f}s" '
                f'dur="0.25s" '
                f'fill="freeze"/>'
                f'</rect>'
            )
        )

    # Footer stats.
    svg.append(
        (
            f'<text '
            f'x="20" '
            f'y="116" '
            f'font-family="monospace" '
            f'font-size="9" '
            f'fill="{TEXT}">'
            f'{total:,} contributions in the last year'
            f'</text>'
        )
    )

    svg.append(
        (
            f'<text '
            f'x="450" '
            f'y="116" '
            f'font-family="monospace" '
            f'font-size="8" '
            f'fill="{MUTED}">'
            f'streak {current_streak} · '
            f'longest {longest_streak}'
            f'</text>'
        )
    )

    # Compact legend.
    legend_x = 690
    legend_y = 109

    svg.append(
        (
            f'<text '
            f'x="{legend_x - 28}" '
            f'y="{legend_y + 7}" '
            f'font-family="monospace" '
            f'font-size="7" '
            f'fill="{MUTED}">'
            f'Less'
            f'</text>'
        )
    )

    for index, color in enumerate(PALETTE):

        x = (
            legend_x
            + index * 13
        )

        svg.append(
            (
                f'<rect '
                f'x="{x}" '
                f'y="{legend_y}" '
                f'width="9" '
                f'height="9" '
                f'rx="2" '
                f'fill="{color}"/>'
            )
        )

    svg.append(
        (
            f'<text '
            f'x="{legend_x + 82}" '
            f'y="{legend_y + 7}" '
            f'font-family="monospace" '
            f'font-size="7" '
            f'fill="{MUTED}">'
            f'More'
            f'</text>'
        )
    )

    svg.append("</svg>")

    OUTPUT.write_text(
        "\n".join(svg),
        encoding="utf-8",
    )

    print(
        f"Created: {OUTPUT}"
    )


if __name__ == "__main__":
    main()