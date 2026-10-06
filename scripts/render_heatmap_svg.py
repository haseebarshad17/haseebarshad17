from pathlib import Path
import json
from datetime import datetime


INPUT = Path(
    "data/contributions.json"
)

OUTPUT = Path(
    "contrib-heatmap.svg"
)


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


CELL = 11
GAP = 3

LEFT = 35
TOP = 35

WIDTH = 860
HEIGHT = 150


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
            "data/contributions.json "
            "not found."
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

    total = data["total"]
    username = data["username"]

    current_streak = data.get(
        "current_streak",
        0,
    )

    longest_streak = data.get(
        "longest_streak",
        0,
    )

    first_date = datetime.strptime(
        days[0]["date"],
        "%Y-%m-%d",
    )

    start_offset = (
        first_date.weekday() + 1
    ) % 7

    padded = (
        [None] * start_offset
        + days
    )

    columns = (
        len(padded) + 6
    ) // 7

    svg = [
        '<?xml version="1.0" encoding="UTF-8"?>',

        (
            f'<svg xmlns="http://www.w3.org/2000/svg" '
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

        "<defs>",

        """
        <style>
            .contribution {
                transform-box: fill-box;
                transform-origin: center;
                animation-name: reveal;
                animation-duration: 0.45s;
                animation-timing-function: ease-out;
                animation-fill-mode: forwards;
                opacity: 0;
            }

            @keyframes reveal {
                from {
                    opacity: 0;
                    transform: translateY(-12px) scale(0.8);
                }

                to {
                    opacity: 1;
                    transform: translateY(0) scale(1);
                }
            }
        </style>
        """,

        "</defs>",

        (
            f'<text '
            f'x="20" '
            f'y="22" '
            f'font-family="monospace" '
            f'font-size="11" '
            f'fill="{MUTED}">'
            f'{escape(username)}@github '
            f'~ contributions'
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
                int(day["level"]),
            ),
        )

        fill = PALETTE[level]

        delay = (
            0.015
            + (column + row) * 0.018
        )

        svg.append(
            (
                f'<rect '
                f'class="contribution" '
                f'x="{x}" '
                f'y="{y}" '
                f'width="{CELL}" '
                f'height="{CELL}" '
                f'rx="2" '
                f'fill="{fill}" '
                f'style="animation-delay:{delay:.3f}s"/>'
            )
        )

    legend_x = 665
    legend_y = 125

    svg.append(
        (
            f'<text '
            f'x="{legend_x - 42}" '
            f'y="{legend_y + 10}" '
            f'font-family="monospace" '
            f'font-size="10" '
            f'fill="{MUTED}">'
            f'Less'
            f'</text>'
        )
    )

    for index, color in enumerate(
        PALETTE
    ):

        x = (
            legend_x
            + index * 16
        )

        svg.append(
            (
                f'<rect '
                f'x="{x}" '
                f'y="{legend_y}" '
                f'width="11" '
                f'height="11" '
                f'rx="2" '
                f'fill="{color}"/>'
            )
        )

    svg.append(
        (
            f'<text '
            f'x="{legend_x + 101}" '
            f'y="{legend_y + 10}" '
            f'font-family="monospace" '
            f'font-size="10" '
            f'fill="{MUTED}">'
            f'More'
            f'</text>'
        )
    )

    svg.append(
        (
            f'<text '
            f'x="20" '
            f'y="125" '
            f'font-family="monospace" '
            f'font-size="11" '
            f'fill="{TEXT}">'
            f'{total:,} contributions '
            f'in the last year'
            f'</text>'
        )
    )

    svg.append(
        (
            f'<text '
            f'x="20" '
            f'y="140" '
            f'font-family="monospace" '
            f'font-size="9" '
            f'fill="{MUTED}">'
            f'streak: {current_streak} '
            f'· longest: {longest_streak}'
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