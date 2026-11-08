from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from encuestas.models import Pregunta, Opcion

def crear_pregunta_opciones(texto_pregunta, texto_opcion1, texto_opcion2, votos_opcion1, votos_opcion2):
    pregunta = Pregunta.objects.create(texto_pregunta=texto_pregunta)
    opcion1 = Opcion.objects.create(texto_opcion = texto_opcion1, votos = votos_opcion1, pregunta = pregunta)
    opcion2 = Opcion.objects.create(texto_opcion = texto_opcion2, votos = votos_opcion2, pregunta = pregunta)
    return pregunta, [opcion1,opcion2]

def print_pregunta(pregunta):
    print(f"PK: {pregunta.pk}, ID: {pregunta.id}, {pregunta}")
    opciones = pregunta.opcion_set.all()
    for opcion in opciones:
        print(f"PK: {opcion.pk}, ID: {opcion.id}, {opcion}")

class EncuestasTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Inicialización de datos para todos los test de la clase
        cls.username = 'usuario'
        cls.password = 'clave'
        User.objects.create_user(username=cls.username, password=cls.password)

    def test_listado_encuestas_vacio(self):
        """Test para obtener un listado de encuestas vacío"""

        response = self.client.get(reverse('home'))

        # Comprobar que la página se carga correctamente
        self.assertEqual(response.status_code, 200)

        # Comprobar que aparece el mensaje correspondiente
        self.assertContains(response, "No hay encuestas")

        # Comprobar que no existen encuestas
        self.assertQuerySetEqual(response.context["preguntas"], [])


    def test_listado_encuestas_una_pregunta(self):
        """Test para obtener un listado de encuestas con una encuesta"""

        pregunta = crear_pregunta_opciones(
            "pregunta 1",
            "opcion 1",
            "opcion 2",
            23,
            25
        )[0]

        response = self.client.get(reverse('home'))

        # Comprobar que la página se carga correctamente
        self.assertEqual(response.status_code, 200)

        # Comprobar que aparece la encuesta en el listado
        self.assertContains(response, "pregunta 1")

        # Comprobar que el listado contiene exactamente esa encuesta
        self.assertQuerySetEqual(
            response.context["preguntas"],
            [pregunta]
        )


    def test_ver_resultados(self):
        """Test para ver los resultados de una encuesta"""

        pregunta = crear_pregunta_opciones(
            "pregunta 1",
            "opcion 1",
            "opcion 2",
            23,
            25
        )[0]

        response = self.client.get(
            reverse('resultados', args=[pregunta.id])
        )

        # Comprobar que la página se muestra correctamente
        self.assertEqual(response.status_code, 200)

        # Comprobar que se muestra la encuesta correcta
        pregunta_mostrada = response.context["pregunta"]
        self.assertEqual(pregunta, pregunta_mostrada)

        # Comprobar el número total de votos
        self.assertEqual(response.context["total_votos"], 48)

        # Comprobar el número de opciones
        self.assertEqual(pregunta_mostrada.opcion_set.count(), 2)


    def test_votar(self):
        """Test para votar en una encuesta"""

        pregunta, opciones = crear_pregunta_opciones(
            "pregunta 1",
            "opcion 1",
            "opcion 2",
            23,
            25
        )

        data = {
            'opcion': opciones[0].id,
        }

        # Enviar voto
        response = self.client.post(
            reverse('votar', args=[pregunta.id]),
            data
        )

        # Comprobar redirección a resultados
        self.assertRedirects(
            response,
            reverse('resultados', args=[pregunta.id])
        )

        # Consultar página de resultados
        response = self.client.get(
            reverse('resultados', args=[pregunta.id])
        )

        self.assertEqual(response.status_code, 200)

        # Comprobar que el voto se ha contabilizado
        pregunta_mostrada = response.context["pregunta"]

        opcion_votada = pregunta_mostrada.opcion_set.get(
            id=opciones[0].id
        )

        self.assertEqual(opcion_votada.votos, 24)

        # Comprobar que la otra opción no ha cambiado
        opcion_no_votada = pregunta_mostrada.opcion_set.get(
            id=opciones[1].id
        )

        self.assertEqual(opcion_no_votada.votos, 25)


    def test_login(self):
        """Test para hacer login"""

        data = {
            'username': self.username,
            'password': self.password
        }

        # Iniciar sesión
        response = self.client.post(reverse('login'), data)

        # Comprobar que se redirige a la página de inicio
        self.assertRedirects(response, reverse('home'))

        # Comprobar que el usuario está autenticado
        self.assertTrue(
            '_auth_user_id' in self.client.session
        )

        # Comprobar que los botones Crear y Logout están disponibles
        response = self.client.get(reverse('home'))

        self.assertContains(response, "Crear")
        self.assertContains(response, "LOGOUT")

        # Cerrar sesión
        response = self.client.get(reverse('logout'))

        # Comprobar que se redirige a la página de inicio
        self.assertRedirects(response, reverse('home'))

        # Comprobar que el usuario ya no está autenticado
        self.assertFalse(
            '_auth_user_id' in self.client.session
        )

    def test_crear_encuesta(self):
        """Test para crear una encuesta"""

        # Iniciar sesión
        self.client.login(
            username=EncuestasTest.username,
            password=EncuestasTest.password
        )

        data = {
            'texto_pregunta': 'pregunta creada',

            'opcion_set-TOTAL_FORMS': '2',
            'opcion_set-INITIAL_FORMS': '0',
            'opcion_set-MIN_NUM_FORMS': '2',
            'opcion_set-MAX_NUM_FORMS': '1000',

            'opcion_set-0-texto_opcion': 'opcion 1',
            'opcion_set-1-texto_opcion': 'opcion 2',
        }

        response = self.client.post(reverse('crear'), data)

        # Comprobar redirección
        self.assertRedirects(response, reverse('home'))

        # Comprobar que la encuesta existe
        pregunta = Pregunta.objects.get(
            texto_pregunta='pregunta creada'
        )

        # Comprobar que se han creado las dos opciones
        opciones = pregunta.opcion_set.all()
        self.assertEqual(opciones.count(), 2)
        self.assertEqual(opciones[0].texto_opcion, 'opcion 1')
        self.assertEqual(opciones[1].texto_opcion, 'opcion 2')

    def test_editar_encuesta(self):
        """Test para editar una encuesta"""

        # Iniciar sesión
        self.client.login(
            username=EncuestasTest.username,
            password=EncuestasTest.password
        )

        # Crear encuesta y opciones
        pregunta, opciones = crear_pregunta_opciones(
            "pregunta 1",
            "opcion 1",
            "opcion 2",
            23,
            25
        )

        data = {
            'texto_pregunta': 'pregunta 1 actualizada',

            # FormSet management data
            'opcion_set-TOTAL_FORMS': '2',
            'opcion_set-INITIAL_FORMS': '2',
            'opcion_set-MIN_NUM_FORMS': '2',
            'opcion_set-MAX_NUM_FORMS': '1000',

            # Updated options
            'opcion_set-0-id': str(opciones[0].id),
            'opcion_set-0-texto_opcion': 'opcion 1 actualizada',
            'opcion_set-1-id': str(opciones[1].id),
            'opcion_set-1-texto_opcion': 'opcion 2 actualizada',
        }

        # Editar encuesta
        response = self.client.post(
            reverse('editar', args=[pregunta.id]),
            data
        )

        # Comprobar redirección
        self.assertRedirects(response, reverse('home'))

        # Comprobar que la encuesta existe
        pregunta_actualizada = Pregunta.objects.get(
            id=pregunta.id
        )

        # Comprobar actualización del texto de la pregunta
        self.assertEqual(
            pregunta_actualizada.texto_pregunta,
            'pregunta 1 actualizada'
        )

        # Comprobar que siguen existiendo exactamente dos opciones
        self.assertEqual(
            pregunta_actualizada.opcion_set.count(),
            2
        )

        # Comprobar que las opciones originales se han actualizado
        opcion1 = Opcion.objects.get(id=opciones[0].id)
        opcion2 = Opcion.objects.get(id=opciones[1].id)

        self.assertEqual(
            opcion1.texto_opcion,
            'opcion 1 actualizada'
        )

        self.assertEqual(
            opcion2.texto_opcion,
            'opcion 2 actualizada'
        )

    def test_eliminar_encuesta(self):
        """Test para eliminar una encuesta"""

        # Iniciar sesión
        self.client.login(
            username=EncuestasTest.username,
            password=EncuestasTest.password
        )

        # Crear encuesta y opciones
        pregunta, opciones = crear_pregunta_opciones(
            "pregunta 1",
            "opcion 1",
            "opcion 2",
            23,
            25
        )

        # Eliminar encuesta
        response = self.client.post(
            reverse('eliminar', args=[pregunta.id])
        )

        # Comprobar redirección
        self.assertRedirects(response, reverse('home'))

        # Comprobar que la encuesta ha sido eliminada
        self.assertFalse(
            Pregunta.objects.filter(id=pregunta.id).exists()
        )

        # Comprobar que las opciones también han sido eliminadas
        for opcion in opciones:
            self.assertFalse(
                Opcion.objects.filter(id=opcion.id).exists()
            )
