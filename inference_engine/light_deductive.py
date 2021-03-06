from fuzzification.fuzzy_dependency import *
from fuzzy_rule_base.read_rule import *

df_initial_values = read_fuzzy_initial_values()
df_fuzzy_values = read_fuzzy_values()

start, stop, step = query_fuzzy_values(df_initial_values, 'speedo')
speedo = np.arange(start, stop, step)
stop   = fuzz.trimf(speedo, query_fuzzy_individual_values(df_fuzzy_values, 'speedo_stop', required_cols=3))
slow   = fuzz.trimf(speedo, query_fuzzy_individual_values(df_fuzzy_values, 'speedo_slow', required_cols=3))
slower = fuzz.trimf(speedo, query_fuzzy_individual_values(df_fuzzy_values, 'speedo_slower', required_cols=3))
fast   = fuzz.trapmf(speedo,query_fuzzy_individual_values(df_fuzzy_values, 'speedo_fast'))

def speed_type(speedvalue, speedtype):
    if speedtype == "Fast":
        new_arg = fuzz.interp_universe(speedo, fast, speedvalue)[-1]
        tip_fast = np.fmin(fast, speedvalue)
        try:
            res = fuzz.defuzz(speedo, tip_fast, 'centroid')
        except:
            return new_arg, 0
    elif speedtype == "Slower":
        new_arg = fuzz.interp_universe(speedo, slower, speedvalue)[-1]
        tip_slower = np.fmin(slower, speedvalue)
        try:
            res = fuzz.defuzz(speedo, tip_slower, 'centroid')
        except:
            return new_arg, 0
    elif speedtype == "Slow":
        new_arg = fuzz.interp_universe(speedo, slow, speedvalue)[-1]
        tip_slow = np.fmin(slow, speedvalue)
        try:
            res = fuzz.defuzz(speedo, tip_slow, 'centroid')
        except:
            return new_arg, 0
    elif speedtype == "Stop":
        new_arg = fuzz.interp_universe(speedo, stop, speedvalue)[-1]
        tip_stop = np.fmin(stop, speedvalue)
        try:
            res = fuzz.defuzz(speedo, tip_stop, 'centroid')
        except:
            return new_arg, 0
    return new_arg, res

class LightDeductive:
    def __init__(self):
        self.rules = read_light_rule()

    def find_light_rule(self, distance_dependency, light_dependency, angle_dependency):
        for rule in self.rules:
            if distance_dependency[0] == rule[0] and light_dependency[0] == rule[1] and angle_dependency[0] == rule[2]:
                return [distance_dependency, light_dependency, angle_dependency, rule[3]]
        return None

    # calculate arguments for integral function
    def cal_function_arguments(self, distance_dependency, light_dependency, angle_dependency):
        for rule in self.rules:
            if distance_dependency[0] == rule[0] and light_dependency[0] == rule[1] and angle_dependency[0] == rule[2]:
                dependencies = [distance_dependency[1], light_dependency[1], angle_dependency[1]]
                min_arg = min(dependencies)
                label = rule[3]
                new_arguments = []
                new_arg_1, res_1 = speed_type(min_arg, label)
                new_arguments.append(new_arg_1)
                return [new_arguments, label, min_arg], res_1

        return [0, "Stop", 1], 0

    def fuzzy_deductive(self, distance, light_status, angle):
        distance_dependencies = cal_distance_dependencies(distance)
        light_dependencies = cal_lamp_dependencies(light_status)
        angle_dependencies = cal_angle_dependencies(angle)
        print(distance_dependencies, light_dependencies, angle_dependencies)
        speed_total = 0
        weight_total = 0
        for distance_dependency in distance_dependencies:
            for light_dependency in light_dependencies:
                for angle_dependency in angle_dependencies:
                    arguments_func, res_1 = self.cal_function_arguments(distance_dependency, light_dependency, angle_dependency)
                    weight = arguments_func[2]
                    speed = res_1
                    print(speed, weight)
                    speed_total += speed * weight
                    weight_total += weight
        speed_average = round(speed_total / weight_total, 2)
        return speed_average