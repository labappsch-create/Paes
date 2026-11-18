"""Preguntas de Ciencias con gráfico, solo con contenidos del temario oficial.
Cada gráfico se dibuja con los mismos datos que usa el programa para calcular la respuesta."""
import os
from fractions import Fraction

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from ciencias2_calculos import itinerario  # noqa: E402
from ciencias_comun import (AMB, ATO, ELE, EST, HER, IMG_DIR, MEC, OND, ORG, PROC, Skip, fint, fmt,  # noqa: E402
                            make, numeric_options, rnd, sup, unit)

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


def sci(x):
    """Escribe un número en notación científica con coma decimal: 1,5 × 10⁸."""
    x = Fraction(x)
    e = 0
    while x >= 10:
        x /= 10
        e += 1
    while x < 1:
        x *= 10
        e -= 1
    return f"{fmt(x)} × 10{sup(e)}"


# ====================================================================== FÍSICA
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
    k = rnd.randint(1, 4)
    if k == 1:
        c, w = numeric_options(v, [-v, x0, v * 2], step=1, positive=False, fn=unit("m/s"))
        return make(MEC, "El gráfico muestra la posición de un móvil que se mueve en línea recta. ¿Cuál es su velocidad?", c, w,
                    f"Velocidad = pendiente = ({xs[-1]} − {x0}) m / {T} s = {fint(v)} m/s.", img)
    if k == 2:
        d = abs(xs[-1] - x0)
        c, w = numeric_options(d, [xs[-1], x0, abs(v) * (T - 1)], step=abs(v), fn=unit("m"))
        return make(MEC, f"Según el gráfico, ¿qué distancia recorre el móvil entre t = 0 s y t = {T} s?", c, w,
                    f"|{xs[-1]} − {x0}| = {d} m.", img)
    if k == 3:
        ans = itinerario(x0, v)
        w = [itinerario(x0, -v), itinerario(xs[-1], v), itinerario(abs(v), x0) if x0 else itinerario(abs(v), 1), itinerario(x0 + v, v)]
        return make(MEC, "¿Cuál es la ecuación de itinerario del móvil representado en el gráfico (x en metros y t en segundos)?", ans, w,
                    f"Posición inicial {x0} m y velocidad {fint(v)} m/s: x(t) = x₀ + v·t.", img)
    ans = "Movimiento rectilíneo uniforme (velocidad constante)"
    w = ["Movimiento rectilíneo uniformemente acelerado", "El móvil está en reposo", "Movimiento con velocidad que aumenta", "Caída libre"]
    return make(MEC, "¿Qué tipo de movimiento representa el gráfico de posición versus tiempo?", ans, w,
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
    k = rnd.randint(1, 3)
    if k == 1:
        c, w = numeric_options(a, [-a, vf, a * 2], step=1, positive=False, fn=unit("m/s²"))
        return make(MEC, "El gráfico muestra la velocidad de un móvil en función del tiempo. ¿Cuál es su aceleración?", c, w,
                    f"a = pendiente = ({vf} − {v0}) m/s / {T} s = {fint(a)} m/s².", img)
    if k == 2:
        d = v0 * T + a * T * T // 2
        c, w = numeric_options(d, [vf * T, vf, v0 * T if v0 * T != d else d + 5], step=max(2, d // 10), fn=unit("m"))
        return make(MEC, f"Según el gráfico de velocidad versus tiempo, ¿qué distancia recorre el móvil entre t = 0 s y t = {T} s?", c, w,
                    f"La distancia es el área bajo la curva: {v0}·{T} + ½·{T}·{abs(vf - v0)} = {d} m.", img)
    m = rnd.choice([2, 5, 10, 20])
    F = m * a
    c, w = numeric_options(F, [m, m + a, -F], step=m, positive=False, fn=unit("N"))
    return make(MEC, f"El gráfico corresponde a un carrito de {m} kg. ¿Cuál es la fuerza neta que actúa sobre él?", c, w,
                f"Del gráfico, a = {fint(a)} m/s²; F = m·a = {m}·{fint(a)} = {fint(F)} N.", img)


def g_onda_em():
    A = rnd.choice([1, 2, 3, 4])
    lam = rnd.choice([1, 2, 3, 5, 10])
    L = lam * 2
    xs = np.linspace(0, L, 500)
    ys = A * np.sin(2 * np.pi * xs / lam)
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    ax.plot(xs, ys, color="#1f77b4", lw=2)
    ax.axhline(0, color="black", lw=1)
    step = 1 if L <= 10 else 2
    ax.set_xticks(range(0, L + 1, step))
    ax.set_yticks(range(-A - 1, A + 2))
    ax.set_xlabel("Posición (m)")
    ax.set_ylabel("Campo eléctrico (unid. arb.)")
    ax.set_title("Onda de radio en un instante")
    grid(ax)
    img = save_fig(fig)
    if rnd.random() < 0.5:
        c, w = numeric_options(lam, [Fraction(lam, 2), L, A], step=1, fn=unit("m"))
        return make(OND, "El gráfico representa una onda de radio en un instante. ¿Cuál es su longitud de onda?", c, w,
                    f"Una onda completa (de una cresta a la siguiente) mide {lam} m.", img)
    f = Fraction(3 * 10 ** 8, lam)
    s = sci(f) + " Hz"
    w = [sci(f * 10) + " Hz", sci(f / 10) + " Hz", sci(Fraction(3 * 10 ** 8 * lam)) + " Hz", sci(f * 2) + " Hz"]
    return make(OND, "La onda de radio del gráfico viaja en el aire a 3 × 10⁸ m/s. ¿Cuál es su frecuencia?", s, w,
                f"Del gráfico, λ = {lam} m. f = c/λ = 3 × 10⁸/{lam} = {s}.", img)


def _resistor(ax, x0, y0, x1, y1, label):
    """Dibuja un resistor en zigzag entre dos puntos (horizontal o vertical)."""
    n = 6
    t = np.linspace(0, 1, 2 * n + 1)
    zz = np.array([0] + [(1 if i % 2 else -1) for i in range(1, 2 * n)] + [0]) * 0.12
    if y0 == y1:
        xs = x0 + 0.2 * (x1 - x0) + 0.6 * (x1 - x0) * t
        ys = y0 + zz
        ax.plot([x0, xs[0]], [y0, y0], "k", lw=2)
        ax.plot([xs[-1], x1], [y0, y0], "k", lw=2)
        ax.plot(xs, ys, "k", lw=2)
        ax.text((x0 + x1) / 2, y0 + 0.25, label, ha="center", fontsize=12, color="#1f4e9c")
    else:
        ys = y0 + 0.2 * (y1 - y0) + 0.6 * (y1 - y0) * t
        xs = x0 + zz
        ax.plot([x0, x0], [y0, ys[0]], "k", lw=2)
        ax.plot([x0, x0], [ys[-1], y1], "k", lw=2)
        ax.plot(xs, ys, "k", lw=2)
        ax.text(x0 + 0.25, (y0 + y1) / 2, label, va="center", fontsize=12, color="#1f4e9c")


def _bateria(ax, x, y0, y1, V):
    ym = (y0 + y1) / 2
    ax.plot([x, x], [y0, ym - 0.15], "k", lw=2)
    ax.plot([x, x], [ym + 0.15, y1], "k", lw=2)
    ax.plot([x - 0.3, x + 0.3], [ym + 0.15, ym + 0.15], "k", lw=2.5)
    ax.plot([x - 0.15, x + 0.15], [ym - 0.15, ym - 0.15], "k", lw=4)
    ax.text(x - 0.45, ym, f"{V} V", ha="right", va="center", fontsize=12, color="#b22222")
    ax.text(x + 0.35, ym + 0.2, "+", fontsize=11)


PARALLEL = [(3, 6, 2), (4, 4, 2), (6, 12, 4), (10, 15, 6), (20, 30, 12), (12, 24, 8), (6, 6, 3), (10, 10, 5), (4, 12, 3), (12, 12, 6)]


def g_circuito():
    tipo = rnd.choice(["serie", "paralelo", "mixto"])
    fig, ax = plt.subplots(figsize=(5.6, 3.6))
    ax.axis("off")
    ax.set_aspect("equal")
    if tipo == "serie":
        r1, r2 = rnd.sample([1, 2, 3, 4, 5, 6, 8, 10], 2)
        Rt = r1 + r2
        I = rnd.randint(1, 4)
        V = Rt * I
        _bateria(ax, 0, 0, 2, V)
        ax.plot([0, 0.5], [2, 2], "k", lw=2)
        _resistor(ax, 0.5, 2, 2.5, 2, f"R₁ = {r1} Ω")
        ax.plot([2.5, 3], [2, 2], "k", lw=2)
        _resistor(ax, 3, 2, 3, 0, f"R₂ = {r2} Ω")
        ax.plot([0, 3], [0, 0], "k", lw=2)
        ax.set_xlim(-1.4, 4.4)
        ax.set_ylim(-0.4, 2.6)
        img = save_fig(fig)
        k = rnd.randint(1, 3)
        if k == 1:
            c, w = numeric_options(I, [V * Rt, V // r1 if V % r1 == 0 and V // r1 != I else I + 2, I * 2], step=1, fn=unit("A"))
            return make(ELE, "En el circuito de la figura, ¿qué corriente entrega la batería?", c, w,
                        f"En serie: R = {r1} + {r2} = {Rt} Ω; I = {V}/{Rt} = {I} A.", img)
        if k == 2:
            c, w = numeric_options(I * r1, [V, I * r2 if I * r2 != I * r1 else V - 1, I], step=1, fn=unit("V"))
            return make(ELE, "En el circuito de la figura, ¿cuál es el voltaje entre los extremos de R₁?", c, w,
                        f"I = {V}/{Rt} = {I} A; V₁ = I·R₁ = {I}·{r1} = {I * r1} V.", img)
        P = V * I
        c, w = numeric_options(P, [V, V + I, P * 2], step=max(2, P // 5), fn=unit("W"))
        return make(ELE, "¿Qué potencia total entrega la batería al circuito de la figura?", c, w,
                    f"I = {V}/{Rt} = {I} A; P = V·I = {V}·{I} = {P} W.", img)
    a, b, r = rnd.choice(PARALLEL)
    R1 = rnd.choice([1, 2, 3, 4, 6]) if tipo == "mixto" else 0
    Rt = R1 + r
    I = rnd.choice([1, 2, 3])
    V = Rt * I
    _bateria(ax, 0, 0, 2, V)
    if tipo == "mixto":
        ax.plot([0, 0.3], [2, 2], "k", lw=2)
        _resistor(ax, 0.3, 2, 2.0, 2, f"R₁ = {R1} Ω")
        x_a = 2.0
    else:
        ax.plot([0, 1.0], [2, 2], "k", lw=2)
        x_a = 1.0
    ax.plot([x_a, x_a + 2.2], [2, 2], "k", lw=2)
    _resistor(ax, x_a + 0.6, 2, x_a + 0.6, 0, f"{'R₂' if tipo == 'mixto' else 'R₁'} = {a} Ω")
    _resistor(ax, x_a + 2.2, 2, x_a + 2.2, 0, f"{'R₃' if tipo == 'mixto' else 'R₂'} = {b} Ω")
    ax.plot([0, x_a + 2.2], [0, 0], "k", lw=2)
    ax.set_xlim(-1.4, x_a + 3.6)
    ax.set_ylim(-0.4, 2.6)
    img = save_fig(fig)
    if tipo == "paralelo":
        if rnd.random() < 0.5:
            c, w = numeric_options(r, [a + b, abs(a - b) or a + 1, (a + b) // 2], step=1, fn=unit("Ω"))
            return make(ELE, "¿Cuál es la resistencia equivalente del circuito de la figura?", c, w,
                        f"En paralelo: R = ({a}·{b})/({a} + {b}) = {r} Ω.", img)
        Ia = Fraction(V, a)
        c, w = numeric_options(Ia, [Fraction(V, b), I, Fraction(V, a + b)], step=1, fn=unit("A"))
        return make(ELE, "En el circuito de la figura, ¿qué corriente pasa por R₁?", c, w,
                    f"En paralelo cada resistencia recibe los {V} V: I₁ = {V}/{a} = {fmt(Ia)} A.", img)
    if rnd.random() < 0.5:
        c, w = numeric_options(Rt, [R1 + a + b, r, R1 + (a + b) // 2], step=1, fn=unit("Ω"))
        return make(ELE, "¿Cuál es la resistencia equivalente del circuito mixto de la figura?", c, w,
                    f"R₂ y R₃ en paralelo: ({a}·{b})/({a} + {b}) = {r} Ω; más R₁ en serie: {R1} + {r} = {Rt} Ω.", img)
    c, w = numeric_options(I, [Fraction(V, R1 + a + b), Fraction(V, r), I * 2], step=1, fn=unit("A"))
    return make(ELE, "¿Qué corriente entrega la batería en el circuito mixto de la figura?", c, w,
                f"R equivalente = {R1} + {r} = {Rt} Ω; I = {V}/{Rt} = {I} A.", img)


ARTEFACTOS = [("Refrigerador", 200), ("Hervidor", 2000), ("Televisor", 100), ("Plancha", 1000), ("Microondas", 1200),
              ("Ampolleta LED", 10), ("Lavadora", 500), ("Secador de pelo", 1500), ("Computador", 300), ("Estufa eléctrica", 2000)]


def g_consumo():
    items = rnd.sample(ARTEFACTOS, 4)
    horas = [rnd.choice([1, 2, 4, 5, 10, 24]) if n in ("Refrigerador", "Ampolleta LED") else rnd.choice([1, 2, 3, 4, 5]) for n, _ in items]
    horas = [24 if n == "Refrigerador" else h for (n, _), h in zip(items, horas)]
    energia = [Fraction(p * h, 1000) for (_, p), h in zip(items, horas)]
    if len(set(energia)) < 4 or len({p for _, p in items}) < 4:
        raise Skip()
    fig, ax = plt.subplots(figsize=(6, 2.6))
    ax.axis("off")
    tbl = ax.table(cellText=[[n, fint(p), str(h)] for (n, p), h in zip(items, horas)],
                   colLabels=["Artefacto", "Potencia (W)", "Uso diario (h)"], loc="center", cellLoc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(12)
    tbl.scale(1, 1.7)
    tbl.auto_set_column_width([0, 1, 2])
    img = save_fig(fig)
    k = rnd.randint(1, 3)
    if k == 1:
        best = items[energia.index(max(energia))][0]
        return make(ELE, "La tabla muestra la potencia y el uso diario de cuatro artefactos de una casa. ¿Cuál consume más energía eléctrica al día?",
                    best, [n for n, _ in items if n != best],
                    "E = P·t. " + "; ".join(f"{n}: {fmt(e)} kWh" for (n, _), e in zip(items, energia)) + ".", img)
    if k == 2:
        i = rnd.randrange(4)
        n, p = items[i]
        e = energia[i]
        c, w = numeric_options(e, [p * horas[i], Fraction(p, 1000), e * 10], step=max(Fraction(1, 10), e / 4), fn=unit("kWh"))
        return make(ELE, f"Según la tabla, ¿cuánta energía consume el artefacto «{n}» en un día?", c, w,
                    f"E = {fmt(Fraction(p, 1000))} kW·{horas[i]} h = {fmt(e)} kWh.", img)
    best = items[[p for _, p in items].index(max(p for _, p in items))][0]
    return make(ELE, "Según la tabla, si todos los artefactos se conectan a 220 V, ¿cuál de ellos hace circular la mayor corriente mientras funciona?",
                best, [n for n, _ in items if n != best],
                f"I = P/V: con el mismo voltaje, la mayor corriente corresponde a la mayor potencia ({best}).", img)


# ====================================================================== QUÍMICA
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
    k = rnd.randint(1, 4)
    if k == 1:
        v = curves[i][j]
        c, w = numeric_options(v, [curves[(i + 1) % 3][j], curves[i][j - 1], v + 10], step=5, fn=unit("g"))
        return make(EST, f"Según el gráfico, ¿cuántos gramos de {names[i]} se disuelven como máximo en 100 g de agua a {T} °C?", c, w,
                    f"Se lee la curva de {names[i]} a {T} °C: {v} g.", img)
    if k == 2:
        vals = [c[j] for c in curves]
        best = names[vals.index(max(vals))]
        return make(EST, f"Según el gráfico, ¿cuál de las sales es más soluble a {T} °C?", best,
                    [n for n in names if n != best] + ["Todas tienen la misma solubilidad"],
                    f"A {T} °C la curva más alta es la de {best} ({max(vals)} g).", img)
    if k == 3:
        v = curves[i][j]
        m = rnd.choice([x for x in (v - 10, v - 5, v + 5, v + 10) if x > 0])
        ans = "Saturada, y quedan sólidos sin disolver" if m > v else "Insaturada"
        exc = "Saturada, y quedan sólidos sin disolver" if m <= v else "Insaturada"
        return make(EST, f"Se agregan {m} g de {names[i]} a 100 g de agua a {T} °C y se agita. Según el gráfico, ¿cómo queda la solución?", ans,
                    [exc, "Sobresaturada estable sin sólido", "No se forma ninguna solución"],
                    f"A {T} °C se disuelven como máximo {v} g; {m} g es {'más' if m > v else 'menos'} que eso.", img)
    hi, lo = sorted(rnd.sample(range(1, 6), 2), reverse=True)
    d = curves[i][hi] - curves[i][lo]
    c, w = numeric_options(d, [curves[i][hi], curves[i][lo], d * 2], step=5, fn=unit("g"))
    return make(EST, f"Una solución saturada de {names[i]} en 100 g de agua a {temps[hi]} °C se enfría hasta {temps[lo]} °C. Según el gráfico, ¿qué masa de sal cristaliza?", c, w,
                f"{curves[i][hi]} g − {curves[i][lo]} g = {d} g.", img)


MATERIALS = {"Corcho": 0.25, "Madera de pino": 0.5, "Hielo": 0.92, "Aceite": 0.9, "Aluminio": 2.7, "Vidrio": 2.5, "Hierro": 7.9,
             "Plástico PVC": 1.4, "Cobre": 8.9, "Goma": 1.2}


def g_density():
    mats = rnd.sample(list(MATERIALS), 4)
    rows = []
    for m in mats:
        V = rnd.choice([10, 20, 40, 50, 100])
        rows.append((m, round(MATERIALS[m] * V, 1), V))
    fig, ax = plt.subplots(figsize=(5.2, 2.6))
    ax.axis("off")
    tbl = ax.table(cellText=[[m, fmt(ms), str(v)] for m, ms, v in rows], colLabels=["Objeto", "Masa (g)", "Volumen (cm³)"],
                   loc="center", cellLoc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(12)
    tbl.scale(1, 1.7)
    tbl.auto_set_column_width([0, 1, 2])
    img = save_fig(fig)
    dens = {m: ms / v for m, ms, v in rows}
    k = rnd.randint(1, 3)
    if k == 1:
        best = max(dens, key=dens.get)
        return make(ATO, "La tabla muestra la masa y el volumen de cuatro objetos macizos. ¿Cuál tiene mayor densidad?", best,
                    [m for m in mats if m != best], f"ρ = m/V; la mayor es la de {best}: {fmt(dens[best])} g/cm³.", img)
    if k == 2:
        floaters = [m for m in mats if dens[m] < 1]
        if len(floaters) != 1:
            raise Skip()
        f = floaters[0]
        return make(ATO, "La tabla muestra la masa y el volumen de cuatro objetos. Si se colocan en agua (densidad 1 g/cm³), ¿cuál de ellos flota?", f,
                    [m for m in mats if m != f], f"Flota el objeto con densidad menor que 1 g/cm³: {f} ({fmt(dens[f])} g/cm³).", img)
    m, ms, v = rnd.choice(rows)
    c, w = numeric_options(dens[m], [ms * v / 100, v / ms, dens[m] * 2], step=0.1, fn=unit("g/cm³"))
    return make(ATO, f"Según la tabla, ¿cuál es la densidad del objeto «{m}»?", c, w, f"ρ = {fmt(ms)} g / {v} cm³ = {fmt(dens[m])} g/cm³.", img)


# Moléculas en fórmula lineal (topológica): cadena principal, orden de cada enlace y ramas (índice, átomo, orden).
MOLECULAS = [
    ("butano", ["C", "C", "C", "C"], [1, 1, 1], [], "Alcano"),
    ("pentano", ["C", "C", "C", "C", "C"], [1, 1, 1, 1], [], "Alcano"),
    ("hexano", ["C", "C", "C", "C", "C", "C"], [1, 1, 1, 1, 1], [], "Alcano"),
    ("1-buteno", ["C", "C", "C", "C"], [2, 1, 1], [], "Alqueno"),
    ("2-penteno", ["C", "C", "C", "C", "C"], [1, 2, 1, 1], [], "Alqueno"),
    ("1-propanol", ["C", "C", "C", "OH"], [1, 1, 1], [], "Alcohol"),
    ("2-butanol", ["C", "C", "C", "C"], [1, 1, 1], [(1, "OH", 1)], "Alcohol"),
    ("butanal", ["C", "C", "C", "C", "O"], [1, 1, 1, 2], [], "Aldehído"),
    ("butanona", ["C", "C", "C", "C"], [1, 1, 1], [(1, "O", 2)], "Cetona"),
    ("2-pentanona", ["C", "C", "C", "C", "C"], [1, 1, 1, 1], [(1, "O", 2)], "Cetona"),
    ("ácido propanoico", ["C", "C", "C", "OH"], [1, 1, 1], [(2, "O", 2)], "Ácido carboxílico"),
    ("ácido butanoico", ["C", "C", "C", "C", "OH"], [1, 1, 1, 1], [(3, "O", 2)], "Ácido carboxílico"),
    ("propanoato de metilo", ["C", "C", "C", "O", "C"], [1, 1, 1, 1], [(2, "O", 2)], "Éster"),
    ("dietil éter", ["C", "C", "O", "C", "C"], [1, 1, 1, 1], [], "Éter"),
    ("1-propanamina", ["C", "C", "C", "NH₂"], [1, 1, 1], [], "Amina"),
    ("propanamida", ["C", "C", "C", "NH₂"], [1, 1, 1], [(2, "O", 2)], "Amida"),
    ("1-clorobutano", ["C", "C", "C", "C", "Cl"], [1, 1, 1, 1], [], "Haluro (halogenuro de alquilo)"),
]
FUNCIONES = sorted({m[4] for m in MOLECULAS} | {"Éster", "Nitrilo", "Fenol"})
H_EN = {"OH": 1, "NH₂": 2, "O": 0, "Cl": 0, "N": 0}
SUBN = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def _formula(chain, bonds, branches):
    val = [0] * len(chain)
    for i, o in enumerate(bonds):
        val[i] += o
        val[i + 1] += o
    for i, at, o in branches:
        val[i] += o
    C = sum(1 for a in chain if a == "C")
    H = sum(4 - val[i] for i, a in enumerate(chain) if a == "C")
    atoms = [a for a in chain if a != "C"] + [b[1] for b in branches]
    H += sum(H_EN[a] for a in atoms)
    O = sum(1 for a in atoms if a in ("O", "OH"))
    N = sum(1 for a in atoms if a in ("NH₂", "N"))
    Cl = sum(1 for a in atoms if a == "Cl")

    def s(sym, n):
        return "" if n == 0 else (sym if n == 1 else sym + str(n).translate(SUBN))
    return s("C", C) + s("H", H) + s("Cl", Cl) + s("N", N) + s("O", O), C, H


def _draw_mol(chain, bonds, branches):
    pts = [(i * 0.87, 0.5 if i % 2 else 0.0) for i in range(len(chain))]
    fig, ax = plt.subplots(figsize=(0.9 * len(chain) + 1.4, 2.6))
    ax.axis("off")
    ax.set_aspect("equal")

    def bond(p, q, order):
        (x0, y0), (x1, y1) = p, q
        ax.plot([x0, x1], [y0, y1], "k", lw=2, zorder=1)
        dx, dy = x1 - x0, y1 - y0
        L = (dx * dx + dy * dy) ** 0.5
        nx, ny = -dy / L * 0.09, dx / L * 0.09
        offs = [1] if order == 2 else ([1, -1] if order == 3 else [])
        for s in offs:
            ax.plot([x0 + s * nx + dx * 0.15, x1 + s * nx - dx * 0.15], [y0 + s * ny + dy * 0.15, y1 + s * ny - dy * 0.15], "k", lw=2, zorder=1)

    for i, o in enumerate(bonds):
        bond(pts[i], pts[i + 1], o)
    for i, at, o in branches:
        x, y = pts[i]
        q = (x, y + 0.75) if y > 0 else (x, y - 0.75)
        bond((x, y), q, o)
        ax.text(q[0], q[1], at, ha="center", va="center", fontsize=15, color="#b22222",
                bbox=dict(facecolor="white", edgecolor="none", pad=1), zorder=3)
    for (x, y), a in zip(pts, chain):
        if a != "C":
            ax.text(x, y, a, ha="center", va="center", fontsize=15, color="#b22222" if a != "Cl" else "#2e8b57",
                    bbox=dict(facecolor="white", edgecolor="none", pad=1), zorder=3)
    ax.set_xlim(-0.5, pts[-1][0] + 0.6)
    ax.set_ylim(-1.0, 1.4)
    return fig


def g_organica():
    name, chain, bonds, branches, func = rnd.choice(MOLECULAS)
    form, C, H = _formula(chain, bonds, branches)
    fig = _draw_mol(chain, bonds, branches)
    img = save_fig(fig)
    k = rnd.randint(1, 3)
    if k == 1:
        return make(ORG, "La figura muestra la fórmula lineal (topológica) de un compuesto orgánico. ¿A qué función orgánica pertenece?",
                    func, rnd.sample([f for f in FUNCIONES if f != func], 5),
                    f"El compuesto es {name}; su estructura corresponde a la función {func.lower()}.", img)
    if k == 2:
        others = set()
        for dh in (2, -2, 4):
            if H + dh > 0:
                others.add(form.replace(f"H{str(H).translate(SUBN)}", f"H{str(H + dh).translate(SUBN)}", 1))
        others.add(form.replace(f"C{str(C).translate(SUBN)}", f"C{str(C + 1).translate(SUBN)}", 1))
        return make(ORG, "La figura muestra la fórmula lineal (topológica) de un compuesto orgánico. ¿Cuál es su fórmula molecular?",
                    form, [o for o in others if o != form],
                    f"Cada vértice y extremo sin letra es un carbono, y cada carbono completa 4 enlaces con H: {form} ({name}).", img)
    c, w = numeric_options(C, [C + 1, C - 1, len(chain) + len(branches)], step=1)
    return make(ORG, "La figura muestra la fórmula lineal (topológica) de un compuesto orgánico. ¿Cuántos átomos de carbono tiene?",
                c, w, f"En la fórmula topológica cada vértice o extremo sin letra es un carbono: {C} ({name}).", img)


PONDERAL = [("magnesio", "oxígeno", "óxido de magnesio", 3, 2), ("carbono", "oxígeno", "dióxido de carbono", 3, 8),
            ("hidrógeno", "oxígeno", "agua", 1, 8), ("calcio", "oxígeno", "óxido de calcio", 5, 2), ("hierro", "azufre", "sulfuro de hierro", 7, 4),
            ("cobre", "azufre", "sulfuro de cobre", 2, 1)]


def g_ponderal():
    A, B, P, ra, rb = rnd.choice(PONDERAL)
    ks = sorted(rnd.sample([1, 2, 3, 4, 5, 6, 8, 10], 3))
    base = rnd.choice([1, 2, 3])
    rows = [(ra * k * base, rb * k * base) for k in ks]
    k = rnd.randint(1, 3)
    data = [[f"Ensayo {i + 1}", fint(a), fint(b), fint(a + b)] for i, (a, b) in enumerate(rows)]
    if k == 1:
        i = rnd.randrange(3)
        data[i][3] = "?"
    elif k == 2:
        i = rnd.randrange(1, 3)
        data[i][2] = "?"
        data[i][3] = "—"
    fig, ax = plt.subplots(figsize=(6.2, 2.4))
    ax.axis("off")
    tbl = ax.table(cellText=data, colLabels=["", f"Masa de {A} (g)", f"Masa de {B} (g)", f"Masa de {P} (g)"], loc="center", cellLoc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(11)
    tbl.scale(1, 1.7)
    tbl.auto_set_column_width([0, 1, 2, 3])
    ax.set_title("Reacción completa, sin sobrantes", fontsize=11)
    img = save_fig(fig)
    if k == 1:
        a, b = rows[i]
        c, w = numeric_options(a + b, [abs(a - b), a * b if a * b != a + b else a + b + 3, max(a, b)], step=max(1, (a + b) // 5), fn=unit("g"))
        return make(EST, f"La tabla muestra ensayos en que el {A} reacciona completamente con el {B}. ¿Qué masa de {P} se forma en el ensayo {i + 1}?", c, w,
                    f"Ley de conservación de la masa: {a} g + {b} g = {a + b} g.", img)
    if k == 2:
        a, b = rows[i]
        c, w = numeric_options(b, [a, a * rb, b * 2], step=max(1, b // 4), fn=unit("g"))
        return make(EST, f"Según la ley de las proporciones definidas, ¿qué masa de {B} reacciona completamente con {a} g de {A} en el ensayo {i + 1}?", c, w,
                    f"La razón es siempre {A} : {B} = {ra} : {rb}; entonces {a}·{rb}/{ra} = {b} g.", img)
    return make(EST, "¿Qué ley ponderal se evidencia al comparar los tres ensayos de la tabla?",
                "La ley de las proporciones definidas", ["La ley de Ohm", "La ley de las proporciones múltiples", "La ley de Hooke"],
                f"En todos los ensayos la razón entre las masas de {A} y {B} es la misma ({ra} : {rb}).", img)


# ====================================================================== BIOLOGÍA
def g_photosynthesis():
    dists = [10, 20, 30, 40, 50]
    b0 = rnd.randint(30, 60)
    bubbles = [b0 - i * rnd.randint(5, 8) for i in range(5)]
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
        return make(AMB, "En el experimento del gráfico, ¿cuál es la variable independiente?", "La distancia de la lámpara (intensidad de luz)",
                    ["El número de burbujas de oxígeno", "El tipo de planta", "La cantidad de agua"],
                    "La variable independiente es la que el investigador modifica: la distancia de la lámpara.", img)
    if k == 2:
        return make(AMB, "En el experimento del gráfico, ¿cuál es la variable dependiente?", "El número de burbujas de O₂ por minuto",
                    ["La distancia de la lámpara", "El color de la lámpara", "La especie de planta"],
                    "La variable dependiente es la que se mide como resultado: las burbujas de O₂.", img)
    if k == 3:
        ans = "A menor distancia de la lámpara (más luz), mayor es la tasa de fotosíntesis"
        w = ["A mayor distancia de la lámpara, mayor es la tasa de fotosíntesis", "La luz no influye en la fotosíntesis",
             "La planta produce CO₂ en lugar de O₂", "La tasa de fotosíntesis es constante"]
        return make(AMB, "¿Qué conclusión es correcta según los resultados del gráfico?", ans, w,
                    "Las burbujas de O₂ disminuyen a medida que la lámpara se aleja.", img)
    i, j = sorted(rnd.sample(range(5), 2))
    d = bubbles[i] - bubbles[j]
    c, w = numeric_options(d, [bubbles[i], bubbles[j], bubbles[i] + bubbles[j]], step=2)
    return make(AMB, f"Según el gráfico, ¿cuántas burbujas por minuto más se producen a {dists[i]} cm que a {dists[j]} cm?", c, w,
                f"{bubbles[i]} − {bubbles[j]} = {d}.", img)


def g_luz_saturacion():
    sat = rnd.choice([400, 500, 600, 800])
    hi, lo = rnd.choice([(40, 20), (30, 15), (50, 25), (60, 30)])
    xs = np.linspace(0, 1200, 300)
    f_hi = np.minimum(xs / sat, 1) * hi
    f_lo = np.minimum(xs / (sat * lo / hi), 1) * lo
    fig, ax = plt.subplots(figsize=(5.8, 3.8))
    ax.plot(xs, f_hi, color="#2ca02c", lw=2, label="CO₂ alto (0,1%)")
    ax.plot(xs, f_lo, color="#9467bd", lw=2, ls="--", label="CO₂ bajo (0,03%)")
    ax.set_xlabel("Intensidad de luz (unidades)")
    ax.set_ylabel("O₂ liberado (mL/h)")
    ax.set_xticks(range(0, 1201, 200))
    ax.set_yticks(range(0, hi + 11, 10 if hi >= 40 else 5))
    grid(ax)
    ax.legend(loc="lower right")
    img = save_fig(fig)
    k = rnd.randint(1, 3)
    if k == 1:
        c, w = numeric_options(hi, [lo, hi // 2, hi + 10], step=5, fn=unit("mL/h"))
        return make(AMB, "Según el gráfico, ¿cuál es la máxima tasa de liberación de O₂ con CO₂ alto?", c, w,
                    f"La curva de CO₂ alto se estabiliza en {hi} mL/h.", img)
    if k == 2:
        ans = "La concentración de CO₂"
        return make(AMB, "Según el gráfico, sobre cierta intensidad de luz la curva de CO₂ bajo deja de subir. ¿Qué factor limita la fotosíntesis en esa zona?", ans,
                    ["La intensidad de la luz", "La cantidad de oxígeno del aire", "La cantidad de clorofila destruida por la luz"],
                    "Aunque haya más luz la tasa no sube; con más CO₂ (otra curva) sí sube: el CO₂ es el factor limitante.", img)
    c, w = numeric_options(sat, [sat // 2, 1200, sat + 200], step=100, fn=unit("unidades"))
    return make(AMB, "Según el gráfico, ¿desde qué intensidad de luz la tasa de fotosíntesis con CO₂ alto ya no aumenta?", c, w,
                f"La curva de CO₂ alto llega a su máximo en {sat} unidades de luz y luego se mantiene.", img)


def g_ciclo_ovarico():
    L = rnd.choice([28, 28, 30, 32])
    ov = L - 14
    d = np.linspace(1, L, 400)
    estr = 20 + 80 * np.exp(-((d - (ov - 1.5)) / 2.2) ** 2) + 30 * np.exp(-((d - (ov + 7)) / 3.5) ** 2)
    lh = 10 + 90 * np.exp(-((d - ov) / 0.9) ** 2)
    prog = 5 + 85 * np.exp(-((d - (ov + 7)) / 3.2) ** 2)
    fig, ax = plt.subplots(figsize=(6.4, 3.9))
    ax.axvspan(1, 5, color="#f4a6a6", alpha=0.45, label="Menstruación")
    ax.plot(d, estr, color="#1f77b4", lw=2, label="Estrógenos")
    ax.plot(d, lh, color="#ff7f0e", lw=2, label="LH")
    ax.plot(d, prog, color="#2ca02c", lw=2, label="Progesterona")
    ax.set_xlabel("Día del ciclo")
    ax.set_ylabel("Nivel hormonal (relativo)")
    ax.set_xticks(range(1, L + 1, 2 if L <= 28 else 3))
    ax.set_yticks([])
    ax.set_xlim(1, L)
    grid(ax)
    ax.legend(fontsize=9, loc="upper left")
    ax.set_title(f"Ciclo de {L} días")
    img = save_fig(fig)
    k = rnd.randint(1, 4)
    if k == 1:
        c, w = numeric_options(ov, [ov - 7, ov + 7, 1], step=3, fn=lambda v: f"Día {fmt(v)}")
        return make(PROC, "El gráfico muestra hormonas de un ciclo sexual femenino. La ovulación ocurre poco después del máximo de LH. ¿Qué día ocurre aproximadamente la ovulación?", c, w,
                    f"El pico de LH se observa cerca del día {ov}, que marca la ovulación.", img)
    if k == 2:
        return make(PROC, f"Según el gráfico, ¿qué hormona alcanza su nivel más alto en la fase lútea (días {ov + 1} a {L})?", "Progesterona",
                    ["LH", "Estrógenos", "Ninguna, todas se mantienen iguales"],
                    "En la fase lútea el cuerpo lúteo secreta mucha progesterona, que prepara el endometrio.", img)
    if k == 3:
        return make(PROC, f"Según el gráfico, ¿en qué fase del ciclo ovárico se encuentran los días 6 a {ov - 1}?", "Fase folicular",
                    ["Fase lútea", "Ovulación", "Embarazo"],
                    "Antes de la ovulación madura un folículo que secreta estrógenos: es la fase folicular.", img)
    return make(PROC, "Según el gráfico, ¿qué ocurre con la progesterona al final del ciclo y qué consecuencia tiene?",
                "Disminuye, y el endometrio se desprende en la menstruación siguiente",
                ["Aumenta, y comienza la ovulación", "Se mantiene alta, y el endometrio sigue creciendo",
                 "Disminuye, y se forma un nuevo cuerpo lúteo de inmediato"],
                "Si no hay fecundación el cuerpo lúteo degenera, baja la progesterona y el endometrio se desprende.", img)


def g_adn_ciclo():
    q = rnd.choice([2, 4, 6, 8, 10])
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    t = [0, 4, 7, 10, 12, 12.001, 16]
    y = [q, q, 2 * q, 2 * q, 2 * q, q, q]
    ax.plot(t, y, color="#d62728", lw=2.5)
    marks = [(0, 4, "I"), (4, 7, "II"), (7, 10, "III"), (10, 12, "IV"), (12, 16, "V")]
    for a, b, lab in marks:
        ax.axvline(a, color="gray", lw=0.8, ls=":")
        ax.text((a + b) / 2, 2 * q * 1.12, lab, ha="center", fontsize=13, color="#1f4e9c")
    ax.set_ylim(0, 2 * q * 1.25)
    ax.set_yticks([q, 2 * q])
    ax.set_yticklabels([f"{q} pg", f"{2 * q} pg"])
    ax.set_xticks([])
    ax.set_xlabel("Tiempo")
    ax.set_ylabel("ADN por célula")
    ax.set_title("Cantidad de ADN durante un ciclo celular")
    img = save_fig(fig)
    k = rnd.randint(1, 3)
    opts = ["I", "II", "III", "IV", "V"]
    if k == 1:
        return make(HER, "En el gráfico, ¿en qué etapa ocurre la replicación del ADN (fase S)?", "II", [o for o in opts if o != "II"],
                    "En la etapa II la cantidad de ADN se duplica: es la fase S de la interfase.", img)
    if k == 2:
        return make(HER, "En el gráfico, ¿qué etapa corresponde a la fase G1, antes de la replicación?", "I", [o for o in opts if o != "I"],
                    "En G1 la célula tiene la cantidad inicial de ADN y aún no lo replica.", img)
    return make(HER, "En el gráfico, ¿qué ocurre al pasar de la etapa IV a la V?",
                "Termina la división: el ADN se reparte entre dos células hijas", ["Se replica el ADN", "La célula muere",
                                                                                   "Ocurre la fecundación", "Se duplican los cromosomas"],
                f"La cantidad baja de {2 * q} pg a {q} pg por célula porque el ADN duplicado se reparte en dos células.", img)


def g_tabla_mitosis():
    n_int = rnd.choice([70, 75, 80, 85, 88])
    resto = 100 - n_int
    pro = rnd.randint(resto // 3, resto // 2)
    meta = rnd.randint(1, (resto - pro) // 2)
    ana = rnd.randint(1, resto - pro - meta - 1)
    telo = resto - pro - meta - ana
    if min(pro, meta, ana, telo) < 1 or len({pro, meta, ana, telo}) < 4:
        raise Skip()
    filas = [("Interfase", n_int), ("Profase", pro), ("Metafase", meta), ("Anafase", ana), ("Telofase", telo)]
    fig, ax = plt.subplots(figsize=(4.8, 2.8))
    ax.axis("off")
    tbl = ax.table(cellText=[[e, str(n)] for e, n in filas], colLabels=["Etapa", "N.º de células"], loc="center", cellLoc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(12)
    tbl.scale(1, 1.6)
    tbl.auto_set_column_width([0, 1])
    ax.set_title("Células de punta de raíz de cebolla (100 contadas)", fontsize=11)
    img = save_fig(fig)
    k = rnd.randint(1, 3)
    if k == 1:
        c, w = numeric_options(resto, [n_int, pro, 100], step=2, fn=lambda v: f"{fmt(v)}%")
        return make(HER, "Según la tabla, ¿qué porcentaje de las células observadas se encontraba en mitosis?", c, w,
                    f"Se suman profase, metafase, anafase y telofase: {pro} + {meta} + {ana} + {telo} = {resto} de 100 = {resto}%.", img)
    if k == 2:
        return make(HER, "Si la cantidad de células en cada etapa es proporcional a su duración, ¿cuál es la etapa más larga del ciclo celular?",
                    "Interfase", ["Profase", "Metafase", "Anafase", "Telofase"],
                    f"La mayoría de las células ({n_int} de 100) estaba en interfase.", img)
    mx = max(filas[1:], key=lambda f: f[1])[0]
    return make(HER, "Según la tabla, ¿cuál es la etapa más larga de la mitosis?", mx, [e for e, _ in filas[1:] if e != mx] + ["Interfase"],
                f"Entre las etapas de la mitosis, la que tiene más células es {mx.lower()}.", img)


def g_seleccion():
    gens = list(range(0, 11))
    g0 = rnd.choice([2, 3, 4])
    p0 = rnd.choice([2, 5, 10])
    vals = []
    for g in gens:
        if g < g0:
            vals.append(p0)
        else:
            vals.append(min(95, p0 + (95 - p0) * (1 - np.exp(-(g - g0) / 1.8))))
    fig, ax = plt.subplots(figsize=(5.8, 3.8))
    ax.plot(gens, vals, color="#8c564b", lw=2, marker="o", ms=4)
    ax.axvline(g0, color="#d62728", ls="--", lw=1.2)
    ax.text(g0 - 0.15, 60, "Se empieza a\nusar el antibiótico", color="#d62728", fontsize=9, ha="right")
    ax.set_xlabel("Generación")
    ax.set_ylabel("Bacterias resistentes (%)")
    ax.set_xticks(gens)
    ax.set_ylim(0, 100)
    grid(ax)
    img = save_fig(fig)
    if rnd.random() < 0.5:
        ans = "El antibiótico eliminó a las bacterias sensibles y las resistentes sobrevivieron y se reprodujeron"
        w = ["El antibiótico transformó a las bacterias sensibles en resistentes", "Las bacterias decidieron volverse resistentes",
             "La resistencia apareció por el uso y desuso de órganos", "Las bacterias resistentes dejaron de reproducirse"]
        return make(HER, "El gráfico muestra el porcentaje de bacterias resistentes en una población. ¿Cómo explica la selección natural el cambio observado?", ans, w,
                    f"Antes del antibiótico ya había un {p0}% de resistentes: la variación existía y el antibiótico la seleccionó.", img)
    c, w = numeric_options(p0, [0, 50, 95], step=1, fn=lambda v: f"{fmt(v)}%")
    return make(HER, "Según el gráfico, ¿qué porcentaje de bacterias resistentes había antes de usar el antibiótico?", c, w,
                f"Antes de la generación {g0} el porcentaje se mantiene en {p0}%: la resistencia ya existía en la población.", img)


GRAPH_PLAN = [(g_xt, 7), (g_vt, 7), (g_onda_em, 5), (g_circuito, 8), (g_consumo, 6),
              (g_solubility, 10), (g_density, 5), (g_organica, 10), (g_ponderal, 8),
              (g_photosynthesis, 8), (g_luz_saturacion, 6), (g_ciclo_ovarico, 8), (g_adn_ciclo, 5), (g_tabla_mitosis, 4), (g_seleccion, 3)]
