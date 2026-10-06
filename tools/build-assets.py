"""Open Graph image for GP METHOD: the official logo (with circle) centred on nero, 1200x630.
Favicons come ready-made in assets/brand/lineare. Run: python3 tools/build-assets.py"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
NERO = (0x19, 0x17, 0x16)


def main():
    logo = Image.open(ROOT / "assets/brand/lineare/png/GP-METHOD-lineare_con-cerchio_scuro.png").convert("RGB")
    logo = logo.resize((600, 600), Image.LANCZOS)  # the PNG already sits on #191716, so it blends in
    og = Image.new("RGB", (1200, 630), NERO)
    og.paste(logo, ((1200 - 600) // 2, (630 - 600) // 2))
    og.save(ROOT / "assets/img/og.jpg", quality=88, optimize=True, progressive=True)
    print("og.jpg", og.size)


if __name__ == "__main__":
    main()
