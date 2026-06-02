"""
PRUEBAS DE INTEGRACIÓN COMPLETAS - API de Matrículas
Tipo: Integración con TestClient (equivalente a Supertest)
Cobertura: CRUD matrículas, estados, validaciones, acceso no autorizado
"""
import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from src.app import app


class TestMatriculasAPI(unittest.TestCase):
    """Pruebas de integración para los endpoints de Matrículas."""

    def setUp(self):
        self.client = TestClient(app)

    # ─── GET /api/matriculas ──────────────────────────────────────────────────

    @patch('src.services.matricula_service.MatriculaRepository')
    def test_get_matriculas_retorna_lista(self, mock_repo):
        """Happy Path: GET matriculas retorna lista correctamente."""
        mock_repo.get_all.return_value = [
            {
                "matriculaid": 1,
                "estudianteid": 1,
                "cursoid": 2,
                "estado": "Pendiente",
                "nombreestudiante": "Juan Perez",
                "nombrecurso": "Matemáticas I"
            }
        ]
        response = self.client.get("/api/matriculas")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIsInstance(data["data"], list)
        self.assertEqual(len(data["data"]), 1)

    @patch('src.services.matricula_service.MatriculaRepository')
    def test_get_matriculas_lista_vacia(self, mock_repo):
        """Edge Case: Sin matrículas registradas."""
        mock_repo.get_all.return_value = []
        response = self.client.get("/api/matriculas")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"], [])

    # ─── POST /api/matriculas ─────────────────────────────────────────────────

    @patch('src.services.matricula_service.MatriculaRepository')
    def test_create_matricula_exitosa(self, mock_repo):
        """Happy Path: Crear matrícula válida."""
        mock_repo.create.return_value = {
            "Exito": True, "ID": 10, "Mensaje": "Matrícula registrada exitosamente"
        }
        response = self.client.post("/api/matriculas", json={
            "estudianteID": 1,
            "cursoID": 2
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])

    @patch('src.services.matricula_service.MatriculaRepository')
    def test_create_matricula_cupos_llenos(self, mock_repo):
        """Unhappy Path: No hay cupos disponibles en el curso."""
        mock_repo.create.return_value = {
            "Exito": False, "Mensaje": "No hay cupos disponibles en este curso"
        }
        response = self.client.post("/api/matriculas", json={
            "estudianteID": 1,
            "cursoID": 5
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("cupos", response.json()["detail"])

    @patch('src.services.matricula_service.MatriculaRepository')
    def test_create_matricula_duplicada(self, mock_repo):
        """Unhappy Path: Estudiante ya matriculado en ese curso."""
        mock_repo.create.return_value = {
            "Exito": False, "Mensaje": "El estudiante ya está matriculado en este curso"
        }
        response = self.client.post("/api/matriculas", json={
            "estudianteID": 1,
            "cursoID": 2
        })
        self.assertEqual(response.status_code, 400)

    @patch('src.services.matricula_service.MatriculaRepository')
    def test_create_matricula_sin_prerequisito(self, mock_repo):
        """Unhappy Path: Estudiante no cumple el prerequisito."""
        mock_repo.create.return_value = {
            "Exito": False, "Mensaje": "El estudiante no cumple los requisitos de créditos"
        }
        response = self.client.post("/api/matriculas", json={
            "estudianteID": 2,
            "cursoID": 7
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("créditos", response.json()["detail"])

    def test_create_matricula_body_invalido(self):
        """Unhappy Path: Body sin campos requeridos devuelve 422."""
        response = self.client.post("/api/matriculas", json={})
        self.assertEqual(response.status_code, 422)

    # ─── PATCH /api/matriculas/{id}/estado ────────────────────────────────────

    @patch('src.services.matricula_service.MatriculaRepository')
    def test_update_estado_aprobada(self, mock_repo):
        """Happy Path: Cambiar estado a 'Aprobada'."""
        mock_repo.update_estado.return_value = {
            "Exito": True, "Mensaje": "Estado actualizado"
        }
        response = self.client.put("/api/matriculas/1/estado?estado=Aprobada")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])

    @patch('src.services.matricula_service.MatriculaRepository')
    def test_update_estado_rechazada(self, mock_repo):
        """Happy Path: Cambiar estado a 'Rechazada'."""
        mock_repo.update_estado.return_value = {
            "Exito": True, "Mensaje": "Estado actualizado"
        }
        response = self.client.put("/api/matriculas/1/estado?estado=Rechazada")
        self.assertEqual(response.status_code, 200)

    def test_update_estado_invalido(self):
        """Unhappy Path: Estado no válido devuelve 400 (lógica de negocio)."""
        response = self.client.put("/api/matriculas/1/estado?estado=INVALIDO")
        self.assertEqual(response.status_code, 400)

    def test_update_estado_pendiente(self):
        """Verifica que 'Pendiente' es un estado válido."""
        with patch('src.services.matricula_service.MatriculaRepository') as mock_repo:
            mock_repo.update_estado.return_value = {"Exito": True, "Mensaje": "OK"}
            response = self.client.put("/api/matriculas/1/estado?estado=Pendiente")
            self.assertEqual(response.status_code, 200)

    def test_update_estado_retirada(self):
        """Verifica que 'Retirada' es un estado válido."""
        with patch('src.services.matricula_service.MatriculaRepository') as mock_repo:
            mock_repo.update_estado.return_value = {"Exito": True, "Mensaje": "OK"}
            response = self.client.put("/api/matriculas/1/estado?estado=Retirada")
            self.assertEqual(response.status_code, 200)

    # ─── Validación de respuestas JSON ────────────────────────────────────────

    @patch('src.services.matricula_service.MatriculaRepository')
    def test_respuesta_json_tiene_campos_correctos(self, mock_repo):
        """Valida la estructura del JSON de respuesta."""
        mock_repo.get_all.return_value = []
        response = self.client.get("/api/matriculas")
        data = response.json()
        self.assertIn("success", data)
        self.assertIn("data", data)
        self.assertIsInstance(data["success"], bool)
        self.assertIsInstance(data["data"], list)

    # ─── Manejo de errores del servidor ──────────────────────────────────────

    @patch('src.services.matricula_service.MatriculaRepository')
    def test_manejo_error_interno(self, mock_repo):
        """Simula error interno del servidor."""
        mock_repo.get_all.side_effect = Exception("Error inesperado de BD")
        # Deshabilitar la propagación de excepciones para capturar el 500
        client_no_raise = TestClient(app, raise_server_exceptions=False)
        response = client_no_raise.get("/api/matriculas")
        self.assertEqual(response.status_code, 500)

    # ─── Content-Type ─────────────────────────────────────────────────────────

    @patch('src.services.matricula_service.MatriculaRepository')
    def test_content_type_es_json(self, mock_repo):
        """Verifica que la respuesta tiene Content-Type application/json."""
        mock_repo.get_all.return_value = []
        response = self.client.get("/api/matriculas")
        self.assertIn("application/json", response.headers["content-type"])


if __name__ == '__main__':
    unittest.main()
