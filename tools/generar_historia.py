#!/usr/bin/env python3
"""Genera las 500 preguntas originales de Historia y Ciencias Sociales (400 de texto + 100 con imagen).

- Las preguntas de fechas, orden cronológico y siglos se arman con la tabla EVENTS.
- Las de personajes, conceptos, institucionalidad y economía salen de historia_datos.py.
- Los cálculos de economía (desempleo, inflación, presupuesto) los resuelve el programa.
- Los gráficos usan hechos reales (líneas de tiempo) o datos de países INVENTADOS
  (claramente indicados) para practicar la lectura de fuentes sin dar cifras reales falsas.
No usa contenido del DEMRE.

Uso: PYTHONPATH=<carpeta con matplotlib> python3 tools/generar_historia.py
"""
import json
import os
import random
import sys
from collections import Counter
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generar_m1 as base  # noqa: E402
from generar_m1 import MINUS, Skip, fint, fmt, numeric_options  # noqa: E402
import historia_fuentes_a  # noqa: E402
import historia_fuentes_b  # noqa: E402
from historia_datos import (CIU, CIVIC, CIVIC_EXTRA, CONCEPTS, ECO, ECON, EVENTS, HIS, MARKET_SHOCKS, PEOPLE, PROCESSES)  # noqa: E402

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(ROOT, "assets", "images", "historia")
OUT_JSON = os.path.join(ROOT, "assets", "questions", "historia.json")
N_TEXT, N_GRAPH = 400, 100

rnd = random.Random(20261120)
base.rnd = rnd
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})


def fix(t):
    return t.replace(" a el ", " al ").replace(" de el ", " del ")


def make(eje, enunciado, correct, wrongs, explicacion, imagen=None):
    q = base.make(eje, fix(enunciado), correct, wrongs, fix(explicacion), imagen)
    q["prueba"] = "historia"
    return q


def cap(t):
    return t[0].upper() + t[1:]


def low(t):
    return t[0].lower() + t[1:]


ROMAN = {18: "XVIII", 19: "XIX", 20: "XX", 21: "XXI", 17: "XVII"}


def century(y):
    return (y - 1) // 100 + 1


def pct(v):
    return f"{fmt(v)}%"


# ================================================================ TEXTO
def t_year():
    e, y, _ = rnd.choice(EVENTS)
    c, w = numeric_options(y, [y + 10, y - 10, y + 3, y - 4, y + 20], step=5, fn=str)
    return make(HIS, f"¿En qué año ocurrió {e}?", c, w, f"{cap(e)} ocurrió en {y}.")


def distinct_events(k, scope=None):
    pool = [ev for ev in EVENTS if scope is None or ev[2] == scope]
    for _ in range(50):
        evs = rnd.sample(pool, k)
        ys = [ev[1] for ev in evs]
        if len(set(ys)) == k and min(abs(a - b) for i, a in enumerate(ys) for b in ys[i + 1:]) >= 2:
            return evs
    raise Skip()


def t_first():
    evs = distinct_events(4, rnd.choice([None, None, "Chile"]))
    first = min(evs, key=lambda e: e[1])
    last = max(evs, key=lambda e: e[1])
    if rnd.random() < 0.5:
        return make(HIS, "¿Cuál de los siguientes hechos ocurrió primero?", cap(first[0]), [cap(e[0]) for e in evs if e != first],
                    "Orden: " + "; ".join(f"{e[0]} ({e[1]})" for e in sorted(evs, key=lambda e: e[1])) + ".")
    return make(HIS, "¿Cuál de los siguientes hechos ocurrió más recientemente?", cap(last[0]), [cap(e[0]) for e in evs if e != last],
                "Orden: " + "; ".join(f"{e[0]} ({e[1]})" for e in sorted(evs, key=lambda e: e[1])) + ".")


def t_order():
    evs = distinct_events(3)
    labels = ["I", "II", "III"]
    order = sorted(range(3), key=lambda i: evs[i][1])
    correct = ", ".join(labels[i] for i in order)
    perms = [", ".join(p) for p in (["I", "II", "III"], ["I", "III", "II"], ["II", "I", "III"], ["II", "III", "I"], ["III", "I", "II"], ["III", "II", "I"])]
    listing = " ".join(f"{labels[i]}. {cap(evs[i][0])}." for i in range(3))
    return make(HIS, f"Ordena cronológicamente, del más antiguo al más reciente, los siguientes hechos: {listing}", correct, [p for p in perms if p != correct],
                "Fechas: " + "; ".join(f"{labels[i]} = {evs[i][1]}" for i in range(3)) + ".")


def t_century():
    e, y, _ = rnd.choice(EVENTS)
    c = century(y)
    opts = [f"Siglo {ROMAN[x]}" for x in (c - 1, c + 1, c - 2, c + 2) if x in ROMAN]
    return make(HIS, f"¿En qué siglo ocurrió {e}?", f"Siglo {ROMAN[c]}", opts,
                f"Ocurrió en {y}; los años {(c - 1) * 100 + 1} a {c * 100} forman el siglo {ROMAN[c]}.")


def t_between():
    a, b = distinct_events(2)
    if a[1] > b[1]:
        a, b = b, a
    d = b[1] - a[1]
    c, w = numeric_options(d, [d + 10, d - 10 if d > 10 else d + 5, d + 1, d - 1], step=3, fn=lambda v: f"{fint(v)} años")
    return make(HIS, f"¿Cuántos años transcurrieron entre {a[0]} y {b[0]}?", c, w, f"{b[1]} − {a[1]} = {d} años.")


def t_same_century():
    e, y, _ = rnd.choice(EVENTS)
    c = century(y)
    same = [ev for ev in EVENTS if century(ev[1]) == c and ev[0] != e]
    diff = [ev for ev in EVENTS if century(ev[1]) != c]
    if not same or len(diff) < 3:
        raise Skip()
    ok = rnd.choice(same)
    return make(HIS, f"¿Cuál de los siguientes hechos ocurrió en el mismo siglo que {e} ({y})?", cap(ok[0]), [cap(x[0]) for x in rnd.sample(diff, 4)],
                f"Ambos ocurrieron en el siglo {ROMAN[c]}: {ok[0]} fue en {ok[1]}.")


def t_unemployment():
    FT = rnd.randrange(2000, 12001, 500) * 1000
    rate = rnd.choice([4, 5, 6, 7, 8, 9, 10, 12, 15])
    D = FT * rate // 100
    if rnd.random() < 0.5:
        c, w = numeric_options(rate, [100 - rate, rate * 2, D * 100 // (FT - D) if FT > D else rate + 3], step=1, fn=pct)
        return make(ECO, f"En un país, la fuerza de trabajo es de {fint(FT)} personas y hay {fint(D)} personas desocupadas. ¿Cuál es la tasa de desempleo?", c, w,
                    f"Tasa de desempleo = desocupados / fuerza de trabajo · 100 = {fint(D)}/{fint(FT)} · 100 = {rate}%.")
    c, w = numeric_options(FT - D, [FT, D, FT + D], step=FT // 20, fn=fint)
    return make(ECO, f"Un país tiene una fuerza de trabajo de {fint(FT)} personas y una tasa de desempleo de {rate}%. ¿Cuántas personas están ocupadas?", c, w,
                f"Desocupados = {rate}% de {fint(FT)} = {fint(D)}; ocupados = {fint(FT)} − {fint(D)} = {fint(FT - D)}.")


def t_inflation():
    p0 = rnd.choice([100, 200, 400, 500, 1000, 2000])
    r = rnd.choice([2, 3, 4, 5, 6, 8, 10, 12, 15, 20])
    p1 = p0 * (100 + r) // 100
    k = rnd.randint(1, 3)
    if k == 1:
        c, w = numeric_options(r, [p1 - p0, r * 2, 100 - r], step=1, fn=pct)
        return make(ECO, f"Una canasta de bienes costaba ${fint(p0)} y un año después cuesta ${fint(p1)}. ¿Cuál fue la inflación de esa canasta en el año?", c, w,
                    f"Variación = ({fint(p1)} − {fint(p0)})/{fint(p0)} · 100 = {r}%.")
    if k == 2:
        n = rnd.choice([3, 4, 5, 6, 8, 10, 12, 15])
        if n == r:
            raise Skip()
        real = n - r
        c, w = numeric_options(real, [n + r, -real, n], step=1, positive=False, fn=lambda v: ("+" if v > 0 else "") + pct(v).replace("-", MINUS))
        return make(ECO, f"El sueldo de una persona sube {n}% en un año en que la inflación fue de {r}%. Aproximadamente, ¿cómo cambió su poder de compra (sueldo real)?", c, w,
                    f"Sueldo real ≈ variación nominal − inflación = {n}% − {r}% = {fmt(real)}%{' (pierde poder de compra)' if real < 0 else ''}.")
    c, w = numeric_options(p1, [p0 + r, p0 * r // 10, p0 * (100 - r) // 100], step=p0 // 20 or 1, fn=lambda v: "$" + fint(v))
    return make(ECO, f"Un producto cuesta ${fint(p0)}. Si la inflación anual es de {r}% y su precio sube igual que la inflación, ¿cuánto costará en un año?", c, w,
                f"{fint(p0)} · {fmt(1 + r / 100)} = ${fint(p1)}.")


def t_budget():
    I = rnd.randrange(40, 120, 2) * 1000
    G = I + rnd.choice([-1, 1]) * rnd.randrange(2, 20, 2) * 1000
    d = I - G
    kind = "superávit" if d > 0 else "déficit"
    c = f"{cap(kind)} de {fint(abs(d))} millones"
    other = "Déficit" if d > 0 else "Superávit"
    w = [f"{other} de {fint(abs(d))} millones", f"{cap(kind)} de {fint(I + G)} millones", "Equilibrio fiscal (ingresos iguales a gastos)", f"{other} de {fint(abs(d) * 2)} millones"]
    return make(ECO, f"En un año, los ingresos de un Estado son {fint(I)} millones y sus gastos son {fint(G)} millones. ¿Cuál es su situación fiscal?", c, w,
                f"Ingresos − gastos = {fint(I)} − {fint(G)} = {fint(d)} millones: {kind}.")


def t_market():
    s, curve, p, q = rnd.choice(MARKET_SHOCKS)
    good = rnd.choice(["las paltas", "las bicicletas", "los celulares", "las entradas al cine", "los libros", "las zapatillas"])
    c = f"{curve}; el precio {p} y la cantidad transada {q}"
    combos = [f"{cv}; el precio {pp} y la cantidad transada {qq}" for cv, pp, qq in [
        ("La demanda aumenta", "sube", "sube"), ("La demanda disminuye", "baja", "baja"), ("La oferta aumenta", "baja", "sube"), ("La oferta disminuye", "sube", "baja"),
        ("La demanda aumenta", "baja", "baja"), ("La oferta aumenta", "sube", "baja")]]
    return make(ECO, f"En el mercado de {good}, {s}. Si lo demás se mantiene constante, ¿qué ocurre?", c, [x for x in combos if x != c],
                f"{curve}. En el nuevo equilibrio el precio {p} y la cantidad {q}.")


def t_opportunity():
    n = rnd.choice(["Camila", "Matías", "Sofía", "Tomás", "Javiera", "Diego"])
    a, b, cc = rnd.sample(range(10, 60, 5), 3)
    opts = {"trabajar en una tienda": a * 1000, "dar clases particulares": b * 1000, "cuidar mascotas": cc * 1000}
    choice = rnd.choice(list(opts))
    rest = {k: v for k, v in opts.items() if k != choice}
    best = max(rest.values())
    ans = f"${fint(best)}"
    w = [f"${fint(v)}" for v in rest.values() if v != best] + [f"${fint(opts[choice])}", f"${fint(sum(rest.values()))}"]
    desc = ", ".join(f"{k} (${fint(v)})" for k, v in opts.items())
    return make(ECO, f"El sábado, {n} puede elegir solo una actividad: {desc}. Si elige {choice}, ¿cuál es su costo de oportunidad?", ans, w,
                "El costo de oportunidad es el valor de la mejor alternativa a la que se renuncia.")


def bank_items():
    items = []
    # Análisis de fuentes: cada fuente original trae 2 o 3 preguntas.
    for eje, intro, texto, preguntas in historia_fuentes_a.FUENTES + historia_fuentes_b.FUENTES:
        for enun, c, w, ex in preguntas:
            items.append((eje, f"{intro}\n\n{texto}\n\n{enun}", c, w, ex))
    names = [p for p, _ in PEOPLE]
    descs = [d for _, d in PEOPLE]
    for p, d in PEOPLE:
        items.append((HIS, f"¿Qué afirmación describe correctamente a {p}?", d, [x for x in descs if x != d], f"{p}: {low(d)}."))
        items.append((HIS, f"¿Qué personaje histórico {low(d)}?", p, [x for x in names if x != p], f"{p}: {low(d)}."))
    cn = [c for c, _ in CONCEPTS]
    cd = [d for _, d in CONCEPTS]
    for c, d in CONCEPTS:
        items.append((HIS, f"¿Qué se entiende por «{c}»?", d, [x for x in cd if x != d], f"{c}: {low(d)}."))
        items.append((HIS, f"¿Qué concepto corresponde a la siguiente definición? «{d}»", c, [x for x in cn if x != c], f"Corresponde a: {c}."))
    items += [(CIU, q, c, w, e) for q, c, w, e in CIVIC + CIVIC_EXTRA]
    items += [(HIS, q, c, w, e) for q, c, w, e in PROCESSES]
    items += [(ECO, q, c, w, e) for q, c, w, e in ECON]
    return items


# Sin preguntas de «¿en qué año...?»: el temario evalúa pensamiento temporal
# (orden, simultaneidad, períodos), no memorizar fechas exactas.
CALC = [t_first, t_order, t_century, t_between, t_same_century,
        t_unemployment, t_inflation, t_market, t_opportunity, t_budget]


# ================================================================ GRÁFICOS
_img = [0]


def save_fig(fig):
    _img[0] += 1
    name = f"historia_img_{_img[0]:03d}.png"
    os.makedirs(IMG_DIR, exist_ok=True)
    fig.savefig(os.path.join(IMG_DIR, name), dpi=100, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return f"assets/images/historia/{name}"


def g_timeline():
    evs = sorted(distinct_events(4, rnd.choice([None, "Chile", "Mundo"])), key=lambda e: e[1])
    y0, y1 = evs[0][1], evs[-1][1]
    if min(evs[i + 1][1] - evs[i][1] for i in range(3)) < (y1 - y0) / 9:
        raise Skip()
    pad = max(5, (y1 - y0) // 10)
    fig, ax = plt.subplots(figsize=(7.2, 2.2))
    ax.axhline(0, color="black", lw=2)
    for i, (e, y, _) in enumerate(evs):
        ax.plot(y, 0, "o", color="#d62728", ms=8)
        ax.text(y, 0.35 if i % 2 == 0 else -0.55, f"{'ABCD'[i]}\n{y}" if i % 2 == 0 else f"{y}\n{'ABCD'[i]}", ha="center", fontsize=11)
    ax.set_xlim(y0 - pad, y1 + pad)
    ax.set_ylim(-1, 1)
    ax.axis("off")
    ax.set_title("Línea de tiempo")
    img = save_fig(fig)
    i = rnd.randrange(4)
    if rnd.random() < 0.6:
        return make(HIS, f"En la línea de tiempo, ¿qué letra corresponde a {evs[i][0]}?", "ABCD"[i], [x for x in "ABCD" if x != "ABCD"[i]],
                    f"{cap(evs[i][0])} ocurrió en {evs[i][1]}, punto {'ABCD'[i]}.", img)
    a, b = sorted(rnd.sample(range(4), 2))
    if b - a < 1:
        raise Skip()
    lets = "ABCD"
    return make(HIS, f"En la línea de tiempo, el punto {lets[a]} corresponde a {evs[a][0]}. ¿Qué hecho corresponde al punto {lets[b]}?", cap(evs[b][0]),
                [cap(e[0]) for k, e in enumerate(evs) if k != b] + [cap(rnd.choice([x for x in EVENTS if x not in evs])[0])],
                f"El punto {lets[b]} marca el año {evs[b][1]}: {evs[b][0]}.", img)


def g_votes():
    names = ["Candidatura A", "Candidatura B", "Candidatura C", "Candidatura D"]
    k = rnd.choice([3, 4])
    while True:
        v = [rnd.randrange(5, 60) for _ in range(k)]
        tot = sum(v)
        p = [x * 100 / tot for x in v]
        if len(set(v)) == k and all(abs(round(x) - x) < 1e-9 or True for x in p):
            break
    tot_votes = rnd.choice([1000000, 2000000, 5000000])
    pr = [round(x * 100 / sum(v)) for x in v]
    pr[-1] = 100 - sum(pr[:-1])
    if min(pr) <= 0 or len(set(pr)) < k:
        raise Skip()
    fig, ax = plt.subplots(figsize=(5.8, 3.6))
    ax.bar(names[:k], pr, color=["#1f77b4", "#ff7f0e", "#2ca02c", "#9467bd"][:k])
    for i, x in enumerate(pr):
        ax.text(i, x + 1, f"{x}%", ha="center")
    ax.set_ylabel("% de votos válidos")
    ax.set_ylim(0, max(pr) + 12)
    ax.set_title("Elección presidencial en un país ficticio")
    img = save_fig(fig)
    top = max(pr)
    win = names[pr.index(top)]
    if rnd.random() < 0.5:
        if top > 50:
            ans = f"Sí: {win} supera el 50% de los votos válidos y gana en primera vuelta"
        else:
            two = sorted(range(k), key=lambda i: -pr[i])[:2]
            ans = f"No: ninguna supera el 50%; habría segunda vuelta entre {names[two[0]]} y {names[two[1]]}"
        w = [f"Sí: {win} gana por tener la mayor cantidad de votos, aunque no supere el 50%", "No: debe repetirse la elección con todas las candidaturas",
             f"No: el Congreso elige entre {names[0]} y {names[-1] if k > 1 else names[0]}", f"Sí: gana {names[(pr.index(top) + 1) % k]}"]
        if top > 50:
            w[0] = "No: siempre hay segunda vuelta"
        return make(CIU, "El gráfico muestra los resultados de una elección presidencial con las mismas reglas que en Chile. ¿Hay un ganador en primera vuelta?", ans, w,
                    "En Chile se necesita más de la mitad de los votos válidamente emitidos; si nadie la obtiene, compiten las dos primeras mayorías.", img)
    i = rnd.randrange(k)
    n = tot_votes * pr[i] // 100
    c, w = numeric_options(n, [pr[i] * 1000, tot_votes - n, n * 2], step=tot_votes // 50, fn=fint)
    return make(CIU, f"Si en la elección del gráfico hubo {fint(tot_votes)} votos válidos, ¿cuántos votos obtuvo la {low(names[i])}?", c, w,
                f"{pr[i]}% de {fint(tot_votes)} = {fint(n)}.", img)


def g_supply_demand():
    s, curve, p, q = rnd.choice(MARKET_SHOCKS)
    xs = np.linspace(0, 10, 50)
    fig, ax = plt.subplots(figsize=(4.8, 4.2))
    ax.plot(xs, 10 - xs * 0.8, color="#1f77b4", lw=2, label="Demanda (D)")
    ax.plot(xs, 2 + xs * 0.8, color="#ff7f0e", lw=2, label="Oferta (O)")
    shift = 2 if "aumenta" in curve else -2
    if "Demanda" in curve or "demanda" in curve:
        ax.plot(xs, 10 + shift - xs * 0.8, color="#1f77b4", lw=2, ls="--", label="Nueva demanda (D')")
    else:
        ax.plot(xs, 2 - shift + xs * 0.8, color="#ff7f0e", lw=2, ls="--", label="Nueva oferta (O')")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("Cantidad")
    ax.set_ylabel("Precio")
    ax.legend(fontsize=9, loc="upper center")
    img = save_fig(fig)
    if rnd.random() < 0.5:
        c = f"El precio {p} y la cantidad transada {q}"
        w = [f"El precio {pp} y la cantidad transada {qq}" for pp, qq in [("sube", "sube"), ("baja", "baja"), ("baja", "sube"), ("sube", "baja")] if (pp, qq) != (p, q)]
        return make(ECO, "El gráfico muestra el desplazamiento de una curva en un mercado (línea punteada). Respecto del equilibrio inicial, ¿qué ocurre?", c, w,
                    f"{curve}: el nuevo cruce de las curvas muestra que el precio {p} y la cantidad {q}.", img)
    pool = [x for x in MARKET_SHOCKS if x[1] == curve]
    ok = rnd.choice(pool)[0]
    bad = [x[0] for x in MARKET_SHOCKS if x[1] != curve]
    return make(ECO, "¿Cuál de las siguientes situaciones podría explicar el desplazamiento que muestra el gráfico (línea punteada)?", cap(ok),
                [cap(b) for b in rnd.sample(bad, 4)], f"{cap(ok)}: {low(curve)}.", img)


def g_pyramid():
    young = rnd.random() < 0.5
    ages = ["0-14", "15-29", "30-44", "45-59", "60-74", "75+"]
    vals = [14, 12, 10, 7, 4, 2] if young else [6, 8, 9, 10, 9, 7]
    vals = [v + rnd.choice([-1, 0, 1]) for v in vals]
    fig, ax = plt.subplots(figsize=(5.4, 3.8))
    y = np.arange(len(ages))
    ax.barh(y, [-v for v in vals], color="#1f77b4", label="Hombres")
    ax.barh(y, vals, color="#ff7f0e", label="Mujeres")
    ax.set_yticks(y)
    ax.set_yticklabels(ages)
    ax.set_xticks([-15, -10, -5, 0, 5, 10, 15])
    ax.set_xticklabels(["15", "10", "5", "0", "5", "10", "15"])
    ax.set_xlabel("% de la población")
    ax.set_title(f"Pirámide de población del país ficticio {'X' if young else 'Y'}")
    ax.legend(fontsize=9)
    img = save_fig(fig)
    if young:
        ans = "Una población joven, con alta natalidad"
        w = ["Una población envejecida, con baja natalidad", "Una población sin niños", "Una población formada solo por adultos mayores"]
        ex = "La base ancha indica muchos niños y jóvenes: alta natalidad."
    else:
        ans = "Una población envejecida, con baja natalidad y alta esperanza de vida"
        w = ["Una población joven, con alta natalidad", "Una población con muy baja esperanza de vida", "Una población que crece muy rápido por nacimientos"]
        ex = "La base angosta y la cima ancha indican pocos nacimientos y muchas personas mayores."
    if rnd.random() < 0.5:
        return make(HIS, "¿Qué característica demográfica muestra la pirámide de población?", ans, w, ex, img)
    if young:
        return make(ECO, "Según la pirámide, ¿qué necesidad pública será más urgente en los próximos años en este país?", "Más escuelas y empleos para jóvenes",
                    ["Más residencias para adultos mayores", "Reducir el número de colegios", "Disminuir los servicios de maternidad"], ex, img)
    return make(ECO, "Según la pirámide, ¿qué desafío enfrentará con mayor probabilidad este país?", "Financiar pensiones y salud para una población mayor creciente",
                ["Construir muchas salas cuna nuevas", "Falta de adultos mayores", "Exceso de niños en las escuelas"], ex, img)


def g_line_data():
    var, unit = rnd.choice([("Tasa de desempleo", "%"), ("Inflación anual", "%"), ("Exportaciones", "miles de millones de US$"), ("Población urbana", "%")])
    years = list(range(rnd.choice([1950, 1960, 1970, 1980, 1990]), 0, 1))[:0] or None
    start = rnd.choice([1950, 1960, 1970, 1980, 1990])
    years = [start + 5 * i for i in range(7)]
    vals = [rnd.randint(3, 25) for _ in years]
    if len(set(vals)) < 7:
        raise Skip()
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(years, vals, marker="o", color="#1f77b4", lw=2)
    for x, v in zip(years, vals):
        ax.annotate(str(v), (x, v), textcoords="offset points", xytext=(0, 7), ha="center", fontsize=10)
    ax.set_xticks(years)
    ax.set_ylabel(unit)
    ax.set_ylim(0, max(vals) + 5)
    ax.grid(alpha=0.3)
    ax.set_title(f"{var} en un país ficticio")
    img = save_fig(fig)
    k = rnd.randint(1, 3)
    if k == 1:
        y = years[vals.index(max(vals))]
        c, w = str(y), [str(x) for x in years if x != y]
        return make(ECO, f"Según el gráfico, ¿en qué año se registró el valor más alto de {low(var)}?", c, w, f"El punto más alto corresponde a {y} ({max(vals)}).", img)
    if k == 2:
        i, j = sorted(rnd.sample(range(7), 2))
        d = vals[j] - vals[i]
        c, w = numeric_options(d, [vals[i] + vals[j], -d, vals[j]], step=2, positive=False, fn=lambda v: fint(v))
        return make(ECO, f"Según el gráfico, ¿cuánto cambió {low(var)} entre {years[i]} y {years[j]}? (valor final − valor inicial, en {unit})", c, w,
                    f"{vals[j]} − {vals[i]} = {fint(vals[j] - vals[i])}.", img)
    ans = "Muestra la evolución de un indicador, pero por sí solo no explica sus causas"
    w = ["Demuestra cuál fue la causa de cada cambio", "Permite conocer las opiniones de la población", "Muestra datos de todos los países del mundo"]
    return make(HIS, "¿Qué se puede afirmar correctamente sobre la información del gráfico como fuente?", ans, w,
                "Un gráfico estadístico describe datos; para explicar causas se necesitan otras fuentes y análisis.", img)


def g_labor_table():
    regions = ["Región Norte", "Región Centro", "Región Sur"]
    rows = []
    for r in regions:
        FT = rnd.randrange(100, 1001, 50) * 1000
        rate = rnd.choice([4, 5, 6, 8, 10, 12, 15])
        rows.append((r, FT, FT * rate // 100, rate))
    if len({x[3] for x in rows}) < 3:
        raise Skip()
    fig, ax = plt.subplots(figsize=(6.2, 2.2))
    ax.axis("off")
    tbl = ax.table(cellText=[[r, fint(ft), fint(d)] for r, ft, d, _ in rows], colLabels=["Región (país ficticio)", "Fuerza de trabajo", "Desocupados"], loc="center", cellLoc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(12)
    tbl.scale(1, 1.7)
    tbl.auto_set_column_width([0, 1, 2])
    img = save_fig(fig)
    if rnd.random() < 0.5:
        best = max(rows, key=lambda x: x[3])
        return make(ECO, "Según la tabla, ¿qué región tiene la mayor tasa de desempleo?", best[0], [r for r in regions if r != best[0]] + ["Todas tienen la misma tasa"],
                    "Tasa = desocupados / fuerza de trabajo: " + "; ".join(f"{r}: {t}%" for r, _, _, t in rows) + ".", img)
    r, ft, d, t = rnd.choice(rows)
    c, w = numeric_options(t, [100 - t, t * 2, t + 3], step=1, fn=pct)
    return make(ECO, f"Según la tabla, ¿cuál es la tasa de desempleo de la {r}?", c, w, f"{fint(d)}/{fint(ft)} · 100 = {t}%.", img)


POWERS = [("Poder Ejecutivo", ["Presidente de la República", "Ministros de Estado"]),
          ("Poder Legislativo", ["Senado", "Cámara de Diputadas y Diputados"]),
          ("Poder Judicial", ["Corte Suprema", "Cortes de Apelaciones"])]


_pw = [0]


def g_powers():
    hide = _pw[0] % 3
    ask_name = (_pw[0] // 3) % 2 == 0
    _pw[0] += 1
    fig, ax = plt.subplots(figsize=(9.6, 3.2))
    ax.axis("off")
    for i, (p, parts) in enumerate(POWERS):
        x = 0.02 + i * 0.33
        ax.add_patch(plt.Rectangle((x, 0.08), 0.30, 0.84, fill=True, facecolor="#e6f0fa", edgecolor="#1f77b4", lw=2, transform=ax.transAxes))
        ax.text(x + 0.15, 0.76, "X" if i == hide else p, ha="center", fontsize=13, fontweight="bold", transform=ax.transAxes, color="#d62728" if i == hide else "black")
        ax.text(x + 0.15, 0.4, "\n\n".join(parts).replace("Cámara de Diputadas y Diputados", "Cámara de Diputadas\ny Diputados"), ha="center", va="center", fontsize=10, transform=ax.transAxes)
    ax.set_title("Organización de los poderes del Estado de Chile")
    img = save_fig(fig)
    name = POWERS[hide][0]
    funcs = {"Poder Ejecutivo": "Gobernar y administrar el Estado", "Poder Legislativo": "Elaborar y aprobar las leyes",
             "Poder Judicial": "Resolver conflictos y juzgar según las leyes"}
    if ask_name:
        return make(CIU, "En el esquema, ¿qué poder del Estado corresponde a la X?", name, [p for p, _ in POWERS if p != name] + ["Poder Electoral"],
                    f"{', '.join(POWERS[hide][1])} forman parte del {name}.", img)
    return make(CIU, "En el esquema, ¿cuál es la función principal del poder del Estado marcado con X?", funcs[name], [v for k, v in funcs.items() if k != name] + ["Controlar la inflación"],
                f"La X corresponde al {name}: {low(funcs[name])}.", img)


GRAPH_PLAN = [(g_timeline, 32), (g_votes, 26), (g_supply_demand, 12), (g_pyramid, 6), (g_line_data, 12), (g_labor_table, 6), (g_powers, 6)]


def build():
    if os.path.isdir(IMG_DIR):
        for f in os.listdir(IMG_DIR):
            if f.endswith(".png"):
                os.remove(os.path.join(IMG_DIR, f))
    seen, out = set(), []

    def add(q):
        key = q["enunciado"] + "|" + q["alternativas"][q["correcta"]]
        if key in seen:
            return False
        seen.add(key)
        out.append(q)
        return True

    for eje, enun, c, w, ex in bank_items():
        add(make(eje, enun, c, rnd.sample(w, min(len(w), 6)), ex))
    n_bank = len(out)
    i = guard = 0
    while len(out) < N_TEXT:
        t = CALC[i % len(CALC)]
        i += 1
        guard += 1
        if guard > 200000:
            raise RuntimeError("No se completaron las preguntas de texto.")
        for _ in range(60):
            try:
                if add(t()):
                    break
            except (Skip, ZeroDivisionError):
                continue
    for fn, n in GRAPH_PLAN:
        made = tries = 0
        while made < n:
            tries += 1
            if tries > 1000:
                raise RuntimeError(fn.__name__)
            before = _img[0]
            try:
                q = fn()
            except (Skip, ZeroDivisionError):
                if _img[0] > before:
                    p = os.path.join(IMG_DIR, f"historia_img_{_img[0]:03d}.png")
                    if os.path.exists(p):
                        os.remove(p)
                    _img[0] -= 1
                continue
            out.append(q)
            made += 1
    rnd.shuffle(out)
    ordered = []
    for n, q in enumerate(out, 1):
        item = {"id": f"historia_{n:03d}", "prueba": "historia", "eje": q["eje"], "enunciado": q["enunciado"],
                "alternativas": q["alternativas"], "correcta": q["correcta"], "explicacion": q["explicacion"]}
        if "imagen" in q:
            item["imagen"] = q["imagen"]
        ordered.append(item)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(ordered, f, ensure_ascii=False, indent=1)
    return ordered, n_bank


if __name__ == "__main__":
    qs, n_bank = build()
    assert len(qs) == N_TEXT + N_GRAPH
    for q in qs:
        assert len(q["alternativas"]) == 4 and len(set(q["alternativas"])) == 4, q
        if "imagen" in q:
            assert os.path.exists(os.path.join(ROOT, q["imagen"]))
    assert sum(1 for q in qs if "imagen" in q) == N_GRAPH == len(os.listdir(IMG_DIR))
    print(f"OK: {len(qs)} preguntas ({n_bank} de bancos), 100 con imagen. Por eje: {dict(Counter(q['eje'] for q in qs))}")
