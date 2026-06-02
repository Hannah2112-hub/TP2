"""
PRUEBAS UNITARIAS AMPLIADAS - Servicio de Aula
Tipo: Unitario con mocks
Cobertura: CRUD, validación, casos límite, manejo de excepciones
"""
import unittest
from unittest.mock import patch, MagicMock, call
from src.services.aula_service import AulaService


class TestAulaService(unittest.TestCase):
    """Pruebas unitarias completas del servicio de Aulas."""

    # ─── get_all ──────────────────────────────────────────────────────────────

    @patch('src.services.aula_service.AulaRepository')
    def test_get_all_retorna_lista_aulas(self, mock_repo):
        """Happy Path: get_all devuelve la lista del repositorio."""
        mock_data = [
            {"aulaid": 1, "nombre": "A-101", "capacidad": 30},
            {"aulaid": 2, "nombre": "A-102", "capacidad": 40},
        ]
        mock_repo.get_all.return_value = mock_data
        resultado = AulaService.get_all()
        self.assertEqual(resultado, mock_data)
        mock_repo.get_all.assert_called_once()

    @patch('src.services.aula_service.AulaRepository')
    def test_get_all_lista_vacia(self, mock_repo):
        """Edge Case: Sin aulas registradas retorna lista vacía."""
        mock_repo.get_all.return_value = []
        resultado = AulaService.get_all()
        self.assertEqual(resultado, [])
        self.assertIsInstance(resultado, list)

    # ─── create ───────────────────────────────────────────────────────────────

    @patch('src.services.aula_service.AulaRepository')
    def test_create_exitoso(self, mock_repo):
        """Happy Path: Crear aula con todos los datos válidos."""
        mock_repo.create.return_value = {
            "Exito": True, "ID": 10, "Mensaje": "Aula creada exitosamente"
        }
        resultado = AulaService.create("Laboratorio-01", 25, "Edificio C", "Proyector, PCs")
        self.assertTrue(resultado["success"])
        self.assertEqual(resultado["data"]["id"], 10)
        self.assertEqual(resultado["data"]["message"], "Aula creada exitosamente")

    @patch('src.services.aula_service.AulaRepository')
    def test_create_sin_equipamiento(self, mock_repo):
        """Edge Case: Crear aula sin equipamiento (campo opcional)."""
        mock_repo.create.return_value = {
            "Exito": True, "ID": 11, "Mensaje": "Aula creada"
        }
        resultado = AulaService.create("Aula-202", 50, "Edificio A")
        self.assertTrue(resultado["success"])
        mock_repo.create.assert_called_once_with("Aula-202", 50, "Edificio A", None)

    @patch('src.services.aula_service.AulaRepository')
    def test_create_falla_nombre_duplicado(self, mock_repo):
        """Unhappy Path: Nombre duplicado devuelve failure."""
        mock_repo.create.return_value = {
            "Exito": False, "Mensaje": "El nombre del aula ya existe"
        }
        resultado = AulaService.create("A-101", 30, "Edificio A")
        self.assertFalse(resultado["success"])
        self.assertEqual(resultado["message"], "El nombre del aula ya existe")
        self.assertNotIn("data", resultado)

    @patch('src.services.aula_service.AulaRepository')
    def test_create_capacidad_cero(self, mock_repo):
        """Edge Case (Caso Límite): Capacidad = 0 es procesada por el repositorio."""
        mock_repo.create.return_value = {
            "Exito": False, "Mensaje": "Capacidad inválida"
        }
        resultado = AulaService.create("Aula-Mini", 0, "Edificio B")
        self.assertFalse(resultado["success"])

    @patch('src.services.aula_service.AulaRepository')
    def test_create_llama_repositorio_con_parametros_correctos(self, mock_repo):
        """Verifica que el servicio pasa los parámetros exactos al repositorio."""
        mock_repo.create.return_value = {"Exito": True, "ID": 1, "Mensaje": "OK"}
        AulaService.create("Lab-Cómputo", 20, "Edificio D", "Pizarra inteligente")
        mock_repo.create.assert_called_once_with(
            "Lab-Cómputo", 20, "Edificio D", "Pizarra inteligente"
        )

    # ─── update ───────────────────────────────────────────────────────────────

    @patch('src.services.aula_service.AulaRepository')
    def test_update_exitoso(self, mock_repo):
        """Happy Path: Actualización de aula retorna success."""
        mock_repo.update.return_value = {
            "Exito": True, "Mensaje": "Aula actualizada correctamente"
        }
        resultado = AulaService.update(1, "A-101-Nuevo", 35, "Edificio A", "Proyector")
        self.assertTrue(resultado["success"])
        self.assertEqual(resultado["data"]["message"], "Aula actualizada correctamente")

    @patch('src.services.aula_service.AulaRepository')
    def test_update_aula_no_existe(self, mock_repo):
        """Unhappy Path: Actualizar aula que no existe devuelve failure."""
        mock_repo.update.return_value = {
            "Exito": False, "Mensaje": "Aula no encontrada"
        }
        resultado = AulaService.update(9999, "X", 10, "Y", None)
        self.assertFalse(resultado["success"])
        self.assertEqual(resultado["message"], "Aula no encontrada")

    @patch('src.services.aula_service.AulaRepository')
    def test_update_llama_repositorio_con_id_correcto(self, mock_repo):
        """Verifica que el update llama al repositorio con el ID correcto (spy)."""
        mock_repo.update.return_value = {"Exito": True, "Mensaje": "OK"}
        AulaService.update(42, "Nueva", 30, "Edificio E", None)
        args = mock_repo.update.call_args[0]
        self.assertEqual(args[0], 42)  # Primer argumento: aula_id

    # ─── delete ───────────────────────────────────────────────────────────────

    @patch('src.services.aula_service.AulaRepository')
    def test_delete_exitoso(self, mock_repo):
        """Happy Path: Eliminar aula devuelve success True."""
        mock_repo.delete.return_value = True
        resultado = AulaService.delete(1)
        self.assertTrue(resultado["success"])
        self.assertEqual(resultado["message"], "Aula eliminada.")

    @patch('src.services.aula_service.AulaRepository')
    def test_delete_llama_repositorio_una_vez(self, mock_repo):
        """Verifica que delete() llama al repositorio exactamente una vez."""
        mock_repo.delete.return_value = True
        AulaService.delete(7)
        mock_repo.delete.assert_called_once_with(7)

    @patch('src.services.aula_service.AulaRepository')
    def test_delete_siempre_retorna_success(self, mock_repo):
        """Caso límite: Delete siempre reporta éxito (idempotente)."""
        mock_repo.delete.return_value = None
        resultado = AulaService.delete(999)
        self.assertTrue(resultado["success"])

    # ─── Manejo de excepciones ────────────────────────────────────────────────

    @patch('src.services.aula_service.AulaRepository')
    def test_create_maneja_excepcion_repositorio(self, mock_repo):
        """Verifica manejo de excepción cuando el repositorio falla."""
        mock_repo.create.side_effect = Exception("Error de conexión a BD")
        with self.assertRaises(Exception):
            AulaService.create("Aula", 20, "Edif")

    # ─── Estructura de respuesta ──────────────────────────────────────────────

    @patch('src.services.aula_service.AulaRepository')
    def test_create_respuesta_tiene_campos_requeridos(self, mock_repo):
        """Valida que la respuesta exitosa tiene los campos 'success' y 'data'."""
        mock_repo.create.return_value = {"Exito": True, "ID": 5, "Mensaje": "OK"}
        resultado = AulaService.create("Aula-Test", 25, "Edif-A")
        self.assertIn("success", resultado)
        self.assertIn("data", resultado)
        self.assertIn("id", resultado["data"])
        self.assertIn("message", resultado["data"])

    @patch('src.services.aula_service.AulaRepository')
    def test_create_falla_respuesta_tiene_message(self, mock_repo):
        """Valida que la respuesta fallida tiene los campos 'success' y 'message'."""
        mock_repo.create.return_value = {"Exito": False, "Mensaje": "Error"}
        resultado = AulaService.create("X", 10, "Y")
        self.assertIn("success", resultado)
        self.assertIn("message", resultado)
        self.assertNotIn("data", resultado)


if __name__ == '__main__':
    unittest.main()
