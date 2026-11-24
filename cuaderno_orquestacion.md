# Cuaderno de orquestación

> Plantilla del ejercicio práctico 3 (sección 2.14). Copia este fichero en la raíz de tu repositorio, rellénalo **a medida que trabajas** (no al final) y súbelo junto con el código. Borra los textos de ejemplo en cursiva.

## 1. Ficha

| Campo | Contenido |
|---|---|
| Nombre y apellidos | Adrián Alonso López |
| Repositorio (URL) | https://github.com/alonsolopezadrian-coder/proyecto-rutas |
| Vídeo (URL) | |
| Fecha de inicio | 24/11/2026 |
| Fecha de entrega | |

### Agentes

Recuerda: cada agente usa un **modelo gratuito diferente** en OpenCode (cuatro modelos distintos en total).

- Versión de OpenCode y sistema operativo:

Versión de OpenCode: 2.4.1
Sistema operativo: Windows 10

| Agente (fichero) | Modelo gratuito (`proveedor/modelo`) | Ficheros de los que es responsable | ¿Cambiaste de modelo durante el trabajo? ¿Por cuál? |
|---|---|---|---|
| Orquestador (`orquestador.md`) | opencode/big-pickle | `contrato.md`, `demo.py`, `README.md`, integración | |
| Agente 1: Datos (`datos.md`) | opencode/deepseek-v4.1-flash-free | `errores.py`, `punto.py`, `mapa.py`, `datos_externos.py`, `graficas.py` | |
| Agente 2: Algoritmos (`algoritmos.md`) | opencode/nemotron-3.5-super-vl-free | `planificadores.py` | |
| Agente 3: Pruebas (`pruebas.md`) | opencode/mimo-v2.6-flash-free | `tests/test_rutas_reparto.py` | |

¿Has modificado las instrucciones de algún fichero de agente respecto a la plantilla? Indica cuál, qué y por qué:

No se han modificado las instrucciones ni las responsabilidades de los cuatro agentes. Únicamente se han sustituido los identificadores de modelo de las plantillas por cuatro modelos gratuitos distintos.


## 2. Contrato de interfaces

El contrato está en `contrato.md`, en la raíz del repositorio. Aquí solo se registran sus versiones.

| Versión | Fecha | Cambio | Quién lo propuso (orquestador o agente) | Por qué |
|---|---|---|---|---|
| 1.0 | 24/11/2026 | Versión inicial con corrección D9 sobre los identificadores de entrega antes de su validación | Orquestador | Definir las interfaces, responsabilidades y reglas de cálculo sin ambigüedades. |
| | | | | |

## 3. Registro de sesiones

Una fila por cada sesión de OpenCode: las sesiones principales con el orquestador y las sesiones hijas de cada subagente (incluidas las de reanudación).

| N.º | Fecha y hora | Agente | Motivo (encargo inicial, corrección, reanudación...) | ¿Respetó qué ficheros podía leer? | Captura o exportación de la sesión |
|---|---|---|---|---|---|
| 1 | 24/11/2026 | Orquestador | Generación y revisión del contrato de interfaces | Sí | exportación sesión  |
| 2 | 24/11/2026 | Datos | Implementar módulos de datos | Sí. Solo contrato, CSV y sus cinco ficheros asignados | exportación sesión |
| 3 | 24/11/2026 | Algoritmos | Implementar planificadores | Sí. Solo contrato y planificadores.py | exportación sesión |
| 4 | 24/11/2026 | Pruebas | Diseñar pruebas unitarias | Sí. No leyó código de implementación; solo contrato, enunciado y CSV | exportación sesión |

## 4. Registro de encargos

Una entrada por cada encargo a un agente: tus instrucciones al orquestador y los encargos que el orquestador pasa a cada subagente (los ves en su sesión hija). Copia el texto **completo**.

### Encargo E1

- **Agente:** Orquestador
- **Sesión n.º:** 1
- **Prompt enviado:**

```
Vamos a realizar el proyecto de planificación de rutas de reparto.

En esta primera fase quiero que te encargues exclusivamente de analizar el enunciado y redactar el archivo contrato.md en la raíz del proyecto.

IMPORTANTE:
- No implementes código.
- No modifiques ningún archivo de los subagentes.
- No delegues todavía tareas a los subagentes.
- No crees ni modifiques otros archivos.
- Tu único archivo de salida en esta fase debe ser contrato.md.
- Si encuentras alguna ambigüedad que impida definir correctamente una interfaz o un comportamiento, pregúntame antes de inventar una solución.

ESTRUCTURA Y REQUISITOS DEL PROYECTO

El proyecto debe permitir planificar rutas de reparto a partir de un almacén y varios puntos de entrega.

El CSV datos/puntos_reparto.csv contiene las columnas:
- id
- nombre
- x
- y

El almacén se identifica como ALM y los puntos de entrega como P01, P02, etc. Las coordenadas deben estar dentro del intervalo 0–100. El CSV contiene intencionadamente filas incorrectas: coordenadas fuera del mapa, valores no numéricos e identificadores duplicados. Se deben descartar e informar las filas erróneas indicando su número.

ESTRUCTURA DE MÓDULOS

El proyecto tendrá estos módulos:

- rutas_reparto/errores.py
- rutas_reparto/punto.py
- rutas_reparto/mapa.py
- rutas_reparto/planificadores.py
- rutas_reparto/datos_externos.py
- rutas_reparto/graficas.py
- demo.py
- tests/test_rutas_reparto.py

FUNCIONALIDADES

1. Punto:
Representa un punto mediante identificador, nombre y coordenadas x e y. Debe disponer del método distancia_a(otro) y una representación __repr__ legible.

2. Ruta:
Representa una ruta mediante el nombre del planificador, una lista de paradas y su longitud. Debe disponer de una representación __repr__ legible.

3. MapaReparto:
- Guarda los puntos en un diccionario indexado por identificador.
- Precalcula una matriz de distancias como diccionario de diccionarios.
- Permite obtener el almacén.
- Permite obtener la lista de entregas ordenada alfabéticamente.
- Permite consultar la distancia entre dos identificadores.
- Permite calcular la longitud de una lista de paradas.

4. Planificadores:
- Debe existir una clase base Planificador con el método planificar(mapa) que devuelve una Ruta y un nombre.
- Debe haber tres planificadores: FuerzaBruta, VecinoMasCercano e InsercionMasBarata.
- MejoraDosOpt debe recibir otro planificador en su constructor mediante composición y mejorar la ruta obtenida.
- La demo debe poder recorrer una lista de planificadores sin tener que preguntar de qué tipo es cada uno.

5. Errores:
Debe existir una jerarquía de excepciones con una clase base y, como mínimo:
- FormatoInvalidoError
- CoordenadaInvalidaError
- PuntoDuplicadoError
- AlmacenNoEncontradoError
- ParametroInvalidoError

6. Carga de datos:
La función cargar_mapa_csv(ruta) debe devolver el mapa y las filas descartadas, indicando el número de cada fila.

7. Resultados:
- Mostrar una tabla comparativa utilizando tabulate.
- La tabla debe incluir planificador, longitud y porcentaje de diferencia respecto a la ruta óptima.
- Utilizar matplotlib para guardar comparativa_rutas.png.
- La figura debe incluir un mapa por planificador, mostrando su ruta y la ruta óptima de fondo, además de una gráfica de barras con el porcentaje de diferencia.

8. Pruebas:
El proyecto debe incluir al menos 12 pruebas con unittest.
El agente de pruebas debe diseñarlas basándose exclusivamente en este contrato, sin consultar el código de implementación.

9. Demo:
demo.py debe:
- Cargar el CSV.
- Informar de los puntos cargados y las filas descartadas.
- Ejecutar los planificadores en este orden:
  1. Fuerza bruta.
  2. Vecino más cercano.
  3. Inserción más barata.
  4. Vecino más cercano + 2-opt.
  5. Inserción más barata + 2-opt.
- Imprimir la tabla comparativa.
- Mostrar el orden de paradas de cada ruta.
- Guardar la figura comparativa.

NORMAS OBLIGATORIAS DE CÁLCULO

Estas reglas son obligatorias y deben quedar definidas expresamente en el contrato.

1. DISTANCIA
La distancia entre dos puntos es la distancia euclídea en línea recta. Se redondea a dos decimales.

2. LONGITUD DE RUTA
La longitud se calcula sumando las distancias de los tramos previamente redondeadas. El resultado total también se redondea a dos decimales.

3. FORMATO DE RUTA
Una ruta es una lista de identificadores que:
- Empieza y termina en ALM.
- Pasa exactamente una vez por cada punto de entrega.

4. DESEMPATES
Cuando haya que resolver un empate entre identificadores, se elige el identificador menor alfabéticamente (por ejemplo, P03 antes que P07).

5. FUERZA BRUTA
- Recorre los órdenes posibles comenzando por los puntos en orden alfabético.
- Solo sustituye la mejor ruta cuando encuentra otra estrictamente más corta.
- Admite como máximo 10 puntos de entrega.
- Si hay más de 10, lanza ParametroInvalidoError.
- Si dos rutas tienen la misma longitud, conserva la primera encontrada.

6. INSERCIÓN MÁS BARATA
- Comienza con la ruta ALM → punto de entrega más cercano al almacén → ALM.
- El coste de insertar un punto p entre a y b es:
  distancia(a,p) + distancia(p,b) - distancia(a,b).
- El coste se redondea a dos decimales.
- En cada paso se inserta el punto con menor coste.
- Si hay empate, se elige primero el identificador menor.
- Si persiste el empate, se elige la posición más cercana al principio de la ruta.

7. 2-OPT
- Realiza pasadas completas.
- Las posiciones i comienzan en la primera entrega y j > i avanza hasta la última entrega, siempre en orden creciente.
- Si invertir el tramo entre i y j produce una ruta estrictamente más corta, se aplica inmediatamente el cambio y se continúa la pasada.
- El algoritmo termina cuando completa una pasada sin aplicar ningún cambio.

CONTENIDO DEL CONTRATO

Quiero que contrato.md defina con precisión:

- La responsabilidad de cada módulo y de cada agente.
- Las clases y funciones que debe implementar cada agente.
- Los nombres exactos de clases, métodos y funciones.
- Los parámetros, sus tipos y los valores de retorno.
- Las excepciones que puede lanzar cada operación y en qué situaciones.
- Las estructuras de datos utilizadas.
- Las reglas de cálculo y redondeo.
- El comportamiento ante datos incorrectos y casos límite.
- Las interfaces que utilizarán los distintos módulos.
- Los criterios que deberán cumplir las pruebas.
- El orden de ejecución e integración de la demo.

El contrato debe ser suficientemente detallado para que los agentes puedan trabajar de forma independiente sin tener que inventar nombres, interfaces ni comportamientos.

No escribas código de implementación dentro del contrato.

Cuando termines, muéstrame un resumen de las decisiones principales y señala cualquier duda que necesite resolver antes de dar el contrato por válido.
```

- **Qué devolvió (resumen):** 
Redactó contrato.md, versión 1.0. Definió las interfaces, responsabilidades, excepciones, reglas de cálculo y pruebas. Inicialmente interpretó que cualquier identificador distinto de ALM podía ser una entrega, por lo que fue necesario solicitar una corrección.

- **¿Respeta el contrato?** Sí / No. Si no, qué incumple: No aplicable: era el encargo de creación del propio contrato.
- **Decisión:** aceptado / rechazado / aceptado con correcciones (encargo n.º ...) aceptado con correcciones

*(Copia el bloque para E2, E3...)*

### Encargo E2

- **Agente:** Orquestador
- **Sesión n.º:** 1
- **Prompt enviado:**

```
Hay una corrección antes de validar el contrato: el enunciado establece expresamente que los identificadores de entrega van de P01 a P09 y que ALM es el almacén. Por tanto, no debemos permitir cualquier identificador distinto de ALM como punto de entrega. Ajusta esa decisión en contrato.md y mantén el resto de decisiones de la versión 1.0 sin cambios, salvo que detectes alguna contradicción con el enunciado. No implementes código ni delegues tareas.
```

- **Qué devolvió (resumen):** 
Detectó que limitar los identificadores a P01–P09 impediría probar la excepción de fuerza bruta con más de 10 entregas. 
Propuso admitir P01–P99 en los mapas generales y mantener P01–P09 en el CSV de control.
- **¿Respeta el contrato?** Sí / No. Si no, qué incumple: Sí
- **Decisión:** aceptado / rechazado / aceptado con correcciones (encargo n.º ...) aceptado 

### Encargo E3

- **Agente:** Orquestador
- **Sesión n.º:** 1
- **Prompt enviado:**

```
Vamos a comenzar la fase 1 del proyecto.

Lee el archivo `contrato.md` y utiliza los subagentes `datos`, `algoritmos` y `pruebas` para desarrollar sus respectivos ficheros según las especificaciones del contrato.

Quiero que los tres subagentes trabajen en paralelo, cada uno en su propia sesión y respetando estrictamente sus responsabilidades y permisos:

- **datos:** únicamente sus ficheros asignados en el contrato.
- **algoritmos:** únicamente `planificadores.py`.
- **pruebas:** únicamente `tests/test_rutas_reparto.py`. Recuerda que este agente solo puede consultar el contrato y el enunciado, nunca el código del proyecto.

No modifiques tú los ficheros asignados a los subagentes ni escribas código por tu cuenta.

Cuando terminen, indícame:
1. Qué subagentes has lanzado y si han terminado.
2. Qué ficheros ha creado o modificado cada uno.
3. Si han respetado sus permisos y responsabilidades.
4. Un resumen de lo realizado y de cualquier problema encontrado.

No ejecutes todavía la demo ni las pruebas. Esa parte la haremos en la fase 2.```

- **Qué devolvió (resumen):** 
Lanzó los tres subagentes en paralelo y en sesiones independientes. 
Los tres terminaron correctamente. Se crearon los cinco módulos del agente Datos, 
rutas_reparto/planificadores.py del agente Algoritmos y tests/test_rutas_reparto.py del agente Pruebas. 
El orquestador comprobó mediante una revisión de solo lectura que los agentes respetaron sus responsabilidades. 
No ejecutó la demo ni las pruebas.


- **¿Respeta el contrato?** Sí / No. Si no, qué incumple: Sí
- **Decisión:** aceptado / rechazado / aceptado con correcciones (encargo n.º ...) aceptado 


### Encargo E4

- **Agente:** Datos
- **Sesión n.º:** 2
- **Prompt enviado:**

```
You are a subagent spawned by another session.
ROL: Agente 1 (datos) del proyecto «planificación de rutas de reparto».

CONTRATO QUE TE ENTREGO: el fichero `contrato.md` de la raíz del repositorio (versión 1.0, decisiones D1–D9). Léelo ÍNTEGRAMENTE antes de escribir nada; es la única fuente de verdad para nombres, firmas, estructuras, excepciones y reglas de cálculo. Si algo no está en el contrato, no lo inventes: indícalo en tu informe final.

TAREA: crear exactamente estos cinco ficheros, con las responsabilidades del apartado 1 del contrato:
1. `rutas_reparto/errores.py`
2. `rutas_reparto/punto.py`
3. `rutas_reparto/mapa.py`
4. `rutas_reparto/datos_externos.py`
5. `rutas_reparto/graficas.py`

LÍMITES ESTRICTOS:
- Escribe SOLO esos cinco ficheros.
- No modifiques ningún otro archivo del proyecto.
- Importa siempre desde módulos concretos, nunca desde la raíz del paquete.
- Respeta literalmente D9 y las reglas de redondeo del contrato.
- No ejecutes la demo ni las pruebas; no instales dependencias. El orquestador hará la integración en la fase 2.

FORMATO DE ENTREGA:
1. Lista de ficheros creados/modificados.
2. Resumen por fichero.
3. Confirmación de que no has escrito ningún otro fichero.
4. Dudas o contradicciones detectadas.```

- **Qué devolvió (resumen):** 
Creó los cinco módulos asignados. Implementó las excepciones, las clases Punto y Ruta, el mapa, la carga del CSV y las funciones de gráficas. 
Declaró haber respetado D9, las reglas de redondeo y sus límites de escritura. 
Indicó algunas decisiones no especificadas expresamente en el contrato.


- **¿Respeta el contrato?** Sí / No. Si no, qué incumple: Sí
- **Decisión:** aceptado / rechazado / aceptado con correcciones (encargo n.º ...) aceptado 


### Encargo E5

- **Agente:** Algoritmos
- **Sesión n.º:** 3
- **Prompt enviado:**

```
You are a subagent spawned by another session.
ROL: Agente 2 (algoritmos) del proyecto «planificación de rutas de reparto».

CONTRATO QUE TE ENTREGO: el fichero `contrato.md` de la raíz del repositorio (versión 1.0, decisiones D1–D9). Léelo ÍNTEGRAMENTE antes de escribir nada; es la única fuente de verdad para nombres, firmas, estructuras, excepciones y reglas de cálculo. No inventes nada que no figure en él; si detectas una laguna, indícala en tu informe final.

TAREA: crear ÚNICAMENTE `rutas_reparto/planificadores.py` con:
- `Planificador` (clase base, `nombre = ""` y `planificar(mapa)` que lanza `NotImplementedError`).
- `FuerzaBruta` (`nombre = "Fuerza bruta"`): permutaciones en orden alfabético, límite de 10 entregas con `ParametroInvalidoError`, sustitución solo si la longitud es estrictamente menor, conserva la primera en caso de empate.
- `VecinoMasCercano` (`nombre = "Vecino más cercano"`): elección por `(distancia, id)`.
- `InsercionMasBarata` (`nombre = "Inserción más barata"`): coste `round(dist(a,p)+dist(p,b)-dist(a,b), 2)`, clave `(coste, id, posición)`.
- `MejoraDosOpt` (D3): composición con otro `Planificador`, propiedad `nombre` = `f"{planificador.nombre} + 2-opt"`, pasadas completas, `i` y `j` crecientes sobre entregas, inversión inmediata si mejora estrictamente, terminación sin cambios.

LÍMITES ESTRICTOS:
- Escribe SOLO `rutas_reparto/planificadores.py`. No modifiques `contrato.md`, `rutas_reparto/__init__.py`, `demo.py`, `README.md`, ningún fichero del agente 1 (`errores.py`, `punto.py`, `mapa.py`, `datos_externos.py`, `graficas.py`) ni `tests/`.
- Importa desde módulos concretos (`rutas_reparto.punto`, `rutas_reparto.mapa`, `rutas_reparto.errores`), nunca desde la raíz del paquete.
- `planificar(mapa)` devuelve un único `Ruta` (D2), nunca una tupla. Usa `mapa.longitud(...)` para todas las longitudes y las distancias redondeadas de la matriz.
- Respeta D9: `ALM` es el almacén; los ids de entrega van de `P01` a `P99`.
- No ejecutes la demo ni las pruebas; no instales dependencias.

FORMATO DE ENTREGA (resumen, sin volcar el código completo):
1. Fichero creado/modificado.
2. Breve resumen de cada clase y de cómo se aplican desempates, redondeo y criterio estricto de mejora.
3. Confirmación explícita de que no has escrito ningún otro fichero.
4. Cualquier duda o posible contradicción detectada; si no hay, indica «sin incidencias».```

- **Qué devolvió (resumen):** 
Creó únicamente rutas_reparto/planificadores.py. 
Implementó la clase base Planificador y los cuatro planificadores: FuerzaBruta, VecinoMasCercano, InsercionMasBarata y MejoraDosOpt.

Respetó las reglas de desempate, redondeo y mejora estricta definidas en el contrato. 
Comprobó manualmente los casos T11 y T12 con las coordenadas de ejemplo y obtuvo los resultados esperados. 
Confirmó que no modificó otros ficheros ni ejecutó la demo o las pruebas.


- **¿Respeta el contrato?** Sí / No. Si no, qué incumple: Sí
- **Decisión:** aceptado / rechazado / aceptado con correcciones (encargo n.º ...) aceptado 

### Encargo E5

- **Agente:** Pruebas
- **Sesión n.º:** 4
- **Prompt enviado:**

```
You are a subagent spawned by another session. ROL: Agente 3 (pruebas) del proyecto «planificación de rutas de reparto».

CONTRATO QUE TE ENTREGO: el fichero `contrato.md` de la raíz del repositorio (versión 1.0, decisiones D1–D9). Léelo ÍNTEGRAMENTE; es tu única fuente de verdad junto con el enunciado que se reproduce abajo y el CSV `datos/puntos_reparto.csv`.

TAREA: crear ÚNICAMENTE `tests/test_rutas_reparto.py` con al menos 12 métodos `unittest.TestCase` (recomendado: los 15 casos T1–T15 del apartado 10 del contrato). Diseña las aserciones SOLO a partir del contrato y del enunciado: valores esperados, excepciones, mensajes, nombres y formatos.

LÍMITES CRÍTICOS DE LECTURA:
- Está PROHIBIDO abrir, leer, listar o importar el código de implementación: `rutas_reparto/errores.py`, `punto.py`, `mapa.py`, `datos_externos.py`, `graficas.py`, `planificadores.py`, ni `demo.py` ni `rutas_reparto/__init__.py`. Tampoco ejecutes las pruebas.
- Puedes leer `contrato.md`, el CSV `datos/puntos_reparto.csv` y el enunciado siguiente. El código importado en tiempo de ejecución por las pruebas no se inspecciona.
- Escribe SOLO `tests/test_rutas_reparto.py`. No modifiques ningún otro fichero, en particular los de los agentes 1 y 2 ni los del orquestador.

ENUNCIADO (resumen íntegro de requisitos):
- Planificar rutas de reparto desde un almacén `ALM` y puntos de entrega. CSV `datos/puntos_reparto.csv` con columnas `id,nombre,x,y`; coordenadas en 0–100; filas incorrectas (fuera de mapa, valores no numéricos, ids duplicados) se descartan informando su número de fila.
- Módulos: `errores.py`, `punto.py`, `mapa.py`, `planificadores.py`, `datos_externos.py`, `graficas.py`, `demo.py`, `tests/test_rutas_reparto.py`.
- Funcionalidades: `Punto` con `distancia_a` y `__repr__`; `Ruta` con nombre, paradas y longitud; `MapaReparto` con matriz de distancias, almacén, entregas ordenadas y longitud; `Planificador` y tres planificadores más `MejoraDosOpt` por composición; jerarquía de excepciones; `cargar_mapa_csv` que devuelve mapa y filas descartadas; tabla con `tabulate` y figura con matplotlib; al menos 12 pruebas; demo en el orden fuerza bruta, vecino, inserción, vecino+2-opt, inserción+2-opt.
- Normas obligatorias de cálculo: distancia euclídea redondeada a 2 decimales; longitud = suma de tramos previamente redondeados y total redondeado; ruta = `ALM` … `ALM` pasando una vez por cada entrega; desempate por id alfabéticamente menor; fuerza bruta recorre órdenes desde el orden alfabético, solo sustituye si es estrictamente más corta, máximo 10 entregas y conserva la primera en empate; inserción con coste `round(dist(a,p)+dist(p,b)-dist(a,b), 2)` y desempate por id y posición; 2-opt con pasadas completas, `i` y `j` crecientes, inversión inmediata si mejora estrictamente y fin cuando una pasada no cambia nada.
- D9: `ALM` es el almacén; entregas `P01`…`P99` (en el CSV de control `P01`…`P09`); cualquier otro id se rechaza con `FormatoInvalidoError`.

FORMATO DE ENTREGA (resumen, sin volcar el código completo):
1. Fichero creado.
2. Lista de los métodos de prueba con su nombre y qué comportamiento del contrato verifica.
3. Confirmación explícita de que no has leído ni modificado código de implementación ni ejecutado las pruebas.
4. Cualquier duda o contradicción detectada entre contrato y enunciado; si no hay, indica «sin incidencias».```

- **Qué devolvió (resumen):** 
Creó únicamente tests/test_rutas_reparto.py, con 34 métodos de prueba unittest.TestCase, superando el mínimo de 12 exigido. 
Cubrió puntos, rutas, mapas, carga del CSV, excepciones, los planificadores, 2-opt y las funciones de comparación y gráficas.

Confirmó que no leyó ni modificó el código de implementación y que no ejecutó las pruebas. 
No detectó contradicciones entre el contrato y el enunciado.

- **¿Respeta el contrato?** Sí / No. Si no, qué incumple: Sí
- **Decisión:** aceptado / rechazado / aceptado con correcciones (encargo n.º ...) aceptado 

## 5. Registro de integración

Una fila por cada fallo detectado al juntar el trabajo de los agentes o al ejecutar la demo y las pruebas.

| N.º | Iteración | Qué falló (mensaje de error o síntoma) | Causa | Agente responsable | Encargo de corrección | ¿Resuelto? |
|---|---|---|---|---|---|---|
| F1 | 1 | *Ej.: `ImportError: cannot import name 'Ruta'`* | *Ej.: el agente 1 la llamó `RutaReparto`, el contrato decía `Ruta`* | Agente 1 | E5 | Sí |
| | | | | | | |

## 6. Gestión de créditos

Anota cada vez que un modelo gratuito dejó de responder por límite de uso.

| Fecha y hora | Modelo | Agente | Qué estabas haciendo | Cómo continuaste (otro modelo gratuito, esperar, prompt de reanudación...) | Tiempo perdido aprox. |
|---|---|---|---|---|---|
| | | | | | |

## 7. Verificación final

### Datos de control

| Dato | Valor esperado (enunciado) | Valor obtenido | ¿Coincide? |
|---|---|---|---|
| Puntos cargados | | | |
| Filas descartadas | | | |
| Longitud: Fuerza bruta | | | |
| Longitud: Vecino más cercano | | | |
| Longitud: Inserción más barata | | | |
| Longitud: Vecino más cercano + 2-opt | | | |
| Longitud: Inserción más barata + 2-opt | | | |

### Pruebas

- Comando ejecutado:
- Número de pruebas y resultado (pega las últimas líneas de la salida):

```text

```

- ¿Alguna prueba del agente 3 encontró un error real en el código de los agentes 1 o 2? ¿Cuál?

## 8. Valoración de los agentes

Puntúa de 1 (muy mal) a 5 (muy bien). Esta tabla es la base de la parte del vídeo sobre qué agentes rindieron mejor.

| Criterio | Orquestador | Agente 1 | Agente 2 | Agente 3 |
|---|---|---|---|---|
| Respeto al contrato | | | | |
| Calidad del código o de las pruebas | | | | |
| Pocas correcciones necesarias | | | | |
| Claridad de sus explicaciones | | | | |
| Gestión del límite de uso gratuito | | | | |
| **Total** | | | | |

**Comentario sobre cada agente** (2 o 3 líneas cada uno):

## 9. Reflexión

1. ¿Qué parte del proceso costó más y por qué?
2. ¿Qué fallos de integración aparecieron y qué los provocó?
3. ¿Qué cambiarías del contrato o de los encargos si volvieras a empezar?
4. ¿Qué has aprendido sobre trabajar con varios agentes y modelos de IA que no sabías antes?
