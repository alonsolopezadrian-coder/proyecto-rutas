# Planificación de rutas de reparto

Proyecto de la unidad 2: planifica rutas de reparto desde un almacén (`ALM`) y varios puntos de entrega (`P01`…`P99`) usando cuatro estrategias y una mejora 2-opt. Los datos de entrada están en `datos/puntos_reparto.csv`.

## Requisitos

- Python 3.10 o superior (se usan anotaciones `str | Path` y tipos genéricos integrados).
- Dependencias externas:

| Paquete | Uso |
|---|---|
| `tabulate` | Tabla comparativa en formato `grid`. |
| `matplotlib` | Figura `comparativa_rutas.png` (mapa por planificador más gráfica de barras). |

Instalación desde la raíz del repositorio:

```bash
python -m pip install tabulate matplotlib
```

No hay dependencias externas para la carga del CSV ni para los algoritmos: usan solo la biblioteca estándar (`csv`, `math`, `itertools`, `pathlib`, `re`, `typing`).

## Estructura del proyecto

```text
proyecto-rutas/
├── contrato.md                    # Contrato de interfaces v1.0 (D1–D9)
├── demo.py                        # Demostración: carga, ejecución y resultados
├── README.md                      # Este fichero
├── datos/
│   └── puntos_reparto.csv         # Datos de entrada (contiene filas incorrectas)
├── rutas_reparto/
│   ├── __init__.py                # API pública (reexportaciones del contrato)
│   ├── errores.py                 # Jerarquía de excepciones
│   ├── punto.py                   # Punto y Ruta
│   ├── mapa.py                    # MapaReparto y matriz de distancias
│   ├── planificadores.py          # FuerzaBruta, VecinoMasCercano, InsercionMasBarata, MejoraDosOpt
│   ├── datos_externos.py          # cargar_mapa_csv
│   └── graficas.py                # calcular_diferencia, formatear_tabla, guardar_comparativa
└── tests/
    ├── __init__.py                # Paquete de pruebas
    └── test_rutas_reparto.py      # Pruebas unitarias (unittest)
```

## Ejecución de la demo

Desde la raíz del repositorio:

```bash
python demo.py
```

La demo:

1. Carga `datos/puntos_reparto.csv` con una ruta independiente del directorio de trabajo.
2. Informa de los puntos cargados y de las filas descartadas, con su número de línea y motivo.
3. Ejecuta, en este orden y sin distinciones de tipo: fuerza bruta, vecino más cercano, inserción más barata, vecino más cercano + 2-opt e inserción más barata + 2-opt.
4. Imprime la tabla comparativa (`Planificador`, `Longitud`, `Diferencia (%)`).
5. Imprime el orden de paradas de cada ruta.
6. Guarda `comparativa_rutas.png` en el directorio actual.

## Ejecución de las pruebas

Desde la raíz del repositorio:

```bash
python -m unittest discover -s tests -v
```

Las pruebas están diseñadas exclusivamente a partir del contrato y del CSV, y cubren los casos T1–T15 del apartado 10 del contrato más casos límite adicionales.

## Reglas de cálculo aplicadas

- La distancia entre dos puntos es euclídea y se redondea a dos decimales.
- La longitud de una ruta suma los tramos **ya redondeados** y redondea el total a dos decimales.
- Una ruta empieza y termina en `ALM` y visita cada entrega una sola vez.
- Los desempates se resuelven por identificador alfabético menor; en inserción, después por posición más temprana.
- Fuerza bruta admite como máximo 10 entregas y conserva la primera ruta en caso de empate.
- El porcentaje de diferencia es `(longitud - longitud_óptima) / longitud_óptima * 100`, con signo.

## Datos de control

Los valores marcados como *pendientes* se cumplimentarán en la verificación final con la salida real de la demo y con los valores que aporte el alumno (decisión D8 del contrato).

| Dato | Valor esperado | Valor obtenido | ¿Coincide? |
|---|---|---|---|
| Puntos cargados | 10 (`ALM` y `P01`…`P09`) | Pendiente de ejecutar | — |
| Filas descartadas | 4 (líneas 6, 9, 12 y 14) | Pendiente de ejecutar | — |
| Longitud: Fuerza bruta | Pendiente de aportar | Pendiente de ejecutar | — |
| Longitud: Vecino más cercano | Pendiente de aportar | Pendiente de ejecutar | — |
| Longitud: Inserción más barata | Pendiente de aportar | Pendiente de ejecutar | — |
| Longitud: Vecino más cercano + 2-opt | Pendiente de aportar | Pendiente de ejecutar | — |
| Longitud: Inserción más barata + 2-opt | Pendiente de aportar | Pendiente de ejecutar | — |

Las filas incorrectas del CSV son: línea 6 (`P10`, `x=105`, fuera de rango), línea 9 (`P11`, `x=abc`, no numérico), línea 12 (`P03` duplicado) y línea 14 (`P12`, `y` vacío). Los identificadores `P10`, `P11` y `P12` cumplen el formato `Pnn` de la decisión D9, por lo que se descartan por las causas indicadas, no por el identificador.

## Contrato

La versión vigente es **1.0** (24/11/2026), con las decisiones D1–D8 aprobadas y la corrección D9 incorporada antes de la validación: `ALM` es el almacén, los mapas en general usan entregas `P01`…`P99` y el CSV de control contiene `P01`…`P09`. El contrato completo está en `contrato.md`.
