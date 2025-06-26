import json
import os

from GymAssistant.models.exercise import Exercise
from GymAssistant.models.workout_plan import WorkoutPlan

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')


def save_data(exercises, plans):
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(os.path.join(DATA_DIR, 'exercises.json'), 'w') as f:
            json.dump([e.__dict__ for e in exercises], f)
        with open(os.path.join(DATA_DIR, 'plans.json'), 'w') as f:
            json.dump([{'name': p.name, 'exercises': [e.__dict__ for e in p.exercises]} for p in plans], f)
    except Exception as e:
        print(f" Błąd zapisu danych: {e}")

def load_data():
    exercises = []
    plans = []
    try:
        with open(os.path.join(DATA_DIR, 'exercises.json'), 'r') as f:
            exercises_json = json.load(f)
            exercises = [Exercise(**e) for e in exercises_json]
        with open(os.path.join(DATA_DIR, 'plans.json'), 'r') as f:
            plans_json = json.load(f)
            for p in plans_json:
                plan = WorkoutPlan(p['name'])
                for e in p['exercises']:
                    plan.add_exercise(Exercise(**e))
                plans.append(plan)
    except Exception as e:
        print(f" Błąd odczytu danych: {e}")
    return exercises, plans

def save_sessions(sessions):
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(os.path.join(DATA_DIR, 'sessions.json'), 'w') as f:
            json.dump([
                {
                    "plan": s.plan.name,
                    "series": [
                        {"exercise": se.exercise.name, "reps": se.reps, "weight": se.weight}
                        for se in s.series
                    ]
                } for s in sessions
            ], f)
    except Exception as e:
        print(f" Błąd zapisu sesji: {e}")

def load_sessions():
    sessions = []
    try:
        from models.workout_plan import TrainingSession, Serie
        from models.exercise import Exercise
        with open(os.path.join(DATA_DIR, 'sessions.json'), 'r') as f:
            sessions_json = json.load(f)
            for s in sessions_json:
                plan = WorkoutPlan(s['plan'])
                session = TrainingSession(plan)
                for se in s['series']:
                    ex = Exercise(se['exercise'], "?")  # grupa mięśniowa nieistotna przy historii
                    session.series.append(Serie(ex, se['reps'], se['weight']))
                sessions.append(session)
    except Exception as e:
        print(f" Błąd odczytu sesji: {e}")
    return sessions

