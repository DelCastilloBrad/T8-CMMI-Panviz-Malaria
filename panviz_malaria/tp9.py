"""Incremento académico TP9 con roles simulados y estado local."""
import argparse
from contextlib import closing
import json
from pathlib import Path
import sqlite3
import sys

from .consolidacion import consolidar, filtrar_distrito
from .importacion import leer_csv
from .validacion import fecha_iso


REQUERIDOS = ("id_registro", "distrito", "fecha_notificacion", "grupo_etario")
COLUMNAS = (*REQUERIDOS, "estado_validacion")
CLAVES_RESUMEN = ("distrito", "grupo_etario")


def validar_tp9(filas):
    aceptados, rechazados, identificadores = [], [], set()
    for numero, original in filas:
        fila = {campo: original[campo].strip() for campo in COLUMNAS}
        identificador = fila["id_registro"]
        motivo = motivo_rechazo(fila, identificadores)
        if motivo:
            rechazados.append({
                "fila": numero, "id_registro": identificador,
                "estado_validacion": "RECHAZADO", "motivo": motivo,
            })
        else:
            identificadores.add(identificador)
            fila["estado_validacion"] = "ACEPTADO"
            aceptados.append(fila)
    return aceptados, rechazados


def motivo_rechazo(fila, identificadores):
    for campo in REQUERIDOS:
        if not fila[campo]:
            return f"CAMPO_VACIO:{campo}"
    try:
        fecha_iso(fila["fecha_notificacion"])
    except ValueError:
        return "FECHA_INVALIDA"
    if fila["id_registro"] in identificadores:
        return "DUPLICADO"
    return None


def inicializar(conexion):
    conexion.executescript("""
        CREATE TABLE IF NOT EXISTS borrador (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            contenido TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS publicacion (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            contenido TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS bitacora (
            id INTEGER PRIMARY KEY,
            fecha TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            rol TEXT NOT NULL,
            resultado TEXT NOT NULL
        );
    """)


def importar(conexion, ruta):
    filas = leer_csv(ruta, columnas=COLUMNAS)
    aceptados, rechazados = validar_tp9(filas)
    estado = {"leidos": len(filas), "aceptados": aceptados, "rechazados": rechazados}
    with conexion:
        conexion.execute(
            "INSERT INTO borrador VALUES (1, ?) "
            "ON CONFLICT(id) DO UPDATE SET contenido = excluded.contenido",
            (json.dumps(estado, ensure_ascii=False),),
        )
    return estado


def cargar_borrador(conexion):
    fila = conexion.execute("SELECT contenido FROM borrador WHERE id = 1").fetchone()
    if fila is None:
        raise ValueError("Importa un CSV para generar el borrador.")
    return json.loads(fila[0])


def resumir(estado, distrito=None):
    grupos = consolidar(estado["aceptados"], claves=CLAVES_RESUMEN)
    if distrito is not None:
        return filtrar_distrito(grupos, distrito)
    return grupos


def publicar(conexion, rol):
    """Solo el rol publicador puede confirmar el resumen en este piloto local."""
    with conexion:
        if rol != "publicador":
            conexion.execute(
                "INSERT INTO bitacora (rol, resultado) VALUES (?, ?)",
                (rol, "DENEGADA"),
            )
            return False

        # La lectura del borrador y la escritura de la publicación forman una transacción.
        conexion.execute("BEGIN IMMEDIATE")
        resumen = resumir(cargar_borrador(conexion))
        conexion.execute(
            "INSERT INTO publicacion VALUES (1, ?) "
            "ON CONFLICT(id) DO UPDATE SET contenido = excluded.contenido",
            (json.dumps(resumen, ensure_ascii=False),),
        )
        conexion.execute(
            "INSERT INTO bitacora (rol, resultado) VALUES (?, ?)",
            (rol, "PUBLICADA"),
        )
        return True


def cargar_publicado(conexion):
    fila = conexion.execute("SELECT contenido FROM publicacion WHERE id = 1").fetchone()
    return None if fila is None else json.loads(fila[0])


def mostrar_resumen(grupos):
    print("Distrito | Grupo etario | Casos")
    for grupo in grupos:
        print(f'{grupo["distrito"]} | {grupo["grupo_etario"]} | {grupo["casos"]}')
    print(f'Total de casos: {sum(grupo["casos"] for grupo in grupos)}')


def ejecutar(conexion, args):
    if args.comando == "importar":
        estado = importar(conexion, args.entrada)
        print(f'Leídos: {estado["leidos"]} | Aceptados: {len(estado["aceptados"])}'
              f' | Rechazados: {len(estado["rechazados"])}')
    elif args.comando == "resumen":
        mostrar_resumen(resumir(cargar_borrador(conexion), args.distrito))
    elif args.comando == "rechazos":
        print("Fila CSV | ID | Motivo")
        for rechazo in cargar_borrador(conexion)["rechazados"]:
            print(f'{rechazo["fila"]} | {rechazo["id_registro"]} | {rechazo["motivo"]}')
    elif args.comando == "publicar":
        if not publicar(conexion, args.rol):
            print("Publicación denegada: el rol carece de permiso.", file=sys.stderr)
            return 3
        print("Resumen publicado.")
    elif args.comando == "publicado":
        publicado = cargar_publicado(conexion)
        if publicado is None:
            print("Aún no hay un resumen publicado.")
        else:
            mostrar_resumen(publicado)
    elif args.comando == "bitacora":
        print("Fecha UTC | Rol | Resultado")
        for fecha, rol, resultado in conexion.execute(
            "SELECT fecha, rol, resultado FROM bitacora ORDER BY id"
        ):
            print(f"{fecha} | {rol} | {resultado}")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="PANVIZ–Malaria TP9 (datos sintéticos)")
    parser.add_argument("--estado", type=Path, default=Path("resultados/tp9.sqlite3"),
                        help="Base de datos local del prototipo")
    acciones = parser.add_subparsers(dest="comando", required=True)
    carga = acciones.add_parser("importar", help="Validar CSV y guardar un borrador")
    carga.add_argument("entrada", type=Path)
    resumen = acciones.add_parser("resumen", help="Consultar el borrador consolidado")
    resumen.add_argument("--distrito", help="Mostrar solamente el distrito indicado")
    acciones.add_parser("rechazos", help="Consultar filas rechazadas y sus causas")
    publicacion = acciones.add_parser("publicar", help="Publicar el resumen con permiso")
    publicacion.add_argument("--rol", choices=("revisor", "publicador"), default="revisor")
    acciones.add_parser("publicado", help="Consultar el último resumen publicado")
    acciones.add_parser("bitacora", help="Consultar los intentos de publicación")
    args = parser.parse_args(argv)
    try:
        args.estado.parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(args.estado)) as conexion:
            inicializar(conexion)
            return ejecutar(conexion, args)
    except (OSError, ValueError, sqlite3.Error) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
