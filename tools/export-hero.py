"""Export the hero portrait: 4:5 crop, warm grade on neutral pixels only, AVIF/WebP/JPG at 3 widths.

Usage: python3 tools/export-hero.py <source-image> [crop_left crop_top crop_width]
The skin and any saturated colour are left untouched; only grey/black pixels
(backdrop, black clothing) are pulled toward the GP METHOD espresso/bronze.
Needs Pillow (with AVIF) and numpy.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

OUT = Path(__file__).resolve().parent.parent / "assets" / "img"
WIDTHS = (480, 800, 1200)

# Warm target for neutrals: espresso #2A2017 in the shadows, bronze-tinted greys above.
SHADOW = np.array([42, 32, 23], dtype=np.float32)
WARM = np.array([1.00, 0.89, 0.79], dtype=np.float32)
STRENGTH = 0.7


def grade(img: Image.Image) -> Image.Image:
    rgb = np.asarray(img.convert("RGB"), dtype=np.float32)
    mx, mn = rgb.max(axis=2), rgb.min(axis=2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)
    lum = (0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2])
    # 1 on neutral pixels, fading to 0 by saturation 0.22 (skin sits well above);
    # highlights (white logo, catchlights) stay untouched.
    mask = np.clip((0.22 - sat) / 0.12, 0, 1) * np.clip((190 - lum) / 60, 0, 1)
    # Blur the mask so fabric noise does not turn into blotches.
    mask_img = Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6))
    mask = (np.asarray(mask_img, dtype=np.float32) / 255)[..., None] * STRENGTH
    warm = np.clip(SHADOW * (1 - lum[..., None] / 255) + lum[..., None] * WARM, 0, 255)
    out = rgb * (1 - mask) + warm * mask
    return Image.fromarray(out.astype(np.uint8))


def main() -> None:
    src = Image.open(sys.argv[1]).convert("RGB")
    if len(sys.argv) >= 5:
        left, top, width = map(int, sys.argv[2:5])
    else:  # default crop for chisono3.png (2048 x 2048)
        left, top, width = 446, 0, 1200
    crop = src.crop((left, top, left + width, top + int(width * 5 / 4)))
    graded = grade(crop)
    OUT.mkdir(parents=True, exist_ok=True)
    for w in WIDTHS:
        im = graded.resize((w, int(w * 5 / 4)), Image.LANCZOS)
        im.save(OUT / f"giorgia-{w}.avif", quality=58)
        im.save(OUT / f"giorgia-{w}.webp", quality=80, method=6)
        im.save(OUT / f"giorgia-{w}.jpg", quality=82, optimize=True, progressive=True)
    for f in sorted(OUT.glob("giorgia-*")):
        print(f.name, f.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
