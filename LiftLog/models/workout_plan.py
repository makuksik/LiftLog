from models.exercise import Exercise

class WorkoutPlan:
    def __init__(self, name: str):
        self.name = name
        self.exercises = []

    def add_exercise(self, exercise: Exercise):
        self.exercises.append(exercise)

class Serie:
    def __init__(self, exercise, reps, weight):
        if not isinstance(reps, int) or not isinstance(weight, (int, float)):
            raise TypeError("Reps must be int and weight must be int or float")
        self.exercise = exercise
        self.reps = reps
        self.weight = weight


class TrainingSession:
    def __init__(self, plan: WorkoutPlan):
        self.plan = plan
        self.series = []

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
                    print("⚠️ Błędna wartość. Spróbuj ponownie.")

# utils/file_handler.py