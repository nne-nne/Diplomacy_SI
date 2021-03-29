import random
import sys
import pygame
from pygame import *
from diplomacy import Game
from diplomacy.utils.export import to_saved_game_format


# penis
# dupa
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
pygame.font.init()  # for writing text on the map
myfont = pygame.font.SysFont('arial', 30)

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
# borders_color = 160, 130, 109, 180
borders_color = 158, 5, 64, 255
seaborders_color = 255, 255, 255, 130
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

army_positions = {
    'ADR': (552, 631),
    'AEG': (708, 727),
    'ALB': (621, 665),
    'ANK': (877, 650),
    'APU': (577, 684),
    'ARM': (947, 632),
    'BAL': (573, 357),
    'BAR': (773, 23),
    'BEL': (387, 424),
    'BER': (519, 417),
    'BLA': (849, 603),
    'BOH': (561, 495),
    'BOT': (635, 266),
    'BRE': (284, 464),
    'BUD': (654, 566),
    'BUL/EC': (746, 634),
    'BUL/SC': (710, 672),
    'BUL': (719, 635),
    'BUR': (412, 495),
    'CLY': (320, 271),
    'CON': (770, 664),
    'DEN': (502, 328),
    'EAS': (795, 808),
    'EDI': (342, 271),
    'ENG': (300, 428),
    'FIN': (672, 213),
    'GAL': (688, 486),
    'GAS': (306, 552),
    'GRE': (655, 714),
    'HEL': (453, 361),
    'HOL': (430, 394),
    'ION': (601, 747),
    'IRI': (243, 387),
    'KIE': (480, 395),
    'LON': (358, 391),
    'LVN': (680, 320),
    'LVP': (330, 344),
    'LYO': (397, 624),
    'MAO': (61, 508),
    'MAR': (376, 586),
    'MOS': (758, 364),
    'MUN': (491, 491),
    'NAF': (271, 772),
    'NAO': (180, 159),
    'NAP': (562, 714),
    'NWY': (492, 249),
    'NTH': (410, 297),
    'NWG': (472, 34),
    'PAR': (357, 493),
    'PIC': (358, 451),
    'PIE': (448, 571),
    'POR': (154, 597),
    'PRU': (617, 390),
    'ROM': (504, 650),
    'RUH': (0, 0),
    'RUM': (0, 0),
    'SER': (0, 0),
    'SEV': (0, 0),
    'SIL': (0, 0),
    'SKA': (0, 0),
    'SMY': (0, 0),
    'SPA/NC': (0, 0),
    'SPA/SC': (0, 0),
    'SPA': (0, 0),
    'STP/NC': (0, 0),
    'STP/SC': (0, 0),
    'STP': (0, 0),
    'SWE': (0, 0),
    'SYR': (0, 0),
    'TRI': (0, 0),
    'TUN': (0, 0),
    'TUS': (0, 0),
    'TYR': (0, 0),
    'TYS': (0, 0),
    'UKR': (0, 0),
    'VEN': (0, 0),
    'VIE': (0, 0),
    'WAL': (0, 0),
    'WAR': (0, 0),
    'WES': (0, 0),
    'YOR': (0, 0),
}

# set canvas size variables
width = 1100
height = 825

# import images
bcg = image.load('background.bmp')
borders = image.load('borders2.png')
seaborders = image.load('seaborders.png')
heightmap = image.load('heightmap.png')
papertexture = image.load('newspaper2.png')
forts = image.load('forts.png')

# draw canvas
screen = display.set_mode((width, height))
display.set_caption('DIPLOMACY!')


def draw_army(pos, col):
    pygame.draw.circle(screen, (0, 0, 0, 255), pos, 9)
    pygame.draw.circle(screen, col, pos, 5)


def draw_fleet(pos, col):
    w = 15
    h = 4
    x, y = pos
    pygame.draw.rect(screen, (0, 0, 0, 255), (x - w/2 - 4, y - h/2 - 4, w + 8, h + 8))
    pygame.draw.rect(screen, col, (x - w/2, y - h/2, w, h))


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
        neutral = True
        for i in range(0, len(power_names)):
            if t.short in game.get_power(power_names[i]).influence:
                draw_tinted(t.image, power_colors[i])
                neutral = False
                break
        if neutral:
            draw_tinted(t.image, neutral_color)


def paint_troops():
    for i in range(0, len(power_names)):
        print(game.get_power(power_names[i]).units)
        for unit in game.get_power(power_names[i]).units:
            type = unit[0]
            position = army_positions.get(unit[2:])
            if type == 'A':
                draw_army(position, power_colors[i])
            else:
                draw_fleet(position, power_colors[i])


def paint_map():
    screen.fill(bcg_color)
    draw_tinted(papertexture, (0, 0, 0, 30))
    paint_terits()
    draw_tinted(borders, borders_color)
    draw_tinted(seaborders, seaborders_color)
    draw_tinted(heightmap, (0, 0, 0, 40))
    screen.blit(forts, (0, 0))
    textsurface = myfont.render(game.get_current_phase(), False, (0, 0, 0))
    screen.blit(textsurface, (0, 0))
    paint_troops()
    display.update()


while not game.is_game_done:
    paint_map()
    # Getting the list of possible orders for all locations
    possible_orders = game.get_all_possible_orders()
    print(game.get_state())
    print(game.get_all_possible_orders())

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

