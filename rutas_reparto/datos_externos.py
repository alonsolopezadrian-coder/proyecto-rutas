"""Carga de mapas de reparto desde ficheros CSV.

Aplica la precedencia de validación del contrato (apartado 3.2): número de
campos, ``id``/``nombre`` vacíos, formato del ``id`` (D9), conversión numérica,
rango y duplicado. De cada fila se registra solo el primer error encontrado.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

from rutas_reparto.errores import (
    AlmacenNoEncontradoError,
    CoordenadaInvalidaError,
    FormatoInvalidoError,
    PuntoDuplicadoError,
    RutasError,
)
from rutas_reparto.mapa import MapaReparto
from rutas_reparto.punto import Punto, _id_valido

_CABECERA_ESPERADA = ["id", "nombre", "x", "y"]
_MENSAJE_CABECERA = "El CSV debe tener exactamente las columnas id,nombre,x,y"
_MENSAJE_ID_INVALIDO = (
    "El identificador {id} no es válido; se espera ALM o P seguido de dos "
    "dígitos entre 01 y 99"
)


def _convertir_coordenada(campo: str, texto: str) -> float:
    """Convierte el texto de una coordenada; lanza ``FormatoInvalidoError``."""
    try:
        return float(texto)
    except (TypeError, ValueError):
        raise FormatoInvalidoError(
            f"La coordenada {campo} no es numérica: {texto!r}"
        ) from None


def _validar_rango(campo: str, valor: float, texto: str) -> None:
    """Comprueba que la coordenada es finita y está en ``[0, 100]``."""
    if not math.isfinite(valor) or valor < 0.0 or valor > 100.0:
        raise CoordenadaInvalidaError(
            f"La coordenada {campo}={texto} está fuera del intervalo [0, 100]"
        )


def _procesar_fila(fila: list[str], puntos: dict[str, Punto]) -> Punto:
    """Valida una fila y devuelve el ``Punto`` correspondiente."""
    if len(fila) != 4:
        raise FormatoInvalidoError(
            f"Se esperaban 4 columnas, se obtuvieron {len(fila)}"
        )

    id_texto, nombre, x_texto, y_texto = [campo.strip() for campo in fila]

    if not id_texto:
        raise FormatoInvalidoError("El campo id está vacío")
    if not nombre:
        raise FormatoInvalidoError("El campo nombre está vacío")
    if not _id_valido(id_texto):
        raise FormatoInvalidoError(
            _MENSAJE_ID_INVALIDO.format(id=repr(id_texto))
        )

    x = _convertir_coordenada("x", x_texto)
    y = _convertir_coordenada("y", y_texto)
    _validar_rango("x", x, x_texto)
    _validar_rango("y", y, y_texto)

    if id_texto in puntos:
        raise PuntoDuplicadoError(f"El identificador {id_texto!r} ya existe")

    return Punto(id_texto, nombre, x, y)


def cargar_mapa_csv(ruta: str | Path) -> tuple[MapaReparto, list[tuple[int, str]]]:
    """Carga un mapa desde un CSV y devuelve el mapa y las filas descartadas.

    El CSV debe tener la cabecera ``id,nombre,x,y``; la cabecera es la línea 1
    y la primera fila de datos la línea 2. Se admiten BOM y saltos CRLF.
    """
    with open(ruta, encoding="utf-8-sig", newline="") as fichero:
        lector = csv.reader(fichero)
        try:
            cabecera = next(lector)
        except StopIteration:
            raise FormatoInvalidoError(_MENSAJE_CABECERA) from None
        if cabecera != _CABECERA_ESPERADA:
            raise FormatoInvalidoError(_MENSAJE_CABECERA)

        puntos: dict[str, Punto] = {}
        descartes: list[tuple[int, str]] = []
        for numero_linea, fila in enumerate(lector, start=2):
            try:
                punto = _procesar_fila(fila, puntos)
            except RutasError as error:
                mensaje = f"{type(error).__name__}: {error}"
                descartes.append((numero_linea, mensaje))
            else:
                puntos[punto.id] = punto

    if "ALM" not in puntos:
        raise AlmacenNoEncontradoError(
            "El CSV no contiene ningún punto con identificador 'ALM'"
        )

    return MapaReparto(list(puntos.values())), sorted(descartes, key=lambda d: d[0])
