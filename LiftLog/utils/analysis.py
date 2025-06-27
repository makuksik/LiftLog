from functools import reduce
from collections import defaultdict
import matplotlib.pyplot as plt
from LiftLog.models.workout_plan import WorkoutPlan


def show_statistics(sessions):
    total_volume = reduce(
        lambda acc, s: acc + sum(x.reps * x.weight for x in s.series),
        sessions,
        0
    )
    print(f"\nCałkowita objętość treningowa: {total_volume:.2f} kg")


def filter_exercises(plan, predicate):
    """
    Rekurencyjnie zwraca listę ćwiczeń z planu i podplanów,
    które spełniają warunek zdefiniowany w predicate.
    """
    filtered = []
    for e in plan.exercises:
        if isinstance(e, WorkoutPlan):  # podplan — rekurencyjnie
            filtered.extend(filter_exercises(e, predicate))
        elif predicate(e):
            filtered.append(e)
    return filtered


def filter_exercises_by_weight(sessions, min_weight):
    """
    Zwraca listę unikalnych ćwiczeń, które w sesjach treningowych
    wykonano z ciężarem większym niż min_weight.
    """
    all_series = [s for session in sessions for s in session.series]
    filtered_series = filter(lambda s: s.weight > min_weight, all_series)
    exercises = map(lambda s: s.exercise, filtered_series)
    unique_exercises = set(exercises)
    return list(unique_exercises)

def plot_total_weight_per_exercise(sessions,
                                   filename="total_weight_per_exercise.png"):
    total_weights = defaultdict(float)
    for session in sessions:
        for serie in session.series:
            total_weights[serie.exercise.name] += serie.reps * serie.weight

    if not total_weights:
        print("Brak danych do wykresu.")
        return

    # Sortowanie według wagi malejąco
    sorted_items = sorted(
        total_weights.items(), key=lambda x: x[1], reverse=True
    )
    exercises, weights = zip(*sorted_items)

    plt.figure(figsize=(10, 6))
    plt.bar(exercises, weights, color='skyblue')
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Całkowity ciężar [kg]")
    plt.title("Całkowity ciężar podniesiony dla ćwiczeń")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"Wykres zapisano do pliku: {filename}")
