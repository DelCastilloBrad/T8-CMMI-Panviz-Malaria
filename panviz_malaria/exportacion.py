"""Salidas CSV/JSON y conciliación de totales (R04/CR01)."""
import csv
import json
from pathlib import Path
from .consolidacion import CLAVES

def guardar(salida, aceptados, rechazados, consolidado, total, distrito=None, filtrado=None):
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
    if distrito is not None:
        if filtrado is None:
            raise ValueError("Falta el consolidado filtrado")
        _csv(salida / "consolidado_filtrado.csv", (*CLAVES, "casos"), filtrado)
        resumen["filtro_distrito"] = distrito
        resumen["grupos_filtrados"] = len(filtrado)
        resumen["suma_filtrada"] = sum(f["casos"] for f in filtrado)
    (salida / "resumen.json").write_text(
        json.dumps(resumen, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return resumen

def _csv(ruta, columnas, filas):
    with ruta.open("w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        escritor.writeheader()
        escritor.writerows(filas)
