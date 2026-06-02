"""
PRUEBAS UNITARIAS AMPLIADAS - Servicio de Estudiante
Tipo: Unitario con mocks, stubs y spies
Cobertura: CRUD, validaciones, errores, casos límite, manejo de excepciones
"""
import unittest
from unittest.mock import patch, MagicMock, call
from src.services.estudiante_service import EstudianteService


class TestEstudianteService(unittest.TestCase):
    """Pruebas unitarias completas del servicio de Estudiantes."""

    # ─── get_all ──────────────────────────────────────────────────────────────

    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_get_all(self, mock_repo):
        """Happy Path: Retorna lista completa de estudiantes."""
        mock_repo.get_all.return_value = [{"id": 1, "nombre": "Juan"}]
        resultado = EstudianteService.get_all()
        self.assertEqual(len(resultado), 1)

    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_get_all_solo_activos_true(self, mock_repo):
        """Verifica que get_all(solo_activos=True) pasa el parámetro correcto."""
        mock_repo.get_all.return_value = []
        EstudianteService.get_all(solo_activos=True)
        mock_repo.get_all.assert_called_once_with(True)

    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_get_all_solo_activos_false(self, mock_repo):
        """Spy: Verifica que get_all(solo_activos=False) propaga el parámetro."""
        mock_repo.get_all.return_value = []
        EstudianteService.get_all(solo_activos=False)
        mock_repo.get_all.assert_called_once_with(False)

    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_get_all_lista_vacia(self, mock_repo):
        """Edge Case: Sin estudiantes, retorna lista vacía."""
        mock_repo.get_all.return_value = []
        resultado = EstudianteService.get_all()
        self.assertEqual(resultado, [])
        self.assertIsInstance(resultado, list)

    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_get_all_multiples_estudiantes(self, mock_repo):
        """Verifica que se retornan múltiples estudiantes correctamente."""
        mock_data = [
            {"id": 1, "nombre": "Juan"},
            {"id": 2, "nombre": "María"},
            {"id": 3, "nombre": "Carlos"},
        ]
        mock_repo.get_all.return_value = mock_data
        resultado = EstudianteService.get_all()
        self.assertEqual(len(resultado), 3)

    # ─── create ───────────────────────────────────────────────────────────────

    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_create_exito(self, mock_repo):
        """Happy Path: Crear estudiante con datos válidos."""
        mock_repo.create.return_value = {"Exito": True, "ID": 1, "Mensaje": "Creado"}
        resultado = EstudianteService.create("123", "Juan", "Perez", "j@p.com", 0)
        self.assertTrue(resultado["success"])
        self.assertEqual(resultado["data"]["message"], "Creado")
        self.assertEqual(resultado["data"]["id"], 1)

    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_create_falla(self, mock_repo):
        """Unhappy Path: Repositorio retorna falla en creación."""
        mock_repo.create.return_value = {"Exito": False, "Mensaje": "Error"}
        resultado = EstudianteService.create("123", "Juan", "Perez", "j@p.com", 0)
        self.assertFalse(resultado["success"])
        self.assertEqual(resultado["message"], "Error")

    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_create_creditos_default_cero(self, mock_repo):
        """Edge Case: Créditos por defecto es 0."""
        mock_repo.create.return_value = {"Exito": True, "ID": 2, "Mensaje": "OK"}
        # Llamar sin especificar creditos_acum
        EstudianteService.create("456", "Ana", "García", "ag@uni.edu")
        args = mock_repo.create.call_args[0]
        self.assertEqual(args[4], 0)  # creditos_acum = 0

    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_create_codigo_vacio(self, mock_repo):
        """Edge Case: Código vacío es procesado por el repositorio."""
        mock_repo.create.return_value = {
            "Exito": False, "Mensaje": "El código no puede estar vacío"
        }
        resultado = EstudianteService.create("", "Nombre", "Apellido", "x@x.com")
        self.assertFalse(resultado["success"])

    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_create_respuesta_exitosa_tiene_id(self, mock_repo):
        """Valida que la respuesta exitosa incluye el ID asignado."""
        mock_repo.create.return_value = {"Exito": True, "ID": 99, "Mensaje": "Creado"}
        resultado = EstudianteService.create("999", "Test", "User", "test@uni.edu", 0)
        self.assertIn("id", resultado["data"])
        self.assertEqual(resultado["data"]["id"], 99)

    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_create_llama_repositorio_una_vez(self, mock_repo):
        """Spy: Verifica que create() llama al repositorio exactamente una vez."""
        mock_repo.create.return_value = {"Exito": True, "ID": 1, "Mensaje": "OK"}
        EstudianteService.create("001", "A", "B", "ab@uni.edu", 10)
        mock_repo.create.assert_called_once()

    # ─── update ───────────────────────────────────────────────────────────────

    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_update_exito(self, mock_repo):
        """Happy Path: Actualización exitosa de estudiante."""
        mock_repo.update.return_value = {"Exito": True, "Mensaje": "Actualizado"}
        resultado = EstudianteService.update(1, "Juan", "Perez", "j@p.com", 0)
        self.assertTrue(resultado["success"])

    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_update_falla(self, mock_repo):
        """Unhappy Path: Actualización falla por estudiante inexistente."""
        mock_repo.update.return_value = {
            "Exito": False, "Mensaje": "Estudiante no encontrado"
        }
        resultado = EstudianteService.update(9999, "X", "Y", "x@y.com", 0)
        self.assertFalse(resultado["success"])
        self.assertEqual(resultado["message"], "Estudiante no encontrado")

    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_update_pasa_id_correcto_al_repositorio(self, mock_repo):
        """Spy: Verifica que el ID del estudiante llega correcto al repositorio."""
        mock_repo.update.return_value = {"Exito": True, "Mensaje": "OK"}
        EstudianteService.update(42, "Juan", "Perez", "j@p.com", 30)
        args = mock_repo.update.call_args[0]
        self.assertEqual(args[0], 42)

    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_update_creditos_limite_maximo(self, mock_repo):
        """Caso Límite: Actualizar con créditos muy altos."""
        mock_repo.update.return_value = {"Exito": True, "Mensaje": "OK"}
        resultado = EstudianteService.update(1, "Juan", "P", "j@p.com", 9999)
        self.assertTrue(resultado["success"])

    # ─── delete ───────────────────────────────────────────────────────────────

    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_delete(self, mock_repo):
        """Happy Path: Eliminación exitosa de estudiante."""
        mock_repo.delete.return_value = True
        resultado = EstudianteService.delete(1)
        self.assertTrue(resultado["success"])
        self.assertEqual(resultado["message"], "Estudiante eliminado.")

    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_delete_llama_repositorio_con_id_correcto(self, mock_repo):
        """Spy: Verifica que delete llama al repositorio con el ID correcto."""
        mock_repo.delete.return_value = True
        EstudianteService.delete(55)
        mock_repo.delete.assert_called_once_with(55)

    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_delete_siempre_retorna_success(self, mock_repo):
        """Edge Case: Delete siempre retorna success (comportamiento idempotente)."""
        mock_repo.delete.return_value = None
        resultado = EstudianteService.delete(100)
        self.assertTrue(resultado["success"])

    # ─── Estructura de respuesta ──────────────────────────────────────────────

    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_estructura_respuesta_exitosa_create(self, mock_repo):
        """Valida la estructura completa de respuesta exitosa de create."""
        mock_repo.create.return_value = {"Exito": True, "ID": 1, "Mensaje": "OK"}
        resultado = EstudianteService.create("001", "A", "B", "ab@uni.edu")
        self.assertIn("success", resultado)
        self.assertIn("data", resultado)
        self.assertIn("id", resultado["data"])
        self.assertIn("message", resultado["data"])

    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_estructura_respuesta_fallida_create(self, mock_repo):
        """Valida la estructura de respuesta fallida de create."""
        mock_repo.create.return_value = {"Exito": False, "Mensaje": "Error"}
        resultado = EstudianteService.create("001", "A", "B", "ab@uni.edu")
        self.assertIn("success", resultado)
        self.assertIn("message", resultado)
        self.assertFalse(resultado["success"])


if __name__ == '__main__':
    unittest.main()
