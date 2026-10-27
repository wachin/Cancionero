# -*- coding: utf-8 -*-
"""Genera las tarjetas de acordes y la lamina de sostenidos/bemoles.
Salida: el mismo dibujo en .svg (vectorial) y .png (para el tutorial)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle, Ellipse

OUT = "/home/wachin/Dev/Cancionero/Piano/Wachi Tutorial de piano/Tutorial de piano"
BLUE = "#6FA8DC"
INK = "#1A1A1A"
GREY = "#3A3A3A"

WHITE = ["Do", "Re", "Mi", "Fa", "Sol", "La", "Si"]
SHARP = ["Do#", "Re#", None, "Fa#", "Sol#", "La#", None]
FLAT = ["Reb", "Mib", None, "Solb", "Lab", "Sib", None]
SIB = ["Do#", "Re#", None, "Fa#", "Sol#", "Sib", None]

W, H = 7.85, 5.25
KH = 3.50                     # alto de la tecla blanca
X0, Y0 = 0.65, 0.95
BASE_KW = 0.936               # ancho de tecla cuando hay 7 teclas
KW_BASE = BASE_KW
BKW, BKH = 0.58, 0.59         # proporcion de la tecla negra


def one_card(ax, title, nkeys, notes, black_labels=SHARP, title_size=19, subtitle=None):
    KW = (W - 2 * X0) / nkeys
    y0 = Y0 + (0.40 if subtitle else 0.0)
    HH = H + (0.50 if subtitle else 0.0)
    s = KW / BASE_KW            # escala de fuentes y puntos segun el ancho de tecla
    r = max(0.17, 0.30 * s)
    f_black = max(6.5, 10 * s)
    f_name = max(8.5, 12.5 * s)
    ax.set_xlim(0, W)
    ax.set_ylim(0, HH)
    ax.axis("off")
    ax.set_aspect("equal")
    ax.add_patch(FancyBboxPatch((0.05, 0.05), W - 0.10, HH - 0.10,
                                boxstyle="round,pad=0.02,rounding_size=0.22",
                                facecolor="white", edgecolor="#C9C9C9", lw=2.2, zorder=1))
    ax.text(0.32, HH - 0.30, title, fontsize=title_size, fontweight="bold",
            va="top", ha="left", color=INK, zorder=6)

    # teclas blancas
    for i in range(nkeys):
        ax.add_patch(Rectangle((X0 + i * KW, y0), KW, KH, facecolor="white",
                               edgecolor=INK, lw=1.5, zorder=2))
    # teclas negras
    for i in range(nkeys - 1):
        lab = black_labels[i % 7]
        if lab is None:
            continue
        cx = X0 + (i + 1) * KW
        bw, bh = KW * BKW, KH * BKH
        ax.add_patch(Rectangle((cx - bw / 2, y0 + KH - bh), bw, bh,
                               facecolor="black", edgecolor="black", lw=1.0, zorder=3))
        ax.text(cx, y0 + KH - bh * 0.50, lab, color="white", ha="center", va="center",
                fontsize=f_black, fontweight="bold", zorder=4)
    # nombres debajo
    for i in range(nkeys):
        ax.text(X0 + (i + 0.5) * KW, y0 - 0.42, WHITE[i % 7], ha="center", va="center",
                fontsize=f_name, fontweight="bold", color=GREY, zorder=4)
    # notas del acorde
    for kind, i in notes:
        if kind == "w":
            x, y = X0 + (i + 0.5) * KW, y0 + 0.22 * KH
        else:
            x, y = X0 + (i + 1) * KW, y0 + KH - KH * BKH + 0.30
        ax.add_patch(Circle((x, y), r, facecolor=BLUE, edgecolor="black", lw=1.7, zorder=5))
    if subtitle:
        ax.text(W / 2, 0.45, subtitle, ha="center", va="center", fontsize=10.5,
                fontweight="bold", color=GREY, zorder=4)


def render(cards, name, per_row=3):
    n = len(cards)
    fig = plt.figure(figsize=(W * 0.62 * n, H * 0.62))
    for k, c in enumerate(cards):
        ax = fig.add_axes([k / n, 0.0, 1 / n, 1.0])
        one_card(ax, *c)
    for ext in ("png", "svg"):
        fig.savefig(f"{OUT}/{name}.{ext}", dpi=200, bbox_inches="tight",
                    facecolor="white", format=ext)
    plt.close(fig)
    print("ok", name)


# --- acordes mayores ---
render([("Do Mayor", 7, [("w", 0), ("w", 2), ("w", 4)]),
        ("Re Mayor", 7, [("w", 1), ("b", 3), ("w", 5)]),
        ("Mi Mayor", 7, [("w", 2), ("b", 4), ("w", 6)])],
       "Acordes-de-piano-mayores-Do-Re-Mi")

render([("Fa Mayor", 9, [("w", 3), ("w", 5), ("w", 7)]),
        ("Sol Mayor", 9, [("w", 4), ("w", 6), ("w", 8)])],
       "Acordes-de-piano-mayore-Fa-Sol")

render([("La Mayor", 12, [("w", 5), ("b", 7), ("w", 9)]),
        ("Si Mayor", 12, [("w", 6), ("b", 8), ("b", 10)])],
       "Acordes-de-piano-mayores-La-Si")

# --- acordes menores ---
render([("Do Menor", 7, [("w", 0), ("b", 1), ("w", 4)]),
        ("Re Menor", 7, [("w", 1), ("w", 3), ("w", 5)]),
        ("Mi Menor", 7, [("w", 2), ("w", 4), ("w", 6)])],
       "Acordes-menores-Do-Re-Mi")

render([("Fa Menor", 9, [("w", 3), ("b", 4), ("w", 7)]),
        ("Sol Menor", 9, [("w", 4), ("b", 5), ("w", 8)])],
       "Acordes-menores-Fa-Sol")

render([("La Menor", 12, [("w", 5), ("w", 7), ("w", 9)]),
        ("Si Menor", 12, [("w", 6), ("w", 8), ("b", 10)])],
       "Acordes-menores-La-Si")

# --- Sib mayor ---
render([("Sib Mayor", 7, [("b", 5), ("w", 1), ("w", 3)], SIB)], "Acorde-Sib-Mayor")

# --- sostenidos y bemoles ---
render([("Sostenidos (#)", 7, []),
        ("Bemoles (\u266d)", 7, [], FLAT)],
       "Sostenidos-y-bemoles")

# --- mapa de teclado: donde nace cada acorde con sostenido ---
def root_map():
    WM, HM = 7.85, 7.20
    fig, ax = plt.subplots(figsize=(WM * 0.62, HM * 0.62))
    ax.set_xlim(0, WM); ax.set_ylim(0, HM); ax.axis("off"); ax.set_aspect("equal")
    ax.add_patch(FancyBboxPatch((0.05, 0.05), WM - 0.10, HM - 0.10,
                                boxstyle="round,pad=0.02,rounding_size=0.22",
                                facecolor="white", edgecolor="#C9C9C9", lw=2.2, zorder=1))
    ax.text(0.32, HM - 0.30, "Acordes con sostenido", fontsize=19, fontweight="bold",
            va="top", ha="left", color=INK, zorder=6)
    ax.text(0.32, HM - 0.92, "Cada uno empieza en una tecla negra", fontsize=11.5,
            va="top", ha="left", color=GREY, zorder=6)

    y0, KH2 = 1.70, 3.00
    top = y0 + KH2
    n = 7
    for i in range(n):
        ax.add_patch(Rectangle((X0 + i * KW_BASE, y0), KW_BASE, KH2, facecolor="white",
                               edgecolor=INK, lw=1.5, zorder=2))
    for i in range(n - 1):
        lab = SHARP[i % 7]
        if lab is None:
            continue
        cx = X0 + (i + 1) * KW_BASE
        bw, bh = KW_BASE * BKW, KH2 * BKH
        ax.add_patch(Rectangle((cx - bw / 2, top - bh), bw, bh,
                               facecolor="black", edgecolor="black", lw=1.0, zorder=3))
        ax.plot([cx, cx], [top + 0.05, top + 0.55], color="#9A9A9A", lw=1.3, zorder=3)
        ax.add_patch(FancyBboxPatch((cx - 0.41, top + 0.55), 0.82, 0.46,
                                    boxstyle="round,pad=0.0,rounding_size=0.23",
                                    facecolor=BLUE, edgecolor="black", lw=1.4, zorder=4))
        ax.text(cx, top + 0.78, lab, ha="center", va="center", fontsize=9.5,
                fontweight="bold", color="white", zorder=5)
    for i in range(n):
        ax.text(X0 + (i + 0.5) * KW_BASE, y0 - 0.44, WHITE[i], ha="center", va="center",
                fontsize=12.5, fontweight="bold", color=GREY, zorder=4)
    ax.text(WM / 2, 0.55, "También se llaman Reb, Mib, Solb, Lab y Sib",
            ha="center", va="center", fontsize=9.5, fontweight="bold", color=GREY)

    for ext in ("png", "svg"):
        fig.savefig(f"{OUT}/Teclado-acordes-sostenidos.{ext}", dpi=200,
                    bbox_inches="tight", facecolor="white", format=ext)
    plt.close(fig)
    print("ok Teclado-acordes-sostenidos")


root_map()


# --- truco: toca una tecla blanca y salta la siguiente ---
def truco_salta():
    WM, HM = 7.60, 6.55
    fig, ax = plt.subplots(figsize=(WM * 0.62, HM * 0.62))
    ax.set_xlim(0, WM); ax.set_ylim(0, HM); ax.axis("off"); ax.set_aspect("equal")
    ax.add_patch(FancyBboxPatch((0.05, 0.05), WM - 0.10, HM - 0.10,
                                boxstyle="round,pad=0.02,rounding_size=0.22",
                                facecolor="white", edgecolor="#C9C9C9", lw=2.2, zorder=1))
    ax.text(0.30, HM - 0.30, "Toca una y salta una", fontsize=18, fontweight="bold",
            va="top", ha="left", color=INK, zorder=6)
    ax.text(0.30, HM - 0.88, "Así se arma Do mayor (y también Fa y Sol)", fontsize=11,
            va="top", ha="left", color=GREY, zorder=6)

    KW2, KH2 = 1.06, 2.55
    X0_2 = (WM - 5 * KW2) / 2
    y0 = 1.30
    top = y0 + KH2

    for i in range(5):
        ax.add_patch(Rectangle((X0_2 + i * KW2, y0), KW2, KH2, facecolor="white",
                               edgecolor=INK, lw=1.6, zorder=2))
    for i in (0, 1, 3):
        cx = X0_2 + (i + 1) * KW2
        bw, bh = KW2 * 0.58, KH2 * 0.60
        ax.add_patch(Rectangle((cx - bw / 2, top - bh), bw, bh,
                               facecolor="black", edgecolor="black", lw=1.0, zorder=3))

    toca = [True, False, True, False, True]
    verde, gris = "#59A14F", "#D9D9D9"
    for i in range(5):
        cx = X0_2 + (i + 0.5) * KW2
        if toca[i]:
            ax.add_patch(FancyBboxPatch((cx - 0.48, top + 0.62), 0.96, 0.44,
                                        boxstyle="round,pad=0.0,rounding_size=0.22",
                                        facecolor=verde, edgecolor="black", lw=1.2, zorder=5))
            ax.text(cx, top + 0.84, "TOCA", ha="center", va="center", fontsize=10,
                    fontweight="bold", color="white", zorder=6)
            ax.add_patch(Circle((cx, y0 + 0.55), 0.20, facecolor=verde,
                                edgecolor="black", lw=1.3, zorder=6))
        else:
            ax.add_patch(FancyBboxPatch((cx - 0.48, top + 0.62), 0.96, 0.44,
                                        boxstyle="round,pad=0.0,rounding_size=0.22",
                                        facecolor=gris, edgecolor="#9A9A9A", lw=1.2, zorder=5))
            ax.text(cx, top + 0.84, "salta", ha="center", va="center", fontsize=10,
                    fontweight="bold", color="#4A4A4A", zorder=6)
        ax.text(cx, top + 1.34, str(i + 1), ha="center", va="center", fontsize=11,
                fontweight="bold", color="#8A8A8A", zorder=6)
        ax.text(cx, y0 - 0.42, WHITE[i], ha="center", va="center", fontsize=12.5,
                fontweight="bold", color=GREY, zorder=4)

    ax.text(WM / 2, 0.45,
            "Las teclas negras no se cuentan: solo se miran las blancas.",
            ha="center", va="center", fontsize=8.6, fontweight="bold", color=GREY)

    for ext in ("png", "svg"):
        fig.savefig(f"{OUT}/Truco-toca-y-salta.{ext}", dpi=200,
                    bbox_inches="tight", facecolor="white", format=ext)
    plt.close(fig)
    print("ok Truco-toca-y-salta")


truco_salta()


# --- mano derecha con los numeros de los dedos ---
def mano_derecha():
    fig, ax = plt.subplots(figsize=(7.9, 5.2))
    ax.set_xlim(-3.1, 4.0); ax.set_ylim(-2.3, 2.8)
    ax.axis("off"); ax.set_aspect("equal")

    skin, edge = "#F4CBA4", "#B98A63"
    ax.add_patch(Ellipse((0, -0.15), 2.6, 2.0, facecolor=skin, edgecolor=edge, lw=2.2, zorder=2))
    for fx, flen, fw, num in [(-0.85, 1.45, 0.42, "2"), (-0.30, 1.62, 0.44, "3"),
                              (0.26, 1.50, 0.43, "4"), (0.80, 1.15, 0.38, "5")]:
        ax.add_patch(FancyBboxPatch((fx - fw / 2, 0.45), fw, flen,
                                    boxstyle="round,pad=0.0,rounding_size=0.2",
                                    facecolor=skin, edgecolor=edge, lw=2.2, zorder=3))
        ax.add_patch(Circle((fx, 0.45 + flen + 0.30), 0.26, facecolor=BLUE,
                            edgecolor="black", lw=1.5, zorder=5))
        ax.text(fx, 0.45 + flen + 0.30, num, ha="center", va="center", fontsize=14,
                fontweight="bold", color="white", zorder=6)

    ax.add_patch(FancyBboxPatch((-2.35, -0.35), 1.35, 0.62,
                                boxstyle="round,pad=0.0,rounding_size=0.28",
                                facecolor=skin, edgecolor=edge, lw=2.2, zorder=3))
    ax.add_patch(Circle((-2.35, 0.05), 0.26, facecolor=BLUE, edgecolor="black", lw=1.5, zorder=5))
    ax.text(-2.35, 0.05, "1", ha="center", va="center", fontsize=14,
            fontweight="bold", color="white", zorder=6)

    ax.text(-1.30, -1.95, "Mano derecha", ha="center", fontsize=15,
            fontweight="bold", color=INK)
    ax.text(1.60, -1.15, "1 = pulgar\n2 = índice\n3 = medio\n4 = anular\n5 = meñique",
            ha="left", va="center", fontsize=11.5, color=GREY, linespacing=1.75)

    for ext in ("png", "svg"):
        fig.savefig(f"{OUT}/Dedos-mano-derecha.{ext}", dpi=200, bbox_inches="tight",
                    facecolor="white", format=ext)
    plt.close(fig)
    print("ok Dedos-mano-derecha")


mano_derecha()
