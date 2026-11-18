#!/usr/bin/env python3
"""Genera las 500 preguntas originales de Matemática M2 (400 de texto + 100 con gráfico).

Cubre los temas propios de M2: raíces y potencias racionales, logaritmos, matemática
financiera, sistemas 2x2 (tipo de solución), funciones exponencial, logarítmica,
potencia, seno y coseno, razones trigonométricas, circunferencia (ángulos, cuerdas,
secantes), esfera, homotecia, rectas en el plano, dispersión, probabilidad
condicional, combinatoria, modelo binomial y distribución normal.

Igual que en M1: cada respuesta la CALCULA el programa y cada gráfico se dibuja con
los mismos datos de la pregunta. No usa contenido del DEMRE.

Uso (desde la carpeta del proyecto):
    PYTHONPATH=<carpeta con matplotlib> python3 tools/generar_m2.py
Escribe: assets/questions/m2.json y assets/images/m2/*.png
"""
import json
import math
import os
import random
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generar_m1 as base  # noqa: E402  (reutiliza formato y armado de alternativas)
import m2_suficiencia  # noqa: E402
from generar_m1 import (  # noqa: E402
    MINUS, Skip, TRIPLES, fint, fmt, money, frac_str, sup, pt, line_str, numeric_options,
)

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Polygon, Circle, Ellipse, Arc  # noqa: E402
import numpy as np  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(ROOT, "assets", "images", "m2")
OUT_JSON = os.path.join(ROOT, "assets", "questions", "m2.json")
N_TEXT = 400
# De las 400 de texto, estas son de suficiencia de datos (5 opciones en orden fijo).
N_SUFICIENCIA = 40
N_GRAPH = 100

rnd = random.Random(20261118)
base.rnd = rnd  # `make` de M1 mezcla las alternativas con este mismo generador.

NUMEROS = "Números"
ALGEBRA = "Álgebra y funciones"
GEOMETRIA = "Geometría"
PROBA = "Probabilidad y estadística"
SQFREE = [2, 3, 5, 6, 7, 10, 11]
SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
NOMBRES = base.NOMBRES


def make(eje, enunciado, correct, wrongs, explicacion, imagen=None):
    q = base.make(eje, enunciado, correct, wrongs, explicacion, imagen)
    q["prueba"] = "m2"
    return q


def nm():
    return rnd.choice(NOMBRES)


def fs(f):
    return frac_str(Fraction(f)).replace("-", MINUS)


def frac_opts(correct, cands):
    correct = Fraction(correct)
    pool = list(cands) + [correct * 2, correct / 2, 1 - correct, correct + Fraction(1, 10), correct + Fraction(1, 4)]
    out = []
    for c in pool:
        c = Fraction(c)
        s = fs(c)
        if c != correct and 0 < c <= 1 and s not in out:
            out.append(s)
    return fs(correct), out


def rad(a, b):
    if b == 1:
        return fint(a)
    return f"√{b}" if a == 1 else f"{fint(a)}√{b}"


def lg(b):
    return "log" + str(b).translate(SUB)


def term(v, var, first):
    if v == 0:
        return ""
    if first:
        sign = MINUS if v < 0 else ""
    else:
        sign = f" {MINUS} " if v < 0 else " + "
    av = abs(v)
    body = var if (av == 1 and var) else f"{fint(av)}{var}"
    return sign + body


def lin2(a, b, c):
    """'2x + 3y = 7'."""
    left = (term(a, "x", True) + term(b, "y", not a)) or "0"
    return f"{left} = {fint(c)}"


def sq(var, h):
    if h == 0:
        return f"{var}²"
    return f"({var} {MINUS if h > 0 else '+'} {abs(h)})²"


def deg(v):
    return f"{fmt(v)}°"


def pct(v):
    return f"{fmt(v)}%"


# ===================================================== NÚMEROS
def t_simplify_root():
    a, b = rnd.randint(2, 9), rnd.choice(SQFREE)
    n = a * a * b
    w = [rad(a + 1, b), rad(a - 1, b), rad(a * a, b), rad(2 * a, b), rad(b, a) if a in SQFREE else rad(a, b + 1)]
    return make(NUMEROS, f"Al simplificar √{n} se obtiene:", rad(a, b), w,
                f"√{n} = √({a * a} · {b}) = {a}√{b}.")


def t_sum_roots():
    b = rnd.choice(SQFREE[:5])
    p, q = rnd.sample(range(1, 7), 2)
    op = rnd.choice(["+", MINUS])
    res = p + q if op == "+" else p - q
    if res == 0:
        raise Skip()
    c = (MINUS if res < 0 else "") + rad(abs(res), b)
    w = [f"√{p * p * b + q * q * b}" if op == "+" else f"√{abs(p * p * b - q * q * b)}", rad(p * q, b), rad(abs(res), 2 * b),
         rad(abs(res) + 1, b), (MINUS if res > 0 else "") + rad(abs(res), b)]
    return make(NUMEROS, f"¿Cuál es el resultado de √{p * p * b} {op} √{q * q * b}?", c, w,
                f"√{p * p * b} = {rad(p, b)} y √{q * q * b} = {rad(q, b)}; entonces {rad(p, b)} {op} {rad(q, b)} = {c}.")


def t_rationalize():
    b = rnd.choice(SQFREE)
    m = rnd.randint(1, 6)
    k = m * b
    w = [rad(k, b), fint(k), rad(m + 1, b), f"{k}/{b}", rad(m, b + 1)]
    return make(NUMEROS, f"Al racionalizar la expresión {k}/√{b} se obtiene:", rad(m, b), w,
                f"{k}/√{b} · √{b}/√{b} = {k}√{b}/{b} = {rad(m, b)}.")


def t_rational_exp():
    c, q = rnd.choice([(2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (2, 3), (3, 3), (4, 3), (2, 4), (3, 4)])
    p = rnd.choice([x for x in (1, 2, 3, 5) if x != q])
    base_ = c ** q
    v = c ** p
    if v > 10000:
        raise Skip()
    cs, ws = numeric_options(v, [base_ * p // q, c ** (p + 1), c * p, base_ ** p // (q * 100) or 7], step=c)
    return make(NUMEROS, f"¿Cuál es el valor de {base_}^({p}/{q})?", cs, ws,
                (f"{base_}^({p}/{q}) = {'' if q == 2 else sup(q)}√{base_} = {c}." if p == 1 else
                 f"{base_}^({p}/{q}) = ({'' if q == 2 else sup(q)}√{base_}){sup(p)} = {c}{sup(p)} = {fint(v)}."))


def t_log_eval():
    b = rnd.choice([2, 3, 4, 5, 10])
    kind = rnd.randint(1, 3)
    if kind == 1:
        k = rnd.randint(1, 6 if b < 5 else 4)
        arg, v, ex = fint(b ** k), k, f"{b}{sup(k)} = {fint(b ** k)}, entonces el logaritmo es {k}."
    elif kind == 2:
        k = rnd.randint(1, 4)
        arg, v, ex = f"1/{fint(b ** k)}", -k, f"1/{fint(b ** k)} = {b}^({MINUS}{k}), entonces el logaritmo es {MINUS}{k}."
    else:
        k = rnd.randint(1, 3)
        arg, v, ex = rad(1, b) if k == 1 and b in SQFREE else None, Fraction(1, 2), f"√{b} = {b}^(1/2), entonces el logaritmo es 1/2."
        if arg is None:
            raise Skip()
        return make(NUMEROS, f"¿Cuál es el valor de {lg(b)}(√{b})?", "1/2", ["2", f"{MINUS}1/2", "1", f"{b}/2"], ex)
    cs, ws = numeric_options(v, [-v, v + 1, b * v if b * v != v else v + 2, v - 1], step=1, positive=False)
    return make(NUMEROS, f"¿Cuál es el valor de {lg(b)}({arg})?", cs, ws, ex)


def t_log_props():
    b = rnd.choice([2, 3, 5, 6, 10])
    k = rnd.randint(2, 4)
    N = b ** k
    divs = [d for d in range(2, N) if N % d == 0]
    if not divs:
        raise Skip()
    if rnd.random() < 0.5:
        x = rnd.choice(divs)
        y = N // x
        enun = f"¿Cuál es el valor de {lg(b)}({fint(x)}) + {lg(b)}({fint(y)})?"
        ex = f"{lg(b)}({x}) + {lg(b)}({y}) = {lg(b)}({x}·{y}) = {lg(b)}({fint(N)}) = {k}."
        wr = [k + 1, k - 1, 2 * k, x + y]
    else:
        m = rnd.choice([v for v in range(2, 10) if v % b])
        enun = f"¿Cuál es el valor de {lg(b)}({fint(N * m)}) {MINUS} {lg(b)}({m})?"
        ex = f"{lg(b)}({fint(N * m)}) {MINUS} {lg(b)}({m}) = {lg(b)}({fint(N * m)}/{m}) = {lg(b)}({fint(N)}) = {k}."
        wr = [k + 1, k - 1, m, N]
    cs, ws = numeric_options(k, wr, step=1)
    return make(NUMEROS, enun, cs, ws, ex)


def t_log_eq():
    b = rnd.choice([2, 3, 4, 5, 10])
    k = rnd.randint(1, 4 if b < 5 else 3)
    c = rnd.choice([v for v in range(-6, 10) if v])
    x = b ** k - c
    inside = f"x {'+' if c > 0 else MINUS} {abs(c)}"
    cs, ws = numeric_options(x, [b * k - c, b ** k + c, k ** b - c if k ** b < 10 ** 6 else x + b], step=b, positive=False)
    return make(NUMEROS, f"Si {lg(b)}({inside}) = {k}, ¿cuál es el valor de x?", cs, ws,
                f"Por definición de logaritmo: {inside} = {b}{sup(k)} = {fint(b ** k)}, entonces x = {fint(x)}.")


def t_exp_eq():
    b = rnd.choice([2, 3, 5])
    k = rnd.randint(2, 6 if b == 2 else 4)
    a = rnd.choice([1, 1, 2, 3])
    c = rnd.randint(-3, 4)
    if (k - c) % a:
        raise Skip()
    x = (k - c) // a
    ax = "x" if a == 1 else f"{a}x"
    expo = ax if c == 0 else f"{ax} {'+' if c > 0 else MINUS} {abs(c)}"
    cs, ws = numeric_options(x, [k, (k + c) // a if (k + c) % a == 0 else k + 1, x + 1, x - 1], step=1, positive=False)
    return make(NUMEROS, f"¿Cuál es el valor de x en la ecuación {b}^({expo}) = {fint(b ** k)}?", cs, ws,
                f"{fint(b ** k)} = {b}{sup(k)}; igualando exponentes: {expo} = {k}, entonces x = {fint(x)}.")


def t_compound():
    r, t, mult = rnd.choice([(10, 2, 1000), (10, 3, 1000), (20, 2, 1000), (20, 3, 1000), (5, 2, 10000), (50, 2, 1000)])
    C = mult * rnd.randint(10, 300)
    F = C * (100 + r) ** t // 100 ** t
    simple = C + C * r * t // 100
    ctx = rnd.choice(["Se invierten", "Se depositan en una cuenta de ahorro", "Una persona ahorra"])
    cs, ws = numeric_options(F, [simple, C * r * t // 100, F - C, F + C * r // 100], step=C // 20, fn=money)
    return make(NUMEROS, f"{ctx} {money(C)} con un interés compuesto de {r}% anual. ¿Cuál es el monto total después de {t} años?", cs, ws,
                f"Monto = C·(1 + r)ᵗ = {money(C)} · ({fmt(1 + r / 100)}){sup(t)} = {money(F)}.")


def t_credit():
    P = rnd.randrange(500000, 5000001, 100000)
    n = rnd.choice([6, 10, 12, 18, 24, 36])
    Q = rnd.randrange(int(P / n * 1.05) // 1000 * 1000 + 1000, int(P / n * 1.4) // 1000 * 1000 + 1000, 1000)
    tot = Q * n
    if rnd.random() < 0.5:
        cs, ws = numeric_options(tot - P, [tot, Q, P // n, tot - P + Q], step=Q, fn=money)
        return make(NUMEROS, f"{nm()} pide un crédito de consumo de {money(P)} y lo paga en {n} cuotas mensuales de {money(Q)}. ¿Cuánto paga en total por intereses y costos?", cs, ws,
                    f"Total pagado = {n} · {money(Q)} = {money(tot)}. Intereses = {money(tot)} {MINUS} {money(P)} = {money(tot - P)}.")
    cs, ws = numeric_options(tot, [tot - P, P + Q, Q * (n - 1)], step=Q, fn=money)
    return make(NUMEROS, f"Un crédito se paga en {n} cuotas mensuales iguales de {money(Q)}. ¿Cuánto se paga en total al terminar el crédito?", cs, ws,
                f"Total = {n} · {money(Q)} = {money(tot)}.")


def t_mortgage():
    """Crédito hipotecario: pie y total pagado."""
    V = rnd.randrange(60, 201, 5) * 1000000
    pie_pct = rnd.choice([10, 20, 25, 30])
    pie = V * pie_pct // 100
    prestamo = V - pie
    if rnd.random() < 0.5:
        cs, ws = numeric_options(pie, [prestamo, V // 10 if pie_pct != 10 else V // 5, pie * 2], step=V // 20, fn=money)
        return make(NUMEROS, f"Para comprar una vivienda de {money(V)}, un banco entrega un crédito hipotecario por el {100 - pie_pct}% del valor. "
                    "El resto lo debe pagar el comprador al contado (el «pie»). ¿Cuánto es el pie?", cs, ws,
                    f"El pie es el {pie_pct}% de {money(V)}: {money(pie)}.")
    anos = rnd.choice([15, 20, 25, 30])
    Q = rnd.randrange(int(prestamo / (anos * 12) * 1.4) // 10000 * 10000 + 10000,
                      int(prestamo / (anos * 12) * 2.0) // 10000 * 10000 + 20000, 10000)
    tot = Q * 12 * anos
    cs, ws = numeric_options(tot - prestamo, [tot, Q * 12, prestamo], step=Q * 12, fn=money)
    return make(NUMEROS, f"Una familia pide un crédito hipotecario de {money(prestamo)} y lo paga en {anos} años con cuotas mensuales fijas de {money(Q)}. "
                "¿Cuánto paga en total por intereses y otros costos del crédito?", cs, ws,
                f"Total pagado = {money(Q)}·12·{anos} = {money(tot)}. Intereses y costos = {money(tot)} {MINUS} {money(prestamo)} = {money(tot - prestamo)}.")


def t_afp():
    S = rnd.randrange(500000, 2500001, 10000)
    if (S * 10) % 100:
        raise Skip()
    m = S // 10
    if rnd.random() < 0.5:
        cs, ws = numeric_options(m, [S // 100, S - m, m * 12, S // 5], step=10000, fn=money)
        return make(NUMEROS, f"En Chile, la cotización obligatoria para la AFP es el 10% del sueldo imponible. Si el sueldo imponible de {nm()} es {money(S)}, ¿cuánto se cotiza al mes?", cs, ws,
                    f"10% de {money(S)} = {money(m)}.")
    cs, ws = numeric_options(m * 12, [m, S * 12, m * 10, S], step=m, fn=money)
    return make(NUMEROS, f"La cotización obligatoria para la AFP es el 10% del sueldo imponible. Si una persona gana {money(S)} imponibles todos los meses, ¿cuánto cotiza en un año?", cs, ws,
                f"Al mes: {money(m)}. En 12 meses: {money(m * 12)}.")


# ===================================================== ÁLGEBRA
def t_system_type():
    a, b = rnd.choice([v for v in range(-6, 7) if v]), rnd.choice([v for v in range(-6, 7) if v])
    c = rnd.randint(-12, 12)
    k = rnd.choice([2, 3, -2, 4])
    kind = rnd.randint(1, 3)
    if kind == 1:
        e2 = lin2(k * a, k * b, k * c)
        ans, ex = "Infinitas soluciones", f"La segunda ecuación es la primera multiplicada por {k}: son la misma recta."
    elif kind == 2:
        e2 = lin2(k * a, k * b, k * c + rnd.choice([1, 2, 3, -1, -5]))
        ans, ex = "No tiene solución", "Los coeficientes de x e y son proporcionales pero el término libre no: son rectas paralelas distintas."
    else:
        a2, b2 = rnd.choice([v for v in range(-6, 7) if v]), rnd.choice([v for v in range(-6, 7) if v])
        if a * b2 == a2 * b:
            raise Skip()
        e2 = lin2(a2, b2, rnd.randint(-12, 12))
        ans, ex = "Una única solución", "Los coeficientes de x e y no son proporcionales: las rectas se cortan en un solo punto."
    opts = ["Una única solución", "Infinitas soluciones", "No tiene solución", "Exactamente dos soluciones"]
    return make(ALGEBRA, f"¿Cuántas soluciones tiene el sistema formado por {lin2(a, b, c)} y {e2}?", ans, [o for o in opts if o != ans], ex)


def t_system_solve():
    x, y = rnd.randint(-6, 8), rnd.randint(-6, 8)
    a1, b1, a2, b2 = [rnd.choice([v for v in range(-5, 6) if v]) for _ in range(4)]
    if a1 * b2 == a2 * b1:
        raise Skip()
    c1, c2 = a1 * x + b1 * y, a2 * x + b2 * y
    ask = rnd.choice(["x", "y", "x + y"])
    v = {"x": x, "y": y, "x + y": x + y}[ask]
    cs, ws = numeric_options(v, [y if ask == "x" else x, x - y, -v, c1], step=1, positive=False)
    return make(ALGEBRA, f"Si {lin2(a1, b1, c1)} y {lin2(a2, b2, c2)}, ¿cuál es el valor de {ask}?", cs, ws,
                f"Resolviendo el sistema se obtiene x = {fint(x)} e y = {fint(y)}.")


def t_exp_growth():
    if rnd.random() < 0.55:
        N0 = rnd.choice([50, 100, 200, 250, 300, 500, 1000])
        h = rnd.choice([1, 2, 3, 4, 6])
        n = rnd.randint(2, 6)
        v = N0 * 2 ** n
        cs, ws = numeric_options(v, [N0 * 2 * n, N0 * 2 ** (n - 1), N0 * 2 ** (n + 1), N0 + 2 ** n], step=N0)
        return make(ALGEBRA, f"Un cultivo comienza con {fint(N0)} bacterias y su cantidad se duplica cada {h} {'hora' if h == 1 else 'horas'}. ¿Cuántas bacterias habrá después de {h * n} horas?", cs, ws,
                    f"En {h * n} horas hay {n} duplicaciones: {fint(N0)} · 2{sup(n)} = {fint(v)}.")
    m = rnd.choice([5, 10, 20, 25, 40])
    n = rnd.randint(2, 5)
    M0 = m * 2 ** n
    T = rnd.choice([5, 8, 10, 20, 30])
    cs, ws = numeric_options(m, [M0 // (2 * n), m * 2, M0 - m, m // 2 or 1], step=max(1, m // 5), fn=lambda v: f"{fmt(v)} g")
    return make(ALGEBRA, f"Una sustancia radiactiva reduce su masa a la mitad cada {T} años. Si hoy hay {fint(M0)} g, ¿cuántos gramos quedarán dentro de {T * n} años?", cs, ws,
                f"En {T * n} años hay {n} reducciones a la mitad: {fint(M0)} / 2{sup(n)} = {m} g.")


def t_exp_eval():
    a, b, k = rnd.choice([1, 2, 3, 5]), rnd.choice([2, 3, 4]), rnd.randint(-2, 4)
    v = Fraction(a) * Fraction(b) ** k
    fx = f"f(x) = {'' if a == 1 else f'{a}·'}{b}ˣ"
    if v.denominator != 1:
        cs, ws = fs(v), [fs(-v), fs(v * b), fs(Fraction(a * b, -k) if k else 2), fs(Fraction(1, a * b * b))]
    else:
        cs, ws = numeric_options(v, [a * b * k, (a * b) ** k if k > 0 else 3, a + b ** k], step=a)
    return make(ALGEBRA, f"Si {fx}, ¿cuál es el valor de f({fint(k)})?", cs, ws,
                f"f({fint(k)}) = {'' if a == 1 else f'{a}·'}{b}{sup(k)} = {fs(v)}.")


def t_power_fn():
    a, n = rnd.choice([1, 2, 3, 4, 5]), rnd.choice([2, 3])
    k = rnd.randint(-4, 5)
    if k in (0, 1):
        raise Skip()
    fx = f"f(x) = {'' if a == 1 else a}x{sup(n)}"
    if rnd.random() < 0.6:
        v = a * k ** n
        cs, ws = numeric_options(v, [a * k * n, (a * k) ** n, -v, a + k ** n], step=a, positive=False)
        return make(ALGEBRA, f"Si {fx}, ¿cuál es el valor de f({fint(k)})?", cs, ws, f"f({fint(k)}) = {a}·({fint(k)}){sup(n)} = {fint(v)}.")
    if n != 3:
        raise Skip()
    v = a * k ** 3
    cs, ws = numeric_options(k, [-k, k + 1, v // a // 3 if v // a // 3 != k else k + 2], step=1, positive=False)
    return make(ALGEBRA, f"Si {fx} y f(x) = {fint(v)}, ¿cuál es el valor de x?", cs, ws, f"{a}x³ = {fint(v)} → x³ = {fint(v // a)} → x = {fint(k)}.")


def t_log_fn():
    b, k, c = rnd.choice([2, 3, 10]), rnd.randint(1, 4), rnd.randint(-5, 6)
    fx = f"f(x) = {lg(b)}(x)" + ("" if c == 0 else f" {'+' if c > 0 else MINUS} {abs(c)}")
    v = k + c
    cs, ws = numeric_options(v, [k, b ** k + c, k - c, v + 1], step=1, positive=False)
    return make(ALGEBRA, f"Si {fx}, ¿cuál es el valor de f({fint(b ** k)})?", cs, ws, f"{lg(b)}({fint(b ** k)}) = {k}; luego f = {k} {'+' if c >= 0 else MINUS} {abs(c)} = {fint(v)}.")


def trig_str(A, fn, B, C):
    arg = "x" if B == 1 else f"{B}x"
    amp = "" if A == 1 else (MINUS if A == -1 else f"{fint(A)}·")
    s = f"f(x) = {amp}{fn}({arg})"
    if C:
        s += f" {'+' if C > 0 else MINUS} {abs(C)}"
    return s


def t_trig_fn():
    A, B, C = rnd.randint(1, 6), rnd.choice([1, 2, 3, 4]), rnd.randint(-4, 4)
    fn = rnd.choice(["sen", "cos"])
    f = trig_str(A, fn, B, C)
    kind = rnd.choice(["max", "min", "amp", "per"])
    if kind == "max":
        cs, ws = numeric_options(C + A, [A, C - A, A * B + C, C + 1], step=1, positive=False)
        return make(ALGEBRA, f"¿Cuál es el valor máximo de la función {f}?", cs, ws, f"{fn} varía entre −1 y 1; el máximo es {A}·1 + ({fint(C)}) = {fint(C + A)}.")
    if kind == "min":
        cs, ws = numeric_options(C - A, [-A, C + A, C, -A * B], step=1, positive=False)
        return make(ALGEBRA, f"¿Cuál es el valor mínimo de la función {f}?", cs, ws, f"El mínimo es {A}·(−1) + ({fint(C)}) = {fint(C - A)}.")
    if kind == "amp":
        cs, ws = numeric_options(A, [B, A + C if A + C != A else A + 2, 2 * A, abs(C) + A + 1], step=1)
        return make(ALGEBRA, f"¿Cuál es la amplitud de la función {f}?", cs, ws, f"La amplitud es el valor absoluto del número que multiplica a {fn}: {A}.")
    cs, ws = numeric_options(360 // B, [360 * B, 180 // B if 180 // B != 360 // B else 90, 360, 90 * B], step=30, fn=deg)
    return make(ALGEBRA, f"¿Cuál es el período de la función {f}? (x en grados)", cs, ws, f"Período = 360°/{B} = {360 // B}°.")


def t_trig_ratio():
    a, b, h = rnd.choice(TRIPLES[:5])
    k = rnd.randint(1, 3)
    which = rnd.choice(["sen", "cos", "tan"])
    vals = {"sen": Fraction(a, h), "cos": Fraction(b, h), "tan": Fraction(a, b)}
    v = vals[which]
    w = [fs(x) for k2, x in vals.items() if k2 != which] + [fs(1 / v), fs(Fraction(h, a))]
    return make(GEOMETRIA, f"En un triángulo rectángulo, el cateto opuesto al ángulo α mide {a * k} cm, el cateto adyacente mide {b * k} cm y la hipotenusa mide {h * k} cm. ¿Cuál es el valor de {which}(α)?",
                fs(v), w, {"sen": "sen = cateto opuesto / hipotenusa", "cos": "cos = cateto adyacente / hipotenusa", "tan": "tan = cateto opuesto / cateto adyacente"}[which] + f" = {fs(v)}.")


def t_special_angle():
    s = rnd.randint(2, 15)
    kind = rnd.randint(1, 4)
    if kind == 1:
        q = f"En un triángulo rectángulo, la hipotenusa mide {2 * s} cm y uno de sus ángulos agudos mide 30°. ¿Cuánto mide el cateto opuesto a ese ángulo?"
        c, w = f"{s} cm", [f"{rad(s, 3)} cm", f"{2 * s} cm", f"{rad(s, 2)} cm", f"{s * 2 * 2} cm"]
        ex = f"sen(30°) = 1/2, entonces el cateto opuesto mide {2 * s}/2 = {s} cm."
    elif kind == 2:
        q = f"En un triángulo rectángulo, la hipotenusa mide {2 * s} cm y uno de sus ángulos agudos mide 60°. ¿Cuánto mide el cateto opuesto a ese ángulo?"
        c, w = f"{rad(s, 3)} cm", [f"{s} cm", f"{rad(2 * s, 3)} cm", f"{rad(s, 2)} cm", f"{2 * s} cm"]
        ex = f"sen(60°) = √3/2, entonces el cateto opuesto mide {2 * s}·√3/2 = {rad(s, 3)} cm."
    elif kind == 3:
        q = f"Los catetos de un triángulo rectángulo isósceles miden {s} cm cada uno. ¿Cuánto mide la hipotenusa?"
        c, w = f"{rad(s, 2)} cm", [f"{2 * s} cm", f"{rad(s, 3)} cm", f"{rad(2 * s, 2)} cm", f"{s * s} cm"]
        ex = f"Los ángulos agudos miden 45°; h = {s}·√2 = {rad(s, 2)} cm."
    else:
        q = f"Una rampa forma un ángulo de 30° con el suelo y mide {2 * s} m de largo. ¿A qué altura llega?"
        c, w = f"{s} m", [f"{rad(s, 3)} m", f"{2 * s} m", f"{s * 4} m", f"{rad(s, 2)} m"]
        ex = f"altura = {2 * s}·sen(30°) = {2 * s}·1/2 = {s} m."
    return make(GEOMETRIA, q, c, w, ex)


def t_inscribed():
    # Ángulos del centro menores que 180°, como en los problemas habituales.
    cen = rnd.randrange(40, 171, 10)
    if rnd.random() < 0.5:
        cs, ws = numeric_options(cen // 2, [cen, 180 - cen // 2, 360 - cen, cen * 2], step=5, fn=deg)
        return make(GEOMETRIA, f"En una circunferencia, un ángulo del centro mide {cen}°. ¿Cuánto mide un ángulo inscrito que subtiende el mismo arco?", cs, ws,
                    f"El ángulo inscrito mide la mitad del ángulo del centro: {cen}°/2 = {cen // 2}°.")
    ins = cen // 2
    cs, ws = numeric_options(cen, [ins // 2 if ins // 2 else 5, 180 - ins, 360 - cen, ins], step=10, fn=deg)
    return make(GEOMETRIA, f"En una circunferencia, un ángulo inscrito mide {ins}°. ¿Cuánto mide el ángulo del centro que subtiende el mismo arco?", cs, ws,
                f"El ángulo del centro mide el doble: 2·{ins}° = {cen}°.")


def t_chords():
    a, b, c = rnd.randint(2, 12), rnd.randint(2, 12), rnd.randint(2, 12)
    if (a * b) % c or a * b // c == c:
        raise Skip()
    d = a * b // c
    cs, ws = numeric_options(d, [a + b - c, a * b, c * a // b if (c * a) % b == 0 else d + 2], step=1, fn=lambda v: f"{fint(v)} cm")
    return make(GEOMETRIA, f"En una circunferencia, las cuerdas AB y CD se cortan en el punto P. Si AP = {a} cm, PB = {b} cm y CP = {c} cm, ¿cuánto mide PD?", cs, ws,
                f"Por el teorema de las cuerdas: AP·PB = CP·PD → {a}·{b} = {c}·PD → PD = {d} cm.")


def t_tangent_secant():
    t = rnd.randint(3, 15)
    divs = [d for d in range(1, t) if (t * t) % d == 0]
    a = rnd.choice(divs)
    whole = t * t // a
    cs, ws = numeric_options(t, [whole - a, (whole + a) // 2, t * t // whole + t // 2, whole], step=1, fn=lambda v: f"{fint(v)} cm")
    return make(GEOMETRIA, f"Desde un punto P exterior a una circunferencia se trazan una tangente PT y una secante que corta a la circunferencia en A y B (A entre P y B). Si PA = {a} cm y PB = {whole} cm, ¿cuánto mide PT?", cs, ws,
                f"PT² = PA·PB = {a}·{whole} = {t * t}, entonces PT = {t} cm.")


def t_sphere():
    if rnd.random() < 0.5:
        r = rnd.choice([3, 6, 9, 12])
        v = 4 * r ** 3 // 3
        c, w = f"{fint(v)}π cm³", [f"{fint(4 * r * r)}π cm³", f"{fint(r ** 3)}π cm³", f"{fint(v * 2)}π cm³", f"{fint(4 * r ** 3)}π cm³"]
        return make(GEOMETRIA, f"¿Cuál es el volumen de una esfera de radio {r} cm?", c, w, f"V = (4/3)·π·r³ = (4/3)·π·{r ** 3} = {fint(v)}π cm³.")
    r = rnd.randint(2, 15)
    c, w = f"{fint(4 * r * r)}π cm²", [f"{fint(r * r)}π cm²", f"{fint(2 * r * r)}π cm²", f"{fint(8 * r)}π cm²", f"{fint(4 * r ** 3)}π cm²"]
    return make(GEOMETRIA, f"¿Cuál es el área de la superficie de una esfera de radio {r} cm?", c, w, f"A = 4·π·r² = 4·π·{r * r} = {fint(4 * r * r)}π cm².")


def t_homothety():
    kind = rnd.randint(1, 3)
    k = rnd.choice([2, 3, 4, Fraction(1, 2), Fraction(1, 3)])
    ks = fs(k)
    if kind == 1:
        x, y = rnd.randint(-6, 6), rnd.randint(-6, 6)
        if (x * k).denominator != 1 or (y * k).denominator != 1 or (x, y) == (0, 0):
            raise Skip()
        c = pt(x * k, y * k)
        w = [pt(x + k, y + k) if (x + k).denominator == 1 else pt(x * 2 + 1, y), pt(x * k, y), pt(y * k, x * k), pt(-x * k, -y * k)]
        return make(GEOMETRIA, f"Se aplica una homotecia de centro en el origen y razón {ks} al punto {pt(x, y)}. ¿Cuáles son las coordenadas del punto imagen?", c, w,
                    f"Se multiplican ambas coordenadas por {ks}: {c}.")
    if kind == 2:
        A = rnd.randint(2, 30)
        v = A * k * k
        if v.denominator != 1:
            raise Skip()
        cs, ws = numeric_options(v, [A * k if (A * k).denominator == 1 else A + 1, A * k * k * k if (A * k ** 3).denominator == 1 else A + 2, A + k * k if (A + k * k).denominator == 1 else A * 3], step=2, fn=lambda z: f"{fmt(z)} cm²")
        return make(GEOMETRIA, f"Una figura de área {A} cm² se transforma con una homotecia de razón {ks}. ¿Cuál es el área de la figura imagen?", cs, ws,
                    f"Las áreas se multiplican por el cuadrado de la razón: {A}·({ks})² = {fmt(v)} cm².")
    L = rnd.randint(2, 30)
    v = L * k
    if v.denominator != 1:
        raise Skip()
    cs, ws = numeric_options(v, [L * k * k if (L * k * k).denominator == 1 else L + 3, L + k if (L + k).denominator == 1 else L + 1, L], step=1, fn=lambda z: f"{fmt(z)} cm")
    return make(GEOMETRIA, f"Un triángulo tiene un lado de {L} cm. Si se le aplica una homotecia de razón {ks}, ¿cuánto mide el lado correspondiente en la imagen?", cs, ws,
                f"Las longitudes se multiplican por la razón: {L}·{ks} = {fmt(v)} cm.")


def t_lines_relative():
    a, b = rnd.choice([v for v in range(-6, 7) if v]), rnd.choice([v for v in range(-6, 7) if v])
    c = rnd.randint(-10, 10)
    kind = rnd.randint(1, 4)
    k = rnd.choice([2, 3, -1, -2])
    if kind == 1:
        e2, ans = lin2(k * a, k * b, k * c + rnd.choice([1, 2, -3])), "Paralelas no coincidentes"
        ex = "Tienen la misma pendiente pero distinto punto de corte con el eje y."
    elif kind == 2:
        e2, ans = lin2(k * a, k * b, k * c), "Coincidentes"
        ex = "Una ecuación es múltiplo de la otra: representan la misma recta."
    elif kind == 3:
        e2, ans = lin2(b * k, -a * k, rnd.randint(-10, 10)), "Perpendiculares"
        ex = f"Las pendientes son {fs(Fraction(-a, b))} y {fs(Fraction(b, a))}; su producto es −1."
    else:
        a2, b2 = rnd.choice([v for v in range(-6, 7) if v]), rnd.choice([v for v in range(-6, 7) if v])
        if a * b2 == a2 * b or a * a2 + b * b2 == 0:
            raise Skip()
        e2, ans = lin2(a2, b2, rnd.randint(-10, 10)), "Secantes no perpendiculares"
        ex = f"Las pendientes son {fs(Fraction(-a, b))} y {fs(Fraction(-a2, b2))}: distintas y su producto no es −1."
    opts = ["Paralelas no coincidentes", "Coincidentes", "Perpendiculares", "Secantes no perpendiculares"]
    return make(GEOMETRIA, f"¿Cuál es la posición relativa de las rectas {lin2(a, b, c)} y {e2}?", ans, [o for o in opts if o != ans], ex)


def t_perp_slope():
    m = Fraction(rnd.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]), rnd.choice([1, 1, 2, 3]))
    if m.denominator != 1 and abs(m.numerator) == 1:
        pass
    perp = -1 / m
    mstr = fs(m)
    b = rnd.randint(-6, 6)
    eq = f"y = {mstr}x" + ("" if b == 0 else f" {'+' if b > 0 else MINUS} {abs(b)}") if m.denominator == 1 else f"y = ({mstr})x" + ("" if b == 0 else f" {'+' if b > 0 else MINUS} {abs(b)}")
    eq = eq.replace("y = 1x", "y = x").replace(f"y = {MINUS}1x", f"y = {MINUS}x")
    w = [fs(m), fs(-m), fs(1 / m), fs(perp * 2)]
    return make(GEOMETRIA, f"¿Cuál es la pendiente de una recta perpendicular a {eq}?", fs(perp), w,
                f"Si dos rectas son perpendiculares, el producto de sus pendientes es −1: m = −1/({mstr}) = {fs(perp)}.")


# ===================================================== PROBABILIDAD
def t_combination():
    n, k = rnd.randint(5, 12), rnd.randint(2, 4)
    v = math.comb(n, k)
    ctx = rnd.choice([f"De un curso de {n} estudiantes se elegirá una comisión de {k} integrantes (sin cargos). ¿Cuántas comisiones distintas se pueden formar?",
                      f"Una heladería ofrece {n} sabores. ¿De cuántas maneras se puede elegir una copa con {k} sabores distintos, si el orden no importa?"])
    cs, ws = numeric_options(v, [math.perm(n, k), n * k, math.comb(n, k - 1), math.comb(n, k) + n], step=n)
    return make(PROBA, ctx, cs, ws, f"No importa el orden: C({n}, {k}) = {n}!/({k}!·{n - k}!) = {fint(v)}.")


def t_perm_k():
    n = rnd.randint(5, 12)
    k = rnd.choice([2, 3])
    v = math.perm(n, k)
    ctx = (f"En una carrera participan {n} corredores. ¿De cuántas maneras distintas se pueden repartir el primer, segundo y tercer lugar?" if k == 3 else
           f"Un club de {n} personas debe elegir un presidente y un secretario (personas distintas). ¿De cuántas maneras puede hacerlo?")
    cs, ws = numeric_options(v, [math.comb(n, k), n ** k, n * k, math.factorial(n) // 100 or n + k], step=n)
    return make(PROBA, ctx, cs, ws, f"Importa el orden: {n}·{n - 1}" + (f"·{n - 2}" if k == 3 else "") + f" = {fint(v)}.")


def t_no_replace():
    r, b = rnd.randint(2, 8), rnd.randint(2, 8)
    T = r + b
    res = Fraction(r * (r - 1), T * (T - 1))
    c, w = frac_opts(res, [Fraction(r * r, T * T), Fraction(r, T), Fraction(r - 1, T - 1), Fraction(2 * r, T * T)])
    return make(PROBA, f"Una caja tiene {r} bolitas rojas y {b} azules. Se sacan dos bolitas al azar, una tras otra y sin devolverlas. ¿Cuál es la probabilidad de que ambas sean rojas?", c, w,
                f"P = {r}/{T} · {r - 1}/{T - 1} = {fs(res)}.")


def t_conditional():
    B = rnd.choice([20, 25, 40, 50, 60, 80])
    cond = rnd.choice([10, 20, 25, 30, 40, 50, 60, 75])
    if (B * cond) % 100:
        raise Skip()
    inter = B * cond // 100
    cs, ws = numeric_options(Fraction(cond, 100), [Fraction(inter * B, 10000), Fraction(inter + B, 100), Fraction(100 - cond, 100), Fraction(inter, 100)], step=Fraction(1, 20))
    return make(PROBA, f"Para dos eventos A y B se sabe que P(B) = {fmt(B / 100)} y P(A ∩ B) = {fmt(inter / 100)}. ¿Cuál es el valor de P(A | B)?", cs, ws,
                f"P(A | B) = P(A ∩ B)/P(B) = {fmt(inter / 100)}/{fmt(B / 100)} = {fmt(cond / 100)}.")


def t_conditional_count():
    total = rnd.randrange(40, 201, 10)
    A = rnd.randrange(10, total - 9, 5)
    both = rnd.randrange(2, A - 1)
    res = Fraction(both, A)
    c, w = frac_opts(res, [Fraction(both, total), Fraction(A, total), Fraction(A - both, A), Fraction(both, total - A)])
    plural, sing = rnd.choice([("practican deporte", "practica deporte"), ("usan transporte público", "usa transporte público"),
                               ("tienen mascota", "tiene mascota"), ("leen todos los días", "lee todos los días")])
    simp = "" if f"{both}/{A}" == fs(res) else f" = {fs(res)}"
    return make(PROBA, f"En un grupo de {total} personas, {A} {plural} y, de ellas, {both} son menores de 18 años. Si se elige al azar una persona que {sing}, ¿cuál es la probabilidad de que sea menor de 18 años?",
                c, w, f"Se consideran solo las {A} personas que {plural}: P = {both}/{A}{simp}.")


def t_binomial():
    n = rnd.randint(3, 6)
    k = rnd.randint(1, n - 1)
    res = Fraction(math.comb(n, k), 2 ** n)
    c, w = frac_opts(res, [Fraction(k, n), Fraction(1, 2 ** n), Fraction(math.comb(n, k), n * 2), Fraction(1, 2)])
    obj = rnd.choice(["una moneda", "una moneda equilibrada"])
    return make(PROBA, f"Se lanza {obj} {n} veces. ¿Cuál es la probabilidad de obtener exactamente {k} {'cara' if k == 1 else 'caras'}?", c, w,
                f"Modelo binomial: C({n},{k})·(1/2){sup(n)} = {math.comb(n, k)}/{2 ** n}" + ("" if f"{math.comb(n, k)}/{2 ** n}" == fs(res) else f" = {fs(res)}") + ".")


def t_binomial_p():
    n, k = rnd.choice([(2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 2)])
    p = rnd.choice([Fraction(1, 3), Fraction(1, 4), Fraction(1, 5), Fraction(2, 5), Fraction(3, 10)])
    res = math.comb(n, k) * p ** k * (1 - p) ** (n - k)
    c, w = frac_opts(res, [p ** k, p ** k * (1 - p) ** (n - k), k * p, math.comb(n, k) * p ** k])
    return make(PROBA, f"La probabilidad de que un tirador acierte un disparo es {fs(p)}, y cada disparo es independiente de los demás. Si realiza {n} disparos, ¿cuál es la probabilidad de que acierte exactamente {k}?", c, w,
                f"P = C({n},{k})·({fs(p)}){sup(k)}·({fs(1 - p)}){sup(n - k)} = {fs(res)}.".replace("·(" + fs(1 - p) + ")⁰", ""))


DEVS = [[-1, 1], [-1, -1, 1, 1], [-1, -7, 1, 7], [-7, -1, 1, 7], [-2, -14, 2, 14]]


def std_data():
    d = list(rnd.choice(DEVS))
    s = rnd.randint(1, 4) if max(abs(x) for x in d) < 3 else 1
    m = rnd.randint(10, 40)
    data = [m + s * x for x in d]
    if min(data) <= 0:
        raise Skip()
    var = Fraction(sum((s * x) ** 2 for x in d), len(d))
    rnd.shuffle(data)
    return data, m, var


def t_std():
    data, m, var = std_data()
    sd = math.isqrt(int(var))
    if sd * sd != var:
        raise Skip()
    if rnd.random() < 0.5:
        cs, ws = numeric_options(sd, [var, m, max(data) - min(data), sd * 2], step=1)
        return make(PROBA, f"¿Cuál es la desviación estándar (poblacional) de los datos {', '.join(map(str, data))}?", cs, ws,
                    f"Promedio {m}; varianza = promedio de los cuadrados de las desviaciones = {fmt(var)}; desviación estándar = √{fmt(var)} = {sd}.")
    cs, ws = numeric_options(var, [sd, m, (max(data) - min(data)) ** 2 // 2, var * 2], step=1)
    return make(PROBA, f"¿Cuál es la varianza (poblacional) de los datos {', '.join(map(str, data))}?", cs, ws,
                f"Promedio {m}; se promedian los cuadrados de las desviaciones: varianza = {fmt(var)}.")


def t_dispersion_compare():
    m = rnd.randint(10, 40)
    s1, s2 = rnd.sample(range(1, 6), 2)
    A = [m - 2 * s1, m - s1, m, m + s1, m + 2 * s1]
    B = [m - 2 * s2, m - s2, m, m + s2, m + 2 * s2]
    rnd.shuffle(A)
    rnd.shuffle(B)
    ans = "El grupo A" if s1 > s2 else "El grupo B"
    opts = ["El grupo A", "El grupo B", "Ambos tienen la misma dispersión", "No se puede saber sin conocer la mediana"]
    return make(PROBA, f"Las notas de dos grupos son A: {', '.join(map(str, A))} y B: {', '.join(map(str, B))}. Ambos tienen promedio {m}. ¿Qué grupo tiene mayor desviación estándar?",
                ans, [o for o in opts if o != ans], f"Los datos de {ans.split()[-1]} están más alejados del promedio, por eso su desviación estándar es mayor.")


NORMAL_RULES = [
    ("entre μ − σ y μ + σ", "68%"), ("entre μ − 2σ y μ + 2σ", "95%"), ("por sobre μ", "50%"),
    ("por sobre μ + σ", "16%"), ("entre μ y μ + σ", "34%"), ("por debajo de μ − 2σ", "2,5%"),
    ("entre μ + σ y μ + 2σ", "13,5%"),
]
NORMAL_VALUES = ["68%", "95%", "50%", "16%", "34%", "2,5%", "13,5%", "99,7%"]


def normal_interval(desc, mu, s):
    return (desc.replace("μ − 2σ", fint(mu - 2 * s)).replace("μ + 2σ", fint(mu + 2 * s))
            .replace("μ − σ", fint(mu - s)).replace("μ + σ", fint(mu + s)).replace("μ", fint(mu)))


def t_normal():
    mu, s, ctx, unit = rnd.choice([(165, 8, "las estaturas de un grupo de adultos", "cm"), (70, 10, "los pesos de un grupo de personas", "kg"),
                                   (500, 100, "los puntajes de una prueba", "puntos"), (40, 5, "los tiempos de un trayecto", "minutos"),
                                   (1000, 50, "las masas de unos paquetes", "g"), (12, 2, "las horas de duración de unas baterías", "horas")])
    desc, ans = rnd.choice(NORMAL_RULES)
    interval = normal_interval(desc, mu, s)
    return make(PROBA, f"Si {ctx} siguen una distribución normal de media {fint(mu)} {unit} y desviación estándar {fint(s)} {unit}, ¿qué porcentaje aproximado de los datos está {interval} {unit}?",
                ans, [v for v in NORMAL_VALUES if v != ans][:6] if False else rnd.sample([v for v in NORMAL_VALUES if v != ans], 3),
                "En una distribución normal, cerca del 68% de los datos está a menos de una desviación estándar de la media y cerca del 95% a menos de dos; la curva es simétrica.")


def t_union():
    a, b = rnd.randrange(20, 75, 5), rnd.randrange(20, 75, 5)
    z = rnd.randrange(5, min(a, b), 5)
    u = a + b - z
    if u > 100:
        raise Skip()
    cs, ws = numeric_options(u, [a + b, a + b + z if a + b + z <= 100 else a + z, z, a * b // 100], step=5, fn=pct)
    return make(PROBA, f"En un grupo, el {a}% habla inglés, el {b}% habla francés y el {z}% habla ambos idiomas. ¿Qué porcentaje habla al menos uno de los dos idiomas?", cs, ws,
                f"P(A ∪ B) = P(A) + P(B) − P(A ∩ B) = {a}% + {b}% − {z}% = {u}%.")


TEXT_TEMPLATES = [
    t_simplify_root, t_sum_roots, t_rationalize, t_rational_exp, t_log_eval, t_log_props, t_log_eq, t_exp_eq,
    t_compound, t_credit, t_mortgage, t_afp,
    t_system_type, t_system_solve, t_exp_growth, t_exp_eval, t_power_fn, t_log_fn, t_trig_fn,
    t_trig_ratio, t_special_angle, t_inscribed, t_chords, t_tangent_secant, t_sphere, t_homothety, t_lines_relative, t_perp_slope,
    t_combination, t_perm_k, t_no_replace, t_conditional, t_conditional_count, t_binomial, t_binomial_p, t_std,
    t_dispersion_compare, t_normal, t_union,
]


# ===================================================== GRÁFICOS
_img = [0]


def save_fig(fig):
    _img[0] += 1
    name = f"m2_img_{_img[0]:03d}.png"
    os.makedirs(IMG_DIR, exist_ok=True)
    fig.savefig(os.path.join(IMG_DIR, name), dpi=100, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return f"assets/images/m2/{name}"


def axes_plane(ax, xr, yr, xstep=1, ystep=1):
    ax.set_xlim(*xr)
    ax.set_ylim(*yr)
    ax.set_xticks(range(math.ceil(xr[0]), math.floor(xr[1]) + 1, xstep))
    ax.set_yticks(range(math.ceil(yr[0]), math.floor(yr[1]) + 1, ystep))
    ax.grid(alpha=0.4)
    ax.axhline(0, color="black", lw=1)
    ax.axvline(0, color="black", lw=1)


def g_trig_graph():
    A, B, C = rnd.randint(1, 4), rnd.choice([1, 2]), rnd.randint(-2, 2)
    fn = rnd.choice(["sen", "cos"])
    xs = np.linspace(0, 360, 721)
    ys = C + A * (np.sin if fn == "sen" else np.cos)(np.radians(B * xs))
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.plot(xs, ys, color="#1f77b4", lw=2)
    ax.set_xlim(0, 360)
    ax.set_xticks(range(0, 361, 45 if B == 2 else 90))
    lo, hi = C - A - 1, C + A + 1
    ax.set_ylim(lo, hi)
    ax.set_yticks(range(lo, hi + 1))
    ax.grid(alpha=0.4)
    ax.axhline(0, color="black", lw=1)
    ax.set_xlabel("x (grados)")
    ax.set_ylabel("f(x)")
    img = save_fig(fig)
    kind = rnd.choice(["max", "min", "per", "fn", "fn"])
    f = trig_str(A, fn, B, C)
    if kind == "max":
        cs, ws = numeric_options(C + A, [A, C - A, C, A + 2 * abs(C) + 1], step=1, positive=False)
        return make(ALGEBRA, "El gráfico muestra una función trigonométrica. ¿Cuál es su valor máximo?", cs, ws, f"El punto más alto del gráfico está en y = {C + A}.", img)
    if kind == "min":
        cs, ws = numeric_options(C - A, [-A, C + A, C, -A - 1], step=1, positive=False)
        return make(ALGEBRA, "El gráfico muestra una función trigonométrica. ¿Cuál es su valor mínimo?", cs, ws, f"El punto más bajo del gráfico está en y = {C - A}.", img)
    if kind == "per":
        cs, ws = numeric_options(360 // B, [360 * B if B == 2 else 180, 90, 270], step=90, fn=deg)
        return make(ALGEBRA, "El gráfico muestra una función trigonométrica. ¿Cuál es su período?", cs, ws, f"La forma de la curva se repite cada {360 // B}°.", img)
    other = "cos" if fn == "sen" else "sen"
    w = [trig_str(A, other, B, C), trig_str(A, fn, 3 - B, C), trig_str(C if C > 0 and C != A else A + 1, fn, B, A if C > 0 and C != A else C)]
    if C != 0:
        w.append(trig_str(A, fn, B, -C))
    w.append(trig_str(A + 1, fn, B, C))
    return make(ALGEBRA, "¿Cuál de las siguientes funciones corresponde al gráfico? (x en grados)", f, w,
                f"Amplitud {A}, período {360 // B}°, desplazamiento vertical {C} y la curva {'parte en el centro y sube' if fn == 'sen' else 'parte en su máximo'} en x = 0: {f}.", img)


def g_exponential():
    b = rnd.choice([2, 3, Fraction(1, 2)])
    c = rnd.choice([1, 2, 3]) if b != Fraction(1, 2) else rnd.choice([4, 8])
    xs = np.linspace(-2, 3, 200)
    ys = [float(c * (b ** 0)) * float(b) ** x for x in xs]
    fig, ax = plt.subplots(figsize=(4.8, 4.4))
    ax.plot(xs, ys, color="#1f77b4", lw=2)
    p0, p1 = (0, c), (1, c * b)
    for px, py in (p0, p1):
        ax.plot(px, float(py), "o", color="#d62728")
        ax.annotate(f"({px}, {fmt(py)})", (px, float(py)), textcoords="offset points", xytext=(8, -4), fontsize=10)
    ax.set_xlim(-2.2, 3.2)
    top = max(ys) * 1.05
    ax.set_ylim(-1, min(top, 30))
    ax.grid(alpha=0.4)
    ax.axhline(0, color="black", lw=1)
    ax.axvline(0, color="black", lw=1)
    img = save_fig(fig)
    bs = fs(b) if b.__class__ is Fraction else str(b)
    bsx = f"({bs})ˣ" if isinstance(b, Fraction) else f"{bs}ˣ"
    def fstr(cc, bb):
        bbx = f"({fs(bb)})ˣ" if isinstance(bb, Fraction) else f"{bb}ˣ"
        return f"f(x) = {'' if cc == 1 else f'{cc}·'}{bbx}"
    correct = fstr(c, b)
    if rnd.random() < 0.55:
        w = [fstr(c, 3 if b == 2 else 2), fstr(c * b if c * b != c else c + 1, b) if (c * b).__class__ is int or Fraction(c * b).denominator == 1 else fstr(c + 1, b),
             f"f(x) = {c} + {bsx}", fstr(int(b) if not isinstance(b, Fraction) else 2, c) if c != 1 else fstr(c + 2, b)]
        return make(ALGEBRA, "El gráfico corresponde a una función exponencial que pasa por los puntos marcados. ¿Cuál es la función?", correct, w,
                    f"f(0) = {c} indica el coeficiente, y f(1)/f(0) = {fmt(c * b)}/{c} = {bs} indica la base.", img)
    k = rnd.choice([2, 3, -1, 4])
    v = Fraction(c) * Fraction(b) ** k
    if v.denominator == 1:
        cs, ws = numeric_options(v, [c * b * k, c + int(b * k) if (b * k).denominator == 1 else c + 5, v * 2, v + c], step=1)
    else:
        cs, ws = fs(v), [fs(v * 2), fs(-v), fs(v + 1), fs(Fraction(1, 2))]
    return make(ALGEBRA, f"El gráfico corresponde a la función f(x) = a·bˣ que pasa por los puntos marcados. ¿Cuál es el valor de f({k})?", cs, ws,
                f"Del gráfico: a = {c} y b = {bs}. Entonces f({k}) = {c}·({bs}){sup(k)} = {fs(v)}.", img)


def g_log():
    b = rnd.choice([2, 3, 4, 5])
    xs = np.linspace(0.05, b * b + 1, 400)
    ys = np.log(xs) / np.log(b)
    fig, ax = plt.subplots(figsize=(5.4, 4))
    ax.plot(xs, ys, color="#1f77b4", lw=2)
    for px, py in ((1, 0), (b, 1), (b * b, 2)):
        ax.plot(px, py, "o", color="#d62728")
        ax.annotate(f"({px}, {py})", (px, py), textcoords="offset points", xytext=(6, -14), fontsize=10)
    ax.set_xlim(-0.5, b * b + 1.5)
    ax.set_ylim(-2.5, 3)
    ax.grid(alpha=0.4)
    ax.axhline(0, color="black", lw=1)
    ax.axvline(0, color="black", lw=1)
    img = save_fig(fig)
    if rnd.random() < 0.5:
        others = [x for x in (2, 3, 4, 5, 10) if x != b]
        return make(ALGEBRA, "El gráfico corresponde a una función logarítmica que pasa por los puntos marcados. ¿Cuál es la función?",
                    f"f(x) = {lg(b)}(x)", [f"f(x) = {lg(o)}(x)" for o in rnd.sample(others, 3)],
                    f"Pasa por ({b}, 1): {lg(b)}({b}) = 1.", img)
    cs, ws = numeric_options(b ** 3, [3 * b, b * b + b, b ** 2 * 2], step=b)
    return make(ALGEBRA, "El gráfico corresponde a una función logarítmica que pasa por los puntos marcados. ¿Para qué valor de x se cumple f(x) = 3?", cs, ws,
                f"La base es {b} (pasa por ({b}, 1)); f(x) = 3 cuando x = {b}³ = {b ** 3}.", img)


def g_trig_triangle():
    a, b, h = rnd.choice(TRIPLES[:5])
    k = rnd.randint(1, 2)
    a, b, h = a * k, b * k, h * k
    fig, ax = plt.subplots(figsize=(4.8, 3.6))
    ax.add_patch(Polygon([(0, 0), (b, 0), (b, a)], closed=True, fill=False, lw=2, color="#1f77b4"))
    s = max(a, b) * 0.06
    ax.add_patch(Polygon([(b, 0), (b - s, 0), (b - s, s), (b, s)], closed=True, fill=False, lw=1))
    ang = math.degrees(math.atan2(a, b))
    ax.add_patch(Arc((0, 0), max(a, b) * 0.3, max(a, b) * 0.3, theta1=0, theta2=ang, color="#d62728"))
    ax.text(max(a, b) * 0.2, max(a, b) * 0.04, "α", color="#d62728", fontsize=13)
    M = max(a, b)
    ax.text(b / 2, -M * 0.09, f"{b} cm", ha="center")
    ax.text(b + M * 0.04, a / 2, f"{a} cm", va="center")
    ax.text(b / 2 - M * 0.08, a / 2 + M * 0.05, f"{h} cm", ha="right")
    ax.set_xlim(-M * 0.25, b + M * 0.3)
    ax.set_ylim(-M * 0.18, a + M * 0.15)
    ax.set_aspect("equal")
    ax.axis("off")
    img = save_fig(fig)
    which = rnd.choice(["sen", "cos", "tan"])
    vals = {"sen": Fraction(a, h), "cos": Fraction(b, h), "tan": Fraction(a, b)}
    v = vals[which]
    w = [fs(x) for kk, x in vals.items() if kk != which] + [fs(1 / v)]
    return make(GEOMETRIA, f"Según el triángulo rectángulo de la figura, ¿cuál es el valor de {which}(α)?", fs(v), w,
                {"sen": "sen = cateto opuesto / hipotenusa", "cos": "cos = cateto adyacente / hipotenusa", "tan": "tan = cateto opuesto / cateto adyacente"}[which] + f" = {fs(v)}.", img)


def g_circle_angle():
    cen = rnd.randrange(40, 161, 10)
    fig, ax = plt.subplots(figsize=(4.2, 4.2))
    ax.add_patch(Circle((0, 0), 1, fill=False, lw=2, color="#1f77b4"))
    ta = rnd.uniform(-60, -20)
    tb = ta + cen
    tc = (ta + tb) / 2 + 180
    P = lambda t: (math.cos(math.radians(t)), math.sin(math.radians(t)))
    A, B, C = P(ta), P(tb), P(tc)
    for (x1, y1), (x2, y2) in (((0, 0), A), ((0, 0), B), (C, A), (C, B)):
        ax.plot([x1, x2], [y1, y2], color="black", lw=1.4)
    for name, (x, y) in (("A", A), ("B", B), ("C", C)):
        ax.plot(x, y, "o", color="black", ms=4)
        ax.text(x * 1.12, y * 1.12, name, ha="center", va="center")
    ax.plot(0, 0, "o", color="black", ms=4)
    ax.text(-0.08, -0.12, "O")
    mid = math.radians((ta + tb) / 2)
    show_central = rnd.random() < 0.5
    lab_c = f"{cen}°" if show_central else "x"
    lab_i = "x" if show_central else f"{cen // 2}°"
    ax.text(0.28 * math.cos(mid), 0.28 * math.sin(mid), lab_c, ha="center", va="center", color="#d62728", fontsize=12)
    dirc = math.atan2(-C[1], -C[0])
    ax.text(C[0] + 0.25 * math.cos(dirc), C[1] + 0.25 * math.sin(dirc), lab_i, ha="center", va="center", color="#d62728", fontsize=12)
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.set_aspect("equal")
    ax.axis("off")
    img = save_fig(fig)
    if show_central:
        cs, ws = numeric_options(cen // 2, [cen, 180 - cen, 360 - cen], step=5, fn=deg)
        return make(GEOMETRIA, "En la circunferencia de centro O, ¿cuánto mide el ángulo inscrito x?", cs, ws,
                    f"El ángulo inscrito ACB mide la mitad del ángulo del centro AOB: {cen}°/2 = {cen // 2}°.", img)
    cs, ws = numeric_options(cen, [cen // 4 if cen // 4 else 10, 180 - cen // 2, 360 - cen, cen // 2], step=10, fn=deg)
    return make(GEOMETRIA, "En la circunferencia de centro O, ¿cuánto mide el ángulo del centro x?", cs, ws,
                f"El ángulo del centro AOB mide el doble del inscrito ACB: 2·{cen // 2}° = {cen}°.", img)


def g_sphere():
    r = rnd.choice([3, 6, 9]) if rnd.random() < 0.5 else rnd.randint(2, 12)
    fig, ax = plt.subplots(figsize=(3.8, 3.8))
    ax.add_patch(Circle((0, 0), 1, fill=True, facecolor="#e6f0fa", edgecolor="#1f77b4", lw=2))
    ax.add_patch(Ellipse((0, 0), 2, 0.5, fill=False, ls="--", color="#1f77b4"))
    ax.plot([0, 1], [0, 0], color="#d62728", lw=2)
    ax.plot(0, 0, "o", color="black", ms=4)
    ax.text(0.5, 0.08, f"{r} cm", ha="center", color="#d62728")
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_aspect("equal")
    ax.axis("off")
    img = save_fig(fig)
    if r % 3 == 0:
        v = 4 * r ** 3 // 3
        c, w = f"{fint(v)}π cm³", [f"{fint(4 * r * r)}π cm³", f"{fint(r ** 3)}π cm³", f"{fint(4 * r ** 3)}π cm³", f"{fint(v // 2)}π cm³"]
        return make(GEOMETRIA, "La figura muestra una esfera y su radio. ¿Cuál es su volumen?", c, w, f"V = (4/3)·π·{r}³ = {fint(v)}π cm³.", img)
    c, w = f"{fint(4 * r * r)}π cm²", [f"{fint(r * r)}π cm²", f"{fint(2 * r * r)}π cm²", f"{fint(4 * r)}π cm²", f"{fint(8 * r * r)}π cm²"]
    return make(GEOMETRIA, "La figura muestra una esfera y su radio. ¿Cuál es el área de su superficie?", c, w, f"A = 4·π·{r}² = {fint(4 * r * r)}π cm².", img)


def g_two_lines():
    x0, y0 = rnd.randint(-4, 4), rnd.randint(-4, 4)
    m1, m2 = rnd.sample([-3, -2, -1, 1, 2, 3], 2)
    b1, b2 = y0 - m1 * x0, y0 - m2 * x0
    if max(abs(b1), abs(b2)) > 8:
        raise Skip()
    fig, ax = plt.subplots(figsize=(4.8, 4.8))
    xs = np.array([-7, 7])
    ax.plot(xs, m1 * xs + b1, color="#1f77b4", lw=2, label="L₁: " + line_str(m1, b1))
    ax.plot(xs, m2 * xs + b2, color="#ff7f0e", lw=2, label="L₂: " + line_str(m2, b2))
    ax.plot(x0, y0, "o", color="#d62728")
    axes_plane(ax, (-7, 7), (-9, 9), 1, 1)
    ax.tick_params(labelsize=8)
    ax.legend(loc="upper left", fontsize=9, framealpha=0.95)
    img = save_fig(fig)
    c = pt(x0, y0)
    w = [pt(y0, x0), pt(-x0, y0), pt(x0, -y0), pt(0, b1), pt(0, b2), pt(x0 + 1, y0)]
    return make(ALGEBRA, "El gráfico muestra las rectas L₁ y L₂. ¿Cuál es la solución del sistema formado por sus ecuaciones?", c, w,
                f"La solución es el punto donde se cortan las rectas: {c}. Se comprueba en ambas ecuaciones.", img)


def g_homothety():
    k = rnd.choice([2, 3])
    pts = [(rnd.randint(1, 3), rnd.randint(1, 3)) for _ in range(3)]
    (x1, y1), (x2, y2), (x3, y3) = pts
    if abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)) < 1:
        raise Skip()
    fig, ax = plt.subplots(figsize=(4.8, 4.8))
    ax.add_patch(Polygon(pts, closed=True, facecolor="#cfe3f5", edgecolor="#1f77b4", lw=2))
    show_image = rnd.random() < 0.5
    if show_image:
        ax.add_patch(Polygon([(k * x, k * y) for x, y in pts], closed=True, fill=False, edgecolor="#ff7f0e", lw=2, ls="--"))
        for x, y in pts:
            ax.plot([0, k * x], [0, k * y], color="gray", lw=0.6, ls=":")
    for name, (x, y) in zip("ABC", pts):
        ax.text(x - 0.25, y + 0.15, name, fontsize=10)
        if show_image:
            ax.text(k * x + 0.1, k * y + 0.15, name + "'", fontsize=10, color="#ff7f0e")
    ax.plot(0, 0, "o", color="black")
    ax.text(0.15, -0.6, "O", fontsize=10)
    axes_plane(ax, (-1, 10), (-1, 10), 1, 1)
    ax.set_aspect("equal")
    img = save_fig(fig)
    if show_image:
        cs, ws = numeric_options(k, [Fraction(1, k), k + 1, -k], step=1, positive=False, fn=fs)
        return make(GEOMETRIA, "El triángulo A'B'C' (línea punteada) es la imagen del triángulo ABC por una homotecia de centro O. ¿Cuál es la razón de la homotecia?", cs, ws,
                    f"Cada vértice imagen está {k} veces más lejos de O: por ejemplo A = {pt(x1, y1)} y A' = {pt(k * x1, k * y1)}. Razón {k}.", img)
    i = rnd.randrange(3)
    x, y = pts[i]
    name = "ABC"[i]
    c = pt(k * x, k * y)
    w = [pt(x + k, y + k), pt(k * x, y), pt(k * y, k * x) if x != y else pt(k * x + 1, k * y), pt(x * (k + 1), y * (k + 1))]
    return make(GEOMETRIA, f"Se aplica al triángulo ABC una homotecia de centro O (el origen) y razón {k}. ¿Cuáles son las coordenadas de la imagen del vértice {name}?", c, w,
                f"{name} = {pt(x, y)}; se multiplican sus coordenadas por {k}: {c}.", img)


NORMAL_REGIONS = [((-1, 1), "68%"), ((-2, 2), "95%"), ((0, 4), "50%"), ((1, 4), "16%"), ((0, 1), "34%"), ((-4, -2), "2,5%"), ((1, 2), "13,5%")]


def g_normal():
    mu, s, ctx, unit = rnd.choice([(165, 8, "las estaturas de un grupo de adultos", "cm"), (70, 10, "los pesos de un grupo de personas", "kg"),
                                   (500, 100, "los puntajes de una prueba", "puntos"), (40, 5, "los tiempos de un trayecto", "min"),
                                   (12, 2, "la duración de unas baterías", "horas")])
    (z1, z2), ans = rnd.choice(NORMAL_REGIONS)
    zs = np.linspace(-3.5, 3.5, 400)
    ys = np.exp(-zs ** 2 / 2)
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    ax.plot(zs, ys, color="#1f77b4", lw=2)
    mask = (zs >= z1) & (zs <= z2)
    ax.fill_between(zs[mask], ys[mask], color="#ff7f0e", alpha=0.5)
    ax.set_xticks(range(-3, 4))
    ax.set_xticklabels([fint(mu + z * s) for z in range(-3, 4)])
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xlabel(unit)
    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(0, 1.1)
    img = save_fig(fig)
    return make(PROBA, f"El gráfico muestra la distribución normal de {ctx}, con media {fint(mu)} {unit} y desviación estándar {fint(s)} {unit}. ¿Qué porcentaje aproximado de los datos corresponde a la zona sombreada?",
                ans, rnd.sample([v for v in NORMAL_VALUES if v != ans], 3),
                "Regla empírica: cerca del 68% está a menos de 1 desviación estándar de la media, cerca del 95% a menos de 2, y la curva es simétrica.", img)


GRAPH_PLAN = [(g_trig_graph, 20), (g_exponential, 12), (g_log, 10), (g_trig_triangle, 14), (g_circle_angle, 10),
              (g_sphere, 8), (g_two_lines, 10), (g_homothety, 8), (g_normal, 8)]


def build():
    if os.path.isdir(IMG_DIR):
        for f in os.listdir(IMG_DIR):
            if f.endswith(".png"):
                os.remove(os.path.join(IMG_DIR, f))
    seen = set()
    out = []
    i = 0
    guard = 0
    n_text = 0
    while n_text < N_TEXT:
        t = TEXT_TEMPLATES[i % len(TEXT_TEMPLATES)]
        i += 1
        guard += 1
        if guard > 100000:
            raise RuntimeError("No se lograron completar las preguntas de texto.")
        for _ in range(60):
            try:
                q = t()
            except (Skip, ZeroDivisionError):
                continue
            if q["enunciado"] in seen:
                continue
            seen.add(q["enunciado"])
            out.append(q)
            n_text += 1
            break
    for fn, n in GRAPH_PLAN:
        made = tries = 0
        while made < n:
            tries += 1
            if tries > 800:
                raise RuntimeError(f"No se pudo completar {fn.__name__}")
            before = _img[0]
            try:
                q = fn()
            except (Skip, ZeroDivisionError):
                if _img[0] > before:
                    p = os.path.join(IMG_DIR, f"m2_img_{_img[0]:03d}.png")
                    if os.path.exists(p):
                        os.remove(p)
                    _img[0] -= 1
                continue
            out.append(q)
            made += 1
    # Se reemplazan las últimas preguntas de texto por las de suficiencia de datos.
    # Así el resto del banco (y los gráficos) quedan iguales que antes.
    texto = [q for q in out if "imagen" not in q]
    graficos = [q for q in out if "imagen" in q]
    out = texto[:N_TEXT - N_SUFICIENCIA] + m2_suficiencia.build(N_SUFICIENCIA) + graficos
    rnd.shuffle(out)
    ordered = []
    for n, q in enumerate(out, 1):
        item = {"id": f"m2_{n:03d}", "prueba": "m2", "eje": q["eje"], "enunciado": q["enunciado"],
                "alternativas": q["alternativas"], "correcta": q["correcta"], "explicacion": q["explicacion"]}
        if "tipo" in q:
            item["tipo"] = q["tipo"]
        if "imagen" in q:
            item["imagen"] = q["imagen"]
        ordered.append(item)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(ordered, f, ensure_ascii=False, indent=1)
    return ordered


def validate(qs):
    assert len(qs) == N_TEXT + N_GRAPH, len(qs)
    for q in qs:
        n_opts = 5 if q.get("tipo") == "suficiencia" else 4
        assert len(q["alternativas"]) == n_opts and len(set(q["alternativas"])) == n_opts, q
        assert 0 <= q["correcta"] < n_opts
        if "imagen" in q:
            assert os.path.exists(os.path.join(ROOT, q["imagen"])), q["imagen"]
    n_img = sum(1 for q in qs if "imagen" in q)
    assert n_img == N_GRAPH, n_img
    assert len(os.listdir(IMG_DIR)) == N_GRAPH
    suf = [q for q in qs if q.get("tipo") == "suficiencia"]
    assert len(suf) == N_SUFICIENCIA, len(suf)
    from collections import Counter
    print(f"OK: {len(qs)} preguntas, {n_img} con gráfico, {len(suf)} de suficiencia de datos "
          f"(respuestas: {dict(sorted(Counter('ABCDE'[q['correcta']] for q in suf).items()))}).")


if __name__ == "__main__":
    validate(build())
