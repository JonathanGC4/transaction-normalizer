"""
config.py

Este modulo centraliza las rutas y constantes generales del proyecto.

Decision del desarrollador: mantener las rutas en un solo lugar para que,
si en el futuro cambia la organizacion de carpetas, solo haya que
modificar este archivo y no cada modulo por separado.
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
CONFIGS_DIR = os.path.join(BASE_DIR, "configs")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

SAMPLE_GOOD_FILE = os.path.join(DATA_DIR, "transactions_good.json")
SAMPLE_BAD_FILE = os.path.join(DATA_DIR, "transactions_bad.json")
SAMPLE_MIXED_FILE = os.path.join(DATA_DIR, "transactions_mixed.json")