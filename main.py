from GameVisualizer import *
from Hasher import *
from Qtable import *
from diplomacy import Game, Power
from diplomacy.utils.export import to_saved_game_format, load_saved_games_from_disk

game = Game()
set_starting_influence(game)
visualizer = GameVisualizer()
q_table_Handler = QtableHandler(game)
iterator = 0
state = 0
while not game.is_game_done:
    iterator += 1
    #visualizer.paint_map(game)
    q_table_Handler.set_turn_info()

    # settings order
    for power_name, power in game.powers.items():
        power_orders = q_table_Handler.chose_orders(power_name)
        game.set_orders(power_name, power_orders)

    #visualizer.paint_orders(game)

    game.process()

    q_table_Handler.set_reward()
    adjust_influence(game)

    if iterator == 2:
        state += 1
        iterator = 0
        print(state)
        q_table_Handler.save()
        game = load_saved_games_from_disk("game.json")[0]
        q_table_Handler.game = game


