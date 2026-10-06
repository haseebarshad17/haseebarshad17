from pathlib import Path
import os


OUTPUT = Path("info-card.svg")

USERNAME = "haseebarshad17"

NOW = "Associate Software Engineer"
PREV = "Full Stack Engineer"
STACK = "React / Next.js / React Native"
HIGHLIGHTS = "Supabase / Node.js / TypeScript"

WIDTH = 490
HEIGHT = 260

BG = "#0d1117"
BORDER = "#30363d"

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


def main():

    static = os.getenv("STATIC") == "1"

    rows = [
        ("Now", NOW),
        ("Prev", PREV),
        ("Stack", STACK),
        ("Highlights", HIGHLIGHTS),
    ]

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
            f'fill="{BG}" '
            f'stroke="{BORDER}"/>'
        ),

        f'<circle cx="20" cy="20" r="5" fill="#ff5f56"/>',
        f'<circle cx="38" cy="20" r="5" fill="#ffbd2e"/>',
        f'<circle cx="56" cy="20" r="5" fill="#27c93f"/>',

        (
            f'<text '
            f'x="78" '
            f'y="25" '
            f'font-family="monospace" '
            f'font-size="13" '
            f'fill="{MUTED}">'
            f'{escape(USERNAME)}@github'
            f'</text>'
        ),

        (
            f'<line '
            f'x1="20" '
            f'y1="45" '
            f'x2="470" '
            f'y2="45" '
            f'stroke="{BORDER}"/>'
        ),
    ]

    for index, (label, value) in enumerate(rows):

        y = 85 + index * 36

        delay = 0 if static else 0.2 + index * 0.18

        if static:
            opacity = "1"

            animation = ""

        else:
            opacity = "0"

            animation = (
                f'<animate '
                f'attributeName="opacity" '
                f'values="0;1" '
                f'keyTimes="0;1" '
                f'begin="{delay:.2f}s" '
                f'dur="0.35s" '
                f'fill="freeze"/>'
            )

        svg.append(
            f'<g opacity="{opacity}">'
        )

        svg.append(
            f'<text '
            f'x="25" '
            f'y="{y}" '
            f'font-family="monospace" '
            f'font-size="13" '
            f'font-weight="bold" '
            f'fill="{GREEN}">'
            f'{escape(label)}'
            f'</text>'
        )

        svg.append(
            f'<text '
            f'x="125" '
            f'y="{y}" '
            f'font-family="monospace" '
            f'font-size="13" '
            f'fill="{TEXT}">'
            f'{escape(value)}'
            f'</text>'
        )

        svg.append(animation)

        svg.append("</g>")

    svg.append(
        f'<text '
        f'x="25" '
        f'y="240" '
        f'font-family="monospace" '
        f'font-size="13" '
        f'fill="{GREEN}">'
        f'$ whoami_'
        f'</text>'
    )

    svg.append("</svg>")

    OUTPUT.write_text(
        "\n".join(svg),
        encoding="UTF-8",
    )

    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    main()