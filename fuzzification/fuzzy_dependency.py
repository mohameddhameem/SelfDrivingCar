import numpy as np
import skfuzzy as fuzz
import sys

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
def distance_near_dependency(distance, dist, dist_near):
    x = fuzz.interp_membership(dist, dist_near, distance)
    return x

def distance_medium_dependency(distance, dist, dist_med):
    x = fuzz.interp_membership(dist, dist_med, distance)
    return x


def distance_far_dependency(distance, dist, dist_far):
    x = fuzz.interp_membership(dist, dist_far, distance)
    return x


# angle dependency
def angle_small_dependency(angle, ang, ang_small):
    y = fuzz.interp_membership(ang, ang_small, angle)
    return y


def angle_medium_dependency(angle, ang, ang_med):
    y = fuzz.interp_membership(ang, ang_med, angle)
    return y


def angle_big_dependency(angle, ang, ang_big):
    y = fuzz.interp_membership(ang, ang_big, angle)
    return y


# lamp dependency
def lamp_red_dependency(time, light, light_red):
    z = fuzz.interp_membership(light, light_red, time)
    return z


def lamp_less_red_dependency(time, light, light_redgreen):
    z = fuzz.interp_membership(light, light_redgreen, time)
    return z


def lamp_less_green_dependency(time, light, light_greenred):
    z = fuzz.interp_membership(light, light_greenred, time)
    return z


def lamp_green_dependency(time, light, light_green):
    z = fuzz.interp_membership(light, light_green, time)
    return z


# calculate distance dependency
def cal_distance_dependencies(distance, dist, dist_near, dist_med, dist_far):
    distance_dependencies = []

    if distance_near_dependency(distance, dist, dist_near) > 0:
        distance_dependencies.append((DISTANCE_NEAR, distance_near_dependency(distance, dist, dist_near)))
    if distance_medium_dependency(distance, dist, dist_med) > 0:
        distance_dependencies.append((DISTANCE_MEDIUM, distance_medium_dependency(distance, dist, dist_med)))
    if distance_far_dependency(distance, dist, dist_far) > 0:
        distance_dependencies.append((DISTANCE_FAR, distance_far_dependency(distance, dist, dist_far)))
    return distance_dependencies


# calculate angle dependencies
def cal_angle_dependencies(angle, ang, ang_small, ang_med, ang_big):
    angle_dependencies = []

    if angle_small_dependency(angle, ang, ang_small) > 0:
        angle_dependencies.append((ANGLE_SMALL, angle_small_dependency(angle, ang, ang_small)))
    if angle_medium_dependency(angle, ang, ang_med) > 0:
        angle_dependencies.append((ANGLE_MEDIUM, angle_medium_dependency(angle, ang, ang_med)))
    if angle_big_dependency(angle, ang, ang_big) > 0:
        angle_dependencies.append((ANGLE_BIG, angle_big_dependency(angle, ang, ang_big)))
    return angle_dependencies


# calculate lamp dependencies
def cal_lamp_dependencies(lamp_status, light, light_green, light_greenred, light_redgreen, light_red):
    lamp_dependencies = []
    time = lamp_status[0]
    status = lamp_status[1]

    if status == 1:
        if lamp_green_dependency(time,  light, light_green) > 0:
            lamp_dependencies.append((GREEN, lamp_green_dependency(time,  light, light_green)))
        if lamp_less_green_dependency(time,  light, light_greenred) > 0:
            lamp_dependencies.append((LESS_GREEN, lamp_less_green_dependency(time,  light, light_greenred)))
    if status == 2:
        if lamp_red_dependency(time, light, light_red) > 0:
            lamp_dependencies.append((RED, lamp_red_dependency(time, light, light_red)))
        if lamp_less_red_dependency(time, light, light_redgreen) > 0:
            lamp_dependencies.append((LESS_RED, lamp_less_red_dependency(time, light, light_redgreen)))
    return lamp_dependencies