import unittest
from unittest.mock import patch
from src.services.curso_service import CursoService

class TestCursoService(unittest.TestCase):
    @patch('src.services.curso_service.CursoRepository')
    def test_get_all(self, mock_repo):
        mock_repo.get_all.return_value = [{"id": 1, "nombre": "Mate"}]
        resultado = CursoService.get_all()
        self.assertEqual(len(resultado), 1)

    @patch('src.services.curso_service.CursoRepository')
    def test_create_exito(self, mock_repo):
        mock_repo.create.return_value = {"Exito": True, "ID": 1, "Mensaje": "Creado"}
        resultado = CursoService.create("MAT101", "Mate", 4, None, 1, 30)
        self.assertTrue(resultado["success"])

    @patch('src.services.curso_service.CursoRepository')
    def test_create_falla(self, mock_repo):
        mock_repo.create.return_value = {"Exito": False, "Mensaje": "Error"}
        resultado = CursoService.create("MAT101", "Mate", 4, None, 1, 30)
        self.assertFalse(resultado["success"])

    @patch('src.services.curso_service.CursoRepository')
    def test_update_exito(self, mock_repo):
        mock_repo.update.return_value = {"Exito": True, "Mensaje": "Actualizado"}
        resultado = CursoService.update(1, "MAT101", "Mate", 4, None, 1, 30)
        self.assertTrue(resultado["success"])
        
    @patch('src.services.curso_service.CursoRepository')
    def test_delete(self, mock_repo):
        mock_repo.delete.return_value = True
        resultado = CursoService.delete(1)
        self.assertTrue(resultado["success"])
