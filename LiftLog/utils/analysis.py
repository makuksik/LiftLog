from functools import reduce
from LiftLog.models.workout_plan import WorkoutPlan
import matplotlib.pyplot as plt
from collections import defaultdict



def show_statistics(sessions):
    total_volume = reduce(lambda acc, s: acc + sum(x.reps * x.weight for x in s.series), sessions, 0)
    print(f"\nCałkowita objętość treningowa: {total_volume:.2f} kg")

def filter_exercises(plan, predicate):
    """
    Rekurencyjnie zwraca listę ćwiczeń z planu i podplanów,
    które spełniają warunek zdefiniowany w predicate (funkcja przyjmująca Exercise i zwracająca bool).
    """
    filtered = []
    for e in plan.exercises:
        if isinstance(e, WorkoutPlan):  # podplan — rekurencyjnie
            filtered.extend(filter_exercises(e, predicate))
        else:
            if predicate(e):
                filtered.append(e)
    return filtered

def filter_exercises_by_weight(sessions, min_weight):
    """
    Zwraca listę unikalnych ćwiczeń, które w sesjach treningowych
    wykonano z ciężarem > min_weight.
    """

    # Najpierw spłaszczamy wszystkie serie ze wszystkich sesji:
    all_series = [serie for session in sessions for serie in session.series]

    # Filtrujemy serie z ciężarem większym niż min_weight
    filtered_series = filter(lambda s: s.weight > min_weight, all_series)

    # Mapujemy te serie na ćwiczenia
    exercises = map(lambda s: s.exercise, filtered_series)

    # Unikalne ćwiczenia (set)
    unique_exercises = set(exercises)

    return list(unique_exercises)

def plot_total_weight_per_exercise(sessions, filename="total_weight_per_exercise.png"):
    total_weights = defaultdict(float)
    for session in sessions:
        for serie in session.series:
            total_weights[serie.exercise.name] += serie.reps * serie.weight

    if not total_weights:
        print("Brak danych do wykresu.")
        return

    exercises = list(total_weights.keys())
    weights = list(total_weights.values())

    plt.figure(figsize=(10, 6))
    plt.bar(exercises, weights, color='skyblue')
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Całkowity ciężar [kg]")
    plt.title("Całkowity ciężar podniesiony dla ćwiczeń")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"Wykres zapisano do pliku: {filename}")
