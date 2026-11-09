
import pytest
from parking_fee import parking_fee, find_slot, monthly_pass


# Existing test cases
def test_free_short_stay():
    assert parking_fee("car", 20, False, False) == 0


def test_any_floor():
    assert find_slot("car", 5, False) == "any floor"


# Parking fee test cases
def test_invalid_vehicle():
    with pytest.raises(ValueError):
        parking_fee("bus", 60, False, False)


def test_negative_duration():
    with pytest.raises(ValueError):
        parking_fee("car", -10, False, False)


def test_free_parking_boundary():
    assert parking_fee("car", 30, False, False) == 0


def test_hourly_rounding():
    assert parking_fee("car", 61, False, False) == 60


def test_exact_hour():
    assert parking_fee("car", 60, False, False) == 30


def test_ev_discount():
    assert parking_fee("car", 60, True, False) == 15


def test_truck_no_ev_discount():
    assert parking_fee("truck", 60, True, False) == 60


def test_lost_ticket():
    assert parking_fee("car", 60, False, True) == 230


def test_bike_fee():
    assert parking_fee("bike", 60, False, False) == 10


def test_free_ev_parking():
    assert parking_fee("bike", 20, True, False) == 0


# Parking slot test cases
def test_full_parking():
    assert find_slot("car", 0, False) == "full"


def test_disabled_parking():
    assert find_slot("car", 5, True) == "ground floor"


def test_truck_parking():
    assert find_slot("truck", 5, False) == "basement"


# Monthly pass test cases
def test_bike_monthly_pass():
    assert monthly_pass("bike", False) == 500


def test_bike_resident_discount():
    assert monthly_pass("bike", True) == 400


def test_car_monthly_pass():
    assert monthly_pass("car", False) == 1500


def test_car_resident_discount():
    assert monthly_pass("car", True) == 1200


def test_invalid_monthly_pass():
    with pytest.raises(ValueError):
        monthly_pass("truck", False)
