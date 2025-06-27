import unittest
from contextlib import redirect_stdout
import time
from io import StringIO

from models.exercise import Exercise
from models.workout_plan import WorkoutPlan, Serie, TrainingSession
from utils.file_handler import save_data, load_data
from utils.analysis import show_statistics


class TestExercise(unittest.TestCase):
    def test_exercise_creation(self):
        ex = Exercise("Przysiad", "Nogi")
        self.assertEqual(ex.name, "Przysiad")
        self.assertEqual(ex.muscle_group, "Nogi")


class TestWorkoutPlan(unittest.TestCase):
    def test_plan_add_exercise(self):
        ex = Exercise("Wyciskanie", "Klatka")
        plan = WorkoutPlan("Plan A")
        plan.add_exercise(ex)
        self.assertIn(ex, plan.exercises)


class TestTrainingSession(unittest.TestCase):
    def test_add_series(self):
        ex = Exercise("Martwy ciąg", "Plecy")
        plan = WorkoutPlan("Plecy")
        plan.add_exercise(ex)
        session = TrainingSession(plan)
        session.series.append(Serie(ex, 10, 100))
        self.assertEqual(len(session.series), 1)
        self.assertEqual(session.series[0].reps, 10)
        self.assertEqual(session.series[0].weight, 100)


class TestFileHandler(unittest.TestCase):
    def test_save_and_load_data(self):
        ex = Exercise("Wiosłowanie", "Plecy")
        plan = WorkoutPlan("Back Day")
        plan.add_exercise(ex)
        save_data([ex], [plan])
        loaded_exercises, loaded_plans = load_data()
        self.assertEqual(len(loaded_exercises), 1)
        self.assertEqual(len(loaded_plans), 1)
        self.assertEqual(loaded_exercises[0].name, "Wiosłowanie")
        self.assertEqual(loaded_plans[0].name, "Back Day")


class TestAnalysis(unittest.TestCase):
    def test_show_statistics_output(self):
        ex = Exercise("Wyciskanie", "Klatka")
        plan = WorkoutPlan("Plan A")
        plan.add_exercise(ex)
        session = TrainingSession(plan)
        session.series.append(Serie(ex, 10, 100))

        captured_output = StringIO()
        with redirect_stdout(captured_output):
            show_statistics([session])

        output = captured_output.getvalue()
        self.assertIn("Całkowita objętość treningowa", output)


class TestEdgeCases(unittest.TestCase):
    def test_invalid_reps_weight(self):
        with self.assertRaises(TypeError):
            Serie("przysiad", "dziesięć", "sto")


class TestFunctionalFlow(unittest.TestCase):
    def test_full_workflow(self):
        ex1 = Exercise("Przysiad", "Nogi")
        ex2 = Exercise("Wyciskanie", "Klatka")
        plan = WorkoutPlan("Plan Siłowy")
        plan.add_exercise(ex1)
        plan.add_exercise(ex2)

        session = TrainingSession(plan)
        session.series.append(Serie(ex1, 10, 80))
        session.series.append(Serie(ex2, 8, 60))

        # symulacja zapisu i odczytu
        save_data([ex1, ex2], [plan])
        loaded_exercises, loaded_plans = load_data()

        self.assertEqual(len(loaded_exercises), 2)
        self.assertEqual(len(loaded_plans), 1)
        self.assertEqual(loaded_plans[0].exercises[0].name, "Przysiad")

        # sprawdzenie statystyk
        captured_output = StringIO()
        with redirect_stdout(captured_output):
            show_statistics([session])
        self.assertIn("Całkowita objętość treningowa", captured_output.getvalue())


# --- Testy wydajnościowe ---
class TestPerformance(unittest.TestCase):
    def test_show_statistics_performance(self):
        ex = Exercise("Wyciskanie", "Klatka")
        plan = WorkoutPlan("Plan A")
        plan.add_exercise(ex)
        session = TrainingSession(plan)
        # Dodajemy dużą liczbę serii, by zasymulować obciążenie
        for _ in range(10000):
            session.series.append(Serie(ex, 10, 100))

        start_time = time.time()
        show_statistics([session])
        end_time = time.time()
        duration = end_time - start_time
        print(f"Czas wykonania show_statistics: {duration:.2f} sekundy")
        self.assertLess(duration, 2, "Funkcja show_statistics działa zbyt wolno")


if __name__ == '__main__':
    unittest.main()
