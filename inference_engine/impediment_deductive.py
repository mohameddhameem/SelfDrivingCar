from fuzzification.fuzzy_dependency import *
from fuzzy_rule_base.read_rule import *

import numpy as np
import skfuzzy as fuzz

class ImpedimentDeductive:
    def __init__(self):
        self.rules = read_impediment_rule()
        df_initial_values = read_fuzzy_initial_values()
        df_fuzzy_values = read_fuzzy_values()

        start, stop, step = query_fuzzy_values(df_initial_values, 'speedo')
        self.speedo = np.arange(start, stop, step)
        self.stop   = fuzz.trimf(self.speedo, query_fuzzy_individual_values(df_fuzzy_values, 'speedo_stop', required_cols=3))
        self.slow   = fuzz.trimf(self.speedo, query_fuzzy_individual_values(df_fuzzy_values, 'speedo_slow', required_cols=3))
        self.slower = fuzz.trimf(self.speedo, query_fuzzy_individual_values(df_fuzzy_values, 'speedo_slower', required_cols=3))
        self.fast   = fuzz.trapmf(self.speedo,query_fuzzy_individual_values(df_fuzzy_values, 'speedo_fast'))

    def find_light_rule(self, distance_dependency, angle_dependency):
        for rule in self.rules:
            if distance_dependency[0] == rule[0] and angle_dependency[0] == rule[1]:
                return [distance_dependency, angle_dependency, rule[2]]
        return None

    def speed_type(speedvalue, speedtype): 
        if speedtype == "Fast": 
            new_arg = fuzz.interp_universe(speedo, fast, speedvalue)[-1]
            tip_fast = np.fmin(fast, new_arg)
            try:
                res = fuzz.defuzz(speedo, tip_fast, 'centroid')
            except:
                return new_arg, 0
        elif speedtype == "Slower":
            new_arg = fuzz.interp_universe(speedo, slower, speedvalue)[-1]
            tip_slower = np.fmin(slower, new_arg)
            try:
                res = fuzz.defuzz(speedo, tip_slower, 'centroid')
            except:
                return new_arg, 0
        elif speedtype == "Slow": 
            new_arg = fuzz.interp_universe(speedo, slow, speedvalue)[-1]
            tip_slow = np.fmin(slow, new_arg)
            try:
                res = fuzz.defuzz(speedo, tip_slow, 'centroid')
            except:
                return new_arg, 0
        elif speedtype == "Stop": 
            new_arg = fuzz.interp_universe(speedo, stop, speedvalue)[-1]
            tip_stop = np.fmin(stop, new_arg)
            try:
                res = fuzz.defuzz(speedo, tip_stop, 'centroid')
            except:
                return new_arg, 0
        return new_arg, res

    # calculate arguments for integral function
    def cal_function_arguments(self, distance_dependency, angle_dependency):
        for rule in self.rules:
            if distance_dependency[0] == rule[0] and angle_dependency[0] == rule[1]:
                dependencies = [distance_dependency[1], angle_dependency[1]]
                min_arg = min(dependencies)
                label = rule[2]
                new_arguments = []
                print("label ")
                print(label)
                new_arg_1, res_1 = self.speed_type(min_arg, label)
                new_arguments.append(new_arg_1)
                return [new_arguments, label, min_arg]

        return [0, "Stop", 1]

    def fuzzy_deductive(self, distance, angle):
        distance_dependencies = cal_distance_dependencies(distance)
        angle_dependencies = cal_angle_dependencies(angle)
        speed_total = 0
        weight_total = 0
        for distance_dependency in distance_dependencies:
            for angle_dependency in angle_dependencies:
                arguments_func, speed = self.cal_function_arguments(distance_dependency, angle_dependency)
                weight = arguments_func[2]
                speed_total += speed * weight
                weight_total += weight

        speed_average = round(speed_total / weight_total, 2)
        return speed_average
