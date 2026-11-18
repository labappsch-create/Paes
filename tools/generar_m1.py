#!/usr/bin/env python3
"""Genera las 500 preguntas originales de Matemática M1 (400 de texto + 100 con gráfico).

Cada respuesta correcta se CALCULA con el programa (no se escribe a mano) y cada
gráfico se dibuja con los mismos datos de la pregunta, así coinciden siempre.
No usa contenido del DEMRE.

Uso (desde la carpeta del proyecto):
    PYTHONPATH=<carpeta con matplotlib> python3 tools/generar_m1.py
Escribe: assets/questions/m1.json y assets/images/m1/*.png
"""
import json
import math
import os
import random
import sys
from fractions import Fraction

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Polygon, Circle, Wedge  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(ROOT, "assets", "images", "m1")
OUT_JSON = os.path.join(ROOT, "assets", "questions", "m1.json")
N_TEXT = 400
N_GRAPH = 100

rnd = random.Random(20261117)
plt.rcParams.update(
    {"font.size": 11, "axes.spines.top": False, "axes.spines.right": False}
)

NUMEROS = "Números"
ALGEBRA = "Álgebra y funciones"
GEOMETRIA = "Geometría"
PROBA = "Probabilidad y estadística"
MINUS = "\u2212"
NOMBRES = ["Camila", "Matías", "Valentina", "Benjamín", "Sofía", "Joaquín",
           "Antonia", "Vicente", "Isidora", "Tomás", "Fernanda", "Diego",
           "Javiera", "Sebastián", "Catalina", "Ignacio", "Martina", "Felipe"]


class Skip(Exception):
    """La plantilla no pudo armar una pregunta válida; se vuelve a intentar."""


# ----------------------------------------------------------------- formato
def fint(n):
    return f"{int(n):,}".replace(",", ".").replace("-", MINUS)


def fmt(x):
    if isinstance(x, Fraction):
        x = float(x) if x.denominator != 1 else int(x)
    if isinstance(x, float) and x == int(x):
        x = int(x)
    if isinstance(x, int):
        return fint(x)
    s = f"{x:.2f}".rstrip("0").rstrip(".").replace(".", ",")
    return s.replace("-", MINUS)


def money(n):
    return "$" + fint(n)


def sgn_pct(v):
    if v == 0:
        return "0%"
    return ("+" if v > 0 else MINUS) + fmt(abs(v)) + "%"


def frac_str(f):
    f = Fraction(f)
    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"


SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def sup(n):
    return str(n).translate(SUP)


def lin(a, b):
    """'3x + 5' o '3x − 5'."""
    return f"{a}x {'+' if b >= 0 else MINUS} {abs(b)}"


def line_str(m, b):
    mpart = "x" if m == 1 else (MINUS + "x" if m == -1 else f"{fint(m)}x")
    if b == 0:
        return f"y = {mpart}"
    return f"y = {mpart} {'+' if b > 0 else MINUS} {abs(b)}"


def pt(x, y):
    return f"({fint(x)}, {fint(y)})"


# ------------------------------------------------------------ construcción
def numeric_options(correct, cands, step=1, positive=True, fn=fmt):
    """Devuelve (texto_correcto, [3+ distractores]) con valores numéricos."""
    seen = {fn(correct)}
    wrongs = []
    pool = list(cands)
    for k in range(1, 12):
        pool += [correct + step * k, correct - step * k]
    for v in pool:
        if positive and v <= 0:
            continue
        s = fn(v)
        if s in seen:
            continue
        seen.add(s)
        wrongs.append(s)
    return fn(correct), wrongs


def make(eje, enunciado, correct, wrongs, explicacion, imagen=None):
    opts = [correct]
    for w in wrongs:
        if w not in opts:
            opts.append(w)
        if len(opts) == 4:
            break
    if len(opts) < 4:
        raise Skip()
    rnd.shuffle(opts)
    q = {
        "prueba": "m1",
        "eje": eje,
        "enunciado": enunciado,
        "alternativas": opts,
        "correcta": opts.index(correct),
        "explicacion": explicacion,
    }
    if imagen:
        q["imagen"] = imagen
    return q


def nm():
    return rnd.choice(NOMBRES)


# ===================================================== PLANTILLAS: NÚMEROS
def t_percent_of():
    pct = rnd.choice([5, 10, 12, 15, 20, 25, 30, 35, 40, 45, 60, 75, 80, 90])
    while True:
        y = rnd.randrange(40, 1500, 10)
        if (pct * y) % 100 == 0:
            break
    v = pct * y // 100
    enun = rnd.choice([
        f"En una tienda hay {fint(y)} productos y el {pct}% está en oferta. ¿Cuántos productos están en oferta?",
        f"¿Cuál es el {pct}% de {fint(y)}?",
        f"Un curso de {fint(y)} personas participa en una encuesta y el {pct}% responde que sí. ¿Cuántas personas responden que sí?",
    ])
    c, w = numeric_options(v, [y - v, pct * y // 10, v * 2], step=max(1, v // 10))
    return make(NUMEROS, enun, c, w, f"{pct}% de {fint(y)} = {pct}/100 · {fint(y)} = {fint(v)}.")


def t_inc_dec():
    a = rnd.choice([10, 20, 25, 30, 40, 50])
    b = rnd.choice([10, 15, 20, 25, 50])
    net = Fraction((100 + a) * (100 - b), 100) - 100
    if net == 0 or (net * 10).denominator != 1:
        raise Skip()
    v = float(net)
    enun = rnd.choice([
        f"Un producto aumenta su precio en {a}% y luego baja {b}%. Respecto al precio original, el precio final varió en:",
        f"El valor de un artículo sube {a}% y después se rebaja {b}%. En comparación con el valor inicial, el valor final es:",
    ])
    c = sgn_pct(v)
    w = [sgn_pct(a - b), sgn_pct(-(a - b)), sgn_pct(a + b), sgn_pct(v + 5), sgn_pct(v - 3), "0%"]
    return make(NUMEROS, enun, c, w,
                f"Factor final: {fmt(1 + a / 100)} × {fmt(1 - b / 100)} = {fmt((100 + a) * (100 - b) / 10000)}, es decir {sgn_pct(v)}.")


def t_discount():
    P = rnd.randrange(10000, 95000, 1000)
    d = rnd.choice([10, 15, 20, 25, 30, 40, 50])
    final = P * (100 - d) // 100
    n = nm()
    enun = f"{n} compra un artículo que cuesta {money(P)} y tiene un {d}% de descuento. ¿Cuánto paga?"
    c, w = numeric_options(final, [P - d, P * d // 100, P * (100 + d) // 100], step=1000, fn=money)
    return make(NUMEROS, enun, c, w, f"Paga el {100 - d}% del precio: {money(P)} · {(100 - d)}/100 = {money(final)}.")


def t_fraction_add():
    dens = [2, 3, 4, 5, 6, 8, 10, 12]
    b, d = rnd.choice(dens), rnd.choice(dens)
    if b == d:
        raise Skip()
    a, c = rnd.randrange(1, b), rnd.randrange(1, d)
    res = Fraction(a, b) + Fraction(c, d)
    op = rnd.choice(["+", MINUS])
    if op == MINUS:
        res = Fraction(a, b) - Fraction(c, d)
        if res <= 0:
            raise Skip()
    cands = [Fraction(a + c, b + d), Fraction(a * c, b * d), Fraction(a + c, b * d), Fraction(a, b) + Fraction(c, d) if op == MINUS else Fraction(a, b) - Fraction(c, d)]
    wrongs = [frac_str(x) for x in cands if x > 0 and x != res]
    wrongs += [frac_str(res + Fraction(1, 12)), frac_str(res + Fraction(1, 6)), frac_str(res * 2)]
    return make(NUMEROS, f"¿Cuál es el resultado de {a}/{b} {op} {c}/{d}?", frac_str(res), wrongs,
                f"Se busca un denominador común y se opera: el resultado es {frac_str(res)}.")


def t_direct_prop():
    kilo = rnd.choice([400, 600, 800, 1200, 1500, 1800, 2500])
    n, m = rnd.choice([(2, 7), (3, 8), (4, 9), (5, 12), (6, 11), (2, 9), (4, 15)])
    total_n, total_m = kilo * n, kilo * m
    prod = rnd.choice(["manzanas", "naranjas", "tomates", "paltas", "papas"])
    enun = f"Si {n} kg de {prod} cuestan {money(total_n)}, ¿cuánto cuestan {m} kg de {prod}?"
    c, w = numeric_options(total_m, [total_n + m * 100, kilo * (m + n), total_n * m // n + 500], step=kilo, fn=money)
    return make(NUMEROS, enun, c, w, f"1 kg cuesta {money(kilo)}; entonces {m} kg cuestan {money(total_m)}.")


def t_inverse_prop():
    w1, d1 = rnd.choice([(6, 12), (8, 15), (4, 30), (5, 24), (10, 18), (12, 10), (9, 20)])
    total = w1 * d1
    cands = [x for x in range(2, 31) if x != w1 and total % x == 0]
    if not cands:
        raise Skip()
    w2 = rnd.choice(cands)
    d2 = total // w2
    enun = f"{w1} obreros construyen un muro en {d1} días trabajando al mismo ritmo. ¿En cuántos días lo construirían {w2} obreros?"
    c, w = numeric_options(d2, [d1 + (w2 - w1), d1 * w2 // w1 if w1 else 1, d1 - (w2 - w1)], step=2)
    return make(NUMEROS, enun, c, w, f"Es proporcionalidad inversa: {w1}·{d1} = {w2}·x, entonces x = {d2}.")


def t_power():
    base = rnd.choice([2, 3, 5, 10])
    a, b = rnd.randint(2, 7), rnd.randint(2, 7)
    c_ = rnd.randint(1, a + b - 1)
    k = a + b - c_
    enun = f"¿Cuál es el valor de ({base}{sup(a)} · {base}{sup(b)}) : {base}{sup(c_)}?"
    cands = [a * b - c_, a + b + c_, k + 1, k - 1, a * b, a + b]
    ws = []
    for e in cands:
        if e != k:
            s = f"{base}{sup(e)}"
            if s not in ws:
                ws.append(s)
    return make(NUMEROS, enun, f"{base}{sup(k)}", ws,
                f"Se suman los exponentes al multiplicar y se restan al dividir: {a}+{b}−{c_} = {k}.")


def t_mean_add():
    n = rnd.choice([4, 5, 6, 8])
    m = rnd.randint(10, 30)
    d2 = rnd.randint(1, 4)
    x = m + (n + 1) * d2
    enun = f"El promedio de {n} números es {m}. Si se agrega un número más, el promedio sube a {m + d2}. ¿Qué número se agregó?"
    c, w = numeric_options(x, [m + d2, m * 2, (n + 1) * d2], step=2)
    return make(NUMEROS, enun, c, w, f"Suma inicial {n * m}; suma final {(n + 1) * (m + d2)}; el número agregado es la diferencia: {x}.")


def t_simple_interest():
    C = rnd.randrange(200000, 2000001, 100000)
    r = rnd.choice([2, 3, 4, 5, 6])
    t = rnd.randint(2, 5)
    I = C * r * t // 100
    enun = f"Se depositan {money(C)} con un interés simple de {r}% anual durante {t} años. ¿Cuánto interés se obtiene en total?"
    c, w = numeric_options(I, [C * r // 100, C + I, C * r * t, I + C * r // 100 // 2], step=C // 100, fn=money)
    return make(NUMEROS, enun, c, w, f"Interés = capital · tasa · tiempo = {money(C)} · {r}/100 · {t} = {money(I)}.")


def t_ratio_share():
    a, b = rnd.choice([(1, 2), (2, 3), (3, 4), (2, 5), (3, 5), (1, 4), (3, 7)])
    k = rnd.randint(4, 30)
    T = (a + b) * k * 100
    big = b * k * 100
    n1, n2 = rnd.sample(NOMBRES, 2)
    enun = f"{n1} y {n2} reparten {money(T)} en la razón {a}:{b}. ¿Cuánto recibe quien recibe más?"
    c, w = numeric_options(big, [a * k * 100, T // 2, T - a * 100], step=k * 100, fn=money)
    return make(NUMEROS, enun, c, w, f"Cada parte vale {money(T)}/{a + b} = {money(k * 100)}. El mayor recibe {b} partes: {money(big)}.")


def t_order_ops():
    form = rnd.randint(1, 3)
    if form == 1:
        a, b, c_, d = rnd.randint(2, 15), rnd.randint(2, 9), rnd.randint(2, 9), rnd.randint(1, 12)
        val = a + b * c_ - d
        wrong = (a + b) * c_ - d
        text = f"{a} + {b} × {c_} {MINUS} {d}"
    elif form == 2:
        a, b, c_, d = rnd.randint(2, 9), rnd.randint(2, 9), rnd.randint(2, 9), rnd.randint(1, 12)
        val = (a + b) * c_ - d
        wrong = a + b * c_ - d
        text = f"({a} + {b}) × {c_} {MINUS} {d}"
    else:
        d = rnd.randint(2, 6)
        c_ = d * rnd.randint(2, 8)
        a, b = rnd.randint(2, 9), rnd.randint(2, 9)
        val = a * b - c_ // d
        wrong = (a * b - c_) // d if (a * b - c_) % d == 0 else a * b - c_ * d
        text = f"{a} × {b} {MINUS} {c_} ÷ {d}"
    c, w = numeric_options(val, [wrong], step=1, positive=False)
    return make(NUMEROS, f"¿Cuál es el valor de {text}?", c, w,
                "Primero se resuelven los paréntesis, luego × y ÷, y al final + y −.")


def t_neg_ops():
    a, b, c_ = rnd.randint(2, 9), rnd.randint(2, 9), rnd.randint(1, 20)
    form = rnd.randint(1, 2)
    if form == 1:
        val = (-a) * b + c_
        text = f"({MINUS}{a}) × {b} + {c_}"
        wrong = a * b + c_
    else:
        val = -a - (-b) * c_
        text = f"{MINUS}{a} {MINUS} ({MINUS}{b}) × {c_}"
        wrong = -a - b * c_
    c, w = numeric_options(val, [wrong, -val], step=1, positive=False)
    return make(NUMEROS, f"¿Cuál es el resultado de {text}?", c, w,
                "Se aplican las reglas de los signos: menos por menos es más; más por menos es menos.")


def t_percent_what():
    pct = rnd.choice([10, 20, 25, 40, 50, 60, 75, 80])
    b = rnd.randrange(40, 400, 20)
    a = pct * b // 100
    if (pct * b) % 100:
        raise Skip()
    n = nm()
    enun = f"{n} resolvió correctamente {a} de {b} ejercicios. ¿Qué porcentaje de los ejercicios resolvió correctamente?"
    cs, ws = numeric_options(pct, [100 - pct, a, 100 * b // a if a else 1], step=5, fn=lambda v: f"{fmt(v)}%")
    return make(NUMEROS, enun, cs, ws, f"{a}/{b} = {pct}/100, es decir {pct}%.")


def t_speed():
    v = rnd.choice([40, 45, 50, 60, 72, 80, 90])
    t = rnd.choice([2, 3, 4, 5])
    D = v * t
    enun = f"Un bus recorre {D} km en {t} horas a velocidad constante. ¿Cuál es su velocidad en km/h?"
    c, w = numeric_options(v, [D + t, D - t, D * t, t], step=5)
    return make(NUMEROS, enun, c, w, f"Velocidad = distancia / tiempo = {D}/{t} = {v} km/h.")


# =================================================== PLANTILLAS: ÁLGEBRA
def t_linear_eq():
    x = rnd.randint(-9, 15)
    a = rnd.randint(2, 9)
    b = rnd.randint(-15, 20)
    cc = a * x + b
    c, w = numeric_options(x, [(cc + b) // a if a else 0, cc - b, cc + b], step=1, positive=False)
    return make(ALGEBRA, f"¿Cuál es el valor de x en la ecuación {lin(a, b)} = {fint(cc)}?", c, w,
                f"{a}x = {fint(cc)} {'−' if b >= 0 else '+'} {abs(b)} = {fint(cc - b)}, entonces x = {fint(x)}.")


def t_eval_fn():
    if rnd.random() < 0.5:
        a, b, k = rnd.randint(2, 7), rnd.randint(-9, 12), rnd.randint(-5, 8)
        val = a * k + b
        txt = f"f(x) = {lin(a, b)}"
        wrong = [a + b + k, a * (k + b), -val]
    else:
        a, b, k = rnd.randint(1, 6), rnd.randint(-8, 10), rnd.randint(-4, 6)
        val = k * k - a * k + b
        txt = f"f(x) = x² {MINUS} {a}x {'+' if b >= 0 else MINUS} {abs(b)}"
        wrong = [k * k + a * k + b, (k - a) ** 2 + b, -val]
    c, w = numeric_options(val, wrong, step=2, positive=False)
    return make(ALGEBRA, f"Si {txt}, ¿cuál es el valor de f({fint(k)})?", c, w, f"Se reemplaza x por {fint(k)}: f({fint(k)}) = {fint(val)}.")


def t_slope():
    m = rnd.choice([-4, -3, -2, -1, 1, 2, 3, 4, 5])
    x1, y1 = rnd.randint(-5, 5), rnd.randint(-5, 5)
    dx = rnd.randint(1, 5)
    x2, y2 = x1 + dx, y1 + m * dx
    c, w = numeric_options(m, [-m, dx, m * dx, Fraction(1, m) if m else 0], step=1, positive=False)
    return make(ALGEBRA, f"¿Cuál es la pendiente de la recta que pasa por los puntos {pt(x1, y1)} y {pt(x2, y2)}?", c, w,
                f"m = (y₂ − y₁)/(x₂ − x₁) = {fint(y2 - y1)}/{fint(dx)} = {fint(m)}.")


def t_system():
    x = rnd.randint(2, 15)
    y = rnd.randint(1, x - 1) if x > 1 else 1
    S, D = x + y, x - y
    ask = rnd.choice(["x", "y"])
    val = x if ask == "x" else y
    enun = f"Si x + y = {S} y x {MINUS} y = {D}, ¿cuál es el valor de {ask}?"
    c, w = numeric_options(val, [S, D, S - val], step=1)
    return make(ALGEBRA, enun, c, w, f"Sumando las ecuaciones: 2x = {S + D}, x = {x}; luego y = {S} {MINUS} {x} = {y}.")


def t_binomial():
    a = rnd.randint(2, 9)
    kind = rnd.randint(1, 3)
    if kind == 1:
        q, c = f"(x + {a})²", f"x² + {2 * a}x + {a * a}"
        w = [f"x² + {a * a}", f"x² + {a}x + {a * a}", f"x² + {2 * a}x + {2 * a}", f"x² {MINUS} {2 * a}x + {a * a}"]
        ex = f"(x + {a})² = x² + 2·{a}·x + {a}²."
    elif kind == 2:
        q, c = f"(x {MINUS} {a})²", f"x² {MINUS} {2 * a}x + {a * a}"
        w = [f"x² {MINUS} {a * a}", f"x² + {2 * a}x + {a * a}", f"x² {MINUS} {a}x + {a * a}", f"x² {MINUS} {2 * a}x {MINUS} {a * a}"]
        ex = f"(x {MINUS} {a})² = x² {MINUS} 2·{a}·x + {a}²."
    else:
        q, c = f"(x + {a})(x {MINUS} {a})", f"x² {MINUS} {a * a}"
        w = [f"x² + {a * a}", f"x² {MINUS} {2 * a}x", f"x² {MINUS} {a}", f"x² + {2 * a}x {MINUS} {a * a}"]
        ex = f"Es suma por diferencia: x² {MINUS} {a}² = x² {MINUS} {a * a}."
    return make(ALGEBRA, f"¿Cuál es el desarrollo de {q}?", c, w, ex)


def t_factor():
    if rnd.random() < 0.5:
        k = rnd.randint(2, 12)
        c = f"(x {MINUS} {k})(x + {k})"
        w = [f"(x {MINUS} {k})²", f"(x + {k})²", f"(x {MINUS} {2 * k})(x + {2 * k})", f"(x {MINUS} {k * k})(x + {k * k})"]
        return make(ALGEBRA, f"¿Cuál es la factorización de x² {MINUS} {k * k}?", c, w, f"Es una diferencia de cuadrados: x² {MINUS} {k}² = (x {MINUS} {k})(x + {k}).")
    p, q = rnd.randint(1, 9), rnd.randint(1, 9)
    if p == q:
        raise Skip()
    c = f"(x + {p})(x + {q})"
    w = [f"(x + {p + q})(x + 1)", f"(x {MINUS} {p})(x {MINUS} {q})", f"(x + {p * q})(x + 1)", f"(x + {p})(x {MINUS} {q})"]
    return make(ALGEBRA, f"¿Cuál es la factorización de x² + {p + q}x + {p * q}?", c, w, f"Se buscan dos números que sumen {p + q} y multipliquen {p * q}: {p} y {q}.")


def t_inequality():
    a = rnd.randint(2, 7)
    b = rnd.randint(-8, 12)
    cc = rnd.randint(15, 60)
    bound = cc - b
    best = (bound - 1) // a
    wrong = [bound // a, best + 1, best - 1, bound // a + 1]
    c, w = numeric_options(best, wrong, step=1, positive=False)
    return make(ALGEBRA, f"¿Cuál es el mayor número entero x que cumple {lin(a, b)} < {cc}?", c, w,
                f"{a}x < {fint(bound)}, entonces x < {fmt(Fraction(bound, a))}. El mayor entero es {fint(best)}.")


def t_age():
    k = rnd.randint(2, 5)
    L = rnd.randint(4, 18)
    S = (k + 1) * L
    a, b = rnd.sample(NOMBRES, 2)
    word = {2: "el doble", 3: "el triple", 4: "el cuádruple", 5: "cinco veces"}[k]
    enun = f"{a} tiene {word} de la edad de {b}. Juntos suman {S} años. ¿Qué edad tiene {b}?"
    c, w = numeric_options(L, [k * L, S // 2, S - k], step=1)
    return make(ALGEBRA, enun, c, w, f"x + {k}x = {S}, entonces {k + 1}x = {S} y x = {L}.")


def t_prop_fn():
    k = rnd.randint(2, 9)
    x1, x2 = rnd.randint(2, 8), rnd.randint(9, 20)
    y1, y2 = k * x1, k * x2
    c, w = numeric_options(y2, [y1 + (x2 - x1), x2 + k, y1 * 2], step=k)
    return make(ALGEBRA, f"y es directamente proporcional a x. Si y = {y1} cuando x = {x1}, ¿cuánto vale y cuando x = {x2}?", c, w,
                f"La constante es y/x = {k}; entonces y = {k}·{x2} = {y2}.")


def t_line_eq():
    m = rnd.choice([-4, -3, -2, -1, 1, 2, 3, 4, 5])
    b = rnd.choice([x for x in range(-8, 9) if x not in (0, m, -m)])
    c = line_str(m, b)
    w = [line_str(b, m), line_str(m, -b), line_str(-m, b), line_str(-m, -b)]
    return make(ALGEBRA, f"¿Cuál es la ecuación de la recta que tiene pendiente {fint(m)} y corta al eje y en el punto (0, {fint(b)})?", c, w,
                "Forma y = mx + n, con m la pendiente y n el valor donde corta al eje y.")


def t_perimeter_alg():
    x, a = rnd.randint(3, 20), rnd.randint(1, 9)
    P = 4 * x + 2 * a
    c, w = numeric_options(x, [x + a, (P - a) // 4, P // 4, P // 2 - a], step=1)
    return make(ALGEBRA, f"Un rectángulo tiene ancho x cm y largo (x + {a}) cm. Si su perímetro es {P} cm, ¿cuánto mide el ancho?", c, w,
                f"2·(x + x + {a}) = {P}, entonces 4x + {2 * a} = {P} y x = {x}.")


# ================================================ PLANTILLAS: GEOMETRÍA
TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41)]


def t_rect():
    l, w_ = rnd.randint(5, 20), rnd.randint(2, 12)
    if l == w_:
        raise Skip()
    P = 2 * (l + w_)
    c, w = numeric_options(l * w_, [P * l // 2, l + w_, P, 2 * (l * w_)], step=l)
    return make(GEOMETRIA, f"Un rectángulo tiene perímetro {P} cm y uno de sus lados mide {l} cm. ¿Cuál es su área?", c, w,
                f"El otro lado mide {P // 2} {MINUS} {l} = {w_} cm. Área = {l}·{w_} = {l * w_} cm².")


def t_pyth():
    a, b, h = rnd.choice(TRIPLES)
    k = rnd.randint(1, 4) if h < 20 else 1
    a, b, h = a * k, b * k, h * k
    if rnd.random() < 0.5:
        enun = f"Una escalera de {h} m apoyada en una pared llega a una altura de {a} m. ¿A qué distancia de la pared está la base de la escalera?"
        c, w = numeric_options(b, [a + h, h - a, a * 2], step=1)
        ex = f"{b}² = {h}² {MINUS} {a}² → {b} m."
    else:
        enun = f"Un triángulo rectángulo tiene catetos de {a} cm y {b} cm. ¿Cuánto mide su hipotenusa?"
        c, w = numeric_options(h, [a + b, b - a, a * b // 2], step=1)
        ex = f"h² = {a}² + {b}² = {a * a + b * b}, entonces h = {h} cm."
    return make(GEOMETRIA, enun, c, w, ex)


def t_circle():
    r = rnd.randint(2, 15)
    if rnd.random() < 0.5:
        c, w = f"{2 * r}π cm", [f"{r * r}π cm", f"{r}π cm", f"{4 * r}π cm", f"{2 * r * r}π cm"]
        return make(GEOMETRIA, f"Una circunferencia tiene radio {r} cm. ¿Cuál es su perímetro?", c, w, f"P = 2πr = 2π·{r} = {2 * r}π cm.")
    c, w = f"{r * r}π cm²", [f"{2 * r}π cm²", f"{r}π cm²", f"{2 * r * r}π cm²", f"{4 * r * r}π cm²"]
    return make(GEOMETRIA, f"Un círculo tiene radio {r} cm. ¿Cuál es su área?", c, w, f"A = πr² = π·{r}² = {r * r}π cm².")


def t_volume():
    kind = rnd.randint(1, 3)
    if kind == 1:
        a = rnd.randint(2, 12)
        c, w = numeric_options(a ** 3, [a * a, 3 * a, 6 * a * a], step=a, fn=lambda v: f"{fint(v)} cm³")
        return make(GEOMETRIA, f"Un cubo tiene arista de {a} cm. ¿Cuál es su volumen?", c, w, f"V = a³ = {a}³ = {a ** 3} cm³.")
    if kind == 2:
        a, b, h = rnd.randint(2, 12), rnd.randint(2, 10), rnd.randint(2, 9)
        if len({a, b, h}) < 3:
            raise Skip()
        c, w = numeric_options(a * b * h, [a + b + h, 2 * (a * b + b * h + a * h), a * b], step=a, fn=lambda v: f"{fint(v)} cm³")
        return make(GEOMETRIA, f"Una caja con forma de prisma rectangular mide {a} cm de largo, {b} cm de ancho y {h} cm de alto. ¿Cuál es su volumen?", c, w, f"V = {a}·{b}·{h} = {a * b * h} cm³.")
    r, h = rnd.randint(2, 8), rnd.randint(2, 12)
    c, w = f"{r * r * h}π cm³", [f"{2 * r * h}π cm³", f"{r * h}π cm³", f"{r * r}π cm³", f"{r * r * h * 2}π cm³"]
    return make(GEOMETRIA, f"Un cilindro tiene radio {r} cm y altura {h} cm. ¿Cuál es su volumen?", c, w, f"V = πr²h = π·{r * r}·{h} = {r * r * h}π cm³.")


def t_thales():
    h = rnd.choice([2, 3, 4, 5, 6])
    s = rnd.choice([1, 2, 3, 4])
    mult = rnd.randint(2, 9)
    S = s * mult
    H = h * mult
    if S == s or h == s:
        raise Skip()
    enun = f"Un poste de {h} m proyecta una sombra de {s} m. En el mismo instante, un árbol proyecta una sombra de {S} m. ¿Cuál es la altura del árbol?"
    c, w = numeric_options(H, [h + S - s, h * S, S + h], step=1, fn=lambda v: f"{fint(v)} m")
    return make(GEOMETRIA, enun, c, w, f"Por semejanza: {h}/{s} = x/{S}, entonces x = {H} m.")


def t_scale():
    n = rnd.choice([25000, 50000, 100000, 200000, 250000, 500000])
    d = rnd.randint(2, 30)
    if (d * n) % 50000:
        raise Skip()
    km = Fraction(d * n, 100000)
    c, w = numeric_options(km, [d * n // 1000, d * n // 10000, d * 2], step=Fraction(1, 2), fn=lambda v: f"{fmt(v)} km")
    return make(GEOMETRIA, f"En un mapa con escala 1:{fint(n)}, dos ciudades están separadas por {d} cm. ¿Cuál es la distancia real entre ellas?", c, w,
                f"{d} cm · {fint(n)} = {fint(d * n)} cm = {fmt(km)} km.")


def t_area_tri():
    b, h = rnd.randint(4, 24), rnd.randint(3, 20)
    if (b * h) % 2:
        raise Skip()
    c, w = numeric_options(b * h // 2, [b * h, b + h, b * h // 4], step=b, fn=lambda v: f"{fint(v)} cm²")
    return make(GEOMETRIA, f"Un triángulo tiene base {b} cm y altura {h} cm. ¿Cuál es su área?", c, w, f"A = base · altura / 2 = {b}·{h}/2 = {b * h // 2} cm².")


def t_dist_points():
    dx3, dy4 = rnd.choice([(3, 4), (6, 8), (5, 12), (8, 6), (9, 12), (4, 3)])
    h = int(math.hypot(dx3, dy4))
    x1, y1 = rnd.randint(-5, 5), rnd.randint(-5, 5)
    x2, y2 = x1 + rnd.choice([-1, 1]) * dx3, y1 + rnd.choice([-1, 1]) * dy4
    c, w = numeric_options(h, [dx3 + dy4, abs(dx3 - dy4), dx3 * dy4 // 2], step=1)
    return make(GEOMETRIA, f"¿Cuál es la distancia entre los puntos {pt(x1, y1)} y {pt(x2, y2)}?", c, w,
                f"d = √({dx3}² + {dy4}²) = √{dx3 * dx3 + dy4 * dy4} = {h}.")


def t_midpoint():
    x1, y1 = rnd.randint(-8, 8), rnd.randint(-8, 8)
    x2, y2 = x1 + 2 * rnd.randint(-6, 6), y1 + 2 * rnd.randint(-6, 6)
    mx, my = (x1 + x2) // 2, (y1 + y2) // 2
    if (x1, y1) == (x2, y2):
        raise Skip()
    c = pt(mx, my)
    w = [pt(x1 + x2, y1 + y2), pt(x2 - x1, y2 - y1), pt(my, mx), pt(mx + 1, my - 1)]
    return make(GEOMETRIA, f"¿Cuáles son las coordenadas del punto medio del segmento con extremos {pt(x1, y1)} y {pt(x2, y2)}?", c, w,
                f"Se promedian las coordenadas: (({fint(x1)} + ({fint(x2)}))/2, ({fint(y1)} + ({fint(y2)}))/2) = {c}.")


def t_reflection():
    a, b = rnd.choice([v for v in range(-8, 9) if v]), rnd.choice([v for v in range(-8, 9) if v])
    if a == b or a == -b:
        raise Skip()
    kind = rnd.choice([("del eje x", pt(a, -b)), ("del eje y", pt(-a, b)), ("del origen", pt(-a, -b))])
    pool = [pt(a, -b), pt(-a, b), pt(-a, -b), pt(b, a)]
    w = [p for p in pool if p != kind[1]]
    return make(GEOMETRIA, f"¿Cuáles son las coordenadas del punto simétrico de {pt(a, b)} respecto {kind[0]}?", kind[1], w,
                {"del eje x": "Al reflejar respecto del eje x cambia el signo de la coordenada y.",
                 "del eje y": "Al reflejar respecto del eje y cambia el signo de la coordenada x.",
                 "del origen": "Al reflejar respecto del origen cambian los signos de ambas coordenadas."}[kind[0]])


def t_translation():
    a, b = rnd.randint(-8, 8), rnd.randint(-8, 8)
    u, v = rnd.choice([v for v in range(-6, 7) if v]), rnd.choice([v for v in range(-6, 7) if v])
    c = pt(a + u, b + v)
    w = [pt(a - u, b - v), pt(a + u, b - v), pt(a - u, b + v), pt(a * u, b * v)]
    return make(GEOMETRIA, f"Al trasladar el punto {pt(a, b)} según el vector ({fint(u)}, {fint(v)}), ¿cuáles son las nuevas coordenadas?", c, w,
                f"Se suman las componentes: ({a}+({u}), {b}+({v})) = {c}.")


# ================================== PLANTILLAS: PROBABILIDAD Y ESTADÍSTICA
def t_mean_list():
    n = rnd.choice([5, 6, 8])
    data = [rnd.randint(2, 20) for _ in range(n)]
    data[-1] += (-sum(data)) % n
    if data[-1] > 40:
        raise Skip()
    m = sum(data) // n
    rnd.shuffle(data)
    c, w = numeric_options(m, [sorted(data)[n // 2], max(data), sum(data) // (n - 1) if n > 1 else 1], step=1)
    return make(PROBA, f"¿Cuál es el promedio de los datos {', '.join(map(str, data))}?", c, w,
                f"Suma = {sum(data)}; promedio = {sum(data)}/{n} = {m}.")


def t_median():
    n = rnd.choice([5, 7, 6, 8])
    data = [rnd.randint(1, 30) for _ in range(n)]
    s = sorted(data)
    med = Fraction(s[n // 2]) if n % 2 else Fraction(s[n // 2 - 1] + s[n // 2], 2)
    if (med * 2).denominator != 1:
        raise Skip()
    rnd.shuffle(data)
    c, w = numeric_options(med, [Fraction(sum(data), n), s[0], s[-1], data[n // 2]], step=Fraction(1, 2))
    return make(PROBA, f"¿Cuál es la mediana de los datos {', '.join(map(str, data))}?", c, w,
                f"Ordenados: {', '.join(map(str, s))}. La mediana es {fmt(med)}.")


def t_prob_bag():
    r, a, v = rnd.randint(2, 9), rnd.randint(2, 9), rnd.randint(1, 8)
    T = r + a + v
    sing, cnt = rnd.choice([("roja", r), ("azul", a), ("verde", v)])
    res = Fraction(cnt, T)
    cands = [Fraction(cnt, T - cnt), Fraction(1, 3), Fraction(T - cnt, T), Fraction(cnt, T + 1), Fraction(1, T)]
    w = [frac_str(x) for x in cands if x != res and 0 < x <= 1]
    return make(PROBA, f"Una bolsa tiene {r} fichas rojas, {a} azules y {v} verdes. Si se saca una ficha al azar, ¿cuál es la probabilidad de que sea {sing}?",
                frac_str(res), w, f"Casos favorables {cnt}, casos totales {T}: P = {frac_str(res)}.")


def t_complement():
    p = rnd.choice([5, 10, 15, 20, 25, 30, 35, 40, 45, 60, 65, 70])
    ev = rnd.choice(["llueva mañana", "un estudiante llegue atrasado", "un producto salga defectuoso", "un equipo gane el partido"])
    neg = {"llueva mañana": "no llueva mañana", "un estudiante llegue atrasado": "un estudiante NO llegue atrasado",
           "un producto salga defectuoso": "un producto NO salga defectuoso", "un equipo gane el partido": "un equipo NO gane el partido"}[ev]
    c, w = numeric_options(100 - p, [p, 100 + p, 50, 100 - 2 * p if p < 50 else 100 - p // 2], step=5, fn=lambda v: f"{fmt(v)}%")
    return make(PROBA, f"La probabilidad de que {ev} es {p}%. ¿Cuál es la probabilidad de que {neg}?", c, w, f"Eventos complementarios suman 100%: 100% {MINUS} {p}% = {100 - p}%.")


def t_independent():
    r, a = rnd.randint(2, 6), rnd.randint(2, 6)
    T = r + a + rnd.randint(1, 4)
    res = Fraction(r * a, T * T)
    cands = [Fraction(r, T) + Fraction(a, T), Fraction(r * a, T * (T - 1)), Fraction(r * r, T * T), Fraction(r, T) * Fraction(1, 2)]
    w = [frac_str(x) for x in cands if x != res]
    return make(PROBA, f"Una urna tiene {T} bolitas: {r} rojas, {a} azules y el resto verdes. Se saca una bolita, se anota su color y se devuelve a la urna; luego se saca otra. ¿Cuál es la probabilidad de que la primera sea roja y la segunda azul?",
                frac_str(res), w, f"Los eventos son independientes: {r}/{T} · {a}/{T} = {frac_str(res)}.")


def t_stat_percent():
    N = rnd.randrange(40, 400, 20)
    p = rnd.choice([10, 15, 20, 25, 30, 35, 40, 45, 60])
    if (N * p) % 100:
        raise Skip()
    yes = N * p // 100
    sport = rnd.choice(["fútbol", "básquetbol", "natación", "vóleibol"])
    c, w = numeric_options(N - yes, [yes, N - p, N + yes], step=max(1, yes // 4))
    return make(PROBA, f"En un colegio de {N} estudiantes, el {p}% practica {sport}. ¿Cuántos estudiantes NO practican {sport}?", c, w,
                f"{p}% de {N} = {yes} practican; los demás son {N} {MINUS} {yes} = {N - yes}.")


# ====================================================== PLANTILLAS NUEVAS (temario 2027)
SUPERS = {2: "", 3: "∛", 4: "∜"}


def root_str(n, x):
    """√x, ∛x o ∜x."""
    return f"{'√' if n == 2 else SUPERS[n]}{fint(x)}"


def poly_str(a, b, c):
    """Escribe ax² + bx + c de forma natural: x² − 5x + 6, −x² + 4x."""
    def term(coef, var, first):
        if coef == 0:
            return ""
        sign = ("" if coef > 0 else MINUS) if first else (" + " if coef > 0 else f" {MINUS} ")
        mag = abs(coef)
        body = (var if mag == 1 and var else f"{fint(mag)}{var}")
        return sign + body
    s = term(a, "x²", True)
    s += term(b, "x", s == "")
    s += term(c, "", s == "")
    return s or "0"


def t_root_simplify():
    n = rnd.choice([2, 2, 3])
    a = rnd.randint(2, 6 if n == 2 else 4)
    b = rnd.choice([2, 3, 5, 6, 7] if n == 2 else [2, 3, 4, 5])
    x = a ** n * b
    c = f"{a}{root_str(n, b)}"
    w = [f"{b}{root_str(n, a)}", f"{a * a}{root_str(n, b)}", f"{a}{root_str(n, b * a)}", f"{a + b}{root_str(n, b)}", f"{root_str(n, a * b)}"]
    return make(NUMEROS, f"Al simplificar {root_str(n, x)} se obtiene:", c, w,
                f"{root_str(n, x)} = {root_str(n, a ** n)}·{root_str(n, b)} = {a}{root_str(n, b)}, porque {a}{sup(n)} = {a ** n}.")


def t_root_eval():
    n = rnd.choice([2, 3, 3, 4])
    r = rnd.randint(2, 10 if n == 2 else (6 if n == 3 else 4))
    x = r ** n
    if rnd.random() < 0.5:
        c, w = numeric_options(r, [x // n if x % n == 0 else r + 2, r * n, r * r if n != 2 else r + 1], step=1)
        return make(NUMEROS, f"¿Cuál es el valor de {root_str(n, x)}?", c, w, f"{r}{sup(n)} = {x}, por lo tanto {root_str(n, x)} = {r}.")
    a, b = rnd.choice([(2, 8), (3, 12), (2, 18), (5, 20), (3, 27), (2, 32), (6, 24), (7, 28)])
    p = int(math.isqrt(a * b))
    c, w = numeric_options(p, [a * b, a + b, p * 2], step=1)
    return make(NUMEROS, f"¿Cuál es el resultado de √{a} · √{b}?", c, w, f"√{a}·√{b} = √({a}·{b}) = √{a * b} = {p}.")


def t_rational_power():
    base, num, den = rnd.choice([(8, 2, 3), (27, 2, 3), (16, 3, 4), (4, 3, 2), (9, 3, 2), (25, 1, 2), (64, 2, 3), (81, 3, 4),
                                 (32, 2, 5), (125, 1, 3), (16, 1, 4), (36, 1, 2), (8, 1, 3), (100, 3, 2)])
    r = round(base ** (1 / den))
    if r ** den != base:
        raise Skip()
    val = r ** num
    c, w = numeric_options(val, [base * num // den if (base * num) % den == 0 else val + 1, r, base ** num // den if num == 1 else r * num], step=1)
    return make(NUMEROS, f"¿Cuál es el valor de {base}^({num}/{den})?", c, w,
                f"{base}^({num}/{den}) = ({root_str(den, base) if den in SUPERS else f'raíz {den} de {base}'})^{num} = {r}^{num} = {val}.")


def t_quad_eq():
    r1, r2 = rnd.sample([v for v in range(-7, 8) if v], 2)
    b, c_ = -(r1 + r2), r1 * r2
    s = lambda u, v: f"x = {fint(min(u, v))} y x = {fint(max(u, v))}"
    corr = s(r1, r2)
    w = [s(-r1, -r2), s(r1, -r2), s(-r1, r2), s(r1 + r2, r1 * r2)]
    return make(ALGEBRA, f"¿Cuáles son las soluciones de la ecuación {poly_str(1, b, c_)} = 0?", corr, w,
                f"Se factoriza: (x {MINUS if r1 > 0 else '+'} {abs(r1)})(x {MINUS if r2 > 0 else '+'} {abs(r2)}) = 0, entonces x = {fint(r1)} o x = {fint(r2)}.")


def t_quad_vertex():
    a = rnd.choice([1, 1, -1])
    h, k = rnd.randint(-5, 5), rnd.randint(-6, 6)
    b, c_ = -2 * a * h, a * h * h + k
    if b == 0:
        raise Skip()
    corr = pt(h, k)
    w = [pt(-h, k), pt(h, -k), pt(-h, -k), pt(k, h), pt(h, c_)]
    return make(ALGEBRA, f"¿Cuáles son las coordenadas del vértice de la parábola f(x) = {poly_str(a, b, c_)}?", corr, w,
                f"x del vértice = −b/(2a) = {fint(-b)}/{fint(2 * a) if a > 0 else '(' + fint(2 * a) + ')'} = {fint(h)}; f({fint(h)}) = {fint(k)}. Vértice {corr}.")


def t_quad_points():
    a = rnd.choice([1, 1, 2, -1])
    r1, r2 = rnd.sample([v for v in range(-6, 7) if v], 2)
    b, c_ = -a * (r1 + r2), a * r1 * r2
    if rnd.random() < 0.5:
        c, w = numeric_options(c_, [-c_, b, a, r1 + r2], step=1, positive=False, fn=lambda v: pt(0, v))
        return make(ALGEBRA, f"¿En qué punto la gráfica de f(x) = {poly_str(a, b, c_)} intersecta al eje y?", c, w,
                    f"Se reemplaza x = 0: f(0) = {fint(c_)}. El punto es {pt(0, c_)}.")
    s = lambda u, v: f"{pt(min(u, v), 0)} y {pt(max(u, v), 0)}"
    corr = s(r1, r2)
    w = [s(-r1, -r2), f"{pt(0, r1)} y {pt(0, r2)}", s(r1, -r2), s(-r1, r2)]
    return make(ALGEBRA, f"¿En qué puntos la gráfica de f(x) = {poly_str(a, b, c_)} intersecta al eje x?", corr, w,
                f"Los ceros cumplen f(x) = 0: {poly_str(a, b, c_)} = 0 da x = {fint(r1)} y x = {fint(r2)}.")


def t_quad_problem():
    if rnd.random() < 0.5:
        v = rnd.choice([10, 20, 30, 40])
        t = v // 10
        H = 5 * t * t
        c, w = numeric_options(H, [v * t, 2 * H, v], step=5, fn=lambda x: f"{fint(x)} m")
        return make(ALGEBRA, f"La altura (en metros) de una pelota lanzada hacia arriba está dada por h(t) = −5t² + {v}t, con t en segundos. ¿Cuál es la altura máxima que alcanza?", c, w,
                    f"El máximo está en el vértice: t = −{v}/(2·(−5)) = {t} s; h({t}) = −5·{t * t} + {v}·{t} = {H} m.")
    x = rnd.randint(3, 12)
    d = rnd.randint(1, 6)
    A = x * (x + d)
    c, w = numeric_options(x, [x + d, A // 2 if A // 2 != x else x + 2, d], step=1, fn=lambda v: f"{fint(v)} cm")
    return make(ALGEBRA, f"Un rectángulo tiene un largo {d} cm mayor que su ancho, y su área es {A} cm². ¿Cuánto mide el ancho?", c, w,
                f"Si el ancho es x: x(x + {d}) = {A}, o sea x² + {d}x − {A} = 0. La solución positiva es x = {x} cm.")


def t_trapezoid():
    B, b, h = rnd.randint(8, 20), rnd.randint(3, 7), rnd.randint(3, 12)
    if (B + b) * h % 2:
        raise Skip()
    A = (B + b) * h // 2
    c, w = numeric_options(A, [(B + b) * h, B * h, b * h, B * b // 2], step=h, fn=lambda v: f"{fint(v)} cm²")
    return make(GEOMETRIA, f"Un trapecio tiene bases de {B} cm y {b} cm, y una altura de {h} cm. ¿Cuál es su área?", c, w,
                f"Área = (base mayor + base menor)·altura/2 = ({B} + {b})·{h}/2 = {A} cm².")


def t_parallelogram():
    b, h = rnd.randint(4, 18), rnd.randint(3, 10)
    lado = h + rnd.randint(1, 4)
    if rnd.random() < 0.6:
        c, w = numeric_options(b * h, [b * lado, 2 * (b + lado), b * h // 2 if (b * h) % 2 == 0 else b * h + 2], step=b, fn=lambda v: f"{fint(v)} cm²")
        return make(GEOMETRIA, f"Un paralelogramo tiene una base de {b} cm, su lado inclinado mide {lado} cm y su altura (perpendicular a la base) mide {h} cm. ¿Cuál es su área?", c, w,
                    f"Área = base·altura = {b}·{h} = {b * h} cm². El lado inclinado no se usa para el área.")
    c, w = numeric_options(2 * (b + lado), [b * h, b + lado, 2 * (b + h)], step=2, fn=lambda v: f"{fint(v)} cm")
    return make(GEOMETRIA, f"Un paralelogramo tiene lados de {b} cm y {lado} cm. ¿Cuál es su perímetro?", c, w,
                f"Los lados opuestos son iguales: 2·({b} + {lado}) = {2 * (b + lado)} cm.")


def t_surface():
    kind = rnd.randint(1, 3)
    cm2 = lambda v: f"{fint(v)} cm²"
    if kind == 1:
        a = rnd.randint(2, 10)
        c, w = numeric_options(6 * a * a, [a ** 3, 4 * a * a, a * a], step=a, fn=cm2)
        return make(GEOMETRIA, f"¿Cuál es el área total de la superficie de un cubo de arista {a} cm?", c, w,
                    f"Un cubo tiene 6 caras cuadradas: 6·{a}² = {6 * a * a} cm².")
    if kind == 2:
        a, b, h = rnd.randint(2, 10), rnd.randint(2, 8), rnd.randint(2, 9)
        if len({a, b, h}) < 3:
            raise Skip()
        S = 2 * (a * b + a * h + b * h)
        c, w = numeric_options(S, [a * b * h, a * b + a * h + b * h, 2 * a * b], step=2, fn=cm2)
        return make(GEOMETRIA, f"Una caja con forma de paralelepípedo mide {a} cm de largo, {b} cm de ancho y {h} cm de alto. ¿Cuánto cartón se necesita para cubrir toda su superficie (área total)?", c, w,
                    f"Área total = 2·({a}·{b} + {a}·{h} + {b}·{h}) = {S} cm².")
    r, h = rnd.randint(2, 6), rnd.randint(3, 12)
    tot = 2 * r * r + 2 * r * h
    c = f"{tot}π cm²"
    w = [f"{r * r * h}π cm²", f"{2 * r * h}π cm²", f"{r * r + 2 * r * h}π cm²", f"{2 * r * r + r * h}π cm²"]
    return make(GEOMETRIA, f"Un cilindro cerrado tiene radio {r} cm y altura {h} cm. ¿Cuál es el área total de su superficie?", c, w,
                f"Área total = 2 tapas + manto = 2π·{r}² + 2π·{r}·{h} = {2 * r * r}π + {2 * r * h}π = {tot}π cm².")


def t_rotation():
    a, b = rnd.choice([v for v in range(-7, 8) if v]), rnd.choice([v for v in range(-7, 8) if v])
    if abs(a) == abs(b):
        raise Skip()
    kind, res, ex = rnd.choice([
        ("90° en sentido antihorario", pt(-b, a), "Al rotar 90° antihorario respecto del origen, (x, y) pasa a (−y, x)."),
        ("90° en sentido horario", pt(b, -a), "Al rotar 90° horario respecto del origen, (x, y) pasa a (y, −x)."),
        ("180°", pt(-a, -b), "Al rotar 180° respecto del origen, (x, y) pasa a (−x, −y)."),
    ])
    pool = [pt(-b, a), pt(b, -a), pt(-a, -b), pt(b, a), pt(a, -b)]
    return make(GEOMETRIA, f"El punto {pt(a, b)} se rota {kind} con centro en el origen. ¿Cuáles son las coordenadas del punto obtenido?", res,
                [p for p in pool if p != res], ex)


def quartile_data():
    """8 datos ordenados en que todos los métodos de cálculo de cuartiles coinciden."""
    while True:
        d = sorted(rnd.sample(range(1, 40), 6))
        data = [d[0], d[1], d[1], d[2], d[3], d[4], d[4], d[5]]
        if len(set(data)) >= 6 and (data[3] + data[4]) % 2 == 0:
            return data


def t_quartiles():
    data = quartile_data()
    q1, q3, med = data[1], data[5], (data[3] + data[4]) // 2
    shown = data[:]
    rnd.shuffle(shown)
    lst = ", ".join(map(str, shown))
    k = rnd.randint(1, 3)
    if k == 1:
        c, w = numeric_options(q1, [med, q3, data[0], data[2] + 1], step=1)
        return make(PROBA, f"¿Cuál es el primer cuartil (Q₁) de los datos {lst}?", c, w,
                    f"Ordenados: {', '.join(map(str, data))}. Q₁ es la mediana de la primera mitad ({', '.join(map(str, data[:4]))}): {q1}.")
    if k == 2:
        c, w = numeric_options(q3, [med, q1, data[-1], data[5] - 1], step=1)
        return make(PROBA, f"¿Cuál es el tercer cuartil (Q₃) de los datos {lst}?", c, w,
                    f"Ordenados: {', '.join(map(str, data))}. Q₃ es la mediana de la segunda mitad ({', '.join(map(str, data[4:]))}): {q3}.")
    c, w = numeric_options(q3 - q1, [data[-1] - data[0], q3, med - q1], step=1)
    return make(PROBA, f"¿Cuál es el rango intercuartil (Q₃ − Q₁) de los datos {lst}?", c, w,
                f"Ordenados: {', '.join(map(str, data))}. Q₁ = {q1} y Q₃ = {q3}; Q₃ − Q₁ = {q3 - q1}.")


def t_percentile():
    n = rnd.choice([40, 50, 80, 120, 200, 300, 400])
    p = rnd.choice([10, 20, 25, 30, 40, 60, 75, 80, 90])
    if (n * p) % 100:
        raise Skip()
    v = n * p // 100
    if rnd.random() < 0.5:
        c, w = numeric_options(v, [n - v, p, n // 2], step=max(1, n // 20))
        return make(PROBA, f"En una prueba rendida por {n} estudiantes, el puntaje de Martina corresponde al percentil {p}. ¿Aproximadamente cuántos estudiantes obtuvieron un puntaje menor o igual que el de Martina?", c, w,
                    f"El percentil {p} deja bajo él (o igual) al {p}% de los datos: {p}% de {n} = {v}.")
    c, w = numeric_options(100 - p, [p, 50, 100 - p // 2], step=5, fn=lambda x: f"{fmt(x)}%")
    return make(PROBA, f"El puntaje de un estudiante corresponde al percentil {p} de su curso. ¿Qué porcentaje aproximado del curso obtuvo un puntaje mayor que el suyo?", c, w,
                f"Bajo el percentil {p} está el {p}% de los datos; por encima queda el {100 - p}%.")


def t_additive():
    if rnd.random() < 0.5:
        r, a, v = rnd.randint(2, 8), rnd.randint(2, 8), rnd.randint(2, 8)
        T = r + a + v
        res = Fraction(r + a, T)
        cands = [Fraction(r * a, T * T), Fraction(r, T), Fraction(a, T), Fraction(v, T), Fraction(r + a, T * 2)]
        return make(PROBA, f"Una caja tiene {r} fichas rojas, {a} azules y {v} verdes. Si se saca una ficha al azar, ¿cuál es la probabilidad de que sea roja o azul?",
                    frac_str(res), [frac_str(x) for x in cands if x != res],
                    f"Son eventos excluyentes: P(roja o azul) = {r}/{T} + {a}/{T} = {frac_str(res)}.")
    A_txt, A = rnd.choice([("un número par", {2, 4, 6}), ("un número impar", {1, 3, 5}), ("un número menor que 3", {1, 2})])
    B_txt, B = rnd.choice([("un número mayor que 4", {5, 6}), ("un múltiplo de 3", {3, 6}), ("el número 1", {1})])
    if not (A & B) and rnd.random() < 0.6:
        raise Skip()
    res = Fraction(len(A | B), 6)
    cands = [Fraction(len(A) + len(B), 6), Fraction(len(A & B), 6), Fraction(len(A) * len(B), 36), Fraction(len(A), 6)]
    ex = (f"P(A o B) = P(A) + P(B) − P(A y B) = {len(A)}/6 + {len(B)}/6 − {len(A & B)}/6 = {frac_str(res)}."
          if A & B else f"No tienen resultados en común: {len(A)}/6 + {len(B)}/6 = {frac_str(res)}.")
    return make(PROBA, f"Se lanza un dado común de seis caras. ¿Cuál es la probabilidad de obtener {A_txt} o {B_txt}?",
                frac_str(res), [frac_str(x) for x in cands if x != res], ex)


TEXT_TEMPLATES = [
    # Números
    t_percent_of, t_inc_dec, t_discount, t_fraction_add, t_direct_prop, t_inverse_prop, t_power,
    t_mean_add, t_simple_interest, t_ratio_share, t_order_ops, t_neg_ops, t_percent_what, t_speed,
    t_root_simplify, t_root_eval, t_rational_power,
    # Álgebra y funciones
    t_linear_eq, t_eval_fn, t_slope, t_system, t_binomial, t_factor, t_inequality, t_age,
    t_prop_fn, t_line_eq, t_perimeter_alg, t_quad_eq, t_quad_vertex, t_quad_points, t_quad_problem,
    # Geometría
    t_rect, t_pyth, t_circle, t_volume, t_thales, t_scale, t_area_tri, t_trapezoid, t_parallelogram, t_surface,
    t_dist_points, t_midpoint, t_reflection, t_translation, t_rotation,
    # Probabilidad y estadística
    t_mean_list, t_median, t_prob_bag, t_complement, t_independent, t_stat_percent,
    t_quartiles, t_percentile, t_additive,
]


# ============================================================== GRÁFICOS
_img_counter = [0]


def save_fig(fig):
    _img_counter[0] += 1
    name = f"m1_img_{_img_counter[0]:03d}.png"
    os.makedirs(IMG_DIR, exist_ok=True)
    fig.savefig(os.path.join(IMG_DIR, name), dpi=100, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return f"assets/images/m1/{name}"


COLORS = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]

BAR_THEMES = [
    ("Libros prestados en la biblioteca", "Libros", ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]),
    ("Goles anotados por jugador", "Goles", ["Pedro", "Luis", "Carla", "Juan", "Rosa", "Mario"]),
    ("Frutas vendidas en una feria", "Kilos", ["Manzanas", "Peras", "Uvas", "Plátanos", "Naranjas", "Duraznos"]),
    ("Estudiantes por taller", "Estudiantes", ["Teatro", "Música", "Ajedrez", "Pintura", "Robótica", "Danza"]),
    ("Entradas vendidas por función", "Entradas", ["Función 1", "Función 2", "Función 3", "Función 4", "Función 5"]),
    ("Botellas recicladas por curso", "Botellas", ["1° A", "1° B", "2° A", "2° B", "3° A"]),
]


def g_bar():
    title, ylab, cats = rnd.choice(BAR_THEMES)
    k = rnd.randint(4, min(6, len(cats)))
    cats = cats[:k]
    vals = rnd.sample(range(4, 21), k)
    vals = [v * 5 for v in vals]
    fig, ax = plt.subplots(figsize=(6, 3.8))
    bars = ax.bar(cats, vals, color=COLORS[:k] if rnd.random() < 0.4 else "#4682b4")
    for b_, v in zip(bars, vals):
        ax.text(b_.get_x() + b_.get_width() / 2, v + max(vals) * 0.015, str(v), ha="center", va="bottom", fontsize=10)
    ax.set_title(title)
    ax.set_ylabel(ylab)
    ax.set_ylim(0, max(vals) * 1.15)
    img = save_fig(fig)
    kind = rnd.choice(["max", "min", "diff", "sum"])
    unit = ylab.lower()
    if kind == "max":
        i = vals.index(max(vals))
        enun = "Observa el gráfico. ¿Cuál es la categoría con el valor más alto?"
        return make(ESTADIST, enun, cats[i], [x for x in cats if x != cats[i]], f"La barra más alta es {cats[i]}, con {vals[i]}.", img)
    if kind == "min":
        i = vals.index(min(vals))
        return make(ESTADIST, "Observa el gráfico. ¿Cuál es la categoría con el valor más bajo?", cats[i], [x for x in cats if x != cats[i]], f"La barra más baja es {cats[i]}, con {vals[i]}.", img)
    if kind == "diff":
        i, j = rnd.sample(range(k), 2)
        if vals[i] < vals[j]:
            i, j = j, i
        d = vals[i] - vals[j]
        c, w = numeric_options(d, [vals[i] + vals[j], vals[i], vals[j]], step=5)
        return make(ESTADIST, f"Según el gráfico, ¿cuántas unidades más tiene \"{cats[i]}\" que \"{cats[j]}\"?", c, w, f"{vals[i]} {MINUS} {vals[j]} = {d}.", img)
    s = sum(vals)
    c, w = numeric_options(s, [s - min(vals), s + 5, max(vals) * k], step=5)
    return make(ESTADIST, "Según el gráfico, ¿cuál es el total de unidades sumando todas las categorías?", c, w, f"Se suman todas las barras: {' + '.join(map(str, vals))} = {s}.", img)


ESTADIST = PROBA
MONTHS = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto"]


def g_line():
    k = rnd.randint(5, 7)
    start = rnd.randint(0, 8 - k)
    ms = MONTHS[start:start + k]
    vals = rnd.sample(range(10, 80), k)
    vals = [v for v in vals]
    fig, ax = plt.subplots(figsize=(6, 3.8))
    ax.plot(ms, vals, marker="o", color="#1f77b4")
    for x, v in zip(ms, vals):
        ax.annotate(str(v), (x, v), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=10)
    ax.set_title(rnd.choice(["Temperatura media mensual (°C × 2)", "Visitas mensuales a un museo (cientos)", "Ventas mensuales de una tienda (unidades)"]))
    ax.grid(axis="y", alpha=0.3)
    ax.set_ylim(min(vals) - 8, max(vals) + 12)
    img = save_fig(fig)
    kind = rnd.choice(["max", "diff", "rise"])
    if kind == "max":
        i = vals.index(max(vals))
        return make(ESTADIST, "Según el gráfico, ¿en qué mes se registró el valor más alto?", ms[i], [m for m in ms if m != ms[i]], f"El punto más alto corresponde a {ms[i]} ({vals[i]}).", img)
    if kind == "diff":
        i, j = sorted(rnd.sample(range(k), 2))
        d = vals[j] - vals[i]
        c, w = numeric_options(d, [abs(d) + 3, vals[i] + vals[j], vals[j]], step=4, positive=False)
        return make(ESTADIST, f"Según el gráfico, ¿en cuántas unidades cambió el valor entre {ms[i]} y {ms[j]}? (valor final {MINUS} valor inicial)", c, w, f"{vals[j]} {MINUS} {vals[i]} = {fint(d)}.", img)
    diffs = [vals[i + 1] - vals[i] for i in range(k - 1)]
    best = max(diffs)
    if diffs.count(best) != 1 or best <= 0:
        raise Skip()
    i = diffs.index(best)
    correct = f"Entre {ms[i]} y {ms[i + 1]}"
    wrongs = [f"Entre {ms[j]} y {ms[j + 1]}" for j in range(k - 1) if j != i]
    return make(ESTADIST, "Según el gráfico, ¿entre qué meses consecutivos hubo el mayor aumento?", correct, wrongs, f"El mayor aumento fue de {best} unidades, entre {ms[i]} y {ms[i + 1]}.", img)


def g_pie():
    cats = rnd.choice([
        ["Fútbol", "Tenis", "Natación", "Básquetbol", "Atletismo"],
        ["Pizza", "Sushi", "Hamburguesa", "Ensalada", "Empanada"],
        ["Azul", "Rojo", "Verde", "Amarillo", "Negro"],
        ["Bus", "Metro", "Bicicleta", "Auto", "A pie"],
    ])
    k = rnd.randint(4, 5)
    cats = cats[:k]
    while True:
        parts = [rnd.randrange(10, 41, 5) for _ in range(k - 1)]
        last = 100 - sum(parts)
        if last >= 5 and last % 5 == 0 and len(set(parts + [last])) == k:
            parts.append(last)
            break
    N = rnd.choice([40, 60, 80, 100, 120, 160, 200, 240, 300])
    fig, ax = plt.subplots(figsize=(5.2, 4.2))
    ax.pie(parts, labels=cats, autopct="%d%%", colors=COLORS[:k], startangle=90, counterclock=False, wedgeprops={"edgecolor": "white"})
    ax.set_title(rnd.choice(["Preferencia de los encuestados", "Resultados de una encuesta"]))
    img = save_fig(fig)
    kind = rnd.choice(["count", "sum", "diff"])
    if kind == "count":
        i = rnd.randrange(k)
        v = parts[i] * N // 100
        c, w = numeric_options(v, [parts[i], N - v, v * 2], step=max(1, N // 20))
        return make(ESTADIST, f"En la encuesta participaron {N} personas. Según el gráfico, ¿cuántas personas eligieron \"{cats[i]}\"?", c, w, f"{parts[i]}% de {N} = {v}.", img)
    if kind == "sum":
        i, j = rnd.sample(range(k), 2)
        v = parts[i] + parts[j]
        c, w = numeric_options(v, [abs(parts[i] - parts[j]), parts[i] * parts[j] // 10, 100 - v], step=5, fn=lambda x: f"{fmt(x)}%")
        return make(ESTADIST, f"Según el gráfico, ¿qué porcentaje representan en conjunto \"{cats[i]}\" y \"{cats[j]}\"?", c, w, f"{parts[i]}% + {parts[j]}% = {v}%.", img)
    i, j = rnd.sample(range(k), 2)
    if parts[i] < parts[j]:
        i, j = j, i
    v = (parts[i] - parts[j]) * N // 100
    c, w = numeric_options(v, [parts[i] - parts[j], (parts[i] + parts[j]) * N // 100, parts[i] * N // 100], step=max(1, N // 20))
    return make(ESTADIST, f"Si se encuestó a {N} personas, ¿cuántas más eligieron \"{cats[i]}\" que \"{cats[j]}\"?", c, w, f"({parts[i]}% {MINUS} {parts[j]}%) de {N} = {v}.", img)


def g_freq_table():
    vals = sorted(rnd.sample(range(1, 11), 5))
    while True:
        freqs = [rnd.randint(1, 12) for _ in vals]
        S = sum(freqs)
        tot = sum(v * f for v, f in zip(vals, freqs))
        if S in (10, 20, 25, 30, 40) or (Fraction(tot, S) * 10).denominator == 1:
            break
    fig, ax = plt.subplots(figsize=(3.6, 2.6))
    ax.axis("off")
    # La moda no está en el temario de M1: solo promedio y mediana.
    kind = rnd.choice(["mean", "median"])
    head = rnd.choice([("Nota", "Frecuencia"), ("Valor", "Frecuencia"), ("Puntos", "Cantidad de estudiantes")])
    tbl = ax.table(cellText=[[str(v), str(f)] for v, f in zip(vals, freqs)], colLabels=list(head), loc="center", cellLoc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(11)
    tbl.scale(1, 1.5)
    img = save_fig(fig)
    data = [v for v, f in zip(vals, freqs) for _ in range(f)]
    if kind == "mean":
        m = Fraction(tot, S)
        if (m * 100).denominator != 1:
            raise Skip()
        c, w = numeric_options(m, [Fraction(sum(vals), 5), vals[2], max(vals)], step=Fraction(1, 2))
        return make(PROBA, "La tabla muestra la distribución de un conjunto de datos. ¿Cuál es el promedio?", c, w, f"Suma de (valor · frecuencia) = {tot}; total de datos = {S}; promedio = {fmt(m)}.", img)
    if kind == "mode":
        mx = max(freqs)
        if freqs.count(mx) != 1:
            raise Skip()
        mode = vals[freqs.index(mx)]
        c, w = numeric_options(mode, [x for x in vals if x != mode], step=1)
        return make(PROBA, "La tabla muestra la distribución de un conjunto de datos. ¿Cuál es la moda?", c, w, f"La mayor frecuencia es {mx}, que corresponde al valor {mode}.", img)
    n = len(data)
    med = Fraction(data[n // 2]) if n % 2 else Fraction(data[n // 2 - 1] + data[n // 2], 2)
    c, w = numeric_options(med, [Fraction(tot, S), vals[2], vals[0] + 1, max(vals)], step=Fraction(1, 2))
    return make(PROBA, "La tabla muestra la distribución de un conjunto de datos. ¿Cuál es la mediana?", c, w, f"Hay {n} datos; ordenados, la mediana es {fmt(med)}.", img)


def g_cartesian():
    m = rnd.choice([-3, -2, -1, 1, 2, 3])
    b = rnd.randint(-4, 4)
    xa, xb = sorted(rnd.sample(range(-3, 4), 2))
    pa, pb = (xa, m * xa + b), (xb, m * xb + b)
    if max(abs(pa[1]), abs(pb[1])) > 8:
        raise Skip()
    fig, ax = plt.subplots(figsize=(4.6, 4.6))
    xs = [-6, 6]
    ys = [m * x + b for x in xs]
    ax.plot(xs, ys, color="#1f77b4")
    for (px, py) in (pa, pb):
        ax.plot(px, py, "o", color="#d62728")
        ax.annotate(f"({px}, {py})", (px, py), textcoords="offset points", xytext=(6, 6), fontsize=10)
    ax.set_xlim(-7, 7)
    ax.set_ylim(-9, 9)
    ax.set_xticks(range(-6, 7, 2))
    ax.set_yticks(range(-8, 9, 2))
    ax.grid(alpha=0.4)
    ax.axhline(0, color="black", lw=1)
    ax.axvline(0, color="black", lw=1)
    ax.text(7.1, 0.0, "x", fontsize=12, va="center")
    ax.text(0.0, 9.4, "y", fontsize=12, ha="center")
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    img = save_fig(fig)
    kind = rnd.choice(["slope", "eq", "value"])
    if kind == "slope":
        c, w = numeric_options(m, [-m, b, 1 / m if False else m + 1], step=1, positive=False)
        return make(ALGEBRA, "La recta del gráfico pasa por los dos puntos marcados. ¿Cuál es su pendiente?", c, w, f"m = ({pb[1]} {MINUS} {pa[1]})/({pb[0]} {MINUS} {pa[0]}) = {m}.", img)
    if kind == "eq":
        if b == 0:
            raise Skip()
        c = line_str(m, b)
        w = [line_str(b, m), line_str(-m, b), line_str(m, -b), line_str(-m, -b)]
        return make(ALGEBRA, "¿Cuál es la ecuación de la recta representada en el gráfico?", c, w, f"Pendiente {m}; corta al eje y en {b}: {c}.", img)
    k = rnd.choice([v for v in range(-4, 5) if v not in (xa, xb)])
    val = m * k + b
    c, w = numeric_options(val, [-val, m + k, b - m * k], step=1, positive=False)
    return make(ALGEBRA, f"La recta del gráfico tiene ecuación {line_str(m, b)}. ¿Cuánto vale y cuando x = {fint(k)}?", c, w, f"y = {m}·({k}) + ({b}) = {val}.", img)


def g_triangle():
    a, b, h = rnd.choice(TRIPLES)
    k = rnd.randint(1, 3) if h < 20 else 1
    a, b, h = a * k, b * k, h * k
    unknown = rnd.choice(["h", "a"])
    fig, ax = plt.subplots(figsize=(4.4, 3.4))
    ax.add_patch(Polygon([(0, 0), (b, 0), (0, a)], closed=True, fill=False, lw=2, color="#1f77b4"))
    s = max(a, b) * 0.07
    ax.add_patch(Polygon([(0, 0), (s, 0), (s, s), (0, s)], closed=True, fill=False, lw=1))
    ax.text(b / 2, -max(a, b) * 0.09, f"{b} cm", ha="center")
    if unknown == "h":
        ax.text(-max(a, b) * 0.05, a / 2, f"{a} cm", ha="right", va="center")
        ax.text(b / 2 + max(a, b) * 0.04, a / 2 + max(a, b) * 0.04, "x", ha="left", fontsize=13, color="#d62728")
    else:
        ax.text(-max(a, b) * 0.05, a / 2, "x", ha="right", va="center", fontsize=13, color="#d62728")
        ax.text(b / 2 + max(a, b) * 0.04, a / 2 + max(a, b) * 0.04, f"{h} cm", ha="left")
    ax.set_xlim(-max(a, b) * 0.3, b + max(a, b) * 0.3)
    ax.set_ylim(-max(a, b) * 0.2, a + max(a, b) * 0.2)
    ax.set_aspect("equal")
    ax.axis("off")
    img = save_fig(fig)
    if unknown == "h":
        c, w = numeric_options(h, [a + b, b - a, a * b // 2], step=1)
        return make(GEOMETRIA, "El triángulo de la figura es rectángulo. ¿Cuánto mide x en centímetros?", c, w, f"x² = {a}² + {b}² = {a * a + b * b}, entonces x = {h}.", img)
    c, w = numeric_options(a, [h - b, h + b, h * b // 2], step=1)
    return make(GEOMETRIA, "El triángulo de la figura es rectángulo. ¿Cuánto mide x en centímetros?", c, w, f"x² = {h}² {MINUS} {b}² = {h * h - b * b}, entonces x = {a}.", img)


def g_lshape():
    W, H = rnd.randint(8, 16), rnd.randint(8, 16)
    w1, h1 = rnd.randint(3, W - 3), rnd.randint(3, H - 3)
    area = W * H - (W - w1) * (H - h1)
    fig, ax = plt.subplots(figsize=(4.4, 4.0))
    poly = [(0, 0), (W, 0), (W, h1), (w1, h1), (w1, H), (0, H)]
    ax.add_patch(Polygon(poly, closed=True, facecolor="#cfe3f5", edgecolor="#1f77b4", lw=2))
    ax.text(W / 2, -0.8, f"{W} cm", ha="center")
    ax.text(-0.5, H / 2, f"{H} cm", ha="right", va="center")
    ax.text(w1 / 2, H + 0.4, f"{w1} cm", ha="center")
    ax.text(W + 0.5, h1 / 2, f"{h1} cm", ha="left", va="center")
    ax.set_xlim(-4, W + 4)
    ax.set_ylim(-2.5, H + 2.5)
    ax.set_aspect("equal")
    ax.axis("off")
    img = save_fig(fig)
    c, w = numeric_options(area, [W * H, (W + H) * 2, w1 * H + h1 * W, area + w1], step=4, fn=lambda v: f"{fint(v)} cm²")
    return make(GEOMETRIA, "La figura está formada solo por ángulos rectos. ¿Cuál es su área?", c, w,
                f"Rectángulo grande {W}·{H} = {W * H}, menos el recorte {W - w1}·{H - h1} = {(W - w1) * (H - h1)}: {area} cm².", img)


def g_circle():
    r = rnd.choice([2, 4, 5, 6, 8, 10, 12])
    semi = rnd.random() < 0.5
    fig, ax = plt.subplots(figsize=(4, 3.6))
    if semi:
        ax.add_patch(Wedge((0, 0), r, 0, 180, fill=False, lw=2, color="#1f77b4"))
        ax.plot([-r, r], [0, 0], color="#1f77b4", lw=2)
        ax.plot([0, r], [0, 0], color="#d62728", lw=2)
        ax.text(r / 2, -r * 0.12, f"{r} cm", ha="center")
        ax.set_ylim(-r * 0.3, r * 1.2)
    else:
        ax.add_patch(Circle((0, 0), r, fill=False, lw=2, color="#1f77b4"))
        ax.plot([0, r], [0, 0], color="#d62728", lw=2)
        ax.text(r / 2, r * 0.07, f"{r} cm", ha="center")
        ax.set_ylim(-r * 1.2, r * 1.2)
    ax.set_xlim(-r * 1.2, r * 1.2)
    ax.set_aspect("equal")
    ax.axis("off")
    img = save_fig(fig)
    if semi:
        if r % 2:
            raise Skip()
        c, w = f"{r * r // 2}π cm²", [f"{r * r}π cm²", f"{r}π cm²", f"{r * r // 4}π cm²", f"{2 * r}π cm²"]
        return make(GEOMETRIA, "La figura es un semicírculo cuyo radio (en rojo) mide lo indicado. ¿Cuál es su área?", c, w, f"Área = πr²/2 = π·{r * r}/2 = {r * r // 2}π cm².", img)
    c, w = f"{r * r}π cm²", [f"{2 * r}π cm²", f"{r}π cm²", f"{2 * r * r}π cm²", f"{4 * r * r}π cm²"]
    return make(GEOMETRIA, "El círculo de la figura tiene el radio (en rojo) indicado. ¿Cuál es su área?", c, w, f"A = πr² = π·{r}² = {r * r}π cm².", img)


def g_contingency():
    sexo = ["Mujeres", "Hombres"]
    dep = rnd.choice([["Fútbol", "Básquetbol", "Vóleibol"], ["Música", "Teatro", "Pintura"], ["Inglés", "Francés", "Alemán"]])
    cells = [[rnd.randint(4, 25) for _ in dep] for _ in sexo]
    rt = [sum(r) for r in cells]
    ct = [sum(cells[i][j] for i in range(2)) for j in range(3)]
    N = sum(rt)
    fig, ax = plt.subplots(figsize=(7.4, 3.0))
    ax.axis("off")
    rows = [[sexo[i]] + [str(v) for v in cells[i]] + [str(rt[i])] for i in range(2)]
    rows.append(["Total"] + [str(v) for v in ct] + [str(N)])
    tbl = ax.table(cellText=rows, colLabels=[""] + dep + ["Total"], loc="center", cellLoc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(11)
    tbl.set_fontsize(14)
    tbl.scale(1, 2.0)
    tbl.auto_set_column_width(list(range(5)))
    img = save_fig(fig)
    kind = rnd.choice(["one", "both"])
    i, j = rnd.randrange(2), rnd.randrange(3)
    if kind == "one":
        res = Fraction(rt[i], N)
        cands = [Fraction(ct[j], N), Fraction(cells[i][j], N), Fraction(cells[i][j], rt[i]), Fraction(rt[1 - i], N)]
        txt = f"sea de \"{sexo[i]}\" "
        q = f"Según la tabla, si se elige una persona al azar, ¿cuál es la probabilidad de que sea de \"{sexo[i]}\"?"
        ex = f"Casos favorables {rt[i]}; casos totales {N}."
    else:
        res = Fraction(cells[i][j], N)
        cands = [Fraction(cells[i][j], rt[i]), Fraction(cells[i][j], ct[j]), Fraction(rt[i], N), Fraction(ct[j], N)]
        q = f"Según la tabla, si se elige una persona al azar, ¿cuál es la probabilidad de que pertenezca a \"{sexo[i]}\" y a \"{dep[j]}\"?"
        ex = f"Casos favorables {cells[i][j]}; casos totales {N}."
    w = [frac_str(x) for x in cands if x != res and 0 < x <= 1]
    w += [frac_str(Fraction(1, N)), frac_str(Fraction(N - 1, N)), frac_str(Fraction(1, 2))]
    return make(PROBA, q, frac_str(res), [x for x in w if x != frac_str(res)], ex + f" P = {frac_str(res)}.", img)


def g_parabola():
    a = rnd.choice([1, 1, -1])
    r1, r2 = sorted(rnd.sample(range(-5, 6), 2))
    if (r1 + r2) % 2:
        raise Skip()
    h = (r1 + r2) // 2
    k = a * (h - r1) * (h - r2)
    c0 = a * r1 * r2
    if abs(k) > 9 or abs(c0) > 12:
        raise Skip()
    xs = [x / 20 for x in range(-140, 141)]
    ys = [a * (x - r1) * (x - r2) for x in xs]
    fig, ax = plt.subplots(figsize=(4.6, 4.6))
    ax.plot(xs, ys, color="#1f77b4", lw=2)
    ax.set_xlim(-7, 7)
    ax.set_ylim(-10, 10)
    ax.set_xticks(range(-6, 7, 1))
    ax.set_yticks(range(-10, 11, 2))
    ax.tick_params(labelsize=8)
    ax.grid(alpha=0.4)
    ax.axhline(0, color="black", lw=1)
    ax.axvline(0, color="black", lw=1)
    ax.text(7.1, 0.0, "x", fontsize=12, va="center")
    ax.text(0.0, 10.4, "y", fontsize=12, ha="center")
    for px, py in ((r1, 0), (r2, 0), (h, k), (0, c0)):
        ax.plot(px, py, "o", color="#d62728", ms=5)
    img = save_fig(fig)
    kind = rnd.choice(["vertex", "zeros", "yint", "axis", "sign"])
    if kind == "vertex":
        corr = pt(h, k)
        return make(ALGEBRA, "El gráfico muestra una parábola. ¿Cuáles son las coordenadas de su vértice?", corr,
                    [pt(-h, k), pt(h, -k), pt(k, h), pt(0, c0) if (0, c0) != (h, k) else pt(h + 1, k)],
                    f"El vértice es el punto más {'bajo' if a > 0 else 'alto'} de la parábola: {corr}.", img)
    if kind == "zeros":
        s_ = lambda u, v: f"x = {fint(u)} y x = {fint(v)}"
        return make(ALGEBRA, "Según el gráfico, ¿cuáles son los ceros de la función cuadrática representada?", s_(r1, r2),
                    [s_(-r2, -r1), s_(h, k), s_(0, c0), s_(r1 - 1, r2 + 1)],
                    f"Los ceros son los valores de x donde la parábola corta al eje x: {fint(r1)} y {fint(r2)}.", img)
    if kind == "yint":
        c, w = numeric_options(c0, [k, -c0, r1 * r2 if a < 0 else -r1 * r2], step=1, positive=False, fn=lambda v: pt(0, v))
        return make(ALGEBRA, "Según el gráfico, ¿en qué punto la parábola corta al eje y?", c, w,
                    f"Se lee la intersección con el eje y: {pt(0, c0)}.", img)
    if kind == "axis":
        c, w = numeric_options(h, [k, r1, r2, -h], step=1, positive=False, fn=lambda v: f"x = {fint(v)}")
        return make(ALGEBRA, "¿Cuál es la ecuación del eje de simetría de la parábola del gráfico?", c, w,
                    f"El eje de simetría pasa por el vértice: x = {fint(h)} (el punto medio entre los ceros {fint(r1)} y {fint(r2)}).", img)
    ans = "a es negativo, porque la parábola abre hacia abajo" if a < 0 else "a es positivo, porque la parábola abre hacia arriba"
    w = ["a es negativo, porque la parábola abre hacia arriba", "a es positivo, porque la parábola abre hacia abajo",
         "a es cero, porque la gráfica es una parábola", "a es negativo, porque abre hacia abajo" if a > 0 else "a es positivo, porque abre hacia arriba"]
    return make(ALGEBRA, "Si la parábola del gráfico corresponde a f(x) = ax² + bx + c, ¿qué se puede afirmar del coeficiente a?", ans, w,
                "Si a > 0 la parábola abre hacia arriba; si a < 0, abre hacia abajo.", img)


def g_boxplot():
    data = quartile_data()
    mn, q1, med, q3, mx = data[0], data[1], (data[3] + data[4]) // 2, data[5], data[7]
    fig, ax = plt.subplots(figsize=(6, 2.6))
    ax.boxplot([data], orientation="horizontal", widths=0.5, whis=(0, 100), patch_artist=True,
               boxprops=dict(facecolor="#cfe3f7", color="#1f4e9c"), medianprops=dict(color="#d62728", lw=2))
    ticks = sorted({mn, q1, med, q3, mx})
    ax.set_xticks(ticks)
    ax.set_yticks([])
    ax.grid(axis="x", alpha=0.4)
    tema = rnd.choice(["Edades de los asistentes (años)", "Puntajes de una prueba", "Minutos de viaje al colegio", "Horas de uso del celular en una semana"])
    ax.set_xlabel(tema)
    img = save_fig(fig)
    kind = rnd.randint(1, 4)
    if kind == 1:
        c, w = numeric_options(med, [q1, q3, (mn + mx) // 2 if (mn + mx) // 2 != med else mx], step=1)
        return make(PROBA, "El diagrama de cajón resume un conjunto de datos. ¿Cuál es la mediana?", c, w,
                    f"La mediana es la línea dentro de la caja: {med}.", img)
    if kind == 2:
        c, w = numeric_options(q3 - q1, [mx - mn, q3, med - q1 if med - q1 != q3 - q1 else q1], step=1)
        return make(PROBA, "Según el diagrama de cajón, ¿cuál es el rango intercuartil (Q₃ − Q₁)?", c, w,
                    f"La caja va de Q₁ = {q1} a Q₃ = {q3}: {q3} − {q1} = {q3 - q1}.", img)
    if kind == 3:
        return make(PROBA, f"Según el diagrama de cajón, ¿qué porcentaje aproximado de los datos es mayor que {q3}?", "25%",
                    ["50%", "75%", "10%", "100%"], f"{q3} es el tercer cuartil: sobre él queda el 25% de los datos.", img)
    c, w = numeric_options(q1, [mn, med, q3], step=1)
    return make(PROBA, "Según el diagrama de cajón, ¿cuál es el primer cuartil (Q₁)?", c, w,
                f"Q₁ es el borde izquierdo de la caja: {q1}.", img)


GRAPH_PLAN = [(g_bar, 12), (g_line, 10), (g_pie, 10), (g_freq_table, 10), (g_cartesian, 12),
              (g_triangle, 8), (g_lshape, 6), (g_circle, 6), (g_contingency, 8), (g_parabola, 10), (g_boxplot, 8)]


# =================================================================== MAIN
def clean_images():
    if os.path.isdir(IMG_DIR):
        for f in os.listdir(IMG_DIR):
            if f.endswith(".png"):
                os.remove(os.path.join(IMG_DIR, f))


def build():
    clean_images()
    seen = set()
    out = []

    # Preguntas de texto: se reparten en partes iguales entre las plantillas.
    counts = {t: 0 for t in TEXT_TEMPLATES}
    i = 0
    guard = 0
    while sum(counts.values()) < N_TEXT:
        t = TEXT_TEMPLATES[i % len(TEXT_TEMPLATES)]
        i += 1
        guard += 1
        if guard > 100000:
            raise RuntimeError("No se logró completar las preguntas de texto.")
        for _ in range(60):
            try:
                q = t()
            except (Skip, ZeroDivisionError):
                continue
            key = q["enunciado"]
            if key in seen:
                continue
            seen.add(key)
            out.append(q)
            counts[t] += 1
            break

    # Preguntas con gráfico.
    for fn, n in GRAPH_PLAN:
        made = 0
        tries = 0
        while made < n:
            tries += 1
            if tries > 500:
                raise RuntimeError(f"No se pudo completar {fn.__name__}")
            before = _img_counter[0]
            try:
                q = fn()
            except (Skip, ZeroDivisionError):
                # Si se alcanzó a guardar una imagen, se descarta.
                if _img_counter[0] > before:
                    p = os.path.join(IMG_DIR, f"m1_img_{_img_counter[0]:03d}.png")
                    if os.path.exists(p):
                        os.remove(p)
                    _img_counter[0] -= 1
                continue
            key = q["enunciado"] + "|" + q.get("imagen", "")
            out.append(q)
            made += 1

    rnd.shuffle(out)
    for n, q in enumerate(out, 1):
        q["id"] = f"m1_{n:03d}"
    ordered = []
    for q in out:
        ordered.append({"id": q["id"], "prueba": q["prueba"], "eje": q["eje"], "enunciado": q["enunciado"],
                        "alternativas": q["alternativas"], "correcta": q["correcta"],
                        "explicacion": q["explicacion"], **({"imagen": q["imagen"]} if "imagen" in q else {})})
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(ordered, f, ensure_ascii=False, indent=1)
    return ordered


def validate(qs):
    assert len(qs) == N_TEXT + N_GRAPH, len(qs)
    ids = set()
    for q in qs:
        assert q["id"] not in ids
        ids.add(q["id"])
        assert len(q["alternativas"]) == 4 and len(set(q["alternativas"])) == 4, q
        assert 0 <= q["correcta"] < 4
        if "imagen" in q:
            assert os.path.exists(os.path.join(ROOT, q["imagen"])), q["imagen"]
    n_img = sum(1 for q in qs if "imagen" in q)
    assert n_img == N_GRAPH, n_img
    print(f"OK: {len(qs)} preguntas, {n_img} con gráfico, {len(os.listdir(IMG_DIR))} imágenes.")


if __name__ == "__main__":
    qs = build()
    validate(qs)
