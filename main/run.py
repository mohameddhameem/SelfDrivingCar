import random, sys, time

sys.path.insert(0, 'D:\\school\\Computational Intelligence II\\tian jing ca\\SelfDrivingCar')

import pygame
from pygame.locals import *
import pandas as pd
import numpy as np
from openpyxl import load_workbook
from pathlib import Path

def make_font(fonts, size):
    available = pygame.font.get_fonts()
    # get_fonts() returns a list of lowercase spaceless font names
    choices = map(lambda x: x.lower().replace(' ', ''), fonts)
    for choice in choices:
        if choice in available:
            return pygame.font.SysFont(choice, size)
    return pygame.font.Font(None, size)


_cached_fonts = {}

def get_font(font_preferences, size):
    global _cached_fonts
    key = str(font_preferences) + '|' + str(size)
    font = _cached_fonts.get(key, None)
    if font == None:
        font = make_font(font_preferences, size)
        _cached_fonts[key] = font
    return font


_cached_text = {}


def create_text(text, fonts, size, color):
    global _cached_text
    key = '|'.join(map(str, (fonts, size, color, text)))
    image = _cached_text.get(key, None)
    if image == None:
        font = get_font(fonts, size)
        image = font.render(text, True, color)
        _cached_text[key] = image
    return image

def main(screen, background, font, CENTER_W, CENTER_H):

    import graphic.camera as camera
    import graphic.maps as maps
    import graphic.stone as stone
    import graphic.traffic_lamp as traffic_lamp
    from graphic import car
    from graphic.car import calculate_angle

    clock = pygame.time.Clock()
    running = True

    cam = camera.Camera()

    stone_impediment = stone.Stone(200, 200, 90, 0)

    map_s = pygame.sprite.Group()
    map_s.add(maps.Map(0, 0, 2))

    start_x = maps.MAP_NAVS[0][0]
    start_y = maps.MAP_NAVS[0][1]
    maps.FINISH_INDEX = len(maps.MAP_NAVS) - 2

    traffic_lamp1 = traffic_lamp.TrafficLamp(maps.TRAFFIC_LAMP_COORDINATES[0])
    traffic_lamp2 = traffic_lamp.TrafficLamp(maps.TRAFFIC_LAMP_COORDINATES[1])

    print(maps.TRAFFIC_LAMP_COORDINATES[0])
    print(maps.TRAFFIC_LAMP_COORDINATES[1])

    start_angle = calculate_angle(maps.MAP_NAVS[0][0],
                                  maps.MAP_NAVS[0][1], maps.MAP_NAVS[1][0], maps.MAP_NAVS[1][1])

    controlled_car = car.Car(start_x, start_y, start_angle)
    cars = pygame.sprite.Group()
    cars.add(controlled_car)

    traffic_lamps = pygame.sprite.Group()
    traffic_lamps.add(traffic_lamp1)
    traffic_lamps.add(traffic_lamp2)

    stones = pygame.sprite.Group()
    stones.add(stone_impediment)

    stone_status = (stone_impediment.status, len(maps.MAP_NAVS) - 1)

    cam.set_pos(controlled_car.x, controlled_car.y)
    flag = 0

    start = pygame.time.get_ticks()

    while running:
        flag += 1
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYUP:
                if keys[K_p]:
                    pass

                if keys[K_q]:
                    pygame.quit()
                    sys.exit(0)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                break

        cam.set_pos(controlled_car.x, controlled_car.y)

        screen.blit(background, (0, 0))

        # update and render map
        map_s.update(cam.x, cam.y)
        map_s.draw(screen)

        # update and render traffic lamps
        traffic_lamps_status = []
        traffic_lamps.update(cam.x, cam.y)
        traffic_lamps.draw(screen)

        stones.update(cam.x, cam.y)
        stones.draw(screen)

        lamp_status1 = traffic_lamp1.render(screen)
        lamp_status2 = traffic_lamp2.render(screen)

        traffic_lamps_status.append(lamp_status1)
        traffic_lamps_status.append(lamp_status2)

        # update and render car
        cars.update(cam.x, cam.y, traffic_lamps_status, stone_status, flag)
        cars.draw(screen)

        ##### Add for timer ~~~

        font_preferences = [
            "Bizarre-Ass Font Sans Serif",
            "They definitely dont have this installed Gothic",
            "Papyrus",
            "Comic Sans MS"]

        counting_time = pygame.time.get_ticks() - start

        # # change milliseconds into minutes, seconds, milliseconds
        counting_minutes = str(int(counting_time / 60000)).zfill(2)
        counting_seconds = str(int((counting_time % 60000) / 1000)).zfill(2)

        counting_string = "%s:%s" % (counting_minutes, counting_seconds)
        font_preferences = ["Comic Sans MS"]

        text = create_text(str(counting_string), font_preferences, 72, (0, 0, 0))

        screen.blit(text, (500, 0))
        text_x = create_text('X ->' + str(controlled_car.x), font_preferences, 20, (3, 252, 78))
        text_y = create_text('Y ->' + str(controlled_car.y), font_preferences, 20, (3, 252, 78))
        text_speed = create_text('Speed ->'+ str(controlled_car.speed), font_preferences, 20, (3, 252, 78))
        screen.blit(text_x, (0,0))
        screen.blit(text_y, (0, 20))
        screen.blit(text_speed, (0, 40))
        # ######

        pygame.display.flip()

        clock.tick(60)

        minutes = int(counting_time / 60000)
        seconds = int((counting_time % 60000) / 1000)
        if controlled_car.x >= 3300 and controlled_car.y >= 1500: 
            travel_time = minutes * 60 + seconds
            return travel_time
        if controlled_car.speed < -100 or controlled_car.speed > 100 or minutes >= 3: # which is highly likely impossible
            return 10000

def get_workbook():
    data_folder = Path("../rule")
    file_to_open = data_folder / 'fuzzy_rule.xlsx' # '../rule/fuzzy_rule.xlsx'
    return file_to_open

def simulate(params): 

    # original: [70, 140, 210, 7, 14, 21, 3, 6, 3, 6, 0.01, 0.5, 1, 1.5]

    if params[1] < params[0] or params[2] < params[1]: 
        print("Problem 1!")
        return 10000
    if params[4] < params[3] or params[5] < params[4]: 
        print("Problem 2!")
        return 10000
    if params[7] < params[6]: 
        print("Problem 3!")
        return 10000
    if params[9] < params[8]: 
        print("Problem 4!")
        return 10000
    if params[12] < params[11] or params[13] < params[12]: 
        print("Problem 5!")
        return 10000

    print("No Problem!")

    A = pd.read_excel(get_workbook(), sheet_name = 'fuzzy_values')

    path = '../rule/fuzzy_rule.xlsx'
    book = load_workbook(get_workbook())
    book.remove_sheet(book.get_sheet_by_name('fuzzy_values'))
    writer = pd.ExcelWriter(path, engine = 'openpyxl')
    writer.book = book

    # 0 - dist_near
    # 1 - dist_med
    # 2 - dist_far
    # 3 - ang_small
    # 4 - ang_med
    # 5 - ang_big
    # 6 - light_red
    # 7 - light_redgreen
    # 8 - light_green
    # 9 - light_greenred
    # 10 - stop
    # 11 - slow
    # 12 - slower
    # 13 - fast

    # params
    #      0         1         2        3         4         5         6        7        8        9        10      11      12      13
    # [(0, 150), (0, 150), (0, 150), (0, 360), (0, 360), (0, 360), (0, 21), (0, 21), (0, 21), (0, 21),  (0, 2), (0, 2), (0, 2), (0, 2)]
    A.loc[0, 'c'] = params[0] # param[0] - reusing value for dist_near C, dist_med A
    A.loc[0, 'd'] = params[1] # param[1] - reusing value for dist_near D, dist_med B, dist_far A
    A.loc[1, 'a'] = params[0]
    A.loc[1, 'b'] = params[1]
    A.loc[1, 'c'] = params[2] # param[2] - reusing value for dist_med C, dist_far B
    A.loc[2, 'a'] = params[1]
    A.loc[2, 'b'] = params[2]
    A.loc[3, 'c'] = params[3] # param[3] - reusing value for ang_small C, ang_med A
    A.loc[3, 'd'] = params[4] # param[4] - reusing value for ang_small D, ang_med B
    A.loc[4, 'a'] = params[3]
    A.loc[4, 'b'] = params[4]
    A.loc[4, 'c'] = params[5]
    A.loc[5, 'a'] = params[4]
    A.loc[5, 'b'] = params[5]
    A.loc[6, 'a'] = params[6]
    A.loc[6, 'b'] = params[7]
    A.loc[7, 'c'] = params[6]
    A.loc[7, 'd'] = params[7]
    A.loc[8, 'a'] = params[8]
    A.loc[8, 'b'] = params[9]
    A.loc[9, 'c'] = params[8]
    A.loc[9, 'd'] = params[9]
    A.loc[10, 'c'] = params[10] # param[10] - value for stop C -> (0, 2)
    A.loc[11, 'b'] = params[11] # param[11] - value for slow B, slower A -> (0, 2)
    A.loc[11, 'c'] = params[12]
    A.loc[12, 'a'] = params[11]
    A.loc[12, 'b'] = params[12]
    A.loc[12, 'c'] = params[13]
    A.loc[13, 'a'] = params[12]
    A.loc[13, 'b'] = params[13]
    
    A.to_excel(writer, sheet_name = 'fuzzy_values', index = False)
    writer.save()
    writer.close()

    try: 
        pygame.init()
        screen = pygame.display.set_mode((1200, 600))
        pygame.display.set_caption("Self Driving Car")
        pygame.mouse.set_visible(True)
        font = pygame.font.Font(None, 24)
        CENTER_W = int(pygame.display.Info().current_w / 2)
        CENTER_H = int(pygame.display.Info().current_h / 2)
        background = pygame.Surface(screen.get_size())
        background = background.convert_alpha(background)
        background.fill((82, 86, 94))
        travel_time = main(screen, background, font, CENTER_W, CENTER_H)
        pygame.quit()
        return travel_time
    except:
        try:
            pygame.quit()
            return 10000
        except:
            return 10000

def de(fobj, bounds, mut=0.8, crossp=0.7, popsize=20, its=1000):
    dimensions = len(bounds)
    pop = np.random.rand(popsize, dimensions)
    min_b, max_b = np.asarray(bounds).T
    diff = np.fabs(min_b - max_b)
    pop_denorm = min_b + pop * diff
    fitness = np.asarray([fobj(ind) for ind in pop_denorm])
    best_idx = np.argmin(fitness)
    best = pop_denorm[best_idx]
    print("DONE")
    for i in range(its):
        for j in range(popsize):
            idxs = [idx for idx in range(popsize) if idx != j]
            a, b, c = pop[np.random.choice(idxs, 3, replace = False)]
            mutant = np.clip(a + mut * (b - c), 0, 1)
            cross_points = np.random.rand(dimensions) < crossp
            if not np.any(cross_points):
                cross_points[np.random.randint(0, dimensions)] = True
            trial = np.where(cross_points, mutant, pop[j])
            trial_denorm = min_b + trial * diff
            f = fobj(trial_denorm)
            if f < fitness[j]:
                fitness[j] = f
                pop[j] = trial
                if f < fitness[best_idx]:
                    best_idx = j
                    best = trial_denorm
        yield best, fitness[best_idx]

if __name__ == '__main__':

    bounds_value = [(0, 150), (0, 150), (0, 150), (0, 360), (0, 360), (0, 360), (0, 21), (0, 21), (0, 21), (0, 21),  (0, 2), (0, 2), (0, 2), (0, 2)]
    listfinal = list(de(simulate, bounds_value, popsize = 3000, its = 2))
    print(listfinal)