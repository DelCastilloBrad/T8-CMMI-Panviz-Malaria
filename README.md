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
python -m panviz_malaria --entrada datos/malaria_20.csv --salida resultados --distrito IQUITOS
```

Para revisar los resultados en **PowerShell**:

```powershell
Get-Content resultados/resumen.json
Get-Content resultados/consolidado_filtrado.csv
Get-Content resultados/rechazos.csv
```

En **CMD**, usar `type resultados\resumen.json`, `type resultados\consolidado_filtrado.csv` o `type resultados\rechazos.csv`.

Se esperan **11 pruebas correctas (OK)** y, sin filtro, el resumen: **20 leídos, 15 aceptados, 5 rechazados, 14 grupos, suma 15 y diferencia 0**. Con `--distrito IQUITOS`, el resultado filtrado esperado es **7 grupos y suma 8**, sin alterar los totales generales. Si Windows no reconoce `python`, sustituirlo por `py`.

## Ejecución en Pop!_OS / Linux
```bash
git clone https://github.com/DelCastilloBrad/T8-CMMI-Panviz-Malaria.git
cd T8-CMMI-Panviz-Malaria
python3 -m unittest discover -s tests -v
python3 -m panviz_malaria --entrada datos/malaria_20.csv --salida resultados
python3 -m panviz_malaria --entrada datos/malaria_20.csv --salida resultados --distrito IQUITOS
cat resultados/resumen.json
cat resultados/consolidado_filtrado.csv
```


## Guía completa de verificación (desde la carpeta del proyecto)

**Importante:** la carpeta de pruebas se llama `tests` (plural). Ejecutar los comandos desde la raíz del repositorio, donde se encuentran `datos/`, `panviz_malaria/` y `tests/`. No se necesitan dependencias externas.

### Paso 1. Ejecutar las pruebas automatizadas

Linux / Pop!_OS:
```bash
python3 -m unittest discover -s tests -v
```

Windows (PowerShell o CMD):
```powershell
python -m unittest discover -s tests -v
```

**Resultado esperado:** `Ran 11 tests` y `OK`. Incluye T01–T06, T07 (filtro CR01), validación del contrato y grupo etario. Estas son pruebas de desarrollo; E4 debe repetirlas y documentar su revisión independiente.

### Paso 2. Ejecutar el flujo general sin filtro

Linux:
```bash
python3 -m panviz_malaria --entrada datos/malaria_20.csv --salida resultados
```

Windows:
```powershell
python -m panviz_malaria --entrada datos/malaria_20.csv --salida resultados
```

**Resultado esperado:** `leidos=20`, `aceptados=15`, `rechazados=5`, `grupos=14`, `suma_consolidado=15` y `diferencia=0`.

### Paso 3. Ejecutar CR01: filtro por distrito

Linux:
```bash
python3 -m panviz_malaria --entrada datos/malaria_20.csv --salida resultados --distrito IQUITOS
```

Windows:
```powershell
python -m panviz_malaria --entrada datos/malaria_20.csv --salida resultados --distrito IQUITOS
```

**Resultado esperado:** se conservan los totales generales y se añaden `filtro_distrito=IQUITOS`, `grupos_filtrados=7` y `suma_filtrada=8`.

### Paso 4. Revisar las cuatro salidas

Linux:
```bash
cat resultados/resumen.json
cat resultados/consolidado_filtrado.csv
cat resultados/consolidado.csv
cat resultados/rechazos.csv
```

Windows PowerShell:
```powershell
Get-Content resultados/resumen.json
Get-Content resultados/consolidado_filtrado.csv
Get-Content resultados/consolidado.csv
Get-Content resultados/rechazos.csv
```

Windows CMD:
```cmd
type resultados\resumen.json
type resultados\consolidado_filtrado.csv
type resultados\consolidado.csv
type resultados\rechazos.csv
```

Comprobar que el consolidado filtrado contiene **7 filas de datos de IQUITOS, con suma de casos 8**; el consolidado general mantiene **14 grupos y suma 15**. Los rechazos deben corresponder a M-003 (duplicado), M-017 (distrito vacío), M-018 (fecha inválida), M-019 (establecimiento vacío) y M-020 (fecha inválida).

### Paso 5. Comprobar la versión del repositorio

```bash
git status
git log -1 --oneline
```

Para un clon actualizado sin cambios locales, `git status` debe mostrar el árbol de trabajo limpio. La salida de `git log` identifica el commit exacto utilizado en la evidencia.

### Evidencias recomendadas para el informe

Guardar capturas o registros de: **11 pruebas OK**, resumen general, resumen CR01 y CSV filtrado, CSV de rechazos y `git status` / `git log`. Adjuntar el commit revisado. No confundir estas pruebas de desarrollo con la aprobación de E1, la revisión independiente de E4 o la liberación formal B1/B2/v0.1.

El informe T8 fija el oráculo de referencia: **20 leídos, 15 aceptados, 5 rechazados, 14 grupos, suma 15 y diferencia 0**. La semana ISO se deriva de `fecha_notificacion`, que es sintética, no de `semana_sintomas` del conjunto público.

### Archivos
- `panviz_malaria/`: importación, validación, consolidación, filtro CR01, exportación y CLI.
- `datos/malaria_20.csv`: 20 casos sintéticos del piloto.
- `tests/`: pruebas automatizadas de desarrollo (no reemplazan la revisión de E4).
- `docs/diseno.md`, `docs/dar-01.md`: diseño y alternativas.
- `docs/configuracion.md`, `docs/cr01.md`: control de versiones y cambio.
- `docs/trazabilidad.md`, `docs/entrega-e4.md`: enlaces y traspaso a QA.
- `resultados/`: archivos generados localmente; no versionados.

### Estado de entregas
**R01–R04:** implementación inicial lista para revisión independiente. **R05:** matriz actualizada, cierre pendiente. **CR01:** implementado técnicamente, T07 automatizada añadida; **aprobación E1 y revisión E4 pendientes de evidencia**. **B1, B2 y etiqueta v0.1:** pendientes de revisión y cierre del equipo.

### Procedencia
Los nombres de variables se inspiran parcialmente en [Vigilancia epidemiológica de malaria — MINSA](https://www.datosabiertos.gob.pe/dataset/vigilancia-epidemiol%C3%B3gica-de-malaria). Los 20 registros son ficticios. Los identificadores, establecimientos y fechas de notificación se incorporaron para el ejercicio académico.

Curso Calidad de Software, UNSA — 2026.
