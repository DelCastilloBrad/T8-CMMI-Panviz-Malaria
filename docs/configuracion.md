# Sección 12 — Gestión de configuración (E3/E5)

## Ítems de configuración
CI-01 datos/malaria_20.csv; CI-02 panviz_malaria/*; CI-03 tests/*; CI-04 docs/*; CI-05 README.md.

## Política de ramas y cambios
- `main`: implementación inicial R01–R04 y CR01 integrada técnicamente.
- CR01 se incorporó directamente a `main` por decisión operativa del piloto corto. No se creó rama separada.
- Commits descriptivos, trazabilidad y revisión independiente E4 antes de declarar una línea base aprobada.
- Evitar editar el oráculo de aceptación para acomodarlo a la salida.
- La aprobación E1 aún no está registrada: se debe documentar la desviación respecto de la secuencia prevista (aprobar antes de implementar).

## Líneas base
| Línea | Contenido | Estado |
|---|---|---|
| B0 | requisitos, contrato y oráculo del informe T8 | Aprobación E1 pendiente de registrar |
| B1 | diseño, código, datos, pruebas revisadas, CR01 | Candidata, pendiente de revisión E4 y aprobación |
| B2 | validación, PPQA, mediciones y liberación | No alcanzada |
| v0.1 | etiqueta de liberación | **No crear hasta cierre de B2** |

No se atribuyen aprobaciones ni revisiones sin actas o registros verificables.
