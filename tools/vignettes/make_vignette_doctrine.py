# Vignette de partage générale : assets/og-image.jpg nettoyée (mention « 1200x630 » retirée) et mise au format 1200 x 630.
from PIL import Image, ImageDraw, ImageFilter
src = Image.open("assets/og-image.jpg").convert("RGB")          # 1168 x 784
ImageDraw.Draw(src).rectangle((50, 66, 335, 128), fill=(13, 29, 48))
zone = src.crop((40, 56, 345, 138)).filter(ImageFilter.GaussianBlur(3))
src.paste(zone, (40, 56))
img = src.resize((round(1168 * 630 / 784), 630), Image.LANCZOS)
out = Image.new("RGB", (1200, 630), (13, 29, 48))
out.paste(img, ((1200 - img.width) // 2, 0))
out.save("assets/partage-doctrine.jpg", quality=86, optimize=True)
