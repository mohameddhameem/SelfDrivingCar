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

def create_interp_membership(calculated_val, val_range, membership_function):
    x = fuzz.interp_membership(val_range, membership_function, calculated_val)
    return x

# calculate distance dependency
def cal_distance_dependencies(distance, dist, dist_near, dist_med, dist_far):
    distance_dependencies = []

    if create_interp_membership(distance, dist, dist_near) > 0:
        distance_dependencies.append((DISTANCE_NEAR, create_interp_membership(distance, dist, dist_near)))
    if create_interp_membership(distance, dist, dist_med) > 0:
        distance_dependencies.append((DISTANCE_MEDIUM, create_interp_membership(distance, dist, dist_med)))
    if create_interp_membership(distance, dist, dist_far) > 0:
        distance_dependencies.append((DISTANCE_FAR, create_interp_membership(distance, dist, dist_far)))
    return distance_dependencies


# calculate angle dependencies
def cal_angle_dependencies(angle, ang, ang_small, ang_med, ang_big):
    angle_dependencies = []

    if create_interp_membership(angle, ang, ang_small) > 0:
        angle_dependencies.append((ANGLE_SMALL, create_interp_membership(angle, ang, ang_small)))
    if create_interp_membership(angle, ang, ang_med) > 0:
        angle_dependencies.append((ANGLE_MEDIUM, create_interp_membership(angle, ang, ang_med)))
    if create_interp_membership(angle, ang, ang_big) > 0:
        angle_dependencies.append((ANGLE_BIG, create_interp_membership(angle, ang, ang_big)))
    return angle_dependencies


# calculate lamp dependencies
def cal_lamp_dependencies(lamp_status, light, light_green, light_greenred, light_redgreen, light_red):
    lamp_dependencies = []
    time = lamp_status[0]
    status = lamp_status[1]

    if status == 1:
        if create_interp_membership(time,  light, light_green) > 0:
            lamp_dependencies.append((GREEN, create_interp_membership(time,  light, light_green)))
        if create_interp_membership(time,  light, light_greenred) > 0:
            lamp_dependencies.append((LESS_GREEN, create_interp_membership(time,  light, light_greenred)))
    if status == 2:
        if create_interp_membership(time, light, light_red) > 0:
            lamp_dependencies.append((RED, create_interp_membership(time, light, light_red)))
        if create_interp_membership(time, light, light_redgreen) > 0:
            lamp_dependencies.append((LESS_RED, create_interp_membership(time, light, light_redgreen)))
    return lamp_dependencies