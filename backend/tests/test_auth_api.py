"""
PRUEBAS DE INTEGRACIÓN - API Auth
Tipo: Integración (Supertest equivalente con TestClient de FastAPI)
Cobertura: Autenticación, autorización, manejo de errores HTTP

NOTA: El router de auth_api no está registrado en el router principal de la app.
      Por ello se crea una mini-app de prueba que lo incluye con el prefijo /api.
"""
import unittest
from unittest.mock import patch, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.apis.auth_api import router as auth_router
from src.app import app as main_app

# Mini-app de prueba que registra el router de auth bajo /api
_test_app = FastAPI()
_test_app.include_router(auth_router, prefix="/api")


class TestAuthAPI(unittest.TestCase):
    """Pruebas de integración para los endpoints de autenticación."""

    def setUp(self):
        self.client = TestClient(_test_app)
        self.main_client = TestClient(main_app)

    # ─── 1. Login Admin ───────────────────────────────────────────────────────

    def test_login_admin_credenciales_correctas(self):
        """Happy Path: Login de admin con credenciales válidas."""
        response = self.client.post("/api/auth/login", json={
            "email": "admin@uni.edu",
            "password": "admin123",
            "tipo": "admin"
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["data"]["tipo"], "admin")
        self.assertEqual(data["data"]["nombre"], "Administrador")

    def test_login_admin_password_incorrecta(self):
        """Unhappy Path: Login admin con contraseña incorrecta devuelve 401."""
        response = self.client.post("/api/auth/login", json={
            "email": "admin@uni.edu",
            "password": "WRONG_PASSWORD",
            "tipo": "admin"
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn("Credenciales incorrectas", response.json()["detail"])

    def test_login_admin_email_incorrecto(self):
        """Unhappy Path: Email incorrecto para admin devuelve 401."""
        response = self.client.post("/api/auth/login", json={
            "email": "otro@email.com",
            "password": "admin123",
            "tipo": "admin"
        })
        self.assertEqual(response.status_code, 401)

    # ─── 2. Login Docente ─────────────────────────────────────────────────────

    @patch('src.apis.auth_api.execute_query')
    def test_login_docente_encontrado(self, mock_query):
        """Happy Path: Login docente existente en BD."""
        mock_query.return_value = [{
            "docenteid": 5,
            "nombre": "Carlos",
            "apellido": "López",
            "correo": "carlos@uni.edu"
        }]
        response = self.client.post("/api/auth/login", json={
            "email": "carlos@uni.edu",
            "password": "cualquier",
            "tipo": "docente"
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["data"]["tipo"], "docente")
        self.assertEqual(data["data"]["id"], 5)
        self.assertIn("Carlos", data["data"]["nombre"])

    @patch('src.apis.auth_api.execute_query')
    def test_login_docente_no_encontrado(self, mock_query):
        """Unhappy Path: Docente no registrado devuelve 401."""
        mock_query.return_value = []
        response = self.client.post("/api/auth/login", json={
            "email": "noexiste@uni.edu",
            "password": "pass",
            "tipo": "docente"
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn("Docente no encontrado", response.json()["detail"])

    # ─── 3. Login Estudiante ──────────────────────────────────────────────────

    @patch('src.apis.auth_api.execute_query')
    def test_login_estudiante_encontrado(self, mock_query):
        """Happy Path: Login estudiante existente."""
        mock_query.return_value = [{
            "estudianteid": 10,
            "nombre": "Ana",
            "apellido": "García",
            "correo": "ana@uni.edu"
        }]
        response = self.client.post("/api/auth/login", json={
            "email": "ana@uni.edu",
            "password": "pass",
            "tipo": "estudiante"
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["data"]["tipo"], "estudiante")
        self.assertEqual(data["data"]["id"], 10)

    @patch('src.apis.auth_api.execute_query')
    def test_login_estudiante_no_encontrado(self, mock_query):
        """Unhappy Path: Estudiante no registrado devuelve 401."""
        mock_query.return_value = []
        response = self.client.post("/api/auth/login", json={
            "email": "noexiste@uni.edu",
            "password": "pass",
            "tipo": "estudiante"
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn("Estudiante no encontrado", response.json()["detail"])

    # ─── 4. Tipo inválido ─────────────────────────────────────────────────────

    def test_login_tipo_invalido(self):
        """Unhappy Path: Tipo de usuario inexistente devuelve 400."""
        response = self.client.post("/api/auth/login", json={
            "email": "test@test.com",
            "password": "pass",
            "tipo": "superuser"
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Tipo de usuario inválido", response.json()["detail"])

    # ─── 5. Validaciones de formato ───────────────────────────────────────────

    def test_login_body_vacio(self):
        """Unhappy Path: Body vacío devuelve 422 (Unprocessable Entity)."""
        response = self.client.post("/api/auth/login", json={})
        self.assertEqual(response.status_code, 422)

    def test_login_falta_campo_tipo(self):
        """Unhappy Path: Campo 'tipo' ausente devuelve error de validación."""
        response = self.client.post("/api/auth/login", json={
            "email": "admin@uni.edu",
            "password": "admin123"
        })
        self.assertEqual(response.status_code, 422)

    def test_login_respuesta_json_valida(self):
        """Valida que la respuesta JSON tiene estructura correcta."""
        response = self.client.post("/api/auth/login", json={
            "email": "admin@uni.edu",
            "password": "admin123",
            "tipo": "admin"
        })
        data = response.json()
        self.assertIn("success", data)
        self.assertIn("data", data)
        self.assertIn("nombre", data["data"])
        self.assertIn("tipo", data["data"])
        self.assertIn("id", data["data"])

    # ─── 6. Headers HTTP ─────────────────────────────────────────────────────

    def test_login_content_type_json(self):
        """Verifica que la respuesta es application/json."""
        response = self.client.post("/api/auth/login", json={
            "email": "admin@uni.edu",
            "password": "admin123",
            "tipo": "admin"
        })
        self.assertIn("application/json", response.headers["content-type"])

    def test_health_check_disponible(self):
        """Verifica que el endpoint /health está disponible."""
        response = self.main_client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "healthy")

    def test_root_endpoint(self):
        """Verifica que el endpoint raíz responde correctamente."""
        response = self.main_client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())


if __name__ == '__main__':
    unittest.main()
