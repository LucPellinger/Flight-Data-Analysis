"""
This module contains a function to calculate the distance between two points
on the earth's surface given their latitude and longitude in degrees.
"""

# Import the necessary libraries
from math import sin, cos, sqrt, atan2, radians

def distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the distance between two points on the earth's surface
    given their latitude and longitude in degrees.

    Parameters
    ------------
    lat1: float
        Latitude of the first point in degrees.
    lon1: float
        Longitude of the first point in degrees.
    lat2: float
        Latitude of the second point in degrees.
    lon2: float
        Longitude of the second point in degrees.

    Returns
    ---------
    float
        The distance between the two points in kilometers.

    Example
    ---------
    distance(55.751244, 37.618423, 59.93863, 30.31413)
    634.0
    """

    # Approximate radius of earth in km
    radius_earth = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a_var = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c_var = 2 * atan2(sqrt(a_var), sqrt(1 - a_var))

    return radius_earth * c_var
