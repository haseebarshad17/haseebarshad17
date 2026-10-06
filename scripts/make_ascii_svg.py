from pathlib import Path

from PIL import Image


INPUT = Path("source-prepped.png")
OUTPUT = Path("avi-ascii.svg")

RAMP = " .`:-=+*cs#%@"

COLUMNS = 100
CHAR_ASPECT = 0.50

FONT_SIZE = 8
CHAR_WIDTH = 4.8
LINE_HEIGHT = 10

TEXT_COLOR = "#c7cbd1"
BACKGROUND = "#0d1117"
CURSOR_COLOR = "#39d353"


def brightness_to_char(value: int) -> str:
    index = int(
        (255 - value)
        / 255
        * (len(RAMP) - 1)
    )

    return RAMP[index]


def escape_xml(value: str) -> str:
    return (
        value
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def main():
    if not INPUT.exists():
        raise FileNotFoundError(
            "source-prepped.png not found. "
            "Run prep_photo.py first."
        )

    image = Image.open(INPUT).convert("L")

    width, height = image.size

    rows = max(
        1,
        round(
            (height / width)
            * COLUMNS
            * CHAR_ASPECT
        ),
    )

    image = image.resize(
        (COLUMNS, rows)
    )

    svg_width = int(
        COLUMNS * CHAR_WIDTH
    )

    svg_height = int(
        rows * LINE_HEIGHT
    )

    svg = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{svg_width}" '
            f'height="{svg_height}" '
            f'viewBox="0 0 {svg_width} {svg_height}">'
        ),

        (
            f'<rect width="100%" height="100%" '
            f'fill="{BACKGROUND}"/>'
        ),

        "<defs>",
        """
        <style>
            .ascii-row {
                animation-timing-function: ease-out;
                animation-fill-mode: forwards;
            }

            @keyframes reveal {
                from {
                    opacity: 0;
                    transform: translateX(-12px);
                }

                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }

            @keyframes cursorReveal {
                from {
                    opacity: 1;
                }

                to {
                    opacity: 0;
                }
            }
        </style>
        """,
        "</defs>",
    ]

    for row in range(rows):

        chars = []

        for x in range(COLUMNS):
            pixel = image.getpixel((x, row))
            chars.append(
                brightness_to_char(pixel)
            )

        line = "".join(chars)

        y = (row + 1) * LINE_HEIGHT

        delay = 0.03 + row * 0.045

        clip_id = f"row-clip-{row}"

        svg.append(
            f'<clipPath id="{clip_id}">'
            f'<rect '
            f'x="0" '
            f'y="{row * LINE_HEIGHT}" '
            f'width="0" '
            f'height="{LINE_HEIGHT + 2}">'
            f'<animate '
            f'attributeName="width" '
            f'from="0" '
            f'to="{svg_width}" '
            f'begin="{delay:.3f}s" '
            f'dur="0.55s" '
            f'fill="freeze"/>'
            f'</rect>'
            f'</clipPath>'
        )

        safe_line = escape_xml(line)

        svg.append(
            f'<g clip-path="url(#{clip_id})">'
        )

        svg.append(
            f'<text '
            f'x="0" '
            f'y="{y}" '
            f'fill="{TEXT_COLOR}" '
            f'font-family="monospace" '
            f'font-size="{FONT_SIZE}px" '
            f'xml:space="preserve">'
            f'{safe_line}'
            f'</text>'
        )

        svg.append("</g>")

        cursor_x = 0

        svg.append(
            f'<rect '
            f'x="{cursor_x}" '
            f'y="{row * LINE_HEIGHT}" '
            f'width="5" '
            f'height="{LINE_HEIGHT}" '
            f'fill="{CURSOR_COLOR}" '
            f'opacity="0">'
            f'<animate '
            f'attributeName="opacity" '
            f'values="0;1;1;0" '
            f'keyTimes="0;0.1;0.8;1" '
            f'begin="{delay:.3f}s" '
            f'dur="0.55s" '
            f'fill="freeze"/>'
            f'</rect>'
        )

    svg.append("</svg>")

    OUTPUT.write_text(
        "\n".join(svg),
        encoding="utf-8",
    )

    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    main()