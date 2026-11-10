# Traspaso al integrante 4 — QA

## Versión
Implementación R01–R04 + CR01 en `main`. **No** es versión final ni B1 aprobada; decisión E1 pendiente de registrar.

## Procedimiento de verificación
1. Clonar el repositorio en carpeta limpia.
2. Ejecutar `python3 -m unittest discover -s tests -v` (11 pruebas de desarrollo, incluyendo T07).
3. Ejecutar `python3 -m panviz_malaria --entrada datos/malaria_20.csv --salida resultados`.
4. Comparar `resultados/resumen.json` con Anexo B: 20, 15, 5, 14, 15, 0.
5. Revisar `resultados/rechazos.csv`: M-003 duplicado, M-017 y M-019 vacíos, M-018 y M-020 fechas imposibles.
6. Revisar `resultados/consolidado.csv` y cotejar cada grupo con el oráculo del informe.
7. Ejecutar `python3 -m panviz_malaria --entrada datos/malaria_20.csv --salida resultados --distrito IQUITOS`.
8. Verificar `resultados/consolidado_filtrado.csv`: 7 grupos, suma 8; general 14 grupos, suma 15, diferencia 0.
9. Repetir T01–T06 como regresión y comprobar que el filtro no altera los archivos generales.
10. Probar archivo inexistente, encabezados faltantes, columnas sobrantes, fecha no canónica y distrito vacío.
11. Registrar hallazgos con ID, pasos, esperado, observado y severidad; revisar código por persona distinta del autor y registrar dictamen.
12. Verificar la aprobación de CR01 por E1 y registrar cualquier desviación del flujo AR-05.

## Registro de hallazgos
| ID | Fecha | Revisor | Caso | Esperado | Observado | Estado |
|---|---|---|---|---|---|---|
| — | — | — | — | — | — | Pendiente |

## Evidencias a adjuntar
Capturas/logs de consola, CSV generados, reporte de pruebas, revisión de código y registro de aprobación. No declarar conformidad hasta que E4 ejecute y documente.
