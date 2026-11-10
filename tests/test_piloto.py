"""Pruebas de desarrollo; E4 debe repetirlas y registrar su revisión independiente."""
import csv
import tempfile
import unittest
from pathlib import Path
from panviz_malaria.importacion import leer_csv, ErrorContrato
from panviz_malaria.validacion import validar, grupo_etario
from panviz_malaria.consolidacion import consolidar, filtrar_distrito
from panviz_malaria.exportacion import guardar
from panviz_malaria.__main__ import main

DATOS = Path(__file__).resolve().parents[1] / "datos" / "malaria_20.csv"

class PilotoTest(unittest.TestCase):
    def setUp(self):
        self.filas = leer_csv(DATOS)
        self.aceptados, self.rechazados = validar(self.filas)
        self.grupos = consolidar(self.aceptados)

    def test_t01_importacion(self):
        self.assertEqual(len(self.filas), 20)

    def test_t02_vacios(self):
        self.assertIn("CAMPO_VACIO:distrito", [r["motivo"] for r in self.rechazados])
        self.assertIn("CAMPO_VACIO:establecimiento", [r["motivo"] for r in self.rechazados])

    def test_t03_fechas(self):
        self.assertEqual(sum(r["motivo"] == "FECHA_INVALIDA" for r in self.rechazados), 2)

    def test_t04_duplicado(self):
        self.assertEqual(sum(r["motivo"] == "DUPLICADO" for r in self.rechazados), 1)

    def test_t05_consolidado(self):
        self.assertEqual((len(self.aceptados), len(self.grupos)), (15, 14))
        self.assertEqual(sum(r["casos"] for r in self.grupos), 15)
        self.assertEqual({r["semana_iso"] for r in self.grupos},
                         {"2025-W10", "2025-W11", "2025-W12"})

    def test_t06_exportacion(self):
        with tempfile.TemporaryDirectory() as tmp:
            resultado = guardar(tmp, self.aceptados, self.rechazados,
                                self.grupos, len(self.filas))
            self.assertEqual(resultado["diferencia"], 0)
            self.assertTrue((Path(tmp) / "consolidado.csv").is_file())
            self.assertTrue((Path(tmp) / "rechazos.csv").is_file())

    def test_t07_filtro_distrito(self):
        filtrado = filtrar_distrito(self.grupos, " iquitos ")
        self.assertEqual(len(filtrado), 7)
        self.assertEqual(sum(r["casos"] for r in filtrado), 8)
        self.assertEqual(len(self.grupos), 14)
        self.assertEqual(sum(r["casos"] for r in self.grupos), 15)
        with tempfile.TemporaryDirectory() as tmp:
            resultado = guardar(tmp, self.aceptados, self.rechazados,
                                self.grupos, len(self.filas),
                                distrito="IQUITOS", filtrado=filtrado)
            self.assertEqual(resultado["grupos_filtrados"], 7)
            self.assertEqual(resultado["suma_filtrada"], 8)
            self.assertEqual(resultado["diferencia"], 0)
            with (Path(tmp) / "consolidado_filtrado.csv").open(encoding="utf-8", newline="") as archivo:
                filas = list(csv.DictReader(archivo))
            self.assertEqual(len(filas), 7)
            self.assertTrue(all(r["distrito"] == "IQUITOS" for r in filas))

    def test_t07_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(main(["--entrada", str(DATOS), "--salida", tmp,
                                   "--distrito", "IQUITOS"]), 0)
            self.assertTrue((Path(tmp) / "consolidado_filtrado.csv").is_file())

    def test_t07_distrito_vacio(self):
        with self.assertRaisesRegex(ValueError, "no puede estar vacío"):
            filtrar_distrito(self.grupos, "   ")

    def test_contrato_columnas(self):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "mal.csv"
            ruta.write_text("id_registro,distrito\nM-001,IQUITOS\n", encoding="utf-8")
            with self.assertRaisesRegex(ErrorContrato, "Columnas faltantes"):
                leer_csv(ruta)

    def test_grupo_etario_meses(self):
        self.assertEqual(grupo_etario("8", "M"), "G1")
        self.assertEqual(grupo_etario("12", "A"), "G2")

if __name__ == "__main__":
    unittest.main()
