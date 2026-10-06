from pathlib import Path
from collections import defaultdict
from datetime import datetime, timedelta
import json
import re
import sys

import requests
from bs4 import BeautifulSoup


USERNAME = "haseebarshad17"

URL = (
    f"https://github.com/users/"
    f"{USERNAME}/contributions"
)

OUTPUT = Path(
    "data/contributions.json"
)


def parse_count(text):

    match = re.search(
        r"([\d,]+)\s+contributions?",
        text,
        re.IGNORECASE,
    )

    if not match:
        return 0

    return int(
        match.group(1).replace(",", "")
    )


def calculate_streaks(days):

    counts = {
        day["date"]: day["count"]
        for day in days
    }

    dates = sorted(counts)

    current_streak = 0

    longest_streak = 0
    running = 0

    today = datetime.utcnow().date()

    for date_string in reversed(dates):

        date = datetime.strptime(
            date_string,
            "%Y-%m-%d",
        ).date()

        if date > today:
            continue

        if counts[date_string] > 0:

            if (
                date == today
                or date == today - timedelta(days=1)
            ):
                current_streak += 1
                today = date

        else:
            if date < today:
                break

    for date_string in dates:

        if counts[date_string] > 0:
            running += 1
            longest_streak = max(
                longest_streak,
                running,
            )
        else:
            running = 0

    return current_streak, longest_streak


def main():

    print(
        f"Fetching contributions "
        f"for @{USERNAME}..."
    )

    response = requests.get(
        URL,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/html",
        },
        timeout=30,
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser",
    )

    cells = soup.select(
        "td.ContributionCalendar-day"
    )

    if not cells:
        print(
            "Could not find contribution cells."
        )

        print(
            "GitHub may have changed "
            "its HTML structure."
        )

        sys.exit(1)

    tooltip_counts = {}

    for tooltip in soup.select(
        "tool-tip[for]"
    ):

        target = tooltip.get("for")

        if not target:
            continue

        text = tooltip.get_text(
            " ",
            strip=True,
        )

        tooltip_counts[target] = parse_count(
            text
        )

    days = []

    for cell in cells:

        date = cell.get(
            "data-date"
        )

        if not date:
            continue

        level = int(
            cell.get(
                "data-level",
                0,
            )
        )

        cell_id = cell.get("id")

        count = 0

        if cell_id:
            count = tooltip_counts.get(
                cell_id,
                0,
            )

        days.append(
            {
                "date": date,
                "count": count,
                "level": level,
            }
        )

    days.sort(
        key=lambda item: item["date"]
    )

    total = sum(
        day["count"]
        for day in days
    )

    current_streak, longest_streak = (
        calculate_streaks(days)
    )

    best_day = max(
        days,
        key=lambda item: item["count"],
    )

    monthly_totals = defaultdict(int)

    for day in days:

        month = day["date"][:7]

        monthly_totals[month] += (
            day["count"]
        )

    result = {
        "username": USERNAME,
        "total": total,

        "current_streak":
            current_streak,

        "longest_streak":
            longest_streak,

        "best_day": {
            "date": best_day["date"],
            "count": best_day["count"],
        },

        "monthly_totals":
            dict(monthly_totals),

        "days": days,
    }

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT.write_text(
        json.dumps(
            result,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(
        f"Days: {len(days)}"
    )

    print(
        f"Total contributions: {total}"
    )

    print(
        f"Current streak: "
        f"{current_streak}"
    )

    print(
        f"Longest streak: "
        f"{longest_streak}"
    )

    print(
        f"Best day: "
        f"{best_day['date']} "
        f"({best_day['count']})"
    )

    print(
        f"Created: {OUTPUT}"
    )


if __name__ == "__main__":
    main()