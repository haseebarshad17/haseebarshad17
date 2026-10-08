from pathlib import Path
import xml.etree.ElementTree as ET


NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)


def compose(output, width, height, panels):
    """Embed original SVG artwork so layout cannot wrap on desktop."""
    root = ET.Element(f"{{{NS}}}svg", {
        "width": str(width), "height": str(height),
        "viewBox": f"0 0 {width} {height}",
    })
    ET.SubElement(root, f"{{{NS}}}title").text = (
        "Haseeb Arshad: ASCII portrait and GitHub analytics"
    )
    for source, x, y, panel_width, panel_height in panels:
        panel = ET.parse(source).getroot()
        panel.set("x", str(x))
        panel.set("y", str(y))
        panel.set("width", str(panel_width))
        panel.set("height", str(panel_height))
        root.append(panel)
    ET.ElementTree(root).write(output, encoding="utf-8", xml_declaration=True)
    print(f"Created: {output}")


def main():
    # Original desktop widths and the analytics card's one-line top offset.
    portrait_height = 370 * 500 / 480
    compose("profile-cards.svg", 860, 386, [
        ("avi-ascii.svg", 0, 0, 370, portrait_height),
        ("info-card.svg", 370, 16, 490, 370),
    ])
    compose("profile-cards-mobile.svg", 360, 1031, [
        ("avi-ascii.svg", 0, 0, 360, 375),
        ("info-card-mobile.svg", 0, 391, 360, 640),
    ])


if __name__ == "__main__":
    main()
