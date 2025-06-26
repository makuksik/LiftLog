from functools import reduce

def show_statistics(sessions):
    total_volume = reduce(lambda acc, s: acc + sum(x.reps * x.weight for x in s.series), sessions, 0)
    print(f"\nCałkowita objętość treningowa: {total_volume:.2f} kg")