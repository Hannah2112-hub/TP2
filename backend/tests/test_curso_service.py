"""
PRUEBAS UNITARIAS AMPLIADAS - Servicio de Curso
Tipo: Unitario con mocks y stubs
Cobertura: CRUD, prerequisitos, validaciones, casos límite
"""
import unittest
from unittest.mock import patch, MagicMock, call
from src.services.curso_service import CursoService


class TestCursoService(unittest.TestCase):
    """Pruebas unitarias completas del servicio de Cursos."""

    # ─── get_all ──────────────────────────────────────────────────────────────

    @patch('src.services.curso_service.CursoRepository')
    def test_get_all_retorna_cursos(self, mock_repo):
        """Happy Path: Retorna todos los cursos del repositorio."""
        mock_data = [
            {"cursoid": 1, "codigo": "MAT-101", "nombre": "Matemáticas I", "creditosreq": 0},
            {"cursoid": 2, "codigo": "FIS-101", "nombre": "Física I", "creditosreq": 3},
        ]
        mock_repo.get_all.return_value = mock_data
        resultado = CursoService.get_all()
        self.assertEqual(len(resultado), 2)
        self.assertEqual(resultado[0]["codigo"], "MAT-101")

    @patch('src.services.curso_service.CursoRepository')
    def test_get_all_sin_cursos(self, mock_repo):
        """Edge Case: Sin cursos, retorna lista vacía."""
        mock_repo.get_all.return_value = []
        resultado = CursoService.get_all()
        self.assertEqual(resultado, [])

    # ─── create ───────────────────────────────────────────────────────────────

    @patch('src.services.curso_service.CursoRepository')
    def test_create_exitoso(self, mock_repo):
        """Happy Path: Crear curso con todos los datos válidos."""
        mock_repo.create.return_value = {
            "Exito": True, "ID": 5, "Mensaje": "Curso creado correctamente"
        }
        resultado = CursoService.create(
            codigo="INF-201",
            nombre="Programación II",
            creditos_req=6,
            prerequisito_id=1,
            docente_id=3,
            cupos=30,
            carrera_id=2
        )
        self.assertTrue(resultado["success"])
        self.assertEqual(resultado["data"]["id"], 5)
        self.assertEqual(resultado["data"]["message"], "Curso creado correctamente")

    @patch('src.services.curso_service.CursoRepository')
    def test_create_sin_prerequisito(self, mock_repo):
        """Edge Case: Curso sin prerequisito (None es válido)."""
        mock_repo.create.return_value = {
            "Exito": True, "ID": 6, "Mensaje": "Creado"
        }
        resultado = CursoService.create("MAT-100", "Cálculo", 0, None, 1, 40)
        self.assertTrue(resultado["success"])
        mock_repo.create.assert_called_once_with("MAT-100", "Cálculo", 0, None, 1, 40, None)

    @patch('src.services.curso_service.CursoRepository')
    def test_create_falla_codigo_duplicado(self, mock_repo):
        """Unhappy Path: Código de curso ya existe."""
        mock_repo.create.return_value = {
            "Exito": False, "Mensaje": "El código del curso ya existe en la base de datos"
        }
        resultado = CursoService.create("MAT-101", "Matemáticas", 0, None, 1, 30)
        self.assertFalse(resultado["success"])
        self.assertIn("ya existe", resultado["message"])

    @patch('src.services.curso_service.CursoRepository')
    def test_create_cupos_limite_cero(self, mock_repo):
        """Caso Límite: Cupos = 0."""
        mock_repo.create.return_value = {
            "Exito": False, "Mensaje": "Los cupos deben ser mayores a 0"
        }
        resultado = CursoService.create("TST-001", "Test", 0, None, 1, 0)
        self.assertFalse(resultado["success"])

    @patch('src.services.curso_service.CursoRepository')
    def test_create_cupos_maximo(self, mock_repo):
        """Caso Límite: Cupos con valor máximo alto."""
        mock_repo.create.return_value = {
            "Exito": True, "ID": 7, "Mensaje": "Creado"
        }
        resultado = CursoService.create("TST-002", "Test Grande", 0, None, 1, 500)
        self.assertTrue(resultado["success"])

    @patch('src.services.curso_service.CursoRepository')
    def test_create_verifica_parametros_al_repositorio(self, mock_repo):
        """Spy: Verifica que los parámetros llegan correctamente al repositorio."""
        mock_repo.create.return_value = {"Exito": True, "ID": 1, "Mensaje": "OK"}
        CursoService.create("C-001", "Curso", 3, 2, 5, 25, 1)
        mock_repo.create.assert_called_once_with("C-001", "Curso", 3, 2, 5, 25, 1)

    # ─── update ───────────────────────────────────────────────────────────────

    @patch('src.services.curso_service.CursoRepository')
    def test_update_exitoso(self, mock_repo):
        """Happy Path: Actualización correcta de curso."""
        mock_repo.update.return_value = {
            "Exito": True, "Mensaje": "Curso actualizado"
        }
        resultado = CursoService.update(1, "INF-202", "Programación III", 9, 2, 4, 35)
        self.assertTrue(resultado["success"])
        self.assertEqual(resultado["data"]["message"], "Curso actualizado")

    @patch('src.services.curso_service.CursoRepository')
    def test_update_curso_inexistente(self, mock_repo):
        """Unhappy Path: Curso no encontrado."""
        mock_repo.update.return_value = {
            "Exito": False, "Mensaje": "Curso no encontrado"
        }
        resultado = CursoService.update(9999, "X", "Y", 0, None, 1, 30)
        self.assertFalse(resultado["success"])
        self.assertEqual(resultado["message"], "Curso no encontrado")

    @patch('src.services.curso_service.CursoRepository')
    def test_update_prerequisito_circular(self, mock_repo):
        """Edge Case: Prerequisito circular (el mismo curso)."""
        mock_repo.update.return_value = {
            "Exito": False, "Mensaje": "El prerequisito no puede ser el mismo curso"
        }
        resultado = CursoService.update(5, "C-005", "Circular", 3, 5, 1, 30)
        self.assertFalse(resultado["success"])

    # ─── delete ───────────────────────────────────────────────────────────────

    @patch('src.services.curso_service.CursoRepository')
    def test_delete_exitoso(self, mock_repo):
        """Happy Path: Eliminar curso exitosamente."""
        mock_repo.delete.return_value = True
        resultado = CursoService.delete(1)
        self.assertTrue(resultado["success"])
        self.assertEqual(resultado["message"], "Curso eliminado.")

    @patch('src.services.curso_service.CursoRepository')
    def test_delete_llama_repositorio_id_correcto(self, mock_repo):
        """Spy: Verifica que se llama con el ID correcto."""
        mock_repo.delete.return_value = True
        CursoService.delete(15)
        mock_repo.delete.assert_called_once_with(15)

    @patch('src.services.curso_service.CursoRepository')
    def test_delete_no_retorna_data(self, mock_repo):
        """Verifica que la respuesta de delete no incluye campo 'data'."""
        mock_repo.delete.return_value = True
        resultado = CursoService.delete(1)
        self.assertNotIn("data", resultado)

    # ─── Estructura de respuesta ──────────────────────────────────────────────

    @patch('src.services.curso_service.CursoRepository')
    def test_create_respuesta_exitosa_estructura(self, mock_repo):
        """Valida la estructura completa de la respuesta exitosa."""
        mock_repo.create.return_value = {"Exito": True, "ID": 1, "Mensaje": "OK"}
        resultado = CursoService.create("X", "Y", 0, None, 1, 30)
        self.assertIn("success", resultado)
        self.assertIn("data", resultado)
        self.assertIn("id", resultado["data"])
        self.assertIn("message", resultado["data"])
        self.assertIsInstance(resultado["success"], bool)

    @patch('src.services.curso_service.CursoRepository')
    def test_create_respuesta_fallida_estructura(self, mock_repo):
        """Valida la estructura de la respuesta fallida."""
        mock_repo.create.return_value = {"Exito": False, "Mensaje": "Error"}
        resultado = CursoService.create("X", "Y", 0, None, 1, 30)
        self.assertIn("success", resultado)
        self.assertIn("message", resultado)
        self.assertFalse(resultado["success"])


if __name__ == '__main__':
    unittest.main()
