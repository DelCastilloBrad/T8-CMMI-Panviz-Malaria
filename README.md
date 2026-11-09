# Panviz–Malaria — piloto CMMI-DEV v1.3

Componente académico independiente de importación, validación, consolidación y exportación de notificaciones **sintéticas** de malaria. Se diseñó tomando como referencia conceptual el producto inicial ISPySA-Pneumonia, pero sin trasladar su modelo predictivo de IRAS. No procesa casos reales ni realiza diagnóstico.

## Requisitos
Python 3.10+; ejecución y pruebas sin paquetes externos.

## Ejecución en Windows (PowerShell o CMD)

Con **Python 3.10+** y **Git** instalados, ejecutar desde la terminal:

```powershell
git clone https://github.com/DelCastilloBrad/T8-CMMI-Panviz-Malaria.git
cd T8-CMMI-Panviz-Malaria
python -m unittest discover -s tests -v
python -m panviz_malaria --entrada datos/malaria_20.csv --salida resultados
```

Para revisar los resultados en **PowerShell**:

```powershell
Get-Content resultados/resumen.json
Get-Content resultados/rechazos.csv
```

En **CMD**, usar:

```cmd
type resultados\resumen.json
type resultados\rechazos.csv
```

Se esperan **8 pruebas correctas (OK)** y el resumen: **20 leídos, 15 aceptados, 5 rechazados, 14 grupos, suma 15 y diferencia 0**. Si Windows no reconoce `python`, sustituirlo por `py`.

## Ejecución en Pop!_OS / Linux
```bash
git clone https://github.com/DelCastilloBrad/T8-CMMI-Panviz-Malaria.git
cd T8-CMMI-Panviz-Malaria
python3 -m unittest discover -s tests -v
python3 -m panviz_malaria --entrada datos/malaria_20.csv --salida resultados
cat resultados/resumen.json
```

El informe T8 fija el oráculo de referencia: **20 leídos, 15 aceptados, 5 rechazados, 14 grupos, suma 15 y diferencia 0**. La semana ISO se deriva de `fecha_notificacion`, que es sintética, no de `semana_sintomas` del conjunto público.

### Archivos
- `panviz_malaria/`: importación, validación, consolidación, exportación y CLI.
- `datos/malaria_20.csv`: 20 casos sintéticos del piloto.
- `tests/`: pruebas automatizadas de desarrollo (no reemplazan la revisión de E4).
- `docs/diseno.md`, `docs/dar-01.md`: diseño y alternativas.
- `docs/configuracion.md`, `docs/cr01.md`: control de versiones y cambio solicitado.
- `docs/trazabilidad.md`, `docs/entrega-e4.md`: enlaces y traspaso a QA.
- `resultados/`: archivos generados localmente; no versionados.

### Estado de entregas
**R01–R04:** implementación inicial lista para revisión independiente. **R05:** matriz preliminar, cierre pendiente. **CR01:** documentado, **no implementado** hasta la aprobación registrada por E1. **B1, B2 y etiqueta v0.1:** pendientes de revisión y cierre del equipo.

### Procedencia
Los nombres de variables se inspiran parcialmente en [Vigilancia epidemiológica de malaria — MINSA](https://www.datosabiertos.gob.pe/dataset/vigilancia-epidemiol%C3%B3gica-de-malaria). Los 20 registros son ficticios. Los identificadores, establecimientos y fechas de notificación se incorporaron para el ejercicio académico.

Curso Calidad de Software, UNSA — 2026.
