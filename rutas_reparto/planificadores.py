"""Planificadores de rutas de reparto.

Implementa los algoritmos definidos en el contrato v1.0 (apartado 6):
:class:`Planificador`, :class:`FuerzaBruta`, :class:`VecinoMasCercano`,
:class:`InsercionMasBarata` y :class:`MejoraDosOpt`.

Todos devuelven un único :class:`Ruta` y son intercambiables sin usar
``isinstance``, ``type`` ni ramas por tipo. Depende solo de
:mod:`rutas_reparto.punto`, :mod:`rutas_reparto.mapa` y
:mod:`rutas_reparto.errores`.
"""

from itertools import permutations

from rutas_reparto.errores import ParametroInvalidoError
from rutas_reparto.mapa import MapaReparto
from rutas_reparto.punto import Ruta


class Planificador:
    """Clase base de los planificadores de rutas."""

    nombre = ""

    def planificar(self, mapa: MapaReparto) -> Ruta:
        """Devuelve la ruta óptima para ``mapa`` (por implementar en subclases)."""
        raise NotImplementedError("Este planificador no implementa planificar")


class FuerzaBruta(Planificador):
    """Fuerza bruta: evalúa todas las permutaciones y se queda con la más corta."""

    nombre = "Fuerza bruta"

    def planificar(self, mapa: MapaReparto) -> Ruta:
        entregas = mapa.obtener_entregas()
        if len(entregas) > 10:
            raise ParametroInvalidoError(
                "Fuerza bruta soporta como máximo 10 entregas"
            )
        if not entregas:
            return Ruta(self.nombre, ["ALM", "ALM"], 0.0)

        mejor_paradas = None
        mejor_longitud = float("inf")
        for permutacion in permutations(entregas):
            paradas = ["ALM", *permutacion, "ALM"]
            longitud = mapa.longitud(paradas)
            if longitud < mejor_longitud:
                mejor_longitud = longitud
                mejor_paradas = paradas

        return Ruta(self.nombre, mejor_paradas, mejor_longitud)


class VecinoMasCercano(Planificador):
    """Vecino más cercano: va siempre a la entrega más próxima (desempate por id)."""

    nombre = "Vecino más cercano"

    def planificar(self, mapa: MapaReparto) -> Ruta:
        entregas = mapa.obtener_entregas()
        if not entregas:
            return Ruta(self.nombre, ["ALM", "ALM"], 0.0)

        paradas = ["ALM"]
        actual = "ALM"
        pendientes = list(entregas)
        while pendientes:
            siguiente = min(
                pendientes, key=lambda e: (mapa.distancia(actual, e), e)
            )
            paradas.append(siguiente)
            pendientes.remove(siguiente)
            actual = siguiente
        paradas.append("ALM")

        return Ruta(self.nombre, paradas, mapa.longitud(paradas))


class InsercionMasBarata(Planificador):
    """Inserción más barata: inserta cada entrega en la posición de menor coste."""

    nombre = "Inserción más barata"

    def planificar(self, mapa: MapaReparto) -> Ruta:
        entregas = mapa.obtener_entregas()
        if not entregas:
            return Ruta(self.nombre, ["ALM", "ALM"], 0.0)

        primero = min(
            entregas, key=lambda e: (mapa.distancia("ALM", e), e)
        )
        paradas = ["ALM", primero, "ALM"]
        pendientes = [e for e in entregas if e != primero]

        while pendientes:
            mejor_clave = None
            mejor_p = None
            mejor_pos = None
            for p in pendientes:
                for pos in range(1, len(paradas)):
                    a = paradas[pos - 1]
                    b = paradas[pos]
                    coste = round(
                        mapa.distancia(a, p)
                        + mapa.distancia(p, b)
                        - mapa.distancia(a, b),
                        2,
                    )
                    clave = (coste, p, pos)
                    if mejor_clave is None or clave < mejor_clave:
                        mejor_clave = clave
                        mejor_p = p
                        mejor_pos = pos
            paradas.insert(mejor_pos, mejor_p)
            pendientes.remove(mejor_p)

        return Ruta(self.nombre, paradas, mapa.longitud(paradas))


class MejoraDosOpt(Planificador):
    """2-opt por composición sobre otro :class:`Planificador` (contrato D3)."""

    def __init__(self, planificador: Planificador):
        if not isinstance(planificador, Planificador):
            raise ParametroInvalidoError(
                "MejoraDosOpt requiere un planificador de tipo Planificador"
            )
        self.planificador = planificador

    @property
    def nombre(self) -> str:
        return f"{self.planificador.nombre} + 2-opt"

    def planificar(self, mapa: MapaReparto) -> Ruta:
        ruta_inicial = self.planificador.planificar(mapa)
        paradas = list(ruta_inicial.paradas)
        longitud = ruta_inicial.longitud

        if len(paradas) - 2 < 2:
            return Ruta(self.nombre, paradas, longitud)

        cambiado = True
        while cambiado:
            cambiado = False
            n = len(paradas)
            for i in range(1, n - 2):
                for j in range(i + 1, n - 1):
                    candidata = (
                        paradas[:i]
                        + list(reversed(paradas[i:j + 1]))
                        + paradas[j + 1:]
                    )
                    longitud_candidata = mapa.longitud(candidata)
                    if longitud_candidata < longitud:
                        paradas = candidata
                        longitud = longitud_candidata
                        cambiado = True

        return Ruta(self.nombre, paradas, longitud)
