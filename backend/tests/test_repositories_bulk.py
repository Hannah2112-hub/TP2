import unittest
from unittest.mock import patch
from src.repositories.aula_repository import AulaRepository
from src.repositories.carrera_repository import CarreraRepository
from src.repositories.curso_repository import CursoRepository
from src.repositories.docente_repository import DocenteRepository
from src.repositories.estudiante_repository import EstudianteRepository
from src.repositories.matricula_repository import MatriculaRepository
from src.repositories.metrics_repository import MetricsRepository

class TestRepositoriesBulk(unittest.TestCase):
    
    @patch('src.repositories.aula_repository.execute_query')
    def test_aula_repository(self, mock_execute):
        mock_execute.return_value = [{"aulaid": 1}]
        self.assertEqual(AulaRepository.get_all(), [{"aulaid": 1}])
        self.assertEqual(AulaRepository.get_by_id(1), {"aulaid": 1})
        self.assertTrue(AulaRepository.create("A1", 30, "Central")["Exito"])
        self.assertTrue(AulaRepository.update(1, "A1", 30, "Central", "Proyector"))

    @patch('src.repositories.carrera_repository.execute_query')
    def test_carrera_repository(self, mock_execute):
        mock_execute.return_value = [{"carreraid": 1}]
        self.assertEqual(CarreraRepository.get_all(), [{"carreraid": 1}])
        self.assertEqual(CarreraRepository.get_by_id(1), {"carreraid": 1})
        self.assertTrue(CarreraRepository.create("Ingeniería", 10)["Exito"])
        self.assertTrue(CarreraRepository.update(1, "Ingeniería", 10))
        self.assertTrue(CarreraRepository.delete(1))
        mock_execute.return_value = None
        CarreraRepository.setup_table()

    @patch('src.repositories.curso_repository.execute_query')
    def test_curso_repository(self, mock_execute):
        mock_execute.return_value = [{"cursoid": 1}]
        self.assertEqual(CursoRepository.get_all(), [{"cursoid": 1}])
        self.assertEqual(CursoRepository.get_by_id(1), {"cursoid": 1})
        self.assertTrue(CursoRepository.create("Matematicas", "MAT1", 4, 1, 30, 1)["Exito"])
        self.assertTrue(CursoRepository.update(1, "Matematicas", "MAT1", 4, 1, 30, 1))
        self.assertTrue(CursoRepository.delete(1))

    @patch('src.repositories.docente_repository.execute_query')
    def test_docente_repository(self, mock_execute):
        mock_execute.return_value = [{"docenteid": 1}]
        self.assertEqual(DocenteRepository.get_all(), [{"docenteid": 1}])
        self.assertEqual(DocenteRepository.get_by_id(1), {"docenteid": 1})
        self.assertTrue(DocenteRepository.create("Juan", "Perez", "jperez@test.com", "Especialista")["Exito"])
        self.assertTrue(DocenteRepository.update(1, "Juan", "Perez", "jperez@test.com", "Especialista"))
        self.assertTrue(DocenteRepository.delete(1))

    @patch('src.repositories.estudiante_repository.execute_query')
    def test_estudiante_repository(self, mock_execute):
        mock_execute.return_value = [{"estudianteid": 1}]
        self.assertEqual(EstudianteRepository.get_all(), [{"estudianteid": 1}])
        self.assertEqual(EstudianteRepository.get_by_id(1), {"estudianteid": 1})
        self.assertTrue(EstudianteRepository.create("E001", "Ana", "Gomez", "ana@test.com")["Exito"])
        self.assertTrue(EstudianteRepository.update(1, "Ana", "Gomez", "ana@test.com", 10))
        self.assertTrue(EstudianteRepository.delete(1))

    @patch('src.repositories.matricula_repository.execute_query')
    def test_matricula_repository(self, mock_execute):
        # Test create - needs side_effect for each execute_query call inside create
        mock_execute.side_effect = [[{"prerequisito_cumplido": True}], [], [{"matriculaid": 1}]]
        res = MatriculaRepository.create(1, 1)
        self.assertIsInstance(res, dict)

    @patch('src.repositories.matricula_repository.execute_query')
    def test_matricula_update_estado(self, mock_execute):
        mock_execute.return_value = []
        result = MatriculaRepository.update_estado(1, "Aprobada")
        self.assertTrue(result["Exito"])
        self.assertIn("Aprobada", result["Mensaje"])

    @patch('src.repositories.metrics_repository.execute_query')
    def test_metrics_repository(self, mock_execute):
        mock_execute.return_value = [{"metricid": 1}]
        self.assertEqual(MetricsRepository.get_global_metrics(), {"metricid": 1})
        self.assertEqual(MetricsRepository.get_recent_metrics(), [{"metricid": 1}])
        self.assertEqual(MetricsRepository.get_endpoints_ranking(), [{"metricid": 1}])
        MetricsRepository.reset_metrics()
        MetricsRepository.setup_table()

if __name__ == '__main__':
    unittest.main()
