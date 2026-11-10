"""Punto de entrada: python -m panviz_malaria."""
import argparse
import json
import sys
from .importacion import ErrorContrato, leer_csv
from .validacion import validar
from .consolidacion import consolidar, filtrar_distrito
from .exportacion import guardar

def main(argv=None):
    parser = argparse.ArgumentParser(description="Piloto Panviz–Malaria (datos sintéticos)")
    parser.add_argument("--entrada", default="datos/malaria_20.csv")
    parser.add_argument("--salida", default="resultados")
    parser.add_argument("--distrito", default=None, help="CR01: exportar también consolidado filtrado por distrito")
    args = parser.parse_args(argv)
    try:
        filas = leer_csv(args.entrada)
        aceptados, rechazados = validar(filas)
        grupos = consolidar(aceptados)
        filtrado = filtrar_distrito(grupos, args.distrito) if args.distrito is not None else None
        resumen = guardar(args.salida, aceptados, rechazados, grupos, len(filas),
                         distrito=args.distrito.strip() if args.distrito is not None else None,
                         filtrado=filtrado)
    except (ErrorContrato, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(resumen, ensure_ascii=False, indent=2))
    return 0 if resumen["diferencia"] == 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())
