from pathlib import Path
import sys

import cv2
import numpy as np
from PIL import Image
from rembg import remove


INPUT = Path("source-photo.jpg")
OUTPUT = Path("source-prepped.png")


def main():
    source = INPUT

    if len(sys.argv) == 2:
        source = Path(sys.argv[1])

    if not source.exists():
        print(f"File not found: {source}")
        sys.exit(1)

    print("Loading photo...")
    image = Image.open(source).convert("RGBA")

    print("Removing background...")
    no_background = remove(image)

    rgba = np.array(no_background)

    alpha = rgba[:, :, 3]
    rgb = rgba[:, :, :3]

    white = np.full_like(rgb, 255)

    alpha_f = alpha[:, :, None] / 255.0

    composited = (
        rgb * alpha_f
        + white * (1 - alpha_f)
    ).astype(np.uint8)

    print("Converting to grayscale...")

    gray = cv2.cvtColor(
        composited,
        cv2.COLOR_RGB2GRAY,
    )

    print("Enhancing local contrast...")

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8),
    )

    enhanced = clahe.apply(gray)

    enhanced = cv2.normalize(
        enhanced,
        None,
        0,
        255,
        cv2.NORM_MINMAX,
    )

    cv2.imwrite(
        str(OUTPUT),
        enhanced,
    )

    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    main()