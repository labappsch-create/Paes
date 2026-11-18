#!/usr/bin/env python3
"""Genera las 500 preguntas originales de Competencia Lectora.

- 400 preguntas de texto: 50 textos originales (lectora_textos_a..e.py), 8 preguntas cada uno.
- 100 preguntas con imagen: afiches, infografías, programas y avisos inventados, dibujados
  con el programa. La respuesta sale de los mismos datos con que se dibuja la imagen.
Todos los textos, instituciones y personajes son ficticios. No usa contenido del DEMRE.

Uso: PYTHONPATH=<carpeta con matplotlib> python3 tools/generar_lectora.py
"""
import json
import os
import random
import sys
import textwrap
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generar_m1 as base  # noqa: E402
from generar_m1 import Skip, fint  # noqa: E402
import lectora_textos_a, lectora_textos_b, lectora_textos_c, lectora_textos_d, lectora_textos_e  # noqa: E401,E402

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(ROOT, "assets", "images", "lectora")
OUT_JSON = os.path.join(ROOT, "assets", "questions", "lectora.json")

rnd = random.Random(20261121)
base.rnd = rnd
L, I, E = "Localizar", "Interpretar", "Evaluar"
NO_NUMBER = {"Poema", "Texto instructivo", "Reglamento", "Aviso", "Entrevista", "Microcuento"}


def make(eje, enunciado, correct, wrongs, explicacion, imagen=None, texto=None):
    q = base.make(eje, enunciado, correct, wrongs, explicacion, imagen)
    q["prueba"] = "lectora"
    if texto:
        q["texto"] = texto
    return q


def render_text(t):
    head = f"{t['titulo']}\n({t['tipo']})\n\n"
    if t["tipo"] in NO_NUMBER:
        body = "\n\n".join(t["parrafos"])
    else:
        body = "\n\n".join(f"({i}) {p}" for i, p in enumerate(t["parrafos"], 1))
    return head + body


def text_questions():
    out = []
    for mod in (lectora_textos_a, lectora_textos_b, lectora_textos_c, lectora_textos_d, lectora_textos_e):
        for t in mod.TEXTS:
            texto = render_text(t)
            assert len(t["preguntas"]) == 8, t["titulo"]
            for hab, enun, c, w, ex in t["preguntas"]:
                assert len(w) == 3 and c not in w and len(set(w)) == 3, (t["titulo"], enun)
                out.append(make(hab, enun, c, w, ex, texto=texto))
    return out


# ================================================================ IMÁGENES
_img = [0]


def save_fig(fig):
    _img[0] += 1
    name = f"lectora_img_{_img[0]:03d}.png"
    os.makedirs(IMG_DIR, exist_ok=True)
    fig.savefig(os.path.join(IMG_DIR, name), dpi=100, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return f"assets/images/lectora/{name}"


def canvas(w=6.0, h=7.6, bg="#fdf6e3"):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.02, 0.02), 0.96, 0.96, boxstyle="round,pad=0.01", facecolor=bg, edgecolor="#555", lw=1.5))
    return fig, ax


def wrap(t, n):
    return "\n".join(textwrap.wrap(t, n))


CAMPAIGNS = [
    ("Cuidemos el agua", "Cada gota cuenta", ["Cierra la llave mientras te cepillas los dientes", "Toma duchas de menos de cinco minutos", "Riega las plantas al atardecer"], "las personas en sus hogares", "ahorrar agua", "#1f77b4"),
    ("Recicla en tu colegio", "Lo que botas puede volver a ser útil", ["Separa papel, plástico y vidrio", "Lava los envases antes de reciclarlos", "Usa los contenedores del patio"], "los estudiantes", "reciclar los residuos", "#2ca02c"),
    ("Adopta con responsabilidad", "Una mascota es para toda la vida", ["Esterilízala y vacúnala", "Ponle placa de identificación", "Nunca la abandones"], "quienes quieren tener una mascota", "practicar la tenencia responsable de mascotas", "#ff7f0e"),
    ("Prevengamos los incendios forestales", "El bosque no se recupera en un día", ["No hagas fogatas en zonas prohibidas", "No botes colillas ni vidrios", "Llévate tu basura de vuelta"], "quienes visitan zonas rurales y bosques", "prevenir incendios forestales", "#d62728"),
    ("Usa casco siempre", "Tu cabeza no tiene repuesto", ["Ajusta bien la correa", "Cámbialo después de un golpe fuerte", "Úsalo incluso en trayectos cortos"], "los ciclistas", "promover el uso del casco al andar en bicicleta", "#9467bd"),
    ("Desconéctate para conectar", "La mejor conversación no tiene wifi", ["Deja el celular lejos durante la comida", "Propón un juego de mesa", "Pregunta cómo estuvo el día"], "las familias", "fomentar la conversación familiar sin pantallas", "#8c564b"),
    ("Respeta el paso de cebra", "Un segundo de espera puede salvar una vida", ["Detente antes de la línea", "Mira a los peatones", "No uses el celular al conducir"], "los conductores", "proteger a los peatones", "#17becf"),
]
ORGS = ["Municipalidad de Río Claro", "Centro de Alumnos del Liceo Los Andes", "Fundación Horizonte Verde", "Junta de Vecinos Villa Sol", "Agrupación Ciudad Amable"]


def g_campaign():
    title, slogan, tips, aud, purpose, col = rnd.choice(CAMPAIGNS)
    org = rnd.choice(ORGS)
    fig, ax = canvas()
    ax.add_patch(FancyBboxPatch((0.06, 0.78), 0.88, 0.16, boxstyle="round,pad=0.01", facecolor=col, edgecolor="none"))
    ax.text(0.5, 0.86, wrap(title.upper(), 24), ha="center", va="center", fontsize=17, color="white", fontweight="bold")
    ax.text(0.5, 0.70, f"«{slogan}»", ha="center", va="center", fontsize=13, style="italic", color=col)
    for k, t in enumerate(tips):
        ax.text(0.10, 0.56 - k * 0.12, "✔", fontsize=16, color=col, va="center")
        ax.text(0.18, 0.56 - k * 0.12, wrap(t, 34), fontsize=11.5, va="center")
    ax.text(0.5, 0.10, f"Una campaña de: {org}", ha="center", fontsize=10.5, color="#333")
    img = save_fig(fig)
    k = rnd.randint(1, 5)
    if k == 1:
        others = [c[4] for c in CAMPAIGNS if c[4] != purpose]
        return make(E, "¿Cuál es el propósito principal del afiche?", f"Promover {purpose}" if not purpose.startswith("promover") else purpose[0].upper() + purpose[1:],
                    [("Promover " + o) if not o.startswith("promover") else o[0].upper() + o[1:] for o in rnd.sample(others, 3)], "El título y los consejos apuntan a ese objetivo.", img)
    if k == 2:
        others = [c[3] for c in CAMPAIGNS if c[3] != aud]
        return make(I, "¿A quiénes se dirige principalmente el afiche?", aud[0].upper() + aud[1:], [o[0].upper() + o[1:] for o in rnd.sample(others, 3)],
                    "Los consejos están pensados para ese público.", img)
    if k == 3:
        return make(L, "Según el afiche, ¿quién organiza la campaña?", org, [o for o in ORGS if o != org][:3], "Aparece al pie del afiche.", img)
    if k == 4:
        tip = rnd.choice(tips)
        other_tips = [t for c in CAMPAIGNS if c[0] != title for t in c[2]]
        return make(L, "¿Cuál de los siguientes consejos aparece en el afiche?", tip, rnd.sample(other_tips, 3), "Está en la lista de consejos.", img)
    return make(I, f"¿Qué función cumple la frase «{slogan}» en el afiche?", "Llamar la atención y resumir el mensaje de forma breve y fácil de recordar",
                ["Entregar datos estadísticos", "Indicar la fecha de la campaña", "Presentar al organizador"], "Es el eslogan de la campaña.", img)


SURVEY_TOPICS = [
    ("¿Cómo llegan los estudiantes al colegio?", ["Caminando", "Bus", "Auto", "Bicicleta", "Metro"]),
    ("¿Cuántas horas duermen los estudiantes en días de clases?", ["Menos de 6", "6 a 7", "7 a 8", "Más de 8"]),
    ("¿Qué actividad prefieren en el recreo?", ["Conversar", "Jugar fútbol", "Usar el celular", "Leer", "Escuchar música"]),
    ("¿Qué taller les gustaría tener?", ["Robótica", "Teatro", "Cocina", "Fotografía", "Ajedrez"]),
]


def g_survey():
    q, cats = rnd.choice(SURVEY_TOPICS)
    k = len(cats)
    while True:
        parts = [rnd.randrange(5, 45) for _ in range(k)]
        tot = sum(parts)
        pct = [round(p * 100 / tot) for p in parts]
        pct[-1] = 100 - sum(pct[:-1])
        if min(pct) > 1 and len(set(pct)) == k:
            break
    n = rnd.choice([120, 200, 250, 300, 400, 500])
    school = rnd.choice(["Liceo Los Andes", "Colegio Bahía Azul", "Liceo Río Claro", "Colegio Valle Verde"])
    fig, ax = plt.subplots(figsize=(6.6, 4.6))
    bars = ax.barh(cats[::-1], pct[::-1], color="#4c9f70")
    for b_, v in zip(bars, pct[::-1]):
        ax.text(v + 0.8, b_.get_y() + b_.get_height() / 2, f"{v}%", va="center")
    ax.set_xlim(0, max(pct) + 12)
    ax.set_xlabel("% de estudiantes")
    ax.set_title(f"{q}\nEncuesta a {n} estudiantes del {school} (datos ficticios)", fontsize=11)
    img = save_fig(fig)
    t = rnd.randint(1, 4)
    best = cats[pct.index(max(pct))]
    worst = cats[pct.index(min(pct))]
    if t == 1:
        return make(L, "Según la infografía, ¿cuál fue la respuesta más frecuente?", best, [c for c in cats if c != best], f"Es la barra más larga ({max(pct)}%).", img)
    if t == 2:
        return make(L, "Según la infografía, ¿cuál fue la respuesta menos frecuente?", worst, [c for c in cats if c != worst], f"Es la barra más corta ({min(pct)}%).", img)
    if t == 3:
        return make(L, "¿A cuántos estudiantes se encuestó?", fint(n), [fint(x) for x in (n * 2, n // 2, 100) if x != n] + [fint(n + 50)], "Lo indica el título del gráfico.", img)
    return make(E, "¿Cuál de las siguientes conclusiones se puede sacar correctamente de la infografía?",
                f"En ese colegio, «{best}» fue la respuesta más elegida por los estudiantes encuestados",
                [f"Todos los estudiantes de Chile prefieren «{best}»", f"Nadie eligió «{worst}»", "La encuesta se hizo a profesores y apoderados"],
                "Las conclusiones deben limitarse a los datos y a quienes respondieron la encuesta.", img)


EVENTS_PROG = [
    ("Semana de la Ciencia", ["Feria de experimentos", "Charla: el universo en tu bolsillo", "Taller de robótica", "Observación astronómica", "Premiación"]),
    ("Fiesta Costumbrista", ["Desfile de huasos", "Competencia de cueca", "Muestra de artesanía", "Almuerzo típico", "Show folclórico"]),
    ("Feria del Libro Juvenil", ["Inauguración", "Lectura de cuentos", "Taller de cómic", "Conversatorio con escritoras", "Firma de libros"]),
    ("Jornada Deportiva", ["Calentamiento masivo", "Torneo de básquetbol", "Carrera de relevos", "Clase de zumba", "Entrega de medallas"]),
]
PLACES = ["Gimnasio", "Biblioteca", "Patio central", "Auditorio", "Sala 12", "Cancha techada"]


def g_program():
    name, acts = rnd.choice(EVENTS_PROG)
    h0 = rnd.choice([9, 10, 15, 16])
    times = [f"{h0 + i}:{rnd.choice(['00', '30'])}" for i in range(5)]
    places = [rnd.choice(PLACES) for _ in acts]
    day = rnd.choice(["sábado 12", "viernes 18", "sábado 26", "jueves 9"])
    fig, ax = plt.subplots(figsize=(7.4, 4.2))
    ax.axis("off")
    tbl = ax.table(cellText=[[t, a, p] for t, a, p in zip(times, acts, places)], colLabels=["Hora", "Actividad", "Lugar"], loc="center", cellLoc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(14)
    tbl.scale(1, 2.1)
    tbl.auto_set_column_width([0, 1, 2])
    for (r, c), cell in tbl.get_celld().items():
        if r == 0:
            cell.set_facecolor("#ffe08a")
    ax.set_title(f"Programa: {name} — {day} (entrada liberada)", fontsize=12)
    img = save_fig(fig)
    i = rnd.randrange(5)
    t = rnd.randint(1, 4)
    if t == 1:
        return make(L, f"Según el programa, ¿a qué hora comienza la actividad «{acts[i]}»?", times[i], [x for x in times if x != times[i]], "Se lee en la fila correspondiente.", img)
    if t == 2:
        if places.count(places[i]) > 1:
            raise Skip()
        return make(L, f"¿En qué lugar se realiza «{acts[i]}»?", places[i], [p for p in PLACES if p != places[i]], "Se lee en la columna «Lugar».", img)
    if t == 3:
        return make(I, "¿Qué actividad se realiza inmediatamente después de la primera?", acts[1], [acts[0], acts[3], acts[4]], "Es la segunda fila del programa.", img)
    return make(I, "Según el programa, ¿cuánto hay que pagar para asistir?", "Nada, porque la entrada es liberada", ["Depende de la actividad", "Solo pagan los adultos", "El programa no entrega esa información"],
                "«Entrada liberada» significa que es gratuita.", img)


SHOWS = [("Concierto de la Orquesta Juvenil", "Teatro Municipal"), ("Obra de teatro «La casa de los vientos»", "Centro Cultural Estación"),
         ("Muestra de cine chileno", "Sala Andes"), ("Festival de bandas escolares", "Anfiteatro del Parque")]


def g_event_poster():
    name, venue = rnd.choice(SHOWS)
    day = rnd.choice(["Viernes 14 de marzo", "Sábado 5 de abril", "Domingo 20 de julio", "Sábado 9 de agosto"])
    hour = rnd.choice(["18:00", "19:30", "20:00", "17:00"])
    price = rnd.choice([0, 2000, 3000, 5000])
    disc = rnd.choice(["Estudiantes y adultos mayores: 50% de descuento", "Niños menores de 10 años no pagan", "Cupos limitados: inscripción previa"])
    fig, ax = canvas(bg="#eef3fb")
    ax.text(0.5, 0.86, wrap(name, 24), ha="center", va="center", fontsize=17, fontweight="bold", color="#1a3d7c")
    ax.text(0.5, 0.66, f"{day}\n{hour} horas", ha="center", va="center", fontsize=14)
    ax.text(0.5, 0.50, venue, ha="center", fontsize=13, style="italic")
    ax.text(0.5, 0.36, "Entrada liberada" if price == 0 else f"Entrada general: ${fint(price)}", ha="center", fontsize=14, fontweight="bold", color="#b03030")
    ax.text(0.5, 0.24, wrap(disc, 36), ha="center", va="center", fontsize=11)
    ax.text(0.5, 0.08, "Organiza: Corporación Cultural Río Claro (ficticia)", ha="center", fontsize=9.5, color="#444")
    img = save_fig(fig)
    t = rnd.randint(1, 4)
    if t == 1:
        return make(L, "Según el afiche, ¿dónde se realizará el evento?", venue, [v for _, v in SHOWS if v != venue], "Aparece bajo la fecha.", img)
    if t == 2:
        hours = ["18:00", "19:30", "20:00", "17:00"]
        return make(L, "¿A qué hora comienza el evento?", f"{hour} horas", [f"{h} horas" for h in hours if h != hour], "Aparece bajo la fecha.", img)
    if t == 3:
        if price == 0 or not disc.startswith("Estudiantes"):
            raise Skip()
        half = price // 2
        return make(I, "Según el afiche, ¿cuánto paga un estudiante por su entrada?", f"${fint(half)}", [f"${fint(price)}", "$0", f"${fint(price * 2)}"],
                    f"Tiene 50% de descuento sobre ${fint(price)}.", img)
    return make(E, "¿Cuál es el propósito principal del afiche?", "Informar e invitar a un evento cultural", ["Vender instrumentos musicales", "Narrar la historia del teatro", "Opinar sobre la cultura"],
                "Entrega datos del evento para que el público asista.", img)


GRAPH_PLAN = [(g_campaign, 30), (g_survey, 30), (g_program, 30), (g_event_poster, 10)]


def build():
    if os.path.isdir(IMG_DIR):
        for f in os.listdir(IMG_DIR):
            if f.endswith(".png"):
                os.remove(os.path.join(IMG_DIR, f))
    out = text_questions()
    assert len(out) == 400, len(out)
    seen = set()
    for fn, n in GRAPH_PLAN:
        made = tries = 0
        while made < n:
            tries += 1
            if tries > 2000:
                raise RuntimeError(fn.__name__)
            before = _img[0]
            try:
                q = fn()
                key = q["enunciado"] + "|" + q["alternativas"][q["correcta"]]
                if key in seen:
                    raise Skip()
            except Skip:
                if _img[0] > before:
                    p = os.path.join(IMG_DIR, f"lectora_img_{_img[0]:03d}.png")
                    if os.path.exists(p):
                        os.remove(p)
                    _img[0] -= 1
                continue
            seen.add(key)
            out.append(q)
            made += 1
    rnd.shuffle(out)
    ordered = []
    for n, q in enumerate(out, 1):
        item = {"id": f"lectora_{n:03d}", "prueba": "lectora", "eje": q["eje"], "enunciado": q["enunciado"],
                "alternativas": q["alternativas"], "correcta": q["correcta"], "explicacion": q["explicacion"]}
        if "texto" in q:
            item["texto"] = q["texto"]
        if "imagen" in q:
            item["imagen"] = q["imagen"]
        ordered.append(item)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(ordered, f, ensure_ascii=False, indent=1)
    return ordered


if __name__ == "__main__":
    qs = build()
    assert len(qs) == 500
    for q in qs:
        assert len(q["alternativas"]) == 4 and len(set(q["alternativas"])) == 4, q
    assert sum(1 for q in qs if "imagen" in q) == 100 == len(os.listdir(IMG_DIR))
    print(f"OK: 500 preguntas, 100 con imagen. Por habilidad: {dict(Counter(q['eje'] for q in qs))}. Correcta por posición: {dict(Counter(q['correcta'] for q in qs))}")
