import itertools
import json
import pickle
import random
import numpy as np

from GameVisualizer import *
from Hasher import *
from pygame import *
from diplomacy import Game, Power
from collections import defaultdict
from diplomacy.utils.export import to_saved_game_format, load_saved_games_from_disk

def make_new_entry(power_name) -> dict:
    power_posible_orders = {loc: {order: 0 for order in game.get_all_possible_orders()[loc]} for loc in
                            game.get_orderable_locations(power_name)
                            if game.get_all_possible_orders()[loc]}
    # print(power_posible_orders)
    return power_posible_orders
def set_gein(power: Power, phase) -> int:
    reward_swither = {
        "bounce": -2,  # odbicie od w trakcie ataku
        "void": -5,  # źle skierowany rozkaz wsparcia
        "cut": -3,  # armii udaję sie wsparcie <3\
        "no convoy": -3,
        "dislodged": -5,
        "disrupted": 0,
        "": 2  # chyba że ok??
    }
    reward = 0
    if (phase == "M"):
        for order, statuses in game.get_order_status(power.name).items():
            if not statuses:
                reward += 0.1 #udalo sie wykonac akcje
            for status in statuses:
                reward += reward_swither[status.message]
    return reward
def get_hash(power_name) -> str:
    return game.get_hash()
def defualtvalue() -> str:
    return "Not Present"
game = Game()
set_starting_influence(game)
visualizer = GameVisualizer()

q_table = defaultdict(defualtvalue)
for power_name, _ in game.powers.items():
    q_table[power_name] = defaultdict(defualtvalue)
try:
    a_file = open("data.json", "r")
    q_table = json.load(a_file)
    for nations in q_table:
        q_table[nations] = defaultdict(defualtvalue, q_table[nations])  # making deafultdics
    a_file.close()
except:
    print("")
iterator = 0
state = 0
while not game.is_game_done:
    iterator += 1
    visualizer.paint_map(game)

    power_orders = {}
    nation_location_orders = {}
    power_hash = {}
    power_influence = {}
    phase = game.phase_type
    for power_name, power in game.powers.items():
        power_hash[power_name] = get_hash(power_name)
        power_influence[power_name] = power.influence.__len__()
        if q_table[power_name][power_hash[power_name]] == "Not Present":
            q_table[power_name][power_hash[power_name]] = make_new_entry(power_name)
        power_orders[power_name] = []
        nation_location_orders[power_name] = {}
        for loc in game.get_orderable_locations(power_name):
            posible_actions = [order for order in q_table[power_name][power_hash[power_name]][loc]]
            # Wyciągniecie prawdopodobieństwa wybrania danej akcji
            logits = [q_table[power_name][power_hash[power_name]][loc][order] for order in
                      q_table[power_name][power_hash[power_name]][loc]]
            logits_exp = np.exp(logits)
            probs = logits_exp / np.sum(logits_exp)
            # wybranie akcji
            order = np.random.choice(posible_actions, p=probs)
            power_orders[power_name].append(order)
            nation_location_orders[power_name][loc] = order  # potrzebne do obliczania reward
        game.set_orders(power_name, power_orders[power_name])

    visualizer.paint_orders(game)
    game.process()
    # set reward
    for power_name, power in game.powers.items():
        reward = set_gein(power, phase);
        for loc_order in nation_location_orders[power_name].items():
            q_table[power_name][power_hash[power_name]][loc_order[0]][loc_order[1]] += \
                (power.influence.__len__() - power_influence[power_name])*10 + reward

    visualizer.paint_map(game)



    if iterator == 2:
        state += 1
        iterator = 0
        print(state)
        a_file = open("data.json", "w")
        json.dump(q_table, a_file)
        a_file.close()
        game = load_saved_games_from_disk("game.json")[0]

    visualizer.paint_orders(game)

    adjust_influence(game)
