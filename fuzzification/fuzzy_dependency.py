import math

DISTANCE_NEAR = "Near"
DISTANCE_MEDIUM = "Medium"
DISTANCE_FAR = "Far"

ANGLE_SMALL = "Small"
ANGLE_MEDIUM = "Medium"
ANGLE_BIG = "Big"

RED = "Red"
LESS_RED = "Less_red"
GREEN = "Green"
LESS_GREEN = "Less_green"

FAST = "Fast"
SLOWER = "Slower"
SLOW = "Slow"
STOP = "Stop"


# distance dependency
def distance_near_dependency(distance):
    if 0 <= distance <= 100:
        return 1.0
    if 100 < distance < 200:
        return (200 - distance) / 100.0
    return 0.0


def distance_medium_dependency(distance):
    if 100 <= distance <= 200:
        return (distance - 100) / 100.0
    if 200 <= distance <= 300:
        return (300 - distance) / 100.0
    return 0.0


def distance_far_dependency(distance):
    if 200 <= distance <= 300:
        return (distance - 200) / 100.0
    if distance >= 300:
        return 1.0
    return 0.0


# angle dependency
def angle_small_dependency(angle):
    if 0 <= angle <= 5:
        return 1.0
    if 5 <= angle <= 10:
        return (10 - angle) / 5.0
    return 0.0


def angle_medium_dependency(angle):
    if 5 <= angle <= 10:
        return (angle - 5) / 5.0
    if 10 <= angle <= 15:
        return (15 - angle) / 5.0
    return 0.0


def angle_big_dependency(angle):
    if angle >= 15:
        return 1.0
    if 10 <= angle <= 15:
        return (angle - 10) / 5.0
    return 0.0


# lamp dependency
def lamp_red_dependency(time):
    if time >= 10:
        return 1.0
    if 5 <= time <= 10:
        return (time - 5) / 5.0
    return 0.0


def lamp_less_red_dependency(time):
    if time <= 5:
        return 1.0
    if 5 <= time <= 10:
        return (10 - time) / 5.0
    return 0.0


def lamp_less_green_dependency(time):
    if 0 <= time <= 5:
        return 1.0
    if 5 <= time <= 10:
        return (10 - time) / 5.0
    return 0.0


def lamp_green_dependency(time):
    if time >= 10:
        return 1.0
    if 5 <= time <= 10:
        return (time - 5) / 5.0
    return 0.0


# speed dependency
def speed_stop_dependency(speed):
    if speed == 0:
        return 1.0
    if 0 < speed < 0.1:
        return (0.1 - speed) / 0.1
    return 0.0


def speed_slow_dependency(speed):
    if 0 <= speed <= 0.5:
        return speed / 0.5
    if 0.5 <= speed <= 1:
        return (1 - speed) / 0.5
    return 0.0


def speed_slower_dependency(speed):
    if 0.5 <= speed <= 1:
        return (speed - 0.5) / 0.5
    if 1 <= speed <= 1.5:
        return (1.5 - speed) / 0.5
    return 0


def speed_fast_dependency(speed):
    if speed >= 1.5:
        return 1.0
    if 1 <= speed <= 1.5:
        return (speed - 1) / 0.5
    return 0.0


# calculate distance dependency
def cal_distance_dependencies(distance):
    distance_dependencies = []
    if distance_near_dependency(distance) > 0:
        distance_dependencies.append((DISTANCE_NEAR, distance_near_dependency(distance)))
    if distance_medium_dependency(distance) > 0:
        distance_dependencies.append((DISTANCE_MEDIUM, distance_medium_dependency(distance)))
    if distance_far_dependency(distance) > 0:
        distance_dependencies.append((DISTANCE_FAR, distance_far_dependency(distance)))
    return distance_dependencies


# calculate angle dependencies
def cal_angle_dependencies(angle):
    angle_dependencies = []
    if angle_small_dependency(angle) > 0:
        angle_dependencies.append((ANGLE_SMALL, angle_small_dependency(angle)))
    if angle_medium_dependency(angle) > 0:
        angle_dependencies.append((ANGLE_MEDIUM, angle_medium_dependency(angle)))
    if angle_big_dependency(angle) > 0:
        angle_dependencies.append((ANGLE_BIG, angle_big_dependency(angle)))
    return angle_dependencies


# calculate lamp dependencies
def cal_lamp_dependencies(lamp_status):
    lamp_dependencies = []
    time = lamp_status[0]
    status = lamp_status[1]
    if status == 1:
        if lamp_green_dependency(time) > 0:
            lamp_dependencies.append((GREEN, lamp_green_dependency(time)))
        if lamp_less_green_dependency(time) > 0:
            lamp_dependencies.append((LESS_GREEN, lamp_less_green_dependency(time)))
    if status == 2:
        if lamp_red_dependency(time) > 0:
            lamp_dependencies.append((RED, lamp_red_dependency(time)))
        if lamp_less_red_dependency(time) > 0:
            lamp_dependencies.append((LESS_RED, lamp_less_red_dependency(time)))
    return lamp_dependencies
