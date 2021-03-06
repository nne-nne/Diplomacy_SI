import json
import math
import random

import numpy as np
from collections import defaultdict
from diplomacy import Game, Power

from Hasher import get_hash
from DiplomacyHelper import*


class LastPhaseInfo:
    def __init__(self):
        self.phase = ""
        self.nation_location_orders = {}
        self.power_influence = {}
        self.power_scs = {}
        self.power_hash = {}


class QtableHandler:
    def __init__(self, game: Game, agent_powers: list, min_learnig_rate=0.1, randomizer=0.01):
        self.randomizer = randomizer
        self.min_learnig_rate = min_learnig_rate
        self.interation_number = 0
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
        if self.lastTurnInfo.phase != "M":
            return self.chose_on_random(power_name, validate=False)

        if power_name in self.agent_powers:
            self.attempts += 1
            if random.random() < self.randomizer:
                return self.chose_on_random(power_name)
            orders = self.chose_on_qtable(power_name)
        else:
            orders = self.chose_on_random(power_name)
        return orders

    def chose_on_random(self, power_name, validate=True):
        game_hash = self.lastTurnInfo.power_hash[power_name]
        power_orders = []
        nation_location_orders = {}
        if self.q_table[power_name][game_hash] == "Not Present":
            self.q_table[power_name][game_hash] = self.make_new_entry(power_name)
        for loc in self.game.get_orderable_locations(power_name):
            possible_orders = self.game.get_all_possible_orders()[loc]
            if validate:
                order = random_valid_order(possible_orders, power_orders)
            else:
                order = random.choice(possible_orders)
            power_orders.append(str(order))
            nation_location_orders[loc] = str(order)
        self.lastTurnInfo.nation_location_orders[power_name] = nation_location_orders
        return power_orders
    def debug(self, probs) -> bool:
        for prob in probs:
            if math.isnan(prob):
                return True
        return False
    def chose_on_qtable(self, power_name):
        game_hash = self.lastTurnInfo.power_hash[power_name]
        power_orders = []
        nation_location_orders = {}

        if self.q_table[power_name][game_hash] == "Not Present":
            self.q_table[power_name][game_hash] = self.make_new_entry(power_name)
        for loc in self.game.get_orderable_locations(power_name):
            posible_actions = [order for order in self.q_table[power_name][game_hash][loc]]
            # Wyci??gniecie prawdopodobie??stwa wybrania danej akcji
            logits = [self.q_table[power_name][game_hash][loc][order] for order in
                      self.q_table[power_name][game_hash][loc]]
            if np.sum(np.abs(logits)) != 0:
                logits = logits / np.sum(np.abs(logits))
            logits_exp = np.exp(logits)
            probs = logits_exp / np.sum(logits_exp)
            # wybranie akcji
            order = choose_valid_order(posible_actions, power_orders, probs)
            power_orders.append(str(order))
            nation_location_orders[loc] = str(order)  # potrzebne do obliczania reward

        self.lastTurnInfo.nation_location_orders[power_name] = nation_location_orders
        return power_orders
    def chose_best(self, power_name):
        game_hash = self.lastTurnInfo.power_hash[power_name]
        power_orders = []

        if self.q_table[power_name][game_hash] == "Not Present":
            self.q_table[power_name][game_hash] = self.make_new_entry(power_name)

        for loc in self.game.get_orderable_locations(power_name):
            posible_actions = [order for order in self.q_table[power_name][game_hash][loc]]
            # Wyci??gniecie prawdopodobie??stwa wybrania danej akcji
            logits = [self.q_table[power_name][game_hash][loc][order] for order in
                      self.q_table[power_name][game_hash][loc]]
            # wybranie akcji
            order = posible_actions[logits.index(max(logits))]
            power_orders.append(str(order))
        return power_orders

    def make_new_entry(self, power_name) -> dict:
        if power_name in self.agent_powers and self.lastTurnInfo.phase == "M":
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
            print("Ups co?? posz??o nie tak z zapisem")

    def set_gain(self, power_name, order, self_orders) -> int:
        order_type = get_order_type(order[1])
        if order_type == 'H':
            # nagradzany je??li:
            # zosta?? zaatakowany przez przeciwnika, tym bardziej je??li wytrzyma?? atak, tym bardziej je??li broni miasta
            # karany je??li:
            # nikt go nie zaatakowa?? - zapewne broni?? si?? niepotrzebnie
            # nie obroni??. Lekko po ??apach, bo jest mo??liwo????, ??e po prostu zabrak??o wsparcia
            if exist_enemy_order(self.game, self.lastTurnInfo, power_name, order[0], ['M']):  # zaatakowany
                if order[0] in get_locs_with_units(self.game,
                                                   power_name):  # dalej tam stoi, czyli obroni?? (TODO: sprawdzi?? jak to si?? ma do odwrotu)
                    if get_order_target(order[1]) in self.game.map.scs:  # obroni?? miasto, kozak!
                        return 5
                    else:  # obroni?? terytorium
                        return 3
                else:  # wyrzucili go :'(    ...czy by??o warto broni??? za ma??o danych :/
                    return 1
            else:  # nikt nie atakowa??, bez sensu broni??, kara
                return -2

        elif order_type == 'M':
            # nagradzany je??li:
            # zaj???? nowe miasto (BRAWO!)
            # zablokowa?? ruch przeciwnikowi (ca??kiem spoko, tym bardziej je??li to miasto, a ju?? w og??le je??li w??asne)
            # przeci???? support komu??
            # karany je??li:
            # zrobi?? self bumpa
            # przeci???? sobie support (xD)
            # zaattakowa?? broni??c?? si?? swoj?? jednostk?? (xDDD)
            # pozosta??e ruchy bez nagr??d i kar, neutralne raczej
            target = get_order_target(order[1])
            if exist_own_order_by_loc(self_orders, target, ['H', 'D', 'O']):
                return -5
            elif exist_own_order_by_loc(self_orders, target, ['M']):
                return 0
            elif target in get_locs_with_units(self.game, power_name):  # stoi tam, czyli zdoby??
                if target in self.game.map.scs:  # zaj???? miasto, yahoo!
                    if target not in self.lastTurnInfo.power_scs:  # nie mia?? tego wcze??niej
                        return 8
                    else:
                        return 0
                else:  # zaj???? terytorium nieb??d??ce miastem
                    return 0
            else:  # nie uda??o si?? zdoby??
                if exist_enemy_order(self.game, self.lastTurnInfo, power_name, target, ['M']):  # kto?? inny tam szed??
                    return 4
                elif count_own_orders(self_orders, target, ['M']) > 1:  # bump z w??asn?? jednostk??
                    return -5
                elif exist_own_order_by_loc(self_orders, target, ['H', 'D', 'O']):  # pr??ba ataku na w??asn?? jednostk??
                    return -10
                elif exist_enemy_order_by_loc(self.game, self.lastTurnInfo, power_name, target,
                                              ['D', 'O']):  # przeci???? czyj?? support
                    return 5

        elif order_type == 'O':
            # przy supportach zak??adamy, ??e s?? valid
            # nagradzany je??li:
            # wr??g chcia?? te?? zaj???? t?? prowincj??
            # tym bardziej je??li uda??o si?? nam, a mu nie
            # karany je??li:
            # wspar?? wroga
            # ??aden wr??g nie chcia?? tam wej????
            if not exist_own_order_by_loc(self_orders, order[1].split(' ')[4],
                                          ['M']):  # wspiera?? wroga albo wyimaginowanego przyjaciela
                return -10
            elif exist_enemy_order(self.game, self.lastTurnInfo, power_name, order[0], ['M']):  # wr??g chcia?? tam i????
                if order[0] in self.game.get_orderable_locations(power_name):  # my to zdobyli??my, fajnie
                    return 5
                else:
                    return 1
            else:  # niepotrzebne wsparcie, ??aden wr??g tam nie szed??
                return -3
        elif order_type == 'D':
            # przy supportach zak??adamy, ??e s?? valid
            # nagradzany je??li:
            # wr??g chcia?? zaj???? t?? prowincj??
            # tym bardziej je??li wrogowi si?? nie uda??o
            # karany je??li:
            # wspar?? wroga
            # ??aden wr??g nie zaatakowa??
            if not exist_own_order_by_loc(self_orders, order[1].split(' ')[4],
                                          ['H']):  # wspiera?? wroga albo wyimaginowanego przyjaciela
                return -10
            elif exist_enemy_order(self.game, self.lastTurnInfo, power_name, order[0], ['M']):  # wr??g chcia?? tam i????
                if order[0] in self.game.get_orderable_locations(power_name):  # my tam jeste??my, fajnie
                    return 5
                else:
                    return 1
            else:  # niepotrzebne wsparcie, ??aden wr??g tam nie szed??
                return -1
        else:
            # zero na te konwoje p??ki co
            return 0  # unknown type
        return 0  #

    def set_reward(self):
        for power_name, power in self.game.powers.items():
            last_orders = self.lastTurnInfo.nation_location_orders[power_name].items()
            if power_name in self.agent_powers:
                for loc_order in last_orders:
                    reward = self.set_gain(power_name, loc_order, last_orders)
                    self.q_table[power_name][self.lastTurnInfo.power_hash[power_name]][loc_order[0]][loc_order[1]] += \
                        (power.influence.__len__() - self.lastTurnInfo.power_influence[power_name]) + reward

    def set_turn_info(self):
        self.lastTurnInfo.phase = self.game.phase_type
        for power_name, power in self.game.powers.items():
            self.lastTurnInfo.power_hash[power_name] = get_hash(self.game, power_name)
            self.lastTurnInfo.power_influence[power_name] = power.influence.__len__()
            self.lastTurnInfo.power_scs[power_name] = self.game.get_centers(power_name)

    def get_accuracy(self):
        return 1 - (self.miss_hits / self.attempts) if self.attempts != 0 else "No accuracy"

    @staticmethod
    def default_value() -> str:
        return "Not Present"
