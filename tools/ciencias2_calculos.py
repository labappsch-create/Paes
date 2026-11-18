"""Preguntas de cálculo de Ciencias, solo con contenidos del temario oficial.
La respuesta la calcula el programa. Los números son sencillos porque en la prueba
real no se permite calculadora.
"""
from fractions import Fraction

from ciencias_comun import (ATO, ELE, EST, HER, MEC, OND, ORG, PROC, Skip, fint, fmt,
                            make, numeric_options, rnd, sup, unit)  # noqa: F401

OBJ = ["Un ciclista", "Un auto", "Un corredor", "Un tren", "Un bus", "Una persona en patines"]


# ===================================================================== FÍSICA: Mecánica
def t_mru():
    v, t = rnd.randint(2, 30), rnd.randint(2, 20)
    d = v * t
    k = rnd.randint(1, 3)
    obj = rnd.choice(OBJ)
    if k == 1:
        c, w = numeric_options(v, [d * t, d + t, d - t], step=2, fn=unit("m/s"))
        return make(MEC, f"{obj} recorre {fint(d)} m en {t} s con rapidez constante. ¿Cuál es su rapidez?", c, w,
                    f"v = d/t = {fint(d)}/{t} = {v} m/s.")
    if k == 2:
        c, w = numeric_options(d, [v + t, d // 2, d * 2], step=v, fn=unit("m"))
        return make(MEC, f"{obj} se mueve con rapidez constante de {v} m/s. ¿Qué distancia recorre en {t} s?", c, w,
                    f"d = v·t = {v}·{t} = {fint(d)} m.")
    c, w = numeric_options(t, [d * v, d - v, t * 2], step=1, fn=unit("s"))
    return make(MEC, f"{obj} viaja a {v} m/s constantes. ¿Cuánto tiempo tarda en recorrer {fint(d)} m?", c, w,
                f"t = d/v = {fint(d)}/{v} = {t} s.")


def t_kmh():
    kmh = rnd.choice([18, 36, 54, 72, 90, 108, 126, 144])
    ms = kmh * 5 // 18
    if rnd.random() < 0.5:
        c, w = numeric_options(ms, [kmh * 36 // 10, kmh // 36 or 1, kmh * 1000 // 60 // 10], step=5, fn=unit("m/s"))
        return make(MEC, f"Un vehículo se mueve a {kmh} km/h. ¿A cuántos metros por segundo equivale esa rapidez?", c, w,
                    f"Se divide por 3,6: {kmh}/3,6 = {ms} m/s.")
    c, w = numeric_options(kmh, [ms, ms * 10, ms * 36], step=18, fn=unit("km/h"))
    return make(MEC, f"Un corredor se mueve a {ms} m/s. ¿A cuántos kilómetros por hora equivale esa rapidez?", c, w,
                f"Se multiplica por 3,6: {ms}·3,6 = {kmh} km/h.")


def itinerario(x0, v):
    """Ecuación de itinerario del MRU escrita de forma natural: x(t) = 10 − 2·t, x(t) = 3·t."""
    vt = f"{abs(v)}·t" if abs(v) != 1 else "t"
    if x0 == 0:
        return f"x(t) = {'−' if v < 0 else ''}{vt}"
    return f"x(t) = {x0} {'+' if v > 0 else '−'} {vt}"


def t_itinerario_mru():
    x0 = rnd.choice([0, 5, 10, 20, 50, 100])
    v = rnd.choice([2, 3, 4, 5, 10, -2, -5])
    t = rnd.randint(2, 10)
    x = x0 + v * t
    eq = itinerario(x0, v)
    c, w = numeric_options(x, [x0 + v, v * t, x0 - v * t], step=abs(v), positive=False, fn=unit("m"))
    return make(MEC, f"La posición de un móvil está dada por la ecuación de itinerario {eq}, con x en metros y t en segundos. ¿Cuál es su posición en t = {t} s?",
                c, w, f"Se reemplaza t = {t} en {eq}: x = {fint(x)} m.")


def t_encuentro():
    d = rnd.choice([100, 120, 150, 200, 240, 300, 360, 400, 600])
    v1, v2 = rnd.choice([(2, 3), (3, 2), (4, 6), (5, 5), (10, 20), (6, 9), (5, 15), (8, 12)])
    if d % (v1 + v2):
        raise Skip()
    t = d // (v1 + v2)
    c, w = numeric_options(t, [d // v1 if d % v1 == 0 else t + 3, d // (v1 + v2) * 2, abs(v2 - v1) or t + 5], step=2, fn=unit("s"))
    return make(MEC, f"Dos ciclistas están separados por {d} m y avanzan en línea recta uno hacia el otro, con rapideces constantes de {v1} m/s y {v2} m/s. ¿Cuánto tiempo tardan en encontrarse?",
                c, w, f"Se acercan a {v1} + {v2} = {v1 + v2} m/s; t = {d}/{v1 + v2} = {t} s.")


def t_dist_desp():
    a, b, h = rnd.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17), (12, 16, 20)])
    if rnd.random() < 0.5:
        c, w = numeric_options(h, [a + b, b - a, a * b // 2], step=1, fn=unit("m"))
        return make(MEC, f"Una persona camina {a} m hacia el este y luego {b} m hacia el norte. ¿Cuál es el módulo de su desplazamiento?", c, w,
                    f"El desplazamiento une el inicio con el final: √({a}² + {b}²) = {h} m.")
    c, w = numeric_options(a + b, [h, b - a, a * b], step=1, fn=unit("m"))
    return make(MEC, f"Una persona camina {a} m hacia el este y luego {b} m hacia el norte. ¿Qué distancia recorrió?", c, w,
                f"La distancia es el largo del camino: {a} + {b} = {a + b} m (el desplazamiento sería {h} m).")


def t_relatividad():
    v1, v2 = rnd.sample([40, 50, 60, 70, 80, 90, 100, 110, 120], 2)
    if rnd.random() < 0.5:
        r = abs(v1 - v2)
        c, w = numeric_options(r, [v1 + v2, v1, v2], step=10, fn=unit("km/h"))
        return make(MEC, f"Dos autos viajan por una carretera recta en el mismo sentido, a {v1} km/h y {v2} km/h. ¿Con qué rapidez se mueve uno respecto del otro?", c, w,
                    f"Según la relatividad de Galileo, en el mismo sentido se restan: |{v1} − {v2}| = {r} km/h.")
    r = v1 + v2
    c, w = numeric_options(r, [abs(v1 - v2), v1, v2], step=10, fn=unit("km/h"))
    return make(MEC, f"Dos autos viajan por una carretera recta en sentidos opuestos, acercándose, a {v1} km/h y {v2} km/h. ¿Con qué rapidez se acerca uno al otro?", c, w,
                f"En sentidos opuestos las rapideces se suman: {v1} + {v2} = {r} km/h.")


def t_tren_pasajero():
    vt, vp = rnd.choice([10, 15, 20, 25, 30]), rnd.choice([1, 2, 3])
    if rnd.random() < 0.5:
        r = vt + vp
        txt, ex = "hacia adelante (en el sentido del tren)", f"{vt} + {vp} = {r} m/s"
    else:
        r = vt - vp
        txt, ex = "hacia atrás (en sentido contrario al tren)", f"{vt} − {vp} = {r} m/s"
    c, w = numeric_options(r, [vt, vp, vt + vp if r != vt + vp else vt - vp], step=1, fn=unit("m/s"))
    return make(MEC, f"Un tren avanza a {vt} m/s respecto del andén. Dentro de él, un pasajero camina a {vp} m/s {txt}. ¿Cuál es la rapidez del pasajero respecto del andén?", c, w,
                f"Relatividad de Galileo: {ex}.")


def t_accel():
    a, t = rnd.randint(1, 8), rnd.randint(2, 12)
    vi = rnd.randint(0, 20)
    vf = vi + a * t
    if rnd.random() < 0.5:
        c, w = numeric_options(a, [vf // t, vf - vi, (vf + vi) // t], step=1, fn=unit("m/s²"))
        return make(MEC, f"Un móvil aumenta su velocidad de {vi} m/s a {vf} m/s en {t} s de manera uniforme. ¿Cuál es su aceleración?", c, w,
                    f"a = (vf − vi)/t = ({vf} − {vi})/{t} = {a} m/s².")
    c, w = numeric_options(vf, [vi + a, a * t, vi * t], step=a, fn=unit("m/s"))
    return make(MEC, f"Un móvil parte con velocidad {vi} m/s y acelera de manera constante a {a} m/s². ¿Qué velocidad tiene después de {t} s?", c, w,
                f"vf = vi + a·t = {vi} + {a}·{t} = {vf} m/s.")


def t_mrua_distancia():
    a, t = rnd.choice([2, 4, 6, 8, 10]), rnd.randint(2, 10)
    v0 = rnd.choice([0, 0, 2, 5, 10])
    d = v0 * t + a * t * t // 2
    c, w = numeric_options(d, [v0 * t + a * t, a * t * t, (v0 + a * t) * t], step=max(2, d // 10), fn=unit("m"))
    ini = "parte del reposo" if v0 == 0 else f"tiene una velocidad inicial de {v0} m/s"
    return make(MEC, f"Un auto {ini} y acelera de manera constante a {a} m/s². ¿Qué distancia recorre en {t} s?", c, w,
                f"d = v₀·t + ½·a·t² = {v0}·{t} + ½·{a}·{t * t} = {fint(d)} m.")


def t_frenado():
    v0, a = rnd.choice([(10, 2), (20, 4), (20, 5), (30, 5), (30, 6), (12, 3), (24, 4), (16, 2)])
    t = v0 // a
    if rnd.random() < 0.5:
        c, w = numeric_options(t, [v0 * a, v0 + a, t * 2], step=1, fn=unit("s"))
        return make(MEC, f"Un auto que va a {v0} m/s frena con una desaceleración constante de {a} m/s². ¿Cuánto tiempo tarda en detenerse?", c, w,
                    f"0 = {v0} − {a}·t → t = {v0}/{a} = {t} s.")
    d = v0 * t // 2
    c, w = numeric_options(d, [v0 * t, v0 * a, d // 2], step=max(2, d // 10), fn=unit("m"))
    return make(MEC, f"Un auto que va a {v0} m/s frena de manera uniforme y se detiene en {t} s. ¿Qué distancia recorre mientras frena?", c, w,
                f"Velocidad media = ({v0} + 0)/2 = {v0 // 2} m/s; d = {v0 // 2}·{t} = {d} m.")


def t_free_fall():
    t = rnd.randint(1, 5)
    if rnd.random() < 0.5:
        v = 10 * t
        c, w = numeric_options(v, [5 * t * t, 10 * t * t, 10 + t], step=5, fn=unit("m/s"))
        return make(MEC, f"Se deja caer una piedra desde el reposo. Despreciando el roce con el aire y usando g = 10 m/s², ¿qué rapidez tiene después de {t} s?", c, w,
                    f"Es un MRUA con a = g: v = g·t = 10·{t} = {v} m/s.")
    h = 5 * t * t
    c, w = numeric_options(h, [10 * t, 10 * t * t, 5 * t], step=5, fn=unit("m"))
    return make(MEC, f"Se deja caer un objeto desde el reposo. Usando g = 10 m/s² y sin roce con el aire, ¿qué distancia cae en {t} s?", c, w,
                f"h = ½·g·t² = 5·{t * t} = {h} m.")


def t_newton2():
    m, a = rnd.randint(2, 60), rnd.randint(1, 10)
    F = m * a
    if rnd.random() < 0.5:
        c, w = numeric_options(F, [m + a, m * a * 2, F // 2 if F > 2 else F + 3], step=m, fn=unit("N"))
        return make(MEC, f"¿Qué fuerza neta se necesita para que un cuerpo de {m} kg acelere a {a} m/s²?", c, w,
                    f"Segunda ley de Newton: F = m·a = {m}·{a} = {F} N.")
    c, w = numeric_options(a, [F * m, F - m, a * 2], step=1, fn=unit("m/s²"))
    return make(MEC, f"Sobre un cuerpo de {m} kg actúa una fuerza neta de {F} N. ¿Cuál es su aceleración?", c, w,
                f"a = F/m = {F}/{m} = {a} m/s².")


def t_fuerza_neta():
    m = rnd.choice([2, 4, 5, 10, 20])
    F1 = rnd.randrange(20, 201, 10)
    F2 = rnd.randrange(10, F1, 10)
    Fn = F1 - F2
    if Fn % m:
        raise Skip()
    a = Fn // m
    c, w = numeric_options(a, [(F1 + F2) // m if (F1 + F2) % m == 0 else a + 4, Fn, F1 // m if F1 % m == 0 else a + 2], step=1, fn=unit("m/s²"))
    return make(MEC, f"Sobre una caja de {m} kg actúan dos fuerzas horizontales opuestas: {F1} N hacia la derecha y {F2} N hacia la izquierda. ¿Cuál es la aceleración de la caja?", c, w,
                f"Fuerza neta = {F1} − {F2} = {Fn} N; a = {Fn}/{m} = {a} m/s².")


def t_weight():
    m = rnd.randint(2, 120)
    if rnd.random() < 0.7:
        c, w = numeric_options(m * 10, [m, m + 10, m * 100], step=10, fn=unit("N"))
        return make(MEC, f"¿Cuál es el peso de un cuerpo de {m} kg en la Tierra? (usa g = 10 m/s²)", c, w,
                    f"P = m·g = {m}·10 = {m * 10} N.")
    m = rnd.choice([5, 10, 20, 50, 60, 80, 100])
    P = m * 16 / 10
    c, w = numeric_options(P, [m * 10, m, m * 16], step=8, fn=unit("N"))
    return make(MEC, f"Un astronauta lleva a la Luna un equipo de {m} kg. Si en la Luna g = 1,6 m/s², ¿cuánto pesa allí el equipo?", c, w,
                f"La masa sigue siendo {m} kg; P = {m}·1,6 = {fmt(P)} N.")


def t_hooke():
    k, x = rnd.choice([10, 20, 50, 100, 200, 500]), rnd.choice([0.02, 0.05, 0.1, 0.2, 0.3])
    F = k * x
    if F != int(F) and rnd.random() < 0.5:
        raise Skip()
    if rnd.random() < 0.6:
        c, w = numeric_options(F, [k * x * 2, k + x, k * x / 2], step=1, fn=unit("N"))
        return make(MEC, f"Un resorte de constante elástica {k} N/m se estira {fmt(x)} m. ¿Qué fuerza elástica ejerce el resorte?", c, w,
                    f"Ley de Hooke: F = k·x = {k}·{fmt(x)} = {fmt(F)} N.")
    c, w = numeric_options(x * 100, [x * 1000, F * k / 100, x * 50], step=1, fn=unit("cm"))
    return make(MEC, f"Un resorte de constante {k} N/m se estira al colgarle un objeto que ejerce una fuerza de {fmt(F)} N. ¿Cuánto se estira?", c, w,
                f"x = F/k = {fmt(F)}/{k} = {fmt(x)} m = {fmt(x * 100)} cm.")


def t_roce():
    m = rnd.choice([2, 4, 5, 10, 20, 50])
    mu = rnd.choice([Fraction(1, 10), Fraction(1, 5), Fraction(1, 4), Fraction(3, 10), Fraction(2, 5), Fraction(1, 2)])
    N = m * 10
    fr = mu * N
    if fr.denominator != 1:
        raise Skip()
    c, w = numeric_options(fr, [N, mu * m, N - fr], step=2, fn=unit("N"))
    return make(MEC, f"Una caja de {m} kg desliza sobre un piso horizontal. Si el coeficiente de roce cinético es {fmt(mu)}, ¿cuál es la fuerza de roce? (usa g = 10 m/s²)", c, w,
                f"Normal = peso = {N} N; f = μ·N = {fmt(mu)}·{N} = {fmt(fr)} N.")


def t_roce_velocidad_cte():
    m = rnd.choice([5, 10, 20, 40])
    mu = rnd.choice([Fraction(1, 5), Fraction(1, 4), Fraction(1, 2), Fraction(1, 10)])
    fr = mu * m * 10
    if fr.denominator != 1:
        raise Skip()
    c, w = numeric_options(fr, [m * 10, fr * 2, m], step=5, fn=unit("N"))
    return make(MEC, f"Se empuja horizontalmente una caja de {m} kg y esta se mueve con velocidad constante. El coeficiente de roce cinético es {fmt(mu)}. ¿Con qué fuerza se la empuja? (usa g = 10 m/s²)", c, w,
                f"Con velocidad constante la fuerza neta es cero: F = roce = {fmt(mu)}·{m * 10} = {fmt(fr)} N.")


def t_kepler3():
    a = rnd.choice([4, 9, 16, 25])
    T = int(a ** 1.5)
    c, w = numeric_options(T, [a, a * a, int(a ** 0.5)], step=4, fn=unit("años"))
    return make(MEC, f"Según la tercera ley de Kepler (T² = a³, con T en años y a en unidades astronómicas), ¿cuál es el período de un planeta ficticio que orbita a {a} UA del Sol?", c, w,
                f"T² = {a}³ = {a ** 3}; T = √{a ** 3} = {T} años.")


# ===================================================================== FÍSICA: Ondas
def t_luz():
    k = rnd.randint(1, 3)
    if k == 1:
        lam = rnd.choice([1, 2, 3, 5, 10, 100])
        f = Fraction(3 * 10 ** 8, lam)
        e = 8 - len(str(lam)) + 1
        m = f / 10 ** e
        if m.denominator != 1:
            raise Skip()
        s = f"{fmt(m)} × 10{sup(e)} Hz"
        w = [f"{fmt(m)} × 10{sup(e + 1)} Hz", f"{fmt(m)} × 10{sup(e - 2)} Hz", f"{lam * 3} × 10{sup(8)} Hz", f"{fmt(m)} × 10{sup(e - 1)} Hz"]
        return make(OND, f"Una onda de radio viaja en el vacío (c = 3 × 10⁸ m/s) y tiene una longitud de onda de {lam} m. ¿Cuál es su frecuencia?", s, w,
                    f"c = λ·f → f = 3 × 10⁸ / {lam} = {s}.")
    if k == 2:
        f_e = rnd.choice([6, 7, 8, 9])
        lam_m = Fraction(3 * 10 ** 8, 10 ** f_e)
        s = f"{fmt(lam_m)} m"
        w = [f"{fmt(lam_m * 10)} m", f"{fmt(lam_m / 10)} m", f"{fmt(lam_m * 100)} m", f"3 × 10{sup(f_e)} m"]
        return make(OND, f"Una onda electromagnética de frecuencia 10{sup(f_e)} Hz viaja en el vacío (c = 3 × 10⁸ m/s). ¿Cuál es su longitud de onda?", s, w,
                    f"λ = c/f = 3 × 10⁸ / 10{sup(f_e)} = {s}.")
    t = rnd.choice([2, 4, 5, 10, 20])
    d = 3 * 10 ** 5 * t
    c, w = numeric_options(d, [3 * 10 ** 5 // t, d * 10, d // 2], step=d // 4, fn=unit("km"))
    return make(OND, f"La luz viaja a 300.000 km/s. ¿Qué distancia recorre en {t} s?", c, w,
                f"d = v·t = 300.000·{t} = {fint(d)} km.")


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


COLORES = [("roja", 4, 75), ("amarilla", 5, 6), ("verde", 6, 5), ("violeta", Fraction(15, 2), 4)]


def t_periodo():
    if rnd.random() < 0.5:
        fm = rnd.choice([1, 2, 5, 10, 20, 50, 100, 200, 500])
        T = Fraction(1, fm * 10 ** 6)
        c = sci(T) + " s"
        w = [sci(fm * 10 ** 6) + " s", sci(T * 10) + " s", sci(T / 10) + " s", sci(T * 2) + " s"]
        return make(OND, f"Una antena emite ondas de radio de {fm} MHz (1 MHz = 10⁶ Hz). ¿Cuál es el período de esas ondas?", c, w,
                    f"T = 1/f = 1/({fm} × 10⁶ Hz) = {c}.")
    color, f14, lam = rnd.choice(COLORES)
    lam_m = Fraction(3 * 10 ** 8) / (Fraction(f14) * 10 ** 14)
    c = sci(lam_m) + " m"
    w = [sci(lam_m * 10) + " m", sci(lam_m / 10) + " m", sci(Fraction(f14) * 10 ** 14 * 3 * 10 ** 8) + " m", sci(lam_m * 1000) + " m"]
    return make(OND, f"La luz {color} tiene una frecuencia de {fmt(f14)} × 10¹⁴ Hz. Si en el vacío c = 3 × 10⁸ m/s, ¿cuál es su longitud de onda?", c, w,
                f"λ = c/f = 3 × 10⁸ / ({fmt(f14)} × 10¹⁴) = {c}.")


def t_onda_v():
    lam, f = rnd.choice([0.5, 1, 2, 3, 4, 5, 10]), rnd.choice([2, 4, 5, 10, 20, 50, 100])
    v = lam * f
    c, w = numeric_options(v, [lam + f, f / lam, v * 2], step=max(1, v / 10), fn=unit("m/s"))
    return make(OND, f"Una onda tiene una longitud de onda de {fmt(lam)} m y una frecuencia de {f} Hz. ¿Cuál es su rapidez de propagación?", c, w,
                f"v = λ·f = {fmt(lam)}·{f} = {fmt(v)} m/s.")


def t_espejo_plano():
    d = rnd.randint(1, 6)
    if rnd.random() < 0.5:
        c, w = numeric_options(2 * d, [d, d + 1, 4 * d], step=1, fn=unit("m"))
        return make(OND, f"Una persona está a {d} m de un espejo plano. ¿A qué distancia de la persona se ve su imagen?", c, w,
                    f"La imagen está {d} m detrás del espejo: {d} + {d} = {2 * d} m de la persona.")
    ang = rnd.choice([20, 25, 30, 35, 40, 50, 60])
    c, w = numeric_options(ang, [90 - ang, 2 * ang, 180 - ang], step=5, fn=lambda v: f"{fmt(v)}°")
    return make(OND, f"Un rayo de luz llega a un espejo plano con un ángulo de incidencia de {ang}° respecto de la normal. ¿Cuál es el ángulo de reflexión?", c, w,
                "Ley de reflexión: el ángulo de reflexión es igual al de incidencia.")


# ===================================================================== FÍSICA: Electricidad
def t_ohm():
    R, I = rnd.choice([2, 4, 5, 6, 8, 10, 12, 20, 25, 50]), rnd.choice([1, 2, 3, 4, 5])
    V = R * I
    k = rnd.randint(1, 3)
    if k == 1:
        c, w = numeric_options(I, [V * R, R // I or 7, V - R], step=1, fn=unit("A"))
        return make(ELE, f"Una resistencia de {R} Ω se conecta a una fuente de {V} V. ¿Qué corriente circula por ella?", c, w,
                    f"Ley de Ohm: I = V/R = {V}/{R} = {I} A.")
    if k == 2:
        c, w = numeric_options(V, [R + I, R // I if R % I == 0 else R + 1, V * 2], step=R, fn=unit("V"))
        return make(ELE, f"Por una resistencia de {R} Ω circula una corriente de {I} A. ¿Cuál es el voltaje entre sus extremos?", c, w,
                    f"V = I·R = {I}·{R} = {V} V.")
    c, w = numeric_options(R, [V * I, V + I, R * 2], step=2, fn=unit("Ω"))
    return make(ELE, f"Una ampolleta conectada a {V} V deja pasar una corriente de {I} A. ¿Cuál es su resistencia?", c, w,
                f"R = V/I = {V}/{I} = {R} Ω.")


PARALLEL = [(3, 6, 2), (4, 4, 2), (6, 12, 4), (10, 15, 6), (20, 30, 12), (12, 24, 8), (6, 6, 3), (10, 10, 5), (4, 12, 3), (12, 12, 6)]


def t_serie():
    rs = rnd.sample([1, 2, 3, 4, 5, 6, 8, 10], rnd.choice([2, 3]))
    Rt = sum(rs)
    I = rnd.randint(1, 4)
    V = Rt * I
    txt = ", ".join(f"{r} Ω" for r in rs[:-1]) + f" y {rs[-1]} Ω"
    if rnd.random() < 0.5:
        c, w = numeric_options(Rt, [max(rs), Rt * 2, min(rs)], step=1, fn=unit("Ω"))
        return make(ELE, f"Se conectan en serie resistencias de {txt}. ¿Cuál es la resistencia equivalente?", c, w,
                    f"En serie se suman: {' + '.join(map(str, rs))} = {Rt} Ω.")
    c, w = numeric_options(I, [V * Rt, V // max(rs) if V // max(rs) != I else I + 2, I * len(rs)], step=1, fn=unit("A"))
    return make(ELE, f"Resistencias de {txt} se conectan en serie a una batería de {V} V. ¿Qué corriente circula por el circuito?", c, w,
                f"R equivalente = {Rt} Ω; I = {V}/{Rt} = {I} A.")


def t_paralelo():
    a, b, r = rnd.choice(PARALLEL)
    if rnd.random() < 0.6:
        c, w = numeric_options(r, [a + b, abs(a - b) or a + 1, (a + b) // 2], step=1, fn=unit("Ω"))
        return make(ELE, f"Se conectan en paralelo dos resistencias de {a} Ω y {b} Ω. ¿Cuál es la resistencia equivalente?", c, w,
                    f"R = ({a}·{b})/({a} + {b}) = {r} Ω.")
    V = a * b * rnd.choice([1, 2])
    I = V // r
    c, w = numeric_options(I, [V // (a + b) if V % (a + b) == 0 else I + 3, V // a, I * 2], step=1, fn=unit("A"))
    return make(ELE, f"Dos resistencias de {a} Ω y {b} Ω se conectan en paralelo a una fuente de {V} V. ¿Qué corriente total entrega la fuente?", c, w,
                f"R equivalente = {r} Ω; I = {V}/{r} = {I} A (o bien {V}/{a} + {V}/{b} = {V // a} + {V // b}).")


def t_mixto():
    a, b, r = rnd.choice(PARALLEL)
    R1 = rnd.choice([1, 2, 3, 4, 5, 6, 10])
    Rt = R1 + r
    c, w = numeric_options(Rt, [R1 + a + b, r, R1 + (a + b) // 2], step=1, fn=unit("Ω"))
    return make(ELE, f"Una resistencia de {R1} Ω se conecta en serie con un grupo de dos resistencias en paralelo de {a} Ω y {b} Ω. ¿Cuál es la resistencia equivalente del circuito?", c, w,
                f"Paralelo: ({a}·{b})/({a} + {b}) = {r} Ω. Luego en serie: {R1} + {r} = {Rt} Ω.")


def t_elec_power():
    k = rnd.randint(1, 3)
    if k == 1:
        V, I = rnd.choice([12, 24, 110, 220]), rnd.choice([1, 2, 3, 5, 10])
        P = V * I
        c, w = numeric_options(P, [V + I, V // I if V % I == 0 else V + 1, P * 2], step=V, fn=unit("W"))
        return make(ELE, f"Un artefacto funciona con {V} V y una corriente de {I} A. ¿Cuál es su potencia eléctrica?", c, w,
                    f"P = V·I = {V}·{I} = {fint(P)} W.")
    if k == 2:
        I, R = rnd.choice([1, 2, 3, 4, 5]), rnd.choice([2, 5, 10, 20])
        P = I * I * R
        c, w = numeric_options(P, [I * R, I * R * 2, I * I], step=max(2, P // 10), fn=unit("W"))
        return make(ELE, f"Por una resistencia de {R} Ω circula una corriente de {I} A. ¿Qué potencia disipa?", c, w,
                    f"P = I²·R = {I * I}·{R} = {P} W.")
    P = rnd.choice([220, 440, 660, 1100, 2200])
    I = P // 220
    c, w = numeric_options(I, [P * 220 // 1000, P // 22, I * 2], step=1, fn=unit("A"))
    return make(ELE, f"Un hervidor de {fint(P)} W se conecta a la red de 220 V. ¿Qué corriente circula por él?", c, w,
                f"I = P/V = {fint(P)}/220 = {I} A.")


def t_kwh():
    P = rnd.choice([100, 200, 500, 1000, 1500, 2000])
    h = rnd.choice([2, 3, 4, 5, 6, 10])
    dias = rnd.choice([1, 10, 30])
    E = Fraction(P * h * dias, 1000)
    if E.denominator != 1:
        raise Skip()
    if rnd.random() < 0.5:
        c, w = numeric_options(E, [P * h * dias, E * 10, Fraction(P * h, 1000)], step=max(1, int(E) // 5), fn=unit("kWh"))
        cuando = "en un día" if dias == 1 else f"en {dias} días"
        return make(ELE, f"Un artefacto de {fint(P)} W se usa {h} horas diarias. ¿Cuánta energía consume {cuando}?", c, w,
                    f"E = P·t = {fmt(Fraction(P, 1000))} kW·{h * dias} h = {fmt(E)} kWh.")
    precio = rnd.choice([100, 150, 200])
    costo = int(E * precio)
    c, w = numeric_options(costo, [int(E) * 10, P * precio, costo * 2], step=max(50, costo // 5), fn=lambda v: f"${fint(v)}")
    cuando = "un día" if dias == 1 else f"{dias} días"
    return make(ELE, f"Un artefacto de {fint(P)} W se usa {h} horas diarias durante {cuando}. Si el kWh cuesta ${precio}, ¿cuánto cuesta esa energía?", c, w,
                f"E = {fmt(Fraction(P, 1000))} kW·{h * dias} h = {fmt(E)} kWh; costo = {fmt(E)}·{precio} = ${fint(costo)}.")


def t_eficiencia():
    Ein = rnd.choice([100, 200, 400, 500, 1000])
    pct = rnd.choice([10, 20, 25, 40, 50, 75, 80, 90])
    Eu = Ein * pct // 100
    if rnd.random() < 0.5:
        c, w = numeric_options(pct, [100 - pct, Eu, pct // 2], step=5, fn=lambda v: f"{fmt(v)}%")
        return make(ELE, f"Una ampolleta recibe {Ein} J de energía eléctrica y entrega {Eu} J como luz. ¿Cuál es su eficiencia?", c, w,
                    f"Eficiencia = energía útil/energía recibida·100 = {Eu}/{Ein}·100 = {pct}%.")
    c, w = numeric_options(Ein - Eu, [Eu, Ein, Ein + Eu], step=10, fn=unit("J"))
    return make(ELE, f"Un motor eléctrico tiene una eficiencia del {pct}% y recibe {Ein} J de energía. ¿Cuánta energía se pierde, principalmente como calor?", c, w,
                f"Energía útil = {pct}% de {Ein} = {Eu} J; se pierden {Ein} − {Eu} = {Ein - Eu} J.")


def t_carga():
    I, t = rnd.choice([1, 2, 3, 4, 5, 10]), rnd.choice([2, 5, 10, 20, 30, 60])
    Q = I * t
    c, w = numeric_options(Q, [I + t, t // I if t % I == 0 and t // I != Q else Q * 2, Q * 10], step=max(1, Q // 5), fn=unit("C"))
    return make(ELE, f"Por un cable circula una corriente constante de {I} A. ¿Cuánta carga eléctrica pasa por él en {t} s?", c, w,
                f"I = Q/t → Q = I·t = {I}·{t} = {Q} C.")


# ===================================================================== QUÍMICA: Estructura atómica
ELEMENTS = [("hidrógeno", "H", 1, 1), ("helio", "He", 2, 4), ("litio", "Li", 3, 7), ("carbono", "C", 6, 12), ("nitrógeno", "N", 7, 14),
            ("oxígeno", "O", 8, 16), ("flúor", "F", 9, 19), ("sodio", "Na", 11, 23), ("magnesio", "Mg", 12, 24), ("aluminio", "Al", 13, 27),
            ("fósforo", "P", 15, 31), ("azufre", "S", 16, 32), ("potasio", "K", 19, 39), ("calcio", "Ca", 20, 40), ("hierro", "Fe", 26, 56)]
IONS = [("Na⁺", 11, 10), ("K⁺", 19, 18), ("Mg²⁺", 12, 10), ("Ca²⁺", 20, 18), ("Al³⁺", 13, 10), ("O²⁻", 8, 10), ("S²⁻", 16, 18),
        ("F⁻", 9, 10), ("Cl⁻", 17, 18)]


def t_subatomic():
    k = rnd.randint(1, 4)
    if k == 3:
        ion, Z, e = rnd.choice(IONS)
        c, w = numeric_options(e, [Z, Z + (Z - e), Z * 2], step=1)
        return make(ATO, f"El ion {ion} proviene de un átomo con número atómico Z = {Z}. ¿Cuántos electrones tiene el ion?", c, w,
                    f"El átomo neutro tiene {Z} electrones; la carga indica que {'perdió' if e < Z else 'ganó'} {abs(Z - e)}, quedando con {e}.")
    name, sym, Z, A = rnd.choice(ELEMENTS)
    if k == 4:
        n = A - Z
        c, w = numeric_options(A, [n, Z, A + Z], step=1)
        return make(ATO, f"Un átomo tiene {Z} protones y {n} neutrones. ¿Cuál es su número másico (A)?", c, w,
                    f"A = protones + neutrones = {Z} + {n} = {A}.")
    if k == 1 and A - Z != Z:
        c, w = numeric_options(A - Z, [A, Z, A + Z], step=1)
        return make(ATO, f"Un átomo de {name} tiene número atómico Z = {Z} y número másico A = {A}. ¿Cuántos neutrones tiene en su núcleo?", c, w,
                    f"Neutrones = A − Z = {A} − {Z} = {A - Z}.")
    c, w = numeric_options(Z, [A, A - Z if A - Z != Z else A + 1, Z + 1], step=1)
    return make(ATO, f"Un átomo neutro de {name} ({sym}) tiene número atómico {Z} y número másico {A}. ¿Cuántos electrones tiene?", c, w,
                f"En un átomo neutro, electrones = protones = Z = {Z}.")


ISOTOPOS = [("carbono", 6, [12, 13, 14]), ("hidrógeno", 1, [1, 2, 3]), ("oxígeno", 8, [16, 17, 18]), ("cloro", 17, [35, 37]),
            ("uranio", 92, [235, 238]), ("nitrógeno", 7, [14, 15])]


def t_isotopos():
    name, Z, As = rnd.choice(ISOTOPOS)
    A = rnd.choice(As)
    c, w = numeric_options(A - Z, [A, Z, A + Z], step=1)
    return make(ATO, f"El {name}-{A} es un isótopo del {name} (Z = {Z}). ¿Cuántos neutrones tiene su núcleo?", c, w,
                f"El número {A} es el número másico: neutrones = {A} − {Z} = {A - Z}.")


def t_densidad():
    V = rnd.choice([2, 4, 5, 10, 20, 50])
    rho = rnd.choice([0.5, 0.8, 1, 2, 2.5, 7.8, 11.3])
    m = V * rho
    if rnd.random() < 0.5:
        c, w = numeric_options(rho, [m * V, m + V, rho * 2], step=0.5, fn=unit("g/cm³"))
        return make(ATO, f"Un objeto tiene una masa de {fmt(m)} g y un volumen de {V} cm³. ¿Cuál es su densidad?", c, w,
                    f"ρ = m/V = {fmt(m)}/{V} = {fmt(rho)} g/cm³.")
    c, w = numeric_options(m, [rho, V / rho, m * 2], step=max(1, m / 5), fn=unit("g"))
    return make(ATO, f"Un líquido tiene una densidad de {fmt(rho)} g/cm³. ¿Qué masa tienen {V} cm³ de este líquido?", c, w,
                f"m = ρ·V = {fmt(rho)}·{V} = {fmt(m)} g.")


# ===================================================================== QUÍMICA: Estequiometría y soluciones
MASSES = {"H": 1, "C": 12, "N": 14, "O": 16, "Na": 23, "Mg": 24, "S": 32, "Cl": 35.5, "K": 39, "Ca": 40}
COMPOUNDS = [("agua", "H₂O", {"H": 2, "O": 1}), ("dióxido de carbono", "CO₂", {"C": 1, "O": 2}), ("amoníaco", "NH₃", {"N": 1, "H": 3}),
             ("metano", "CH₄", {"C": 1, "H": 4}), ("cloruro de sodio", "NaCl", {"Na": 1, "Cl": 1}),
             ("ácido sulfúrico", "H₂SO₄", {"H": 2, "S": 1, "O": 4}), ("carbonato de calcio", "CaCO₃", {"Ca": 1, "C": 1, "O": 3}),
             ("glucosa", "C₆H₁₂O₆", {"C": 6, "H": 12, "O": 6}), ("hidróxido de sodio", "NaOH", {"Na": 1, "O": 1, "H": 1}),
             ("óxido de magnesio", "MgO", {"Mg": 1, "O": 1}), ("etanol", "C₂H₆O", {"C": 2, "H": 6, "O": 1}),
             ("oxígeno molecular", "O₂", {"O": 2}), ("nitrógeno molecular", "N₂", {"N": 2})]


def mm(comp):
    return sum(MASSES[e] * n for e, n in comp.items())


def masses_txt(comp):
    return ", ".join(f"{e} = {fmt(MASSES[e])}" for e in comp)


def t_molar():
    name, f, comp = rnd.choice(COMPOUNDS)
    M = mm(comp)
    k = rnd.randint(1, 3)
    if k == 1:
        c, w = numeric_options(M, [sum(MASSES[e] for e in comp), M + 16, M - 1 if M > 2 else M + 2], step=2, fn=unit("g/mol"))
        return make(EST, f"¿Cuál es la masa molar del {name} ({f})? (masas atómicas en g/mol: {masses_txt(comp)})", c, w,
                    f"Se suman las masas de todos los átomos: {' + '.join(f'{n}·{fmt(MASSES[e])}' for e, n in comp.items())} = {fmt(M)} g/mol.")
    n = rnd.choice([0.5, 2, 3, 4, 5, 10])
    m = M * n
    if k == 2:
        c, w = numeric_options(n, [m * M, M / m if m else 1, n * 2], step=0.5, fn=unit("mol"))
        return make(EST, f"¿Cuántos moles hay en {fmt(m)} g de {name} ({f})? (masa molar: {fmt(M)} g/mol)", c, w,
                    f"n = m/M = {fmt(m)}/{fmt(M)} = {fmt(n)} mol.")
    c, w = numeric_options(m, [M, M / n, m * 2], step=max(1, M / 2), fn=unit("g"))
    return make(EST, f"¿Qué masa tienen {fmt(n)} mol de {name} ({f})? (masa molar: {fmt(M)} g/mol)", c, w,
                f"m = n·M = {fmt(n)}·{fmt(M)} = {fmt(m)} g.")


def t_avogadro():
    n = rnd.choice([0.5, 2, 3, 5, 10])
    val = n * 6.02
    exp = 23
    while val >= 10:
        val /= 10
        exp += 1
    s = f"{fmt(round(val, 3))} × 10{sup(exp)}"
    w = ["6,02 × 10²³", f"{fmt(round(val, 3))} × 10{sup(exp + 1)}", f"{fmt(n)} × 10²³",
         f"{fmt(round(val * 2 if val * 2 < 10 else val / 2, 3))} × 10{sup(exp)}"]
    sust = rnd.choice(["agua", "dióxido de carbono", "metano", "amoníaco"])
    return make(EST, f"¿Cuántas moléculas hay en {fmt(n)} mol de {sust}? (número de Avogadro: 6,02 × 10²³)", s, w,
                f"N = n·N_A = {fmt(n)}·6,02 × 10²³ = {s}.")


def t_molaridad():
    k = rnd.randint(1, 3)
    if k == 1:
        n, V = rnd.choice([0.1, 0.2, 0.5, 1, 2, 3]), rnd.choice([0.25, 0.5, 1, 2])
        M = n / V
        c, w = numeric_options(M, [n * V, V / n, M * 2], step=0.1, fn=unit("mol/L"))
        return make(EST, f"Se disuelven {fmt(n)} mol de soluto en agua hasta completar {fmt(V)} L de solución. ¿Cuál es la concentración molar?", c, w,
                    f"M = n/V = {fmt(n)}/{fmt(V)} = {fmt(M)} mol/L.")
    if k == 2:
        M, V = rnd.choice([0.1, 0.2, 0.5, 1, 2]), rnd.choice([0.5, 1, 2, 3])
        n = M * V
        c, w = numeric_options(n, [M / V, M + V, n * 2], step=0.1, fn=unit("mol"))
        return make(EST, f"¿Cuántos moles de soluto hay en {fmt(V)} L de una solución de concentración {fmt(M)} mol/L?", c, w,
                    f"n = M·V = {fmt(M)}·{fmt(V)} = {fmt(n)} mol.")
    g, V = rnd.choice([(20, 0.5), (40, 1), (80, 2), (10, 0.25), (40, 0.5), (20, 1)])
    n = Fraction(g, 40)
    M = n / Fraction(V).limit_denominator()
    c, w = numeric_options(M, [g / V, n, M * 2], step=Fraction(1, 4), fn=unit("mol/L"))
    return make(EST, f"Se disuelven {g} g de NaOH (masa molar 40 g/mol) en agua hasta completar {fmt(V)} L de solución. ¿Cuál es la concentración molar?", c, w,
                f"n = {g}/40 = {fmt(n)} mol; M = {fmt(n)}/{fmt(V)} = {fmt(M)} mol/L.")


def t_molalidad():
    n, kg = rnd.choice([(0.5, 0.25), (1, 0.5), (2, 1), (1, 0.25), (0.2, 0.1), (3, 1.5), (0.5, 0.5)])
    m = n / kg
    c, w = numeric_options(m, [n * kg, kg / n, m * 2], step=0.5, fn=unit("mol/kg"))
    return make(EST, f"Se disuelven {fmt(n)} mol de glucosa en {fmt(kg * 1000)} g de agua. ¿Cuál es la concentración molal (molalidad) de la solución?", c, w,
                f"molalidad = moles de soluto / kg de solvente = {fmt(n)}/{fmt(kg)} = {fmt(m)} mol/kg.")


def t_fraccion_molar():
    a, b = rnd.choice([(1, 4), (2, 8), (1, 9), (3, 7), (2, 3), (1, 1), (5, 15)])
    X = Fraction(a, a + b)
    c, w = numeric_options(X, [Fraction(a, b), Fraction(b, a + b), Fraction(a, a + b) * 2], step=Fraction(1, 10), fn=lambda v: fmt(v))
    return make(EST, f"Una solución contiene {a} mol de etanol y {b} mol de agua. ¿Cuál es la fracción molar del etanol?", c, w,
                f"X = moles de etanol / moles totales = {a}/({a} + {b}) = {fmt(X)}.")


def t_porcentajes():
    k = rnd.randint(1, 4)
    if k == 1:
        s, total = rnd.choice([5, 10, 15, 20, 25, 40, 50]), rnd.choice([100, 200, 250, 500])
        p = Fraction(s * 100, total)
        if (p * 10).denominator != 1:
            raise Skip()
        c, w = numeric_options(p, [Fraction(s * 100, total - s), s, Fraction(total, s)], step=1, fn=lambda v: f"{fmt(v)}% m/m")
        return make(EST, f"Se disuelven {s} g de sal en agua y se obtienen {total} g de solución. ¿Cuál es el porcentaje masa/masa (% m/m)?", c, w,
                    f"% m/m = masa de soluto/masa de solución·100 = {s}/{total}·100 = {fmt(p)}%.")
    if k == 2:
        s, V = rnd.choice([(5, 100), (10, 200), (20, 250), (2, 50), (15, 300), (25, 500), (9, 100)])
        p = Fraction(s * 100, V)
        c, w = numeric_options(p, [Fraction(V, s), s, p * 2], step=1, fn=lambda v: f"{fmt(v)}% m/v")
        return make(EST, f"Se disuelven {s} g de azúcar en agua hasta completar {V} mL de solución. ¿Cuál es su concentración en % m/v?", c, w,
                    f"% m/v = g de soluto/mL de solución·100 = {s}/{V}·100 = {fmt(p)}%.")
    if k == 3:
        a, V = rnd.choice([(12, 100), (40, 200), (25, 250), (70, 100), (30, 500), (60, 300)])
        p = Fraction(a * 100, V)
        c, w = numeric_options(p, [Fraction(a * 100, V + a), a, p * 2], step=1, fn=lambda v: f"{fmt(v)}% v/v")
        return make(EST, f"Se mezclan {a} mL de alcohol con agua hasta completar {V} mL de solución. ¿Cuál es su concentración en % v/v?", c, w,
                    f"% v/v = mL de soluto/mL de solución·100 = {a}/{V}·100 = {fmt(p)}%.")
    pct, total = rnd.choice([(10, 200), (5, 400), (20, 150), (25, 80), (15, 200), (4, 500)])
    s = pct * total // 100
    c, w = numeric_options(s, [total - s, pct, s * 2], step=max(1, s // 4), fn=unit("g"))
    return make(EST, f"¿Cuántos gramos de soluto hay en {total} g de una solución al {pct}% m/m?", c, w,
                f"{pct}% de {total} g = {pct}·{total}/100 = {s} g.")


def t_ppm():
    if rnd.random() < 0.5:
        mg, kg = rnd.choice([(2, 1), (5, 2), (3, 0.5), (10, 4), (6, 3), (1, 0.25)])
        p = mg / kg
        c, w = numeric_options(p, [mg * kg, p * 1000, kg / mg], step=1, fn=unit("ppm"))
        return make(EST, f"Una muestra de {fmt(kg)} kg de agua contiene {mg} mg de un contaminante. ¿Cuál es su concentración en ppm (mg/kg)?", c, w,
                    f"ppm = mg de soluto / kg de solución = {mg}/{fmt(kg)} = {fmt(p)} ppm.")
    p, L = rnd.choice([(2, 10), (5, 4), (0.5, 20), (3, 3), (10, 5), (4, 25)])
    mg = p * L
    c, w = numeric_options(mg, [p, L, mg * 1000], step=max(1, mg / 5), fn=unit("mg"))
    return make(EST, f"El agua de un pozo tiene {fmt(p)} ppm de hierro (1 ppm = 1 mg/L en agua). ¿Cuántos mg de hierro hay en {L} L de esa agua?", c, w,
                f"mg = ppm·L = {fmt(p)}·{L} = {fmt(mg)} mg.")


def t_dilucion():
    C1, V1, f = rnd.choice([1, 2, 3, 4, 6]), rnd.choice([50, 100, 200, 250]), rnd.choice([2, 4, 5, 10])
    V2 = V1 * f
    C2 = C1 / f
    if rnd.random() < 0.6:
        c, w = numeric_options(C2, [C1 * f, C1, C2 * 2], step=0.1, fn=unit("mol/L"))
        return make(EST, f"Se toman {V1} mL de una solución {C1} mol/L y se agrega agua hasta completar {V2} mL. ¿Cuál es la nueva concentración?", c, w,
                    f"C₁·V₁ = C₂·V₂ → C₂ = {C1}·{V1}/{V2} = {fmt(C2)} mol/L.")
    c, w = numeric_options(V1, [V2, V2 - V1 if V2 - V1 != V1 else V1 * 3, V1 // 2], step=10, fn=unit("mL"))
    return make(EST, f"¿Qué volumen de una solución {C1} mol/L se necesita para preparar {V2} mL de una solución {fmt(C2)} mol/L?", c, w,
                f"V₁ = C₂·V₂/C₁ = {fmt(C2)}·{V2}/{C1} = {V1} mL.")


def t_mezcla_soluciones():
    V1, C1 = rnd.choice([100, 200, 300, 500]), rnd.choice([1, 2, 3, 4])
    V2, C2 = rnd.choice([100, 200, 300, 500]), rnd.choice([1, 2, 3, 4])
    if C1 == C2:
        raise Skip()
    Cf = Fraction(V1 * C1 + V2 * C2, V1 + V2)
    if (Cf * 10).denominator != 1:
        raise Skip()
    c, w = numeric_options(Cf, [C1 + C2, Fraction(C1 + C2, 2) if Fraction(C1 + C2, 2) != Cf else Cf + 1, max(C1, C2)], step=Fraction(1, 2), fn=unit("mol/L"))
    return make(EST, f"Se mezclan {V1} mL de una solución de NaCl {C1} mol/L con {V2} mL de otra solución de NaCl {C2} mol/L. ¿Cuál es la concentración de la mezcla?", c, w,
                f"Moles totales = {fmt(Fraction(V1, 1000))}·{C1} + {fmt(Fraction(V2, 1000))}·{C2} = {fmt(Fraction(V1 * C1 + V2 * C2, 1000))} mol; "
                f"volumen = {fmt(Fraction(V1 + V2, 1000))} L; C = {fmt(Cf)} mol/L.")


def t_composicion():
    name, f, comp, el = rnd.choice([("carbonato de calcio", "CaCO₃", {"Ca": 1, "C": 1, "O": 3}, "Ca"),
                                    ("carbonato de calcio", "CaCO₃", {"Ca": 1, "C": 1, "O": 3}, "C"),
                                    ("carbonato de calcio", "CaCO₃", {"Ca": 1, "C": 1, "O": 3}, "O"),
                                    ("metano", "CH₄", {"C": 1, "H": 4}, "C"), ("metano", "CH₄", {"C": 1, "H": 4}, "H"),
                                    ("óxido de magnesio", "MgO", {"Mg": 1, "O": 1}, "Mg"), ("óxido de magnesio", "MgO", {"Mg": 1, "O": 1}, "O"),
                                    ("hidróxido de sodio", "NaOH", {"Na": 1, "O": 1, "H": 1}, "O")])
    M = mm(comp)
    pe = MASSES[el] * comp[el] * 100 / M
    pe_v = round(pe, 1)
    c, w = numeric_options(pe_v, [round(100 - pe_v, 1), round(MASSES[el] * 100 / M, 1) if comp[el] > 1 else round(pe_v / 2, 1), comp[el] * 10],
                           step=5, fn=lambda v: f"{fmt(round(v, 1))}%")
    return make(EST, f"¿Cuál es el porcentaje en masa de {el} en el {name} ({f})? (masas atómicas en g/mol: {masses_txt(comp)}; masa molar {fmt(M)} g/mol)", c, w,
                f"% {el} = {comp[el]}·{fmt(MASSES[el])}/{fmt(M)}·100 ≈ {fmt(pe_v)}%.")


EMPIRICAS = [("C₆H₁₂O₆ (glucosa)", "CH₂O", ["C₆H₁₂O₆", "C₂H₄O₂", "CHO"]), ("C₂H₄ (eteno)", "CH₂", ["C₂H₄", "CH₄", "C₂H₂"]),
             ("H₂O₂ (agua oxigenada)", "HO", ["H₂O", "H₂O₂", "HO₂"]), ("C₆H₆ (benceno)", "CH", ["C₆H₆", "CH₂", "C₃H₃"]),
             ("C₄H₁₀ (butano)", "C₂H₅", ["C₄H₁₀", "CH₂", "CH₃"]), ("N₂O₄", "NO₂", ["N₂O₄", "NO", "N₂O"]),
             ("C₂H₆ (etano)", "CH₃", ["C₂H₆", "CH₂", "CH₄"]), ("C₃H₆ (propeno)", "CH₂", ["C₃H₆", "CH₃", "C₃H₈"])]


def t_empirica():
    if rnd.random() < 0.6:
        mol, emp, wr = rnd.choice(EMPIRICAS)
        return make(EST, f"¿Cuál es la fórmula empírica del compuesto de fórmula molecular {mol}?", emp, wr + ["C₂H₂O"],
                    f"Se dividen los subíndices por su máximo común divisor: la proporción más simple es {emp}.")
    emp, Memp, M, mol, wr = rnd.choice([("CH₂O", 30, 180, "C₆H₁₂O₆", ["C₃H₆O₃", "C₂H₄O₂", "CH₂O"]), ("CH₂", 14, 56, "C₄H₈", ["C₂H₄", "C₃H₆", "C₅H₁₀"]),
                                         ("CH", 13, 78, "C₆H₆", ["C₂H₂", "C₄H₄", "C₃H₃"]), ("CH₂", 14, 42, "C₃H₆", ["C₂H₄", "C₄H₈", "CH₂"]),
                                         ("CH₂O", 30, 60, "C₂H₄O₂", ["CH₂O", "C₃H₆O₃", "C₆H₁₂O₆"])])
    return make(EST, f"Un compuesto tiene fórmula empírica {emp} (masa {Memp} g/mol) y masa molar {M} g/mol. ¿Cuál es su fórmula molecular?", mol, wr,
                f"{M}/{Memp} = {M // Memp}; se multiplican los subíndices de {emp} por {M // Memp}: {mol}.")


REACTIONS = [("2 H₂ + O₂ → 2 H₂O", "H₂", "H₂O", 2, 2), ("N₂ + 3 H₂ → 2 NH₃", "N₂", "NH₃", 1, 2), ("N₂ + 3 H₂ → 2 NH₃", "H₂", "NH₃", 3, 2),
             ("CH₄ + 2 O₂ → CO₂ + 2 H₂O", "CH₄", "H₂O", 1, 2), ("CH₄ + 2 O₂ → CO₂ + 2 H₂O", "O₂", "CO₂", 2, 1),
             ("2 Mg + O₂ → 2 MgO", "Mg", "MgO", 2, 2), ("C₃H₈ + 5 O₂ → 3 CO₂ + 4 H₂O", "C₃H₈", "CO₂", 1, 3),
             ("2 Na + Cl₂ → 2 NaCl", "Cl₂", "NaCl", 1, 2)]


def t_stoich():
    if rnd.random() < 0.25:
        a, b = rnd.randint(5, 80), rnd.randint(5, 80)
        c, w = numeric_options(a + b, [abs(a - b), a * b // 10, max(a, b)], step=5, fn=unit("g"))
        return make(EST, f"En un recipiente cerrado reaccionan completamente {a} g de un reactivo con {b} g de otro. Según la ley de conservación de la masa, ¿qué masa total de productos se forma?", c, w,
                    f"En un sistema cerrado la masa se conserva: {a} g + {b} g = {a + b} g.")
    eq, r, p, cr, cp = rnd.choice(REACTIONS)
    n = rnd.choice([1, 2, 3, 4, 5, 6, 10])
    if (n * cp) % cr:
        raise Skip()
    v = Fraction(n * cp, cr)
    c, w = numeric_options(v, [n, n * cr * cp, Fraction(n * cr, cp)], step=1, fn=unit("mol"))
    return make(EST, f"Según la ecuación balanceada {eq}, ¿cuántos moles de {p} se forman a partir de {n} mol de {r}, si hay suficiente cantidad de los demás reactivos?", c, w,
                f"La proporción es {cr} mol de {r} : {cp} mol de {p}; entonces {n}·{cp}/{cr} = {fmt(v)} mol.")


def t_stoich_masa():
    eq, r, Mr, p, Mp, cr, cp = rnd.choice([("2 H₂ + O₂ → 2 H₂O", "H₂", 2, "H₂O", 18, 2, 2), ("2 Mg + O₂ → 2 MgO", "Mg", 24, "MgO", 40, 2, 2),
                                           ("C + O₂ → CO₂", "C", 12, "CO₂", 44, 1, 1), ("CH₄ + 2 O₂ → CO₂ + 2 H₂O", "CH₄", 16, "H₂O", 18, 1, 2)])
    n = rnd.choice([1, 2, 3, 4, 5])
    m_r = n * Mr
    m_p = Fraction(n * cp, cr) * Mp
    c, w = numeric_options(m_p, [m_r, n * Mp, m_p * 2], step=Mp // 2, fn=unit("g"))
    return make(EST, f"Según la ecuación {eq}, ¿qué masa de {p} se obtiene a partir de {m_r} g de {r}, con exceso del otro reactivo? (masas molares: {r} = {Mr} g/mol; {p} = {Mp} g/mol)", c, w,
                f"{m_r} g de {r} = {n} mol; producen {fmt(Fraction(n * cp, cr))} mol de {p}; masa = {fmt(Fraction(n * cp, cr))}·{Mp} = {fmt(m_p)} g.")


def t_limitante():
    eq, A, B, a, b, P, pc = rnd.choice([("N₂ + 3 H₂ → 2 NH₃", "N₂", "H₂", 1, 3, "NH₃", 2), ("2 H₂ + O₂ → 2 H₂O", "H₂", "O₂", 2, 1, "H₂O", 2),
                                        ("2 Mg + O₂ → 2 MgO", "Mg", "O₂", 2, 1, "MgO", 2), ("CH₄ + 2 O₂ → CO₂ + 2 H₂O", "CH₄", "O₂", 1, 2, "CO₂", 1)])
    nA, nB = rnd.randint(1, 8), rnd.randint(1, 12)
    if Fraction(nA, a) == Fraction(nB, b):
        raise Skip()
    lim, nl, cl = (A, nA, a) if Fraction(nA, a) < Fraction(nB, b) else (B, nB, b)
    exc = B if lim == A else A
    if rnd.random() < 0.5:
        return make(EST, f"Según la ecuación {eq}, se hacen reaccionar {nA} mol de {A} con {nB} mol de {B}. ¿Cuál es el reactivo limitante?",
                    lim, [exc, P, "Ninguno: ambos se consumen por completo", "No se puede saber sin las masas"],
                    f"{A}: {nA}/{a} = {fmt(Fraction(nA, a))}; {B}: {nB}/{b} = {fmt(Fraction(nB, b))}. El menor cociente indica el limitante: {lim}.")
    prod = Fraction(nl * pc, cl)
    if prod.denominator != 1:
        raise Skip()
    otro = Fraction((nB if lim == A else nA) * pc, b if lim == A else a)
    c, w = numeric_options(prod, [otro, nA + nB, prod * 2], step=1, fn=unit("mol"))
    return make(EST, f"Según la ecuación {eq}, se hacen reaccionar {nA} mol de {A} con {nB} mol de {B}. ¿Cuántos moles de {P} se forman como máximo?", c, w,
                f"El reactivo limitante es {lim}; {nl} mol de {lim}·{pc}/{cl} = {fmt(prod)} mol de {P}.")


def t_balance():
    eq, coef, wr, ex = rnd.choice([
        ("_ H₂ + O₂ → 2 H₂O", "2", ["1", "3", "4"], "Hay 4 H a la derecha (2·H₂O): se necesitan 2 H₂."),
        ("N₂ + _ H₂ → 2 NH₃", "3", ["1", "2", "6"], "Hay 6 H en 2 NH₃: se necesitan 3 H₂."),
        ("CH₄ + _ O₂ → CO₂ + 2 H₂O", "2", ["1", "3", "4"], "A la derecha hay 2 + 2 = 4 O: se necesitan 2 O₂."),
        ("_ Mg + O₂ → 2 MgO", "2", ["1", "3", "4"], "Hay 2 Mg en 2 MgO."),
        ("C₃H₈ + 5 O₂ → _ CO₂ + 4 H₂O", "3", ["1", "2", "5"], "Hay 3 C en el propano: se forman 3 CO₂."),
        ("2 Na + Cl₂ → _ NaCl", "2", ["1", "3", "4"], "Hay 2 Na y 2 Cl a la izquierda: se forman 2 NaCl."),
        ("_ Al + 3 O₂ → 2 Al₂O₃", "4", ["2", "3", "6"], "Hay 2·2 = 4 Al en 2 Al₂O₃."),
        ("C₂H₆O + _ O₂ → 2 CO₂ + 3 H₂O", "3", ["1", "2", "4"], "A la derecha hay 4 + 3 = 7 O; el etanol aporta 1, faltan 6 = 3 O₂."),
    ])
    return make(EST, f"¿Qué coeficiente debe ir en el espacio para que la ecuación quede balanceada? {eq}", coef, wr, ex)


# ===================================================================== QUÍMICA: Química orgánica
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
    if rnd.random() < 0.6:
        w = [formula(n, x) for x in (2 * n + 2, 2 * n, 2 * n - 2, 2 * n + 4) if x != h and x > 0] + [formula(n + 1, h)]
        return make(ORG, f"¿Cuál es la fórmula molecular del {name}?", formula(n, h), w, f"Fórmula general {gen}; con n = {n}: {formula(n, h)}.")
    tipos = {"ano": "Alcano (solo enlaces simples)", "eno": "Alqueno (un enlace doble)", "ino": "Alquino (un enlace triple)"}
    return make(ORG, f"¿A qué tipo de hidrocarburo corresponde la fórmula {formula(n, h)}, si es de cadena abierta?", tipos[kind],
                [v for k2, v in tipos.items() if k2 != kind] + ["Hidrocarburo aromático"],
                f"Con n = {n}: CₙH₂ₙ₊₂ = {formula(n, 2 * n + 2)}, CₙH₂ₙ = {formula(n, 2 * n)}, CₙH₂ₙ₋₂ = {formula(n, 2 * n - 2)}.")


GRUPOS = [("CH₃–CH₂–OH", "Alcohol"), ("CH₃–CH₂–CH₂–OH", "Alcohol"), ("CH₃–CHO", "Aldehído"), ("CH₃–CH₂–CHO", "Aldehído"),
          ("CH₃–CO–CH₃", "Cetona"), ("CH₃–CO–CH₂–CH₃", "Cetona"), ("CH₃–COOH", "Ácido carboxílico"), ("CH₃–CH₂–COOH", "Ácido carboxílico"),
          ("CH₃–COO–CH₃", "Éster"), ("CH₃–COO–CH₂–CH₃", "Éster"), ("CH₃–O–CH₃", "Éter"), ("CH₃–CH₂–O–CH₂–CH₃", "Éter"),
          ("CH₃–NH₂", "Amina"), ("CH₃–CH₂–NH₂", "Amina"), ("CH₃–CONH₂", "Amida"), ("CH₃–CH₂–CONH₂", "Amida"),
          ("CH₃–C≡N", "Nitrilo"), ("CH₃–CH₂–C≡N", "Nitrilo"), ("CH₃–CH₂–Cl", "Haluro (halogenuro de alquilo)"),
          ("CH₃–Br", "Haluro (halogenuro de alquilo)"), ("CH₃–S–CH₃", "Sulfuro (tioéter)"), ("CH₃–CO–O–CO–CH₃", "Anhídrido de ácido"),
          ("C₆H₅–OH", "Fenol")]
NOMBRES_GRUPO = sorted({g for _, g in GRUPOS})
SIMBOLO = {"Alcohol": "–OH", "Aldehído": "–CHO", "Cetona": "–CO– (entre dos carbonos)", "Ácido carboxílico": "–COOH",
           "Éster": "–COO–", "Éter": "–O–", "Amina": "–NH₂", "Amida": "–CONH₂", "Nitrilo": "–C≡N",
           "Haluro (halogenuro de alquilo)": "–X (F, Cl, Br, I)", "Sulfuro (tioéter)": "–S–", "Anhídrido de ácido": "–CO–O–CO–",
           "Fenol": "–OH unido a un anillo aromático"}


def t_grupo_funcional():
    f, g = rnd.choice(GRUPOS)
    if rnd.random() < 0.7:
        return make(ORG, f"¿A qué función orgánica pertenece el compuesto {f}?", g, rnd.sample([x for x in NOMBRES_GRUPO if x != g], 5),
                    f"El grupo característico {SIMBOLO[g]} identifica a la función {g.lower()}.")
    return make(ORG, f"¿Cuál es el grupo funcional característico de la función «{g}»?", SIMBOLO[g],
                rnd.sample([SIMBOLO[x] for x in NOMBRES_GRUPO if x != g], 5), f"La función {g.lower()} se reconoce por {SIMBOLO[g]}.")


def t_contar_atomos():
    f, mol, ex = rnd.choice([("CH₃–CH₂–CH₂–CH₃", (4, 10), "butano"), ("CH₃–CH₂–OH", (2, 6), "etanol"), ("CH₃–CH=CH₂", (3, 6), "propeno"),
                             ("CH≡C–CH₃", (3, 4), "propino"), ("CH₃–CH₂–CH₂–CH₂–CH₃", (5, 12), "pentano"), ("CH₂=CH₂", (2, 4), "eteno"),
                             ("CH₃–CO–CH₃", (3, 6), "propanona"), ("CH₃–CH(CH₃)–CH₃", (4, 10), "metilpropano")])
    C, H = mol
    if rnd.random() < 0.5:
        c, w = numeric_options(H, [C, H + 2, H - 2], step=1)
        return make(ORG, f"¿Cuántos átomos de hidrógeno tiene la molécula de fórmula semidesarrollada {f} ({ex})?", c, w,
                    f"Se suman los H de cada grupo: en total {H} átomos de hidrógeno.")
    c, w = numeric_options(C, [H, C + 1, C - 1], step=1)
    return make(ORG, f"¿Cuántos átomos de carbono tiene la molécula {f} ({ex})?", c, w, f"Se cuentan las C de la fórmula: {C}.")


def t_hibridacion():
    f, preg, ans, ex = rnd.choice([
        ("CH₃–CH₃", "los carbonos", "sp³", "Solo hay enlaces simples: cada carbono es sp³."),
        ("CH₂=CH₂", "los carbonos", "sp²", "Cada carbono participa en un enlace doble: es sp²."),
        ("CH≡CH", "los carbonos", "sp", "Cada carbono participa en un enlace triple: es sp."),
        ("CH₃–CH=CH₂", "el carbono 1 (CH₃)", "sp³", "El CH₃ solo tiene enlaces simples."),
        ("CH₃–CH=CH₂", "el carbono 2 (CH)", "sp²", "El carbono 2 participa del enlace doble."),
        ("CH≡C–CH₃", "el carbono 3 (CH₃)", "sp³", "El CH₃ solo tiene enlaces simples."),
        ("CH≡C–CH₃", "el carbono 1 (CH)", "sp", "El carbono 1 participa del enlace triple."),
        ("CH₃–CO–CH₃", "el carbono central (C=O)", "sp²", "El carbono del grupo carbonilo tiene un enlace doble con el oxígeno."),
    ])
    return make(ORG, f"En la molécula {f}, ¿qué hibridación tiene {preg}?", ans, [x for x in ["sp", "sp²", "sp³", "No tiene hibridación"] if x != ans], ex)


def t_enlaces():
    f, s, d, t = rnd.choice([("CH₂=CH–CH₃", 7, 1, 0), ("CH≡C–CH₃", 5, 0, 1), ("CH₃–CH₃", 7, 0, 0), ("CH₂=CH₂", 4, 1, 0),
                             ("CH≡CH", 2, 0, 1), ("CH₂=CH–CH=CH₂", 7, 2, 0)])
    pi = d + 2 * t
    sigma = s + d + t
    if rnd.random() < 0.5:
        c, w = numeric_options(pi, [d + t, sigma, pi + 2], step=1, positive=False)
        return make(ORG, f"¿Cuántos enlaces pi (π) tiene la molécula {f}?", c, w,
                    f"Cada enlace doble tiene 1 π y cada triple tiene 2 π: {d}·1 + {t}·2 = {pi}.")
    c, w = numeric_options(sigma, [s, sigma + pi, sigma - 1], step=1)
    return make(ORG, f"¿Cuántos enlaces sigma (σ) tiene la molécula {f}?", c, w,
                f"Todo enlace simple, doble o triple tiene exactamente un σ: {s} simples + {d} dobles + {t} triples = {sigma}.")


# ===================================================================== BIOLOGÍA
SPECIES = [("el ser humano", 46), ("el perro", 78), ("el gato", 38), ("el chimpancé", 48), ("la mosca de la fruta", 8),
           ("la arveja", 14), ("la cebolla", 16), ("el caballo", 64), ("el maíz", 20), ("la vaca", 60)]


def de_(sp):
    return ("del " + sp[3:]) if sp.startswith("el ") else ("de " + sp)


def t_chromosomes():
    sp, n2 = rnd.choice(SPECIES)
    de = de_(sp)
    k = rnd.randint(1, 5)
    if k == 1:
        c, w = numeric_options(n2 // 2, [n2, n2 * 2, n2 // 4 or 3], step=2)
        return make(HER, f"Las células somáticas {de} tienen {n2} cromosomas (2n = {n2}). ¿Cuántos cromosomas tiene cada uno de sus gametos?", c, w,
                    f"La meiosis reduce el número a la mitad: n = {n2 // 2}.")
    if k == 2:
        c, w = numeric_options(n2, [n2 // 2, n2 * 2, n2 + 2], step=2)
        return make(HER, f"Una célula somática {de} (2n = {n2}) se divide por mitosis. ¿Cuántos cromosomas tiene cada célula hija?", c, w,
                    f"La mitosis produce células con el mismo número de cromosomas que la original: {n2}.")
    if k == 3:
        c, w = numeric_options(n2 * 2, [n2, n2 // 2, n2 * 4], step=2)
        return make(HER, f"Una célula {de} (2n = {n2}) está en metafase de mitosis. ¿Cuántas cromátidas tiene en total?", c, w,
                    f"Cada uno de los {n2} cromosomas está duplicado (2 cromátidas): {n2}·2 = {n2 * 2}.")
    if k == 4:
        c, w = numeric_options(n2 // 2, [n2, n2 * 2, n2 // 4 or 3], step=2)
        return make(HER, f"Una célula {de} (2n = {n2}) completa la meiosis I. ¿Cuántos cromosomas tiene cada célula resultante?", c, w,
                    f"En la meiosis I se separan los homólogos: cada célula queda con n = {n2 // 2} cromosomas (cada uno con 2 cromátidas).")
    c, w = numeric_options(n2, [n2 // 2, n2 * 2, n2 + 1], step=2)
    return make(PROC, f"Un ovocito y un espermatozoide {de} tienen {n2 // 2} cromosomas cada uno. ¿Cuántos cromosomas tendrá el cigoto que se forma en la fecundación?", c, w,
                f"{n2 // 2} + {n2 // 2} = {n2} cromosomas (2n).")


def t_divisiones():
    if rnd.random() < 0.5:
        n = rnd.randint(2, 6)
        c, w = numeric_options(2 ** n, [2 * n, n, 2 ** (n + 1)], step=2)
        return make(HER, f"Una célula se divide por mitosis y cada célula hija vuelve a dividirse, hasta completar {n} divisiones sucesivas. ¿Cuántas células se obtienen?", c, w,
                    f"Cada mitosis duplica el número de células: 2^{n} = {2 ** n}.")
    k = rnd.choice([1, 2, 3, 5, 10, 25])
    c, w = numeric_options(4 * k, [2 * k, k, 8 * k], step=2)
    return make(HER, f"{'Una célula' if k == 1 else f'{k} células'} diploide{'s' if k > 1 else ''} completa{'n' if k > 1 else ''} la meiosis. ¿Cuántas células haploides se forman en total?", c, w,
                f"Cada meiosis forma 4 células haploides: {k}·4 = {4 * k}.")


def t_ovulacion():
    L = rnd.choice([26, 28, 30, 32, 34, 35])
    d = L - 14
    c, w = numeric_options(d, [L // 2 if L // 2 != d else d + 3, 14 if d != 14 else 10, L - 7], step=1, fn=lambda v: f"Día {fmt(v)}")
    return make(PROC, f"Una mujer tiene ciclos menstruales regulares de {L} días. Si la fase lútea dura siempre unos 14 días, ¿en qué día del ciclo ocurre aproximadamente la ovulación? (el día 1 es el primer día de la menstruación)", c, w,
                f"La ovulación ocurre unos 14 días antes del siguiente ciclo: {L} − 14 = día {d}.")


def t_adn_ciclo():
    q = rnd.choice([2, 4, 6, 8, 10, 12])
    fase, v, ex = rnd.choice([("G2", 2 * q, "Después de la fase S el ADN está duplicado"),
                              ("G1", q, "Antes de la fase S el ADN aún no se ha replicado"),
                              ("metafase de mitosis", 2 * q, "El ADN sigue duplicado hasta la anafase"),
                              ("cada célula hija al terminar la mitosis", q, "Cada célula hija recibe la misma cantidad que tenía la célula en G1"),
                              ("cada célula al terminar la meiosis II", q // 2, "Al final de la meiosis cada célula tiene la mitad del ADN de una célula en G1")])
    c, w = numeric_options(v, [q, 2 * q, q // 2, 4 * q], step=1, fn=unit("pg"))
    return make(HER, f"Una célula en G1 contiene {q} picogramos (pg) de ADN. ¿Cuánto ADN tendrá en {fase}?", c, w, f"{ex}: {fmt(v)} pg.")


# Plantillas por eje: (función, peso). Mayor peso = más preguntas de ese tipo.
CALC_FIS = [(t_mru, 3), (t_kmh, 2), (t_itinerario_mru, 2), (t_encuentro, 1), (t_dist_desp, 2), (t_relatividad, 2), (t_tren_pasajero, 1),
            (t_accel, 2), (t_mrua_distancia, 2), (t_frenado, 1), (t_free_fall, 2), (t_newton2, 3), (t_fuerza_neta, 2), (t_weight, 2),
            (t_hooke, 2), (t_roce, 2), (t_roce_velocidad_cte, 1), (t_kepler3, 1), (t_luz, 3), (t_periodo, 2), (t_onda_v, 2),
            (t_espejo_plano, 2), (t_ohm, 3), (t_serie, 2), (t_paralelo, 2), (t_mixto, 2), (t_elec_power, 3), (t_kwh, 3),
            (t_eficiencia, 2), (t_carga, 1)]
CALC_QUI = [(t_subatomic, 4), (t_isotopos, 2), (t_densidad, 2), (t_molar, 4), (t_avogadro, 2), (t_molaridad, 4), (t_molalidad, 2),
            (t_fraccion_molar, 2), (t_porcentajes, 4), (t_ppm, 2), (t_dilucion, 3), (t_mezcla_soluciones, 2), (t_composicion, 2),
            (t_empirica, 2), (t_stoich, 3), (t_stoich_masa, 2), (t_limitante, 3), (t_balance, 2), (t_hydrocarbon, 3),
            (t_grupo_funcional, 5), (t_contar_atomos, 2), (t_hibridacion, 2), (t_enlaces, 2)]
CALC_BIO = [(t_chromosomes, 3), (t_divisiones, 2), (t_ovulacion, 1), (t_adn_ciclo, 2)]
