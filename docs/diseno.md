# Sección 10 — Diseño de solución (E3)

## 10.1 Arquitectura
Entrada CSV → contrato de columnas → validación por fila → (aceptados / rechazos) → agrupación por semana ISO, establecimiento, distrito y grupo etario → filtro opcional CR01 sobre consolidado → exportación CSV + resumen JSON → reconciliación general.

## 10.2 Componentes
| Componente | Responsabilidad | Interfaz |
|---|---|---|
| importacion.py | CSV UTF-8, encabezados, filas | leer_csv(ruta) |
| validacion.py | Vacíos, duplicados, fecha, edad | validar(filas) |
| consolidacion.py | Contar por clave compuesta y filtrar por distrito | consolidar(aceptados), filtrar_distrito(consolidado, distrito) |
| exportacion.py | CSV de salida, CSV filtrado opcional y resumen | guardar(salida,...) |
| __main__.py | CLI y códigos de salida | python -m panviz_malaria |

## 10.3 Contratos
- Entrada: 14 columnas documentadas en `importacion.COLUMNAS`; siete obligatorias no vacías.
- Rechazos: `fila,id_registro,motivo`. Número de fila inicia en 2 por el encabezado.
- Consolidado: `semana_iso,establecimiento,distrito,grupo_etario,casos`.
- Resumen: `leidos,aceptados,rechazados,grupos,suma_consolidado,diferencia`; con filtro agrega `filtro_distrito,grupos_filtrados,suma_filtrada`.
- CR01: `--distrito IQUITOS` genera `consolidado_filtrado.csv` adicional; general permanece intacto.
- `semana_iso` se deriva de fecha sintética de notificación, no semana de síntomas de MINSA.
- Códigos de salida: 0 conciliado; 1 descuadre; 2 error de contrato/archivo/argumento.

## 10.4 Alternativas
Se consideraron (A) biblioteca estándar `csv` + módulos funcionales y (B) `pandas` + DataFrame. La primera reduce dependencias y facilita inspección fila a fila. La segunda puede simplificar análisis de volúmenes mayores. La matriz está en `dar-01.md`.

## 10.5 Límites
No existe interfaz web, diagnóstico, mapa geográfico, ingestión directa de datos MINSA ni datos personales reales. CR01 está implementado técnicamente, pendiente de revisión independiente y registro de aprobación E1.
