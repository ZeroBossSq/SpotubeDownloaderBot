def to_fixed(num_obj: float, dig=0) -> float:
    return float(f'{num_obj:.{dig}f}')


print(to_fixed())
