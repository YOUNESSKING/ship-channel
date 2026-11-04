"""Spectrogram contact sheet of every kit sound (log frequency 20 Hz - 16 kHz, 0-6 s): a quick visual check after a re-make.
python3 kit/ship/sfx/spectro_sheet.py  -> kit/ship/sfx/spectro_sheet.jpg"""
import glob, os, numpy as np, soundfile as sf
from scipy import signal
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); W, H, COLS = 300, 90, 6
FONT = ImageFont.truetype(os.path.join(HERE, "../../../tools/fonts/Anton-Regular.ttf"), 13)
files = sorted(glob.glob(os.path.join(HERE, "out", "*_[0-9].wav")))
rows = (len(files) + COLS - 1) // COLS
sheet = Image.new("RGB", (COLS * W, rows * (H + 18)), (12, 16, 22)); d = ImageDraw.Draw(sheet)
for k, f in enumerate(files):
    x, sr = sf.read(f); x = x.mean(1)[: sr * 6]
    fr, t, S = signal.stft(x, sr, nperseg=2048, noverlap=1536)
    S = 20 * np.log10(np.abs(S) + 1e-9)
    ly = np.geomspace(20, 16000, H)[::-1]; cols = np.linspace(0, 6, W) * sr / 512
    img = np.full((H, W), -120.0)
    for j, c in enumerate(cols.astype(int)):
        if c < S.shape[1]: img[:, j] = np.interp(ly, fr, S[:, c])
    v = np.clip((img + 90) / 70, 0, 1)
    rgb = np.stack([v ** 0.8 * 255, v ** 1.2 * 220, (0.35 + 0.65 * v) * v * 255 + 25 * (1 - v)], -1).astype(np.uint8)
    X, Y = (k % COLS) * W, (k // COLS) * (H + 18)
    sheet.paste(Image.fromarray(rgb), (X, Y + 18)); d.text((X + 4, Y + 1), os.path.basename(f)[:-4], font=FONT, fill=(230, 222, 200))
sheet.save(os.path.join(HERE, "spectro_sheet.jpg"), quality=82); print("wrote spectro_sheet.jpg", sheet.size)
