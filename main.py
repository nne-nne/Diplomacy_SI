import random
from GameVisualizer import *
from Hasher import *

game = Game()
set_starting_influence(game)
visualizer = GameVisualizer()

while not game.is_game_done:

    visualizer.paint_map(game)

    # pozyskanie hasha:
    for power_name in get_power_names(game):
        print(get_hash(game, power_name))

    possible_orders = game.get_all_possible_orders()
    wait_for_any_key()

    for power_name, power in game.powers.items():
        power_orders = [random.choice(possible_orders[loc]) for loc in game.get_orderable_locations(power_name)
                        if possible_orders[loc]]
        game.set_orders(power_name, power_orders)

    visualizer.paint_orders(game)
    wait_for_any_key()

    game.process()
    adjust_influence(game)

