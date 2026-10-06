from pathlib import Path
import json
import re
import sys

import requests
from bs4 import BeautifulSoup


USERNAME = "haseebarshad17"

URL = f"https://github.com/users/{USERNAME}/contributions"

OUTPUT = Path("data/contributions.json")


def main():
    print(f"Fetching contributions for @{USERNAME}...")

    response = requests.get(
        URL,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/html",
        },
        timeout=30,
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    cells = soup.select(
        "td.ContributionCalendar-day[data-date]"
    )

    if not cells:
        print("Could not find contribution cells.")
        print("GitHub may have changed its HTML structure.")
        sys.exit(1)

    # GitHub's tooltips contain exact contribution counts.
    tooltip_counts = {}

    for tooltip in soup.select("tool-tip[for]"):
        target = tooltip.get("for")

        if not target:
            continue

        text = tooltip.get_text(" ", strip=True)

        match = re.search(
            r"([\d,]+)\s+contributions?",
            text,
            re.IGNORECASE,
        )

        if match:
            count = int(match.group(1).replace(",", ""))
            tooltip_counts[target] = count

    days = []

    for cell in cells:
        date = cell.get("data-date")
        level = int(cell.get("data-level", 0))
        cell_id = cell.get("id")

        count = 0

        if cell_id:
            count = tooltip_counts.get(cell_id, 0)

        days.append({
            "date": date,
            "count": count,
            "level": level,
        })

    days.sort(key=lambda item: item["date"])

    total = sum(day["count"] for day in days)

    result = {
        "username": USERNAME,
        "total": total,
        "days": days,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    OUTPUT.write_text(
        json.dumps(result, indent=2),
        encoding="utf-8",
    )

    print(f"Days: {len(days)}")
    print(f"Total contributions: {total}")
    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    main()