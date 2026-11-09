# Panviz–Malaria | Piloto CMMI-DEV v1.3

Componente **independiente** de procesamiento de notificaciones sintéticas de malaria. Se inspira en el proyecto académico ISPySA-Pneumonia (análisis de IRAS), pero **no reutiliza su modelo predictivo** ni afirma disponer de datos reales. El diseño implementa el contrato del T8: importación, validación, consolidación y exportación.

## Requisitos previos
Python 3.10 o superior. No se requieren dependencias de terceros para ejecutar el programa.

## Ejecutar
```bash
git clone https://github.com/DelCastilloBrad/T8-CMMI-Panviz-Malaria.git
cd T8-CMMI-Panviz-Malaria
python3 -m panviz_malaria --entrada datos/malaria_20.csv --salida resultados
cat resultados/resumen.json
```

**Resultados de referencia del Anexo B:** 20 filas, 15 aceptadas, 5 rechazadas, 14 grupos, suma 15 y diferencia 0. Las semanas se calculan a partir de `fecha_notificacion`, no de `semana_sintomas`.

## Para el integrante 4
```bash
python3 -m unittest discover -s tests -v
```
Se solicita revisión independiente de código, ejecución de T01–T06, observaciones y evidencias. **CR01 (filtro por distrito) está documentado como cambio pendiente de aprobación y se incorporará en una segunda etapa.** No se afirma que las revisiones, pruebas independientes, aprobaciones B0/B1/B2 o la liberación v0.1 hayan ocurrido.

## Estructura
- `panviz_malaria/`: importación, validación, agregación, exportación y CLI.
- `datos/`: dataset sintético de control.
- `tests/`: pruebas de desarrollo para reproducibilidad (no sustituyen QA independiente).
- `docs/`: diseño, decisión técnica, trazabilidad, configuración y CR01.
- `resultados/`: salidas generadas localmente (ignoradas por Git).

## Procedencia y límites
Los campos territoriales y demográficos se inspiran en el conjunto público [Vigilancia epidemiológica de malaria del MINSA](https://www.datosabiertos.gob.pe/dataset/vigilancia-epidemiol%C3%B3gica-de-malaria). `id_registro`, `fecha_notificacion`, `establecimiento`, `semana_iso` y `grupo_etario` corresponden al contrato didáctico. **Los 20 casos son inventados**. El sistema no realiza diagnóstico ni vigilancia en producción.

Proyecto de Calidad de Software — Universidad Nacional de San Agustín, 2026.
