#!/usr/bin/env python3
"""Genera las 500 preguntas originales de Ciencias (400 de texto + 100 con gráfico),
siguiendo el temario oficial de la prueba de Ciencias (ejes y áreas temáticas).

- Conceptos: listas revisadas en ciencias2_conceptos_bio.py y ciencias2_conceptos_fq.py.
- Habilidades científicas: experimentos ficticios en ciencias2_habilidades.py.
- Cálculos: la respuesta la calcula el programa (ciencias2_calculos.py).
- Gráficos: se dibujan con los mismos datos de la pregunta (ciencias2_graficos.py).
Cada pregunta lleva "eje" (Biología, Física o Química) y "area" (área temática oficial).
No usa contenido del DEMRE.

Uso (desde la carpeta del proyecto):
    PYTHONPATH=<carpeta con matplotlib> python3 tools/generar_ciencias.py
Escribe: assets/questions/ciencias.json y assets/images/ciencias/*.png
"""
import json
import os
from collections import Counter

from ciencias_comun import AREAS, BIO, FIS, IMG_DIR, OUT_JSON, QUI, ROOT, Skip, make, rnd
import ciencias2_calculos as C
import ciencias2_conceptos_bio as CB
import ciencias2_conceptos_fq as CFQ
import ciencias2_graficos as G
import ciencias2_habilidades as H

N_GRAPH = 100
# Preguntas de texto por eje (suman 400). Biología tiene más conceptos y menos cálculos.
TEXT_QUOTA = {BIO: 142, FIS: 130, QUI: 128}
CALC = {BIO: C.CALC_BIO, FIS: C.CALC_FIS, QUI: C.CALC_QUI}


def build():
    if os.path.isdir(IMG_DIR):
        for f in os.listdir(IMG_DIR):
            if f.endswith(".png"):
                os.remove(os.path.join(IMG_DIR, f))
    seen = set()
    text = []

    def add(q, bucket):
        key = q["enunciado"] + "|" + q["alternativas"][q["correcta"]]
        if key in seen:
            return False
        seen.add(key)
        bucket.append(q)
        return True

    # 1) Conceptos: todos, una vez cada uno.
    for area, enun, correct, wrongs, expl in CB.FACTS + CFQ.FACTS:
        if not add(make(area, enun, correct, rnd.sample(wrongs, len(wrongs)), expl), text):
            raise RuntimeError(f"Concepto repetido: {enun}")
    n_facts = len(text)

    # 2) Habilidades científicas.
    for q in H.build():
        add(q, text)
    n_hab = len(text) - n_facts

    # 3) Cálculos, hasta completar la cuota de texto de cada eje.
    for eje, quota in TEXT_QUOTA.items():
        have = sum(1 for q in text if q["eje"] == eje)
        if have > quota:
            raise RuntimeError(f"{eje}: hay {have} preguntas de texto y la cuota es {quota}")
        plan = [fn for fn, w in CALC[eje] for _ in range(w)]
        i = guard = 0
        while have < quota:
            fn = plan[i % len(plan)]
            i += 1
            guard += 1
            if guard > 100000:
                raise RuntimeError(f"No se completaron los cálculos de {eje}")
            for _ in range(60):
                try:
                    if add(fn(), text):
                        have += 1
                        break
                except (Skip, ZeroDivisionError):
                    continue

    # 4) Preguntas con gráfico.
    graphs = []
    for fn, n in G.GRAPH_PLAN:
        made = tries = 0
        while made < n:
            tries += 1
            if tries > 2000:
                raise RuntimeError(f"No se pudo completar {fn.__name__}")
            before = G._img[0]
            try:
                q = fn()
            except (Skip, ZeroDivisionError):
                if G._img[0] > before:
                    os.remove(os.path.join(IMG_DIR, f"ciencias_img_{G._img[0]:03d}.png"))
                    G._img[0] -= 1
                continue
            graphs.append(q)
            made += 1

    out = text + graphs
    rnd.shuffle(out)
    ordered = []
    for n, q in enumerate(out, 1):
        item = {"id": f"ciencias_{n:03d}", "prueba": "ciencias", "eje": q["eje"], "area": q["area"], "enunciado": q["enunciado"],
                "alternativas": q["alternativas"], "correcta": q["correcta"], "explicacion": q["explicacion"]}
        if "imagen" in q:
            item["imagen"] = q["imagen"]
        ordered.append(item)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(ordered, f, ensure_ascii=False, indent=1)
    return ordered, n_facts, n_hab


def validate(qs):
    assert len(qs) == sum(TEXT_QUOTA.values()) + N_GRAPH, len(qs)
    nombres = {a[1] for a in AREAS}
    for q in qs:
        assert len(q["alternativas"]) == 4 and len(set(q["alternativas"])) == 4, q
        assert 0 <= q["correcta"] < 4
        assert q["area"] in nombres, q["area"]
        if "imagen" in q:
            assert os.path.exists(os.path.join(ROOT, q["imagen"])), q["imagen"]
    n_img = sum(1 for q in qs if "imagen" in q)
    assert n_img == N_GRAPH and len(os.listdir(IMG_DIR)) == N_GRAPH, n_img


if __name__ == "__main__":
    qs, n_facts, n_hab = build()
    validate(qs)
    print(f"OK: {len(qs)} preguntas ({n_facts} de conceptos, {n_hab} de habilidades), {N_GRAPH} con gráfico.")
    print("Por eje:", dict(Counter(q["eje"] for q in qs)))
    for (eje, area), n in sorted(Counter((q["eje"], q["area"]) for q in qs).items()):
        print(f"  {eje:9} | {area}: {n}")
