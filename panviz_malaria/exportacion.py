"""Salidas CSV/JSON y conciliación de totales (R04)."""
import csv
import json
from pathlib import Path
from .consolidacion import CLAVES

def guardar(salida, aceptados, rechazados, consolidado, total):
    salida = Path(salida)
    salida.mkdir(parents=True, exist_ok=True)
    _csv(salida / "consolidado.csv", (*CLAVES, "casos"), consolidado)
    _csv(salida / "rechazos.csv", ("fila", "id_registro", "motivo"), rechazados)
    resumen = {
        "leidos": total,
        "aceptados": len(aceptados),
        "rechazados": len(rechazados),
        "grupos": len(consolidado),
        "suma_consolidado": sum(f["casos"] for f in consolidado),
    }
    resumen["diferencia"] = resumen["suma_consolidado"] - resumen["aceptados"]
    (salida / "resumen.json").write_text(
        json.dumps(resumen, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return resumen

def _csv(ruta, columnas, filas):
    with ruta.open("w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        escritor.writeheader()
        escritor.writerows(filas)
