"""Consolidación determinista por semana ISO y territorio (R03/CR01)."""
from collections import Counter

CLAVES = ("semana_iso", "establecimiento", "distrito", "grupo_etario")

def consolidar(aceptados):
    conteo = Counter(tuple(fila[clave] for clave in CLAVES) for fila in aceptados)
    return [dict(zip(CLAVES, clave), casos=conteo[clave]) for clave in sorted(conteo)]

def filtrar_distrito(consolidado, distrito):
    """CR01: filtrar grupos consolidados sin modificar el resultado general."""
    criterio = distrito.strip().casefold()
    if not criterio:
        raise ValueError("El distrito no puede estar vacío")
    return [grupo for grupo in consolidado
            if grupo["distrito"].strip().casefold() == criterio]
