import random
import sys

sys.path.insert(0, 'D:\\school\\Computational Intelligence II\\tian jing ca\\SelfDrivingCar')
import pygame
from pygame.locals import *

import graphic.camera as camera
import graphic.maps as maps
import graphic.stone as stone
import graphic.traffic_lamp as traffic_lamp
from graphic import car
from graphic.car import calculate_angle


#####
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


#########

def main():
    clock = pygame.time.Clock()
    running = True

    cam = camera.Camera()

    # traffic_lamp1 = traffic_lamp.TrafficLamp(1610, 420, 90, 0)
    # traffic_lamp2 = traffic_lamp.TrafficLamp(2710, 1520, 90, 1)

    stone_impediment = stone.Stone(200, 200, 90, 0)

    map_s = pygame.sprite.Group()
    map_s.add(maps.Map(0, 0, 2))

    start_x = maps.MAP_NAVS[0][0]
    start_y = maps.MAP_NAVS[0][1]
    maps.FINISH_INDEX = len(maps.MAP_NAVS) - 2

    traffic_lamp1 = traffic_lamp.TrafficLamp(maps.TRAFFIC_LAMP_COORDINATES[0])
    traffic_lamp2 = traffic_lamp.TrafficLamp(maps.TRAFFIC_LAMP_COORDINATES[1])

    print('________')
    print(maps.TRAFFIC_LAMP_COORDINATES[0])
    print(maps.TRAFFIC_LAMP_COORDINATES[1])

    start_angle = calculate_angle(maps.MAP_NAVS[0][0],
                                  maps.MAP_NAVS[0][1], maps.MAP_NAVS[1][0], maps.MAP_NAVS[1][1])
    # print("Start angle: ", start_angle)
    # print("Finish index: ", maps.FINISH_INDEX)

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

    ##
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

            # mouse event

            if event.type == pygame.MOUSEBUTTONDOWN:
                pressed1, pressed2, pressed3 = pygame.mouse.get_pressed()
                #if pressed1:
                #    print("left click")
                #    current_index = controlled_car.current_nav_index
                #    random_index = random.randrange(current_index + 3, current_index + 6)
                #    if random_index <= (len(maps.MAP_NAVS) - 3) and stone_impediment.status == 0:
                #        x = maps.MAP_NAVS[random_index][0]
                #        y = maps.MAP_NAVS[random_index][1]
                #        stone_impediment.switch_status(x, y)
                #        stone_status = (stone_impediment.status, random_index)
                #    else:
                #        stone_impediment.switch_status(0, 0)
                #        stone_status = (0, len(maps.MAP_NAVS) - 1)
                #
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

        # for lamp in traffic_lamps:
        #     lamp_status = lamp.render(screen)
        #     traffic_lamps_status.append(lamp_status)
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

        # change milliseconds into minutes, seconds, milliseconds
        counting_minutes = str(int(counting_time / 60000)).zfill(2)
        counting_seconds = str(int((counting_time % 60000) / 1000)).zfill(2)

        counting_string = "%s:%s" % (counting_minutes, counting_seconds)

        counting_text = font.render(str(counting_string), 1, (0, 0, 0))

        font_preferences = ["Comic Sans MS"]

        text = create_text(str(counting_string), font_preferences, 72, (0, 0, 0))

        screen.blit(text, (500, 0))
        text_x = create_text('X ->' + str(controlled_car.x), font_preferences, 20, (3, 252, 78))
        text_y = create_text('Y ->' + str(controlled_car.y), font_preferences, 20, (3, 252, 78))
        text_speed = create_text('Speed ->'+ str(controlled_car.speed), font_preferences, 20, (3, 252, 78))
        screen.blit(text_x, (0,0))
        screen.blit(text_y, (0, 20))
        screen.blit(text_speed, (0, 40))
        ######

        pygame.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((1200, 600))
    pygame.display.set_caption("Self Driving Car")
    pygame.mouse.set_visible(True)
    font = pygame.font.Font(None, 24)

    CENTER_W = int(pygame.display.Info().current_w / 2)
    CENTER_H = int(pygame.display.Info().current_h / 2)

    # new background surface
    background = pygame.Surface(screen.get_size())
    background = background.convert_alpha(background)
    background.fill((82, 86, 94))

    # main loop
    main()

    pygame.quit()
    sys.exit(0)
