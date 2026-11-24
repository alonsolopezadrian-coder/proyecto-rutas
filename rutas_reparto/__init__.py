"""API pública del paquete ``rutas_reparto`` (contrato v1.0, apartado 2).

Se reexportan únicamente los nombres definidos en el contrato. Los módulos
internos continúan importando desde módulos concretos para evitar ciclos.
"""

from rutas_reparto.errores import (
    AlmacenNoEncontradoError,
    CoordenadaInvalidaError,
    FormatoInvalidoError,
    ParametroInvalidoError,
    PuntoDuplicadoError,
    RutasError,
)
from rutas_reparto.punto import Punto, Ruta
from rutas_reparto.mapa import MapaReparto
from rutas_reparto.planificadores import (
    FuerzaBruta,
    InsercionMasBarata,
    MejoraDosOpt,
    Planificador,
    VecinoMasCercano,
)
from rutas_reparto.datos_externos import cargar_mapa_csv
from rutas_reparto.graficas import (
    calcular_diferencia,
    formatear_tabla,
    guardar_comparativa,
)

__all__ = [
    "AlmacenNoEncontradoError",
    "CoordenadaInvalidaError",
    "FormatoInvalidoError",
    "ParametroInvalidoError",
    "PuntoDuplicadoError",
    "RutasError",
    "Punto",
    "Ruta",
    "MapaReparto",
    "Planificador",
    "FuerzaBruta",
    "VecinoMasCercano",
    "InsercionMasBarata",
    "MejoraDosOpt",
    "cargar_mapa_csv",
    "calcular_diferencia",
    "formatear_tabla",
    "guardar_comparativa",
]
