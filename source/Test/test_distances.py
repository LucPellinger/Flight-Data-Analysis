"""
This module constains three tests for the distance function in the distances.py module.
The tests are:
    1. Test that the function raises a TypeError when the inputs are not numbers.
    2. Test that the function returns the correct distance between two points.
    3. Test that the function returns the correct distance between two points.
    Here, we test the case where the two points are the same.

The tests are run by running the command `pytest` in the terminal.

The expected output is:
    - test_one: PASSED
    - test_two: PASSED
    - test_three: PASSED

If the output is different, the test has failed.

The distance function calculates the distance between two points on the earth's surface given their latitude and longitude in degrees.
The function uses the Haversine formula to calculate the distance between two points on the earth's surface.
The function takes four parameters:
    - lat1: float
        Latitude of the first point in degrees.
    - lon1: float
        Longitude of the first point in degrees.
    - lat2: float
        Latitude of the second point in degrees.
    - lon2: float
        Longitude of the second point in degrees.

The function returns the distance between the two points in kilometers.

The function raises a TypeError when the inputs are not numbers.
The function returns the correct distance between two points.
The function returns the correct distance between two points.
Here, we test the case where the two points are the same.

The function is tested using the following tests:
    - Test that the function raises a TypeError when the inputs are not numbers.
    - Test that the function returns the correct distance between two points.
    - Test that the function returns the correct distance between two points.
    Here, we test the case where the two points are the same.

The tests are run by running the command `pytest` in the terminal.
"""

import sys
import pytest

sys.path.append("./Functions/")
from Functions.distances import distance


def test_one():
    """
    Test that the function raises a TypeError when the inputs are not numbers.
    """
    with pytest.raises(TypeError):
        distance("Test", 0, 0, 0)
        distance(0, "Test", 0, 0)
        distance(0, 0, "Test", 0)
        distance(0, 0, 0, "Test")


def test_two():
    """
    Test that the function returns the correct distance between two points.
    """
    # distance between San Diego airport and Frankfurt airport
    coord_dus = (51.289501, 6.766780000000001)  # coordinates for Dusseldorf airport
    coord_sd = (32.7336006165, -117.190002441)  # coordinates for San Diego airport
    test_distance = 9192
    assert distance(
        coord_dus[0], coord_dus[1], coord_sd[0], coord_sd[1]
    ) == pytest.approx(test_distance, 10)


def test_three():
    """
    Test that the function returns the correct distance between two points.
    Here, we test the case where the two points are the same.
    """
    # distance between San Diego airport and Frankfurt airport
    coord_fra = (50.033333, 8.570556)  # coordinates for Frankfurt airport
    test_distance = 0
    assert (
        distance(coord_fra[0], coord_fra[1], coord_fra[0], coord_fra[1])
        == test_distance
    )
