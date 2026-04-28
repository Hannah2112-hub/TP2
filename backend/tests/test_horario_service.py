import unittest
from unittest.mock import patch
from src.services.horario_service import HorarioService

class TestHorarioService(unittest.TestCase):
    @patch('src.services.horario_service.HorarioRepository')
    def test_generar_exitoso(self, mock_repo):
        # Simulamos respuesta exitosa del repositorio
        mock_repo.generar.return_value = {
            "Exito": True,
            "Mensaje": "Generado correctamente",
            "HorariosCreados": 15,
            "Detalles": []
        }
        
        resultado = HorarioService.generar("08:00", 2)
        
        self.assertTrue(resultado["success"])
        self.assertEqual(resultado["data"]["horarios_creados"], 15)
        self.assertEqual(len(resultado["data"]["detalles"]), 0)

    @patch('src.services.horario_service.HorarioRepository')
    def test_generar_falla_sin_cursos(self, mock_repo):
        # Simulamos falla (ej. sin cursos)
        mock_repo.generar.return_value = {
            "Exito": False,
            "Mensaje": "No hay cursos activos"
        }
        
        resultado = HorarioService.generar("08:00", 2)
        
        self.assertFalse(resultado["success"])
        self.assertEqual(resultado["message"], "No hay cursos activos")
        self.assertNotIn("data", resultado)

    @patch('src.services.horario_service.HorarioRepository')
    def test_validar_horarios_retorna_metricas(self, mock_repo):
        # Simulamos que todo el horario es válido sin conflictos
        mock_repo.validar.return_value = {
            "Valido": True,
            "ConflictosAula": [],
            "ConflictosDocente": [],
            "ErroresCapacidad": []
        }
        
        resultado = HorarioService.validar()
        
        self.assertTrue(resultado["Valido"])
        self.assertEqual(len(resultado["ConflictosAula"]), 0)

if __name__ == '__main__':
    unittest.main()
