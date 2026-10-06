from pathlib import Path

from PIL import Image


INPUT = Path("source-prepped.png")
OUTPUT = Path("avi-ascii.svg")

# Bright -> dark
RAMP = " .`:-=+*cs#%@"

COLUMNS = 90
CHAR_ASPECT = 0.50

TEXT_COLOR = "#c7cbd1"
BACKGROUND = "#0d1117"

FONT_SIZE = 8
CHAR_WIDTH = 4.8
LINE_HEIGHT = 10


def brightness_to_char(value: int) -> str:
    index = int((255 - value) / 255 * (len(RAMP) - 1))
    return RAMP[index]


def main():
    if not INPUT.exists():
        raise FileNotFoundError(
            "source-prepped.png not found. Run prep_photo.py first."
        )

    image = Image.open(INPUT).convert("L")

    width, height = image.size

    rows = max(
        1,
        round((height / width) * COLUMNS * CHAR_ASPECT),
    )

    image = image.resize((COLUMNS, rows))

    svg_width = int(COLUMNS * CHAR_WIDTH)
    svg_height = int(rows * LINE_HEIGHT)

    lines = []

    for y in range(rows):
        chars = []

        for x in range(COLUMNS):
            pixel = image.getpixel((x, y))
            chars.append(brightness_to_char(pixel))

        lines.append("".join(chars))

    svg = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{svg_width}" height="{svg_height}" '
        f'viewBox="0 0 {svg_width} {svg_height}">',
        f'<rect width="100%" height="100%" fill="{BACKGROUND}"/>',
        (
            f'<g fill="{TEXT_COLOR}" '
            f'font-family="monospace" '
            f'font-size="{FONT_SIZE}px" '
            f'xml:space="preserve">'
        ),
    ]

    for row, text in enumerate(lines):
        y = (row + 1) * LINE_HEIGHT

        # Every row starts invisible and reveals itself using SMIL.
        svg.append(
            f'<text x="0" y="{y}" opacity="0">'
            f'{escape_xml(text)}'
            f'<animate '
            f'attributeName="opacity" '
            f'values="0;1" '
            f'keyTimes="0;1" '
            f'begin="{0.01 + row * 0.035:.3f}s" '
            f'dur="0.35s" '
            f'fill="freeze"/>'
            f'</text>'
        )

    svg.extend([
        "</g>",
        "</svg>",
    ])

    OUTPUT.write_text("\n".join(svg), encoding="utf-8")

    print(f"Created: {OUTPUT}")


def escape_xml(value: str) -> str:
    return (
        value
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


if __name__ == "__main__":
    main()