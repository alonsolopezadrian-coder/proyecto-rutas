"""Mapa de reparto: puntos, matriz de distancias precalculada y consultas."""

from __future__ import annotations

from typing import Iterable, Sequence

from rutas_reparto.errores import (
    AlmacenNoEncontradoError,
    ParametroInvalidoError,
    PuntoDuplicadoError,
)
from rutas_reparto.punto import Punto


class MapaReparto:
    """Conjunto de puntos indexados por id con su matriz de distancias."""

    def __init__(self, puntos: Iterable[Punto]) -> None:
        self.puntos: dict[str, Punto] = {}
        for punto in puntos:
            if not isinstance(punto, Punto):
                raise ParametroInvalidoError(
                    "Todos los elementos de un MapaReparto deben ser Punto"
                )
            if punto.id in self.puntos:
                raise PuntoDuplicadoError(
                    f"El identificador {punto.id!r} ya existe en el mapa"
                )
            self.puntos[punto.id] = punto

        self.distancias: dict[str, dict[str, float]] = {}
        for id_a, punto_a in self.puntos.items():
            fila: dict[str, float] = {}
            for id_b, punto_b in self.puntos.items():
                if id_a == id_b:
                    fila[id_b] = 0.0
                else:
                    fila[id_b] = punto_a.distancia_a(punto_b)
            self.distancias[id_a] = fila

    def obtener_almacen(self) -> Punto:
        """Devuelve el punto ``ALM`` o lanza ``AlmacenNoEncontradoError``."""
        if "ALM" not in self.puntos:
            raise AlmacenNoEncontradoError(
                "El mapa no contiene ningún punto con identificador 'ALM'"
            )
        return self.puntos["ALM"]

    def obtener_entregas(self) -> list[str]:
        """Ids de entrega (``Pnn``) ordenados alfabéticamente."""
        return sorted(id_punto for id_punto in self.puntos if id_punto != "ALM")

    def distancia(self, id_a: str, id_b: str) -> float:
        """Distancia ya redondeada entre dos puntos del mapa."""
        if id_a not in self.distancias or id_b not in self.distancias:
            raise ParametroInvalidoError(
                f"Alguno de los identificadores {id_a!r} / {id_b!r} no existe en el mapa"
            )
        return self.distancias[id_a][id_b]

    def longitud(self, paradas: Sequence[str]) -> float:
        """Longitud de una secuencia de paradas, sumando tramos redondeados."""
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
            raise ParametroInvalidoError(
                "Para calcular una longitud se necesitan al menos dos paradas"
            )

        total = 0.0
        for origen, destino in zip(lista_paradas, lista_paradas[1:]):
            total += self.distancia(origen, destino)
        return round(total, 2)
