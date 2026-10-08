"""Open Graph image for GP METHOD (link preview on WhatsApp, Instagram, Facebook): the metal logo, 600px high,
centred on #E2D9D0 (the tone of the render, so its edges disappear), 1200x630. Run: python3 tools/build-assets.py
Favicons come ready-made in assets/brand/lineare. After changing the image, bump ?v= in OG_IMAGE (build-pages.py)."""
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def main():
    n = 600
    logo = Image.open(ROOT / "assets/chiaro/logo-metallo-900.jpg").convert("RGB").resize((n, n), Image.LANCZOS)
    # circular fade, as on the home band: opaque to 94% of the radius, transparent at the edge
    y, x = np.mgrid[0:n, 0:n]
    r = np.hypot(x - (n - 1) / 2, y - (n - 1) / 2) / (n / 2)
    mask = Image.fromarray((np.clip((1 - r) / 0.06, 0, 1) * 255).astype("uint8"))
    og = Image.new("RGB", (1200, 630), (0xE2, 0xD9, 0xD0))
    og.paste(logo, ((1200 - n) // 2, (630 - n) // 2), mask)
    (ROOT / "assets/og").mkdir(exist_ok=True)
    og.save(ROOT / "assets/og/og-gp-method.jpg", quality=90, optimize=True, progressive=True)
    print("og-gp-method.jpg", og.size)


if __name__ == "__main__":
    main()
