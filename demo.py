# -*- coding: utf-8 -*-
"""Demostración del proyecto de planificación de rutas de reparto.

Sigue literalmente el orden de ejecución del apartado 9 del contrato:
carga del CSV, información de puntos y descartes, ejecución de los cinco
planificadores, tabla comparativa, orden de paradas y figura comparativa.
"""

from pathlib import Path

from rutas_reparto import (
    FuerzaBruta,
    InsercionMasBarata,
    MejoraDosOpt,
    VecinoMasCercano,
    calcular_diferencia,
    cargar_mapa_csv,
    formatear_tabla,
    guardar_comparativa,
)

RUTA_CSV = Path(__file__).resolve().parent / "datos" / "puntos_reparto.csv"
ARCHIVO_FIGURA = "comparativa_rutas.png"


def main() -> None:
    """Ejecuta la demo completa y muestra los resultados por pantalla."""
    mapa, descartes = cargar_mapa_csv(RUTA_CSV)

    print(f"Puntos cargados: {len(mapa.puntos)}")
    for id_punto in sorted(mapa.puntos):
        punto = mapa.puntos[id_punto]
        print(f"  {punto.id}: {punto.nombre} ({punto.x:.2f}, {punto.y:.2f})")

    print(f"Filas descartadas: {len(descartes)}")
    for numero_fila, mensaje in descartes:
        print(f"  Fila {numero_fila}: {mensaje}")

    planificadores = [
        FuerzaBruta(),
        VecinoMasCercano(),
        InsercionMasBarata(),
        MejoraDosOpt(VecinoMasCercano()),
        MejoraDosOpt(InsercionMasBarata()),
    ]

    rutas = [planificador.planificar(mapa) for planificador in planificadores]
    ruta_optima = rutas[0]
    diferencias = [
        calcular_diferencia(ruta.longitud, ruta_optima.longitud) for ruta in rutas
    ]

    filas_tabla = [
        (ruta.nombre, ruta.longitud, diferencia)
        for ruta, diferencia in zip(rutas, diferencias)
    ]
    print(formatear_tabla(filas_tabla))

    print("Orden de paradas:")
    for ruta in rutas:
        print(f"  {ruta.nombre}: {' -> '.join(ruta.paradas)}")

    archivo = guardar_comparativa(
        rutas, diferencias, ruta_optima, mapa, ARCHIVO_FIGURA
    )
    print(f"Figura guardada en: {archivo}")


if __name__ == "__main__":
    main()
