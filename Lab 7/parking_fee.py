
import re

RATES = {"bike": 10, "car": 30, "truck": 60}


def minutes_parked(times):
    if not isinstance(times, str):
        raise ValueError("Time must be a string")

    match = re.fullmatch(
        r"(\d{2}):(\d{2})-(\d{2}):(\d{2})",
        times
    )

    if not match:
        raise ValueError("Invalid time format")

    h1, m1, h2, m2 = map(int, match.groups())

    if h1 > 23 or h2 > 23 or m1 > 59 or m2 > 59:
        raise ValueError("Invalid time")

    entry = h1 * 60 + m1
    exit_time = h2 * 60 + m2

    duration = exit_time - entry

    if duration < 0:
        duration += 24 * 60

    return duration


def hourly_rate(vehicle):
    if not isinstance(vehicle, str):
        raise ValueError("Invalid vehicle type")

    vehicle = vehicle.strip().lower()

    if vehicle not in RATES:
        raise ValueError("Unknown vehicle type")

    return RATES[vehicle]


def format_plate(plate):
    if not isinstance(plate, str):
        raise ValueError("Plate must be a string")

    plate = plate.strip().upper()

    if not re.fullmatch(r"[A-Z]{2}\d{2}[A-Z]{2}\d{4}", plate):
        raise ValueError("Invalid number plate")

    return (
        plate[0:2] + " " +
        plate[2:4] + " " +
        plate[4:6] + " " +
        plate[6:10]
    )


def main():
    print("==== Running minutes_parked ====")
    user_input = input("Enter entry and exit time (e.g. 09:30-11:45): ")
    result = minutes_parked(user_input)
    print("Minutes Parked:", result)

    print("\n==== Running hourly_rate ====")
    user_input = input("Enter vehicle type (bike/car/truck): ")
    result = hourly_rate(user_input)
    print("Hourly Rate:", result)

    print("\n==== Running format_plate ====")
    user_input = input("Enter a number plate (e.g. ka01ab1234): ")
    result = format_plate(user_input)
    print("Formatted Plate:", result)


if __name__ == "__main__":
    main()
