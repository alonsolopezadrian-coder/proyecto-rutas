"""Modelo de datos: ``Punto`` y ``Ruta`` (decisión D1 del contrato).

Este módulo depende únicamente de ``rutas_reparto.errores``.
"""

from __future__ import annotations

import math
import re
from typing import Any, Sequence

from rutas_reparto.errores import (
    CoordenadaInvalidaError,
    FormatoInvalidoError,
    ParametroInvalidoError,
)

# ``ALM`` es el único almacén; las entregas son ``P`` + dos dígitos, de 01 a 99.
_PATRON_ID = re.compile(r"ALM|P(?:0[1-9]|[1-9][0-9])")


def _id_valido(valor: object) -> bool:
    """Devuelve ``True`` si ``valor`` es un id admitido por D9."""
    return isinstance(valor, str) and _PATRON_ID.fullmatch(valor) is not None


def _validar_coordenada(valor: Any, nombre_campo: str) -> float:
    """Convierte y valida una coordenada de un :class:`Punto`."""
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise FormatoInvalidoError(
            f"La coordenada {nombre_campo} debe ser numérica: {valor!r}"
        )
    numero = float(valor)
    if not math.isfinite(numero) or not 0.0 <= numero <= 100.0:
        raise CoordenadaInvalidaError(
            f"La coordenada {nombre_campo}={valor} está fuera del intervalo [0, 100]"
        )
    return numero


class Punto:
    """Punto geográfico del reparto: almacén (``ALM``) o entrega (``Pnn``)."""

    def __init__(self, id: str, nombre: str, x: float, y: float) -> None:
        if not isinstance(id, str) or not id.strip():
            raise FormatoInvalidoError("El identificador no puede estar vacío")
        identificador = id.strip()
        if not _id_valido(identificador):
            raise FormatoInvalidoError(
                f"El identificador {identificador!r} no es válido; se espera ALM "
                "o P seguido de dos dígitos entre 01 y 99"
            )
        if not isinstance(nombre, str) or not nombre.strip():
            raise FormatoInvalidoError("El nombre no puede estar vacío")

        self.id = identificador
        self.nombre = nombre
        self.x = _validar_coordenada(x, "x")
        self.y = _validar_coordenada(y, "y")

    def distancia_a(self, otro: Punto) -> float:
        """Distancia euclídea a ``otro``, redondeada a 2 decimales."""
        if not isinstance(otro, Punto):
            raise ParametroInvalidoError(
                "El argumento de distancia_a debe ser una instancia de Punto"
            )
        diferencia_x = self.x - otro.x
        diferencia_y = self.y - otro.y
        distancia = math.sqrt(diferencia_x * diferencia_x + diferencia_y * diferencia_y)
        return round(distancia, 2)

    def __repr__(self) -> str:
        return (
            f"Punto(id={self.id!r}, nombre={self.nombre!r}, "
            f"x={self.x!r}, y={self.y!r})"
        )

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Punto):
            return False
        return (
            self.id == otro.id
            and self.nombre == otro.nombre
            and self.x == otro.x
            and self.y == otro.y
        )

    def __hash__(self) -> int:
        return hash((self.id, self.nombre, self.x, self.y))


class Ruta:
    """Ruta cerrada que empieza y termina en ``ALM``."""

    def __init__(self, nombre: str, paradas: Sequence[str], longitud: float) -> None:
        if not isinstance(nombre, str) or not nombre.strip():
            raise ParametroInvalidoError("El nombre de la ruta no puede estar vacío")

        if isinstance(paradas, (str, bytes)):
            raise ParametroInvalidoError(
                "Las paradas deben ser una secuencia de identificadores, no una cadena"
            )
        try:
            lista_paradas = list(paradas)
        except TypeError:
            raise ParametroInvalidoError(
                "Las paradas deben ser una secuencia de identificadores"
            ) from None

        if len(lista_paradas) < 2:
            raise ParametroInvalidoError("La ruta debe tener al menos dos paradas")
        if any(not isinstance(parada, str) for parada in lista_paradas):
            raise ParametroInvalidoError(
                "Todas las paradas deben ser identificadores de texto"
            )
        if lista_paradas[0] != "ALM" or lista_paradas[-1] != "ALM":
            raise ParametroInvalidoError(
                "La ruta debe empezar y terminar en 'ALM'"
            )

        entregas = lista_paradas[1:-1]
        if len(set(entregas)) != len(entregas):
            raise ParametroInvalidoError(
                "Una entrega no puede aparecer dos veces en la misma ruta"
            )
        for entrega in entregas:
            if entrega == "ALM" or not _id_valido(entrega):
                raise ParametroInvalidoError(
                    f"El identificador {entrega!r} no es una entrega válida; "
                    "se espera P seguido de dos dígitos entre 01 y 99"
                )

        if isinstance(longitud, bool) or not isinstance(longitud, (int, float)):
            raise ParametroInvalidoError("La longitud de la ruta debe ser numérica")
        valor_longitud = float(longitud)
        if not math.isfinite(valor_longitud) or valor_longitud < 0.0:
            raise ParametroInvalidoError(
                "La longitud de la ruta debe ser finita y no negativa"
            )

        self.nombre = nombre
        self.paradas = lista_paradas
        self.longitud = float(round(valor_longitud, 2))

    def __repr__(self) -> str:
        return (
            f"Ruta(nombre={self.nombre!r}, paradas={self.paradas!r}, "
            f"longitud={self.longitud!r})"
        )

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Ruta):
            return False
        return (
            self.nombre == otro.nombre
            and self.paradas == otro.paradas
            and self.longitud == otro.longitud
        )
