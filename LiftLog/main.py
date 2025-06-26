from models.exercise import Exercise
from models.workout_plan import WorkoutPlan, TrainingSession
from utils.file_handler import save_data, load_data, save_sessions, load_sessions
from utils.analysis import show_statistics, filter_exercises, filter_exercises_by_weight, plot_total_weight_per_exercise


def main_menu():
    print("\n=== APLIKACJA: PLAN TRENINGOWY ===")
    print("1. Dodaj ćwiczenie")
    print("2. Utwórz plan treningowy")
    print("3. Rozpocznij trening")
    print("4. Analiza treningów")
    print("5. Zapisz dane")
    print("6. Wczytaj dane")
    print("7. Usuń ćwiczenie")
    print("8. Usuń plan treningowy")
    print("9. Wyświetl historię treningów")
    print("10. Filtruj ćwiczenia wg grupy mięśniowej")
    print("11. Pokaż dostępne grupy mięśniowe")
    print("12. Pokaż ćwiczenia z ciężarem powyżej podanego")
    print("13. Wygeneruj wykres ciężarów ćwiczeń")
    print("0. Wyjście")

def main():
    exercises, plans = load_data()
    sessions = load_sessions()

    while True:
        main_menu()
        choice = input("Wybierz opcję: ")

        if choice == '1':
            name = input("Nazwa ćwiczenia: ")
            muscle = input("Grupa mięśniowa: ")
            assert name.strip(), "Nazwa ćwiczenia nie może być pusta"
            assert muscle.strip(), "Grupa mięśniowa nie może być pusta"
            exercises.append(Exercise(name, muscle))
            print("✓ Ćwiczenie dodane.")

        elif choice == '2':
            plan_name = input("Nazwa planu: ")
            plan = WorkoutPlan(plan_name)
            for ex in exercises:
                print(f"- {ex.name} ({ex.muscle_group})")
            selected = input("Wpisz nazwę ćwiczenia do dodania (Enter = koniec): ")
            while selected:
                match = next((e for e in exercises if e.name == selected), None)
                if match:
                    plan.add_exercise(match)
                    print("✓ Dodano.")
                else:
                    print("️Nie znaleziono ćwiczenia.")
                selected = input("Dodaj kolejne ćwiczenie (Enter = koniec): ")
            plans.append(plan)

        elif choice == '3':
            if not plans:
                print("️Brak planów treningowych.")
                continue
            for i, plan in enumerate(plans):
                print(f"{i + 1}. {plan.name}")
            idx = int(input("Wybierz plan: ")) - 1
            session = TrainingSession(plans[idx])
            session.start()
            sessions.append(session)

        elif choice == '4':
            show_statistics(sessions)

        elif choice == '5':
            save_data(exercises, plans)
            save_sessions(sessions)
            print("✓ Dane zapisane.")

        elif choice == '6':
            exercises, plans = load_data()
            sessions = load_sessions()
            print("✓ Dane wczytane.")

        elif choice == '7':
            if not exercises:
                print("️Brak ćwiczeń do usunięcia.")
                continue
            for i, ex in enumerate(exercises):
                print(f"{i + 1}. {ex.name} ({ex.muscle_group})")
            try:
                idx = int(input("Wybierz numer ćwiczenia do usunięcia: ")) - 1
                removed = exercises.pop(idx)
                print(f"✓ Usunięto ćwiczenie: {removed.name}")
            except (ValueError, IndexError):
                print("️Nieprawidłowy wybór.")

        elif choice == '8':
            if not plans:
                print("️Brak planów do usunięcia.")
                continue
            for i, plan in enumerate(plans):
                print(f"{i + 1}. {plan.name}")
            try:
                idx = int(input("Wybierz numer planu do usunięcia: ")) - 1
                removed = plans.pop(idx)
                print(f"✓ Usunięto plan: {removed.name}")
            except (ValueError, IndexError):
                print("️Nieprawidłowy wybór.")

        elif choice == '9':
            if not sessions:
                print("️Brak historii treningów.")
                continue
            print("\n=== Historia treningów ===")
            for i, session in enumerate(sessions):
                print(f"\nTrening {i+1} - Plan: {session.plan.name}")
                for serie in session.series:
                    print(f" - {serie.exercise.name}: {serie.reps} x {serie.weight}kg")

        elif choice == '10':
            if not plans:
                print("️Brak planów treningowych.")
                continue
            for i, plan in enumerate(plans):
                print(f"{i + 1}. {plan.name}")
            try:
                idx = int(input("Wybierz plan do filtrowania: ")) - 1
                selected_plan = plans[idx]
                muscle_group = input("Podaj nazwę grupy mięśniowej do filtrowania: ")
                filtered = filter_exercises(selected_plan, lambda e: e.muscle_group.lower() == muscle_group.lower())
                if filtered:
                    print(f"\nĆwiczenia na grupę mięśniową '{muscle_group}':")
                    for ex in filtered:
                        print(f"- {ex.name}")
                else:
                    print(f"\nBrak ćwiczeń dla grupy mięśniowej '{muscle_group}' w planie '{selected_plan.name}'.")
            except (ValueError, IndexError):
                print("Nieprawidłowy wybór planu.")

        elif choice == '11':
            if not exercises:
                print("Brak ćwiczeń.")
                continue
            unique_muscles = set(e.muscle_group for e in exercises)
            print("\nDostępne grupy mięśniowe:")
            for muscle in sorted(unique_muscles):
                print(f"✓ {muscle}")

        elif choice == '12':  # nowa opcja
            if not sessions:
                print("Brak historii treningów.")
                continue
            try:
                min_w = float(input("Podaj minimalny ciężar (kg): "))
                filtered_ex = filter_exercises_by_weight(sessions, min_w)
                if filtered_ex:
                    print(f"\nĆwiczenia z ciężarem większym niż {min_w} kg:")
                    for ex in filtered_ex:
                        print(f"- {ex.name} ({ex.muscle_group})")
                else:
                    print(f"Brak ćwiczeń z ciężarem większym niż {min_w} kg.")
            except ValueError:
                print("Nieprawidłowa wartość.")

        elif choice == '13':
            if not sessions:
                print("Brak historii treningów.")
                continue
            plot_total_weight_per_exercise(sessions)


        elif choice == '0':
            print("Do zobaczenia!")
            break

        else:
            print("Nieprawidłowa opcja.")

if __name__ == "__main__":
    main()
