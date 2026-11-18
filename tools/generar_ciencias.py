#!/usr/bin/env python3
"""Genera las 500 preguntas originales de Ciencias (400 de texto + 100 con gráfico).

- Preguntas de conceptos: escritas a partir de listas de datos en ciencias_textos.py.
- Preguntas de cálculo (Física, Química y genética): la respuesta la calcula el programa.
- Preguntas con gráfico: el gráfico se dibuja con los mismos datos de la pregunta.
No usa contenido del DEMRE.

Uso (desde la carpeta del proyecto):
    PYTHONPATH=<carpeta con matplotlib> python3 tools/generar_ciencias.py
Escribe: assets/questions/ciencias.json y assets/images/ciencias/*.png
"""
import json
import os

from ciencias_comun import IMG_DIR, OUT_JSON, ROOT, Skip, make, rnd
import ciencias_graficos as G
import ciencias_textos as T

N_TEXT = 400
N_GRAPH = 100


def build():
    if os.path.isdir(IMG_DIR):
        for f in os.listdir(IMG_DIR):
            if f.endswith(".png"):
                os.remove(os.path.join(IMG_DIR, f))
    seen = set()
    out = []

    def add(q):
        key = q["enunciado"] + "|" + q["alternativas"][q["correcta"]]
        if key in seen:
            return False
        seen.add(key)
        out.append(q)
        return True

    # 1) Todas las preguntas de conceptos, una vez cada una.
    for eje, enun, correct, wrongs, expl in T.FACTS:
        add(make(eje, enun, correct, rnd.sample(wrongs, min(len(wrongs), 5)), expl))
    n_facts = len(out)

    # 2) Preguntas de cálculo, repartidas entre las plantillas, hasta completar 400.
    i = guard = 0
    while len(out) < N_TEXT:
        t = T.CALC_TEMPLATES[i % len(T.CALC_TEMPLATES)]
        i += 1
        guard += 1
        if guard > 200000:
            raise RuntimeError("No se lograron completar las preguntas de texto.")
        for _ in range(60):
            try:
                if add(t()):
                    break
            except (Skip, ZeroDivisionError):
                continue

    # 3) Preguntas con gráfico.
    for fn, n in G.GRAPH_PLAN:
        made = tries = 0
        while made < n:
            tries += 1
            if tries > 1000:
                raise RuntimeError(f"No se pudo completar {fn.__name__}")
            before = G._img[0]
            try:
                q = fn()
            except (Skip, ZeroDivisionError):
                if G._img[0] > before:
                    p = os.path.join(IMG_DIR, f"ciencias_img_{G._img[0]:03d}.png")
                    if os.path.exists(p):
                        os.remove(p)
                    G._img[0] -= 1
                continue
            out.append(q)
            made += 1

    rnd.shuffle(out)
    ordered = []
    for n, q in enumerate(out, 1):
        item = {"id": f"ciencias_{n:03d}", "prueba": "ciencias", "eje": q["eje"], "enunciado": q["enunciado"],
                "alternativas": q["alternativas"], "correcta": q["correcta"], "explicacion": q["explicacion"]}
        if "imagen" in q:
            item["imagen"] = q["imagen"]
        ordered.append(item)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(ordered, f, ensure_ascii=False, indent=1)
    return ordered, n_facts


def validate(qs):
    assert len(qs) == N_TEXT + N_GRAPH, len(qs)
    for q in qs:
        assert len(q["alternativas"]) == 4 and len(set(q["alternativas"])) == 4, q
        assert 0 <= q["correcta"] < 4
        if "imagen" in q:
            assert os.path.exists(os.path.join(ROOT, q["imagen"])), q["imagen"]
    n_img = sum(1 for q in qs if "imagen" in q)
    assert n_img == N_GRAPH and len(os.listdir(IMG_DIR)) == N_GRAPH, n_img


if __name__ == "__main__":
    qs, n_facts = build()
    validate(qs)
    from collections import Counter
    print(f"OK: {len(qs)} preguntas ({n_facts} de conceptos), 100 con gráfico. Por eje: {dict(Counter(q['eje'] for q in qs))}")
