"""Preguntas de texto de Ciencias: cálculos (resueltos por el programa) y
preguntas de conceptos (escritas a partir de listas de datos revisadas)."""
import math
from fractions import Fraction

from ciencias_comun import (BIO, FIS, QUI, MINUS, Skip, fint, fmt, frac_str, make,
                            numeric_options, pick_others, rnd, sup, unit)


# ============================================================ FÍSICA (cálculo)
def t_mru():
    v, t = rnd.randint(2, 30), rnd.randint(2, 20)
    d = v * t
    k = rnd.randint(1, 3)
    obj = rnd.choice(["Un ciclista", "Un auto", "Un corredor", "Un tren", "Una persona en patines"])
    if k == 1:
        c, w = numeric_options(v, [d * t, d + t, d - t], step=2, fn=unit("m/s"))
        return make(FIS, f"{obj} recorre {fint(d)} m en {t} s con rapidez constante. ¿Cuál es su rapidez?", c, w, f"v = d/t = {fint(d)}/{t} = {v} m/s.")
    if k == 2:
        c, w = numeric_options(d, [v + t, d // 2, d * 2], step=v, fn=unit("m"))
        return make(FIS, f"{obj} se mueve con rapidez constante de {v} m/s. ¿Qué distancia recorre en {t} s?", c, w, f"d = v·t = {v}·{t} = {fint(d)} m.")
    c, w = numeric_options(t, [d * v, d - v, t * 2], step=1, fn=unit("s"))
    return make(FIS, f"{obj} viaja a {v} m/s constantes. ¿Cuánto tiempo tarda en recorrer {fint(d)} m?", c, w, f"t = d/v = {fint(d)}/{v} = {t} s.")


def t_kmh():
    kmh = rnd.choice([18, 36, 54, 72, 90, 108, 126, 144])
    ms = kmh * 5 // 18
    c, w = numeric_options(ms, [kmh * 36 // 10, kmh // 36 or 1, kmh * 1000 // 60 // 10], step=5, fn=unit("m/s"))
    return make(FIS, f"Un vehículo se mueve a {kmh} km/h. ¿A cuántos metros por segundo equivale esa rapidez?", c, w,
                f"Se divide por 3,6: {kmh}/3,6 = {ms} m/s.")


def t_accel():
    a, t = rnd.randint(1, 8), rnd.randint(2, 12)
    vi = rnd.randint(0, 20)
    vf = vi + a * t
    if rnd.random() < 0.5:
        c, w = numeric_options(a, [vf // t, vf - vi, (vf + vi) // t], step=1, fn=unit("m/s²"))
        return make(FIS, f"Un móvil aumenta su velocidad de {vi} m/s a {vf} m/s en {t} s de manera uniforme. ¿Cuál es su aceleración?", c, w,
                    f"a = (vf − vi)/t = ({vf} − {vi})/{t} = {a} m/s².")
    c, w = numeric_options(vf, [vi + a, a * t, vi * t], step=a, fn=unit("m/s"))
    return make(FIS, f"Un móvil parte con velocidad {vi} m/s y acelera de manera constante a {a} m/s². ¿Qué velocidad tiene después de {t} s?", c, w,
                f"vf = vi + a·t = {vi} + {a}·{t} = {vf} m/s.")


def t_free_fall():
    t = rnd.randint(1, 5)
    if rnd.random() < 0.5:
        v = 10 * t
        c, w = numeric_options(v, [5 * t * t, 10 * t * t, 10 + t], step=5, fn=unit("m/s"))
        return make(FIS, f"Se deja caer una piedra desde el reposo. Despreciando el roce con el aire y usando g = 10 m/s², ¿qué rapidez tiene después de {t} s?", c, w, f"v = g·t = 10·{t} = {v} m/s.")
    h = 5 * t * t
    c, w = numeric_options(h, [10 * t, 10 * t * t, 5 * t], step=5, fn=unit("m"))
    return make(FIS, f"Se deja caer un objeto desde el reposo. Usando g = 10 m/s² y sin roce con el aire, ¿qué distancia cae en {t} s?", c, w, f"h = ½·g·t² = 5·{t * t} = {h} m.")


def t_newton2():
    m, a = rnd.randint(2, 60), rnd.randint(1, 10)
    F = m * a
    if rnd.random() < 0.5:
        c, w = numeric_options(F, [m + a, m * a * 2, F // 2 if F > 2 else F + 3], step=m, fn=unit("N"))
        return make(FIS, f"¿Qué fuerza neta se necesita para que un cuerpo de {m} kg acelere a {a} m/s²?", c, w, f"F = m·a = {m}·{a} = {F} N.")
    c, w = numeric_options(a, [F * m, F - m, a * 2], step=1, fn=unit("m/s²"))
    return make(FIS, f"Sobre un cuerpo de {m} kg actúa una fuerza neta de {F} N. ¿Cuál es su aceleración?", c, w, f"a = F/m = {F}/{m} = {a} m/s².")


def t_weight():
    m = rnd.randint(2, 120)
    c, w = numeric_options(m * 10, [m, m + 10, m * 100], step=10, fn=unit("N"))
    return make(FIS, f"¿Cuál es el peso de un cuerpo de {m} kg en la Tierra? (usa g = 10 m/s²)", c, w, f"P = m·g = {m}·10 = {m * 10} N.")


def t_energy():
    k = rnd.randint(1, 3)
    if k == 1:
        m, v = rnd.choice([2, 4, 6, 8, 10, 20, 50]), rnd.randint(2, 12)
        E = m * v * v // 2
        c, w = numeric_options(E, [m * v, m * v * v, m * v // 2], step=max(1, E // 10), fn=unit("J"))
        return make(FIS, f"¿Cuál es la energía cinética de un cuerpo de {m} kg que se mueve a {v} m/s?", c, w, f"Ec = ½·m·v² = ½·{m}·{v * v} = {fint(E)} J.")
    if k == 2:
        m, h = rnd.randint(1, 30), rnd.randint(2, 40)
        E = m * 10 * h
        c, w = numeric_options(E, [m * h, m + 10 + h, E // 2], step=max(10, E // 10), fn=unit("J"))
        return make(FIS, f"¿Cuál es la energía potencial gravitatoria de un objeto de {m} kg a {h} m de altura? (usa g = 10 m/s²)", c, w, f"Ep = m·g·h = {m}·10·{h} = {fint(E)} J.")
    h = rnd.choice([5, 20, 45, 80])
    v = int(math.isqrt(20 * h))
    c, w = numeric_options(v, [20 * h, 10 * h // 5, v * 2], step=5, fn=unit("m/s"))
    return make(FIS, f"Un cuerpo se suelta desde {h} m de altura. Si la energía mecánica se conserva (sin roce) y g = 10 m/s², ¿con qué rapidez llega al suelo?", c, w,
                f"m·g·h = ½·m·v² → v = √(2·g·h) = √{20 * h} = {v} m/s.")


def t_work_power():
    F, d, t = rnd.randint(5, 200), rnd.randint(2, 30), rnd.choice([2, 4, 5, 10])
    W = F * d
    if W % t or rnd.random() < 0.5:
        c, w = numeric_options(W, [F + d, F * d * 2, W // 2], step=max(5, W // 10), fn=unit("J"))
        return make(FIS, f"Una persona empuja una caja con una fuerza constante de {F} N en la dirección del movimiento y la desplaza {d} m. ¿Qué trabajo realiza?", c, w, f"W = F·d = {F}·{d} = {fint(W)} J.")
    P = W // t
    c, w = numeric_options(P, [W * t, W, P * 2], step=max(5, P // 5), fn=unit("W"))
    return make(FIS, f"Un motor realiza un trabajo de {fint(W)} J en {t} s. ¿Cuál es su potencia media?", c, w, f"P = W/t = {fint(W)}/{t} = {fint(P)} W.")


def t_ohm():
    R, I = rnd.choice([2, 4, 5, 6, 8, 10, 12, 20, 25, 50]), rnd.choice([1, 2, 3, 4, 5])
    V = R * I
    k = rnd.randint(1, 3)
    if k == 1:
        c, w = numeric_options(I, [V * R, R // I or 7, V - R], step=1, fn=unit("A"))
        return make(FIS, f"Una resistencia de {R} Ω se conecta a una fuente de {V} V. ¿Qué corriente circula por ella?", c, w, f"Ley de Ohm: I = V/R = {V}/{R} = {I} A.")
    if k == 2:
        c, w = numeric_options(V, [R + I, R // I if R % I == 0 else R + 1, V * 2], step=R, fn=unit("V"))
        return make(FIS, f"Por una resistencia de {R} Ω circula una corriente de {I} A. ¿Cuál es el voltaje entre sus extremos?", c, w, f"V = I·R = {I}·{R} = {V} V.")
    c, w = numeric_options(R, [V * I, V + I, R * 2], step=2, fn=unit("Ω"))
    return make(FIS, f"Una ampolleta conectada a {V} V deja pasar una corriente de {I} A. ¿Cuál es su resistencia?", c, w, f"R = V/I = {V}/{I} = {R} Ω.")


PARALLEL = [(3, 6, 2), (4, 4, 2), (6, 12, 4), (10, 15, 6), (20, 30, 12), (12, 24, 8), (6, 6, 3), (10, 10, 5), (4, 12, 3), (12, 12, 6)]


def t_circuits():
    if rnd.random() < 0.5:
        rs = rnd.sample([1, 2, 3, 4, 5, 6, 8, 10], rnd.choice([2, 3]))
        Rt = sum(rs)
        I = rnd.randint(1, 4)
        V = Rt * I
        txt = ", ".join(f"{r} Ω" for r in rs[:-1]) + f" y {rs[-1]} Ω"
        if rnd.random() < 0.5:
            c, w = numeric_options(Rt, [max(rs), Rt * 2, min(rs)], step=1, fn=unit("Ω"))
            return make(FIS, f"Se conectan en serie resistencias de {txt}. ¿Cuál es la resistencia equivalente?", c, w, f"En serie se suman: {' + '.join(map(str, rs))} = {Rt} Ω.")
        c, w = numeric_options(I, [V * Rt, V // max(rs) if V // max(rs) != I else I + 2, I * len(rs)], step=1, fn=unit("A"))
        return make(FIS, f"Resistencias de {txt} se conectan en serie a una batería de {V} V. ¿Qué corriente circula por el circuito?", c, w, f"R total = {Rt} Ω; I = {V}/{Rt} = {I} A.")
    a, b, r = rnd.choice(PARALLEL)
    c, w = numeric_options(r, [a + b, abs(a - b) or a + 1, (a + b) // 2], step=1, fn=unit("Ω"))
    return make(FIS, f"Se conectan en paralelo dos resistencias de {a} Ω y {b} Ω. ¿Cuál es la resistencia equivalente?", c, w,
                f"1/R = 1/{a} + 1/{b} → R = ({a}·{b})/({a} + {b}) = {r} Ω.")


def t_elec_power():
    V, I = rnd.choice([12, 24, 110, 220]), rnd.choice([1, 2, 3, 5, 10])
    P = V * I
    c, w = numeric_options(P, [V + I, V // I if V % I == 0 else V + 1, P * 2], step=V, fn=unit("W"))
    return make(FIS, f"Un artefacto funciona con {V} V y una corriente de {I} A. ¿Cuál es su potencia eléctrica?", c, w, f"P = V·I = {V}·{I} = {fint(P)} W.")


def t_wave():
    k = rnd.randint(1, 3)
    if k == 1:
        lam, f = rnd.choice([0.5, 1, 2, 3, 4, 5, 10]), rnd.choice([2, 4, 5, 10, 20, 50, 100])
        v = lam * f
        c, w = numeric_options(v, [lam + f, f / lam, v * 2], step=max(1, v / 10), fn=unit("m/s"))
        return make(FIS, f"Una onda tiene longitud de onda {fmt(lam)} m y frecuencia {f} Hz. ¿Cuál es su rapidez de propagación?", c, w, f"v = λ·f = {fmt(lam)}·{f} = {fmt(v)} m/s.")
    if k == 2:
        f = rnd.choice([2, 4, 5, 10, 20, 50])
        T = Fraction(1, f)
        c, w = frac_str(T) + " s", [f"{f} s", f"{f * 2} s", frac_str(Fraction(1, f * 2)) + " s", frac_str(Fraction(2, f)) + " s"]
        return make(FIS, f"Una onda tiene una frecuencia de {f} Hz. ¿Cuál es su período?", c, w, f"T = 1/f = 1/{f} s.")
    n, t = rnd.choice([(20, 4), (30, 5), (60, 10), (40, 8), (100, 20), (50, 2), (120, 6)])
    f = n // t
    c, w = numeric_options(f, [n * t, n - t, t], step=1, fn=unit("Hz"))
    return make(FIS, f"Un péndulo realiza {n} oscilaciones completas en {t} s. ¿Cuál es su frecuencia?", c, w, f"f = n.º de oscilaciones / tiempo = {n}/{t} = {f} Hz.")


def t_echo():
    t = rnd.choice([0.2, 0.4, 0.5, 1, 1.5, 2, 3, 4])
    d = 340 * t / 2
    c, w = numeric_options(d, [340 * t, 340 / t, d / 2], step=17, fn=unit("m"))
    return make(FIS, f"Una persona grita frente a un cerro y escucha el eco {fmt(t)} s después. Si el sonido viaja a 340 m/s en el aire, ¿a qué distancia está el cerro?", c, w,
                f"El sonido va y vuelve: d = v·t/2 = 340·{fmt(t)}/2 = {fmt(d)} m.")


def t_pressure_density():
    k = rnd.randint(1, 3)
    if k == 1:
        A, P = rnd.choice([0.5, 1, 2, 4, 5]), rnd.choice([100, 200, 400, 500, 1000, 2000])
        F = A * P
        c, w = numeric_options(P, [F * A, F + A, P * 2], step=max(10, P // 10), fn=unit("Pa"))
        return make(FIS, f"Una fuerza de {fmt(F)} N actúa perpendicularmente sobre una superficie de {fmt(A)} m². ¿Qué presión ejerce?", c, w, f"P = F/A = {fmt(F)}/{fmt(A)} = {fmt(P)} Pa.")
    if k == 2:
        V, rho = rnd.choice([2, 4, 5, 10, 20, 50]), rnd.choice([0.5, 0.8, 1, 2, 2.5, 7.8, 11.3])
        m = V * rho
        c, w = numeric_options(rho, [m * V, m + V, rho * 2], step=0.5, fn=unit("g/cm³"))
        return make(FIS, f"Un objeto tiene una masa de {fmt(m)} g y un volumen de {V} cm³. ¿Cuál es su densidad?", c, w, f"ρ = m/V = {fmt(m)}/{V} = {fmt(rho)} g/cm³.")
    h = rnd.choice([2, 5, 10, 20, 30])
    P = 1000 * 10 * h
    c, w = numeric_options(P, [10 * h, 1000 * h, P * 2], step=10000, fn=unit("Pa"))
    return make(FIS, f"¿Qué presión ejerce el agua (densidad 1.000 kg/m³) a {h} m de profundidad, sin contar la presión atmosférica? (usa g = 10 m/s²)", c, w,
                f"P = ρ·g·h = 1.000·10·{h} = {fint(P)} Pa.")


def t_heat():
    m, dT = rnd.choice([50, 100, 200, 250, 500, 1000]), rnd.randint(5, 60)
    Q = m * dT
    if rnd.random() < 0.5:
        c, w = numeric_options(Q, [m + dT, m * dT * 2, m // dT if m // dT else 3], step=max(50, Q // 10), fn=unit("cal"))
        return make(FIS, f"¿Cuánto calor se necesita para elevar en {dT} °C la temperatura de {m} g de agua? (calor específico del agua: 1 cal/g·°C)", c, w, f"Q = m·c·ΔT = {m}·1·{dT} = {fint(Q)} cal.")
    c, w = numeric_options(dT, [Q * m, Q // 10, dT * 2], step=2, fn=unit("°C"))
    return make(FIS, f"Se entregan {fint(Q)} cal a {m} g de agua (calor específico 1 cal/g·°C). ¿En cuánto aumenta su temperatura?", c, w, f"ΔT = Q/(m·c) = {fint(Q)}/{m} = {dT} °C.")


def t_hooke_momentum():
    if rnd.random() < 0.5:
        k, x = rnd.choice([10, 20, 50, 100, 200, 500]), rnd.choice([0.02, 0.05, 0.1, 0.2, 0.3])
        F = k * x
        c, w = numeric_options(F, [k * x * 2, k + x, k * x / 2], step=1, fn=unit("N"))
        return make(FIS, f"Un resorte de constante elástica {k} N/m se estira {fmt(x)} m. ¿Qué fuerza ejerce el resorte?", c, w, f"Ley de Hooke: F = k·x = {k}·{fmt(x)} = {fmt(F)} N.")
    m, v = rnd.randint(2, 80), rnd.randint(2, 25)
    p = m * v
    c, w = numeric_options(p, [m + v, p * 2, m * v * v // 2], step=m, fn=unit("kg·m/s"))
    return make(FIS, f"¿Cuál es el momentum lineal de un cuerpo de {m} kg que se mueve a {v} m/s?", c, w, f"p = m·v = {m}·{v} = {fint(p)} kg·m/s.")


# ============================================================ QUÍMICA (cálculo)
ELEMENTS = [("hidrógeno", "H", 1, 1), ("helio", "He", 2, 4), ("litio", "Li", 3, 7), ("carbono", "C", 6, 12), ("nitrógeno", "N", 7, 14),
            ("oxígeno", "O", 8, 16), ("flúor", "F", 9, 19), ("sodio", "Na", 11, 23), ("magnesio", "Mg", 12, 24), ("aluminio", "Al", 13, 27),
            ("fósforo", "P", 15, 31), ("azufre", "S", 16, 32), ("potasio", "K", 19, 39), ("calcio", "Ca", 20, 40), ("hierro", "Fe", 26, 56)]
IONS = [("Na⁺", 11, 10), ("K⁺", 19, 18), ("Mg²⁺", 12, 10), ("Ca²⁺", 20, 18), ("Al³⁺", 13, 10), ("O²⁻", 8, 10), ("S²⁻", 16, 18), ("F⁻", 9, 10), ("Cl⁻", 17, 18)]


def t_subatomic():
    k = rnd.randint(1, 3)
    if k == 3:
        ion, Z, e = rnd.choice(IONS)
        c, w = numeric_options(e, [Z, Z + (Z - e), Z * 2], step=1)
        return make(QUI, f"El ion {ion} proviene de un átomo con número atómico Z = {Z}. ¿Cuántos electrones tiene el ion?", c, w,
                    f"Un átomo neutro tiene {Z} electrones; la carga del ion indica que {'perdió' if e < Z else 'ganó'} {abs(Z - e)}, quedando con {e}.")
    name, sym, Z, A = rnd.choice(ELEMENTS)
    if k == 1 and A - Z != Z:
        c, w = numeric_options(A - Z, [A, Z, A + Z], step=1)
        return make(QUI, f"Un átomo de {name} tiene número atómico Z = {Z} y número másico A = {A}. ¿Cuántos neutrones tiene en su núcleo?", c, w, f"Neutrones = A − Z = {A} − {Z} = {A - Z}.")
    c, w = numeric_options(Z, [A, A - Z if A - Z != Z else A + 1, Z + 1], step=1)
    return make(QUI, f"Un átomo neutro de {name} ({sym}) tiene número atómico {Z} y número másico {A}. ¿Cuántos electrones tiene?", c, w, f"En un átomo neutro, electrones = protones = Z = {Z}.")


MASSES = {"H": 1, "C": 12, "N": 14, "O": 16, "Na": 23, "Mg": 24, "S": 32, "Cl": 35.5, "K": 39, "Ca": 40}
COMPOUNDS = [("agua", "H₂O", {"H": 2, "O": 1}), ("dióxido de carbono", "CO₂", {"C": 1, "O": 2}), ("amoníaco", "NH₃", {"N": 1, "H": 3}),
             ("metano", "CH₄", {"C": 1, "H": 4}), ("cloruro de sodio", "NaCl", {"Na": 1, "Cl": 1}), ("ácido sulfúrico", "H₂SO₄", {"H": 2, "S": 1, "O": 4}),
             ("carbonato de calcio", "CaCO₃", {"Ca": 1, "C": 1, "O": 3}), ("glucosa", "C₆H₁₂O₆", {"C": 6, "H": 12, "O": 6}),
             ("hidróxido de sodio", "NaOH", {"Na": 1, "O": 1, "H": 1}), ("ácido clorhídrico", "HCl", {"H": 1, "Cl": 1}),
             ("óxido de magnesio", "MgO", {"Mg": 1, "O": 1}), ("hidróxido de potasio", "KOH", {"K": 1, "O": 1, "H": 1}),
             ("etanol", "C₂H₆O", {"C": 2, "H": 6, "O": 1}), ("oxígeno molecular", "O₂", {"O": 2}), ("nitrógeno molecular", "N₂", {"N": 2})]


def mm(comp):
    return sum(MASSES[e] * n for e, n in comp.items())


def masses_txt(comp):
    return ", ".join(f"{e} = {fmt(MASSES[e])}" for e in comp)


def t_molar():
    name, f, comp = rnd.choice(COMPOUNDS)
    M = mm(comp)
    k = rnd.randint(1, 2)
    if k == 1:
        c, w = numeric_options(M, [sum(MASSES[e] for e in comp), M + 16, M - 1 if M > 2 else M + 2], step=2, fn=unit("g/mol"))
        return make(QUI, f"¿Cuál es la masa molar del {name} ({f})? (masas atómicas en g/mol: {masses_txt(comp)})", c, w,
                    f"Se suman las masas de todos los átomos: {' + '.join(f'{n}·{fmt(MASSES[e])}' for e, n in comp.items())} = {fmt(M)} g/mol.")
    n = rnd.choice([0.5, 2, 3, 4, 5, 10])
    m = M * n
    c, w = numeric_options(n, [m * M, M / m if m else 1, n * 2], step=0.5, fn=unit("mol"))
    return make(QUI, f"¿Cuántos moles hay en {fmt(m)} g de {name} ({f})? (masa molar: {fmt(M)} g/mol)", c, w, f"n = m/M = {fmt(m)}/{fmt(M)} = {fmt(n)} mol.")


def t_avogadro():
    n = rnd.choice([0.5, 2, 3, 5, 10])
    val = n * 6.02
    exp = 23
    while val >= 10:
        val /= 10
        exp += 1
    s = f"{fmt(round(val, 3))} × 10{sup(exp)}"
    w = [f"6,02 × 10²³", f"{fmt(round(val, 3))} × 10{sup(exp + 1)}", f"{fmt(n)} × 10²³", f"{fmt(round(val * 2 if val * 2 < 10 else val / 2, 3))} × 10{sup(exp)}"]
    return make(QUI, f"¿Cuántas moléculas hay en {fmt(n)} mol de agua? (número de Avogadro: 6,02 × 10²³)", s, w, f"N = n·N_A = {fmt(n)}·6,02 × 10²³ = {s}.")


def t_solutions():
    k = rnd.randint(1, 4)
    if k == 1:
        n, V = rnd.choice([0.1, 0.2, 0.5, 1, 2, 3]), rnd.choice([0.25, 0.5, 1, 2])
        M = n / V
        c, w = numeric_options(M, [n * V, V / n, M * 2], step=0.1, fn=unit("mol/L"))
        return make(QUI, f"Se disuelven {fmt(n)} mol de soluto en agua hasta completar {fmt(V)} L de solución. ¿Cuál es la concentración molar?", c, w, f"M = n/V = {fmt(n)}/{fmt(V)} = {fmt(M)} mol/L.")
    if k == 2:
        C1, V1, f = rnd.choice([1, 2, 3, 4, 6]), rnd.choice([50, 100, 200, 250]), rnd.choice([2, 4, 5, 10])
        V2 = V1 * f
        C2 = C1 / f
        c, w = numeric_options(C2, [C1 * f, C1, C2 * 2], step=0.1, fn=unit("mol/L"))
        return make(QUI, f"Se toman {V1} mL de una solución {C1} mol/L y se agrega agua hasta completar {V2} mL. ¿Cuál es la nueva concentración?", c, w,
                    f"C₁·V₁ = C₂·V₂ → C₂ = {C1}·{V1}/{V2} = {fmt(C2)} mol/L.")
    if k == 3:
        s, total = rnd.choice([5, 10, 15, 20, 25, 40, 50]), rnd.choice([100, 200, 250, 500])
        p = Fraction(s * 100, total)
        if p.denominator != 1 and (p * 10).denominator != 1:
            raise Skip()
        c, w = numeric_options(p, [Fraction(s * 100, total - s), s, Fraction(total, s)], step=1, fn=lambda v: f"{fmt(v)}% m/m")
        return make(QUI, f"Se disuelven {s} g de sal en agua y se obtienen {total} g de solución. ¿Cuál es el porcentaje en masa (% m/m) de la sal?", c, w,
                    f"% m/m = masa de soluto/masa de solución·100 = {s}/{total}·100 = {fmt(p)}%.")
    M, V = rnd.choice([0.1, 0.2, 0.5, 1, 2]), rnd.choice([0.5, 1, 2, 3])
    n = M * V
    c, w = numeric_options(n, [M / V, M + V, n * 2], step=0.1, fn=unit("mol"))
    return make(QUI, f"¿Cuántos moles de soluto hay en {fmt(V)} L de una solución de concentración {fmt(M)} mol/L?", c, w, f"n = M·V = {fmt(M)}·{fmt(V)} = {fmt(n)} mol.")


def t_ph():
    k = rnd.randint(1, 3)
    e = rnd.randint(1, 6)
    if k == 1:
        c, w = numeric_options(e, [14 - e, -e, e + 1], step=1, positive=False)
        return make(QUI, f"Una solución de un ácido fuerte tiene [H⁺] = 10{sup(-e)} mol/L. ¿Cuál es su pH?", c, w, f"pH = −log[H⁺] = −log(10{sup(-e)}) = {e}.")
    if k == 2:
        c, w = numeric_options(14 - e, [e, 14 + e, 7], step=1)
        return make(QUI, f"Una solución básica tiene [OH⁻] = 10{sup(-e)} mol/L a 25 °C. ¿Cuál es su pH?", c, w, f"pOH = {e}; pH = 14 − pOH = {14 - e}.")
    p = rnd.choice([1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13])
    ans = "Ácida" if p < 7 else "Básica"
    return make(QUI, f"A 25 °C, una solución tiene pH = {p}. ¿Cómo se clasifica?", ans, [x for x in ["Ácida", "Básica", "Neutra", "No se puede clasificar con el pH"] if x != ans],
                "Con pH < 7 la solución es ácida; con pH > 7 es básica; con pH = 7 es neutra.")


def t_gases():
    if rnd.random() < 0.5:
        P1, V1, f = rnd.choice([1, 2, 3, 4]), rnd.choice([2, 4, 6, 8, 10, 12]), rnd.choice([2, 3, 4])
        if (V1 % f):
            raise Skip()
        P2, V2 = P1 * f, V1 // f
        c, w = numeric_options(V2, [V1 * f, V1, V1 - f], step=1, fn=unit("L"))
        return make(QUI, f"Un gas ocupa {V1} L a {P1} atm. Si a temperatura constante la presión aumenta a {P2} atm, ¿qué volumen ocupará?", c, w, f"Ley de Boyle: P₁·V₁ = P₂·V₂ → V₂ = {P1}·{V1}/{P2} = {V2} L.")
    T1, f = rnd.choice([200, 250, 300, 400]), rnd.choice([2, Fraction(3, 2)])
    V1 = rnd.choice([2, 4, 6, 10])
    T2, V2 = T1 * f, V1 * f
    if Fraction(T2).denominator != 1 or Fraction(V2).denominator != 1:
        raise Skip()
    c, w = numeric_options(V2, [V1, V1 * T1 // int(T2) if int(T2) else 1, V2 * 2], step=1, fn=unit("L"))
    return make(QUI, f"Un gas ocupa {V1} L a {T1} K. Si a presión constante la temperatura sube a {fint(T2)} K, ¿qué volumen ocupará?", c, w, f"Ley de Charles: V₁/T₁ = V₂/T₂ → V₂ = {V1}·{fint(T2)}/{T1} = {fmt(V2)} L.")


REACTIONS = [("2 H₂ + O₂ → 2 H₂O", "H₂", "H₂O", 2, 2), ("N₂ + 3 H₂ → 2 NH₃", "N₂", "NH₃", 1, 2), ("N₂ + 3 H₂ → 2 NH₃", "H₂", "NH₃", 3, 2),
             ("CH₄ + 2 O₂ → CO₂ + 2 H₂O", "CH₄", "H₂O", 1, 2), ("CH₄ + 2 O₂ → CO₂ + 2 H₂O", "O₂", "CO₂", 2, 1), ("2 Mg + O₂ → 2 MgO", "Mg", "MgO", 2, 2),
             ("C₃H₈ + 5 O₂ → 3 CO₂ + 4 H₂O", "C₃H₈", "CO₂", 1, 3), ("2 Na + Cl₂ → 2 NaCl", "Cl₂", "NaCl", 1, 2)]


def t_stoich():
    if rnd.random() < 0.3:
        a, b = rnd.randint(5, 80), rnd.randint(5, 80)
        c, w = numeric_options(a + b, [abs(a - b), a * b // 10, max(a, b)], step=5, fn=unit("g"))
        return make(QUI, f"En un recipiente cerrado reaccionan completamente {a} g de un reactivo con {b} g de otro. Según la ley de conservación de la masa, ¿qué masa total de productos se forma?", c, w,
                    f"En un sistema cerrado la masa se conserva: {a} g + {b} g = {a + b} g.")
    eq, r, p, cr, cp = rnd.choice(REACTIONS)
    n = rnd.choice([1, 2, 3, 4, 5, 6, 10])
    if (n * cp) % cr:
        raise Skip()
    v = Fraction(n * cp, cr)
    c, w = numeric_options(v, [n, n * cr * cp, Fraction(n * cr, cp)], step=1, fn=unit("mol"))
    return make(QUI, f"Según la ecuación balanceada {eq}, ¿cuántos moles de {p} se forman a partir de {n} mol de {r}, si hay suficiente cantidad de los demás reactivos?", c, w,
                f"La proporción es {cr} mol de {r} : {cp} mol de {p}; entonces {n}·{cp}/{cr} = {fmt(v)} mol.")


def t_kelvin():
    C = rnd.randrange(-50, 201, 5)
    if rnd.random() < 0.5:
        c, w = numeric_options(C + 273, [C - 273, 273 - C, C + 100], step=5, fn=unit("K"), positive=False)
        return make(QUI, f"¿A cuántos kelvin equivale una temperatura de {fint(C)} °C?", c, w, f"K = °C + 273 = {fint(C)} + 273 = {C + 273} K.")
    K = C + 273
    c, w = numeric_options(C, [K + 273, 273 - K, C + 100], step=5, fn=unit("°C"), positive=False)
    return make(QUI, f"¿A cuántos grados Celsius equivale una temperatura de {K} K?", c, w, f"°C = K − 273 = {K} − 273 = {fint(C)} °C.")


ALK = ["met", "et", "prop", "but", "pent", "hex", "hept", "oct"]
SUBN = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def formula(c, h):
    return f"C{'' if c == 1 else str(c).translate(SUBN)}H{str(h).translate(SUBN)}"


def t_hydrocarbon():
    kind = rnd.choice(["ano", "eno", "ino"])
    n = rnd.randint(1 if kind == "ano" else 2, 8)
    h = {"ano": 2 * n + 2, "eno": 2 * n, "ino": 2 * n - 2}[kind]
    name = ALK[n - 1] + kind
    gen = {"ano": "CₙH₂ₙ₊₂ (solo enlaces simples)", "eno": "CₙH₂ₙ (un enlace doble)", "ino": "CₙH₂ₙ₋₂ (un enlace triple)"}[kind]
    w = [formula(n, x) for x in (2 * n + 2, 2 * n, 2 * n - 2, 2 * n + 4) if x != h and x > 0] + [formula(n + 1, h)]
    return make(QUI, f"¿Cuál es la fórmula molecular del {name}?", formula(n, h), w, f"Fórmula general {gen}; con n = {n}: {formula(n, h)}.")


# ============================================================ BIOLOGÍA (cálculo)
TRAITS = [("arvejas", "semillas amarillas", "semillas verdes", "A"), ("flores", "pétalos púrpura", "pétalos blancos", "P"),
          ("ratones", "pelaje negro", "pelaje café", "N"), ("plantas de tomate", "tallo alto", "tallo enano", "T"),
          ("conejos", "pelaje corto", "pelaje largo", "L"), ("cobayos", "pelo liso", "pelo crespo", "R")]


def t_mono():
    org, dom, rec, L = rnd.choice(TRAITS)
    l = L.lower()
    cross = rnd.randint(1, 4)
    pre = f"En {org}, el rasgo {dom} ({L}) es dominante sobre {rec} ({l})."
    if cross == 1:
        q = f"{pre} Si se cruzan dos individuos heterocigotos ({L}{l} × {L}{l}), ¿qué proporción de la descendencia se espera con {rec}?"
        c, w, ex = "1/4", ["3/4", "1/2", "0", "1"], f"{L}{l} × {L}{l} da {L}{L}, {L}{l}, {L}{l}, {l}{l}: solo 1 de 4 es {l}{l}."
    elif cross == 2:
        q = f"{pre} Si se cruzan dos individuos heterocigotos ({L}{l} × {L}{l}), ¿qué proporción de la descendencia se espera que sea heterocigota?"
        c, w, ex = "1/2", ["1/4", "3/4", "1", "0"], f"De {L}{L}, {L}{l}, {L}{l}, {l}{l}, son heterocigotos 2 de 4 = 1/2."
    elif cross == 3:
        q = f"{pre} Si se cruza un individuo heterocigoto con uno homocigoto recesivo ({L}{l} × {l}{l}), ¿qué proporción de la descendencia se espera con {dom}?"
        c, w, ex = "1/2", ["1/4", "3/4", "1", "0"], f"{L}{l} × {l}{l} da {L}{l}, {L}{l}, {l}{l}, {l}{l}: la mitad muestra el rasgo dominante."
    else:
        q = f"{pre} Si se cruza un individuo homocigoto dominante con uno homocigoto recesivo ({L}{L} × {l}{l}), ¿qué proporción de la descendencia será heterocigota?"
        c, w, ex = "1", ["1/2", "1/4", "3/4", "0"], f"Todos los hijos reciben {L} de un progenitor y {l} del otro: 100% {L}{l}."
    return make(BIO, q, c, w, ex)


def t_dihybrid():
    which = rnd.choice([("dominantes para ambos rasgos", "9/16"), ("dominante para el primer rasgo y recesivo para el segundo", "3/16"), ("recesivos para ambos rasgos", "1/16")])
    w = [x for x in ["9/16", "3/16", "1/16", "1/4", "3/4"] if x != which[1]]
    return make(BIO, f"Se cruzan dos individuos dihíbridos (AaBb × AaBb). Si los genes se heredan de forma independiente y A y B son dominantes, ¿qué proporción de la descendencia será {which[0]}?",
                which[1], w, "La proporción fenotípica esperada de un cruce dihíbrido es 9 : 3 : 3 : 1 (sobre 16).")


COMP_DNA = {"A": "T", "T": "A", "G": "C", "C": "G"}
COMP_RNA = {"A": "U", "T": "A", "G": "C", "C": "G"}


def t_dna():
    seq = "".join(rnd.choice("ATGC") for _ in range(rnd.randint(6, 9)))
    if rnd.random() < 0.5:
        comp = "".join(COMP_DNA[b] for b in seq)
        w = [seq, "".join(COMP_RNA[b] for b in seq), comp[::-1], "".join({"A": "G", "G": "A", "T": "C", "C": "T"}[b] for b in seq)]
        return make(BIO, f"Una hebra de ADN tiene la secuencia {seq}. ¿Cuál es la secuencia de la hebra complementaria (leída en el mismo orden)?", comp, w,
                    "En el ADN, A se aparea con T y G con C.")
    rna = "".join(COMP_RNA[b] for b in seq)
    w = ["".join(COMP_DNA[b] for b in seq), seq.replace("T", "U"), rna[::-1], "".join({"A": "G", "G": "A", "T": "C", "C": "T"}[b] for b in seq)]
    return make(BIO, f"Una hebra molde de ADN tiene la secuencia {seq}. ¿Qué secuencia tendrá el ARN mensajero transcrito a partir de ella?", rna, w,
                "En la transcripción, A del ADN se aparea con U del ARN, T con A, G con C y C con G.")


def t_chargaff():
    a = rnd.randrange(10, 41)
    g = (100 - 2 * a) / 2
    ask = rnd.choice(["timina", "guanina", "citosina"])
    v = a if ask == "timina" else g
    c, w = numeric_options(v, [100 - a, a if v != a else g, 100 - 2 * a, 50 - a / 2], step=5, fn=lambda x: f"{fmt(x)}%")
    return make(BIO, f"En una molécula de ADN de doble hebra, el {a}% de las bases nitrogenadas son adenina. ¿Qué porcentaje corresponde a {ask}?", c, w,
                f"A = T = {a}%; G = C = (100 − 2·{a})/2 = {fmt(g)}%.")


def t_codons():
    n = rnd.randint(4, 120) * 3
    c, w = numeric_options(n // 3, [n, n * 3, n // 2], step=2)
    return make(BIO, f"Un ARN mensajero tiene {n} nucleótidos que codifican aminoácidos (sin contar codones de término). ¿Cuántos aminoácidos tendrá la proteína?", c, w,
                f"Cada codón tiene 3 nucleótidos y codifica un aminoácido: {n}/3 = {n // 3}.")


SPECIES = [("el ser humano", 46), ("el perro", 78), ("el gato", 38), ("el chimpancé", 48), ("la mosca de la fruta", 8), ("la arveja", 14),
           ("la cebolla", 16), ("el caballo", 64), ("el maíz", 20), ("la vaca", 60)]


def t_chromosomes():
    sp, n2 = rnd.choice(SPECIES)
    de = ("del " + sp[3:]) if sp.startswith("el ") else ("de " + sp)
    k = rnd.randint(1, 3)
    if k == 1:
        c, w = numeric_options(n2 // 2, [n2, n2 * 2, n2 // 4 or 3], step=2)
        return make(BIO, f"Las células somáticas {de} tienen {n2} cromosomas (2n = {n2}). ¿Cuántos cromosomas tiene cada uno de sus gametos?", c, w, f"La meiosis reduce el número a la mitad: n = {n2 // 2}.")
    if k == 2:
        c, w = numeric_options(n2, [n2 // 2, n2 * 2, n2 + 2], step=2)
        return make(BIO, f"Una célula somática {de} (2n = {n2}) se divide por mitosis. ¿Cuántos cromosomas tiene cada célula hija?", c, w, f"La mitosis produce células idénticas a la original: {n2} cromosomas.")
    c, w = numeric_options(n2, [n2 // 2, n2 * 2, n2 + 1], step=2)
    return make(BIO, f"Un óvulo y un espermatozoide {de} tienen {n2 // 2} cromosomas cada uno. ¿Cuántos cromosomas tendrá el cigoto que se forma en la fecundación?", c, w, f"{n2 // 2} + {n2 // 2} = {n2} cromosomas (2n).")


def t_energy_chain():
    E = rnd.choice([1000, 5000, 10000, 20000, 50000, 100000])
    lvl = rnd.randint(2, 4)
    names = {2: "consumidores primarios", 3: "consumidores secundarios", 4: "consumidores terciarios"}
    v = E // 10 ** (lvl - 1)
    c, w = numeric_options(v, [E // 10 ** lvl, E // 10 ** (lvl - 2) if lvl > 2 else E // 2, E // (10 * (lvl - 1))], step=v // 2 or 1, fn=unit("kcal"))
    return make(BIO, f"Los productores de un ecosistema fijan {fint(E)} kcal. Si en cada nivel trófico pasa aproximadamente el 10% de la energía al siguiente, ¿cuánta energía llega a los {names[lvl]}?", c, w,
                f"Se multiplica por 0,1 en cada paso: {fint(E)}·0,1{sup(lvl - 1)} = {fint(v)} kcal.")


CALC_TEMPLATES = [t_mru, t_kmh, t_accel, t_free_fall, t_newton2, t_weight, t_energy, t_work_power, t_ohm, t_circuits, t_elec_power,
                  t_wave, t_echo, t_pressure_density, t_heat, t_hooke_momentum,
                  t_subatomic, t_molar, t_avogadro, t_solutions, t_ph, t_gases, t_stoich, t_kelvin, t_hydrocarbon,
                  t_mono, t_dihybrid, t_dna, t_chargaff, t_codons, t_chromosomes, t_energy_chain]


# ===================================================== CONCEPTOS (bancos)
def low(t):
    """Primera letra en minúscula, salvo símbolos o siglas."""
    return t if (len(t) < 3 or t[1].isupper() or not t[0].isalpha()) else t[0].lower() + t[1:]


def matching(eje, pairs, q_fwd, q_back, expl):
    """Crea preguntas en ambos sentidos a partir de pares (nombre, descripción)."""
    out = []
    names = [a for a, _ in pairs]
    descs = [b for _, b in pairs]
    for a, b in pairs:
        if q_fwd:
            out.append((eje, q_fwd.format(a=a), b, [d for d in descs if d != b], expl.format(a=a, b=low(b))))
        if q_back:
            out.append((eje, q_back.format(b=low(b)), a, [n for n in names if n != a], expl.format(a=a, b=low(b))))
    return out


FACTS = []

FACTS += matching(BIO, [
    ("Núcleo", "Contiene la mayor parte del material genético de la célula"),
    ("Mitocondria", "Realiza la respiración celular y produce la mayor parte del ATP"),
    ("Cloroplasto", "Realiza la fotosíntesis"),
    ("Ribosoma", "Sintetiza proteínas"),
    ("Aparato de Golgi", "Modifica, empaqueta y distribuye proteínas"),
    ("Lisosoma", "Realiza la digestión intracelular mediante enzimas"),
    ("Retículo endoplasmático liso", "Sintetiza lípidos"),
    ("Membrana plasmática", "Regula el paso de sustancias entre la célula y su entorno"),
    ("Pared celular", "Da soporte y protección a las células vegetales"),
    ("Vacuola central", "Almacena agua y mantiene la turgencia de las células vegetales"),
], "¿Cuál es la función principal de la estructura celular llamada «{a}»?", "¿Qué estructura celular {b}?", "{a}: {b}.")

FACTS += matching(BIO, [
    ("Insulina", "Disminuye la concentración de glucosa en la sangre"),
    ("Glucagón", "Aumenta la concentración de glucosa en la sangre"),
    ("Tiroxina", "Regula la velocidad del metabolismo"),
    ("Hormona del crecimiento", "Estimula el crecimiento de huesos y tejidos"),
    ("Adrenalina", "Prepara al organismo para responder ante situaciones de estrés o peligro"),
    ("Hormona antidiurética (ADH)", "Aumenta la reabsorción de agua en los riñones"),
    ("Oxitocina", "Estimula las contracciones del útero durante el parto"),
    ("Progesterona", "Prepara y mantiene el endometrio para un posible embarazo"),
], "¿Cuál es el efecto principal de la hormona «{a}»?", "¿Qué hormona {b}?", "{a}: {b}.")

FACTS += matching(BIO, [
    ("Mutualismo", "Ambas especies se benefician de la relación"),
    ("Comensalismo", "Una especie se beneficia y la otra no se ve afectada"),
    ("Parasitismo", "Una especie se beneficia a costa de la otra, que se ve perjudicada"),
    ("Depredación", "Una especie captura y se alimenta de otra"),
    ("Competencia", "Dos especies usan el mismo recurso limitado y ambas se perjudican"),
], "¿Qué caracteriza a la interacción ecológica llamada «{a}»?", "¿Cómo se llama la interacción en que {b}?", "{a}: {b}.")

FACTS += matching(BIO, [
    ("Profase", "Los cromosomas se condensan y la envoltura nuclear se desintegra"),
    ("Metafase", "Los cromosomas se alinean en el plano ecuatorial de la célula"),
    ("Anafase", "Las cromátidas hermanas se separan hacia polos opuestos"),
    ("Telofase", "Se forman nuevas envolturas nucleares alrededor de cada grupo de cromosomas"),
], "¿Qué ocurre durante la etapa de la mitosis llamada «{a}»?", "¿En qué fase de la mitosis {b}?", "{a}: {b}.")

MONO = [("Proteínas", "Aminoácidos"), ("Ácidos nucleicos", "Nucleótidos"), ("Polisacáridos (como el almidón)", "Monosacáridos (como la glucosa)")]
MONO_W = ["Aminoácidos", "Nucleótidos", "Monosacáridos (como la glucosa)", "Ácidos grasos y glicerol", "Fosfolípidos"]
FACTS += [(BIO, f"¿Cuáles son los monómeros (unidades básicas) que forman las moléculas de tipo «{a}»?", b, [x for x in MONO_W if x != b], f"{a}: están formados por {b.lower()}.") for a, b in MONO]

FACTS += matching(BIO, [
    ("Inmunidad activa natural", "Se genera al enfermarse y producir anticuerpos propios"),
    ("Inmunidad activa artificial", "Se genera al recibir una vacuna"),
    ("Inmunidad pasiva natural", "Se adquiere al recibir anticuerpos de la madre, por ejemplo a través de la leche materna"),
    ("Inmunidad pasiva artificial", "Se adquiere al recibir anticuerpos ya formados, como en un suero"),
], None, "¿Qué tipo de inmunidad {b}?", "{a}: {b}.")

FACTS += matching(BIO, [
    ("Dendritas", "Reciben los impulsos nerviosos de otras neuronas"),
    ("Axón", "Conduce el impulso nervioso desde el cuerpo celular hacia otras células"),
    ("Vaina de mielina", "Aísla el axón y aumenta la velocidad del impulso nervioso"),
    ("Sinapsis", "Permite la comunicación entre una neurona y otra célula"),
], "En el sistema nervioso, ¿qué función cumple la estructura llamada «{a}»?", "¿Qué estructura del sistema nervioso {b}?", "{a}: {b}.")

FACTS += [
    (BIO, "¿Cuáles son los productos de la fotosíntesis?", "Glucosa y oxígeno", ["Dióxido de carbono y agua", "Glucosa y dióxido de carbono", "Oxígeno y agua", "ATP y ácido láctico"],
     "En la fotosíntesis, CO₂ y agua, usando energía luminosa, forman glucosa y O₂."),
    (BIO, "¿Cuáles son los productos de la respiración celular aeróbica?", "Dióxido de carbono, agua y energía (ATP)", ["Glucosa y oxígeno", "Ácido láctico y ATP", "Etanol y dióxido de carbono", "Oxígeno y agua"],
     "La glucosa se oxida con O₂ y se liberan CO₂, H₂O y energía en forma de ATP."),
    (BIO, "¿Qué producto se forma en la fermentación láctica que ocurre en los músculos durante un ejercicio intenso?", "Ácido láctico", ["Etanol", "Glucosa", "Oxígeno", "Almidón"],
     "Sin suficiente O₂, las células musculares transforman el piruvato en ácido láctico."),
    (BIO, "¿Qué productos forma la fermentación alcohólica que realizan las levaduras?", "Etanol y dióxido de carbono", ["Ácido láctico y oxígeno", "Glucosa y oxígeno", "Agua y oxígeno", "Almidón y etanol"],
     "Las levaduras transforman la glucosa en etanol y CO₂; por eso se usan para hacer pan y vino."),
    (BIO, "¿Cuál es una diferencia correcta entre mitosis y meiosis?", "La mitosis produce 2 células idénticas y la meiosis produce 4 células con la mitad de cromosomas",
     ["La mitosis produce gametos y la meiosis produce células del cuerpo", "Ambas producen 4 células haploides", "La meiosis produce 2 células idénticas a la célula madre", "La mitosis reduce el número de cromosomas a la mitad"],
     "La mitosis mantiene el número de cromosomas; la meiosis lo reduce a la mitad y forma gametos."),
    (BIO, "¿En qué etapa de la meiosis ocurre el entrecruzamiento (crossing-over) entre cromosomas homólogos?", "Profase I", ["Metafase II", "Anafase I", "Telofase II", "Interfase"],
     "En la profase I los cromosomas homólogos se aparean e intercambian fragmentos."),
    (BIO, "¿Qué científico propuso la selección natural como mecanismo de la evolución?", "Charles Darwin", ["Jean-Baptiste Lamarck", "Gregor Mendel", "Louis Pasteur", "Robert Hooke"],
     "Darwin (junto con Wallace) propuso que los individuos mejor adaptados sobreviven y se reproducen más."),
    (BIO, "La idea de que las características adquiridas durante la vida se heredan a la descendencia corresponde a:", "Jean-Baptiste Lamarck", ["Charles Darwin", "Gregor Mendel", "Alfred Wallace", "James Watson"],
     "Lamarck propuso la herencia de caracteres adquiridos, idea que hoy no es aceptada."),
    (BIO, "El brazo humano y el ala de un murciélago tienen huesos similares aunque cumplen funciones distintas. ¿Cómo se llaman estas estructuras?", "Estructuras homólogas", ["Estructuras análogas", "Estructuras vestigiales", "Estructuras convergentes", "Mutaciones"],
     "Las estructuras homólogas tienen el mismo origen evolutivo, aunque su función pueda ser distinta."),
    (BIO, "El ala de un ave y el ala de una mariposa cumplen la misma función pero tienen origen distinto. ¿Cómo se llaman estas estructuras?", "Estructuras análogas", ["Estructuras homólogas", "Estructuras vestigiales", "Órganos idénticos", "Fósiles guía"],
     "Las estructuras análogas cumplen la misma función, pero no comparten origen evolutivo."),
    (BIO, "¿Qué células del sistema inmune producen anticuerpos?", "Linfocitos B (células plasmáticas)", ["Glóbulos rojos", "Plaquetas", "Neuronas", "Linfocitos T citotóxicos"],
     "Los linfocitos B se diferencian en células plasmáticas, que secretan anticuerpos."),
    (BIO, "¿Qué organismos de un ecosistema transforman la materia orgánica muerta en sustancias inorgánicas?", "Los descomponedores", ["Los productores", "Los consumidores primarios", "Los consumidores secundarios", "Los herbívoros"],
     "Hongos y bacterias descomponedoras reciclan la materia y devuelven nutrientes al suelo."),
    (BIO, "¿Qué organismos de un ecosistema fabrican su propio alimento a partir de energía luminosa?", "Los productores", ["Los descomponedores", "Los consumidores primarios", "Los carnívoros", "Los parásitos"],
     "Los productores (plantas, algas) realizan fotosíntesis."),
    (BIO, "¿Cuál de los siguientes gases es el principal responsable del aumento del efecto invernadero por actividades humanas?", "Dióxido de carbono (CO₂)", ["Oxígeno (O₂)", "Nitrógeno (N₂)", "Argón (Ar)", "Helio (He)"],
     "La quema de combustibles fósiles libera CO₂, que retiene calor en la atmósfera."),
    (BIO, "En la molécula de ADN, ¿qué base nitrogenada se aparea con la citosina?", "Guanina", ["Adenina", "Timina", "Uracilo", "Citosina"], "En el ADN, G se aparea con C y A con T."),
    (BIO, "¿Qué base nitrogenada está presente en el ARN pero no en el ADN?", "Uracilo", ["Timina", "Adenina", "Guanina", "Citosina"], "El ARN tiene uracilo en lugar de timina."),
    (BIO, "¿Dónde ocurre la transcripción del ADN en una célula eucarionte?", "En el núcleo", ["En el ribosoma", "En la mitocondria", "En el aparato de Golgi", "En la membrana plasmática"],
     "El ARN mensajero se forma en el núcleo y luego sale al citoplasma."),
    (BIO, "¿Dónde ocurre la traducción del ARN mensajero a proteína?", "En los ribosomas", ["En el núcleo", "En los lisosomas", "En la vacuola", "En la pared celular"],
     "Los ribosomas leen los codones del ARNm y unen los aminoácidos."),
    (BIO, "Un individuo con genotipo Aa para un gen se denomina:", "Heterocigoto", ["Homocigoto dominante", "Homocigoto recesivo", "Haploide", "Mutante"], "Tiene dos alelos distintos del mismo gen."),
    (BIO, "¿Qué tipo de célula NO tiene núcleo definido?", "Célula procarionte (bacteria)", ["Célula animal", "Célula vegetal", "Célula de hongo", "Neurona"],
     "En las procariontes el ADN está libre en el citoplasma, sin envoltura nuclear."),
    (BIO, "El paso de agua a través de una membrana semipermeable desde una zona con menos solutos a otra con más solutos se llama:", "Osmosis", ["Difusión facilitada", "Transporte activo", "Endocitosis", "Fagocitosis"],
     "En la osmosis el agua se mueve hacia donde hay mayor concentración de solutos."),
    (BIO, "¿Qué tipo de transporte a través de la membrana requiere gasto de energía (ATP)?", "Transporte activo", ["Difusión simple", "Osmosis", "Difusión facilitada", "Filtración pasiva"],
     "El transporte activo mueve sustancias contra su gradiente de concentración usando ATP."),
    (BIO, "Si se coloca un glóbulo rojo en agua destilada, ¿qué le ocurre?", "Se hincha y puede romperse, porque entra agua por osmosis", ["Se arruga, porque pierde agua", "No le ocurre nada", "Pierde todas sus proteínas", "Se divide por mitosis"],
     "El agua destilada es hipotónica respecto del glóbulo rojo, por lo que entra agua a la célula."),
]

FACTS += matching(QUI, [
    ("Sodio", "Na"), ("Potasio", "K"), ("Hierro", "Fe"), ("Oro", "Au"), ("Plata", "Ag"), ("Cobre", "Cu"),
    ("Plomo", "Pb"), ("Mercurio", "Hg"), ("Calcio", "Ca"), ("Fósforo", "P"), ("Azufre", "S"), ("Nitrógeno", "N"),
], "¿Cuál es el símbolo químico del elemento «{a}»?", None, "El símbolo de {a} es {b}.")

BONDS = [("NaCl", "Iónico"), ("KCl", "Iónico"), ("MgO", "Iónico"), ("CaF₂", "Iónico"), ("H₂O", "Covalente polar"), ("HCl", "Covalente polar"),
         ("NH₃", "Covalente polar"), ("O₂", "Covalente apolar"), ("N₂", "Covalente apolar"), ("Cl₂", "Covalente apolar"), ("un trozo de cobre (Cu)", "Metálico"),
         ("un clavo de hierro (Fe)", "Metálico")]
BOND_EXPL = {"Iónico": "Se une un metal con un no metal: hay transferencia de electrones.",
             "Covalente polar": "Se comparten electrones entre no metales de distinta electronegatividad.",
             "Covalente apolar": "Se comparten electrones entre átomos iguales (misma electronegatividad).",
             "Metálico": "Los átomos de un metal comparten una 'nube' de electrones móviles."}
FACTS += [(QUI, f"¿Qué tipo de enlace químico predomina en {s}?", t, [x for x in BOND_EXPL if x != t], BOND_EXPL[t]) for s, t in BONDS]

FACTS += matching(QUI, [
    ("Etanol", "Alcohol"), ("Ácido acético", "Ácido carboxílico"), ("Propanona (acetona)", "Cetona"),
    ("Metanal (formaldehído)", "Aldehído"), ("Metilamina", "Amina"), ("Acetato de etilo", "Éster"),
], "¿A qué función orgánica pertenece el compuesto «{a}»?", None, "{a} pertenece a la función {b}.")

FACTS += matching(QUI, [
    ("Alcohol", "–OH unido a un carbono saturado"), ("Ácido carboxílico", "–COOH"), ("Amina", "–NH₂"), ("Aldehído", "–CHO (carbonilo en un extremo)"),
], "¿Qué grupo funcional caracteriza a la función orgánica «{a}»?", None, "{a}: grupo {b}.")

FACTS += matching(QUI, [
    ("Litio (Li)", "Metales alcalinos (grupo 1)"), ("Sodio (Na)", "Metales alcalinos (grupo 1)"), ("Magnesio (Mg)", "Metales alcalinotérreos (grupo 2)"),
    ("Calcio (Ca)", "Metales alcalinotérreos (grupo 2)"), ("Cloro (Cl)", "Halógenos (grupo 17)"), ("Flúor (F)", "Halógenos (grupo 17)"),
    ("Neón (Ne)", "Gases nobles (grupo 18)"), ("Argón (Ar)", "Gases nobles (grupo 18)"),
], "¿A qué familia de la tabla periódica pertenece el {a}?", None, "{a} pertenece a {b}.")

REACT_TYPES = [("2 H₂ + O₂ → 2 H₂O", "Síntesis"), ("2 Na + Cl₂ → 2 NaCl", "Síntesis"), ("CaCO₃ → CaO + CO₂", "Descomposición"),
               ("2 H₂O₂ → 2 H₂O + O₂", "Descomposición"), ("Zn + 2 HCl → ZnCl₂ + H₂", "Sustitución simple"),
               ("Fe + CuSO₄ → FeSO₄ + Cu", "Sustitución simple"), ("NaOH + HCl → NaCl + H₂O", "Neutralización"), ("KOH + HNO₃ → KNO₃ + H₂O", "Neutralización")]
FACTS += [(QUI, f"¿Qué tipo de reacción química representa la ecuación {e}?", t, [x for x in ["Síntesis", "Descomposición", "Sustitución simple", "Neutralización"] if x != t],
           {"Síntesis": "Dos o más sustancias se unen para formar una sola.", "Descomposición": "Una sustancia se separa en otras más simples.",
            "Sustitución simple": "Un elemento reemplaza a otro en un compuesto.", "Neutralización": "Un ácido reacciona con una base y forma sal y agua."}[t]) for e, t in REACT_TYPES]

SEPAR = [("agua y arena", "Filtración"), ("agua y aceite", "Decantación"), ("agua y sal disuelta, para recuperar la sal", "Evaporación"),
         ("agua y alcohol", "Destilación"), ("limaduras de hierro y arena", "Separación magnética"), ("piedras pequeñas y arena fina", "Tamizado")]
SEP_EXPL = {"Filtración": "Separa un sólido insoluble de un líquido.", "Decantación": "Separa líquidos que no se mezclan (inmiscibles), por diferencia de densidad.",
            "Evaporación": "Se evapora el líquido y queda el sólido que estaba disuelto.", "Destilación": "Separa líquidos con distinto punto de ebullición.",
            "Separación magnética": "Un imán atrae al hierro y lo separa.", "Tamizado": "Separa sólidos de distinto tamaño con un tamiz o colador."}
FACTS += [(QUI, f"¿Qué método es el más adecuado para separar una mezcla de {m}?", t, [x for x in SEP_EXPL if x != t], SEP_EXPL[t]) for m, t in SEPAR]

FACTS += matching(QUI, [
    ("Fusión", "Paso de sólido a líquido"), ("Solidificación", "Paso de líquido a sólido"), ("Vaporización", "Paso de líquido a gas"),
    ("Condensación", "Paso de gas a líquido"), ("Sublimación", "Paso directo de sólido a gas"), ("Deposición (sublimación inversa)", "Paso directo de gas a sólido"),
], None, "¿Cómo se llama el cambio de estado que corresponde al {b}?", "{a}: {b}.")

PH_EX = [("jugo de limón", "Ácida"), ("vinagre", "Ácida"), ("agua pura a 25 °C", "Neutra"), ("solución de bicarbonato de sodio", "Básica"),
         ("cloro doméstico (lejía)", "Básica"), ("jugo gástrico", "Ácida"), ("agua jabonosa", "Básica")]
FACTS += [(QUI, f"¿Cómo se clasifica el {s} según su pH?", t, [x for x in ["Ácida", "Neutra", "Básica", "No tiene pH"] if x != t],
           f"El {s} tiene pH {'menor que 7' if t == 'Ácida' else ('igual a 7' if t == 'Neutra' else 'mayor que 7')}.") for s, t in PH_EX]

FACTS += [
    (QUI, "¿Qué partícula subatómica tiene carga eléctrica negativa?", "Electrón", ["Protón", "Neutrón", "Núcleo"], "El electrón tiene carga negativa y se encuentra fuera del núcleo."),
    (QUI, "¿Qué partícula subatómica no tiene carga eléctrica?", "Neutrón", ["Protón", "Electrón", "Ion"], "El neutrón es neutro y se encuentra en el núcleo, junto a los protones."),
    (QUI, "¿Qué indica el número atómico (Z) de un elemento?", "La cantidad de protones de su núcleo", ["La suma de protones y neutrones", "La cantidad de neutrones", "La masa del átomo en gramos", "La cantidad de moléculas"],
     "Z es el número de protones; identifica al elemento."),
    (QUI, "Dos átomos que tienen el mismo número de protones pero distinto número de neutrones se llaman:", "Isótopos", ["Isóbaros", "Iones", "Moléculas", "Alótropos"],
     "Los isótopos son átomos del mismo elemento con distinto número másico."),
    (QUI, "En un período de la tabla periódica, al avanzar de izquierda a derecha, el radio atómico en general:", "Disminuye", ["Aumenta", "No cambia", "Primero disminuye y luego se duplica"],
     "Al aumentar la carga nuclear, los electrones son atraídos con más fuerza y el átomo se hace más pequeño."),
    (QUI, "En un grupo de la tabla periódica, al bajar, la electronegatividad en general:", "Disminuye", ["Aumenta", "No cambia", "Se vuelve cero"],
     "Los electrones de valencia están más lejos del núcleo y son atraídos con menos fuerza."),
    (QUI, "¿Cuál es el elemento más electronegativo de la tabla periódica?", "Flúor", ["Cesio", "Oxígeno", "Hidrógeno", "Neón"], "El flúor tiene la mayor electronegatividad (4,0 en la escala de Pauling)."),
    (QUI, "¿Cuál de las siguientes es una mezcla homogénea?", "Agua con sal disuelta", ["Agua con arena", "Agua con aceite", "Ensalada de frutas", "Granito"],
     "En una mezcla homogénea no se distinguen sus componentes a simple vista."),
    (QUI, "¿Cuál de las siguientes es una sustancia pura compuesta?", "Agua destilada (H₂O)", ["Aire", "Agua de mar", "Oxígeno (O₂)", "Bebida gaseosa"],
     "El agua destilada está formada por un solo tipo de molécula con dos elementos distintos."),
    (QUI, "Según la ley de conservación de la masa (Lavoisier), en una reacción química en un sistema cerrado:", "La masa total de reactivos es igual a la masa total de productos",
     ["La masa de los productos siempre es mayor", "La masa de los productos siempre es menor", "Se crean átomos nuevos", "Desaparecen los átomos de los reactivos"],
     "Los átomos solo se reorganizan; no se crean ni se destruyen."),
    (QUI, "¿Qué efecto tiene un catalizador sobre una reacción química?", "Aumenta la velocidad de reacción sin consumirse", ["Cambia los productos de la reacción", "Disminuye siempre la temperatura", "Se transforma en producto", "Detiene la reacción"],
     "Un catalizador disminuye la energía de activación y se recupera al final."),
    (QUI, "Si se aumenta la temperatura, la velocidad de la mayoría de las reacciones químicas:", "Aumenta", ["Disminuye", "No cambia", "Se vuelve cero"],
     "Las partículas se mueven más rápido y chocan con más energía y frecuencia."),
    (QUI, "Una reacción que libera calor al entorno se llama:", "Exotérmica", ["Endotérmica", "Neutra", "Catalítica", "Isotérmica"], "Exo = hacia afuera: libera energía térmica."),
    (QUI, "Una reacción que absorbe calor del entorno se llama:", "Endotérmica", ["Exotérmica", "De combustión", "Espontánea", "De neutralización"], "Endo = hacia adentro: absorbe energía térmica."),
    (QUI, "¿Cuántos electrones de valencia tienen los elementos del grupo 17 (halógenos)?", "7", ["1", "2", "8"], "Los halógenos tienen 7 electrones en su último nivel y tienden a ganar 1."),
    (QUI, "¿Qué gas se libera en la combustión completa de un hidrocarburo, además de vapor de agua?", "Dióxido de carbono", ["Hidrógeno", "Oxígeno", "Monóxido de nitrógeno", "Helio"],
     "La combustión completa de un hidrocarburo produce CO₂ y H₂O."),
    (QUI, "¿Cuántos enlaces covalentes forma normalmente un átomo de carbono en los compuestos orgánicos?", "4", ["2", "3", "6"], "El carbono es tetravalente."),
    (QUI, "Los compuestos que tienen la misma fórmula molecular pero distinta estructura se llaman:", "Isómeros", ["Isótopos", "Polímeros", "Alótropos", "Iones"],
     "Por ejemplo, butano e isobutano tienen la fórmula C₄H₁₀."),
]

UNITS = [("Fuerza", "Newton (N)"), ("Energía", "Joule (J)"), ("Potencia", "Watt (W)"), ("Presión", "Pascal (Pa)"), ("Frecuencia", "Hertz (Hz)"),
         ("Carga eléctrica", "Coulomb (C)"), ("Resistencia eléctrica", "Ohm (Ω)"), ("Corriente eléctrica", "Ampere (A)"), ("Voltaje", "Volt (V)")]
FACTS += matching(FIS, UNITS, "En el Sistema Internacional, ¿cuál es la unidad de la magnitud «{a}»?", None, "La unidad SI de {a} es el {b}.")

VEC = ["Velocidad", "Fuerza", "Aceleración", "Desplazamiento", "Momentum lineal"]
ESC = ["Masa", "Temperatura", "Tiempo", "Energía", "Rapidez", "Distancia recorrida"]
for v in VEC:
    FACTS.append((FIS, "¿Cuál de las siguientes magnitudes es vectorial?", v, ESC, f"{v} es vectorial: necesita módulo, dirección y sentido."))
for e in ESC:
    FACTS.append((FIS, "¿Cuál de las siguientes magnitudes es escalar?", e, VEC, f"{e} es escalar: queda definida solo con su valor y unidad."))

NEWTON = [("Cuando un bus frena bruscamente, los pasajeros se inclinan hacia adelante.", "Primera ley (inercia)"),
          ("Al retirar muy rápido un mantel, la vajilla que está encima se queda en la mesa.", "Primera ley (inercia)"),
          ("Con la misma fuerza, un carro de supermercado vacío acelera más que uno lleno.", "Segunda ley (F = m·a)"),
          ("Para acelerar más rápido una bicicleta, hay que aplicar una fuerza mayor en los pedales.", "Segunda ley (F = m·a)"),
          ("Un cohete expulsa gases hacia abajo y se impulsa hacia arriba.", "Tercera ley (acción y reacción)"),
          ("Al remar, el remo empuja el agua hacia atrás y el bote avanza hacia adelante.", "Tercera ley (acción y reacción)"),
          ("Al saltar desde un bote hacia el muelle, el bote se mueve hacia atrás.", "Tercera ley (acción y reacción)")]
FACTS += [(FIS, f"«{s}» ¿Qué ley de Newton explica mejor esta situación?", t,
           [x for x in ["Primera ley (inercia)", "Segunda ley (F = m·a)", "Tercera ley (acción y reacción)", "Ley de gravitación universal"] if x != t],
           {"Primera ley (inercia)": "Un cuerpo tiende a mantener su estado de reposo o movimiento si no actúa una fuerza neta.",
            "Segunda ley (F = m·a)": "La aceleración es proporcional a la fuerza neta e inversamente proporcional a la masa.",
            "Tercera ley (acción y reacción)": "A toda acción le corresponde una reacción de igual módulo y sentido contrario."}[t]) for s, t in NEWTON]

WAVE_PHEN = [("Escuchar el eco de la voz en una quebrada.", "Reflexión"), ("Un lápiz dentro de un vaso con agua parece quebrado.", "Refracción"),
             ("Se escucha a una persona que habla detrás de una pared, aunque no se la vea.", "Difracción"),
             ("La sirena de una ambulancia se oye más aguda al acercarse y más grave al alejarse.", "Efecto Doppler"),
             ("Una copa de cristal se quiebra cuando un cantante emite una nota de la misma frecuencia natural de la copa.", "Resonancia")]
FACTS += [(FIS, f"«{s}» ¿Qué fenómeno ondulatorio se describe?", t, [x for x in ["Reflexión", "Refracción", "Difracción", "Efecto Doppler", "Resonancia"] if x != t],
           {"Reflexión": "La onda rebota al chocar con una superficie.", "Refracción": "La onda cambia de rapidez y dirección al pasar de un medio a otro.",
            "Difracción": "La onda rodea obstáculos o pasa por aberturas.", "Efecto Doppler": "La frecuencia percibida cambia por el movimiento relativo de la fuente.",
            "Resonancia": "Un cuerpo vibra con gran amplitud al recibir ondas de su frecuencia natural."}[t]) for s, t in WAVE_PHEN]

HEAT = [("Una cuchara metálica se calienta entera al dejar un extremo en una taza de té caliente.", "Conducción"),
        ("El agua del fondo de una olla se calienta, sube, y el agua fría baja.", "Convección"),
        ("Sentimos el calor del Sol aunque entre el Sol y la Tierra casi no hay materia.", "Radiación"),
        ("El aire caliente de una estufa sube y calienta la habitación.", "Convección"),
        ("Al tocar una sartén caliente, el calor pasa a la mano.", "Conducción"),
        ("Una fogata calienta la cara de quien está frente a ella.", "Radiación")]
FACTS += [(FIS, f"«{s}» ¿Por qué mecanismo se transmite principalmente el calor?", t, [x for x in ["Conducción", "Convección", "Radiación", "Evaporación"] if x != t],
           {"Conducción": "El calor pasa por contacto directo entre partículas.", "Convección": "El calor se transporta por el movimiento de un fluido.",
            "Radiación": "El calor viaja como ondas electromagnéticas, incluso en el vacío."}[t]) for s, t in HEAT]

FACTS += [
    (FIS, "¿Cuál de las siguientes afirmaciones sobre el sonido es correcta?", "Es una onda mecánica y no se propaga en el vacío", ["Es una onda electromagnética", "Se propaga más rápido en el vacío", "Es una onda transversal en el aire", "Viaja a la misma rapidez que la luz"],
     "El sonido necesita un medio material; en el aire es una onda longitudinal."),
    (FIS, "¿Qué característica del sonido depende principalmente de la frecuencia?", "El tono (agudo o grave)", ["La intensidad (fuerte o débil)", "El timbre", "La rapidez en el aire"], "A mayor frecuencia, el sonido es más agudo."),
    (FIS, "¿Qué característica del sonido depende principalmente de la amplitud de la onda?", "La intensidad (volumen)", ["El tono", "El timbre", "La longitud de onda"], "A mayor amplitud, el sonido se percibe más fuerte."),
    (FIS, "La característica que permite distinguir una misma nota tocada por un piano y por una guitarra es:", "El timbre", ["El tono", "La intensidad", "La rapidez"], "El timbre depende de la forma de la onda (sus armónicos)."),
    (FIS, "¿Cuál de las siguientes ondas electromagnéticas tiene mayor frecuencia?", "Rayos gamma", ["Ondas de radio", "Microondas", "Luz visible", "Infrarrojo"], "En orden creciente de frecuencia: radio, microondas, infrarrojo, visible, ultravioleta, rayos X, gamma."),
    (FIS, "¿Cuál de las siguientes ondas electromagnéticas tiene mayor longitud de onda?", "Ondas de radio", ["Rayos X", "Ultravioleta", "Luz visible", "Rayos gamma"], "La longitud de onda es mayor cuando la frecuencia es menor."),
    (FIS, "¿Cuál de los siguientes materiales es un buen conductor eléctrico?", "Cobre", ["Plástico", "Vidrio", "Goma", "Madera seca"], "Los metales tienen electrones libres que transportan la carga."),
    (FIS, "¿Cuál de los siguientes materiales es un aislante eléctrico?", "Goma", ["Cobre", "Aluminio", "Hierro", "Agua salada"], "En los aislantes los electrones no se mueven con facilidad."),
    (FIS, "Al frotar un globo con el pelo, el globo queda cargado. ¿Qué ocurrió?", "Hubo transferencia de electrones entre el pelo y el globo", ["Se crearon cargas nuevas", "Se transfirieron protones", "El globo se volvió conductor", "El pelo perdió neutrones"],
     "La electrización por frotamiento transfiere electrones; la carga total se conserva."),
    (FIS, "¿Qué capa de la Tierra se encuentra en estado líquido?", "El núcleo externo", ["La corteza", "El núcleo interno", "La litosfera", "El manto superior completo"], "El núcleo externo es líquido y su movimiento genera el campo magnético terrestre."),
    (FIS, "¿Qué tipo de ondas sísmicas no se propaga a través de líquidos?", "Ondas S (secundarias)", ["Ondas P (primarias)", "Todas las ondas sísmicas", "Ondas de radio"], "Las ondas S son transversales y no atraviesan líquidos; por eso se sabe que el núcleo externo es líquido."),
    (FIS, "¿Cuáles son las ondas sísmicas que llegan primero a una estación de registro?", "Ondas P", ["Ondas S", "Ondas superficiales", "Ondas de sonido"], "Las ondas P son las más rápidas."),
    (FIS, "La gran actividad sísmica de Chile se debe principalmente a:", "La subducción de la placa de Nazca bajo la placa Sudamericana", ["La separación de la placa Sudamericana y la Africana", "Las mareas producidas por la Luna", "La erosión de la cordillera", "El calor del Sol"],
     "En un límite convergente, una placa oceánica se hunde bajo una continental."),
    (FIS, "La escala que mide la energía liberada por un sismo (magnitud) es:", "La escala de magnitud (Richter o de momento)", ["La escala de Mercalli", "La escala de Celsius", "La escala de pH", "La escala de Beaufort"],
     "Mercalli mide la intensidad (efectos observados); la magnitud mide la energía liberada."),
    (FIS, "¿Cuál es la principal causa de las estaciones del año en la Tierra?", "La inclinación del eje de rotación terrestre", ["La distancia variable entre la Tierra y el Sol", "La rotación de la Luna", "Los cambios en el tamaño del Sol", "Las mareas"],
     "La inclinación del eje hace que cada hemisferio reciba distinta cantidad de luz solar durante el año."),
    (FIS, "Un eclipse de Sol ocurre cuando:", "La Luna se interpone entre el Sol y la Tierra", ["La Tierra se interpone entre el Sol y la Luna", "El Sol se interpone entre la Tierra y la Luna", "La Luna está en fase llena"], "La sombra de la Luna cae sobre la Tierra."),
    (FIS, "Un eclipse de Luna ocurre cuando:", "La Tierra se interpone entre el Sol y la Luna", ["La Luna se interpone entre el Sol y la Tierra", "La Luna está en fase nueva", "El Sol se interpone entre la Tierra y la Luna"], "La sombra de la Tierra cae sobre la Luna."),
    (FIS, "Según la primera ley de Kepler, los planetas giran alrededor del Sol en órbitas:", "Elípticas, con el Sol en uno de sus focos", ["Circulares, con el Sol en el centro", "Rectas", "Parabólicas", "Cuadradas"], "Kepler demostró que las órbitas son elipses."),
    (FIS, "Si se lanza una pelota hacia arriba, en su punto más alto su velocidad es:", "Cero, y su aceleración sigue siendo la de gravedad", ["Máxima", "Igual a la inicial", "Cero, y su aceleración también es cero"], "En el punto más alto se detiene un instante, pero la gravedad sigue actuando."),
    (FIS, "En ausencia de roce, ¿qué ocurre con la energía mecánica de un péndulo que oscila?", "Se mantiene constante", ["Aumenta en cada oscilación", "Disminuye hasta cero", "Se transforma toda en calor"], "La energía se transforma entre cinética y potencial, pero la suma se conserva."),
    (FIS, "¿Qué es la temperatura de un cuerpo?", "Una medida de la energía cinética promedio de sus partículas", ["La cantidad total de calor que contiene", "La masa de sus partículas", "La presión que ejerce"],
     "El calor es energía en tránsito; la temperatura mide la agitación promedio de las partículas."),
    (FIS, "Dos cuerpos a distinta temperatura se ponen en contacto. ¿Qué ocurre?", "El calor fluye del más caliente al más frío hasta igualar sus temperaturas", ["El frío pasa del cuerpo frío al caliente", "Ambos se calientan", "No ocurre nada si son del mismo material"],
     "Se alcanza el equilibrio térmico."),
]


def fact_template_for(eje):
    items = [f for f in FACTS if f[0] == eje]

    def t():
        e, q, c, w, ex = rnd.choice(items)
        return make(e, q, c, rnd.sample(w, min(len(w), 5)), ex)
    t.__name__ = f"facts_{eje}"
    return t


FACT_TEMPLATES = [fact_template_for(e) for e in (BIO, QUI, FIS)]
