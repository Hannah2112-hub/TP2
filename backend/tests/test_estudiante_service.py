import unittest
from unittest.mock import patch
from src.services.estudiante_service import EstudianteService

class TestEstudianteService(unittest.TestCase):
    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_get_all(self, mock_repo):
        mock_repo.get_all.return_value = [{"id": 1, "nombre": "Juan"}]
        resultado = EstudianteService.get_all()
        self.assertEqual(len(resultado), 1)

    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_create_exito(self, mock_repo):
        mock_repo.create.return_value = {"Exito": True, "ID": 1, "Mensaje": "Creado"}
        resultado = EstudianteService.create("123", "Juan", "Perez", "j@p.com", 0)
        self.assertTrue(resultado["success"])
        self.assertEqual(resultado["data"]["message"], "Creado")

    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_create_falla(self, mock_repo):
        mock_repo.create.return_value = {"Exito": False, "Mensaje": "Error"}
        resultado = EstudianteService.create("123", "Juan", "Perez", "j@p.com", 0)
        self.assertFalse(resultado["success"])
        self.assertEqual(resultado["message"], "Error")

    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_update_exito(self, mock_repo):
        mock_repo.update.return_value = {"Exito": True, "Mensaje": "Actualizado"}
        resultado = EstudianteService.update(1, "Juan", "Perez", "j@p.com", 0)
        self.assertTrue(resultado["success"])
        
    @patch('src.services.estudiante_service.EstudianteRepository')
    def test_delete(self, mock_repo):
        mock_repo.delete.return_value = True
        resultado = EstudianteService.delete(1)
        self.assertTrue(resultado["success"])
