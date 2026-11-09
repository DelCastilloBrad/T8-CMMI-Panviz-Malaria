"""Contrato de lectura de archivos CSV del piloto (R01)."""
import csv
from pathlib import Path

COLUMNAS = (
    "id_registro", "fecha_notificacion", "establecimiento", "evento",
    "ano", "semana_sintomas", "departamento", "provincia", "distrito",
    "ubigeo", "diagnostico", "edad", "tipo_edad", "sexo",
)

class ErrorContrato(ValueError):
    """El archivo no cumple el contrato de entrada."""

def leer_csv(ruta):
    """Devuelve [(número de línea física, fila)] sin modificar la fuente."""
    ruta = Path(ruta)
    try:
        with ruta.open("r", encoding="utf-8-sig", newline="") as archivo:
            lector = csv.DictReader(archivo)
            if lector.fieldnames is None:
                raise ErrorContrato("CSV sin encabezado")
            faltantes = sorted(set(COLUMNAS) - set(lector.fieldnames))
            if faltantes:
                raise ErrorContrato("Columnas faltantes: " + ", ".join(faltantes))
            if len(lector.fieldnames) != len(set(lector.fieldnames)):
                raise ErrorContrato("Encabezados duplicados")
            filas = []
            for numero, fila in enumerate(lector, start=2):
                if None in fila or any(valor is None for valor in fila.values()):
                    raise ErrorContrato(f"Fila {numero}: cantidad de columnas incorrecta")
                filas.append((numero, fila))
            return filas
    except (OSError, UnicodeError, csv.Error) as exc:
        raise ErrorContrato(f"No se pudo leer el CSV: {exc}") from exc
