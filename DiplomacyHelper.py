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

