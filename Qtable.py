import json
import random

import numpy as np
from collections import defaultdict
from diplomacy import Game, Power

from Hasher import get_hash


class LastPhaseInfo:
    def __init__(self):
        self.phase = ""
        self.nation_location_orders = {}
        self.power_influence = {}
        self.power_hash = {}


class QtableHandler:
    def __init__(self, game: Game, agent_powers: list):
        self.game = game
        self.miss_hits = 0
        self.attempts = 0
        self.lastTurnInfo = LastPhaseInfo()
        self.q_table = self.load_q_table()
        self.agent_powers = agent_powers

    def load_q_table(self):
        q_table = defaultdict(self.default_value)
        for power_name, _ in self.game.powers.items():
            q_table[power_name] = defaultdict(self.default_value)
        try:
            a_file = open("data.json", "r")
            q_table = json.load(a_file)
            for nations in q_table:
                q_table[nations] = defaultdict(self.default_value, q_table[nations])  # making deafultdics
            a_file.close()
        except:
            print("File not loaded")
        return q_table

    def chose_orders(self, power_name):
        if power_name in self.agent_powers:
            return self.chose_on_qtable(power_name)
        else:
            self.attempts += 1
            return self.chose_on_random(power_name)

    def chose_on_random(self,power_name):
        possible_orders = self.game.get_all_possible_orders()
        return [random.choice(possible_orders[loc]) for loc in self.game.get_orderable_locations(power_name)
                        if possible_orders[loc]]

    def chose_on_qtable(self,power_name):
        game_hash = self.lastTurnInfo.power_hash[power_name]
        power_orders = []
        nation_location_orders = {}

        if self.q_table[power_name][game_hash] == "Not Present":
            self.q_table[power_name][game_hash] = self.make_new_entry(power_name)
        for loc in self.game.get_orderable_locations(power_name):
            posible_actions = [order for order in self.q_table[power_name][game_hash][loc]]
            # Wyciągniecie prawdopodobieństwa wybrania danej akcji
            logits = [self.q_table[power_name][game_hash][loc][order] for order in
                      self.q_table[power_name][game_hash][loc]]
            if np.sum(logits) != 0:
                logits = logits / np.sum(logits)
            logits_exp = np.exp(logits)
            probs = logits_exp / np.sum(logits_exp)
            # wybranie akcji
            order = np.random.choice(posible_actions, p=probs)
            power_orders.append(str(order))
            nation_location_orders[loc] = str(order)  # potrzebne do obliczania reward

        self.lastTurnInfo.nation_location_orders[power_name] = nation_location_orders
        return power_orders

    def make_new_entry(self, power_name) -> dict:
        self.miss_hits += 1
        power_posible_orders = {loc: {order: 0 for order in self.game.get_all_possible_orders()[loc]} for loc in
                                self.game.get_orderable_locations(power_name)
                                if self.game.get_all_possible_orders()[loc]}
        return power_posible_orders

    def save(self):
        try:
            a_file = open("data.json", "w")
            json.dump(self.q_table, a_file)
            a_file.close()
        except OSError:
            print("Ups coś poszło nie tak z zapisem")

    def set_gain(self, power: Power) -> int:

        reward_swither = {
            "bounce": -2,  # odbicie od w trakcie ataku
            "void": -5,  # źle skierowany rozkaz wsparcia
            "cut": -3,  # armii udaję sie wsparcie <3\
            "no convoy": -3,
            "dislodged": -5,
            "disrupted": 0,
            "": 0  # chyba że ok??
        }
        reward = 0
        if self.lastTurnInfo.phase == "M":
            for order, statuses in self.game.get_order_status(power.name).items():
                if not statuses:
                    reward += 0.1  # udalo sie wykonac akcje
                for status in statuses:
                    reward += reward_swither[status.message]
        return reward

    def set_reward(self):
        for power_name, power in self.game.powers.items():
            if power_name in self.agent_powers:
                reward = self.set_gain(power)
                for loc_order in self.lastTurnInfo.nation_location_orders[power_name].items():
                    self.q_table[power_name][self.lastTurnInfo.power_hash[power_name]][loc_order[0]][loc_order[1]] += \
                        (power.influence.__len__() - self.lastTurnInfo.power_influence[power_name])

    def set_turn_info(self):
        self.lastTurnInfo.phase = self.game.phase_type
        for power_name, power in self.game.powers.items():
            self.lastTurnInfo.power_hash[power_name] = get_hash(self.game, power_name)
            self.lastTurnInfo.power_influence[power_name] = power.influence.__len__()

    def get_accuracy(self):
        return 1 - (self.miss_hits/self.attempts)
    @staticmethod
    def default_value() -> str:
        return "Not Present"
