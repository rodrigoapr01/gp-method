"""Logo snippets, favicon and Open Graph image for GP METHOD v4.
Logo paths come untouched from assets/brand/svg; only the fill becomes currentColor."""
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance

ROOT = Path(__file__).resolve().parents[1]
BRAND = ROOT / "assets/brand"
OUT = ROOT / "assets/img"
PIETRA, NERO = (0xE0, 0xE2, 0xDB), (0x19, 0x17, 0x16)


def paths(name):
    s = re.sub(r"<metadata>.*?</metadata>", "", (BRAND / f"svg/{name}.svg").read_text(), flags=re.S)
    return "".join(re.sub(r'\sfill="[^"]*"', "", p) for p in re.findall(r"<path [^>]+/>", s))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    logo = paths("GP-METHOD_senza-cerchio_trasparente-scuro")
    mono = paths("GP-METHOD_solo-GP_trasparente-scuro")
    (OUT / "_logo-paths.txt").write_text(logo)  # inlined by the pages (viewBox 300 244 403 499)
    (OUT / "favicon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="262 254 480 492">'
        '<rect x="262" y="254" width="480" height="492" rx="96" fill="#191716"/>'
        f'<g fill="#E0E2DB">{mono}</g></svg>\n')
    # PNG icons and OG from the brand PNGs, recoloured to pietra (alpha kept)
    def recolor(png):
        im = Image.open(BRAND / f"png/{png}.png").convert("RGBA")
        im = im.crop(im.getbbox())
        solid = Image.new("RGBA", im.size, PIETRA + (255,))
        solid.putalpha(im.getchannel("A"))
        return solid
    mono_png = recolor("GP-METHOD_solo-GP_trasparente-scuro")
    for size, name in [(180, "apple-touch-icon.png"), (32, "favicon-32.png")]:
        bg = Image.new("RGBA", (size, size), NERO + (255,))
        m = mono_png.copy(); m.thumbnail((int(size * 0.72),) * 2, Image.LANCZOS)
        bg.alpha_composite(m, ((size - m.width) // 2, (size - m.height) // 2))
        bg.convert("RGB").save(OUT / name)
    # Open Graph 1200x630: the neon wall, a nero veil on the left, the logo over it
    photo = Image.open(ROOT / "assets/palestra/neon-stronger-manubri.jpg").convert("RGB")
    w = photo.width; h = round(w * 630 / 1200)
    shot = photo.crop((0, 0, w, h)).resize((1200, 630), Image.LANCZOS)
    shot = ImageEnhance.Brightness(shot).enhance(0.8)
    og = Image.new("RGBA", (1200, 630), NERO + (255,))
    og.paste(shot, (260, 0))  # the neon moves right, the logo gets the left third
    veil = Image.new("RGBA", og.size, (0, 0, 0, 0)); d = ImageDraw.Draw(veil)
    for x in range(520):
        d.line([(x, 0), (x, 630)], fill=NERO + (255 if x < 260 else int(255 * (1 - (x - 260) / 260)),))
    og.alpha_composite(veil)
    logo_png = recolor("GP-METHOD_senza-cerchio_trasparente-scuro"); logo_png.thumbnail((200, 260), Image.LANCZOS)
    og.alpha_composite(logo_png, (64, (630 - logo_png.height) // 2))
    og.convert("RGB").save(OUT / "og.jpg", quality=85, optimize=True, progressive=True)
    print("ok", logo_png.size)


if __name__ == "__main__":
    main()
