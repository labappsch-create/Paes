"""Herramientas compartidas para generar las preguntas de Ciencias."""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generar_m1 as base  # noqa: E402
from generar_m1 import MINUS, Skip, fint, fmt, frac_str, numeric_options, sup  # noqa: E402,F401

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(ROOT, "assets", "images", "ciencias")
OUT_JSON = os.path.join(ROOT, "assets", "questions", "ciencias.json")

rnd = random.Random(20261119)
base.rnd = rnd  # `make` mezcla las alternativas con este generador.

BIO = "Biología"
FIS = "Física"
QUI = "Química"


def make(eje, enunciado, correct, wrongs, explicacion, imagen=None):
    q = base.make(eje, enunciado, correct, wrongs, explicacion, imagen)
    q["prueba"] = "ciencias"
    return q


def unit(u):
    """Formatea un número seguido de una unidad: unit('m/s')(12) -> '12 m/s'."""
    return lambda v: f"{fmt(v)} {u}"


def pick_others(items, exclude, k=3):
    pool = [x for x in dict.fromkeys(items) if x != exclude]
    return rnd.sample(pool, min(k + 2, len(pool)))
