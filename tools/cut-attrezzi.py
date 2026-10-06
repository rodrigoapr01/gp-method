"""Scontorna le foto degli attrezzi (assets/attrezzi/src) e salva PNG + WebP con alpha in assets/attrezzi/.

Richiede: pip install "rembg[cpu]" onnxruntime pillow numpy scipy
Uso: python tools/cut-attrezzi.py
"""
from pathlib import Path

import numpy as np
from PIL import Image
from rembg import new_session, remove
from scipy.ndimage import binary_closing, binary_fill_holes, grey_erosion

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'assets/attrezzi/src'
OUT = ROOT / 'assets/attrezzi'
JOBS = {  # sorgente -> (nome, lato massimo)
    'gp-manubrio.webp': ('manubrio', 1200),
    'gp-kettlebell.webp': ('kettlebell', 1200),
    'gp-disco-bumper.webp': ('disco', 1200),
    'gp-palla-medica.webp': ('palla', 1200),
    'gp-bilanciere.webp': ('bilanciere', 2000),
}

session = new_session('isnet-general-use')

for src, (name, max_side) in JOBS.items():
    img = Image.open(SRC / src).convert('RGB')
    cut = remove(img, session=session, alpha_matting=True,
                 alpha_matting_foreground_threshold=240,
                 alpha_matting_background_threshold=10,
                 alpha_matting_erode_size=10)
    rgba = np.asarray(cut.convert('RGBA')).astype(np.float32)
    a = rgba[..., 3] / 255

    if name == 'bilanciere':
        # the shiny middle of the bar reflects the white backdrop and rembg punches a hole in it:
        # bridge it vertically, fill it with the original pixels (the kettlebell handle hole is real, so only here)
        solid = binary_fill_holes(binary_closing(a > 0.5, structure=np.ones((25, 1)), iterations=1))
        holes = solid & (a < 1)
        rgba[holes, :3] = np.asarray(img).astype(np.float32)[holes]
        a[holes] = 1

    # erode the alpha by 1px: the outermost ring is where the white background bleeds in
    a = grey_erosion(a, size=(3, 3))
    a[a < 0.04] = 0

    # un-mix the white background from semi-transparent edge pixels: c = (c - (1-a)*255) / a
    rgb = rgba[..., :3]
    edge = (a > 0) & (a < 1)
    aa = np.maximum(a, 1e-3)[..., None]
    rgb = np.where(edge[..., None], np.clip((rgb - (1 - aa) * 255) / aa, 0, 255), rgb)

    out = Image.fromarray(np.dstack([rgb, a * 255]).round().astype(np.uint8), 'RGBA')
    out = out.crop(out.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox())
    out.thumbnail((max_side, max_side), Image.LANCZOS)
    out.save(OUT / f'{name}.png', optimize=True)
    out.save(OUT / f'{name}.webp', quality=82, method=6)
    print(name, out.size,
          (OUT / f'{name}.png').stat().st_size // 1024, 'KB png',
          (OUT / f'{name}.webp').stat().st_size // 1024, 'KB webp')
