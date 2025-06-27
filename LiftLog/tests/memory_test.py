import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.exercise import Exercise
from models.workout_plan import WorkoutPlan, TrainingSession, Serie

from memory_profiler import profile

@profile
def test_memory():
    plan = WorkoutPlan("Test plan")
    ex = Exercise("Przysiady", "Nogi")
    session = TrainingSession(plan)

    for _ in range(10000):
        session.series.append(Serie(ex, 10, 100))

    return session

if __name__ == "__main__":
    test_memory()
