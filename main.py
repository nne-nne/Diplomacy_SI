import random
import sys
import pygame
from pygame import *
import pygame.gfxdraw
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


def draw_tinted(img, col, pos=(0,0)):
    tinted = img.convert_alpha()
    tinted.fill(col, None, BLEND_RGBA_MULT)
    screen.blit(tinted, pos)


def set_starting_influence():
    game.get_power('AUSTRIA').influence.extend(['GAL', 'BOH', 'TYR'])
    game.get_power('ENGLAND').influence.extend(['CLY', 'YOR', 'WAL'])
    game.get_power('FRANCE').influence.extend(['BUR', 'GAS', 'PIC'])
    game.get_power('GERMANY').influence.extend(['RUH', 'PRU', 'SIL'])
    game.get_power('ITALY').influence.extend(['PIE', 'TUS', 'APU'])
    game.get_power('RUSSIA').influence.extend(['LVN', 'UKR', 'FIN'])
    game.get_power('TURKEY').influence.extend(['SYR', 'ARM'])


def adjust_influence():
    for i in range(0, len(power_names)):
        cur_power = game.get_power(power_names[i])
        for terit in cur_power.influence:
            if terit in game.map.scs and terit not in cur_power.centers:
                cur_power.influence.remove(terit)
        for terit in cur_power.centers:
            if terit not in cur_power.influence:
                cur_power.influence.append(terit)



# Creating a game
# Alternatively, a map_name can be specified as an argument. e.g. Game(map_name='pure')
game = Game()
set_starting_influence()
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
    'ARM': (964, 642),
    'BAL': (573, 357),
    'BAR': (773, 23),
    'BEL': (387, 424),
    'BER': (564, 393),
    'BLA': (849, 603),
    'BOH': (561, 495),
    'BOT': (635, 266),
    'BRE': (284, 464),
    'BUD': (654, 566),
    'BUL/EC': (746, 634),
    'BUL/SC': (710, 672),
    'BUL': (719, 635),
    'BUR': (412, 495),
    'CLY': (324, 269),
    'CON': (775, 685),
    'DEN': (502, 328),
    'EAS': (795, 808),
    'EDI': (349, 281),
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
    'MAR': (371, 582),
    'MOS': (758, 364),
    'MUN': (491, 491),
    'NAF': (271, 772),
    'NAO': (180, 159),
    'NAP': (562, 714),
    'NWY': (492, 249),
    'NTH': (410, 297),
    'NWG': (472, 34),
    'PAR': (364, 489),
    'PIC': (358, 451),
    'PIE': (448, 571),
    'POR': (154, 597),
    'PRU': (617, 390),
    'ROM': (502, 645),
    'RUH': (440, 458),
    'RUM': (741, 592),
    'SER': (646, 630),
    'SEV': (843, 520),
    'SIL': (567, 444),
    'SKA': (506, 284),
    'SMY': (827, 730),
    'SPA/NC': (209, 554),
    'SPA/SC': (240, 688),
    'SPA': (250, 628),
    'STP/NC': (780, 164),
    'STP/SC': (725, 267),
    'STP': (783, 237),
    'SWE': (576, 263),
    'SYR': (934, 766),
    'TRI': (574, 610),
    'TUN': (426, 774),
    'TUS': (478, 617),
    'TYR': (500, 535),
    'TYS': (486, 694),
    'UKR': (772, 466),
    'VEN': (494, 584),
    'VIE': (591, 540),
    'WAL': (307, 378),
    'WAR': (630, 437),
    'WES': (299, 705),
    'YOR': (347, 365),
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
shield = image.load('shield.png')
arrow = image.load('arrow.png')

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
        # print(game.get_power(power_names[i]).units)
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


def midpoint(p1, p2):
    return (p1[0] + p2[0])//2, (p1[0] + p2[0])//2


# def arrow(p1, p2, col):
   # m1 = midpoint(p1, p2)
   # pygame.gfxdraw.bezier(screen, (p1, m1, p2), 5, col)


def trigon(p1, p2, col):
    if p2[1] - p1[1] == 0:
        pygame.gfxdraw.filled_trigon(p1[0], p1[1]+10, p1[0], p1[0]-10, p2[0], p2[1], (0, 0, 0, 255))
        pygame.gfxdraw.filled_trigon(p1[0], p1[1]+7, p1[0], p1[0]-7, p2[0], p2[1], col)
    if p2[0]-p1[0] == 0:
        u = 0
    else:
        a = (p2[1]-p1[1])/(p2[0]-p1[0])
        u = -1/a


def draw_arrow_nieeeee(s, d):
    w = 10
    if d[0] == s[0]:
        a = 'INF'
        u = 0
    elif d[1] == s[1]:
        a = 0
        u = 'INF'
    else:
        a = (d[1] - s[1])/(d[0] - s[0])
        u = -1/a
    print(w, " ", a, " ", u)


def dir_v(s, d):
    x = d[0] - s[0]
    y = d[1] - s[1]
    return x, y


def interpolation(s, d, v):
    direction = dir_v(s, d)
    return v*direction[0], v*direction[1]


def draw_arrow(s, d, col):
    direction = dir_v(s, d)
    udir = direction[1], -direction[0]
    m1 = s[0]+0.75*direction[0] - 0.05*udir[0], s[1]+0.75*direction[1] -0.05*udir[1]
    m2 = s[0]+0.75*direction[0] + 0.05*udir[0], s[1]+0.75*direction[1] +0.05*udir[1]
    mcol = col[0], col[1], col[2], 180
    pygame.gfxdraw.filled_polygon(screen, (s, m1, d, m2), (0, 0, 0, 255))
    pygame.gfxdraw.filled_polygon(screen, (s, m1, d, m2), mcol)


def paint_orders():
    for i in range(0, len(power_names)):
        for order in game.get_orders(power_names[i]):
            # print(order)
            sp = order.split(' ')
            if sp[2] == 'H':
                draw_tinted(shield, power_colors[i], army_positions.get(sp[1]))
                # print("hold at ", sp[1], " ", army_positions.get(sp[1]))
            elif sp[2] == '-':
                # draw_tinted(arrow, power_colors[i], army_positions.get(sp[3]))
                draw_arrow(army_positions.get(sp[1]), army_positions.get(sp[3]), power_colors[i])
                # arrow(army_positions.get(sp[1]), army_positions.get(sp[3]), power_colors[i])
            elif sp[2] == 'S':
                mypos = army_positions.get(sp[1])
                if len(sp) == 5:
                    supported = army_positions.get(sp[3])
                    # print(dir_v(mypos, supported))
                    # draw_arrow(mypos, supported, power_colors[i])
                    # draw_tinted(shield, power_colors[i], interpolation(mypos, supported, 0.5))
                else:
                    supported = army_positions.get(sp[4])
                    # target = army_positions.get(sp[6])
                    # draw_arrow(mypos, interpolation(supported, target, 0.7), power_colors[i])
    display.update()


while not game.is_game_done:
    paint_map()
    # Getting the list of possible orders for all locations
    possible_orders = game.get_all_possible_orders()
    # print(game.get_state())
    # print(game.get_all_possible_orders())
    wait_for_any_key()

    print(game.get_all_possible_orders())
    print(game.build_caches())
    # For each power, randomly sampling a valid order
    for power_name, power in game.powers.items():
        # print(game.get_orderable_locations(power_name))
        power_orders = [random.choice(possible_orders[loc]) for loc in game.get_orderable_locations(power_name)
                        if possible_orders[loc]]
        game.set_orders(power_name, power_orders)

    paint_orders()
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
    # print(game.get_current_phase())
    game.process()
    adjust_influence()

    # print('Russian centres:', game.get_centers('RUSSIA'))
    # print(game.get_all_possible_orders())
    # print(game.get_units('GERMANY'))
    # print(game.get_map_power_names())
# to_saved_game_format(game, output_path='game.json')

