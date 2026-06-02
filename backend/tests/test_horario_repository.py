import unittest
from unittest.mock import patch
from src.repositories.horario_repository import HorarioRepository, DashboardRepository

class TestHorarioRepository(unittest.TestCase):

    @patch('src.repositories.horario_repository.execute_query')
    def test_get_all(self, mock_execute):
        mock_execute.return_value = [{"horarioid": 1}]
        result = HorarioRepository.get_all()
        self.assertEqual(result, [{"horarioid": 1}])
        mock_execute.assert_called_once()

    @patch('src.repositories.horario_repository.execute_query')
    def test_create_traslape_aula(self, mock_execute):
        mock_execute.return_value = [{"1": 1}] # Simula traslape de aula
        result = HorarioRepository.create(1, 1, "Lunes", "08:00", "10:00")
        self.assertFalse(result["Exito"])
        self.assertIn("aula", result["Mensaje"])

    @patch('src.repositories.horario_repository.execute_query')
    def test_create_traslape_docente(self, mock_execute):
        # Primero no hay traslape de aula (retorna []), luego el curso tiene docente (retorna [{"docenteid": 2}]),
        # luego hay traslape de docente (retorna [{"1": 1}])
        mock_execute.side_effect = [[], [{"docenteid": 2}], [{"1": 1}]]
        result = HorarioRepository.create(1, 1, "Lunes", "08:00", "10:00")
        self.assertFalse(result["Exito"])
        self.assertIn("docente", result["Mensaje"])

    @patch('src.repositories.horario_repository.execute_query')
    def test_create_exito(self, mock_execute):
        mock_execute.side_effect = [[], [], [{"horarioid": 5}]]
        result = HorarioRepository.create(1, 1, "Lunes", "08:00", "10:00")
        self.assertTrue(result["Exito"])
        self.assertEqual(result["ID"], 5)

    @patch('src.repositories.horario_repository.execute_query')
    def test_delete(self, mock_execute):
        result = HorarioRepository.delete(1)
        self.assertTrue(result)
        mock_execute.assert_called_once()

    @patch('src.repositories.horario_repository.execute_query')
    def test_generar_sin_cursos(self, mock_execute):
        mock_execute.return_value = []
        result = HorarioRepository.generar()
        self.assertFalse(result["Exito"])
        self.assertIn("cursos", result["Mensaje"])

    @patch('src.repositories.horario_repository.execute_query')
    def test_generar_sin_aulas(self, mock_execute):
        mock_execute.side_effect = [[{"cursoid": 1, "cupos": 20}], []]
        result = HorarioRepository.generar()
        self.assertFalse(result["Exito"])
        self.assertIn("aulas", result["Mensaje"])

    @patch('src.repositories.horario_repository.execute_query')
    def test_validar_invalido(self, mock_execute):
        # Simula conflictos
        mock_execute.side_effect = [[{"colision_id": 2}], [], []]
        result = HorarioRepository.validar()
        self.assertFalse(result["Valido"])

    @patch('src.repositories.horario_repository.execute_query')
    def test_validar_valido(self, mock_execute):
        # Simula sin conflictos
        mock_execute.side_effect = [[], [], []]
        result = HorarioRepository.validar()
        self.assertTrue(result["Valido"])

class TestDashboardRepository(unittest.TestCase):
    @patch('src.repositories.horario_repository.execute_query')
    def test_get_metrics(self, mock_execute):
        mock_execute.return_value = [{"total_estudiantes": 10}]
        result = DashboardRepository.get_metrics()
        self.assertEqual(result["total_estudiantes"], 10)

    @patch('src.repositories.horario_repository.execute_query')
    def test_get_metrics_empty(self, mock_execute):
        mock_execute.return_value = []
        result = DashboardRepository.get_metrics()
        self.assertEqual(result["total_estudiantes"], 0)

if __name__ == '__main__':
    unittest.main()
