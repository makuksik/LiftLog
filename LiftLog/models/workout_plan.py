from models.exercise import Exercise

# Klasa reprezentująca plan treningowy z listą ćwiczeń
class WorkoutPlan:
    def __init__(self, name: str):
        self.name = name
        self.exercises = []

    # Dodaje ćwiczenie do planu
    def add_exercise(self, exercise: Exercise):
        self.exercises.append(exercise)

# Klasa reprezentująca jedną serię danego ćwiczenia
class Serie:
    def __init__(self, exercise, reps, weight):
        # Walidacja typów
        if not isinstance(reps, int) or not isinstance(weight, (int, float)):
            raise TypeError("Reps must be int and weight must be int or float")
        self.exercise = exercise
        self.reps = reps
        self.weight = weight

# Klasa reprezentująca pełną sesję treningową na podstawie planu
class TrainingSession:
    def __init__(self, plan: WorkoutPlan):
        self.plan = plan
        self.series = []  # lista wykonanych serii

    # Przeprowadza trening z inputem użytkownika
    def start(self):
        print(f"\nRozpoczynasz trening: {self.plan.name}")
        for exercise in self.plan.exercises:
            print(f"\nĆwiczenie: {exercise.name}")
            while True:
                try:
                    reps = int(input("Liczba powtórzeń (0 = koniec): "))
                    if reps == 0:
                        break
                    weight = float(input("Ciężar [kg]: "))
                    self.series.append(Serie(exercise, reps, weight))
                except ValueError:
                    print("Błędna wartość. Spróbuj ponownie.")
