"""
PRUEBAS DE INTEGRACIÓN COMPLETAS - APIs faltantes
Cobertura: Aulas, Cursos, Docentes, Carreras, Horarios
"""
import pytest
import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from src.app import app


@pytest.mark.integration
class TestAulasAPI(unittest.TestCase):
    """Pruebas de integración para CRUD de Aulas."""

    def setUp(self):
        self.client = TestClient(app)
        self.aula_valida = {
            "nombre": "A-101",
            "capacidad": 40,
            "edificio": "Principal",
            "equipamiento": "Proyector"
        }

    @patch('src.services.aula_service.AulaRepository')
    def test_get_aulas_retorna_lista(self, mock_repo):
        """Happy Path: GET aulas retorna lista con éxito."""
        mock_repo.get_all.return_value = [
            {"aulaid": 1, "nombre": "A-101", "capacidad": 40, "edificio": "Principal", "equipamiento": "Proyector", "activo": True}
        ]
        response = self.client.get("/api/aulas")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIsInstance(data["data"], list)
        self.assertEqual(len(data["data"]), 1)

    @patch('src.services.aula_service.AulaRepository')
    def test_get_aulas_lista_vacia(self, mock_repo):
        """Edge Case: GET aulas retorna lista vacía."""
        mock_repo.get_all.return_value = []
        response = self.client.get("/api/aulas")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"], [])

    @patch('src.services.aula_service.AulaRepository')
    def test_create_aula_exitoso(self, mock_repo):
        """Happy Path: Crear aula con datos válidos."""
        mock_repo.create.return_value = {
            "Exito": True, "ID": 1, "Mensaje": "Aula creada con éxito"
        }
        response = self.client.post("/api/aulas", json=self.aula_valida)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["data"]["id"], 1)

    @patch('src.services.aula_service.AulaRepository')
    def test_create_aula_nombre_duplicado(self, mock_repo):
        """Unhappy Path: Nombre de aula duplicado devuelve 400."""
        mock_repo.create.return_value = {
            "Exito": False, "Mensaje": "El aula ya existe"
        }
        response = self.client.post("/api/aulas", json=self.aula_valida)
        self.assertEqual(response.status_code, 400)
        self.assertIn("El aula ya existe", response.json()["detail"])

    def test_create_aula_sin_campos_requeridos(self):
        """Unhappy Path: Datos incompletos devuelven 422."""
        response = self.client.post("/api/aulas", json={"nombre": "Solo nombre"})
        self.assertEqual(response.status_code, 422)

    @patch('src.services.aula_service.AulaRepository')
    def test_update_aula_exitoso(self, mock_repo):
        """Happy Path: Actualización de aula existente."""
        mock_repo.update.return_value = {
            "Exito": True, "Mensaje": "Aula actualizada"
        }
        response = self.client.put("/api/aulas/1", json={
            "nombre": "A-102", "capacidad": 50, "edificio": "Norte"
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])

    @patch('src.services.aula_service.AulaRepository')
    def test_update_aula_no_encontrado(self, mock_repo):
        """Unhappy Path: Actualizar aula inexistente devuelve 400."""
        mock_repo.update.return_value = {
            "Exito": False, "Mensaje": "Aula no encontrada"
        }
        response = self.client.put("/api/aulas/9999", json={
            "nombre": "X", "capacidad": 10, "edificio": "Z"
        })
        self.assertEqual(response.status_code, 400)

    @patch('src.services.aula_service.AulaRepository')
    def test_delete_aula_exitoso(self, mock_repo):
        """Happy Path: Eliminar aula existente."""
        mock_repo.delete.return_value = True
        response = self.client.delete("/api/aulas/1")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])

    @patch('src.services.aula_service.AulaRepository')
    def test_respuesta_json_estructura_correcta(self, mock_repo):
        """Valida estructura del JSON de respuesta en GET."""
        mock_repo.get_all.return_value = []
        response = self.client.get("/api/aulas")
        data = response.json()
        self.assertIn("success", data)
        self.assertIn("data", data)
        self.assertIsInstance(data["success"], bool)

    @patch('src.services.aula_service.AulaRepository')
    def test_manejo_excepcion_repositorio(self, mock_repo):
        """Verifica manejo de excepciones inesperadas."""
        mock_repo.get_all.side_effect = Exception("Error de base de datos")
        client_no_raise = TestClient(app, raise_server_exceptions=False)
        response = client_no_raise.get("/api/aulas")
        self.assertEqual(response.status_code, 500)


@pytest.mark.integration
class TestCursosAPI(unittest.TestCase):
    """Pruebas de integración para CRUD de Cursos."""

    def setUp(self):
        self.client = TestClient(app)
        self.curso_valido = {
            "codigo": "MAT-101",
            "nombre": "Matemáticas I",
            "creditosReq": 0,
            "docenteID": 1,
            "cupos": 30,
            "carreraID": 1
        }

    @patch('src.services.curso_service.CursoRepository')
    def test_get_cursos_retorna_lista(self, mock_repo):
        """Happy Path: GET cursos retorna lista con éxito."""
        mock_repo.get_all.return_value = [
            {"cursoid": 1, "codigo": "MAT-101", "nombre": "Matemáticas I", "creditosreq": 0}
        ]
        response = self.client.get("/api/cursos")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIsInstance(data["data"], list)

    @patch('src.services.curso_service.CursoRepository')
    def test_get_cursos_lista_vacia(self, mock_repo):
        """Edge Case: GET cursos retorna lista vacía."""
        mock_repo.get_all.return_value = []
        response = self.client.get("/api/cursos")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"], [])

    @patch('src.services.curso_service.CursoRepository')
    def test_create_curso_exitoso(self, mock_repo):
        """Happy Path: Crear curso con datos válidos."""
        mock_repo.create.return_value = {
            "Exito": True, "ID": 5, "Mensaje": "Curso creado con éxito"
        }
        response = self.client.post("/api/cursos", json=self.curso_valido)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["data"]["id"], 5)

    @patch('src.services.curso_service.CursoRepository')
    def test_create_curso_codigo_duplicado(self, mock_repo):
        """Unhappy Path: Código duplicado devuelve 400."""
        mock_repo.create.return_value = {
            "Exito": False, "Mensaje": "El código del curso ya existe"
        }
        response = self.client.post("/api/cursos", json=self.curso_valido)
        self.assertEqual(response.status_code, 400)
        self.assertIn("código", response.json()["detail"])

    def test_create_curso_sin_campos_requeridos(self):
        """Unhappy Path: Datos incompletos devuelven 422."""
        response = self.client.post("/api/cursos", json={"nombre": "Solo nombre"})
        self.assertEqual(response.status_code, 422)

    @patch('src.services.curso_service.CursoRepository')
    def test_update_curso_exitoso(self, mock_repo):
        """Happy Path: Actualización de curso existente."""
        mock_repo.update.return_value = {
            "Exito": True, "Mensaje": "Curso actualizado"
        }
        response = self.client.put("/api/cursos/1", json={
            "codigo": "MAT-102", "nombre": "Matemáticas II", "creditosReq": 4,
            "docenteID": 2, "cupos": 35
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])

    @patch('src.services.curso_service.CursoRepository')
    def test_update_curso_no_encontrado(self, mock_repo):
        """Unhappy Path: Actualizar curso inexistente devuelve 400."""
        mock_repo.update.return_value = {
            "Exito": False, "Mensaje": "Curso no encontrado"
        }
        response = self.client.put("/api/cursos/9999", json={
            "codigo": "X", "nombre": "Y", "creditosReq": 0, "docenteID": 1, "cupos": 30
        })
        self.assertEqual(response.status_code, 400)

    @patch('src.services.curso_service.CursoRepository')
    def test_delete_curso_exitoso(self, mock_repo):
        """Happy Path: Eliminar curso existente."""
        mock_repo.delete.return_value = True
        response = self.client.delete("/api/cursos/1")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])

    @patch('src.services.curso_service.CursoRepository')
    def test_respuesta_json_estructura_correcta(self, mock_repo):
        """Valida estructura del JSON de respuesta en GET."""
        mock_repo.get_all.return_value = []
        response = self.client.get("/api/cursos")
        data = response.json()
        self.assertIn("success", data)
        self.assertIn("data", data)

    @patch('src.services.curso_service.CursoRepository')
    def test_manejo_excepcion_repositorio(self, mock_repo):
        """Verifica manejo de excepciones inesperadas."""
        mock_repo.get_all.side_effect = Exception("Error de base de datos")
        client_no_raise = TestClient(app, raise_server_exceptions=False)
        response = client_no_raise.get("/api/cursos")
        self.assertEqual(response.status_code, 500)


@pytest.mark.integration
class TestDocentesAPI(unittest.TestCase):
    """Pruebas de integración para CRUD de Docentes."""

    def setUp(self):
        self.client = TestClient(app)
        self.docente_valido = {
            "codigo": "DOC-001",
            "nombre": "Carlos",
            "apellido": "López",
            "especialidad": "Matemáticas",
            "correo": "carlos@uni.edu"
        }

    @patch('src.services.docente_service.DocenteRepository')
    def test_get_docentes_retorna_lista(self, mock_repo):
        """Happy Path: GET docentes retorna lista con éxito."""
        mock_repo.get_all.return_value = [
            {"docenteid": 1, "codigo": "DOC-001", "nombre": "Carlos", "apellido": "López", "activo": True}
        ]
        response = self.client.get("/api/docentes")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIsInstance(data["data"], list)

    @patch('src.services.docente_service.DocenteRepository')
    def test_get_docentes_lista_vacia(self, mock_repo):
        """Edge Case: GET docentes retorna lista vacía."""
        mock_repo.get_all.return_value = []
        response = self.client.get("/api/docentes")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"], [])

    @patch('src.services.docente_service.DocenteRepository')
    def test_get_docentes_solo_activos_param(self, mock_repo):
        """Verifica que el parámetro solo_activos se procesa."""
        mock_repo.get_all.return_value = []
        response = self.client.get("/api/docentes?solo_activos=false")
        self.assertEqual(response.status_code, 200)
        mock_repo.get_all.assert_called_once_with(False)

    @patch('src.services.docente_service.DocenteRepository')
    def test_create_docente_exitoso(self, mock_repo):
        """Happy Path: Crear docente con datos válidos."""
        mock_repo.create.return_value = {
            "Exito": True, "ID": 10, "Mensaje": "Docente creado con éxito"
        }
        response = self.client.post("/api/docentes", json=self.docente_valido)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["data"]["id"], 10)

    @patch('src.services.docente_service.DocenteRepository')
    def test_create_docente_codigo_duplicado(self, mock_repo):
        """Unhappy Path: Código duplicado devuelve 400."""
        mock_repo.create.return_value = {
            "Exito": False, "Mensaje": "El código ya existe"
        }
        response = self.client.post("/api/docentes", json=self.docente_valido)
        self.assertEqual(response.status_code, 400)
        self.assertIn("código", response.json()["detail"])

    def test_create_docente_sin_campos_requeridos(self):
        """Unhappy Path: Datos incompletos devuelven 422."""
        response = self.client.post("/api/docentes", json={"nombre": "Solo nombre"})
        self.assertEqual(response.status_code, 422)

    @patch('src.services.docente_service.DocenteRepository')
    def test_update_docente_exitoso(self, mock_repo):
        """Happy Path: Actualización de docente existente."""
        mock_repo.update.return_value = {
            "Exito": True, "Mensaje": "Docente actualizado"
        }
        response = self.client.put("/api/docentes/1", json={
            "nombre": "Carlos Actualizado", "apellido": "García",
            "especialidad": "Física", "correo": "carlos.new@uni.edu"
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])

    @patch('src.services.docente_service.DocenteRepository')
    def test_update_docente_no_encontrado(self, mock_repo):
        """Unhappy Path: Actualizar docente inexistente devuelve 400."""
        mock_repo.update.return_value = {
            "Exito": False, "Mensaje": "Docente no encontrado"
        }
        response = self.client.put("/api/docentes/9999", json={
            "nombre": "X", "apellido": "Y", "especialidad": "Z", "correo": "x@y.com"
        })
        self.assertEqual(response.status_code, 400)

    @patch('src.services.docente_service.DocenteRepository')
    def test_delete_docente_exitoso(self, mock_repo):
        """Happy Path: Eliminar docente existente."""
        mock_repo.delete.return_value = True
        response = self.client.delete("/api/docentes/1")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])

    @patch('src.services.docente_service.DocenteRepository')
    def test_manejo_excepcion_repositorio(self, mock_repo):
        """Verifica manejo de excepciones inesperadas."""
        mock_repo.get_all.side_effect = Exception("Error de base de datos")
        client_no_raise = TestClient(app, raise_server_exceptions=False)
        response = client_no_raise.get("/api/docentes")
        self.assertEqual(response.status_code, 500)


@pytest.mark.integration
class TestCarrerasAPI(unittest.TestCase):
    """Pruebas de integración para CRUD de Carreras."""

    def setUp(self):
        self.client = TestClient(app)
        self.carrera_valida = {
            "nombre": "Ingeniería de Sistemas",
            "facultad": "Ingeniería"
        }

    @patch('src.apis.carrera_api.CarreraRepository')
    def test_get_carreras_retorna_lista(self, mock_repo):
        """Happy Path: GET carreras retorna lista con éxito."""
        mock_repo.get_all.return_value = [
            {"carreraid": 1, "nombre": "Ingeniería de Sistemas", "facultad": "Ingeniería", "activo": True}
        ]
        response = self.client.get("/api/carreras/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIsInstance(data["data"], list)

    @patch('src.apis.carrera_api.CarreraRepository')
    def test_get_carreras_lista_vacia(self, mock_repo):
        """Edge Case: GET carreras retorna lista vacía."""
        mock_repo.get_all.return_value = []
        response = self.client.get("/api/carreras/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"], [])

    @patch('src.apis.carrera_api.CarreraRepository')
    def test_get_carrera_por_id_exitoso(self, mock_repo):
        """Happy Path: GET carrera por ID existente."""
        mock_repo.get_by_id.return_value = {
            "carreraid": 1, "nombre": "Ingeniería de Sistemas", "facultad": "Ingeniería", "activo": True
        }
        response = self.client.get("/api/carreras/1")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["data"]["carreraid"], 1)

    @patch('src.apis.carrera_api.CarreraRepository')
    def test_get_carrera_por_id_no_encontrado(self, mock_repo):
        """Unhappy Path: Carrera inexistente devuelve 404."""
        mock_repo.get_by_id.return_value = None
        response = self.client.get("/api/carreras/9999")
        self.assertEqual(response.status_code, 404)
        self.assertIn("no encontrada", response.json()["detail"])

    @patch('src.apis.carrera_api.CarreraRepository')
    def test_create_carrera_exitoso(self, mock_repo):
        """Happy Path: Crear carrera con datos válidos."""
        mock_repo.create.return_value = {
            "Exito": True, "ID": 3, "Mensaje": "Carrera registrada"
        }
        response = self.client.post("/api/carreras/", json=self.carrera_valida)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["data"]["id"], 3)

    @patch('src.apis.carrera_api.CarreraRepository')
    def test_create_carrera_error(self, mock_repo):
        """Unhappy Path: Error al crear carrera."""
        mock_repo.create.return_value = {
            "Exito": False, "Mensaje": "Error al registrar"
        }
        response = self.client.post("/api/carreras/", json=self.carrera_valida)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["success"])

    def test_create_carrera_sin_campos_requeridos(self):
        """Unhappy Path: Datos incompletos devuelven 422."""
        response = self.client.post("/api/carreras/", json={"nombre": "Solo nombre"})
        self.assertEqual(response.status_code, 422)

    @patch('src.apis.carrera_api.CarreraRepository')
    def test_update_carrera_exitoso(self, mock_repo):
        """Happy Path: Actualización de carrera existente."""
        mock_repo.update.return_value = True
        response = self.client.put("/api/carreras/1", json={
            "nombre": "Ingeniería de Software", "facultad": "Ingeniería"
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])

    @patch('src.apis.carrera_api.CarreraRepository')
    def test_update_carrera_error(self, mock_repo):
        """Unhappy Path: Error al actualizar carrera."""
        mock_repo.update.return_value = False
        response = self.client.put("/api/carreras/1", json={
            "nombre": "Nueva", "facultad": "Facultad"
        })
        self.assertEqual(response.status_code, 400)

    @patch('src.apis.carrera_api.CarreraRepository')
    def test_delete_carrera_exitoso(self, mock_repo):
        """Happy Path: Eliminar carrera existente."""
        mock_repo.delete.return_value = True
        response = self.client.delete("/api/carreras/1")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        self.assertIn("eliminada", response.json()["message"])

    @patch('src.apis.carrera_api.CarreraRepository')
    def test_manejo_excepcion_repositorio(self, mock_repo):
        """Verifica manejo de excepciones inesperadas."""
        mock_repo.get_all.side_effect = Exception("Error de base de datos")
        client_no_raise = TestClient(app, raise_server_exceptions=False)
        response = client_no_raise.get("/api/carreras/")
        self.assertEqual(response.status_code, 500)


@pytest.mark.integration
class TestHorariosAPI(unittest.TestCase):
    """Pruebas de integración para endpoints de Horarios."""

    def setUp(self):
        self.client = TestClient(app)
        self.horario_valido = {
            "cursoID": 1,
            "aulaID": 2,
            "diaSemana": "Lunes",
            "horaInicio": "08:00",
            "horaFin": "10:00"
        }

    @patch('src.services.horario_service.HorarioRepository')
    def test_get_horarios_retorna_lista(self, mock_repo):
        """Happy Path: GET horarios retorna lista con éxito."""
        mock_repo.get_all.return_value = [
            {"horarioid": 1, "cursoid": 1, "aulaid": 2, "diasemana": "Lunes",
             "horainicio": "08:00", "horafin": "10:00"}
        ]
        response = self.client.get("/api/horarios")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIsInstance(data["data"], list)

    @patch('src.services.horario_service.HorarioRepository')
    def test_get_horarios_lista_vacia(self, mock_repo):
        """Edge Case: GET horarios retorna lista vacía."""
        mock_repo.get_all.return_value = []
        response = self.client.get("/api/horarios")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"], [])

    @patch('src.services.horario_service.HorarioRepository')
    def test_create_horario_exitoso(self, mock_repo):
        """Happy Path: Crear horario con datos válidos."""
        mock_repo.create.return_value = {
            "Exito": True, "ID": 7, "Mensaje": "Horario registrado"
        }
        response = self.client.post("/api/horarios", json=self.horario_valido)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["data"]["id"], 7)

    @patch('src.services.horario_service.HorarioRepository')
    def test_create_horario_conflicto(self, mock_repo):
        """Unhappy Path: Conflicto de horario devuelve 400."""
        mock_repo.create.return_value = {
            "Exito": False, "Mensaje": "Conflicto de horario con aula"
        }
        response = self.client.post("/api/horarios", json=self.horario_valido)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Conflicto", response.json()["detail"])

    def test_create_horario_sin_campos_requeridos(self):
        """Unhappy Path: Datos incompletos devuelven 422."""
        response = self.client.post("/api/horarios", json={"cursoID": 1})
        self.assertEqual(response.status_code, 422)

    @patch('src.services.horario_service.HorarioRepository')
    def test_generar_horarios_exitoso(self, mock_repo):
        """Happy Path: Generar horarios automáticamente."""
        mock_repo.generar.return_value = {
            "Exito": True, "Mensaje": "Horarios generados",
            "HorariosCreados": 10, "Detalles": []
        }
        response = self.client.post("/api/horarios/generar")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["data"]["horarios_creados"], 10)

    @patch('src.services.horario_service.HorarioRepository')
    def test_generar_horarios_con_parametros(self, mock_repo):
        """Happy Path: Generar horarios con parámetros personalizados."""
        mock_repo.generar.return_value = {
            "Exito": True, "Mensaje": "Horarios generados",
            "HorariosCreados": 5, "Detalles": []
        }
        response = self.client.post("/api/horarios/generar?hora_inicio=10:00&bloques_horas=3&carrera_id=2")
        self.assertEqual(response.status_code, 200)
        mock_repo.generar.assert_called_once_with("10:00", 3, 2)

    @patch('src.services.horario_service.HorarioRepository')
    def test_validar_horarios_exitoso(self, mock_repo):
        """Happy Path: Validar horarios sin conflictos."""
        mock_repo.validar.return_value = {
            "valido": True, "conflictos": [], "mensaje": "Horario válido"
        }
        response = self.client.get("/api/horarios/validar")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIn("valido", data["data"])

    @patch('src.services.horario_service.DashboardRepository')
    def test_dashboard_retorna_metricas(self, mock_repo):
        """Happy Path: GET dashboard retorna métricas."""
        mock_repo.get_metrics.return_value = {
            "totalEstudiantes": 100,
            "totalDocentes": 20,
            "totalCursos": 15,
            "totalAulas": 10,
            "matriculasAprobadas": 50,
            "matriculasRechazadas": 5
        }
        response = self.client.get("/api/dashboard")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIn("totalEstudiantes", data["data"])

    @patch('src.services.horario_service.HorarioRepository')
    def test_manejo_excepcion_horarios(self, mock_repo):
        """Verifica manejo de excepciones en horarios."""
        mock_repo.get_all.side_effect = Exception("Error de base de datos")
        client_no_raise = TestClient(app, raise_server_exceptions=False)
        response = client_no_raise.get("/api/horarios")
        self.assertEqual(response.status_code, 500)


if __name__ == '__main__':
    unittest.main()
