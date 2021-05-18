import pygame
from pygame import *
from DiplomacyHelper import *
import pygame.gfxdraw
import sys
import numpy as np


def dir_vec(s, d):
    x = d[0] - s[0]
    y = d[1] - s[1]
    return x, y

def midpoint(s, d):
    return (s[0] + d[0])/2, (s[1] + d[1])/2

def interpolation(s, d, v):
    direction = dir_vec(s, d)
    return v * direction[0], v * direction[1]


def vec180(vec):
    return -1 * vec[0], -1 * vec[1]

def vec_clockwise90(vec):
    return vec[1], -1 * vec[0]

def vec_counterclockwise90(vec):
    return -1 * vec[1], vec[0]


def vec_of_length(vec, length):
    ratio =  length / np.linalg.norm(vec)
    return vec[0] * ratio, vec[1] * ratio


def move_by_vec(point, vec):
    return point[0]+vec[0], point[1]+vec[1]


def wait_for_any_key():
    while True:
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            if e.type == KEYDOWN:
                return


class VisualTerit:
    def __init__(self, short, position, path=""):
        self.short = short
        self.position = position
        if path != "":
            self.image = image.load(path)


def mantain_window():
    running = True
    while running:
        print("działam sobie")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                pass
        pygame.display.flip()


class GameVisualizer:
    def __init__(self):
        # set canvas size variables
        width = 1100
        height = 825
        self.screen = display.set_mode((width, height))

        pygame.font.init()  # for writing text on the map
        self.myfont = pygame.font.SysFont('arial', 30)
        display.set_caption('DIPLOMACY!')

        self.visual_terits = [VisualTerit('ALB', (0, 0), "classic_terits/alb.png"),
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
        self.power_colors = [(213, 167, 136, 255),
                (156, 78, 101, 255),
                (105, 125, 150, 255),
                (110, 70, 85, 255),
                (175, 157, 103, 255),
                (255, 238, 231, 255),
                (161, 114, 99, 255)]
        self.alt_power_colors = [(231, 231, 153, 255),
                (210, 44, 92, 255),
                (104, 186, 216, 255),
                (144, 96, 118, 255),
                (143, 208, 80, 255),
                (129, 146, 151, 255),
                (206, 130, 82, 255)]
        self.special_colors = {'bcg': (187, 187, 187, 255),
                               'borders': (0, 0, 0, 255),
                               'sea_borders': (255, 255, 255, 130),
                               'neutral': (221, 205, 183, 255)}
        self. army_positions = {
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
        # import images
        self.bcg = image.load('background.bmp')
        self.seaborders = image.load('seaborders.png')
        self.heightmap = image.load('heightmap.png')
        self.papertexture = image.load('newspaper2.png')
        self.mapgizmos = image.load('MapGizmos.png')

    def draw_tinted(self, img, col, pos=(0, 0)):
        tinted = img.convert_alpha()
        tinted.fill(col, None, BLEND_RGBA_MULT)
        self.screen.blit(tinted, pos)

    def draw_army(self, pos, col):
        pygame.draw.circle(self.screen, (0, 0, 0, 255), pos, 9)
        pygame.draw.circle(self.screen, col, pos, 5)

    def draw_fleet(self, pos, col):
        w = 15
        h = 4
        x, y = pos
        pygame.draw.rect(self.screen, (0, 0, 0, 255), (x - w / 2 - 4, y - h / 2 - 4, w + 8, h + 8))
        pygame.draw.rect(self.screen, col, (x - w / 2, y - h / 2, w, h))

    def draw_defense(self, pos, col):
        size = 20
        pygame.draw.rect(self.screen, col, (pos[0] - size/2, pos[1] - size/2, size, size), 5)

    def paint_terits(self, game):
        for t in self.visual_terits:
            neutral = True
            for i in range(0, len(get_power_names(game))):
                if t.short in game.get_power(get_power_names(game)[i]).influence:
                    self.draw_tinted(t.image, self.power_colors[i])
                    neutral = False
                    break
            if neutral:
                self.draw_tinted(t.image, self.special_colors.get('neutral'))

    def paint_troops(self, game):
        for i in range(0, len(get_power_names(game))):
            for unit in game.get_power(get_power_names(game)[i]).units:
                unit_type = unit[0]
                position = self.army_positions.get(unit[2:])
                if unit_type == 'A':
                    self.draw_army(position, self.alt_power_colors[i])
                else:
                    self.draw_fleet(position, self.alt_power_colors[i])

    def paint_map(self, game):
        self.screen.fill(self.special_colors.get('bcg'))
        self.draw_tinted(self.papertexture, (0, 0, 0, 30))
        self.paint_terits(game)
        self.draw_tinted(self.seaborders, self.special_colors.get('sea_borders'))
        self.draw_tinted(self.heightmap, (0, 0, 0, 40))
        self.draw_tinted(self.mapgizmos, self.special_colors.get('borders'))
        textsurface = self.myfont.render(game.get_current_phase(), False, (0, 0, 0))
        self.screen.blit(textsurface, (0, 0))
        self.paint_troops(game)
        display.update()

    def draw_arrow(self, s, d, col):
        width = 10
        direction = dir_vec(s, d)
        udir = vec_counterclockwise90(direction)
        m1 = move_by_vec(s, vec_of_length(udir, width))
        m2 = move_by_vec(d, vec_of_length(udir, width/2))
        mcol = col[0], col[1], col[2], 220
        pygame.gfxdraw.filled_polygon(self.screen, (s, m1, m2), mcol)

    def draw_supp_o(self, source, supported, destination, col):
        joint = move_by_vec(supported, interpolation(supported, destination, 0.7))
        pygame.draw.line(self.screen, col, source, joint, 3)
        pygame.draw.line(self.screen, col, joint, destination, 3)
        pygame.draw.circle(self.screen, col, joint, 6)

    def draw_supp_d(self, source, destination, col):
        size = 6
        step = 10
        vec = dir_vec(source, destination)
        udir = vec_counterclockwise90(vec)
        s = move_by_vec(source, vec_of_length(udir, 5))
        length = np.linalg.norm(vec)
        n = int(length // step)
        for i in range(n):
            pos = move_by_vec(s, interpolation(s, destination, i/n))
            pygame.draw.rect(self.screen, col, (pos[0] - size/2, pos[1] - size/2, size, size), 3)

    def paint_orders(self, game):
        for i in range(0, len(get_power_names(game))):
            for order in game.get_orders(get_power_names(game)[i]):
                sp = order.split(' ')
                unit = self.army_positions.get(sp[1])
                col = self.alt_power_colors[i]
                if sp[2] == 'S': #support...
                    if len(sp) == 7: #...offensive
                        supported = self.army_positions.get(sp[4])
                        target = self.army_positions.get(sp[6])
                        self.draw_supp_o(unit, supported, target, col)
                    else: #...defensive
                        supported = self.army_positions.get(sp[4])
                        self.draw_supp_d(unit, supported, col)
                elif sp[2] == 'H': #hold the position
                    self.draw_defense(unit, col)
                elif sp[2] == '-': #move
                    self.draw_arrow(unit, self.army_positions.get(sp[3]), col)
        display.update()




