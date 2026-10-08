from pathlib import Path
from datetime import datetime
import json
import math


INPUT = Path("data/contributions.json")
OUTPUT = Path("info-card.svg")

WIDTH = 490
HEIGHT = 370

BG = "#0d1117"
PANEL = "#161b22"
BORDER = "#30363d"
TEXT = "#c9d1d9"
MUTED = "#8b949e"
GREEN = "#39d353"
GREEN_DARK = "#0e4429"


def esc(value):
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def text(x, y, value, size=10, fill=TEXT, weight="normal"):
    return (
        f'<text x="{x}" y="{y}" '
        f'font-family="monospace" '
        f'font-size="{size}px" '
        f'font-weight="{weight}" '
        f'fill="{fill}">'
        f'{esc(value)}</text>'
    )


def line(x1, y1, x2, y2, fill=BORDER):
    return (
        f'<line x1="{x1}" y1="{y1}" '
        f'x2="{x2}" y2="{y2}" '
        f'stroke="{fill}" stroke-width="1"/>'
    )


def metric(svg, x, y, label, value):
    svg.append(text(x, y, label.upper(), 7, MUTED))
    svg.append(
        text(
            x,
            y + 17,
            value,
            13,
            TEXT,
            "bold",
        )
    )


def bar(svg, x, y, width, value, maximum):
    ratio = 0 if maximum == 0 else value / maximum
    ratio = max(0, min(1, ratio))

    svg.append(
        f'<rect x="{x}" y="{y}" width="{width}" height="5" '
        f'rx="2.5" fill="{GREEN_DARK}"/>'
    )

    svg.append(
        f'<rect x="{x}" y="{y}" width="{width * ratio:.1f}" '
        f'height="5" rx="2.5" fill="{GREEN}"/>'
    )


def render_mobile(metrics, weekday_names, weekday_totals):
    """Reflow all desktop metrics into two readable columns for phones."""
    width, height = 360, 640
    svg = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
        f'height="{height}" viewBox="0 0 {width} {height}">',
        '<title>GitHub engineering telemetry</title>',
        f'<rect width="{width}" height="{height}" rx="10" '
        f'fill="{BG}" stroke="{BORDER}"/>',
        text(18, 28, "ENGINEERING TELEMETRY", 14, TEXT, "bold"),
        text(18, 47, "github activity / 365 day window", 11, MUTED),
        line(18, 60, 342, 60),
        text(18, 79, "ACTIVITY", 11, GREEN, "bold"),
    ]
    for index, (label, value) in enumerate(metrics):
        if index < 8:
            row = index // 2
            y = 100 + row * 48
        else:
            row = (index - 8) // 2
            y = 322 + row * 48
        x = 18 + (index % 2) * 162
        svg.append(text(x, y, label.upper(), 10, MUTED))
        svg.append(text(x, y + 21, value, 18, TEXT, "bold"))
    svg.extend([
        line(18, 280, 342, 280),
        text(18, 301, "ENGINEERING SIGNALS", 11, GREEN, "bold"),
        line(18, 409, 342, 409),
        text(18, 431, "ACTIVITY DISTRIBUTION", 11, GREEN, "bold"),
    ])
    maximum = max(weekday_totals)
    for index, value in enumerate(weekday_totals):
        y = 450 + index * 22
        svg.append(text(18, y + 6, weekday_names[index], 10, MUTED))
        bar(svg, 56, y, 225, value, maximum)
        svg.append(text(291, y + 6, f"{value:,}", 10))
    svg.extend([
        line(18, 610, 342, 610),
        text(18, 628, "PUBLIC GITHUB TELEMETRY", 10, MUTED),
        "</svg>",
    ])
    Path("info-card-mobile.svg").write_text("\n".join(svg), encoding="utf-8")


def main():
    if not INPUT.exists():
        raise FileNotFoundError(
            "data/contributions.json not found."
        )

    data = json.loads(
        INPUT.read_text(encoding="utf-8")
    )

    days = sorted(
        data.get("days", []),
        key=lambda item: item["date"],
    )

    if not days:
        raise ValueError(
            "No contribution data found."
        )

    days = days[-365:]

    total = sum(
        day.get("count", 0)
        for day in days
    )

    active_days = sum(
        1
        for day in days
        if day.get("count", 0) > 0
    )

    best_day = max(
        days,
        key=lambda day: day.get("count", 0),
    )

    current_streak = data.get(
        "current_streak",
        0,
    )

    longest_streak = data.get(
        "longest_streak",
        0,
    )

    average_day = (
        total / len(days)
        if days
        else 0
    )

    average_active_day = (
        total / active_days
        if active_days
        else 0
    )

    consistency = (
        active_days / len(days) * 100
        if days
        else 0
    )

    # Weekday analysis.
    weekday_totals = [0] * 7

    for day in days:
        date = datetime.strptime(
            day["date"],
            "%Y-%m-%d",
        )

        weekday_totals[
            date.weekday()
        ] += day.get("count", 0)

    weekday_names = [
        "MON",
        "TUE",
        "WED",
        "THU",
        "FRI",
        "SAT",
        "SUN",
    ]

    max_weekday = max(
        weekday_totals
    )

    # Monthly activity.
    monthly = {}

    for day in days:
        month = day["date"][:7]

        monthly[month] = (
            monthly.get(month, 0)
            + day.get("count", 0)
        )

    recent_30 = sum(
        day.get("count", 0)
        for day in days[-30:]
    )

    recent_90 = sum(
        day.get("count", 0)
        for day in days[-90:]
    )

    previous_30 = sum(
        day.get("count", 0)
        for day in days[-60:-30]
    )

    growth = 0

    if previous_30:
        growth = (
            (recent_30 - previous_30)
            / previous_30
            * 100
        )

    # Activity index.
    #
    # This is a derived indicator, not a GitHub metric.
    # It combines volume, consistency and streak.
    volume_score = min(
        100,
        (total / 1000) * 40,
    )

    consistency_score = (
        consistency * 0.4
    )

    streak_score = min(
        20,
        longest_streak / 5,
    )

    activity_index = min(
        100,
        volume_score
        + consistency_score
        + streak_score,
    )

    svg = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{WIDTH}" height="{HEIGHT}" '
            f'viewBox="0 0 {WIDTH} {HEIGHT}">'
        ),

        f'<rect width="{WIDTH}" height="{HEIGHT}" '
        f'rx="10" fill="{BG}" '
        f'stroke="{BORDER}" stroke-width="1"/>',

        # Header
        text(
            18,
            23,
            "ENGINEERING TELEMETRY",
            10,
            TEXT,
            "bold",
        ),

        text(
            18,
            37,
            "github activity · 365 day window",
            7,
            MUTED,
        ),

        text(
            420,
            23,
            "● LIVE",
            8,
            GREEN,
            "bold",
        ),

        line(18, 49, 472, 49),

        # Core metrics
        text(
            18,
            65,
            "ACTIVITY",
            7,
            GREEN,
            "bold",
        ),
    ]

    metric(
        svg,
        18,
        80,
        "Contributions",
        f"{total:,}",
    )

    metric(
        svg,
        125,
        80,
        "Active Days",
        f"{active_days}/{len(days)}",
    )

    metric(
        svg,
        235,
        80,
        "Current Streak",
        f"{current_streak}d",
    )

    metric(
        svg,
        335,
        80,
        "Longest Streak",
        f"{longest_streak}d",
    )

    metric(
        svg,
        18,
        124,
        "Avg / Day",
        f"{average_day:.1f}",
    )

    metric(
        svg,
        125,
        124,
        "Avg Active Day",
        f"{average_active_day:.1f}",
    )

    metric(
        svg,
        235,
        124,
        "Best Day",
        str(best_day.get("count", 0)),
    )

    metric(
        svg,
        335,
        124,
        "Consistency",
        f"{consistency:.0f}%",
    )

    # Intelligence section
    svg.extend([
        line(18, 163, 472, 163),
        text(
            18,
            180,
            "ENGINEERING SIGNALS",
            7,
            GREEN,
            "bold",
        ),
    ])

    metric(
        svg,
        18,
        195,
        "Activity Index",
        f"{activity_index:.0f}/100",
    )

    metric(
        svg,
        145,
        195,
        "30D Activity",
        f"{recent_30:,}",
    )

    metric(
        svg,
        270,
        195,
        "90D Activity",
        f"{recent_90:,}",
    )

    growth_label = (
        f"+{growth:.0f}%"
        if growth >= 0
        else f"{growth:.0f}%"
    )

    metric(
        svg,
        380,
        195,
        "30D Trend",
        growth_label,
    )

    # Weekday distribution
    svg.extend([
        line(18, 236, 472, 236),
        text(
            18,
            253,
            "ACTIVITY DISTRIBUTION",
            7,
            GREEN,
            "bold",
        ),
    ])

    for index, value in enumerate(
        weekday_totals
    ):
        y = 267 + index * 11

        svg.append(
            text(
                18,
                y + 5,
                weekday_names[index],
                6,
                MUTED,
            )
        )

        bar(
            svg,
            52,
            y,
            330,
            value,
            max_weekday,
        )

        svg.append(
            text(
                395,
                y + 5,
                f"{value:,}",
                6,
                TEXT,
            )
        )

    # Footer
    svg.extend([
        line(18, 345, 472, 345),

        text(
            18,
            360,
            "PUBLIC GITHUB TELEMETRY",
            6,
            MUTED,
        ),

        text(
            350,
            360,
            "DATA → CONTRIBUTIONS",
            6,
            MUTED,
        ),

        "</svg>",
    ])

    OUTPUT.write_text(
        "\n".join(svg),
        encoding="utf-8",
    )

    render_mobile(
        [
            ("Contributions", f"{total:,}"),
            ("Active Days", f"{active_days}/{len(days)}"),
            ("Current Streak", f"{current_streak}d"),
            ("Longest Streak", f"{longest_streak}d"),
            ("Avg / Day", f"{average_day:.1f}"),
            ("Avg Active Day", f"{average_active_day:.1f}"),
            ("Best Day", str(best_day.get("count", 0))),
            ("Consistency", f"{consistency:.0f}%"),
            ("Activity Index", f"{activity_index:.0f}/100"),
            ("30D Activity", f"{recent_30:,}"),
            ("90D Activity", f"{recent_90:,}"),
            ("30D Trend", growth_label),
        ],
        weekday_names,
        weekday_totals,
    )

    print(f"Created: {OUTPUT} and info-card-mobile.svg")


if __name__ == "__main__":
    main()