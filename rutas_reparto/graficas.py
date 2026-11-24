"""Cálculo de diferencias, tabla comparativa y figura de rutas.

La generación de la figura usa el backend no interactivo ``Agg`` y nunca llama
a ``plt.show()``, de modo que funciona en entornos sin pantalla.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Sequence

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402  (debe ir tras seleccionar Agg)
from tabulate import tabulate  # noqa: E402

from rutas_reparto.errores import ParametroInvalidoError  # noqa: E402
from rutas_reparto.mapa import MapaReparto  # noqa: E402
from rutas_reparto.punto import Ruta  # noqa: E402

_CABECERAS_TABLA = ["Planificador", "Longitud", "Diferencia (%)"]


def _validar_longitud(valor: Any, nombre: str) -> float:
    """Convierte a ``float`` una longitud válida (finita y no negativa)."""
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ParametroInvalidoError(f"El valor {nombre} debe ser numérico")
    numero = float(valor)
    if not math.isfinite(numero) or numero < 0.0:
        raise ParametroInvalidoError(
            f"El valor {nombre} debe ser finito y no negativo"
        )
    return numero


def calcular_diferencia(longitud: float, longitud_optima: float) -> float:
    """Porcentaje con signo respecto de la longitud óptima (regla 5.7)."""
    valor = _validar_longitud(longitud, "longitud")
    optima = _validar_longitud(longitud_optima, "longitud_optima")
    if optima == 0.0:
        return 0.0
    return round((valor - optima) / optima * 100.0, 2)


def formatear_tabla(filas: Sequence[tuple[str, float, float]]) -> str:
    """Devuelve la tabla ``tabulate`` en formato grid con dos decimales."""
    cuerpo = [
        [nombre, f"{longitud:.2f}", f"{porcentaje:.2f}"]
        for nombre, longitud, porcentaje in filas
    ]
    return tabulate(
        cuerpo,
        headers=_CABECERAS_TABLA,
        tablefmt="grid",
        disable_numparse=True,
    )


def _coordenadas(paradas: Sequence[str], mapa: MapaReparto) -> tuple[list[float], list[float]]:
    """Convierte una secuencia de ids en listas de coordenadas x e y."""
    xs = [mapa.puntos[parada].x for parada in paradas]
    ys = [mapa.puntos[parada].y for parada in paradas]
    return xs, ys


def _dibujar_ruta(
    eje: Any,
    ruta: Ruta,
    mapa: MapaReparto,
    optima_x: list[float],
    optima_y: list[float],
) -> None:
    """Dibuja en ``eje`` los puntos, la ruta óptima y la ruta del planificador."""
    entregas = [id_punto for id_punto in mapa.puntos if id_punto != "ALM"]
    eje.scatter(
        [mapa.puntos[id_punto].x for id_punto in entregas],
        [mapa.puntos[id_punto].y for id_punto in entregas],
        color="#1f77b4",
        marker="o",
        s=40,
        label="Entregas",
        zorder=3,
    )

    almacen = mapa.obtener_almacen()
    eje.scatter(
        [almacen.x],
        [almacen.y],
        color="#d62728",
        marker="s",
        s=90,
        label="Almacén",
        zorder=4,
    )

    eje.plot(
        optima_x,
        optima_y,
        linestyle="--",
        color="#7f7f7f",
        linewidth=1.5,
        label="Óptima",
        zorder=2,
    )

    ruta_x, ruta_y = _coordenadas(ruta.paradas, mapa)
    eje.plot(
        ruta_x,
        ruta_y,
        linestyle="-",
        marker="o",
        color="#2ca02c",
        label=ruta.nombre,
        zorder=5,
    )

    eje.set_title(ruta.nombre)
    eje.set_aspect("equal", adjustable="datalim")
    eje.grid(True, alpha=0.3)
    eje.legend(fontsize="small")


def _dibujar_barras(
    eje: Any, rutas: Sequence[Ruta], diferencias: Sequence[float]
) -> None:
    """Dibuja el gráfico de barras con la diferencia de cada planificador."""
    posiciones = list(range(len(rutas)))
    eje.bar(posiciones, diferencias, color="#4c72b0")
    eje.axhline(0.0, color="#333333", linewidth=1.0)

    eje.set_xticks(posiciones)
    eje.set_xticklabels(
        [ruta.nombre for ruta in rutas], rotation=30, ha="right"
    )
    eje.set_ylabel("Diferencia (%)")
    eje.set_title("Comparativa de planificadores")
    eje.grid(True, axis="y", alpha=0.3)

    for posicion, diferencia in zip(posiciones, diferencias):
        eje.annotate(
            f"{diferencia:.2f}",
            (posicion, diferencia),
            textcoords="offset points",
            xytext=(0, 4),
            ha="center",
            fontsize="small",
        )


def guardar_comparativa(
    rutas: Sequence[Ruta],
    diferencias: Sequence[float],
    ruta_optima: Ruta,
    mapa: MapaReparto,
    archivo: str | Path = "comparativa_rutas.png",
) -> Path:
    """Genera la figura comparativa, la guarda y devuelve su ruta."""
    lista_rutas = list(rutas)
    lista_diferencias = list(diferencias)
    if len(lista_rutas) != len(lista_diferencias):
        raise ParametroInvalidoError(
            "Las listas de rutas y de diferencias deben tener la misma longitud"
        )

    total_ejes = len(lista_rutas) + 1
    columnas = 3
    filas = math.ceil(total_ejes / columnas)

    figura, ejes = plt.subplots(
        filas, columnas, figsize=(15, 4 * filas), squeeze=False
    )
    ejes_planos = ejes.reshape(-1)

    optima_x, optima_y = _coordenadas(ruta_optima.paradas, mapa)
    for indice, ruta in enumerate(lista_rutas):
        _dibujar_ruta(ejes_planos[indice], ruta, mapa, optima_x, optima_y)

    _dibujar_barras(ejes_planos[len(lista_rutas)], lista_rutas, lista_diferencias)

    for eje_sobrante in ejes_planos[total_ejes:]:
        eje_sobrante.set_visible(False)

    figura.savefig(archivo, dpi=150, bbox_inches="tight")
    plt.close(figura)
    return Path(archivo)
