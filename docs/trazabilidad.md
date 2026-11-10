# Matriz de trazabilidad — E3

| ID | Diseño | Código | Prueba de desarrollo | Evidencia E4 | Estado |
|---|---|---|---|---|---|
| R01 | Contrato CSV | importacion.py | test_t01_importacion, test_contrato_columnas | Pendiente | Implementado, sin revisión |
| R02 | Reglas de aceptación | validacion.py | test_t02_vacios, test_t03_fechas, test_t04_duplicado | Pendiente | Implementado, sin revisión |
| R03 | Clave compuesta | consolidacion.py | test_t05_consolidado | Pendiente | Implementado, sin revisión |
| R04 | CSV + reconciliación | exportacion.py | test_t06_exportacion | Pendiente | Implementado, sin revisión |
| R05 | Matriz y versionado | docs/configuracion.md, este archivo | Revisión RV-05 | Pendiente | Parcial |
| CR01 | docs/cr01.md | __main__.py, consolidacion.py, exportacion.py | test_t07_filtro_distrito, test_t07_cli, test_t07_distrito_vacio + regresión T01–T06 | Pendiente | Implementación técnica, aprobación E1 pendiente |

Los resultados de desarrollo no sustituyen la revisión independiente de E4. B1/B2 y v0.1 no están aprobadas.
