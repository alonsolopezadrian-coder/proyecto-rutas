"""Jerarquía de excepciones del proyecto de planificación de rutas.

Todas las excepciones propias del proyecto heredan de :class:`RutasError`,
que a su vez hereda de :class:`Exception`. Las clases derivadas no añaden
comportamiento: aceptan un mensaje de texto opcional y ``str(exc)`` devuelve
dicho mensaje. Un ``except RutasError`` captura cualquier error del proyecto.
"""


class RutasError(Exception):
    """Clase base de todos los errores propios del proyecto."""


class FormatoInvalidoError(RutasError):
    """Formato de dato inválido (cabecera, campos, identificador, tipo...)."""


class CoordenadaInvalidaError(RutasError):
    """Coordenada no finita o fuera del intervalo cerrado [0, 100]."""


class PuntoDuplicadoError(RutasError):
    """Identificador de punto repetido en una carga o en un mapa."""


class AlmacenNoEncontradoError(RutasError):
    """No existe ningún punto con el identificador de almacén ``ALM``."""


class ParametroInvalidoError(RutasError):
    """Argumento o combinación de argumentos no válidos para una operación."""
