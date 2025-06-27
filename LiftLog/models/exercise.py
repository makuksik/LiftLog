# Klasa reprezentująca pojedyncze ćwiczenie siłowe
class Exercise:
    def __init__(self, name: str, muscle_group: str):
        # Nazwa ćwiczenia (np. "Przysiad", "Wyciskanie")
        self.name = name
        # Grupa mięśniowa, na którą działa ćwiczenie
        # (np. "Nogi", "Klatka piersiowa")
        self.muscle_group = muscle_group
