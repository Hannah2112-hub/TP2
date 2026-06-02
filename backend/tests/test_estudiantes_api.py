"""
PRUEBAS DE INTEGRACIÓN - API Estudiantes
Tipo: Integración con TestClient (equivalente a Supertest)
Cobertura: CRUD completo, validación JSON, códigos HTTP, manejo de errores
"""
import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from src.app import app


class TestEstudiantesAPI(unittest.TestCase):
    """Pruebas de integración para los endpoints CRUD de Estudiantes."""

    def setUp(self):
        self.client = TestClient(app)
        self.estudiante_valido = {
            "codigo": "EST-001",
            "nombre": "Pedro",
            "apellido": "Ramirez",
            "correo": "pedro@uni.edu",
            "creditosAcum": 30
        }

    # ─── GET /api/estudiantes ─────────────────────────────────────────────────

    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_get_estudiantes_retorna_lista(self, mock_repo):
        """Happy Path: GET estudiantes retorna lista con éxito."""
        mock_repo.get_all.return_value = [
            {"estudianteid": 1, "nombre": "Juan", "apellido": "Perez", "correo": "jp@uni.edu", "creditosacum": 0}
        ]
        response = self.client.get("/api/estudiantes")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIsInstance(data["data"], list)

    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_get_estudiantes_lista_vacia(self, mock_repo):
        """Edge Case: GET estudiantes retorna lista vacía."""
        mock_repo.get_all.return_value = []
        response = self.client.get("/api/estudiantes")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["data"], [])

    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_get_estudiantes_solo_activos_param(self, mock_repo):
        """Verifica que el parámetro solo_activos se procesa correctamente."""
        mock_repo.get_all.return_value = []
        response = self.client.get("/api/estudiantes?solo_activos=false")
        self.assertEqual(response.status_code, 200)
        mock_repo.get_all.assert_called_once_with(False)

    # ─── POST /api/estudiantes ────────────────────────────────────────────────

    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_create_estudiante_exitoso(self, mock_repo):
        """Happy Path: Crear estudiante con datos válidos."""
        mock_repo.create.return_value = {
            "Exito": True, "ID": 99, "Mensaje": "Estudiante creado con éxito"
        }
        response = self.client.post("/api/estudiantes", json=self.estudiante_valido)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["data"]["id"], 99)

    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_create_estudiante_codigo_duplicado(self, mock_repo):
        """Unhappy Path: Código duplicado devuelve 400."""
        mock_repo.create.return_value = {
            "Exito": False, "Mensaje": "El código ya existe"
        }
        response = self.client.post("/api/estudiantes", json=self.estudiante_valido)
        self.assertEqual(response.status_code, 400)
        self.assertIn("El código ya existe", response.json()["detail"])

    def test_create_estudiante_sin_campos_requeridos(self):
        """Unhappy Path: Datos incompletos devuelven 422."""
        response = self.client.post("/api/estudiantes", json={"nombre": "Solo Nombre"})
        self.assertEqual(response.status_code, 422)

    def test_create_estudiante_correo_invalido(self):
        """Edge Case: Correo con formato inválido."""
        datos_invalidos = self.estudiante_valido.copy()
        datos_invalidos["correo"] = "no-es-un-email"
        response = self.client.post("/api/estudiantes", json=datos_invalidos)
        # FastAPI/Pydantic debería rechazar el correo inválido
        self.assertIn(response.status_code, [400, 422])

    # ─── PUT /api/estudiantes/{id} ────────────────────────────────────────────

    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_update_estudiante_exitoso(self, mock_repo):
        """Happy Path: Actualización de estudiante existente."""
        mock_repo.update.return_value = {
            "Exito": True, "Mensaje": "Estudiante actualizado"
        }
        response = self.client.put("/api/estudiantes/1", json={
            "nombre": "Pedro Nuevo",
            "apellido": "Garcia",
            "correo": "pedro.new@uni.edu",
            "creditosAcum": 60
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])

    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_update_estudiante_no_encontrado(self, mock_repo):
        """Unhappy Path: Actualizar estudiante que no existe devuelve 400."""
        mock_repo.update.return_value = {
            "Exito": False, "Mensaje": "Estudiante no encontrado"
        }
        response = self.client.put("/api/estudiantes/9999", json={
            "nombre": "X", "apellido": "Y", "correo": "x@y.com", "creditosAcum": 0
        })
        self.assertEqual(response.status_code, 400)

    # ─── DELETE /api/estudiantes/{id} ─────────────────────────────────────────

    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_delete_estudiante_exitoso(self, mock_repo):
        """Happy Path: Eliminar estudiante existente."""
        mock_repo.delete.return_value = True
        response = self.client.delete("/api/estudiantes/1")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])

    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_delete_estudiante_retorna_mensaje(self, mock_repo):
        """Verifica que la respuesta de eliminación incluye mensaje de confirmación."""
        mock_repo.delete.return_value = True
        response = self.client.delete("/api/estudiantes/5")
        data = response.json()
        self.assertIn("message", data)

    # ─── Validación JSON ─────────────────────────────────────────────────────

    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_respuesta_json_estructura_correcta(self, mock_repo):
        """Valida la estructura del JSON de respuesta en GET."""
        mock_repo.get_all.return_value = []
        response = self.client.get("/api/estudiantes")
        data = response.json()
        self.assertIn("success", data)
        self.assertIn("data", data)
        self.assertIsInstance(data["success"], bool)

    # ─── Manejo de errores del servidor ──────────────────────────────────────

    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_manejo_excepcion_repositorio(self, mock_repo):
        """Verifica el manejo de excepciones inesperadas del repositorio."""
        mock_repo.get_all.side_effect = Exception("Error de base de datos")
        # Deshabilitar la propagación de excepciones para capturar el 500
        client_no_raise = TestClient(app, raise_server_exceptions=False)
        response = client_no_raise.get("/api/estudiantes")
        # FastAPI devuelve 500 Internal Server Error
        self.assertEqual(response.status_code, 500)


if __name__ == '__main__':
    unittest.main()
