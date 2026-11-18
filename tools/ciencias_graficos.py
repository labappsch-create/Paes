"""Preguntas de Ciencias con gráficos o imágenes. Cada gráfico se dibuja con los
mismos datos que usa el programa para calcular la respuesta."""
import os
from fractions import Fraction

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from ciencias_comun import (BIO, FIS, QUI, IMG_DIR, MINUS, Skip, fint, fmt, make,  # noqa: E402
                            numeric_options, rnd, unit)

plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})
_img = [0]


def save_fig(fig):
    _img[0] += 1
    name = f"ciencias_img_{_img[0]:03d}.png"
    os.makedirs(IMG_DIR, exist_ok=True)
    fig.savefig(os.path.join(IMG_DIR, name), dpi=100, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return f"assets/images/ciencias/{name}"


def grid(ax):
    ax.grid(alpha=0.35)


# ------------------------------------------------------------------ FÍSICA
def g_xt():
    x0 = rnd.choice([0, 5, 10, 20, 30])
    v = rnd.choice([1, 2, 3, 4, 5, -2, -3])
    T = rnd.choice([5, 6, 8, 10])
    if x0 + v * T < 0:
        raise Skip()
    ts = list(range(0, T + 1))
    xs = [x0 + v * t for t in ts]
    fig, ax = plt.subplots(figsize=(5.6, 3.8))
    ax.plot(ts, xs, color="#1f77b4", lw=2, marker="o", ms=3)
    ax.set_xlabel("Tiempo (s)")
    ax.set_ylabel("Posición (m)")
    ax.set_xticks(ts)
    ax.set_ylim(min(xs) - 5 if min(xs) >= 5 else 0, max(xs) + 5)
    grid(ax)
    ax.set_title("Posición de un móvil en el tiempo")
    img = save_fig(fig)
    k = rnd.randint(1, 3)
    if k == 1:
        c, w = numeric_options(v, [-v, x0, xs[-1] // T if T else 1, v * 2], step=1, positive=False, fn=unit("m/s"))
        return make(FIS, "El gráfico muestra la posición de un móvil que se mueve en línea recta. ¿Cuál es su velocidad?", c, w,
                    f"Velocidad = pendiente = ({xs[-1]} − {x0}) m / {T} s = {fint(v)} m/s.", img)
    if k == 2:
        d = abs(xs[-1] - x0)
        c, w = numeric_options(d, [xs[-1], x0, abs(v) * (T - 1)], step=abs(v), fn=unit("m"))
        return make(FIS, f"Según el gráfico, ¿qué distancia recorre el móvil entre t = 0 s y t = {T} s?", c, w, f"|{xs[-1]} − {x0}| = {d} m.", img)
    ans = "Movimiento rectilíneo uniforme (velocidad constante)"
    w = ["Movimiento uniformemente acelerado", "El móvil está en reposo", "Movimiento con velocidad que aumenta", "Caída libre"]
    return make(FIS, "¿Qué tipo de movimiento representa el gráfico de posición versus tiempo?", ans, w,
                "El gráfico posición-tiempo es una recta inclinada: la posición cambia lo mismo en cada segundo.", img)


def g_vt():
    v0 = rnd.choice([0, 2, 4, 5, 10])
    a = rnd.choice([1, 2, 3, 4, -1, -2])
    T = rnd.choice([4, 5, 6, 8, 10])
    vf = v0 + a * T
    if vf < 0 or (a * T * T) % 2:
        raise Skip()
    ts = list(range(0, T + 1))
    vs = [v0 + a * t for t in ts]
    fig, ax = plt.subplots(figsize=(5.6, 3.8))
    ax.plot(ts, vs, color="#d62728", lw=2, marker="o", ms=3)
    ax.fill_between(ts, vs, color="#d62728", alpha=0.12)
    ax.set_xlabel("Tiempo (s)")
    ax.set_ylabel("Velocidad (m/s)")
    ax.set_xticks(ts)
    ax.set_ylim(0, max(vs) + 3)
    grid(ax)
    ax.set_title("Velocidad de un móvil en el tiempo")
    img = save_fig(fig)
    if rnd.random() < 0.5:
        c, w = numeric_options(a, [-a, vf, vf // T if T else 1, a * 2], step=1, positive=False, fn=unit("m/s²"))
        return make(FIS, "El gráfico muestra la velocidad de un móvil en función del tiempo. ¿Cuál es su aceleración?", c, w,
                    f"a = pendiente = ({vf} − {v0}) m/s / {T} s = {fint(a)} m/s².", img)
    d = v0 * T + a * T * T // 2
    c, w = numeric_options(d, [vf * T, vf, v0 * T if v0 * T != d else d + 5], step=max(2, d // 10), fn=unit("m"))
    return make(FIS, f"Según el gráfico de velocidad versus tiempo, ¿qué distancia recorre el móvil entre t = 0 s y t = {T} s?", c, w,
                f"La distancia es el área bajo la curva: {v0}·{T} + ½·{T}·{abs(vf - v0)} = {d} m.", img)


def g_wave():
    A = rnd.choice([1, 2, 3, 4, 5])
    lam = rnd.choice([2, 4, 5, 6, 8])
    L = lam * 2
    xs = np.linspace(0, L, 500)
    ys = A * np.sin(2 * np.pi * xs / lam)
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    ax.plot(xs, ys, color="#1f77b4", lw=2)
    ax.axhline(0, color="black", lw=1)
    ax.set_xticks(range(0, L + 1))
    ax.set_yticks(range(-A - 1, A + 2))
    ax.set_xlabel("Posición (m)")
    ax.set_ylabel("Desplazamiento (cm)")
    grid(ax)
    img = save_fig(fig)
    k = rnd.randint(1, 3)
    if k == 1:
        c, w = numeric_options(A, [2 * A, lam, A + 1], step=1, fn=unit("cm"))
        return make(FIS, "El gráfico muestra una onda en un instante. ¿Cuál es su amplitud?", c, w, f"La amplitud es el desplazamiento máximo desde el equilibrio: {A} cm.", img)
    if k == 2:
        c, w = numeric_options(lam, [lam // 2 or 1, L, A], step=1, fn=unit("m"))
        return make(FIS, "El gráfico muestra una onda en un instante. ¿Cuál es su longitud de onda?", c, w, f"Una onda completa (dos crestas consecutivas) mide {lam} m.", img)
    f = rnd.choice([2, 3, 5, 10])
    c, w = numeric_options(lam * f, [lam + f, Fraction(lam, f), A * f], step=lam, fn=unit("m/s"))
    return make(FIS, f"La onda del gráfico tiene una frecuencia de {f} Hz. ¿Cuál es su rapidez de propagación?", c, w,
                f"Del gráfico, λ = {lam} m. Entonces v = λ·f = {lam}·{f} = {lam * f} m/s.", img)


# ------------------------------------------------------------------ QUÍMICA
def g_solubility():
    temps = [0, 20, 40, 60, 80, 100]
    names = ["Sal A", "Sal B", "Sal C"]
    curves = []
    for _ in names:
        s0 = rnd.randrange(10, 41, 5)
        slope = rnd.choice([5, 10, 15, 20])
        curves.append([s0 + slope * i for i in range(6)])
    if len({c[1] for c in curves}) < 3 or len({c[3] for c in curves}) < 3:
        raise Skip()
    fig, ax = plt.subplots(figsize=(5.8, 4.2))
    cols = ["#1f77b4", "#ff7f0e", "#2ca02c"]
    for n, cv, col in zip(names, curves, cols):
        ax.plot(temps, cv, marker="o", color=col, lw=2, label=n)
    ax.set_xlabel("Temperatura (°C)")
    ax.set_ylabel("Solubilidad (g / 100 g de agua)")
    ax.set_xticks(temps)
    ax.set_yticks(range(0, max(max(c) for c in curves) + 11, 10))
    grid(ax)
    ax.legend()
    img = save_fig(fig)
    i = rnd.randrange(3)
    j = rnd.randrange(1, 6)
    T = temps[j]
    if len({c[j] for c in curves}) < 3:
        raise Skip()
    k = rnd.randint(1, 3)
    if k == 1:
        v = curves[i][j]
        c, w = numeric_options(v, [curves[(i + 1) % 3][j], curves[i][j - 1], v + 10], step=5, fn=unit("g"))
        return make(QUI, f"Según el gráfico, ¿cuántos gramos de {names[i]} se disuelven como máximo en 100 g de agua a {T} °C?", c, w, f"Se lee la curva de {names[i]} a {T} °C: {v} g.", img)
    if k == 2:
        vals = [c[j] for c in curves]
        best = names[vals.index(max(vals))]
        return make(QUI, f"Según el gráfico, ¿cuál de las sales es más soluble a {T} °C?", best, [n for n in names if n != best] + ["Todas tienen la misma solubilidad"],
                    f"A {T} °C la curva más alta es la de {best} ({max(vals)} g).", img)
    hi, lo = rnd.sample(range(1, 6), 2)
    if hi < lo:
        hi, lo = lo, hi
    d = curves[i][hi] - curves[i][lo]
    c, w = numeric_options(d, [curves[i][hi], curves[i][lo], d * 2], step=5, fn=unit("g"))
    return make(QUI, f"Una solución saturada de {names[i]} en 100 g de agua a {temps[hi]} °C se enfría hasta {temps[lo]} °C. Según el gráfico, ¿qué masa de sal cristaliza (precipita)?", c, w,
                f"{curves[i][hi]} g − {curves[i][lo]} g = {d} g.", img)


def g_heating():
    fig, ax = plt.subplots(figsize=(6, 3.8))
    ts = [0, 2, 6, 10, 16, 20]
    Ts = [-20, 0, 0, 100, 100, 120]
    ax.plot(ts, Ts, color="#d62728", lw=2, marker="o", ms=3)
    labels = ["A", "B", "C", "D", "E"]
    for i, lab in enumerate(labels):
        ax.text((ts[i] + ts[i + 1]) / 2, (Ts[i] + Ts[i + 1]) / 2 + 7, lab, ha="center", fontsize=12, color="#1f77b4")
    ax.set_xlabel("Tiempo (min)")
    ax.set_ylabel("Temperatura (°C)")
    ax.set_yticks(range(-20, 141, 20))
    grid(ax)
    ax.set_title("Calentamiento de una muestra de agua")
    img = save_fig(fig)
    k = rnd.choice(["fus", "vap", "liq", "temp", "gas"])
    opts = ["Tramo A", "Tramo B", "Tramo C", "Tramo D", "Tramo E"]
    if k == "fus":
        return make(QUI, "En el gráfico de calentamiento del agua, ¿en qué tramo ocurre la fusión (el hielo se derrite)?", "Tramo B", [o for o in opts if o != "Tramo B"],
                    "En el tramo B la temperatura se mantiene en 0 °C: el calor se usa para cambiar de sólido a líquido.", img)
    if k == "vap":
        return make(QUI, "En el gráfico de calentamiento del agua, ¿en qué tramo ocurre la ebullición?", "Tramo D", [o for o in opts if o != "Tramo D"],
                    "En el tramo D la temperatura se mantiene en 100 °C mientras el líquido pasa a gas.", img)
    if k == "liq":
        return make(QUI, "En el gráfico, ¿en qué tramo el agua se encuentra solo en estado líquido y su temperatura aumenta?", "Tramo C", [o for o in opts if o != "Tramo C"],
                    "Entre 0 °C y 100 °C (tramo C) el agua es líquida y se calienta.", img)
    if k == "gas":
        return make(QUI, "En el gráfico, ¿en qué tramo el agua está solo en estado gaseoso?", "Tramo E", [o for o in opts if o != "Tramo E"],
                    "Sobre 100 °C (tramo E) toda el agua es vapor.", img)
    ans = "La energía se usa para cambiar de estado, no para subir la temperatura"
    w = ["El mechero se apagó", "El agua pierde calor", "La masa de agua aumenta", "El termómetro dejó de funcionar"]
    return make(QUI, "¿Por qué la temperatura se mantiene constante en los tramos B y D del gráfico?", ans, w,
                "Durante un cambio de estado el calor absorbido rompe las interacciones entre partículas (calor latente).", img)


MATERIALS = ["Corcho", "Madera de pino", "Hielo", "Aceite", "Aluminio", "Vidrio", "Hierro", "Plástico PVC", "Cobre", "Goma"]
DENS = {"Corcho": 0.25, "Madera de pino": 0.5, "Hielo": 0.92, "Aceite": 0.9, "Aluminio": 2.7, "Vidrio": 2.5, "Hierro": 7.9,
        "Plástico PVC": 1.4, "Cobre": 8.9, "Goma": 1.2}


def g_density():
    mats = rnd.sample(MATERIALS, 4)
    rows = []
    for m in mats:
        V = rnd.choice([10, 20, 40, 50, 100])
        rows.append((m, round(DENS[m] * V, 1), V))
    fig, ax = plt.subplots(figsize=(5.2, 2.6))
    ax.axis("off")
    tbl = ax.table(cellText=[[m, fmt(ms), str(v)] for m, ms, v in rows], colLabels=["Objeto", "Masa (g)", "Volumen (cm³)"], loc="center", cellLoc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(12)
    tbl.scale(1, 1.7)
    tbl.auto_set_column_width([0, 1, 2])
    img = save_fig(fig)
    dens = {m: ms / v for m, ms, v in rows}
    k = rnd.randint(1, 3)
    if k == 1:
        best = max(dens, key=dens.get)
        return make(QUI, "La tabla muestra la masa y el volumen de cuatro objetos macizos. ¿Cuál tiene mayor densidad?", best, [m for m in mats if m != best],
                    f"ρ = m/V; la mayor es la de {best}: {fmt(dens[best])} g/cm³.", img)
    if k == 2:
        floaters = [m for m in mats if dens[m] < 1]
        if len(floaters) != 1:
            raise Skip()
        f = floaters[0]
        return make(QUI, "La tabla muestra la masa y el volumen de cuatro objetos. Si se colocan en agua (densidad 1 g/cm³), ¿cuál de ellos flota?", f, [m for m in mats if m != f],
                    f"Flota el objeto con densidad menor que 1 g/cm³: {f} ({fmt(dens[f])} g/cm³).", img)
    m, ms, v = rnd.choice(rows)
    c, w = numeric_options(dens[m], [ms * v / 100, v / ms, dens[m] * 2], step=0.1, fn=unit("g/cm³"))
    return make(QUI, f"Según la tabla, ¿cuál es la densidad del objeto «{m}»?", c, w, f"ρ = {fmt(ms)} g / {v} cm³ = {fmt(dens[m])} g/cm³.", img)


# ------------------------------------------------------------------ BIOLOGÍA
def g_enzyme():
    if rnd.random() < 0.5:
        T1, T2 = rnd.sample([20, 30, 35, 40, 50, 60, 70], 2)
        xs = np.linspace(0, 90, 400)
        fig, ax = plt.subplots(figsize=(5.8, 3.8))
        for T0, col, lab in ((T1, "#1f77b4", "Enzima X"), (T2, "#ff7f0e", "Enzima Y")):
            ax.plot(xs, 100 * np.exp(-((xs - T0) / 12) ** 2), color=col, lw=2, label=lab)
        ax.set_xticks(range(0, 91, 10))
        ax.set_xlabel("Temperatura (°C)")
        ax.set_ylabel("Actividad enzimática (%)")
        grid(ax)
        ax.legend()
        img = save_fig(fig)
        which = rnd.choice([("Enzima X", T1), ("Enzima Y", T2)])
        c, w = numeric_options(which[1], [T1 if which[1] == T2 else T2, 90, which[1] + 20], step=10, fn=unit("°C"))
        return make(BIO, f"El gráfico muestra la actividad de dos enzimas según la temperatura. ¿Cuál es la temperatura óptima de la {which[0]}?", c, w,
                    f"La temperatura óptima es donde la actividad es máxima: {which[1]} °C.", img)
    p1, p2 = rnd.choice([(2, 8), (2, 7), (3, 9), (5, 8), (2, 10)])
    xs = np.linspace(0, 14, 400)
    fig, ax = plt.subplots(figsize=(5.8, 3.8))
    ax.plot(xs, 100 * np.exp(-((xs - p1) / 1.4) ** 2), color="#1f77b4", lw=2, label="Enzima X")
    ax.plot(xs, 100 * np.exp(-((xs - p2) / 1.4) ** 2), color="#ff7f0e", lw=2, label="Enzima Y")
    ax.set_xticks(range(0, 15))
    ax.set_xlabel("pH")
    ax.set_ylabel("Actividad enzimática (%)")
    grid(ax)
    ax.legend()
    img = save_fig(fig)
    if rnd.random() < 0.5:
        return make(BIO, "Según el gráfico, ¿qué enzima funciona mejor en un medio ácido, como el estómago?", "Enzima X",
                    ["Enzima Y", "Ambas por igual", "Ninguna de las dos"], f"La enzima X tiene su máxima actividad a pH {p1}, que es ácido.", img)
    c, w = numeric_options(p2, [p1, 7 if p2 != 7 else 6, 14], step=1, fn=lambda v: f"pH {fmt(v)}")
    return make(BIO, "Según el gráfico, ¿cuál es el pH óptimo de la enzima Y?", c, w, f"La curva de la enzima Y alcanza su máximo en pH {p2}.", img)


def g_population():
    K = rnd.choice([200, 400, 500, 600, 800, 1000])
    N0 = K // rnd.choice([10, 20])
    r = rnd.uniform(0.6, 0.9)
    ts = np.linspace(0, 20, 300)
    Ns = K / (1 + (K / N0 - 1) * np.exp(-r * ts))
    fig, ax = plt.subplots(figsize=(5.8, 3.8))
    ax.plot(ts, Ns, color="#2ca02c", lw=2)
    ax.axhline(K, color="gray", ls="--", lw=1)
    ax.set_xlabel("Tiempo (semanas)")
    ax.set_ylabel("Número de individuos")
    ax.set_ylim(0, K * 1.15)
    ax.set_yticks(range(0, int(K * 1.15) + 1, K // 5))
    grid(ax)
    img = save_fig(fig)
    if rnd.random() < 0.6:
        c, w = numeric_options(K, [K // 2, N0, K * 2], step=K // 5)
        return make(BIO, "El gráfico muestra el crecimiento de una población. ¿Cuál es la capacidad de carga del ambiente?", c, w,
                    f"La capacidad de carga es el máximo de individuos que el ambiente puede sostener: la población se estabiliza en {fint(K)}.", img)
    ans = "Los recursos del ambiente (alimento, espacio) se vuelven limitantes"
    w = ["La población dejó de reproducirse por completo", "Los individuos viven para siempre", "Aumenta la cantidad de recursos", "No hay competencia entre individuos"]
    return make(BIO, "En el gráfico, ¿por qué la población deja de crecer después de un tiempo?", ans, w,
                "Es un crecimiento logístico: al aumentar la población, la competencia por recursos frena el crecimiento.", img)


def g_punnett():
    L = rnd.choice(["A", "B", "R", "T"])
    l = L.lower()
    p1, p2 = rnd.choice([(L + l, L + l), (L + l, l + l), (L + L, l + l), (L + L, L + l)])
    cells = [[sorted(a + b, key=lambda ch: (ch.islower(), ch)) for b in p2] for a in p1]
    cells = [["".join(c) for c in row] for row in cells]
    fig, ax = plt.subplots(figsize=(3.6, 3.6))
    ax.axis("off")
    tbl = ax.table(cellText=[[p1[0], cells[0][0], cells[0][1]], [p1[1], cells[1][0], cells[1][1]]], colLabels=["", p2[0], p2[1]], loc="center", cellLoc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(16)
    tbl.scale(1, 2.6)
    for (r, c), cell in tbl.get_celld().items():
        if r == 0 or c == 0:
            cell.set_facecolor("#e6f0fa")
    ax.set_title(f"Cruce {p1} × {p2}", fontsize=13)
    img = save_fig(fig)
    flat = [c for row in cells for c in row]
    k = rnd.choice(["het", "rec", "dom"])
    if k == "het":
        v = Fraction(sum(1 for g in flat if g[0] != g[1]), 4)
        q = "Según el cuadro de Punnett, ¿qué proporción de la descendencia es heterocigota?"
        ex = f"Hay {sum(1 for g in flat if g[0] != g[1])} heterocigotos ({L}{l}) de 4."
    elif k == "rec":
        v = Fraction(sum(1 for g in flat if g == l + l), 4)
        q = f"Según el cuadro de Punnett, ¿qué proporción de la descendencia muestra el rasgo recesivo ({l}{l})?"
        ex = f"Hay {sum(1 for g in flat if g == l + l)} individuos {l}{l} de 4."
    else:
        v = Fraction(sum(1 for g in flat if L in g), 4)
        q = f"Si {L} es dominante sobre {l}, ¿qué proporción de la descendencia del cuadro muestra el rasgo dominante?"
        ex = f"Muestran el rasgo dominante los que tienen al menos un {L}: {sum(1 for g in flat if L in g)} de 4."
    def s(fr):
        return "0" if fr == 0 else ("1" if fr == 1 else f"{fr.numerator}/{fr.denominator}")
    opts = ["0", "1/4", "1/2", "3/4", "1"]
    return make(BIO, q, s(v), [o for o in opts if o != s(v)], ex, img)


def g_photosynthesis():
    dists = [10, 20, 30, 40, 50]
    base = rnd.randint(30, 60)
    bubbles = [base - i * rnd.randint(5, 8) for i in range(5)]
    if min(bubbles) <= 0:
        raise Skip()
    fig, ax = plt.subplots(figsize=(5.8, 3.8))
    ax.bar([str(d) for d in dists], bubbles, color="#2ca02c")
    for i, b in enumerate(bubbles):
        ax.text(i, b + 0.8, str(b), ha="center")
    ax.set_xlabel("Distancia de la lámpara a la planta (cm)")
    ax.set_ylabel("Burbujas de O₂ por minuto")
    ax.set_title("Fotosíntesis de una planta acuática (Elodea)")
    ax.set_ylim(0, max(bubbles) * 1.15)
    img = save_fig(fig)
    k = rnd.randint(1, 4)
    if k == 1:
        return make(BIO, "En el experimento del gráfico, ¿cuál es la variable independiente?", "La distancia de la lámpara (intensidad de luz)",
                    ["El número de burbujas de oxígeno", "El tipo de planta", "La cantidad de agua"], "La variable independiente es la que el investigador modifica: la distancia de la lámpara.", img)
    if k == 2:
        return make(BIO, "En el experimento del gráfico, ¿cuál es la variable dependiente?", "El número de burbujas de O₂ por minuto",
                    ["La distancia de la lámpara", "El color de la lámpara", "La especie de planta"], "La variable dependiente es la que se mide como resultado: las burbujas de O₂.", img)
    if k == 3:
        ans = "A menor distancia de la lámpara (más luz), mayor es la tasa de fotosíntesis"
        w = ["A mayor distancia de la lámpara, mayor es la tasa de fotosíntesis", "La luz no influye en la fotosíntesis", "La planta produce CO₂ en lugar de O₂", "La tasa de fotosíntesis es constante"]
        return make(BIO, "¿Qué conclusión es correcta según los resultados del gráfico?", ans, w, "Las burbujas de O₂ disminuyen a medida que la lámpara se aleja.", img)
    i, j = sorted(rnd.sample(range(5), 2))
    d = bubbles[i] - bubbles[j]
    c, w = numeric_options(d, [bubbles[i], bubbles[j], bubbles[i] + bubbles[j]], step=2)
    return make(BIO, f"Según el gráfico, ¿cuántas burbujas por minuto más se producen a {dists[i]} cm que a {dists[j]} cm?", c, w, f"{bubbles[i]} − {bubbles[j]} = {d}.", img)


def g_pyramid():
    E = rnd.choice([10000, 20000, 50000, 100000])
    pct = rnd.choice([10, 10, 20])
    levels = [E]
    for _ in range(3):
        levels.append(levels[-1] * pct // 100)
    names = ["Productores", "Consumidores primarios", "Consumidores secundarios", "Consumidores terciarios"]
    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    widths = [1.0, 0.85, 0.7, 0.55]
    for i, (wd, v) in enumerate(zip(widths, levels)):
        ax.barh(i, wd, left=(1 - wd) / 2, height=0.9, color=["#2ca02c", "#9acd32", "#ffb347", "#ff7f50"][i], edgecolor="black")
        ax.text(0.5, i, f"{names[i]}\n{fint(v)} kcal", ha="center", va="center", fontsize=10)
    ax.set_xlim(0, 1)
    ax.axis("off")
    ax.set_title("Pirámide de energía")
    img = save_fig(fig)
    if rnd.random() < 0.5:
        c, w = numeric_options(pct, [100 - pct, pct * 2, 1], step=5, fn=lambda v: f"{fmt(v)}%")
        return make(BIO, "Según la pirámide, ¿qué porcentaje de la energía de un nivel pasa al nivel siguiente?", c, w,
                    f"{fint(levels[1])}/{fint(levels[0])} = {pct}%. El resto se pierde principalmente como calor.", img)
    ans = "Se pierde principalmente como calor en la respiración y en actividades vitales"
    w = ["Se acumula en los productores", "Vuelve al Sol", "Se transforma en materia inorgánica sin pérdida", "Pasa completa al nivel siguiente"]
    return make(BIO, "En la pirámide, ¿por qué disminuye la energía disponible en cada nivel trófico?", ans, w,
                "En cada nivel los organismos usan energía para vivir y la liberan como calor.", img)


GRAPH_PLAN = [(g_xt, 12), (g_vt, 12), (g_wave, 10), (g_solubility, 10), (g_heating, 6), (g_density, 8),
              (g_enzyme, 10), (g_population, 6), (g_punnett, 12), (g_photosynthesis, 8), (g_pyramid, 6)]
