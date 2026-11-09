# Panviz–Malaria — piloto CMMI-DEV v1.3

Componente académico independiente de importación, validación, consolidación y exportación de notificaciones **sintéticas** de malaria. Se diseñó tomando como referencia conceptual el producto inicial ISPySA-Pneumonia, pero sin trasladar su modelo predictivo de IRAS. No procesa casos reales ni realiza diagnóstico.

## Requisitos
Python 3.10+; ejecución y pruebas sin paquetes externos.

## Ejecución en Windows (PowerShell o CMD)

**Requisitos:** instalar [Python 3.10 o superior](https://www.python.org/downloads/windows/) y [Git para Windows](https://git-scm.com/downloads/win). Durante la instalación de Python, activar **Add Python to PATH** si se ofrece. Comprobar en la terminal:

```powershell
python --version
git --version
```

Si `python` no se reconoce, probar `py --version` y sustituir `python` por `py` en los comandos siguientes. No es necesario instalar paquetes con pip.

**1. Clonar el proyecto y entrar en la carpeta:**

```powershell
git clone https://github.com/DelCastilloBrad/T8-CMMI-Panviz-Malaria.git
cd T8-CMMI-Panviz-Malaria
```

**2. (Opcional) Crear un entorno virtual** para aislar la ejecución. El proyecto funciona también sin este paso:

PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

CMD:
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

Si PowerShell bloquea la activación por la política de ejecución, se puede **omitir la activación** y usar `.\.venv\Scripts\python.exe` en lugar de `python`, o continuar con el Python instalado normalmente. La carpeta `.venv` no se sube al repositorio.

**3. Ejecutar las pruebas automatizadas:**

```powershell
python -m unittest discover -s tests -v
```

Resultado esperado: **8 pruebas correctas** y `OK`.

**4. Procesar el CSV de ejemplo:**

```powershell
python -m panviz_malaria --entrada datos/malaria_20.csv --salida resultados
```

La salida esperada es:

```json
{
  "leidos": 20,
  "aceptados": 15,
  "rechazados": 5,
  "grupos": 14,
  "suma_consolidado": 15,
  "diferencia": 0
}
```

**5. Consultar los archivos generados:**

PowerShell:
```powershell
Get-Content resultados/resumen.json
Get-Content resultados/rechazos.csv
Get-Content resultados/consolidado.csv
```

CMD:
```cmd
type resultados\resumen.json
type resultados\rechazos.csv
type resultados\consolidado.csv
```

También pueden abrirse los archivos CSV con Excel. Los cinco rechazos esperados son M-003 (duplicado), M-017 (distrito vacío), M-018 (fecha imposible), M-019 (establecimiento vacío) y M-020 (fecha imposible).

**6. (Opcional) Desactivar el entorno virtual:**

```powershell
deactivate
```

**Para el integrante 4 (QA):** seguir además la lista de revisión de [docs/entrega-e4.md](docs/entrega-e4.md) y registrar los resultados en el [Issue #1](https://github.com/DelCastilloBrad/T8-CMMI-Panviz-Malaria/issues/1). Las ejecuciones documentadas hasta ahora son de Linux; la ejecución en Windows debe verificarse y registrarse independientemente.

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
