# Contrato de interfaces — Planificación de rutas de reparto

**Versión:** 1.0
**Fecha:** 24/11/2026
**Propuesta por:** Orquestador
**Estado:** pendiente de validación por el alumno; incluye la corrección D9 recibida antes de la validación.

Este documento es la única fuente de verdad para nombres, firmas, estructuras de datos, reglas de cálculo y comportamiento ante errores. Ningún agente debe inventar un nombre, una firma ni un comportamiento que no figure aquí. Si durante la implementación aparece una situación no descrita, se comunica al orquestador para proponer una versión 1.1 del contrato antes de cambiar la interfaz.

**No contiene código de implementación.** Las firmas que aparecen son declaraciones de interfaz.

---

## 0. Decisiones confirmadas con el orquestador

Las decisiones D1–D8 se preguntaron explícitamente antes de redactar el contrato y fueron aprobadas. D9 es una corrección del enunciado recibida antes de validar el contrato; no modifica D1–D8:

| # | Decisión |
|---|---|
| D1 | `Ruta` se define en `rutas_reparto/punto.py`, junto a `Punto`. |
| D2 | `Planificador.planificar(mapa)` devuelve **un único `Ruta`**; esa `Ruta` lleva `Ruta.nombre`, y la clase del planificador expone además el atributo/propiedad `nombre`. No se devuelve tupla. |
| D3 | `MejoraDosOpt` hereda de `Planificador`, recibe un planificador en el constructor por composición y genera automáticamente el nombre `f"{planificador.nombre} + 2-opt"`. |
| D4 | `filas_descartadas` es `list[tuple[int, str]]`: `(número de línea física del CSV, mensaje de error)`. La cabecera es la línea 1 y la primera fila de datos es la línea 2. Se devuelve ordenado por número de fila. |
| D5 | Con identificadores duplicados se conserva la **primera** aparición válida y se descartan las posteriores con `PuntoDuplicadoError`. |
| D6 | El porcentaje de diferencia es `(longitud - longitud_óptima) / longitud_óptima * 100`, **con signo**, redondeado a 2 decimales; vale `0.0` si la ruta es la óptima y también `0.0` si la óptima tiene longitud `0`. |
| D7 | La tabla usa `tabulate` con `tablefmt="grid"`, tres columnas (`Planificador`, `Longitud`, `Diferencia (%)`) y números formateados a 2 decimales sin símbolo `%`. |
| D8 | Los valores numéricos de control del enunciado los aportará el alumno en la fase de integración; hasta entonces no se da el proyecto por verificado. |
| D9 | `ALM` es el único identificador de almacén y los puntos de entrega usan identificadores con formato `P` seguido de dos dígitos con valor entre 01 y 99 (`P01`…`P99`; no `P00`). En el CSV de control las entregas van de `P01` a `P09`. No se admite cualquier otro identificador como punto de entrega. |

---

## 1. Estructura de ficheros y responsables

| Fichero | Agente responsable | Responsabilidad exacta |
|---|---|---|
| `contrato.md` | Orquestador | Definir interfaces, reglas y criterios de prueba. Único fichero escrito en la fase 1. |
| `rutas_reparto/__init__.py` | Orquestador | Reexportar la API pública. No contiene lógica de negocio. |
| `demo.py` | Orquestador | Cargar datos, ejecutar los 5 planificadores en orden, imprimir tabla y paradas, guardar la figura. |
| `README.md` | Orquestador | Instalación, ejecución, estructura, versiones del contrato y tabla de datos de control. |
| `rutas_reparto/errores.py` | Agente 1 (datos) | Jerarquía de excepciones. Sin dependencias del paquete. |
| `rutas_reparto/punto.py` | Agente 1 (datos) | `Punto` y `Ruta` (D1). Depende solo de `errores`. |
| `rutas_reparto/mapa.py` | Agente 1 (datos) | `MapaReparto`: diccionario de puntos, matriz de distancias y consultas. Depende de `punto` y `errores`. |
| `rutas_reparto/datos_externos.py` | Agente 1 (datos) | `cargar_mapa_csv`: lectura, validación, descartes y construcción del mapa. Depende de `punto`, `mapa`, `errores`. |
| `rutas_reparto/graficas.py` | Agente 1 (datos) | Cálculo del porcentaje, tabla `tabulate` y figura `matplotlib`. Depende de `punto`, `mapa`, `errores`, `tabulate`, `matplotlib`. |
| `rutas_reparto/planificadores.py` | Agente 2 (algoritmos) | `Planificador`, `FuerzaBruta`, `VecinoMasCercano`, `InsercionMasBarata`, `MejoraDosOpt`. Depende de `punto`, `mapa`, `errores`. |
| `tests/test_rutas_reparto.py` | Agente 3 (pruebas) | Al menos 12 pruebas `unittest`, diseñadas **solo leyendo este contrato**, sin consultar el código de los otros agentes. |

### Regla de importación

Para evitar ciclos, los módulos internos importan siempre del módulo concreto (`from rutas_reparto.punto import Punto, Ruta`, etc.). `demo.py` y los tests pueden importar desde la API pública de `rutas_reparto`. El agente 1 no escribe en `planificadores.py`; el agente 2 no escribe en los ficheros del agente 1; el agente 3 no escribe en ningún fichero de implementación.

---

## 2. API pública reexportada por `rutas_reparto/__init__.py`

El paquete expone exactamente estos nombres:

- De `errores`: `RutasError`, `FormatoInvalidoError`, `CoordenadaInvalidaError`, `PuntoDuplicadoError`, `AlmacenNoEncontradoError`, `ParametroInvalidoError`.
- De `punto`: `Punto`, `Ruta`.
- De `mapa`: `MapaReparto`.
- De `planificadores`: `Planificador`, `FuerzaBruta`, `VecinoMasCercano`, `InsercionMasBarata`, `MejoraDosOpt`.
- De `datos_externos`: `cargar_mapa_csv`.
- De `graficas`: `calcular_diferencia`, `formatear_tabla`, `guardar_comparativa`.

No se reexportan alias ni nombres alternativos. No se admiten renombrados como `RutaReparto` o `Mapa`.

---

## 3. Excepciones (`errores.py`)

### 3.1 Jerarquía

```
Exception
└── RutasError
    ├── FormatoInvalidoError
    ├── CoordenadaInvalidaError
    ├── PuntoDuplicadoError
    ├── AlmacenNoEncontradoError
    └── ParametroInvalidoError
```

`RutasError` es la clase base. Todas las clases derivadas heredan directamente de ella, no añaden comportamiento y aceptan un mensaje de texto opcional (`str(exc)` devuelve dicho mensaje). Un `except RutasError` captura cualquier error propio del proyecto.

### 3.2 Cuándo se lanza cada una

| Excepción | Situaciones obligatorias |
|---|---|
| `FormatoInvalidoError` | Cabecera del CSV distinta de `id,nombre,x,y` (nombres o orden). Fila con número de campos distinto de 4. Campo `id` o `nombre` vacío tras quitar espacios. Coordenada vacía o no convertible a `float` (por ejemplo `abc`). Construcción de `Punto` con `id`/`nombre` vacíos o con coordenadas de tipo no numérico. Identificador que no es `ALM` ni `P` seguido de dos dígitos (D9), tanto en el CSV como en `Punto(...)`. |
| `CoordenadaInvalidaError` | Coordenada finita pero fuera del intervalo cerrado `[0, 100]`. Coordenada `NaN` o infinita. Se aplica tanto al CSV como a `Punto(...)`. |
| `PuntoDuplicadoError` | Un `id` ya existente aparece en una fila posterior del CSV (D5) o se intenta introducir dos veces en `MapaReparto`. |
| `AlmacenNoEncontradoError` | `MapaReparto.obtener_almacen()` cuando no existe el id `ALM`. También la lanza `cargar_mapa_csv(...)` cuando, tras descartar filas, no queda ningún punto `ALM`. |
| `ParametroInvalidoError` | Argumento de programa no válido: `FuerzaBruta` con más de 10 entregas; `MejoraDosOpt` cuyo argumento no es `Planificador`; `MapaReparto.distancia`/`longitud` con ids desconocidos o con menos de dos paradas; `Punto.distancia_a` con un objeto que no es `Punto`; `Ruta(...)` con paradas que no empiezan y terminan en `ALM`, con entregas repetidas, con ids de entrega no permitidos por D9, con `nombre` vacío o con `longitud` negativa/no finita; `graficas` con longitudes negativas o con listas de rutas y diferencias de distinta longitud. |
| `FileNotFoundError` | `cargar_mapa_csv` con una ruta inexistente. Se propaga tal cual; no se convierte en `RutasError`. |
| `NotImplementedError` | Llamada directa a `Planificador.planificar(...)` en la clase base. |

**Regla de precedencia en el CSV:** para una fila se comprueba, en este orden, número de campos → `id`/`nombre` vacíos → formato del `id` (D9) → conversión numérica → rango → duplicado. Solo se registra el **primer** error de cada fila.

---

## 4. Modelo de datos

### 4.1 `Punto` (`rutas_reparto/punto.py`)

**Constructor:** `Punto(id: str, nombre: str, x: float, y: float)`

- `id`: cadena no vacía tras `strip()` que debe ser exactamente `ALM` o `P` seguido de dos dígitos entre 01 y 99 (`P01`…`P99`, no `P00`; D9); cualquier otro valor lanza `FormatoInvalidoError`.
- `nombre`: cadena no vacía tras `strip()`. Se conserva tal cual se recibe; la normalización de espacios del CSV se hace en `cargar_mapa_csv`.
- `x` e `y`: `int` o `float` (no `bool`), finitos y en `[0, 100]`. Se almacenan convertidos a `float`.
- Atributos públicos de solo lectura por convención: `id: str`, `nombre: str`, `x: float`, `y: float`.
- Excepciones: `FormatoInvalidoError` (strings vacíos, id no permitido por D9 o tipo no numérico), `CoordenadaInvalidaError` (fuera de rango, `NaN`, infinito).

**Método:** `distancia_a(self, otro: Punto) -> float`

- Devuelve la distancia euclídea en línea recta: raíz cuadrada de `(self.x - otro.x)² + (self.y - otro.y)²`, redondeada con `round(resultado, 2)`.
- Lanza `ParametroInvalidoError` si `otro` no es una instancia de `Punto`.
- Es coherente con la matriz: `mapa.distancia(a, b) == mapa.puntos[a].distancia_a(mapa.puntos[b])`.

**Métodos especiales:**

- `__repr__() -> str` devuelve exactamente `Punto(id='ALM', nombre='Almacén do Tambre', x=50.0, y=50.0)` (comillas simples alrededor de cadenas, tal como `repr(str)`).
- `__eq__(self, otro: object) -> bool`: `True` solo si `otro` es `Punto` y coinciden `id`, `nombre`, `x` e `y`. `__hash__` coherente con esos cuatro valores.

### 4.2 `Ruta` (`rutas_reparto/punto.py`, D1)

**Constructor:** `Ruta(nombre: str, paradas: Sequence[str], longitud: float)`

- `nombre`: cadena no vacía; se guarda tal cual (la demo usa los nombres definidos en el apartado 6).
- `paradas`: secuencia de cadenas; se guarda como `list[str]` nueva (copia). Debe cumplir el formato del apartado 5.3: longitud ≥ 2, `paradas[0] == paradas[-1] == "ALM"`, las paradas intermedias sin repeticiones y cada una con un id `Pnn` válido según D9. Para cero entregas, `["ALM", "ALM"]` es válido.
- `longitud`: número finito ≥ 0; se guarda como `float(round(longitud, 2))`.
- Excepciones: `ParametroInvalidoError` en cualquiera de las validaciones anteriores.

**Atributos públicos:** `nombre: str`, `paradas: list[str]`, `longitud: float`.

**Métodos especiales:**

- `__repr__() -> str` devuelve exactamente `Ruta(nombre='Fuerza bruta', paradas=['ALM', 'P01', 'ALM'], longitud=99.3)` (misma forma que `repr` de los atributos).
- `__eq__`: `True` solo si coinciden `nombre`, `paradas` y `longitud`.

### 4.3 `MapaReparto` (`rutas_reparto/mapa.py`)

**Constructor:** `MapaReparto(puntos: Iterable[Punto])`

- Construye `puntos: dict[str, Punto]` indexado por `Punto.id`, conservando el orden de inserción.
- Si un elemento no es `Punto`: `ParametroInvalidoError`. Si un `id` aparece dos veces: `PuntoDuplicadoError`.
- Precalcula `distancias: dict[str, dict[str, float]]`: para cada par de ids (incluido el mismo id, con valor `0.0`), `distancias[id_a][id_b] = puntos[id_a].distancia_a(puntos[id_b])`. Es simétrica y usa valores ya redondeados a 2 decimales.
- El constructor **no** exige que exista `ALM`; la ausencia se detecta al llamar a `obtener_almacen()` o en `cargar_mapa_csv`. Así se pueden construir mapas sintéticos en las pruebas.

**Atributos públicos:** `puntos: dict[str, Punto]`, `distancias: dict[str, dict[str, float]]`.

**Métodos:**

| Método | Contrato |
|---|---|
| `obtener_almacen(self) -> Punto` | Devuelve `self.puntos["ALM"]`. Lanza `AlmacenNoEncontradoError` si no existe. |
| `obtener_entregas(self) -> list[str]` | Devuelve una lista nueva con todos los ids de entrega (formato `Pnn` según D9), ordenada alfabéticamente con la ordenación por defecto de cadenas de Python (`sorted`). |
| `distancia(self, id_a: str, id_b: str) -> float` | Devuelve `self.distancias[id_a][id_b]` (ya redondeado a 2 decimales). Lanza `ParametroInvalidoError` si alguno de los ids no está en el mapa. |
| `longitud(self, paradas: Sequence[str]) -> float` | Suma las distancias de los tramos consecutivos tomadas de la matriz (ya redondeadas) y devuelve `round(suma, 2)`. Con menos de dos paradas, o con un id desconocido, lanza `ParametroInvalidoError`. |

No hay otros métodos públicos obligatorios en `MapaReparto`.

---

## 5. Reglas obligatorias de cálculo

### 5.1 Distancia

Euclídea en línea recta entre las coordenadas `x, y`, con `round(..., 2)` de Python (redondeo half-to-even del tipo `float`; por ejemplo, cuando el tercer decimal es exactamente 5 se aplica el comportamiento de `round`). Todas las distancias que se guarden en la matriz, y por tanto todas las que usen los algoritmos, son valores redondeados a 2 decimales.

### 5.2 Longitud de ruta

Se suman **las distancias de los tramos previamente redondeadas** y al total se le aplica `round(..., 2)`. Ejemplo: `ALM → P01 → ALM` con distancia de tramo `49.65` tiene longitud `99.3` (no `99.30` como valor numérico; la representación con dos decimales se aplica solo al imprimir).

### 5.3 Formato de ruta

`list[str]` que empieza y termina en `"ALM"` y contiene cada punto de entrega exactamente una vez. Cero entregas ⇒ `["ALM", "ALM"]`, longitud `0.0`. Solo son entregas los ids con formato `P` seguido de dos dígitos (D9); `ALM` es exclusivamente el almacén y no puede aparecer como entrega. No se admite cualquier otro identificador.

### 5.4 Desempates

Orden alfabético = orden lexicográfico por defecto de `str` en Python (`P03 < P07`). Regla general: ante un empate se elige el **identificador menor**. Si tras el identificador sigue habiendo empate (inserción), se elige la **posición más cercana al principio de la ruta**. En fuerza bruta, al empatar se conserva la primera ruta encontrada.

### 5.5 Comparaciones de longitud

Las decisiones de "estrictamente más corta" (fuerza bruta y 2-opt) se toman comparando los valores de longitud **ya redondeados a 2 decimales**. Una mejora real menor que media centésima no produce cambio. El operador es siempre `<`, nunca `<=`.

### 5.6 Coste de inserción

Para insertar `p` entre `a` y `b`:

`coste = round(dist(a, p) + dist(p, b) - dist(a, b), 2)`

donde las tres distancias proceden de la matriz y ya están redondeadas. La clave de selección es `(coste, id_p, posición)`, minimizada en ese orden.

### 5.7 Porcentaje de diferencia

`diferencia = round((longitud - longitud_óptima) / longitud_óptima * 100, 2)`; `0.0` si `longitud_óptima == 0`. Positivo significa peor que la óptima; negativo, mejor (solo posible si la supuesta óptima no lo fuera). Implementado por `calcular_diferencia`.

---

## 6. Planificadores (`rutas_reparto/planificadores.py`, agente 2)

Todos los planificadores devuelven `Ruta` (D2) y son intercambiables: la demo itera sobre una lista de `Planificador` sin usar `isinstance`, `type` ni ramas por tipo.

### 6.1 `Planificador`

- Clase base. Atributo de clase `nombre: str = ""`.
- Método abstracto por convención: `planificar(self, mapa: MapaReparto) -> Ruta`. En la base lanza `NotImplementedError`.
- Ninguna clase concreta cambia la firma.

### 6.2 `FuerzaBruta(Planificador)`

- `nombre = "Fuerza bruta"`.
- `planificar(mapa) -> Ruta`.
- Obtiene las entregas con `mapa.obtener_entregas()` (ya alfabéticas). Si hay más de 10, lanza `ParametroInvalidoError` **antes** de generar permutaciones.
- Recorre `itertools.permutations(entregas)` en el orden natural que produce la lista ordenada (primer orden = orden alfabético). Para cada permutación construye la secuencia formada por `ALM`, las entregas de la permutación en ese orden y de nuevo `ALM`, y calcula su longitud con `mapa.longitud`.
- Mantiene la primera mejor ruta; solo sustituye si `longitud < mejor_longitud` (estricto, apartado 5.5). Con empate se conserva la primera encontrada.
- Con cero entregas devuelve `Ruta("Fuerza bruta", ["ALM", "ALM"], 0.0)`.
- Es la ruta óptima: ningún otro planificador puede tener longitud menor que ella con las mismas reglas de redondeo.

### 6.3 `VecinoMasCercano(Planificador)`

- `nombre = "Vecino más cercano"`.
- Parte de `ALM`. Mientras queden entregas, elige la de menor distancia desde la parada actual; si hay empate, la de id menor (`min(..., key=(distancia, id))`).
- Cierra con `ALM` y calcula la longitud con `mapa.longitud`. Cero entregas ⇒ `["ALM", "ALM"]`, `0.0`.

### 6.4 `InsercionMasBarata(Planificador)`

- `nombre = "Inserción más barata"`.
- Primera parada: la entrega más cercana a `ALM`; empate por id menor. Ruta inicial `["ALM", primero, "ALM"]`.
- Mientras queden entregas, evalúa **toda** combinación `(entrega pendiente, posición de inserción)`; posiciones `1 ... len(ruta)-1`, es decir, entre `ruta[pos-1]` y `ruta[pos]` (no se inserta antes de `ALM` ni después del `ALM` final).
- Elige el mínimo según `(coste, id, posición)` (apartado 5.6), inserta y repite.
- Cero entregas ⇒ `["ALM", "ALM"]`, `0.0`. Longitud final con `mapa.longitud`.

### 6.5 `MejoraDosOpt(Planificador)` (D3)

- Constructor: `MejoraDosOpt(planificador: Planificador)`. Guarda el objeto en `self.planificador`. Si no es `Planificador`: `ParametroInvalidoError`.
- `nombre` es una propiedad calculada: `f"{self.planificador.nombre} + 2-opt"`. Por tanto, con los planificadores de esta sección los nombres son exactamente `"Vecino más cercano + 2-opt"` e `"Inserción más barata + 2-opt"`.
- `planificar(mapa) -> Ruta`:
  1. Obtiene `ruta_inicial = self.planificador.planificar(mapa)` y trabaja sobre una copia de `ruta_inicial.paradas`; no modifica la ruta original.
  2. Si hay menos de dos entregas, devuelve la ruta inicial con `self.nombre` y la misma longitud.
  3. Índices: `i` recorre `1 .. len(paradas)-3` (primera entrega en adelante) y `j` recorre `i+1 .. len(paradas)-2` (hasta la última entrega), siempre en orden creciente. `j > i`.
  4. Se invierte el orden de las paradas comprendidas entre `i` y `j`, ambos inclusive, dejando el resto de la ruta igual. Se calcula la longitud de la ruta resultante con `mapa.longitud`.
  5. Si es **estrictamente menor** que la longitud actual (apartado 5.5), se aplica de inmediato, se actualiza la longitud y **se continúa la misma pasada** con el siguiente `j` (sin reiniciar ni romper el bucle).
  6. Repetir pasadas completas hasta que una pasada termine sin ningún cambio. Entonces devolver `Ruta(self.nombre, paradas_finales, longitud_final)`.

---

## 7. Carga de datos (`rutas_reparto/datos_externos.py`, agente 1)

**Función:** `cargar_mapa_csv(ruta: str | Path) -> tuple[MapaReparto, list[tuple[int, str]]]`

1. Abrir con codificación `utf-8-sig` y `newline=""` (el CSV puede traer BOM y saltos CRLF). `ruta` puede ser relativa o absoluta. Si no existe: `FileNotFoundError`.
2. Leer la cabecera. Debe ser exactamente `["id", "nombre", "x", "y"]` en ese orden y con esos nombres; en caso contrario lanzar `FormatoInvalidoError` con el mensaje `El CSV debe tener exactamente las columnas id,nombre,x,y`.
3. Numerar las líneas con `enumerate` empezando en 1 para la cabecera; la primera fila de datos es la línea 2 (D4). Las líneas vacías cuentan como fila de datos y se descartan por número de campos.
4. Para cada fila, quitar espacios en blanco a cada campo y aplicar la precedencia del apartado 3.2. Las filas válidas se añaden al diccionario de puntos; las inválidas se descartan y se registra `(numero_de_linea, mensaje)` donde `mensaje = f"{NombreDeLaExcepcion}: {texto}"`.
5. Textos obligatorios de los mensajes descartados:

| Error | Texto exacto del mensaje |
|---|---|
| Número de campos | `Se esperaban 4 columnas, se obtuvieron {n}` |
| `id` vacío | `El campo id está vacío` |
| Identificador no permitido (D9) | `El identificador {id!r} no es válido; se espera ALM o P seguido de dos dígitos entre 01 y 99` |
| `nombre` vacío | `El campo nombre está vacío` |
| Coordenada no numérica | `La coordenada {x o y} no es numérica: {valor!r}` |
| Coordenada fuera de rango o no finita | `La coordenada {x o y}={valor} está fuera del intervalo [0, 100]` |
| Duplicado | `El identificador {id!r} ya existe` |

6. Tras procesar todas las filas, si `"ALM"` no está entre los puntos válidos, lanzar `AlmacenNoEncontradoError` (no se devuelve un mapa parcial).
7. Devolver `(MapaReparto(puntos_validos), descartes)` con `descartes` ordenado por número de fila ascendente.

**Datos de control del CSV incluido en el repositorio (`datos/puntos_reparto.csv`):** debe cargar 10 puntos (`ALM` y `P01`…`P09`) y descartar 4 filas: línea 6 (`P10`, `x=105` → `CoordenadaInvalidaError`), línea 9 (`P11`, `x=abc` → `FormatoInvalidoError`), línea 12 (`P03` duplicado de la línea 5 → `PuntoDuplicadoError`) y línea 14 (`P12`, `y` vacío → `FormatoInvalidoError`). Con esos puntos hay 9 entregas, dentro del límite de fuerza bruta. Los ids `P10`, `P11` y `P12` cumplen el formato `Pnn` de D9, por lo que sus filas se descartan por las causas indicadas (coordenada no válida o duplicado), no por el identificador.

---

## 8. Resultados (`rutas_reparto/graficas.py`, agente 1)

### 8.1 `calcular_diferencia(longitud: float, longitud_optima: float) -> float`

Aplica la regla 5.7. `ParametroInvalidoError` si alguno de los dos valores es negativo o no finito. Devuelve `float`.

### 8.2 `formatear_tabla(filas: Sequence[tuple[str, float, float]]) -> str`

- Cada fila es `(nombre_del_planificador, longitud, porcentaje)`.
- Convierte `longitud` y `porcentaje` a cadenas con formato `f"{valor:.2f}"` antes de pasarlas a `tabulate`.
- Llama a `tabulate(cuerpo, headers=["Planificador", "Longitud", "Diferencia (%)"], tablefmt="grid")`.
- Devuelve la cadena resultante; no imprime por pantalla (la demo la imprime).

### 8.3 `guardar_comparativa(rutas, diferencias, ruta_optima, mapa, archivo="comparativa_rutas.png") -> Path`

Firma exacta:
`guardar_comparativa(rutas: Sequence[Ruta], diferencias: Sequence[float], ruta_optima: Ruta, mapa: MapaReparto, archivo: str | Path = "comparativa_rutas.png") -> Path`

- `rutas` y `diferencias` tienen la misma longitud y están en el orden de ejecución de la demo; `diferencias[k]` corresponde a `rutas[k]`. Si no: `ParametroInvalidoError`.
- Crea una cuadrícula de 3 columnas y `ceil((len(rutas)+1)/3)` filas. Los primeros `len(rutas)` ejes muestran, para cada planificador:
  - puntos de entrega dispersos y almacén con marca/color distinto, usando `mapa.puntos`;
  - la ruta óptima de fondo en línea discontinua gris (etiqueta `Óptima`);
  - la ruta del planificador en línea continua con marcadores (etiqueta `ruta.nombre`);
  - título `ruta.nombre`, ejes con igual escala, rejilla tenue y leyenda.
- El último eje es una gráfica de barras: una barra por planificador con su `diferencias[k]`, línea horizontal en 0, etiquetas de los nombres rotadas para que no se solapen, valor anotado con 2 decimales y etiqueta del eje Y `Diferencia (%)`.
- Guarda con `fig.savefig(archivo, dpi=150, bbox_inches="tight")`, cierra la figura con `plt.close(fig)` y **no llama nunca a `plt.show()`** (la generación debe funcionar sin pantalla).
- Devuelve `Path(archivo)`.
- El fichero generado se llama `comparativa_rutas.png` cuando la demo no pasa otro nombre.

---

## 9. Demo (`demo.py`, orquestador)

Orden de ejecución obligatorio:

1. Resolver el CSV como `Path(__file__).resolve().parent / "datos" / "puntos_reparto.csv"` para que funcione desde cualquier directorio de trabajo.
2. `cargar_mapa_csv(...)` e imprimir primero `Puntos cargados: {n}` y una línea por punto ordenada por id con el formato `  {id}: {nombre} ({x:.2f}, {y:.2f})`. Después imprimir `Filas descartadas: {n}` y una línea por descarte con el formato `  Fila {numero}: {mensaje}`.
3. Crear la lista de planificadores, exactamente en este orden y sin comprobaciones de tipo:
   1. `FuerzaBruta()`
   2. `VecinoMasCercano()`
   3. `InsercionMasBarata()`
   4. `MejoraDosOpt(VecinoMasCercano())`
   5. `MejoraDosOpt(InsercionMasBarata())`
4. Ejecutar `planificar(mapa)` para cada uno y guardar las cinco rutas en una lista. La primera es la óptima; no se ejecuta fuerza bruta dos veces.
5. Calcular diferencias con `calcular_diferencia(ruta.longitud, ruta_optima.longitud)` para las cinco rutas.
6. Imprimir `formatear_tabla([(ruta.nombre, ruta.longitud, diferencia), ...])`.
7. Imprimir `Orden de paradas:` y, para cada ruta, `  {ruta.nombre}: {' -> '.join(ruta.paradas)}`.
8. Llamar a `guardar_comparativa(rutas, diferencias, ruta_optima, mapa, "comparativa_rutas.png")` e imprimir `Figura guardada en: {ruta_devuelta}`.

La demo no define algoritmos propios, no valida formatos por su cuenta y no crea excepciones nuevas.

---

## 10. Criterios para las pruebas (agente 3)

`tests/test_rutas_reparto.py` debe usar `unittest.TestCase` y contener **al menos 12 métodos de prueba**. El agente 3 diseña las aserciones leyendo **solo este contrato y el CSV**; no abre los ficheros de implementación. Puede crear mapas sintéticos con `Punto(...)` y `MapaReparto([...])` y definir un planificador stub en el propio fichero de pruebas para forzar una ruta concreta.

Cobertura obligatoria (los valores son los que se deducen del contrato):

| # | Prueba obligatoria |
|---|---|
| T1 | Con ids válidos según D9 (por ejemplo `ALM` y `P01`), `distancia_a` entre `(0, 0)` y `(3, 4)` devuelve `5.0`; además un caso con redondeo a 2 decimales. |
| T2 | `Punto` con id válido y coordenada fuera de `[0,100]` lanza `CoordenadaInvalidaError`; con coordenada `abc` lanza `FormatoInvalidoError`; con id no permitido por D9 lanza `FormatoInvalidoError`. |
| T3 | `Ruta` rechaza paradas que no empiezan/terminan en `ALM` y entregas repetidas (`ParametroInvalidoError`); `repr` contiene nombre, paradas y longitud. |
| T4 | `MapaReparto` con `ALM`, `P01`, `P02`: matriz simétrica, diagonal `0.0`, y distancia `ALM↔P01` correcta según coordenadas elegidas. |
| T5 | `obtener_entregas()` devuelve ids ordenados alfabéticamente; `obtener_almacen()` sin `ALM` lanza `AlmacenNoEncontradoError`. |
| T6 | `longitud(["ALM","P01","ALM"])` suma tramos ya redondeados (ej. `49.65 + 49.65 == 99.3`). |
| T7 | `cargar_mapa_csv` sobre `datos/puntos_reparto.csv`: 10 puntos, 4 descartes con filas exactas `[6, 9, 12, 14]` y tipos de error `[CoordenadaInvalidaError, FormatoInvalidoError, PuntoDuplicadoError, FormatoInvalidoError]`. |
| T8 | `FuerzaBruta` con 11 entregas (ids `P01`…`P11`, válidos según D9) lanza `ParametroInvalidoError`. |
| T9 | `FuerzaBruta` con dos entregas empatadas conserva el orden alfabético de la primera ruta encontrada. |
| T10 | `VecinoMasCercano` resuelve un empate eligiendo el id menor. |
| T11 | `InsercionMasBarata` con `ALM(0,0)`, `P01(10,0)`, `P02(0,10)`, `P03(10,10)` produce `['ALM','P02','P03','P01','ALM']` con longitud `40.0` (según reglas 5.1, 5.2 y 5.6). |
| T12 | `MejoraDosOpt` con un planificador stub (nombre `"Stub"`) que devuelve `['ALM','P01','P02','P03','ALM']` sobre `ALM(0,0)`, `P01(10,0)`, `P02(0,10)`, `P03(10,10)` mejora a `['ALM','P01','P03','P02','ALM']` con longitud `40.0` y nombre `"Stub + 2-opt"`. |
| T13 | `calcular_diferencia(105, 100) == 5.0`, `calcular_diferencia(95, 100) == -5.0` y `calcular_diferencia(0, 0) == 0.0`. |
| T14 | `formatear_tabla` usa cabeceras exactas, `tablefmt="grid"` y dos decimales (comprobar presencia de `Diferencia (%)` y `5.00`). |
| T15 | Los cinco planificadores devuelven rutas válidas sobre el CSV y ninguna es más corta que `FuerzaBruta`. |

Reglas para el agente 3: una sola aserción conceptual por prueba cuando sea posible; mensajes de aserción descriptivos; sin depender del orden de ejecución de las pruebas; sin leer ni modificar los ficheros de los agentes 1 y 2. El comando de ejecución será `python -m unittest discover -s tests -v`.

---

## 11. Integración y verificación final (orquestador)

1. Fase 1: orquestador escribe solo `contrato.md`.
2. Fase 2: encargos paralelos al agente 1 (cinco ficheros), agente 2 (`planificadores.py`) y agente 3 (`tests/test_rutas_reparto.py`, sin acceso al código). Cada agente recibe este contrato como referencia obligatoria.
3. Fase 3: orquestador escribe `rutas_reparto/__init__.py`, `demo.py` y `README.md`; ejecuta la demo y las pruebas.
4. Ante cada fallo se identifica la causa, se asigna al agente responsable según la tabla del apartado 1 y se relanza un encargo de corrección concreto. Si la causa es ambigüedad del contrato, se propone explícitamente una versión 1.1 y se avisa antes de cambiar nada.
5. La verificación final compara la salida con los datos de control que aportará el alumno (D8): puntos cargados, filas descartadas y las cinco longitudes. Además se comprueba que `comparativa_rutas.png` existe y que las pruebas pasan.

### Contenido obligatorio de `README.md`

Instalación de dependencias (`tabulate`, `matplotlib`), árbol de ficheros, ejecución (`python demo.py`), ejecución de pruebas (`python -m unittest discover -s tests -v`), tabla de datos de control y registro de la versión 1.0 de este contrato.

---

## 12. Casos límite cubiertos

| Caso | Comportamiento |
|---|---|
| CSV sin `ALM` | `AlmacenNoEncontradoError` en `cargar_mapa_csv`; en un `MapaReparto` construido a mano, al llamar a `obtener_almacen()`. |
| Cero entregas | Todas las rutas son `["ALM","ALM"]` con longitud `0.0`; porcentajes `0.0`. |
| Una entrega | `["ALM","P01","ALM"]`; 2-opt no puede mejorar. |
| Más de 10 entregas | Solo falla `FuerzaBruta` (`ParametroInvalidoError`); los demás planificadores funcionan. |
| Empate de distancias | id alfabéticamente menor; en inserción, además, posición más temprana. |
| Distancias que empatan tras redondear | Se tratan como iguales; no se aplica cambio en 2-opt ni reemplazo en fuerza bruta. |
| Identificador de entrega no permitido (por ejemplo `X01` o `pedido1`) | `FormatoInvalidoError` en `Punto(...)` y descarte de la fila del CSV con su número (D9). |
| Coordenada exactamente `0` o `100` | Válida (intervalo cerrado). |
| Coordenada `NaN`/infinita | `CoordenadaInvalidaError`. |
| Fila con espacios sobrantes | Se normaliza con `strip()` antes de validar. |
| Encabezado con columnas cambiadas de orden | `FormatoInvalidoError`; no se devuelven descartes. |
