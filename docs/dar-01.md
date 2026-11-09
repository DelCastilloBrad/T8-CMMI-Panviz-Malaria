# DAR-01 — Selección del mecanismo de procesamiento

**Estado:** propuesta técnica de E3; pendiente de revisión y ratificación por E1. Los puntajes son juicios del equipo propuestos, no mediciones experimentales.

| Criterio | Peso | Biblioteca csv | pandas |
|---|---:|---:|---:|
| Simplicidad de despliegue | 0.30 | 5 | 3 |
| Trazabilidad por fila | 0.25 | 5 | 4 |
| Facilidad de mantenimiento | 0.20 | 4 | 4 |
| Rendimiento en grandes volúmenes | 0.15 | 3 | 5 |
| Dependencias mínimas | 0.10 | 5 | 2 |
| **Total ponderado** | **1.00** | **4.45** | **3.65** |

**Decisión propuesta:** `csv` de Python, separando importación, validación, consolidación y exportación. Revisar si el alcance crece a grandes archivos.
