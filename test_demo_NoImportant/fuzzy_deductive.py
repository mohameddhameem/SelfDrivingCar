import xlrd

from defuzzification.speed_calculator import calculate_speed
from fuzzification.fuzzy_dependency import *


# read light rule
def read_light_rule():
    light_rule = []
    with xlrd.open_workbook('media/fuzzy_rule.xlsx') as book:
        sheet = book.sheet_by_index(1)

        distance = [x for x in sheet.col_values(1)]
        light_status = [y for y in sheet.col_values(2)]
        angle = [z for z in sheet.col_values(3)]
        speed = [t for t in sheet.col_values(4)]

        for i in range(1, len(distance)):
            light_rule.append((distance[i].strip(), light_status[i].strip(), angle[i].strip(), speed[i].strip()))

    return light_rule


light_rules = read_light_rule()


# find rule fit with distance, light_status, angle
def find_light_rule(distance_dependency, light_dependency, angle_dependency):
    for rule in light_rules:
        if distance_dependency[0] == rule[0] and light_dependency[0] == rule[1] and angle_dependency[0] == rule[2]:
            return [distance_dependency, light_dependency, angle_dependency, rule[3]]
    return None
