"""Consolidación determinista por semana ISO y territorio (R03)."""
from collections import Counter

CLAVES = ("semana_iso", "establecimiento", "distrito", "grupo_etario")

def consolidar(aceptados):
    conteo = Counter(tuple(fila[clave] for clave in CLAVES) for fila in aceptados)
    return [dict(zip(CLAVES, clave), casos=conteo[clave]) for clave in sorted(conteo)]
