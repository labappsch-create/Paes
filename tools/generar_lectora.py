#!/usr/bin/env python3
"""Genera las 500 preguntas originales de Competencia Lectora, según el temario oficial:

- 40 textos continuos (literarios narrativos y no literarios), cada uno con 10 preguntas.
  Los textos base están en lectora_textos_a..e.py y se amplían con lectora2_amplia_a..d.py
  (oraciones agregadas al final de párrafos existentes, sin cambiar la numeración).
- 10 textos discontinuos (infografías), cada uno con 10 preguntas (lectora2_infografias.py).
  La imagen se dibuja con los mismos datos de las preguntas.
No hay poemas (el temario solo considera narraciones como textos literarios) ni preguntas de
clasificación como «¿Qué tipo de texto es?». Todos los textos, personas e instituciones son
ficticios. No usa contenido del DEMRE.

Uso (desde la carpeta del proyecto):
    PYTHONPATH=<carpeta con matplotlib> python3 tools/generar_lectora.py
Escribe: assets/questions/lectora.json y assets/images/lectora/*.png
"""
import json
import os
import random
import re
import sys
import textwrap
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generar_m1 as base  # noqa: E402
import lectora_textos_a, lectora_textos_b, lectora_textos_c, lectora_textos_d, lectora_textos_e  # noqa: E401,E402
import lectora2_amplia_a, lectora2_amplia_b, lectora2_amplia_c, lectora2_amplia_d  # noqa: E401,E402
import lectora2_amplia2  # noqa: E402
import lectora2_infografias  # noqa: E402

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Rectangle  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(ROOT, "assets", "images", "lectora")
OUT_JSON = os.path.join(ROOT, "assets", "questions", "lectora.json")

rnd = random.Random(20261121)
base.rnd = rnd
PREGUNTAS_POR_TEXTO = 10
NO_NUMBER = {"Texto instructivo", "Reglamento", "Entrevista"}
LITERARIOS = {"Cuento breve"}
PATRON_FUERA = r"tipo de texto|formato de este texto|persona gramatical|De qué lengua proviene"


def make(eje, enunciado, correct, wrongs, explicacion, imagen=None, texto=None, texto_tipo=None):
    q = base.make(eje, enunciado, correct, wrongs, explicacion, imagen)
    q["prueba"] = "lectora"
    if texto:
        q["texto"] = texto
    q["texto_tipo"] = texto_tipo
    return q


# ================================================================ TEXTOS CONTINUOS
def textos_base():
    return {t["titulo"]: t for m in (lectora_textos_a, lectora_textos_b, lectora_textos_c, lectora_textos_d, lectora_textos_e)
            for t in m.TEXTS}


def render_text(titulo, tipo, parrafos):
    if tipo in NO_NUMBER:
        body = "\n\n".join(parrafos)
    else:
        body = "\n\n".join(f"({i}) {p}" for i, p in enumerate(parrafos, 1))
    return f"{titulo}\n\n{body}"


def text_questions():
    base_txt = textos_base()
    out, palabras = [], []
    for mod in (lectora2_amplia_a, lectora2_amplia_b, lectora2_amplia_c, lectora2_amplia_d):
        for amp in mod.AMPLIA:
            t = base_txt[amp["titulo"]]
            parrafos = list(t["parrafos"])
            for n, extra in amp["amplia"].items():
                parrafos[n - 1] = parrafos[n - 1].rstrip() + " " + extra
            for n, extra in lectora2_amplia2.AMPLIA2.get(amp["titulo"], {}).items():
                parrafos[n - 1] = parrafos[n - 1].rstrip() + " " + extra
            preguntas = list(t["preguntas"])
            for i, q in amp["reemplaza"].items():
                preguntas[i] = q
            preguntas += amp["nuevas"]
            assert len(preguntas) == PREGUNTAS_POR_TEXTO, (amp["titulo"], len(preguntas))
            texto = render_text(t["titulo"], t["tipo"], parrafos)
            palabras.append(sum(len(p.split()) for p in parrafos))
            tipo = "literario" if t["tipo"] in LITERARIOS else "no literario"
            for hab, enun, c, w, ex in preguntas:
                assert len(w) == 3 and c not in w and len(set(w)) == 3, (t["titulo"], enun)
                assert not re.search(PATRON_FUERA, enun), (t["titulo"], enun)
                out.append(make(hab, enun, c, w, ex, texto=texto, texto_tipo=tipo))
    return out, palabras


# ================================================================ INFOGRAFÍAS
W = 7.0  # ancho de la imagen en pulgadas
FS = 13  # tamaño base de letra
_img = [0]


def save_fig(fig):
    _img[0] += 1
    name = f"lectora_img_{_img[0]:03d}.png"
    os.makedirs(IMG_DIR, exist_ok=True)
    fig.savefig(os.path.join(IMG_DIR, name), dpi=110, facecolor="white")
    plt.close(fig)
    return f"assets/images/lectora/{name}"


def wrap(t, n):
    return "\n".join(textwrap.wrap(t, n)) or t


def lineas_fila(fila, n_cols):
    ancho = 30 if n_cols <= 2 else 22
    return max(len(textwrap.wrap(str(c), ancho)) or 1 for c in fila)


def alto_fila(fila, n_cols):
    """Alto (pulgadas) de una fila de tabla según cuántas líneas tiene su celda más larga."""
    return 0.42 * (1 + 0.55 * (lineas_fila(fila, n_cols) - 1))


def alto_bloque(b):
    k = b[0]
    if k == "datos":
        return 1.45
    if k == "barras":
        return 0.75 + 0.48 * len(b[2])
    if k == "torta":
        return 3.2
    if k == "lista":
        lineas = sum(len(textwrap.wrap(x, 58)) for x in b[2])
        return 0.6 + 0.3 * lineas
    if k == "tabla":
        return 0.5 + sum(alto_fila(r, len(b[2])) for r in [b[2]] + b[3]) + 0.05
    if k == "nota":
        return 0.35 + 0.3 * len(textwrap.wrap(b[1], 62))
    raise ValueError(k)


def dibujar_bloque(fig, b, y0, h, color):
    """Dibuja un bloque en la franja [y0 - h, y0] (coordenadas de figura en pulgadas)."""
    H = fig.get_figheight()
    k = b[0]
    ax = fig.add_axes([0.05, (y0 - h) / H, 0.9, h / H])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    if k == "datos":
        n = len(b[1])
        for i, (val, txt) in enumerate(b[1]):
            x = i / n + 0.01
            ax.add_patch(FancyBboxPatch((x, 0.06), 1 / n - 0.02, 0.88, boxstyle="round,pad=0.01,rounding_size=0.03",
                                        facecolor=color, alpha=0.12, edgecolor=color))
            ax.text(x + (1 / n - 0.02) / 2, 0.63, val, ha="center", va="center", fontsize=FS + 7, fontweight="bold", color=color)
            ax.text(x + (1 / n - 0.02) / 2, 0.27, wrap(txt, 22 if n == 3 else 34), ha="center", va="center", fontsize=FS - 2)
        return
    titulo = b[1] if k != "nota" else None
    if titulo:
        ax.text(0, 1, titulo, ha="left", va="top", fontsize=FS + 1, fontweight="bold", color=color)
    top = 1 - 0.42 / h
    if k == "barras":
        _, _, datos, unidad = b
        sub = fig.add_axes([0.38, (y0 - h + 0.15) / H, 0.5, (h - 0.6) / H])
        labels = [d[0] for d in datos][::-1]
        vals = [d[1] for d in datos][::-1]
        sub.barh(labels, vals, color=color, alpha=0.85)
        for i, v in enumerate(vals):
            sub.text(v + max(vals) * 0.02, i, f"{v:g} {unidad}" if unidad != "%" else f"{v:g}%", va="center", fontsize=FS - 2)
        sub.set_xlim(0, max(vals) * 1.3)
        sub.set_xticks([])
        for s in ("top", "right", "bottom"):
            sub.spines[s].set_visible(False)
        sub.tick_params(axis="y", labelsize=FS - 1, length=0)
        return
    if k == "torta":
        _, _, datos = b
        sub = fig.add_axes([0.06, (y0 - h + 0.1) / H, 0.42, (h - 0.55) / H])
        colores = [color] + ["#90a4ae", "#ffb74d", "#81c784", "#ba68c8", "#4dd0e1"]
        sub.pie([d[1] for d in datos], colors=colores[:len(datos)], startangle=90, counterclock=False,
                wedgeprops=dict(edgecolor="white", linewidth=2))
        sub.set_aspect("equal")
        for i, (lab, v) in enumerate(datos):
            yy = top - 0.1 - i * min(0.15, 0.75 / len(datos))
            ax.add_patch(Rectangle((0.53, yy - 0.025), 0.03, 0.05, color=colores[i]))
            ax.text(0.58, yy, f"{lab}: {v}%", va="center", fontsize=FS - 1)
        return
    if k == "lista":
        y = top
        paso = 0.3 / h
        for item in b[2]:
            lineas = textwrap.wrap(item, 58)
            ax.text(0.02, y, "•", fontsize=FS, va="top", color=color)
            ax.text(0.06, y, "\n".join(lineas), fontsize=FS - 1, va="top", linespacing=1.25)
            y -= paso * len(lineas) + 0.02 / h
        return
    if k == "tabla":
        _, _, cols, filas = b
        ancho = 30 if len(cols) <= 2 else 22
        celdas = [[wrap(str(c), ancho) for c in r] for r in filas]
        sub = fig.add_axes([0.05, (y0 - h) / H, 0.9, (h - 0.45) / H])
        sub.axis("off")
        tb = sub.table(cellText=celdas, colLabels=cols, loc="upper center", cellLoc="center")
        tb.auto_set_font_size(False)
        tb.set_fontsize(FS - 2)
        tb.scale(1, 1.0)
        for (r, c), cell in tb.get_celld().items():
            cell.set_edgecolor("#bbbbbb")
            cell.set_height(alto_fila(cols if r == 0 else filas[r - 1], len(cols)) / (h - 0.45))
            if r == 0:
                cell.set_facecolor(color)
                cell.get_text().set_color("white")
                cell.get_text().set_fontweight("bold")
        return
    if k == "nota":
        ax.add_patch(FancyBboxPatch((0, 0.05), 1, 0.9, boxstyle="round,pad=0.01,rounding_size=0.02",
                                    facecolor="#f5f5f5", edgecolor="#cccccc"))
        ax.text(0.03, 0.5, wrap(b[1], 62), va="center", fontsize=FS - 1, linespacing=1.3)
        return


def dibujar_infografia(spec):
    cab, pie, sep = 1.35, 0.55, 0.25
    altos = [alto_bloque(b) for b in spec["bloques"]]
    H = cab + sum(altos) + sep * len(altos) + pie
    fig = plt.figure(figsize=(W, H))
    color = spec["color"]
    ax = fig.add_axes([0, (H - cab) / H, 1, cab / H])
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 1, 1, color=color, transform=ax.transAxes))
    ax.text(0.05, 0.62, wrap(spec["titulo"], 38), color="white", fontsize=FS + 8, fontweight="bold", va="center", transform=ax.transAxes)
    ax.text(0.05, 0.2, wrap(spec["subtitulo"], 70), color="white", fontsize=FS - 1, va="center", transform=ax.transAxes)
    y = H - cab - sep
    for b, h in zip(spec["bloques"], altos):
        dibujar_bloque(fig, b, y, h, color)
        y -= h + sep
    fig.text(0.05, 0.25 / H, wrap("Fuente: " + spec["fuente"], 90), fontsize=FS - 4, style="italic", color="#555555")
    return save_fig(fig)


def infographic_questions():
    out = []
    for spec in lectora2_infografias.INFOGRAFIAS:
        assert len(spec["preguntas"]) == PREGUNTAS_POR_TEXTO, spec["titulo"]
        img = dibujar_infografia(spec)
        for hab, enun, c, w, ex in spec["preguntas"]:
            assert len(w) == 3 and c not in w and len(set(w)) == 3, (spec["titulo"], enun)
            out.append(make(hab, f"Observa la infografía «{spec['titulo']}». {enun}", c, w, ex, imagen=img, texto_tipo="discontinuo"))
    return out


# ================================================================ PRINCIPAL
def build():
    if os.path.isdir(IMG_DIR):
        for f in os.listdir(IMG_DIR):
            if f.endswith(".png"):
                os.remove(os.path.join(IMG_DIR, f))
    textos, palabras = text_questions()
    infos = infographic_questions()
    # Se ordenan por texto (las preguntas de un mismo texto quedan juntas en el archivo);
    # la app las agrupa y las mezcla por bloques.
    out = textos + infos
    ordered = []
    for n, q in enumerate(out, 1):
        item = {"id": f"lectora_{n:03d}", "prueba": "lectora", "eje": q["eje"], "enunciado": q["enunciado"],
                "alternativas": q["alternativas"], "correcta": q["correcta"], "explicacion": q["explicacion"],
                "texto_tipo": q["texto_tipo"]}
        if "texto" in q:
            item["texto"] = q["texto"]
        if "imagen" in q:
            item["imagen"] = q["imagen"]
        ordered.append(item)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(ordered, f, ensure_ascii=False, indent=1)
    return ordered, palabras


def validate(qs, palabras):
    assert len(qs) == 500, len(qs)
    assert sum(1 for q in qs if "imagen" in q) == 100
    assert len({q["texto"] for q in qs if "texto" in q}) == 40
    assert len(os.listdir(IMG_DIR)) == 10
    for q in qs:
        assert len(q["alternativas"]) == 4 and len(set(q["alternativas"])) == 4, q
        assert 0 <= q["correcta"] < 4
    print(f"OK: 500 preguntas: 40 textos x 10 y 10 infografías x 10 (100 con imagen).")
    print(f"Palabras por texto: mín {min(palabras)}, máx {max(palabras)}, promedio {sum(palabras) // len(palabras)}.")
    print("Por habilidad:", dict(Counter(q["eje"] for q in qs)))
    print("Por tipo de texto:", dict(Counter(q["texto_tipo"] for q in qs)))
    print("Correcta por posición:", dict(sorted(Counter(q["correcta"] for q in qs).items())))


if __name__ == "__main__":
    validate(*build())
