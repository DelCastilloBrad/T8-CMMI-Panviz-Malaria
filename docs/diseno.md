# Sección 10 — Diseño de solución (E3)

## 10.1 Arquitectura
Entrada CSV → contrato de columnas → validación por fila → (aceptados / rechazos) → agrupación por semana ISO, establecimiento, distrito y grupo etario → exportación CSV + resumen JSON → reconciliación.

## 10.2 Componentes
| Componente | Responsabilidad | Interfaz |
|---|---|---|
| importacion.py | CSV UTF-8, encabezados, filas | leer_csv(ruta) |
| validacion.py | Vacíos, duplicados, fecha, edad | validar(filas) |
| consolidacion.py | Contar por clave compuesta | consolidar(aceptados) |
| exportacion.py | CSV de salida y resumen | guardar(salida,...) |
| __main__.py | CLI y códigos de salida | python -m panviz_malaria |

## 10.3 Contratos
- Entrada: 14 columnas documentadas en `importacion.COLUMNAS`; siete obligatorias no vacías.
- Rechazos: `fila,id_registro,motivo`. Número de fila inicia en 2 por el encabezado.
- Consolidado: `semana_iso,establecimiento,distrito,grupo_etario,casos`.
- Resumen: `leidos,aceptados,rechazados,grupos,suma_consolidado,diferencia`.
- `semana_iso` se deriva de la fecha sintética de notificación, no de la semana de síntomas de MINSA.
- Códigos de salida: 0 conciliado; 1 descuadre; 2 error de contrato/archivo.

## 10.4 Alternativas
Se consideraron (A) biblioteca estándar `csv` + módulos funcionales y (B) `pandas` + DataFrame. La primera reduce dependencias y facilita inspección fila a fila. La segunda puede simplificar análisis de volúmenes mayores. La matriz y su carácter propositivo están en `dar-01.md`.

## 10.5 Límites
No existe interfaz web, diagnóstico, mapa geográfico, ingestión directa de datos MINSA ni datos personales reales. La versión inicial **no implementa CR01** hasta registrar la aprobación. Diseño pendiente de revisión por persona distinta del autor.
