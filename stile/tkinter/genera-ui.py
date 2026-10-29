# Genera le immagini dell'interfaccia (cartella ui/) con la grafica standard AI-OS:
# pannello grafite a vetro, pulsanti a pillola con gradiente oro -> corallo, icona.
# Uso: python genera-ui.py   (rifà tutte le immagini nella cartella ui/ accanto allo script).
# Esempio vero: Remoto\strumenti\sottotitoli (Video con sottotitoli). Cambia misure e nomi per la tua app.

import os
from PIL import Image, ImageDraw, ImageFilter

UI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui")
X = 4  # sovracampionamento per bordi morbidi

PANNELLO = (33, 33, 33, 255)      # vetro #242424 al 72% sullo sfondo #1A1A1A
BORDO = (51, 51, 51, 255)         # bianco all'8% sul vetro
LOG = (29, 29, 29, 255)
ORO_CHIARO, ORO, CORALLO = (255, 193, 94), (245, 166, 35), (255, 107, 107)


def pillola_gradiente(w, h, chiaro=0.0, raggio=None):
    """Gradiente a 135 gradi FFC15E -> F5A623 -> FF6B6B dentro una pillola."""
    W, H = w * X, h * X
    grad = Image.new("RGBA", (W, H))
    px = grad.load()
    for x in range(W):
        for y in range(0, H, 1):
            t = (x / W) * 0.8 + (y / H) * 0.2
            a, b, u = (ORO_CHIARO, ORO, t / 0.55) if t < 0.55 else (ORO, CORALLO, (t - 0.55) / 0.45)
            c = [round(a[i] + (b[i] - a[i]) * u) for i in range(3)]
            c = [round(v + (255 - v) * chiaro) for v in c]
            px[x, y] = (*c, 255)
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, W - 1, H - 1), radius=H // 2 if raggio is None else raggio * X, fill=255)
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    out.paste(grad, (0, 0), mask)
    return out.resize((w, h), Image.LANCZOS)


def pulsante(nome, w, h, pad=8):
    for suff, chiaro, alone in (("", 0.0, 70), ("_hover", 0.12, 120)):
        img = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
        glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(glow).rounded_rectangle((pad, pad + 3, pad + w, pad + h + 1), radius=h // 2, fill=(*ORO, alone))
        img = Image.alpha_composite(img, glow.filter(ImageFilter.GaussianBlur(pad / 2)))
        img.alpha_composite(pillola_gradiente(w, h, chiaro), (pad, pad))
        img.save(os.path.join(UI, nome + suff + ".png"))


def riquadro(nome, w, h, raggio, fondo):
    big = Image.new("RGBA", (w * X, h * X), (0, 0, 0, 0))
    ImageDraw.Draw(big).rounded_rectangle((0, 0, w * X - 1, h * X - 1), radius=raggio * X, fill=fondo, outline=BORDO, width=X)
    big.resize((w, h), Image.LANCZOS).save(os.path.join(UI, nome + ".png"))


def icona(lato=84):
    W = lato * X
    img = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    base = pillola_gradiente(lato, lato, raggio=22).resize((W, W))
    mask = Image.new("L", (W, W), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, W - 1, W - 1), radius=22 * X, fill=255)
    img.paste(base, (0, 0), mask)
    d = ImageDraw.Draw(img)
    s = W / 84
    d.polygon([(34 * s, 20 * s), (34 * s, 44 * s), (54 * s, 32 * s)], fill=(26, 26, 26, 255))      # play
    d.rounded_rectangle((16 * s, 54 * s, 68 * s, 60 * s), radius=3 * s, fill=(26, 26, 26, 255))    # riga 1
    d.rounded_rectangle((26 * s, 65 * s, 58 * s, 71 * s), radius=3 * s, fill=(26, 26, 26, 255))    # riga 2
    img.resize((lato, lato), Image.LANCZOS).save(os.path.join(UI, "icona.png"))


if __name__ == "__main__":
    os.makedirs(UI, exist_ok=True)
    riquadro("pannello_app", 740, 780, 24, PANNELLO)
    riquadro("pannello_log", 696, 150, 16, LOG)
    pulsante("pulsante", 560, 56)
    pulsante("pulsante_small", 320, 46)
    pulsante("pulsante_micro", 140, 34)
    icona()
    print("Immagini rifatte in", UI)
