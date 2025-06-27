# LiftLog – Program do planowania treningów siłowych

## Cel projektu
LiftLog to aplikacja konsolowa napisana w Pythonie, służąca do efektywnego planowania i monitorowania treningów siłowych. Pozwala na tworzenie spersonalizowanych planów treningowych, rejestrowanie szczegółowych danych sesji treningowych oraz analizę postępów za pomocą raportów i wykresów.

Dzięki trwałemu zapisywaniu danych w plikach JSON, użytkownik ma dostęp do historii treningów i może świadomie rozwijać swoją siłę oraz kondycję.

## Autor
- Mateusz Petelicki  
- Grupa: 2ID12B, Informatyka 2 rok  
- Data: 27.06.2025

## Wymagania
- Python 3.13.3  
- biblioteka matplotlib (do wykresów)  
- standardowa biblioteka Pythona (json, os, unittest, itd.)

## Struktura projektu
LiftLog/
├── main.py
├── models/
│ ├── init.py
│ ├── exercise.py
│ ├── workout_plan.py
├── utils/
│ ├── init.py
│ ├── file_handler.py
│ ├── analysis.py
├── data/
│ ├── exercises.json
│ ├── plans.json
│ ├── sessions.json
├── tests/
│ ├── init.py
│ ├── test_workout.py
│ ├── memory_test.py


## Uruchomienie
1. Zainstaluj Pythona 3.13.3.  
2. Zainstaluj matplotlib:
pip install matplotlib
3. Uruchom program z katalogu głównego:
python main.py
4. Postępuj zgodnie z instrukcjami w menu konsoli.

---

Dziękuję za zainteresowanie projektem LiftLog!