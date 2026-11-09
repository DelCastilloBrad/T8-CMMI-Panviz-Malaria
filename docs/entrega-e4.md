# Traspaso al integrante 4 — QA

## Versión
Primera entrega R01–R04; **no** versión final ni B1 aprobada.

## Procedimiento de verificación
1. Clonar el repositorio en carpeta limpia.
2. Ejecutar `python3 -m unittest discover -s tests -v`.
3. Ejecutar `python3 -m panviz_malaria --entrada datos/malaria_20.csv --salida resultados`.
4. Comparar `resultados/resumen.json` con el Anexo B: 20, 15, 5, 14, 15, 0.
5. Revisar `resultados/rechazos.csv`: M-003 duplicado, M-017 y M-019 vacíos, M-018 y M-020 fechas imposibles.
6. Revisar `resultados/consolidado.csv` y cotejar cada grupo con el oráculo del informe.
7. Probar archivo inexistente, encabezados faltantes, columnas sobrantes y fecha no canónica.
8. Registrar hallazgos con ID, pasos de reproducción, esperado, observado y severidad.
9. Revisar el código por persona distinta del autor y registrar dictamen.
10. Tras aprobación de CR01, ejecutar T07 y repetir T01–T06.

## Registro de hallazgos
| ID | Fecha | Revisor | Caso | Esperado | Observado | Estado |
|---|---|---|---|---|---|---|
| — | — | — | — | — | — | Pendiente |

## Evidencias a adjuntar
Capturas/logs de consola, CSV generados, reporte de pruebas, revisión de código y registro de aprobación. No declarar conformidad hasta que E4 ejecute y documente.
