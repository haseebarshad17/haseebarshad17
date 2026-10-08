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


def render_mobile(padded, username, total, current_streak, longest_streak):
    """Show the same year in three bands instead of shrinking 53 weeks."""
    width, height = 360, 540
    svg = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
        f'height="{height}" viewBox="0 0 {width} {height}">',
        '<title>GitHub contributions over the last year</title>',
        f'<rect width="{width}" height="{height}" rx="12" fill="{BG}"/>',
        f'<text x="20" y="25" font-family="monospace" font-size="12" '
        f'fill="{TEXT}">{escape(username)}@github</text>',
    ]
    for band in range(3):
        start, stop = band * 18 * 7, (band + 1) * 18 * 7
        band_days = padded[start:stop]
        dated = [day for day in band_days if day is not None]
        if not dated:
            continue
        top = 60 + band * 140
        label = f'{dated[0]["date"]} / {dated[-1]["date"]}'
        svg.append(f'<text x="20" y="{top - 10}" font-family="monospace" '
                   f'font-size="11" fill="{MUTED}">{escape(label)}</text>')
        for index, day in enumerate(band_days):
            if day is None:
                continue
            column, row = divmod(index, 7)
            level = max(0, min(5, int(day.get("level", 0))))
            x, y = 20 + column * 17, top + row * 17
            svg.append(f'<rect x="{x}" y="{y}" width="13" height="13" '
                       f'rx="2" fill="{PALETTE[level]}">'
                       f'<title>{escape(day["date"])}: '
                       f'{int(day.get("count", 0))} contributions</title></rect>')
    svg.extend([
        f'<text x="20" y="478" font-family="monospace" font-size="12" '
        f'fill="{TEXT}">{total:,} contributions in the last year</text>',
        f'<text x="20" y="500" font-family="monospace" font-size="11" '
        f'fill="{MUTED}">streak {current_streak} / longest {longest_streak}</text>',
        f'<text x="20" y="524" font-family="monospace" font-size="10" '
        f'fill="{MUTED}">Less</text>',
    ])
    for index, color in enumerate(PALETTE):
        svg.append(f'<rect x="{55 + index * 17}" y="514" width="13" '
                   f'height="13" rx="2" fill="{color}"/>')
    svg.extend([
        f'<text x="164" y="524" font-family="monospace" font-size="10" '
        f'fill="{MUTED}">More</text>',
        '</svg>',
    ])
    Path("contrib-heatmap-mobile.svg").write_text("\n".join(svg), encoding="utf-8")


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

    render_mobile(padded, username, total, current_streak, longest_streak)

    print(
        f"Created: {OUTPUT}"
    )


if __name__ == "__main__":
    main()