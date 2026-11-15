# PANVIZ Malaria

Prototipo académico de vigilancia epidemiológica con datos sintéticos. El **TP9** permite importar y validar un CSV, consultar los rechazos, consolidar los registros aceptados por distrito y grupo etario, y publicar un resumen con roles locales simulados. El **TP8** conserva el flujo original de conciliación y exportación a CSV y JSON.

## Pruebas

Desde la raíz de la rama `tp9-incremento`, con **Python 3.10 o posterior**. El proyecto usa la biblioteca estándar. Según el sistema, el comando puede ser `python`, `python3` o `py`.

| Alcance | Comando | Resultado esperado |
| --- | --- | --- |
| Suite completa y regresión T12 | `python -m unittest discover -s tests -v` | 21 comprobaciones correctas, 11 del TP8 y 10 del TP9. |
| Comprobaciones del TP9 | `python -m unittest discover -s tests -p test_tp9.py -v` | 10 comprobaciones correctas. Cubre T01–T08, T11 y la conservación del borrador ante un CSV malformado. |
| Regla del catálogo etario T11 | `python -m unittest discover -s tests -p test_tp9.py -k t11 -v` | Rechaza el grupo fuera del catálogo y conserva los dos válidos. |

T01–T08 comprueban validación, consolidación, tiempos de operación, persistencia y publicación protegida. **T09 y T10 son manuales**. El usuario simulado corrige un registro rechazado en una copia del CSV y verifica la reimportación en T09. En T10 localiza el resumen del distrito asignado. Cada tarea se cronometra por separado, con un límite de 90 segundos y sin ayuda del desarrollador. La sintaxis de la interfaz se puede consultar con `python -m panviz_malaria.tp9 --help`.

La pestaña [Actions](https://github.com/DelCastilloBrad/T8-CMMI-Panviz-Malaria/actions/workflows/pruebas.yml) muestra las ejecuciones de la suite y la conciliación del piloto TP8.

## Demostración del TP9

Los comandos comparten una base SQLite. Para una demostración desde cero, elige una ruta de estado nueva.

```sh
python -m panviz_malaria.tp9 --estado resultados/demo-tp9.sqlite3 importar datos/malaria_tp9_30.csv
python -m panviz_malaria.tp9 --estado resultados/demo-tp9.sqlite3 rechazos
python -m panviz_malaria.tp9 --estado resultados/demo-tp9.sqlite3 resumen
```

La muestra tiene **30 filas**. Se esperan **24 aceptadas, 6 rechazadas y 4 grupos de 6**. La consulta de rechazos muestra la fila, el ID y el motivo. Para un distrito, añade `--distrito NOMBRE_DEL_DISTRITO` después de `resumen`. Cada importación reemplaza el borrador y las consultas posteriores recuperan ese estado desde SQLite.

| Operación de publicación | Subcomando | Resultado |
| --- | --- | --- |
| Publicar el borrador | `publicar --rol publicador` | Guarda una publicación separada del borrador. |
| Intentar publicar como revisor | `publicar --rol revisor` | Devuelve código 3 y conserva la publicación. |
| Consultar la publicación y su historial | `publicado` y `bitacora` | Muestra el resumen publicado y los resultados de los intentos de publicación. |

Para probar estas operaciones, usa el mismo prefijo de los ejemplos, `python -m panviz_malaria.tp9 --estado resultados/demo-tp9.sqlite3`. Los roles elegidos en la consola simulan el control de permisos en el prototipo local.

## Piloto TP8

```sh
python -m panviz_malaria --entrada datos/malaria_20.csv --salida resultados/tp8
```

Se esperan **20 leídos, 15 aceptados y 5 rechazados**, con una diferencia de conciliación de **0**. El piloto genera `resumen.json`, `consolidado.csv` y `rechazos.csv`. Al añadir `--distrito IQUITOS`, también exporta `consolidado_filtrado.csv` (7 grupos con 8 casos).

El código está en [`panviz_malaria/`](panviz_malaria/), las muestras en [`datos/`](datos/), las pruebas en [`tests/`](tests/) y la documentación técnica en [`docs/`](docs/).

Calidad de Software, Escuela Profesional de Ingeniería de Sistemas, UNSA.
