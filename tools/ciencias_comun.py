"""Herramientas compartidas para generar las preguntas de Ciencias.

Cada pregunta lleva su eje (Biología, Física o Química) y su área temática,
con los mismos nombres del temario oficial de la prueba de Ciencias.
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generar_m1 as base  # noqa: E402
from fractions import Fraction  # noqa: E402

from generar_m1 import MINUS, Skip, fint, fmt, frac_str, sup  # noqa: E402,F401

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(ROOT, "assets", "images", "ciencias")
OUT_JSON = os.path.join(ROOT, "assets", "questions", "ciencias.json")

rnd = random.Random(20261117)
base.rnd = rnd  # `make` mezcla las alternativas con este generador.

BIO = "Biología"
FIS = "Física"
QUI = "Química"

# Áreas temáticas del temario oficial: (eje, nombre del área).
CEL = (BIO, "Organización, estructura y actividad celular")
PROC = (BIO, "Procesos y funciones biológicas")
HER = (BIO, "Herencia y evolución")
AMB = (BIO, "Organismo y ambiente")
OND = (FIS, "Ondas")
MEC = (FIS, "Mecánica")
TIE = (FIS, "Energía – Tierra")
ELE = (FIS, "Electricidad")
ATO = (QUI, "Estructura atómica")
ORG = (QUI, "Química orgánica")
EST = (QUI, "Reacciones químicas y estequiometría")

AREAS = [CEL, PROC, HER, AMB, OND, MEC, TIE, ELE, ATO, ORG, EST]


def make(area, enunciado, correct, wrongs, explicacion, imagen=None):
    eje, nombre = area
    q = base.make(eje, enunciado, correct, wrongs, explicacion, imagen)
    q["prueba"] = "ciencias"
    q["area"] = nombre
    return q


def unit(u):
    """Formatea un número seguido de una unidad: unit('m/s')(12) -> '12 m/s'."""
    return lambda v: f"{fmt(v)} {u}"


def pick_others(items, exclude, k=3):
    pool = [x for x in dict.fromkeys(items) if x != exclude]
    return rnd.sample(pool, min(k + 2, len(pool)))


def exacto(v):
    """True si el número se puede escribir exacto con 2 decimales como máximo (sin redondear)."""
    try:
        return (Fraction(v).limit_denominator(10 ** 6) * 100).denominator == 1
    except (TypeError, ValueError):
        return False


def numeric_options(correct, cands, step=1, positive=True, fn=fmt):
    """Como generar_m1.numeric_options, pero descarta valores que habría que redondear.
    Si la respuesta correcta no es exacta, se descarta la pregunta (Skip)."""
    if not exacto(correct):
        raise Skip()
    return base.numeric_options(correct, [c for c in cands if exacto(c)], step=step, positive=positive, fn=fn)
