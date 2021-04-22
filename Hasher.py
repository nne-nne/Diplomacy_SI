from DiplomacyHelper import *

def get_locs_of_interest(game, player_power):
    result = []
    result.extend(game.get_centers(player_power))
    result.extend(x for x in get_locs_with_units(game, player_power) if x not in result)
    others = []
    for location in result:
        for neighbour in game.map.abut_list(location, True):
            others.append(neighbour.upper())
            for far_neighbour in game.map.abut_list(neighbour, True):
                others.append(far_neighbour.upper())
    result.extend(x for x in others if x not in result)
    return result


def get_hashletter(game, location, player_power):
    for pow_name in get_power_names(game):
        unit_type = get_unit_type(game, pow_name, location)
        if unit_type != '?':
            if pow_name == player_power:
                if unit_type == 'A':
                    return 'a'
                else:
                    return 'f'
            else:
                if unit_type == 'A':
                    return 'e'
                else:
                    return 'r'
    return '-'


def get_hash(game, player_power):
    # '-' brak jednostek i naszych miast / są jednostki ale za daleko
    # 's' nasze miasto bez obrony
    # 'a' nasza armia
    # 'A' nasza armia z miastem
    # 'f' nasza flota
    # 'F' nasza flota z miastem
    # 'e' wroga armia
    # 'r' wroga flota
    # 'E' wroga armia w naszym mieście
    # 'R' wroga flota w naszym mieście

    result = list('-' * len(game.map.locs))
    result.append(game.get_current_phase()[-1])
    locations_of_interest = get_locs_of_interest(game, player_power)

    for i in range(len(game.map.locs)):
        location = game.map.locs[i]
        loc_upper = location.upper()  # some location names needs uppercase, e.g. stp

        if loc_upper in locations_of_interest:
            result[i] = get_hashletter(game, loc_upper, player_power)
            if loc_upper in game.get_centers(player_power):  # if this is our centre, should be uppercase.
                if result[i] == '-':  # if there is no army, mark it with 's'
                    result[i] = 's'
                result[i] = result[i].upper()
        else:
            result[i] = '-'  # too far, doesn't matter
    return ''.join(result)
