import json
import os

from models.exercise import Exercise
from models.workout_plan import WorkoutPlan

# Automatyczne ustalenie ścieżki głównego folderu projektu
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')


# Zapisuje dane ćwiczeń i planów treningowych do plików JSON
def save_data(exercises, plans):
    try:
        os.makedirs(DATA_DIR, exist_ok=True)

        with open(os.path.join(DATA_DIR, 'exercises.json'), 'w') as f:
            json.dump([e.__dict__ for e in exercises], f)

        with open(os.path.join(DATA_DIR, 'plans.json'), 'w') as f:
            json.dump([
                {
                    'name': p.name,
                    'exercises': [e.__dict__ for e in p.exercises]
                }
                for p in plans
            ], f)

    except Exception as e:
        print(f"Błąd zapisu danych: {e}")


# Wczytuje dane ćwiczeń i planów z plików JSON
def load_data():
    exercises = []
    plans = []
    try:
        with open(os.path.join(DATA_DIR, 'exercises.json'), 'r') as f:
            exercises_json = json.load(f)
            exercises = [Exercise(**e) for e in exercises_json]

        with open(os.path.join(DATA_DIR, 'plans.json'), 'r') as f:
            plans_json = json.load(f)
            plans = [create_plan_from_json(p) for p in plans_json]

    except Exception as e:
        print(f"Błąd odczytu danych: {e}")

    return exercises, plans


# Zapisuje historię sesji treningowych do sessions.json
def save_sessions(sessions):
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(os.path.join(DATA_DIR, 'sessions.json'), 'w') as f:
            json.dump([
                {
                    "plan": s.plan.name,
                    "series": [
                        {
                            "exercise": se.exercise.name,
                            "reps": se.reps,
                            "weight": se.weight
                        }
                        for se in s.series
                    ]
                }
                for s in sessions
            ], f)
    except Exception as e:
        print(f"Błąd zapisu sesji: {e}")


# Wczytuje historię sesji treningowych z sessions.json
def load_sessions():
    sessions = []
    try:
        from models.workout_plan import TrainingSession, Serie

        with open(os.path.join(DATA_DIR, 'sessions.json'), 'r') as f:
            sessions_json = json.load(f)
            for s in sessions_json:
                plan = WorkoutPlan(s['plan'])
                session = TrainingSession(plan)
                for se in s['series']:
                    ex = Exercise(se['exercise'], "?")
                    session.series.append(
                        Serie(ex, se['reps'], se['weight'])
                    )
                sessions.append(session)
    except Exception as e:
        print(f"Błąd odczytu sesji: {e}")
    return sessions


def create_plan_from_json(plan_json):
    plan = WorkoutPlan(plan_json['name'])
    for e in plan_json['exercises']:
        if 'exercises' in e:
            subplan = create_plan_from_json(e)
            plan.add_exercise(subplan)
        else:
            plan.add_exercise(Exercise(**e))
    return plan
