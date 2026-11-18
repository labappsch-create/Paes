"""Preguntas de suficiencia de datos para M2 (originales, no usan contenido del DEMRE).

En este tipo de pregunta no se pide calcular el resultado: hay que decidir si la
información (1) y (2) alcanza para responder. Siempre tienen las mismas 5 opciones,
en el mismo orden (por eso no se mezclan).

Cada caso se construye para que su respuesta sea una opción conocida:
  A: (1) basta y (2) no.         B: (2) basta y (1) no.
  C: se necesitan las dos juntas. D: cada una basta por sí sola.
  E: ni juntas alcanzan.
"""
import random
from fractions import Fraction

from generar_m1 import MINUS, fint

OPCIONES = [
    "(1) por sí sola",
    "(2) por sí sola",
    "Ambas juntas, (1) y (2)",
    "Cada una por sí sola, (1) o (2)",
    "Se requiere información adicional",
]
LETRA = {k: i for i, k in enumerate("ABCDE")}
EXPL_OPCION = {
    "A": "Con (1) basta, pero con (2) no.",
    "B": "Con (2) basta, pero con (1) no.",
    "C": "Ninguna basta por separado, pero juntas sí.",
    "D": "Cada una, por separado, permite responder.",
    "E": "Ni siquiera juntas permiten responder: falta información.",
}

NUMEROS = "Números"
ALGEBRA = "Álgebra y funciones"
GEOMETRIA = "Geometría"
PROBA = "Probabilidad y estadística"

rnd = random.Random(20261118)


def num(n):
    """Entero con signo menos tipográfico."""
    return fint(n)


def lineal(m, n):
    """Escribe m·x + n de forma natural: 3x − 2, −x + 4, 2x."""
    mx = "x" if m == 1 else (MINUS + "x" if m == -1 else f"{num(m)}x")
    if n == 0:
        return mx
    return f"{mx} {'+' if n > 0 else MINUS} {abs(n)}"


def simple(a, b):
    """« = 1/3» si la fracción a/b se puede simplificar; si no, nada."""
    f = Fraction(a, b)
    return "" if f.denominator == b else f" = {f.numerator}/{f.denominator}"


def q(eje, contexto, objetivo, d1, d2, letra, porque):
    enun = f"{contexto}Se puede determinar {objetivo} si:\n(1) {d1}\n(2) {d2}"
    return {
        "prueba": "m2",
        "eje": eje,
        "tipo": "suficiencia",
        "enunciado": enun,
        "alternativas": list(OPCIONES),
        "correcta": LETRA[letra],
        "explicacion": f"{EXPL_OPCION[letra]} {porque}",
    }


# ------------------------------------------------------------------ familias
def f_dos_numeros(letra):
    x, y = rnd.sample(range(2, 21), 2)
    s, d = x + y, x - y
    ctx = "Sean x e y números reales. "
    obj = "el valor de x"
    if letra == "A":
        return q(ALGEBRA, ctx, obj, f"3x = {3 * x}", f"x + y = {s}", "A",
                 f"De (1), x = {x}. De (2) hay infinitas parejas con suma {s}.")
    if letra == "B":
        return q(ALGEBRA, ctx, obj, f"x + y = {s}", f"2x + 4 = {2 * x + 4}", "B",
                 f"De (2), 2x = {2 * x} y x = {x}. Con (1) solo se conoce la suma.")
    if letra == "C":
        return q(ALGEBRA, ctx, obj, f"x + y = {s}", f"x − y = {num(d)}", "C",
                 f"Sumando ambas ecuaciones: 2x = {s + d}, x = {x}.")
    if letra == "D":
        return q(ALGEBRA, ctx, obj, f"3x = {3 * x}", f"x − 5 = {num(x - 5)}", "D",
                 f"De (1), x = {x}; de (2), x = {num(x - 5)} + 5 = {x}.")
    return q(ALGEBRA, ctx, obj, f"x + y = {s}", f"2x + 2y = {2 * s}", "E",
             "La ecuación (2) es la (1) multiplicada por 2: no entrega información nueva.")


PITAGORICOS = [(6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17), (3, 4, 5), (12, 16, 20), (7, 24, 25)]


def f_rectangulo(letra):
    ctx = "Un rectángulo tiene su largo mayor que su ancho. "
    obj = "su área"
    if letra == "C":
        w = rnd.randint(2, 15)
        return q(GEOMETRIA, ctx, obj, f"su perímetro es {6 * w} cm", "su largo es el doble de su ancho", "C",
                 f"Con ancho a y largo 2a: 6a = {6 * w}, a = {w}; área = {w}·{2 * w} = {2 * w * w} cm².")
    if letra == "E":
        P = rnd.randrange(20, 81, 2)
        return q(GEOMETRIA, ctx, obj, f"su perímetro es {P} cm", "su largo mide más de 5 cm", "E",
                 f"Hay muchos rectángulos de perímetro {P} cm con largo mayor que 5 cm y distinta área.")
    a, b, c = rnd.choice(PITAGORICOS)
    k = rnd.choice([1, 1, 2])
    w, l, dg = a * k, b * k, c * k
    if letra in "AB":
        suf = f"su largo mide {l} cm y su diagonal mide {dg} cm"
        insuf = f"su perímetro es {2 * (w + l)} cm"
        d1, d2 = (suf, insuf) if letra == "A" else (insuf, suf)
        return q(GEOMETRIA, ctx, obj, d1, d2, letra,
                 f"Por Pitágoras, ancho = √({dg}² − {l}²) = {w} cm y área = {w * l} cm². "
                 f"Con el perímetro solo se conoce la suma de los lados.")
    return q(GEOMETRIA, ctx, obj, f"su largo mide {l} cm y su diagonal mide {dg} cm",
             f"su ancho mide {w} cm y su diagonal mide {dg} cm", "D",
             f"En ambos casos el otro lado sale por Pitágoras: lados {w} y {l} cm, área {w * l} cm².")


VECES = [(2, "el doble"), (3, "el triple"), (4, "el cuádruple")]


def f_bolitas(letra):
    ctx = "Una caja contiene solo bolitas rojas y azules. "
    obj = "la probabilidad de sacar al azar una bolita roja"
    k, txt = rnd.choice(VECES)
    r = rnd.randint(2, 12)
    b = k * r
    rel = f"hay {txt} de bolitas azules que de bolitas rojas"
    if letra in "AB":
        d1, d2 = (rel, f"hay {r} bolitas rojas") if letra == "A" else (f"hay {r} bolitas rojas", rel)
        return q(PROBA, ctx, obj, d1, d2, letra,
                 f"Si hay {txt} de azules, de cada {k + 1} bolitas 1 es roja: P = 1/{k + 1}. "
                 f"Saber solo cuántas rojas hay no basta.")
    if letra == "C":
        return q(PROBA, ctx, obj, f"hay {r + b} bolitas en total", f"hay {b} bolitas azules", "C",
                 f"Juntas: rojas = {r + b} − {b} = {r}; P = {r}/{r + b}{simple(r, r + b)}.")
    if letra == "D":
        return q(PROBA, ctx, obj, rel, f"la probabilidad de sacar una bolita azul es {k}/{k + 1}", "D",
                 f"Con (1), P = 1/{k + 1}. Con (2), P = 1 − {k}/{k + 1} = 1/{k + 1}.")
    return q(PROBA, ctx, obj, f"hay {r} bolitas rojas", "hay más bolitas azules que rojas", "E",
             "No se sabe cuántas azules hay exactamente, así que no se conoce el total.")


def f_funcion(letra):
    m = rnd.choice([-3, -2, -1, 2, 3, 4, 5])
    n = rnd.choice([-6, -4, -2, 1, 3, 5, 7])
    t = rnd.choice([3, 4, 5, 10])
    ctx = "La función f es lineal afín, de la forma f(x) = mx + n. "
    obj = f"el valor de f({t})"
    dos = f"f(1) = {num(m + n)} y f(2) = {num(2 * m + n)}"
    if letra in "AB":
        d1, d2 = (dos, f"f(0) = {num(n)}") if letra == "A" else (f"f(0) = {num(n)}", dos)
        return q(ALGEBRA, ctx, obj, d1, d2, letra,
                 f"Con dos puntos se obtiene m = {num(m)} y n = {num(n)}: f({t}) = {num(m * t + n)}. "
                 "Con f(0) solo se conoce n.")
    if letra == "C":
        return q(ALGEBRA, ctx, obj, f"f(0) = {num(n)}", f"la pendiente de su gráfica es {num(m)}", "C",
                 f"Juntas: f(x) = {lineal(m, n)}, f({t}) = {num(m * t + n)}.")
    if letra == "D":
        return q(ALGEBRA, ctx, obj, dos, f"su gráfica pasa por los puntos (0, {num(n)}) y (3, {num(3 * m + n)})", "D",
                 f"Cada dato entrega dos puntos de la recta: f(x) = {lineal(m, n)}, f({t}) = {num(m * t + n)}.")
    return q(ALGEBRA, ctx, obj, f"f(0) = {num(n)}", f"su gráfica corta al eje Y en el punto (0, {num(n)})", "E",
             "Ambos datos dicen lo mismo (n); falta la pendiente m.")


PUNTOS = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 6, 10), (0, 7, 7), (9, 12, 15)]


def f_circulo(letra):
    r = rnd.randint(2, 12)
    ctx = "Una circunferencia está dibujada en el plano cartesiano. "
    obj = "el área del círculo que encierra"
    diam = f"su diámetro mide {2 * r} cm"
    if letra in "AB":
        d1, d2 = (diam, "su centro está en el origen") if letra == "A" else ("su centro está en el origen", diam)
        return q(GEOMETRIA, ctx, obj, d1, d2, letra,
                 f"Con el diámetro, r = {r} cm y área = π·{r}² = {r * r}π cm². La posición del centro no da el tamaño.")
    if letra == "C":
        a, b, c = rnd.choice(PUNTOS)
        return q(GEOMETRIA, ctx, obj, f"el punto ({a}, {b}) pertenece a la circunferencia", "su centro está en el origen", "C",
                 f"Juntas: r = distancia del origen a ({a}, {b}) = √({a}² + {b}²) = {c}; área = {c * c}π.")
    if letra == "D":
        return q(GEOMETRIA, ctx, obj, diam, f"su perímetro mide {2 * r}π cm", "D",
                 f"Con cualquiera de los dos, r = {r} cm y área = {r * r}π cm².")
    return q(GEOMETRIA, ctx, obj, "su centro está en el origen", "la circunferencia corta al eje X", "E",
             "Toda circunferencia con centro en el origen corta al eje X; el radio sigue sin conocerse.")


NOMBRES = [("Ana", "Bruno"), ("Camila", "Diego"), ("Elena", "Felipe"), ("Isidora", "Tomás"), ("Josefa", "Martín")]


def f_edades(letra):
    p1, p2 = rnd.choice(NOMBRES)
    a = rnd.randint(15, 40)
    b = a - rnd.randint(2, 9)
    s = a + b
    ctx = f"{p1} es mayor que {p2}. "
    obj = f"la edad actual de {p1}"
    fut = f"dentro de 5 años {p1} tendrá {a + 5} años"
    if letra in "AB":
        d1, d2 = (fut, f"la suma de sus edades es {s} años") if letra == "A" else (f"la suma de sus edades es {s} años", fut)
        return q(ALGEBRA, ctx, obj, d1, d2, letra,
                 f"Del dato de los 5 años: {a + 5} − 5 = {a}. Con solo la suma no se pueden separar las edades.")
    if letra == "C":
        return q(ALGEBRA, ctx, obj, f"la suma de sus edades es {s} años", f"{p1} tiene {a - b} años más que {p2}", "C",
                 f"Juntas: 2·(edad de {p1}) = {s} + {a - b} = {2 * a}, edad = {a}.")
    if letra == "D":
        return q(ALGEBRA, ctx, obj, fut, f"hace 3 años {p1} tenía {a - 3} años", "D",
                 f"Con (1): {a + 5} − 5 = {a}. Con (2): {a - 3} + 3 = {a}.")
    return q(ALGEBRA, ctx, obj, f"la suma de sus edades es {s} años", f"el doble de la suma de sus edades es {2 * s} años", "E",
             "El dato (2) es el (1) multiplicado por 2: falta la diferencia de edades.")


def f_interes(letra):
    C = rnd.choice([100000, 200000, 500000, 1000000])
    r = rnd.choice([2, 3, 4, 5, 10])
    ctx = "Se deposita dinero en un banco a interés compuesto anual, sin retiros. "
    obj = "el monto que habrá en la cuenta después de 2 años"
    if letra == "C":
        M = C * (100 + r) ** 2 // 10000
        return q(NUMEROS, ctx, obj, f"el capital inicial es ${fint(C)}", f"la tasa de interés es {r}% anual", "C",
                 f"Juntas: M = {fint(C)}·(1 + {r}/100)² = ${fint(M)}.")
    if letra == "E":
        return q(NUMEROS, ctx, obj, f"el capital inicial es ${fint(C)}", "la tasa de interés anual es mayor que 1%", "E",
                 "Sin la tasa exacta no se puede calcular el monto.")
    if letra in "AB":
        M1 = C * (100 + r) // 100
        M2 = C * (100 + r) ** 2 // 10000
        suf = f"al cabo de 1 año el monto era ${fint(M1)} y la tasa es {r}% anual"
        insuf = "el depósito se hizo en enero"
        d1, d2 = (suf, insuf) if letra == "A" else (insuf, suf)
        return q(NUMEROS, ctx, obj, d1, d2, letra,
                 f"Con el monto del primer año y la tasa: {fint(M1)}·(1 + {r}/100) = ${fint(M2)}. El mes del depósito no influye.")
    M1 = C * (100 + r) // 100
    M2 = C * (100 + r) ** 2 // 10000
    return q(NUMEROS, ctx, obj, f"el capital inicial es ${fint(C)} y la tasa es {r}% anual",
             f"al cabo de 1 año el monto era ${fint(M1)} y la tasa es {r}% anual", "D",
             f"Cada dato permite calcularlo: el monto a los 2 años es ${fint(M2)}.")


def f_promedio(letra):
    n = rnd.choice([20, 25, 30, 32, 35, 40])
    prom10 = rnd.randint(45, 62)  # promedio × 10, para notas de 1,0 a 7,0
    S = n * prom10 / 10
    if S != int(S):
        S = round(S, 1)
    s_txt = fint(S) if S == int(S) else f"{S:.1f}".replace(".", ",")
    p_txt = f"{prom10 / 10:.1f}".replace(".", ",")
    mediana = f"{(prom10 + rnd.choice([-3, 2, 4])) / 10:.1f}".replace(".", ",")
    if letra == "C":
        ctx = "Un curso rindió una prueba. "
        return q(PROBA, ctx, "el promedio de las notas del curso", f"la suma de todas las notas es {s_txt}",
                 f"el curso tiene {n} estudiantes", "C", f"Juntas: promedio = {s_txt}/{n} = {p_txt}.")
    ctx = f"Los {n} estudiantes de un curso rindieron una prueba. "
    obj = "el promedio de las notas del curso"
    if letra in "AB":
        suf, insuf = f"la suma de todas las notas es {s_txt}", f"la mediana de las notas es {mediana}"
        d1, d2 = (suf, insuf) if letra == "A" else (insuf, suf)
        return q(PROBA, ctx, obj, d1, d2, letra,
                 f"Promedio = suma/{n} = {p_txt}. La mediana no determina el promedio.")
    if letra == "D":
        return q(PROBA, ctx, obj, f"la suma de todas las notas es {s_txt}",
                 f"si a cada nota se le suma 0,5, el nuevo promedio es {f'{prom10 / 10 + 0.5:.1f}'.replace('.', ',')}", "D",
                 f"Con (1): {s_txt}/{n} = {p_txt}. Con (2): {f'{prom10 / 10 + 0.5:.1f}'.replace('.', ',')} − 0,5 = {p_txt}.")
    return q(PROBA, ctx, obj, f"la mediana de las notas es {mediana}", "la nota más alta es 7,0", "E",
             "Ni la mediana ni la nota máxima determinan la suma de las notas.")


FAMILIAS = [f_dos_numeros, f_rectangulo, f_bolitas, f_funcion, f_circulo, f_edades, f_interes, f_promedio]


def build(n):
    """Devuelve n preguntas distintas, repartidas en partes iguales entre A, B, C, D y E."""
    out, seen = [], set()
    i = guard = 0
    while len(out) < n:
        letra = "ABCDE"[len(out) % 5]
        fam = FAMILIAS[i % len(FAMILIAS)]
        i += 1
        guard += 1
        if guard > 10000:
            raise RuntimeError("No se completaron las preguntas de suficiencia de datos")
        item = fam(letra)
        if item["enunciado"] in seen:
            continue
        seen.add(item["enunciado"])
        out.append(item)
    return out
