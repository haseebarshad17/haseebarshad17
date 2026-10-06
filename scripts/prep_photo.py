from pathlib import Path
import sys

import cv2
import numpy as np
from PIL import Image
from rembg import remove


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/prep_photo.py source-photo.jpg")
        sys.exit(1)

    source = Path(sys.argv[1])

    if not source.exists():
        print(f"File not found: {source}")
        sys.exit(1)

    print("Removing background...")

    image = Image.open(source).convert("RGBA")
    no_background = remove(image)

    rgba = np.array(no_background)

    alpha = rgba[:, :, 3]
    rgb = rgba[:, :, :3]

    # White background
    white = np.full_like(rgb, 255)
    alpha_f = alpha[:, :, None] / 255.0

    composited = (
        rgb * alpha_f +
        white * (1 - alpha_f)
    ).astype(np.uint8)

    # Grayscale
    gray = cv2.cvtColor(composited, cv2.COLOR_RGB2GRAY)

    # Improve local contrast
    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8),
    )

    enhanced = clahe.apply(gray)

    # Slightly increase contrast
    enhanced = cv2.normalize(
        enhanced,
        None,
        0,
        255,
        cv2.NORM_MINMAX,
    )

    output = Path("source-prepped.png")

    cv2.imwrite(str(output), enhanced)

    print(f"Created: {output}")


if __name__ == "__main__":
    main()