import unittest
from unittest.mock import patch
from src.services.matricula_service import MatriculaService

class TestMatriculaService(unittest.TestCase):
    @patch('src.services.matricula_service.MatriculaRepository')
    def test_update_estado_valido_retorna_exito(self, mock_repo):
        # Configurar el mock para simular éxito en la base de datos
        mock_repo.update_estado.return_value = {"Exito": True, "Mensaje": "Actualizado correctamente"}
        
        # Ejecutar
        resultado = MatriculaService.update_estado(1, "Aprobada")
        
        # Validar
        self.assertTrue(resultado["success"])
        self.assertEqual(resultado["message"], "Actualizado correctamente")
        mock_repo.update_estado.assert_called_once_with(1, "Aprobada")

    @patch('src.services.matricula_service.MatriculaRepository')
    def test_update_estado_invalido_retorna_error(self, mock_repo):
        # Ejecutar con un estado que NO está permitido
        resultado = MatriculaService.update_estado(1, "EstadoInventado")
        
        # Validar
        self.assertFalse(resultado["success"])
        self.assertIn("Estado inválido", resultado["message"])
        # El repositorio NO debe haber sido llamado
        mock_repo.update_estado.assert_not_called()

if __name__ == '__main__':
    unittest.main()
