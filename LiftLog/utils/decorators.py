def log_start_end(func):
    def wrapper(*args, **kwargs):
        print(f"Rozpoczynam funkcję '{func.__name__}'...")
        result = func(*args, **kwargs)
        print(f"Funkcja '{func.__name__}' zakończona.")
        return result
    return wrapper
