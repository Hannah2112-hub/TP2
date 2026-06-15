import unittest
from unittest.mock import patch, MagicMock
from src.repositories.horario_repository import HorarioRepository, DashboardRepository


class TestHorarioRepositoryGenerar(unittest.TestCase):
    """Tests for HorarioRepository.generar and internal methods."""

    def test_generar_slots_basic(self):
        slots = HorarioRepository._generar_slots("08:00", 2)
        self.assertIsInstance(slots, list)
        self.assertGreater(len(slots), 0)
        for d, h_start, h_end in slots:
            self.assertIn(d, [1, 2, 3, 4, 5])
            self.assertEqual(h_end - h_start, 2)
            self.assertGreaterEqual(h_start, 8)
            self.assertLessEqual(h_end, 22)

    def test_generar_slots_1_hour(self):
        slots = HorarioRepository._generar_slots("08:00", 1)
        for d, h_start, h_end in slots:
            self.assertEqual(h_end - h_start, 1)

    def test_generar_slots_3_hour(self):
        slots = HorarioRepository._generar_slots("08:00", 3)
        for d, h_start, h_end in slots:
            self.assertEqual(h_end - h_start, 3)

    def test_generar_slots_10_hours(self):
        slots = HorarioRepository._generar_slots("08:00", 10)
        for d, h_start, h_end in slots:
            self.assertEqual(h_end - h_start, 10)

    @patch('src.repositories.horario_repository.execute_query')
    def test_obtener_cursos_con_carrera(self, mock_query):
        mock_query.return_value = [{"cursoid": 1, "nombre": "Mate"}]
        result = HorarioRepository._obtener_cursos(1)
        self.assertEqual(len(result), 1)

    @patch('src.repositories.horario_repository.execute_query')
    def test_obtener_cursos_sin_carrera(self, mock_query):
        mock_query.return_value = [{"cursoid": 1}, {"cursoid": 2}]
        result = HorarioRepository._obtener_cursos(None)
        self.assertEqual(len(result), 2)

    @patch('src.repositories.horario_repository.execute_query')
    def test_obtener_aulas(self, mock_query):
        mock_query.return_value = [{"aulaid": 1, "capacidad": 30}]
        result = HorarioRepository._obtener_aulas()
        self.assertEqual(len(result), 1)

    @patch('src.repositories.horario_repository.execute_query')
    def test_generar_no_cursos(self, mock_query):
        mock_query.return_value = []
        result = HorarioRepository.generar()
        self.assertFalse(result["Exito"])
        self.assertIn("No hay cursos", result["Mensaje"])

    @patch('src.repositories.horario_repository.execute_query')
    def test_generar_no_aulas(self, mock_query):
        mock_query.side_effect = [
            [{"cursoid": 1, "nombre": "Mate", "cupos": 20, "docenteid": 1, "carreraid": 1}],
            [],
        ]
        result = HorarioRepository.generar()
        self.assertFalse(result["Exito"])
        self.assertIn("No hay aulas", result["Mensaje"])

    @patch('src.repositories.horario_repository.execute_query')
    def test_generar_no_variables(self, mock_query):
        mock_query.side_effect = [
            [{"cursoid": 1, "nombre": "Mate", "cupos": 200, "docenteid": 1, "carreraid": 1}],
            [{"aulaid": 1, "capacidad": 10}],
        ]
        result = HorarioRepository.generar()
        self.assertFalse(result["Exito"])

    @patch('src.repositories.horario_repository.execute_query')
    def test_generar_exito(self, mock_query):
        mock_query.side_effect = [
            [{"cursoid": 1, "nombre": "Mate", "cupos": 10, "docenteid": 1, "carreraid": 1}],
            [{"aulaid": 1, "capacidad": 30}],
            [],
            [],
            [],
            [],
            [],
        ]
        result = HorarioRepository.generar()
        self.assertTrue(result["Exito"])

    @patch('src.repositories.horario_repository.execute_query')
    def test_generar_con_carrera(self, mock_query):
        mock_query.side_effect = [
            [{"cursoid": 1, "nombre": "Mate", "cupos": 10, "docenteid": 1, "carreraid": 1}],
            [{"aulaid": 1, "capacidad": 30}],
            [],
            [],
            [],
            [],
            [],
        ]
        result = HorarioRepository.generar(carrera_id=1)
        self.assertTrue(result["Exito"])

    @patch('src.repositories.horario_repository.execute_query')
    def test_generar_con_errores_cursos(self, mock_query):
        mock_query.side_effect = [
            [{"cursoid": 1, "nombre": "Mate", "cupos": 10, "docenteid": 1, "carreraid": 1},
             {"cursoid": 2, "nombre": "Fisica", "cupos": 100, "docenteid": 2, "carreraid": 1}],
            [{"aulaid": 1, "capacidad": 30}],
            [],
            [],
            [],
            [],
            [],
        ]
        result = HorarioRepository.generar()
        self.assertTrue(result["Exito"])

    def test_generar_slots_no_slots(self):
        slots = HorarioRepository._generar_slots("22:00", 2)
        self.assertEqual(len(slots), 0)


class TestHorarioRepositoryCreate(unittest.TestCase):
    """Tests for create, delete, get_all."""

    @patch('src.repositories.horario_repository.execute_query')
    def test_create_success(self, mock_query):
        mock_query.side_effect = [
            [],
            [],
            [{"horarioid": 1}],
        ]
        result = HorarioRepository.create(1, 1, "Lunes", "08:00", "10:00")
        self.assertTrue(result["Exito"])

    @patch('src.repositories.horario_repository.execute_query')
    def test_create_traslape_aula(self, mock_query):
        mock_query.return_value = [{"1": 1}]
        result = HorarioRepository.create(1, 1, "Lunes", "08:00", "10:00")
        self.assertFalse(result["Exito"])
        self.assertIn("aula", result["Mensaje"])

    @patch('src.repositories.horario_repository.execute_query')
    def test_create_traslape_docente(self, mock_query):
        mock_query.side_effect = [
            [],
            [{"docenteid": 1}],
            [{"1": 1}],
        ]
        result = HorarioRepository.create(1, 1, "Lunes", "08:00", "10:00")
        self.assertFalse(result["Exito"])
        self.assertIn("docente", result["Mensaje"])

    @patch('src.repositories.horario_repository.execute_query')
    def test_create_docente_none(self, mock_query):
        mock_query.side_effect = [
            [],
            [{"docenteid": None}],
            [{"horarioid": 1}],
        ]
        result = HorarioRepository.create(1, 1, "Lunes", "08:00", "10:00")
        self.assertTrue(result["Exito"])

    @patch('src.repositories.horario_repository.execute_query')
    def test_create_error_insert(self, mock_query):
        mock_query.side_effect = [
            [],
            [],
            [],
        ]
        result = HorarioRepository.create(1, 1, "Lunes", "08:00", "10:00")
        self.assertFalse(result["Exito"])

    @patch('src.repositories.horario_repository.execute_query')
    def test_delete(self, mock_query):
        result = HorarioRepository.delete(1)
        self.assertTrue(result)

    @patch('src.repositories.horario_repository.execute_query')
    def test_get_all(self, mock_query):
        mock_query.return_value = [{"horarioid": 1}]
        result = HorarioRepository.get_all()
        self.assertEqual(len(result), 1)


class TestHorarioRepositoryValidar(unittest.TestCase):
    @patch('src.repositories.horario_repository.execute_query')
    def test_validar_sin_conflictos(self, mock_query):
        mock_query.side_effect = [[], [], []]
        result = HorarioRepository.validar()
        self.assertTrue(result["Valido"])

    @patch('src.repositories.horario_repository.execute_query')
    def test_validar_con_conflictos(self, mock_query):
        mock_query.side_effect = [
            [{"horarioid": 1}],
            [],
            [],
        ]
        result = HorarioRepository.validar()
        self.assertFalse(result["Valido"])

    @patch('src.repositories.horario_repository.execute_query')
    def test_validar_conflicto_docente(self, mock_query):
        mock_query.side_effect = [
            [],
            [{"horarioid": 2}],
            [],
        ]
        result = HorarioRepository.validar()
        self.assertFalse(result["Valido"])

    @patch('src.repositories.horario_repository.execute_query')
    def test_validar_error_capacidad(self, mock_query):
        mock_query.side_effect = [
            [],
            [],
            [{"horarioid": 3}],
        ]
        result = HorarioRepository.validar()
        self.assertFalse(result["Valido"])


class TestDashboardRepository(unittest.TestCase):
    @patch('src.repositories.horario_repository.execute_query')
    def test_get_metrics_with_data(self, mock_query):
        mock_query.return_value = [{
            "total_estudiantes": 10,
            "total_docentes": 5,
            "total_cursos": 20,
            "total_aulas": 8,
            "matriculas_aprobadas": 50,
            "matriculas_rechazadas": 3,
        }]
        result = DashboardRepository.get_metrics()
        self.assertEqual(result["total_estudiantes"], 10)

    @patch('src.repositories.horario_repository.execute_query')
    def test_get_metrics_empty(self, mock_query):
        mock_query.return_value = []
        result = DashboardRepository.get_metrics()
        self.assertEqual(result["total_estudiantes"], 0)


class TestHorarioRepositoryModel(unittest.TestCase):
    @patch('src.repositories.horario_repository.execute_query')
    def test_construir_modelo(self, mock_query):
        from ortools.sat.python import cp_model
        model = cp_model.CpModel()
        cursos = [{"cursoid": 1, "nombre": "Mate", "cupos": 10, "docenteid": 1, "carreraid": 1}]
        aulas = [{"aulaid": 1, "capacidad": 30}]
        slots = [(1, 8, 10), (1, 10, 12)]
        x = HorarioRepository._construir_modelo(model, cursos, aulas, slots)
        self.assertGreater(len(x), 0)

    @patch('src.repositories.horario_repository.execute_query')
    def test_aplicar_restricciones(self, mock_query):
        from ortools.sat.python import cp_model
        model = cp_model.CpModel()
        cursos = [{"cursoid": 1, "nombre": "Mate", "cupos": 10, "docenteid": 1, "carreraid": 1}]
        aulas = [{"aulaid": 1, "capacidad": 30}]
        slots = [(1, 8, 10), (1, 10, 12), (2, 8, 10), (2, 10, 12)]
        x = HorarioRepository._construir_modelo(model, cursos, aulas, slots)
        errores = HorarioRepository._aplicar_restricciones(model, x, cursos, aulas, slots)
        self.assertIsInstance(errores, list)

    @patch('src.repositories.horario_repository.execute_query')
    def test_aplicar_restricciones_curso_sin_aula(self, mock_query):
        from ortools.sat.python import cp_model
        model = cp_model.CpModel()
        cursos = [{"cursoid": 1, "nombre": "Mate", "cupos": 200, "docenteid": 1, "carreraid": 1}]
        aulas = [{"aulaid": 1, "capacidad": 10}]
        slots = [(1, 8, 10)]
        x = HorarioRepository._construir_modelo(model, cursos, aulas, slots)
        errores = HorarioRepository._aplicar_restricciones(model, x, cursos, aulas, slots)
        self.assertGreater(len(errores), 0)

    @patch('src.repositories.horario_repository.execute_query')
    def test_insertar_horarios(self, mock_query):
        from ortools.sat.python import cp_model
        model = cp_model.CpModel()
        cursos = [{"cursoid": 1, "nombre": "Mate", "cupos": 10, "docenteid": 1, "carreraid": 1}]
        aulas = [{"aulaid": 1, "capacidad": 30}]
        slots = [(1, 8, 10)]
        x = HorarioRepository._construir_modelo(model, cursos, aulas, slots)
        solver = cp_model.CpSolver()
        status = solver.Solve(model)
        if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            HorarioRepository._insertar_horarios(solver, x, cursos, aulas, slots, None)

    @patch('src.repositories.horario_repository.execute_query')
    def test_insertar_horarios_con_carrera(self, mock_query):
        from ortools.sat.python import cp_model
        model = cp_model.CpModel()
        cursos = [{"cursoid": 1, "nombre": "Mate", "cupos": 10, "docenteid": 1, "carreraid": 1}]
        aulas = [{"aulaid": 1, "capacidad": 30}]
        slots = [(1, 8, 10)]
        x = HorarioRepository._construir_modelo(model, cursos, aulas, slots)
        solver = cp_model.CpSolver()
        status = solver.Solve(model)
        if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            HorarioRepository._insertar_horarios(solver, x, cursos, aulas, slots, 1)


if __name__ == '__main__':
    unittest.main()
