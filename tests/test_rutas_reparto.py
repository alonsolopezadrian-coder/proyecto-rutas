# -*- coding: utf-8 -*-
"""Pruebas unitarias de «planificación de rutas de reparto».

Diseñadas EXCLUSIVAMENTE a partir de `contrato.md` (v1.0, decisiones D1-D9)
y del CSV `datos/puntos_reparto.csv`. No se ha consultado ningún fichero de
implementación. Comando de ejecución:

    python -m unittest discover -s tests -v

Cobertura: casos T1-T15 del apartado 10 del contrato (más T16 sobre
2-opt), casos límite del apartado 12 y la jerarquía de excepciones del
apartado 3.
"""

import tempfile
import unittest
from pathlib import Path

from rutas_reparto import (
    AlmacenNoEncontradoError,
    CoordenadaInvalidaError,
    FuerzaBruta,
    FormatoInvalidoError,
    InsercionMasBarata,
    MapaReparto,
    MejoraDosOpt,
    ParametroInvalidoError,
    Planificador,
    Punto,
    PuntoDuplicadoError,
    Ruta,
    RutasError,
    VecinoMasCercano,
    calcular_diferencia,
    cargar_mapa_csv,
    formatear_tabla,
    guardar_comparativa,
)

RUTA_CSV_CONTROL = (
    Path(__file__).resolve().parent.parent / "datos" / "puntos_reparto.csv"
)


def punto(id_, nombre, x, y):
    """Fábrica corta de Punto (helper; no es una prueba)."""
    return Punto(id_, nombre, x, y)


def mapa_ejemplo():
    """Mapa sintético: ALM(0,0), P01(3,4), P02(0,10)."""
    return MapaReparto([
        punto("ALM", "Almacén", 0, 0),
        punto("P01", "Entrega 1", 3, 4),
        punto("P02", "Entrega 2", 0, 10),
    ])


def mapa_cruces():
    """ALM(0,0), P01(10,0), P02(0,10), P03(10,10): cruces de distancias."""
    return MapaReparto([
        punto("ALM", "Almacén", 0, 0),
        punto("P01", "Uno", 10, 0),
        punto("P02", "Dos", 0, 10),
        punto("P03", "Tres", 10, 10),
    ])


class _StubPlanificador(Planificador):
    """Stub definido en el propio fichero de pruebas (apartado 10)."""

    nombre = "Stub"

    def __init__(self, paradas):
        self.paradas_fijas = list(paradas)

    def planificar(self, mapa):
        return Ruta(
            self.nombre, list(self.paradas_fijas), mapa.longitud(self.paradas_fijas)
        )


class TestPunto(unittest.TestCase):
    """T1, T2 y propiedades de Punto (apartados 4.1, 5.1)."""

    def test_T01_distancia_a_euclidea_redondeada(self):
        # T1: (0,0)-(3,4) -> 5.0 y un caso con redondeo a 2 decimales.
        alm = punto("ALM", "Almacén", 0, 0)
        p01 = punto("P01", "Entrega 1", 3, 4)
        p02 = punto("P02", "Entrega 2", 1, 1)
        self.assertEqual(
            alm.distancia_a(p01), 5.0,
            "La distancia euclídea (0,0)-(3,4) debe ser exactamente 5.0",
        )
        self.assertEqual(
            alm.distancia_a(p02), 1.41,
            "sqrt(2) debe redondearse a 1.41 con round(..., 2)",
        )
        self.assertEqual(
            p01.distancia_a(alm), 5.0, "La distancia debe ser simétrica"
        )

    def test_T02_punto_valida_id_coordenadas(self):
        # T2: fuera de rango -> CoordenadaInvalidaError; no numérico o id
        # D9 inválido -> FormatoInvalidoError.
        casos_rango = [
            ("x mayor que 100", 105, 50),
            ("y negativa", 50, -5),
        ]
        for etiqueta, x, y in casos_rango:
            with self.subTest(caso=etiqueta):
                with self.assertRaises(CoordenadaInvalidaError):
                    punto("P01", "Uno", x, y)
        with self.assertRaises(CoordenadaInvalidaError):
            punto("P01", "Uno", float("nan"), 50)
        with self.assertRaises(CoordenadaInvalidaError):
            punto("P01", "Uno", 50, float("inf"))
        with self.assertRaises(FormatoInvalidoError):
            punto("P01", "Uno", "abc", 50)
        with self.assertRaises(FormatoInvalidoError):
            punto("P01", "Uno", True, 50)  # bool no es numérico aceptado
        for id_invalido in ("X01", "P00", "P1", "P001", "pedido1", ""):
            with self.subTest(id=id_invalido):
                with self.assertRaises(FormatoInvalidoError):
                    punto(id_invalido, "Uno", 10, 10)
        with self.assertRaises(FormatoInvalidoError):
            punto("P01", "", 10, 10)
        # Límites del intervalo cerrado [0, 100] y ids D9 válidos: sin error.
        valido = punto("P99", "Última", 100, 0)
        self.assertEqual(valido.x, 100.0, "La coordenada 100 debe ser válida")

    def test_punto_repr_exacto(self):
        p = Punto("ALM", "Almacén do Tambre", 50, 50)
        self.assertEqual(
            repr(p),
            "Punto(id='ALM', nombre='Almacén do Tambre', x=50.0, y=50.0)",
            "repr debe ser exactamente Punto(id=..., nombre=..., x=..., y=...)",
        )

    def test_punto_igualdad_y_hash(self):
        a = Punto("P01", "Uno", 10, 20)
        b = Punto("P01", "Uno", 10, 20)
        c = Punto("P01", "Otro", 10, 20)
        self.assertEqual(a, b, "Mismos id, nombre, x e y deben ser iguales")
        self.assertNotEqual(a, c, "Nombres distintos deben dar desigualdad")
        self.assertNotEqual(a, "P01", "Un Punto no debe igualar a otra cosa")
        self.assertEqual(
            len({a, b, c}), 2, "__hash__ debe ser coherente con los 4 atributos"
        )


class TestRuta(unittest.TestCase):
    """T3 y propiedades de Ruta (apartado 4.2, regla 5.3)."""

    def test_T03_ruta_rechaza_paradas_invalidas(self):
        # T3: no empezar/terminar en ALM y entregas repetidas -> error.
        casos_invalidos = [
            (["P01", "ALM"], "no empieza en ALM"),
            (["ALM", "P01"], "no termina en ALM"),
            (["ALM", "P01", "P01", "ALM"], "entrega repetida"),
            (["ALM", "ALM", "ALM"], "ALM intermedio no es una entrega"),
            (["ALM"], "menos de dos paradas"),
            (["ALM", "X01", "ALM"], "id de entrega no permitido por D9"),
        ]
        for paradas, etiqueta in casos_invalidos:
            with self.subTest(caso=etiqueta):
                with self.assertRaises(ParametroInvalidoError):
                    Ruta("Ruta inválida", paradas, 10.0)
        with self.assertRaises(ParametroInvalidoError):
            Ruta("", ["ALM", "ALM"], 0.0)
        with self.assertRaises(ParametroInvalidoError):
            Ruta("Con negativa", ["ALM", "ALM"], -1.0)
        with self.assertRaises(ParametroInvalidoError):
            Ruta("Con infinita", ["ALM", "ALM"], float("inf"))

    def test_T03_repr_contiene_nombre_paradas_y_longitud(self):
        r = Ruta("Fuerza bruta", ["ALM", "P01", "ALM"], 99.3)
        self.assertEqual(
            repr(r),
            "Ruta(nombre='Fuerza bruta', paradas=['ALM', 'P01', 'ALM'], "
            "longitud=99.3)",
            "repr debe reproducir nombre, paradas y longitud con repr de atributos",
        )

    def test_ruta_guarda_copia_de_paradas(self):
        original = ["ALM", "P01", "ALM"]
        r = Ruta("Fuerza bruta", original, 99.3)
        original.append("P02")
        self.assertEqual(
            r.paradas, ["ALM", "P01", "ALM"],
            "paradas debe guardarse como list[str] nueva (copia)",
        )

    def test_ruta_igualdad(self):
        r = Ruta("Fuerza bruta", ["ALM", "P01", "ALM"], 99.3)
        self.assertEqual(
            r, Ruta("Fuerza bruta", ["ALM", "P01", "ALM"], 99.3),
            "__eq__ debe comparar nombre, paradas y longitud",
        )
        self.assertNotEqual(r, Ruta("Otra", ["ALM", "P01", "ALM"], 99.3))
        self.assertNotEqual(r, Ruta("Fuerza bruta", ["ALM", "P02", "ALM"], 99.3))


class TestMapa(unittest.TestCase):
    """T4, T5, T6 y validaciones de MapaReparto (apartado 4.3, 5.2)."""

    def test_T04_matriz_distancias_simetrica_y_diagonal(self):
        # T4: matriz simétrica, diagonal 0.0 y ALM<->P01 = 5.0 con (3,4).
        mapa = mapa_ejemplo()
        self.assertEqual(
            mapa.distancias["ALM"]["ALM"], 0.0, "La diagonal debe valer 0.0"
        )
        self.assertEqual(
            mapa.distancias["ALM"]["P01"], 5.0,
            "La distancia ALM(0,0)-P01(3,4) debe ser 5.0",
        )
        for a in mapa.puntos:
            for b in mapa.puntos:
                with self.subTest(a=a, b=b):
                    self.assertEqual(
                        mapa.distancias[a][b], mapa.distancias[b][a],
                        "La matriz de distancias debe ser simétrica",
                    )
        self.assertEqual(
            mapa.distancia("ALM", "P01"),
            mapa.puntos["ALM"].distancia_a(mapa.puntos["P01"]),
            "mapa.distancia debe coincidir con Punto.distancia_a",
        )

    def test_T05_obtener_entregas_ordenadas_y_almacen(self):
        # T5: entregas ordenadas alfabéticamente; sin ALM -> excepción.
        mapa = MapaReparto([
            punto("P03", "Tres", 1, 1),
            punto("ALM", "Almacén", 0, 0),
            punto("P01", "Uno", 2, 2),
            punto("P02", "Dos", 3, 3),
        ])
        self.assertEqual(
            mapa.obtener_entregas(), ["P01", "P02", "P03"],
            "obtener_entregas debe devolver los ids ordenados con sorted",
        )
        self.assertEqual(
            mapa.obtener_almacen().id, "ALM", "obtener_almacen devuelve el ALM"
        )
        mapa_sin_almacen = MapaReparto([
            punto("P01", "Uno", 1, 1), punto("P02", "Dos", 2, 2)
        ])
        with self.assertRaises(AlmacenNoEncontradoError):
            mapa_sin_almacen.obtener_almacen()

    def test_T06_longitud_suma_tramos_redondeados(self):
        # T6: 49.65 + 49.65 == 99.3 (tramos redondeados antes de sumar).
        mapa_tramo = MapaReparto([
            punto("ALM", "Almacén", 0, 0), punto("P01", "Uno", 49.65, 0)
        ])
        self.assertEqual(
            mapa_tramo.longitud(["ALM", "P01", "ALM"]), 99.3,
            "49.65 + 49.65 debe dar 99.3 y no 99.30 ni otra aproximación",
        )
        # Regla 5.2: se suman los tramos YA redondeados (1.41+1.41=2.82),
        # no la suma de las distancias crudas (2.8284... -> 2.83).
        mapa_diagonal = MapaReparto([
            punto("ALM", "Almacén", 0, 0), punto("P01", "Uno", 1, 1)
        ])
        self.assertEqual(
            mapa_diagonal.longitud(["ALM", "P01", "ALM"]), 2.82,
            "Cada tramo se redondea a 2 decimales antes de sumar",
        )

    def test_mapa_construccion_validaciones(self):
        with self.assertRaises(PuntoDuplicadoError):
            MapaReparto([punto("ALM", "A", 0, 0), punto("ALM", "B", 1, 1)])
        with self.assertRaises(ParametroInvalidoError):
            MapaReparto(["ALM"])  # un str no es un Punto
        # El constructor no exige que exista ALM (apartado 4.3).
        mapa_sin_almacen = MapaReparto([punto("P01", "Uno", 1, 1)])
        self.assertNotIn("ALM", mapa_sin_almacen.puntos)

    def test_consultas_mapa_ids_desconocidos_o_cortas(self):
        mapa = mapa_ejemplo()
        with self.assertRaises(ParametroInvalidoError):
            mapa.distancia("ALM", "P99")
        with self.assertRaises(ParametroInvalidoError):
            mapa.distancia("P99", "ALM")
        with self.assertRaises(ParametroInvalidoError):
            mapa.longitud(["ALM"])
        with self.assertRaises(ParametroInvalidoError):
            mapa.longitud(["ALM", "P99", "ALM"])


class TestCargaCsv(unittest.TestCase):
    """T7 y carga de datos (apartado 7)."""

    def test_T07_csv_de_control(self):
        # T7: 10 puntos, 4 descartes en filas [6, 9, 12, 14] con esos tipos.
        mapa, descartes = cargar_mapa_csv(RUTA_CSV_CONTROL)
        self.assertEqual(
            len(mapa.puntos), 10,
            "El CSV de control debe cargar 10 puntos (ALM y P01..P09)",
        )
        self.assertEqual(
            mapa.obtener_entregas(),
            ["P01", "P02", "P03", "P04", "P05", "P06", "P07", "P08", "P09"],
            "Las 9 entregas del CSV de control deben cargarse ordenadas",
        )
        self.assertEqual(
            [fila for fila, _ in descartes], [6, 9, 12, 14],
            "Las filas descartadas del CSV de control son 6, 9, 12 y 14",
        )
        tipos_esperados = [
            "CoordenadaInvalidaError", "FormatoInvalidoError",
            "PuntoDuplicadoError", "FormatoInvalidoError",
        ]
        tipos_obtenidos = [
            mensaje.split(":", 1)[0] for _, mensaje in descartes
        ]
        self.assertEqual(
            tipos_obtenidos, tipos_esperados,
            "Cada descarte debe ir precedido del nombre de su excepción",
        )
        self.assertTrue(
            all(fila_a < fila_b for (fila_a, _), (fila_b, _) in
                zip(descartes, descartes[1:])),
            "Los descartes deben venir ordenados por número de fila (D4)",
        )
        # Los ids P10/P11/P12 cumplen D9: se descartan por otras causas.
        self.assertIn("fuera del intervalo [0, 100]", descartes[0][1])
        self.assertIn("no es numérica", descartes[1][1])
        self.assertEqual(
            descartes[2][1], "PuntoDuplicadoError: El identificador 'P03' ya existe",
            "El duplicado de la línea 12 debe informar del id repetido",
        )

    def test_csv_con_filas_erroneas_creado_en_la_prueba(self):
        # CSV con filas incorrectas creado dentro de la propia prueba:
        # número de campos, id/nombre vacíos, id D9 inválido, conversión
        # numérica, rango, duplicado, línea vacía, precedencia y strip().
        contenido = (
            "id,nombre,x,y\n"                       # línea 1 (cabecera)
            "ALM,Almacén do Tambre,50,50\n"         # 2: válida
            "P01,Uno,10,10\n"                       # 3: válida
            "X01,Malo,20,20\n"                       # 4: id D9 inválido
            "X02,También malo,abc,20\n"              # 5: id antes que número
            ",SinId,20,20\n"                        # 6: id vacío
            "P02,,30,30\n"                          # 7: nombre vacío
            "P03,SinCampos,40\n"                    # 8: 3 columnas
            "P04,Rango,200,10\n"                    # 9: fuera de [0, 100]
            "P05,NoNum,abc,10\n"                    # 10: no numérica
            "\n"                                    # 11: línea vacía
            "P01,Dup,11,11\n"                       # 12: duplicado de P01
            "P06,Seis,60,60\n"                      # 13: válida
            "  P07   ,  Espacios con márgenes  ,  70  ,  70  \n"  # 14: strip()
        )
        with tempfile.TemporaryDirectory() as tmp:
            ruta = Path(tmp) / "filas_erroneas.csv"
            ruta.write_text(contenido, encoding="utf-8")
            mapa, descartes = cargar_mapa_csv(str(ruta))

        self.assertEqual(
            list(mapa.puntos), ["ALM", "P01", "P06", "P07"],
            "Solo las filas válidas deben cargarse, con strip() aplicado",
        )
        self.assertEqual(
            mapa.puntos["P07"].nombre, "Espacios con márgenes",
            "Los campos deben normalizarse con strip() antes de validar",
        )
        self.assertEqual(
            [fila for fila, _ in descartes], [4, 5, 6, 7, 8, 9, 10, 11, 12],
            "Debe descartarse exactamente una entrada por fila incorrecta",
        )
        mensajes = {fila: mensaje for fila, mensaje in descartes}
        self.assertEqual(
            mensajes[4],
            "FormatoInvalidoError: El identificador 'X01' no es válido; "
            "se espera ALM o P seguido de dos dígitos entre 01 y 99",
            "Mensaje exacto de id no permitido (D9)",
        )
        self.assertEqual(
            mensajes[5],
            "FormatoInvalidoError: El identificador 'X02' no es válido; "
            "se espera ALM o P seguido de dos dígitos entre 01 y 99",
            "Precedencia: el error del id se registra antes que el numérico",
        )
        self.assertNotIn("numérica", mensajes[5])
        self.assertEqual(
            mensajes[6], "FormatoInvalidoError: El campo id está vacío",
            "Mensaje exacto de id vacío",
        )
        self.assertEqual(
            mensajes[7], "FormatoInvalidoError: El campo nombre está vacío",
            "Mensaje exacto de nombre vacío",
        )
        for fila in (8, 11):
            with self.subTest(fila=fila):
                self.assertTrue(
                    mensajes[fila].startswith(
                        "FormatoInvalidoError: Se esperaban 4 columnas"
                    ),
                    "Filas con número de campos distinto de 4 (incluida la "
                    "vacía) se descartan por número de columnas",
                )
        self.assertTrue(
            mensajes[9].startswith("CoordenadaInvalidaError: La coordenada x=")
            and "está fuera del intervalo [0, 100]" in mensajes[9],
            "Coordenada fuera de rango con su mensaje exacto",
        )
        self.assertTrue(
            mensajes[10].startswith("FormatoInvalidoError: La coordenada x")
            and "no es numérica" in mensajes[10],
            "Coordenada no numérica con su mensaje exacto",
        )
        self.assertEqual(
            mensajes[12], "PuntoDuplicadoError: El identificador 'P01' ya existe",
            "Mensaje exacto de id duplicado (D5)",
        )

    def test_csv_cabecera_invalida(self):
        contenidos = [
            "nombre,id,y,x\nAlmacén,ALM,50,50\n",   # orden cambiado
            "id,nombre,x\nP01,Uno,10\n",            # falta una columna
        ]
        for contenido in contenidos:
            with self.subTest(contenido=contenido.splitlines()[0]):
                with tempfile.TemporaryDirectory() as tmp:
                    ruta = Path(tmp) / "cabecera_mala.csv"
                    ruta.write_text(contenido, encoding="utf-8")
                    with self.assertRaises(FormatoInvalidoError) as ctx:
                        cargar_mapa_csv(ruta)
                self.assertEqual(
                    str(ctx.exception),
                    "El CSV debe tener exactamente las columnas id,nombre,x,y",
                    "Cabecera distinta de id,nombre,x,y: mensaje exacto",
                )

    def test_csv_sin_almacen(self):
        contenidos = [
            "id,nombre,x,y\nP01,Uno,10,10\n",        # nunca hay ALM
            "id,nombre,x,y\nALM,Almacén,200,50\n",    # ALM descartado por rango
        ]
        for contenido in contenidos:
            with self.subTest(contenido=contenido.splitlines()[1]):
                with tempfile.TemporaryDirectory() as tmp:
                    ruta = Path(tmp) / "sin_almacen.csv"
                    ruta.write_text(contenido, encoding="utf-8")
                    with self.assertRaises(AlmacenNoEncontradoError):
                        cargar_mapa_csv(ruta)

    def test_csv_inexistente_file_not_found(self):
        with tempfile.TemporaryDirectory() as tmp:
            inexistente = Path(tmp) / "no_existe_este.csv"
            with self.assertRaises(FileNotFoundError):
                cargar_mapa_csv(str(inexistente))


class TestPlanificadores(unittest.TestCase):
    """T8-T12, T15, T16 y casos límite (apartados 6 y 12)."""

    def test_T08_fuerza_bruta_rechaza_mas_de_10_entregas(self):
        # T8: 11 entregas (P01..P11, válidas según D9) -> ParametroInvalidoError.
        puntos = [punto("ALM", "Almacén", 50, 50)]
        for n in range(1, 12):
            puntos.append(punto(f"P{n:02d}", f"Entrega {n}", n * 8, n * 5))
        mapa = MapaReparto(puntos)
        with self.assertRaises(ParametroInvalidoError):
            FuerzaBruta().planificar(mapa)
        # Apartado 12: solo falla FuerzaBruta; los demás siguen funcionando
        # y devuelven rutas válidas con las 11 entregas.
        entregas = mapa.obtener_entregas()
        for planificador in (VecinoMasCercano(), InsercionMasBarata()):
            with self.subTest(planificador=planificador.nombre):
                r = planificador.planificar(mapa)
                self.assertEqual(
                    r.paradas[0], "ALM", "La ruta debe salir del almacén"
                )
                self.assertEqual(
                    r.paradas[-1], "ALM", "La ruta debe volver al almacén"
                )
                self.assertEqual(
                    sorted(r.paradas[1:-1]), entregas,
                    "Debe visitar cada entrega exactamente una vez",
                )

    def test_T09_fuerza_bruta_conserva_primera_en_empate(self):
        # T9: dos órdenes empatan (34.14); se conserva el orden alfabético.
        mapa = MapaReparto([
            punto("ALM", "Almacén", 0, 0),
            punto("P02", "Dos", 0, 10),
            punto("P01", "Uno", 10, 0),
        ])
        r = FuerzaBruta().planificar(mapa)
        self.assertEqual(
            r.paradas, ["ALM", "P01", "P02", "ALM"],
            "Con empate se conserva la primera ruta encontrada (orden alfabético)",
        )
        self.assertEqual(
            r.longitud, 34.14, "10 + 14.14 + 10 = 34.14 con tramos redondeados"
        )

    def test_T10_vecino_mas_cercano_empate_id_menor(self):
        # T10: empate de distancias desde ALM; se elige el id menor (P01),
        # aunque P02 se inserte antes en el mapa.
        mapa = MapaReparto([
            punto("ALM", "Almacén", 0, 0),
            punto("P02", "Dos", 0, 10),
            punto("P01", "Uno", 10, 0),
        ])
        r = VecinoMasCercano().planificar(mapa)
        self.assertEqual(
            r.paradas, ["ALM", "P01", "P02", "ALM"],
            "Ante empate de distancias debe elegirse el id alfabéticamente menor",
        )

    def test_T11_insercion_mas_barata_resultado_esperado(self):
        # T11: con la rejilla de cruces la ruta esperada es
        # ALM -> P02 -> P03 -> P01 -> ALM con longitud 40.0.
        r = InsercionMasBarata().planificar(mapa_cruces())
        self.assertEqual(
            r.paradas, ["ALM", "P02", "P03", "P01", "ALM"],
            "Inserción con clave (coste, id, posición) produce esa ruta",
        )
        self.assertEqual(
            r.longitud, 40.0,
            "10+10+10+10 con distancias ya redondeadas = 40.0",
        )
        self.assertEqual(
            r.nombre, "Inserción más barata",
            "La Ruta lleva el nombre del planificador (D2)",
        )

    def test_T12_mejora_dos_opt_con_stub(self):
        # T12: el stub devuelve ALM-P01-P02-P03-ALM (48.28) y 2-opt la
        # mejora a ALM-P01-P03-P02-ALM (40.0) con nombre "Stub + 2-opt".
        stub = _StubPlanificador(["ALM", "P01", "P02", "P03", "ALM"])
        plan = MejoraDosOpt(stub)
        self.assertEqual(
            plan.nombre, "Stub + 2-opt",
            "El nombre se genera como f'{planificador.nombre} + 2-opt' (D3)",
        )
        r = plan.planificar(mapa_cruces())
        self.assertIsInstance(
            r, Ruta, "planificar devuelve un único Ruta (D2)"
        )
        self.assertEqual(
            r.nombre, "Stub + 2-opt", "La Ruta devuelta lleva el nombre 2-opt"
        )
        self.assertEqual(
            r.paradas, ["ALM", "P01", "P03", "P02", "ALM"],
            "2-opt invierte el tramo que mejora de forma estricta",
        )
        self.assertEqual(
            r.longitud, 40.0,
            "La longitud tras 2-opt es 10+10+10+10 = 40.0",
        )
        self.assertEqual(
            stub.paradas_fijas, ["ALM", "P01", "P02", "P03", "ALM"],
            "2-opt trabaja sobre una copia y no modifica la ruta inicial",
        )


class TestGraficas(unittest.TestCase):
    """T13, T14 y validaciones de graficas (apartado 8)."""

    def test_T13_calcular_diferencia(self):
        # T13: diferencias con signo redondeadas a 2 decimales (D6).
        self.assertEqual(
            calcular_diferencia(105, 100), 5.0,
            "(105-100)/100*100 debe dar 5.0",
        )
        self.assertEqual(
            calcular_diferencia(95, 100), -5.0,
            "La diferencia se calcula con signo: debe dar -5.0",
        )
        self.assertEqual(
            calcular_diferencia(0, 0), 0.0,
            "Si la óptima es 0 la diferencia vale 0.0 (D6)",
        )
        self.assertEqual(
            calcular_diferencia(100, 0), 0.0,
            "Con óptima 0 cualquier longitud da 0.0 (D6)",
        )

    def test_graficas_rechazan_longitudes_invalidas(self):
        casos = [
            ("longitud negativa", -1, 100),
            ("óptima negativa", 100, -1),
            ("longitud NaN", float("nan"), 100),
            ("óptima infinita", 100, float("inf")),
        ]
        for etiqueta, longitud, optima in casos:
            with self.subTest(caso=etiqueta):
                with self.assertRaises(ParametroInvalidoError):
                    calcular_diferencia(longitud, optima)

    def test_guardar_comparativa_listas_de_distinta_longitud(self):
        mapa = mapa_ejemplo()
        r = Ruta("Fuerza bruta", ["ALM", "P01", "ALM"], 10.0)
        with self.assertRaises(ParametroInvalidoError):
            guardar_comparativa([r], [], r, mapa)

    def test_T14_formatear_tabla(self):
        # T14: cabeceras exactas, tablefmt="grid" y números a 2 decimales.
        tabla = formatear_tabla([
            ("Fuerza bruta", 100.0, 0.0),
            ("Vecino más cercano", 105.0, 5.0),
        ])
        self.assertIn(
            "Planificador", tabla, "La cabecera 1 debe ser Planificador"
        )
        self.assertIn("Longitud", tabla, "La cabecera 2 debe ser Longitud")
        self.assertIn(
            "Diferencia (%)", tabla, "La cabecera 3 debe ser Diferencia (%)"
        )
        self.assertIn(
            "105.00", tabla, "Las longitudes se formatean a 2 decimales"
        )
        self.assertIn(
            "5.00", tabla, "Los porcentajes se formatean a 2 decimales"
        )
        self.assertIn("+", tabla, "tablefmt='grid' dibuja la rejilla con + y -")
        self.assertIn("|", tabla, "tablefmt='grid' separa las celdas con |")


class TestExcepciones(unittest.TestCase):
    """Apartado 3: jerarquía y situaciones de cada excepción."""

    def test_jerarquia_de_excepciones(self):
        self.assertIs(
            RutasError.__bases__[0], Exception,
            "RutasError hereda directamente de Exception",
        )
        derivadas = (
            FormatoInvalidoError, CoordenadaInvalidaError,
            PuntoDuplicadoError, AlmacenNoEncontradoError,
            ParametroInvalidoError,
        )
        for cls in derivadas:
            with self.subTest(exc=cls.__name__):
                self.assertIs(
                    cls.__bases__[0], RutasError,
                    f"{cls.__name__} debe heredar directamente de RutasError",
                )
        self.assertEqual(
            str(FormatoInvalidoError("detalle del error")),
            "detalle del error",
            "Las excepciones aceptan un mensaje opcional que str() devuelve",
        )
        self.assertEqual(
            str(CoordenadaInvalidaError()), "",
            "El mensaje es opcional; sin él str(exc) es la cadena vacía",
        )
        try:
            raise PuntoDuplicadoError("dup")
        except RutasError as exc:
            capturada = exc
        else:  # pragma: no cover - solo si nadie lanzó
            self.fail("except RutasError debe capturar cualquier error propio")
        self.assertEqual(str(capturada), "dup")

    def test_planificador_base_lanza_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            Planificador().planificar(mapa_ejemplo())

    def test_parametro_invalido_en_consultas_diversas(self):
        with self.assertRaises(ParametroInvalidoError):
            punto("ALM", "Almacén", 0, 0).distancia_a("P01")
        with self.assertRaises(ParametroInvalidoError):
            MejoraDosOpt("Vecino más cercano")


class TestCasosLimite(unittest.TestCase):
    """Apartado 12: cero entregas, una entrega y 2-opt sin empeorar."""

    def test_cero_entregas_todos_los_planificadores(self):
        mapa = MapaReparto([punto("ALM", "Almacén", 50, 50)])
        planificadores = [
            FuerzaBruta(), VecinoMasCercano(), InsercionMasBarata(),
            MejoraDosOpt(VecinoMasCercano()),
            MejoraDosOpt(InsercionMasBarata()),
        ]
        for planificador in planificadores:
            with self.subTest(planificador=planificador.nombre):
                r = planificador.planificar(mapa)
                self.assertEqual(
                    r.paradas, ["ALM", "ALM"],
                    "Sin entregas la ruta es ['ALM', 'ALM']",
                )
                self.assertEqual(
                    r.longitud, 0.0, "Sin entregas la longitud es 0.0"
                )

    def test_una_entrega_dos_opt_no_puede_mejorar(self):
        mapa = MapaReparto([
            punto("ALM", "Almacén", 0, 0), punto("P01", "Uno", 10, 0)
        ])
        stub = _StubPlanificador(["ALM", "P01", "ALM"])
        r = MejoraDosOpt(stub).planificar(mapa)
        self.assertEqual(
            r.paradas, ["ALM", "P01", "ALM"],
            "Con menos de dos entregas 2-opt devuelve la ruta inicial",
        )
        self.assertEqual(
            r.longitud, 20.0, "10 + 10 = 20.0 con tramos redondeados"
        )
        self.assertEqual(
            r.nombre, "Stub + 2-opt", "La ruta lleva el nombre del 2-opt"
        )

    def test_T15_planificadores_sobre_csv_rutas_validas(self):
        # T15: las cinco rutas sobre el CSV de control son válidas y
        # ninguna es más corta que la de fuerza bruta.
        mapa, _ = cargar_mapa_csv(RUTA_CSV_CONTROL)
        planificadores = [
            FuerzaBruta(), VecinoMasCercano(), InsercionMasBarata(),
            MejoraDosOpt(VecinoMasCercano()),
            MejoraDosOpt(InsercionMasBarata()),
        ]
        nombres = [
            "Fuerza bruta", "Vecino más cercano", "Inserción más barata",
            "Vecino más cercano + 2-opt", "Inserción más barata + 2-opt",
        ]
        entregas = mapa.obtener_entregas()
        rutas = [planificador.planificar(mapa) for planificador in planificadores]
        optima = rutas[0]
        for nombre, r in zip(nombres, rutas):
            with self.subTest(planificador=nombre):
                self.assertIsInstance(r, Ruta, "planificar devuelve un Ruta (D2)")
                self.assertEqual(
                    r.nombre, nombre, "La Ruta lleva el nombre del planificador"
                )
                self.assertEqual(
                    r.paradas[0], "ALM", "La ruta debe salir del almacén"
                )
                self.assertEqual(
                    r.paradas[-1], "ALM", "La ruta debe volver al almacén"
                )
                self.assertEqual(
                    sorted(r.paradas[1:-1]), entregas,
                    "Debe visitar cada entrega exactamente una vez",
                )
                self.assertGreaterEqual(
                    r.longitud, optima.longitud,
                    "Ninguna ruta puede ser más corta que la fuerza bruta",
                )

    def test_T16_dos_opt_nunca_empeora(self):
        # T16: 2-opt por composición no aumenta la longitud de la base.
        mapa, _ = cargar_mapa_csv(RUTA_CSV_CONTROL)
        for base in (VecinoMasCercano(), InsercionMasBarata()):
            with self.subTest(base=base.nombre):
                r_base = base.planificar(mapa)
                r_mejorada = MejoraDosOpt(base).planificar(mapa)
                self.assertLessEqual(
                    r_mejorada.longitud, r_base.longitud,
                    "2-opt solo aplica inversiones estrictamente mejores",
                )
                self.assertEqual(
                    r_mejorada.nombre, base.nombre + " + 2-opt",
                    "El nombre compuesto sigue el patrón de D3",
                )


if __name__ == "__main__":
    unittest.main()
