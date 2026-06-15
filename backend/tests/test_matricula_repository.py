import unittest
from unittest.mock import patch
from src.repositories.matricula_repository import MatriculaRepository


class TestMatriculaRepository(unittest.TestCase):

    @patch('src.repositories.matricula_repository.execute_query')
    def test_get_all_sin_filtro(self, mock_query):
        mock_query.return_value = [{"matriculaid": 1}]
        result = MatriculaRepository.get_all()
        self.assertEqual(len(result), 1)

    @patch('src.repositories.matricula_repository.execute_query')
    def test_get_all_con_estudiante_id(self, mock_query):
        mock_query.return_value = [{"matriculaid": 1, "estudianteid": 5}]
        result = MatriculaRepository.get_all(estudiante_id=5)
        self.assertEqual(len(result), 1)
        mock_query.assert_called_once()

    @patch('src.repositories.matricula_repository.execute_query')
    def test_get_by_id_found(self, mock_query):
        mock_query.return_value = [{"matriculaid": 1}]
        result = MatriculaRepository.get_by_id(1)
        self.assertIsNotNone(result)
        self.assertEqual(result["matriculaid"], 1)

    @patch('src.repositories.matricula_repository.execute_query')
    def test_get_by_id_not_found(self, mock_query):
        mock_query.return_value = []
        result = MatriculaRepository.get_by_id(999)
        self.assertIsNone(result)

    @patch('src.repositories.matricula_repository.execute_query')
    def test_create_estudiante_no_existe(self, mock_query):
        mock_query.side_effect = [
            [],
            [{"creditosreq": 10}],
            [],
        ]
        result = MatriculaRepository.create(999, 1)
        self.assertFalse(result["Exito"])
        self.assertIn("no existe", result["Mensaje"])

    @patch('src.repositories.matricula_repository.execute_query')
    def test_create_curso_no_existe(self, mock_query):
        mock_query.side_effect = [
            [{"creditosacum": 50}],
            [],
            [],
        ]
        result = MatriculaRepository.create(1, 999)
        self.assertFalse(result["Exito"])
        self.assertIn("Curso no existe", result["Mensaje"])

    @patch('src.repositories.matricula_repository.execute_query')
    def test_create_creditos_insuficientes(self, mock_query):
        mock_query.side_effect = [
            [{"creditosacum": 5}],
            [{"creditosreq": 20}],
            [],
        ]
        result = MatriculaRepository.create(1, 1)
        self.assertFalse(result["Exito"])
        self.assertIn("insuficientes", result["Mensaje"])

    @patch('src.repositories.matricula_repository.execute_query')
    def test_create_ya_matriculado(self, mock_query):
        mock_query.side_effect = [
            [{"creditosacum": 50}],
            [{"creditosreq": 10}],
            [{"1": 1}],
        ]
        result = MatriculaRepository.create(1, 1)
        self.assertFalse(result["Exito"])
        self.assertIn("ya se encuentra", result["Mensaje"])

    @patch('src.repositories.matricula_repository.execute_query')
    def test_create_exito(self, mock_query):
        mock_query.side_effect = [
            [{"creditosacum": 50}],
            [{"creditosreq": 10}],
            [],
            [{"matriculaid": 10}],
        ]
        result = MatriculaRepository.create(1, 1)
        self.assertTrue(result["Exito"])
        self.assertEqual(result["ID"], 10)

    @patch('src.repositories.matricula_repository.execute_query')
    def test_create_error_insert(self, mock_query):
        mock_query.side_effect = [
            [{"creditosacum": 50}],
            [{"creditosreq": 10}],
            [],
            [],
        ]
        result = MatriculaRepository.create(1, 1)
        self.assertFalse(result["Exito"])

    @patch('src.repositories.matricula_repository.execute_query')
    def test_update_estado(self, mock_query):
        result = MatriculaRepository.update_estado(1, "Rechazada")
        self.assertTrue(result["Exito"])
        self.assertIn("Rechazada", result["Mensaje"])


if __name__ == '__main__':
    unittest.main()
