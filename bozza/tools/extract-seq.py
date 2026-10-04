"""Video -> WebP frame sequence for the "Giorgia ti guida" canvas.

Usage: python3 bozza/tools/extract-seq.py <video.mp4> [fps=24] [width=480]

1. ffmpeg extracts PNG frames (this ffmpeg build has no libwebp encoder).
2. The backdrop colour is sampled from the first frame's edges and printed:
   paste it into --bg in bozza/styles.css.
3. Every frame is divided by that colour, so the backdrop becomes white.
   Drawn with mix-blend-mode: multiply over --bg, the canvas then reproduces
   the original image exactly and the video rectangle disappears.
   (Multiply can never be lighter than --bg: the few highlights brighter than
   the backdrop are capped at it.)
4. Frames are saved as WebP q78 in bozza/assets/seq/f_001.webp ...
After a new video: update BEATS and FRAME_COUNT in bozza/main.js.
"""
import glob
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

OUT = Path(__file__).resolve().parent.parent / "assets" / "seq"


def main() -> None:
    video = sys.argv[1]
    fps = sys.argv[2] if len(sys.argv) > 2 else "24"
    width = sys.argv[3] if len(sys.argv) > 3 else "480"
    tmp = tempfile.mkdtemp()
    subprocess.run(["ffmpeg", "-v", "error", "-i", video, "-vf", f"fps={fps},scale={width}:-2",
                    f"{tmp}/f_%03d.png"], check=True)
    frames = sorted(glob.glob(f"{tmp}/f_*.png"))

    first = np.asarray(Image.open(frames[0]).convert("RGB")).astype(np.float32)
    edge = np.concatenate([first[:60, :60].reshape(-1, 3), first[:60, -60:].reshape(-1, 3),
                           first[:, :20].reshape(-1, 3), first[:, -20:].reshape(-1, 3)])
    bg = np.median(edge, axis=0)
    print("--bg:", "#%02X%02X%02X" % tuple(int(round(c)) for c in bg), "rgb", bg)

    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("f_*.webp"):
        old.unlink()
    for f in frames:
        a = np.asarray(Image.open(f).convert("RGB")).astype(np.float32)
        norm = np.clip(a / bg * 255, 0, 255).astype(np.uint8)
        Image.fromarray(norm).save(OUT / (Path(f).stem + ".webp"), quality=78, method=6)
    shutil.rmtree(tmp)
    total = sum(p.stat().st_size for p in OUT.glob("f_*.webp"))
    print(f"{len(frames)} frames, {total / 1024 / 1024:.2f} MB -> {OUT}")


if __name__ == "__main__":
    main()
