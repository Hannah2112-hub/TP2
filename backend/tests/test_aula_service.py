import unittest
from unittest.mock import patch
from src.services.aula_service import AulaService

class TestAulaService(unittest.TestCase):
    @patch('src.services.aula_service.AulaRepository')
    def test_get_all(self, mock_repo):
        mock_repo.get_all.return_value = [{"id": 1, "nombre": "101"}]
        resultado = AulaService.get_all()
        self.assertEqual(len(resultado), 1)

    @patch('src.services.aula_service.AulaRepository')
    def test_create_exito(self, mock_repo):
        mock_repo.create.return_value = {"Exito": True, "ID": 1, "Mensaje": "Creado"}
        resultado = AulaService.create("101", "Aula 101", 30, "Proyector")
        self.assertTrue(resultado["success"])

    @patch('src.services.aula_service.AulaRepository')
    def test_create_falla(self, mock_repo):
        mock_repo.create.return_value = {"Exito": False, "Mensaje": "Error"}
        resultado = AulaService.create("101", "Aula 101", 30, "Proyector")
        self.assertFalse(resultado["success"])

    @patch('src.services.aula_service.AulaRepository')
    def test_update_exito(self, mock_repo):
        mock_repo.update.return_value = {"Exito": True, "Mensaje": "Actualizado"}
        resultado = AulaService.update(1, "101", "Aula 101", 30, "Proyector")
        self.assertTrue(resultado["success"])
        
    @patch('src.services.aula_service.AulaRepository')
    def test_delete(self, mock_repo):
        mock_repo.delete.return_value = True
        resultado = AulaService.delete(1)
        self.assertTrue(resultado["success"])
