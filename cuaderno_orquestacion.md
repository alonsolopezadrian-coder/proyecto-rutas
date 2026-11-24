# Cuaderno de orquestación

> Plantilla del ejercicio práctico 3 (sección 2.14). Copia este fichero en la raíz de tu repositorio, rellénalo **a medida que trabajas** (no al final) y súbelo junto con el código. Borra los textos de ejemplo en cursiva.

## 1. Ficha

| Campo | Contenido |
|---|---|
| Nombre y apellidos | Adrián Alonso López |
| Repositorio (URL) | |
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
| 1.0 | | Versión inicial | Orquestador | |
| | | | | |

## 3. Registro de sesiones

Una fila por cada sesión de OpenCode: las sesiones principales con el orquestador y las sesiones hijas de cada subagente (incluidas las de reanudación).

| N.º | Fecha y hora | Agente | Motivo (encargo inicial, corrección, reanudación...) | ¿Respetó qué ficheros podía leer? | Captura o exportación de la sesión |
|---|---|---|---|---|---|
| 1 | | Orquestador | Redactar el contrato | — | |
| | | | | |

## 4. Registro de encargos

Una entrada por cada encargo a un agente: tus instrucciones al orquestador y los encargos que el orquestador pasa a cada subagente (los ves en su sesión hija). Copia el texto **completo**.

### Encargo E1

- **Agente:**
- **Sesión n.º:**
- **Prompt enviado:**

```text
(pega aquí el prompt completo)
```

- **Qué devolvió (resumen):**
- **¿Respeta el contrato?** Sí / No. Si no, qué incumple:
- **Decisión:** aceptado / rechazado / aceptado con correcciones (encargo n.º ...)

*(Copia el bloque para E2, E3...)*

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
