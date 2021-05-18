import json
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
    def __init__(self, game: Game):
        self.game = game
        self.lastTurnInfo = LastPhaseInfo()
        self.q_table = self.load_q_table()
        self.start_value = 100

    def load_q_table(self):
        q_table = defaultdict(self.default_value)
        for power_name, _ in self.game.powers.items():
            q_table[power_name] = defaultdict(self.default_value)
        try:
            a_file = open("orders_values.json", "r")
            q_table = json.load(a_file)
            for nations in q_table:
                q_table[nations] = defaultdict(self.default_value, q_table[nations])  # making deafultdics
            a_file.close()
        except:
            print("table not loaded")
        return q_table

    def choose_order(self, power_name, game_hash, loc):
        posible_actions = [order for order in self.q_table[power_name][game_hash][loc]]
        # Wyciągniecie prawdopodobieństwa wybrania danej akcji
        logits = [self.q_table[power_name][game_hash][loc][order] for order in
                  self.q_table[power_name][game_hash][loc]]
        logits_sum = np.sum(logits)
        if logits_sum != 0:
            probs = logits / np.sum(logits)
        else:
            probs = [1 / len(logits)] * len(logits)  # wszystkie ruchy są jednakowo złe xD
        return np.random.choice(posible_actions, p=probs)


    def chose_orders(self, power_name):
        game_hash = self.lastTurnInfo.power_hash[power_name]
        power_orders = []
        nation_location_orders = {}
        if self.q_table[power_name][game_hash] == "Not Present":
            self.q_table[power_name][game_hash] = self.make_new_entry(power_name)
        for loc in self.game.get_orderable_locations(power_name):
            order = self.choose_order(power_name, game_hash, loc)
            power_orders.append(str(order))
            nation_location_orders[loc] = str(order)  # potrzebne do obliczania reward

        print("power orders: ", power_orders)
        print("support orders: ", filter_support_orders(power_orders))

        self.lastTurnInfo.nation_location_orders[power_name] = nation_location_orders
        return power_orders

    def make_new_entry(self, power_name) -> dict:
        power_posible_orders = {loc: {order: self.start_value for order in self.game.get_all_possible_orders()[loc]} for loc in
                                self.game.get_orderable_locations(power_name)
                                if self.game.get_all_possible_orders()[loc]}
        return power_posible_orders

    def save(self):
        try:
            a_file = open("orders_values.json", "w")
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

    def my_set_gain(self, power_name, order, self_orders)->int:
        order_type = get_order_type(order[1])
        if order_type == 'H':
            # nagradzany jeśli:
                # został zaatakowany przez przeciwnika, tym bardziej jeśli wytrzymał atak, tym bardziej jeśli broni miasta
            # karany jeśli:
                # nikt go nie zaatakował - zapewne bronił się niepotrzebnie
                # nie obronił. Lekko po łapach, bo jest możliwość, że po prostu zabrakło wsparcia
            if exist_enemy_order(self.game, self.lastTurnInfo, power_name, order[0], ['M']): # zaatakowany
                if order[0] in get_locs_with_units(self.game, power_name): # dalej tam stoi, czyli obronił (TODO: sprawdzić jak to się ma do odwrotu)
                    if get_order_target(order[1]) in self.game.map.scs: # obronił miasto, kozak!
                        return 5
                    else: # obronił terytorium
                        return 3
                else: # wyrzucili go :'(    ...czy było warto bronić? za mało danych :/
                    return 1
            else: # nikt nie atakował, bez sensu bronił, kara
                return -2

        elif order_type == 'M':
            # nagradzany jeśli:
                # zajął nowe miasto (BRAWO!)
                # zablokował ruch przeciwnikowi (całkiem spoko, tym bardziej jeśli to miasto, a już w ogóle jeśli własne)
                # przeciął support komuś
            # karany jeśli:
                # zrobił self bumpa
                # przeciął sobie support (xD)
                # zaattakował broniącą się swoją jednostkę (xDDD)
            # pozostałe ruchy bez nagród i kar, neutralne raczej
            target = get_order_target(order[1])
            if exist_own_order_by_loc(self_orders, target, ['H', 'D', 'O']):
                return -5
            elif exist_own_order_by_loc(self_orders, target, ['M']):
                return 0
            elif target in get_locs_with_units(self.game, power_name): # stoi tam, czyli zdobył
                if target in self.game.map.scs: # zajął miasto, yahoo!
                    if target not in self.lastTurnInfo.power_scs:  # nie miał tego wcześniej
                        return 8
                    else:
                        return 0
                else: # zajął terytorium niebędące miastem
                    return 0
            else: # nie udało się zdobyć
                if exist_enemy_order(self.game, self.lastTurnInfo, power_name, target, ['M']): #ktoś inny tam szedł
                   return 4
                elif count_own_orders(self_orders, target, ['M']) > 1: # bump z własną jednostką
                    return -5
                elif exist_own_order_by_loc(self_orders, target, ['H', 'D', 'O']): # próba ataku na własną jednostkę
                    return -10
                elif exist_enemy_order_by_loc(self.game, self.lastTurnInfo, power_name, target, ['D', 'O']): # przeciął czyjś support
                    return 5

        elif order_type == 'O':
            # przy supportach zakładamy, że są valid
            # nagradzany jeśli:
                # wróg chciał też zająć tę prowincję
                # tym bardziej jeśli udało się nam, a mu nie
            # karany jeśli:
                # wsparł wroga
                # żaden wróg nie chciał tam wejść
            if not exist_own_order_by_loc(self_orders, order[1].split(' ')[4], ['M']): # wspierał wroga albo wyimaginowanego przyjaciela
                return -10
            elif exist_enemy_order(self.game, self.lastTurnInfo, power_name, order[0], ['M']): # wróg chciał tam iść
                if order[0] in self.game.get_orderable_locations(power_name): # my to zdobyliśmy, fajnie
                    return 5
                else:
                    return 1
            else: # niepotrzebne wsparcie, żaden wróg tam nie szedł
                return -3
        elif order_type == 'D':
            # przy supportach zakładamy, że są valid
            # nagradzany jeśli:
                # wróg chciał zająć tę prowincję
                # tym bardziej jeśli wrogowi się nie udało
            # karany jeśli:
                # wsparł wroga
                # żaden wróg nie zaatakował
            if not exist_own_order_by_loc(self_orders, order[1].split(' ')[4], ['H']):  # wspierał wroga albo wyimaginowanego przyjaciela
                return -10
            elif exist_enemy_order(self.game, self.lastTurnInfo, power_name, order[0], ['M']):  # wróg chciał tam iść
                if order[0] in self.game.get_orderable_locations(power_name):  # my tam jesteśmy, fajnie
                    return 5
                else:
                    return 1
            else:  # niepotrzebne wsparcie, żaden wróg tam nie szedł
                return -1
        else:
            # zero na te konwoje póki co
            return 0 #unknown type
        return 0  # POMINIĘTE W KTÓRYMŚ IFIE :(((((

    def set_reward(self):
        #for power_name, power in self.game.powers.items():
        #    reward = self.set_gain(power)
        #    for loc_order in self.lastTurnInfo.nation_location_orders[power_name].items():
        #       self.q_table[power_name][self.lastTurnInfo.power_hash[power_name]][loc_order[0]][loc_order[1]] += \
        #            (power.influence.__len__() - self.lastTurnInfo.power_influence[power_name]) + reward
        for power_name, power in self.game.powers.items():
            last_orders = self.lastTurnInfo.nation_location_orders[power_name].items()
            for loc_order in last_orders:
                result = self.q_table[power_name][self.lastTurnInfo.power_hash[power_name]][loc_order[0]][loc_order[1]] + \
                                self.my_set_gain(power_name, loc_order, last_orders)
                # to jest limit żeby nie było nieskończoności w prawdopodobieństwie
                #if result > self.max_value:
                #    result = self.max_value
                if result < 0:
                    result = 0
                self.q_table[power_name][self.lastTurnInfo.power_hash[power_name]][loc_order[0]][loc_order[1]] = result

    def set_turn_info(self):
        self.lastTurnInfo.phase = self.game.phase_type
        for power_name, power in self.game.powers.items():
            self.lastTurnInfo.power_hash[power_name] = get_hash(self.game, power_name)
            self.lastTurnInfo.power_influence[power_name] = power.influence.__len__()
            self.lastTurnInfo.power_scs[power_name] = self.game.get_centers(power_name)

    @staticmethod
    def default_value() -> str:
        return "Not Present"
