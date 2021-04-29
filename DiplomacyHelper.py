from diplomacy import Game


def set_starting_influence(game):
    game.get_power('AUSTRIA').influence.extend(['GAL', 'BOH', 'TYR'])
    game.get_power('ENGLAND').influence.extend(['CLY', 'YOR', 'WAL'])
    game.get_power('FRANCE').influence.extend(['BUR', 'GAS', 'PIC'])
    game.get_power('GERMANY').influence.extend(['RUH', 'PRU', 'SIL'])
    game.get_power('ITALY').influence.extend(['PIE', 'TUS', 'APU'])
    game.get_power('RUSSIA').influence.extend(['LVN', 'UKR', 'FIN'])
    game.get_power('TURKEY').influence.extend(['SYR', 'ARM'])


def adjust_influence(game):
    for i in range(0, len(get_power_names(game))):
        cur_power = game.get_power(get_power_names(game)[i])
        for terit in cur_power.influence:
            if terit in game.map.scs and terit not in cur_power.centers:
                cur_power.influence.remove(terit)
        for terit in cur_power.centers:
            if terit not in cur_power.influence:
                cur_power.influence.append(terit)


def get_unit_type(game, power_name, location):
    for unit in game.get_units(power_name):
        sp = unit.split(' ')
        if sp[1] == location:
            return sp[0]
    return '?'


def get_locs_with_units(game, power_name):
    result = []
    for unit in game.get_units(power_name):
        sp = unit.split(' ')
        result.append(sp[1])
    return result


def get_power_names(game):
    return list(game.get_map_power_names())

# H for hold, M for movement, D for defensive support, O for offensive support
def get_order_type(order):
    order_elems = order.split(' ')
    if order_elems[2] == 'H':  # hold the position
        return 'H'
    elif order_elems[2] == '-':  # move
        return 'M'
    elif order_elems[2] == 'S':  # support...
        if len(order_elems) == 5:  # defensive support
            return 'D'
        else:
            return 'O'

#return the teritory army is trying to take or defend
def get_order_target(order):
    order_elems = order.split(' ')
    if order_elems[2] == 'H':  # hold the position
        result = order_elems[1].split('/')[0] # e.g. A >>VIE<< H  # split('/') is for multi-coast like STP/SC
    else:
        result = order_elems[-1].split('/')[0] # e.g. A VIE - >>BUD<< or A VIE S A GAL - >>BUD<<
    return result

def exist_enemy_order(game:Game, last_turn_info, power_name, dest, ord_types):
    for enemy_name in get_power_names(game):
        if enemy_name != power_name:
            their_orders = last_turn_info.nation_location_orders[enemy_name].items()
            for order in their_orders:
                if get_order_target(order[1]) == dest and get_order_type(order[1]) in ord_types: return True
    return False

def exist_enemy_order_by_loc(game:Game, last_turn_info, power_name, dest, ord_types):
    for enemy_name in get_power_names(game):
        if enemy_name != power_name:
            their_orders = last_turn_info.nation_location_orders[enemy_name].items()
            for order in their_orders:
                if order[0] == dest and get_order_type(order[1]) in ord_types: return True
    return False

def exist_own_order(orders, dest, ord_types):
    for order in orders:
        if get_order_target(order[1]) == dest and get_order_type(order[1]) in ord_types: return True
    return False

def exist_own_order_by_loc(orders, dest, ord_types):
    for order in orders:
        if order[0] == dest and get_order_type(order[1]) in ord_types: return True
    return False

def count_own_orders(orders, dest, ord_types)->int:
    sum = 0
    for order in orders:
        if get_order_target(order[1]) == dest and get_order_type(order[1]) in ord_types: sum += 1
    return sum