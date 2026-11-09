
from hypothesis import given, strategies as st
import pytest
import re

from parking_fee import minutes_parked, hourly_rate, format_plate


# 1. Fuzz testing for parking time inputs
@given(st.one_of(st.text(), st.none()))
def test_minutes_parked_no_crash(s):
    try:
        result = minutes_parked(s)
        assert isinstance(result, int)
        assert result >= 0
    except (ValueError, TypeError, AttributeError):
        pass


# 2. Fuzz testing for vehicle types
@given(st.one_of(st.text(), st.none()))
def test_hourly_rate_no_crash(s):
    try:
        result = hourly_rate(s)
        assert isinstance(result, int)
        assert result > 0
    except (KeyError, ValueError, TypeError, AttributeError):
        pass


# 3. Fuzz testing for number plates
@given(st.one_of(st.text(), st.none()))
def test_format_plate_no_crash(s):
    try:
        result = format_plate(s)
        assert isinstance(result, str)
    except (ValueError, TypeError, AttributeError, IndexError):
        pass


# 4. Test parking duration is calculated correctly
@given(
    st.integers(min_value=0, max_value=23),
    st.integers(min_value=0, max_value=59),
    st.integers(min_value=0, max_value=23),
    st.integers(min_value=0, max_value=59)
)
def test_parking_duration_non_negative(h1, m1, h2, m2):
    entry = f"{h1:02d}:{m1:02d}"
    exit_time = f"{h2:02d}:{m2:02d}"

    result = minutes_parked(f"{entry}-{exit_time}")

    assert result >= 0


# 5. Test valid vehicle rates
@given(st.sampled_from(["bike", "car", "truck"]))
def test_valid_hourly_rates(vehicle):
    expected_rates = {
        "bike": 10,
        "car": 30,
        "truck": 60
    }

    assert hourly_rate(vehicle) == expected_rates[vehicle]


# 6. Test valid number plate formatting
@given(
    st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=2, max_size=2),
    st.text(alphabet="0123456789", min_size=2, max_size=2),
    st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=2, max_size=2),
    st.text(alphabet="0123456789", min_size=4, max_size=4)
)
def test_valid_plate_format(state, district, letters, numbers):
    plate = state + district + letters + numbers
    result = format_plate(plate)

    assert result == f"{state} {district} {letters} {numbers}"


# 7. Test exact parking duration
@given(
    st.integers(min_value=0, max_value=23),
    st.integers(min_value=0, max_value=59),
    st.integers(min_value=0, max_value=23),
    st.integers(min_value=0, max_value=59)
)
def test_exact_parking_duration(h1, m1, h2, m2):
    entry = f"{h1:02d}:{m1:02d}"
    exit_time = f"{h2:02d}:{m2:02d}"

    expected = ((h2 * 60 + m2) - (h1 * 60 + m1)) % 1440

    assert minutes_parked(f"{entry}-{exit_time}") == expected


# 8. Test invalid vehicle rejection
@given(st.sampled_from(["bus", "plane", "", "van", "bikee"]))
def test_invalid_vehicle_rejected(vehicle):
    with pytest.raises(ValueError):
        hourly_rate(vehicle)


# 9. Test invalid number plate rejection
@given(st.text(min_size=0, max_size=20))
def test_invalid_plate_rejected(plate):
    if not re.fullmatch(
        r"[A-Z]{2}\d{2}[A-Z]{2}\d{4}",
        plate.strip().upper()
    ):
        with pytest.raises(ValueError):
            format_plate(plate)


# 10. Test invalid time rejection
@given(st.sampled_from([
    "25:00-12:00",
    "12:60-13:00",
    "invalid",
    "",
    "09:30",
    "09:30-"
]))
def test_invalid_time_rejected(times):
    with pytest.raises(ValueError):
        minutes_parked(times)
