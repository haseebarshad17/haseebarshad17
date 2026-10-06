from pathlib import Path


OUTPUT = Path("info-card.svg")

USERNAME = "haseebarshad17"

ROLE = "Software Engineer"
STACK = "React / Next.js / React Native"
BACKEND = "Node.js / Supabase"
FOCUS = "Full Stack Development"
BUILDING = "eDaara / Deenify / Servita / Mountspeak"


WIDTH = 490
HEIGHT = 260

BG = "#0d1117"
BORDER = "#30363d"
GREEN = "#39d353"
TEXT = "#c9d1d9"
MUTED = "#8b949e"


def escape(value: str) -> str:
    return (
        value
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def main():
    rows = [
        ("Role", ROLE),
        ("Stack", STACK),
        ("Backend", BACKEND),
        ("Focus", FOCUS),
        ("Building", BUILDING),
    ]

    svg = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{WIDTH}" height="{HEIGHT}" '
            f'viewBox="0 0 {WIDTH} {HEIGHT}">'
        ),

        f'<rect width="100%" height="100%" rx="12" '
        f'fill="{BG}" stroke="{BORDER}"/>',

        # Terminal dots
        f'<circle cx="20" cy="20" r="5" fill="#ff5f56"/>',
        f'<circle cx="38" cy="20" r="5" fill="#ffbd2e"/>',
        f'<circle cx="56" cy="20" r="5" fill="#27c93f"/>',

        f'<text x="78" y="25" '
        f'font-family="monospace" font-size="13" '
        f'fill="{MUTED}">'
        f'{escape(USERNAME)}@github'
        f'</text>',

        f'<line x1="20" y1="45" x2="470" y2="45" '
        f'stroke="{BORDER}"/>',
    ]

    for index, (label, value) in enumerate(rows):
        y = 80 + index * 32
        delay = 0.2 + index * 0.18

        svg.append(
            f'<g opacity="0">'
            f'<text x="25" y="{y}" '
            f'font-family="monospace" font-size="13" '
            f'font-weight="bold" fill="{GREEN}">'
            f'{escape(label):<10}'
            f'</text>'
            f'<text x="125" y="{y}" '
            f'font-family="monospace" font-size="13" '
            f'fill="{TEXT}">'
            f'{escape(value)}'
            f'</text>'
            f'<animate '
            f'attributeName="opacity" '
            f'values="0;1" '
            f'keyTimes="0;1" '
            f'begin="{delay}s" '
            f'dur="0.35s" '
            f'fill="freeze"/>'
            f'</g>'
        )

    svg.extend([
        f'<text x="25" y="240" '
        f'font-family="monospace" font-size="13" '
        f'fill="{GREEN}">'
        f'$ whoami_'
        f'</text>',
        "</svg>",
    ])

    OUTPUT.write_text("\n".join(svg), encoding="utf-8")

    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    main()