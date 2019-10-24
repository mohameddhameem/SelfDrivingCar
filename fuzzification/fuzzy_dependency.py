import numpy as np
import skfuzzy as fuzz

from fuzzy_rule_base.read_rule import read_fuzzy_initial_values, read_fuzzy_values, query_fuzzy_individual_values, \
    query_fuzzy_values

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

df_initial_values = read_fuzzy_initial_values()
df_fuzzy_values = read_fuzzy_values()

start, stop, step = query_fuzzy_values(df_initial_values, 'distance')
dist = np.arange(start, stop, step)
dist_near = fuzz.trapmf(dist, query_fuzzy_individual_values(df_fuzzy_values, 'dist_near'))
dist_med = fuzz.trimf(dist, query_fuzzy_individual_values(df_fuzzy_values, 'dist_med', required_cols=3))
dist_far = fuzz.trapmf(dist, query_fuzzy_individual_values(df_fuzzy_values, 'dist_far'))

start, stop, step = query_fuzzy_values(df_initial_values, 'angle')
ang = np.arange(start, stop, step)
ang_small = fuzz.trapmf(ang, query_fuzzy_individual_values(df_fuzzy_values, 'ang_small'))
ang_med = fuzz.trimf(ang, query_fuzzy_individual_values(df_fuzzy_values, 'ang_med', required_cols=3))
ang_big = fuzz.trapmf(ang, query_fuzzy_individual_values(df_fuzzy_values, 'ang_big'))

start, stop, step = query_fuzzy_values(df_initial_values, 'light')
light = np.arange(start, stop, step)
light_red = fuzz.trapmf(light, query_fuzzy_individual_values(df_fuzzy_values, 'light_red'))
light_redgreen = fuzz.trapmf(light, query_fuzzy_individual_values(df_fuzzy_values, 'light_redgreen'))
light_green = fuzz.trapmf(light, query_fuzzy_individual_values(df_fuzzy_values, 'light_green'))
light_greenred = fuzz.trapmf(light, query_fuzzy_individual_values(df_fuzzy_values, 'light_greenred'))


# distance dependency
def distance_near_dependency(distance):
    x = fuzz.interp_membership(dist, dist_near, distance)
    return x


def distance_medium_dependency(distance):
    x = fuzz.interp_membership(dist, dist_med, distance)
    return x


def distance_far_dependency(distance):
    x = fuzz.interp_membership(dist, dist_far, distance)
    return x


# angle dependency
def angle_small_dependency(angle):
    y = fuzz.interp_membership(ang, ang_small, angle)
    return y


def angle_medium_dependency(angle):
    y = fuzz.interp_membership(ang, ang_med, angle)
    return y


def angle_big_dependency(angle):
    y = fuzz.interp_membership(ang, ang_big, angle)
    return y


# lamp dependency
def lamp_red_dependency(time):
    z = fuzz.interp_membership(light, light_red, time)
    return z


def lamp_less_red_dependency(time):
    z = fuzz.interp_membership(light, light_redgreen, time)
    return z


def lamp_less_green_dependency(time):
    z = fuzz.interp_membership(light, light_greenred, time)
    return z


def lamp_green_dependency(time):
    z = fuzz.interp_membership(light, light_green, time)
    return z


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