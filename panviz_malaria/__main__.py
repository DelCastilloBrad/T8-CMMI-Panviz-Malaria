"""Punto de entrada: python -m panviz_malaria."""
import argparse
import json
import sys
from .importacion import ErrorContrato, leer_csv
from .validacion import validar
from .consolidacion import consolidar
from .exportacion import guardar

def main(argv=None):
    parser = argparse.ArgumentParser(description="Piloto Panviz–Malaria (datos sintéticos)")
    parser.add_argument("--entrada", default="datos/malaria_20.csv")
    parser.add_argument("--salida", default="resultados")
    args = parser.parse_args(argv)
    try:
        filas = leer_csv(args.entrada)
        aceptados, rechazados = validar(filas)
        grupos = consolidar(aceptados)
        resumen = guardar(args.salida, aceptados, rechazados, grupos, len(filas))
    except (ErrorContrato, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(resumen, ensure_ascii=False, indent=2))
    return 0 if resumen["diferencia"] == 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())
