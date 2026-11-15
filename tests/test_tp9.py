"""Comprobaciones automatizadas del incremento TP9."""
from contextlib import closing, redirect_stdout
import io
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
from time import perf_counter
import unittest

from panviz_malaria.importacion import ErrorContrato
from panviz_malaria.tp9 import (
    cargar_borrador, cargar_publicado, importar, inicializar, mostrar_resumen,
    publicar, resumir,
)


RAIZ = Path(__file__).resolve().parents[1]
DATOS = RAIZ / "datos" / "malaria_tp9_30.csv"


class IncrementoTP9Test(unittest.TestCase):
    def setUp(self):
        temporal = tempfile.TemporaryDirectory()
        self.addCleanup(temporal.cleanup)
        self.archivo_estado = Path(temporal.name) / "estado.sqlite3"
        self.conexion = sqlite3.connect(self.archivo_estado)
        self.addCleanup(self.conexion.close)
        inicializar(self.conexion)

    def cli(self, *args):
        return subprocess.run(
            [sys.executable, "-X", "utf8", "-m", "panviz_malaria.tp9", "--estado",
             str(self.archivo_estado), *args],
            cwd=RAIZ, capture_output=True, text=True, encoding="utf-8", timeout=10,
        )

    def test_t01_detecta_los_seis_invalidos_y_conserva_originales(self):
        estado = importar(self.conexion, DATOS)
        self.assertEqual(estado["leidos"], 30)
        self.assertEqual(len(estado["aceptados"]), 24)
        self.assertEqual(
            [(r["fila"], r["id_registro"], r["motivo"]) for r in estado["rechazados"]],
            [(26, "TP9-025", "CAMPO_VACIO:distrito"),
             (27, "TP9-026", "CAMPO_VACIO:grupo_etario"),
             (28, "TP9-027", "FECHA_INVALIDA"),
             (29, "TP9-028", "FECHA_INVALIDA"),
             (30, "TP9-001", "DUPLICADO"),
             (31, "TP9-013", "DUPLICADO")],
        )
        originales = {r["id_registro"]: r for r in estado["aceptados"]}
        self.assertEqual(originales["TP9-001"]["distrito"], "MIRAFLORES")
        self.assertEqual(originales["TP9-013"]["distrito"], "CHIVAY")

    def test_t02_resumen_coincide_con_el_calculo_manual(self):
        estado = importar(self.conexion, DATOS)
        grupos = resumir(estado)
        self.assertEqual(
            [(g["distrito"], g["grupo_etario"], g["casos"]) for g in grupos],
            [("CHIVAY", "ADULTO_MAYOR", 6), ("CHIVAY", "INFANTIL", 6),
             ("MIRAFLORES", "ADULTO_MAYOR", 6), ("MIRAFLORES", "INFANTIL", 6)],
        )
        self.assertEqual(sum(g["casos"] for g in grupos), 24)
        filtrado = resumir(estado, "miraflores")
        self.assertEqual(len(filtrado), 2)
        self.assertEqual(sum(g["casos"] for g in filtrado), 12)

    def test_t03_importacion_dentro_del_umbral(self):
        tiempos = []
        for _ in range(3):
            inicio = perf_counter()
            estado = importar(self.conexion, DATOS)
            tiempos.append(perf_counter() - inicio)
            self.assertEqual(estado["leidos"], 30)
        self.assertLessEqual(max(tiempos), 2, tiempos)

    def test_t04_resumen_dentro_del_umbral(self):
        importar(self.conexion, DATOS)
        tiempos = []
        for _ in range(3):
            with redirect_stdout(io.StringIO()) as salida:
                inicio = perf_counter()
                mostrar_resumen(resumir(cargar_borrador(self.conexion)))
                tiempos.append(perf_counter() - inicio)
            self.assertIn("Total de casos: 24", salida.getvalue())
        self.assertLessEqual(max(tiempos), 2, tiempos)

    def test_t05_reimportacion_preserva_el_conjunto_sin_duplicar(self):
        primero = importar(self.conexion, DATOS)
        segundo = importar(self.conexion, DATOS)
        self.assertEqual(primero, segundo)
        self.assertEqual(len(segundo["aceptados"]), 24)
        self.assertEqual(cargar_borrador(self.conexion), primero)

    def test_t06_recupera_el_conjunto_en_procesos_distintos(self):
        proceso = self.cli("importar", str(DATOS))
        self.assertEqual(proceso.returncode, 0, proceso.stderr)
        anterior = cargar_borrador(self.conexion)
        proceso = self.cli("resumen")
        self.assertEqual(proceso.returncode, 0, proceso.stderr)
        self.assertIn("Total de casos: 24", proceso.stdout)
        with closing(sqlite3.connect(self.archivo_estado)) as reinicio:
            self.assertEqual(cargar_borrador(reinicio), anterior)

    def test_t07_denegacion_preserva_publicacion_y_deja_bitacora(self):
        importar(self.conexion, DATOS)
        self.assertTrue(publicar(self.conexion, "publicador"))
        anterior = cargar_publicado(self.conexion)
        candidato = self.archivo_estado.with_name("candidato.csv")
        filas = DATOS.read_text(encoding="utf-8").splitlines()
        candidato.write_text("\n".join(filas[:2]) + "\n", encoding="utf-8")
        importar(self.conexion, candidato)
        self.assertNotEqual(resumir(cargar_borrador(self.conexion)), anterior)

        proceso = self.cli("publicar")
        self.assertEqual(proceso.returncode, 3)
        self.assertIn("Publicación denegada", proceso.stderr)
        self.assertEqual(cargar_publicado(self.conexion), anterior)
        self.assertIn("revisor | DENEGADA", self.cli("bitacora").stdout)

    def test_t08_publica_con_permiso_y_registra_la_operacion(self):
        borrador = importar(self.conexion, DATOS)
        proceso = self.cli("publicar", "--rol", "publicador")
        self.assertEqual(proceso.returncode, 0, proceso.stderr)
        self.assertEqual(cargar_publicado(self.conexion), resumir(borrador))
        self.assertIn("publicador | PUBLICADA", self.cli("bitacora").stdout)

    def test_csv_malformado_no_sustituye_el_borrador(self):
        anterior = importar(self.conexion, DATOS)
        invalido = self.archivo_estado.with_name("invalido.csv")
        invalido.write_text("id_registro,distrito\nID,MIRAFLORES\n", encoding="utf-8")
        with self.assertRaises(ErrorContrato):
            importar(self.conexion, invalido)
        self.assertEqual(cargar_borrador(self.conexion), anterior)
