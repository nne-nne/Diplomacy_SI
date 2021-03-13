import random
import sys
import pygame
from pygame import *
from diplomacy import Game
from diplomacy.utils.export import to_saved_game_format

#penis
class VisualTerit:
    def __init__(self, short, position, path=""):
        self.short = short
        self.position = position
        if path != "":
            self.image = image.load(path)


def draw_tinted(img, col):
    tinted = img.convert_alpha()
    tinted.fill(col, None, BLEND_RGBA_MULT)
    screen.blit(tinted, (0, 0))


def adjust_influence():
    game.get_power('AUSTRIA').influence.extend(['GAL', 'BOH', 'TYR'])
    game.get_power('ENGLAND').influence.extend(['CLY', 'YOR', 'WAL'])
    game.get_power('FRANCE').influence.extend(['BUR', 'GAS', 'PIC'])
    game.get_power('GERMANY').influence.extend(['RUH', 'PRU', 'SIL'])
    game.get_power('ITALY').influence.extend(['PIE', 'TUS', 'APU'])
    game.get_power('RUSSIA').influence.extend(['LVN', 'UKR', 'FIN'])
    game.get_power('TURKEY').influence.extend(['SYR', 'ARM'])


# Creating a game
# Alternatively, a map_name can be specified as an argument. e.g. Game(map_name='pure')
game = Game()
adjust_influence()
power_names = ['AUSTRIA',
               'ENGLAND',
               'FRANCE',
               'GERMANY',
               'ITALY',
               'RUSSIA',
               'TURKEY']

power_colors = [(213, 167, 136, 255),
                (156, 78, 101, 255),
                (105, 125, 150, 255),
                (110, 70, 85, 255),
                (175, 157, 103, 255),
                (255, 238, 231, 255),
                (161, 114, 99, 255)]
bcg_color = 187, 187, 187, 255
borders_color = 160, 130, 109, 180
neutral_color = 221, 205, 183, 255

visual_terits = [VisualTerit('ALB', (0, 0), "classic_terits/alb.png"),
                 VisualTerit('ANK', (0, 0), "classic_terits/ank.png"),
                 VisualTerit('APU', (0, 0), "classic_terits/apu.png"),
                 VisualTerit('ARM', (0, 0), "classic_terits/arm.png"),
                 VisualTerit('BEL', (0, 0), "classic_terits/bel.png"),
                 VisualTerit('BER', (0, 0), "classic_terits/ber.png"),
                 VisualTerit('BOH', (0, 0), "classic_terits/boh.png"),
                 VisualTerit('BRE', (0, 0), "classic_terits/bre.png"),
                 VisualTerit('BUD', (0, 0), "classic_terits/bud.png"),
                 VisualTerit('BUL', (0, 0), "classic_terits/bul.png"),
                 VisualTerit('BUR', (0, 0), "classic_terits/bur.png"),
                 VisualTerit('CLY', (0, 0), "classic_terits/cly.png"),
                 VisualTerit('CON', (0, 0), "classic_terits/sta.png"),
                 VisualTerit('DEN', (0, 0), "classic_terits/den.png"),
                 VisualTerit('EDI', (0, 0), "classic_terits/edi.png"),
                 VisualTerit('FIN', (0, 0), "classic_terits/fin.png"),
                 VisualTerit('GAL', (0, 0), "classic_terits/gal.png"),
                 VisualTerit('GAS', (0, 0), "classic_terits/gas.png"),
                 VisualTerit('GRE', (0, 0), "classic_terits/gre.png"),
                 VisualTerit('HOL', (0, 0), "classic_terits/hol.png"),
                 VisualTerit('KIE', (0, 0), "classic_terits/kie.png"),
                 VisualTerit('SMY', (0, 0), "classic_terits/kon.png"),
                 VisualTerit('LON', (0, 0), "classic_terits/lon.png"),
                 VisualTerit('LVN', (0, 0), "classic_terits/lvn.png"),
                 VisualTerit('LVP', (0, 0), "classic_terits/lvp.png"),
                 VisualTerit('MAR', (0, 0), "classic_terits/mar.png"),
                 VisualTerit('MOS', (0, 0), "classic_terits/mos.png"),
                 VisualTerit('MUN', (0, 0), "classic_terits/mun.png"),
                 VisualTerit('NAF', (0, 0), "classic_terits/naf.png"),
                 VisualTerit('NAP', (0, 0), "classic_terits/nap.png"),
                 VisualTerit('NWY', (0, 0), "classic_terits/nwy.png"),
                 VisualTerit('PAR', (0, 0), "classic_terits/par.png"),
                 VisualTerit('PIC', (0, 0), "classic_terits/pic.png"),
                 VisualTerit('PIE', (0, 0), "classic_terits/pie.png"),
                 VisualTerit('POR', (0, 0), "classic_terits/por.png"),
                 VisualTerit('PRU', (0, 0), "classic_terits/pru.png"),
                 VisualTerit('ROM', (0, 0), "classic_terits/rom.png"),
                 VisualTerit('RUH', (0, 0), "classic_terits/ruh.png"),
                 VisualTerit('RUM', (0, 0), "classic_terits/rum.png"),
                 VisualTerit('SER', (0, 0), "classic_terits/ser.png"),
                 VisualTerit('SEV', (0, 0), "classic_terits/sev.png"),
                 VisualTerit('SIL', (0, 0), "classic_terits/sil.png"),
                 VisualTerit('SPA', (0, 0), "classic_terits/spa.png"),
                 VisualTerit('STP', (0, 0), "classic_terits/stp.png"),
                 VisualTerit('SWE', (0, 0), "classic_terits/swe.png"),
                 VisualTerit('SYR', (0, 0), "classic_terits/syr.png"),
                 VisualTerit('TRI', (0, 0), "classic_terits/tri.png"),
                 VisualTerit('TUN', (0, 0), "classic_terits/tun.png"),
                 VisualTerit('TUS', (0, 0), "classic_terits/tus.png"),
                 VisualTerit('TYR', (0, 0), "classic_terits/tyr.png"),
                 VisualTerit('UKR', (0, 0), "classic_terits/ukr.png"),
                 VisualTerit('VEN', (0, 0), "classic_terits/ven.png"),
                 VisualTerit('VIE', (0, 0), "classic_terits/vie.png"),
                 VisualTerit('WAL', (0, 0), "classic_terits/wal.png"),
                 VisualTerit('WAR', (0, 0), "classic_terits/war.png"),
                 VisualTerit('YOR', (0, 0), "classic_terits/yor.png")]

# set canvas size variables
width = 1100
height = 825

# import images
bcg = image.load('background.bmp')
borders = image.load('map.png')

# draw canvas
screen = display.set_mode((width, height))
display.set_caption('DIPLOMACY!')


def wait_for_any_key():
    while True:
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            if e.type == KEYDOWN:
                return


def paint_terits():
    for t in visual_terits:
        draw_tinted(t.image, neutral_color)
        for i in range(0, len(power_names)):
            if t.short in game.get_power(power_names[i]).influence:
                draw_tinted(t.image, power_colors[i])
                break


def paint_map():
    screen.fill(bcg_color)
    paint_terits()
    draw_tinted(borders, borders_color)
    display.update()


while not game.is_game_done:
    paint_map()
    # Getting the list of possible orders for all locations
    possible_orders = game.get_all_possible_orders()

    # For each power, randomly sampling a valid order
    for power_name, power in game.powers.items():
        power_orders = [random.choice(possible_orders[loc]) for loc in game.get_orderable_locations(power_name)
                        if possible_orders[loc]]
        game.set_orders(power_name, power_orders)

    # Messages can be sent locally with game.add_message
    # e.g. game.add_message(Message(sender='FRANCE',
    #                               recipient='ENGLAND',
    #                               message='This is a message',
    #                               phase=self.get_current_phase(),
    #                               time_sent=int(time.time())))
    wait_for_any_key()
    # Processing the game to move to the next phase
    # print(game.get_orders('GERMANY'))
    print("next phase")
    print(game.get_current_phase())
    game.process()
    # print('Russian centres:', game.get_centers('RUSSIA'))
    # print(game.get_all_possible_orders())
    # print(game.get_units('GERMANY'))
    # print(game.get_map_power_names())
# to_saved_game_format(game, output_path='game.json')

