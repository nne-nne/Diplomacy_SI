from GameVisualizer import *
from Hasher import *
from Qtable import *
from diplomacy import Game, Power
from diplomacy.utils.export import to_saved_game_format, load_saved_games_from_disk
from GameSaver import *

game = Game()
set_starting_influence(game)
saver = GameSaver()
#visualizer = GameVisualizer()
q_table_Handler = QtableHandler(game, game.get_map_power_names())
iterator = 0
state = 0
turn_number = 4
finish = False
while not game.is_game_done and not finish:
    iterator += 1
    #visualizer.paint_map(game)
    q_table_Handler.set_turn_info()

    # settings order
    phase = game.get_current_phase()[-1]
    for power_name, power in game.powers.items():
        power_orders = q_table_Handler.chose_orders(power_name)
        game.set_orders(power_name, power_orders)


    #visualizer.paint_orders(game)
    # saver.save_game(game, "gierka")

    game.process()

    if phase == 'M':
        q_table_Handler.set_reward()
    adjust_influence(game)

    if iterator == turn_number:
        state += 1
        if state % 100 == 0:
            q_table_Handler.save()
        if state == 10000:
            exit(0)
        iterator = 0
        print("State: ", state)
        print("Accuracy: {0}".format(q_table_Handler.get_accuracy()))
        print("Number of Germany centers: ", game.get_centers("GERMANY").__len__())
        game = load_saved_games_from_disk("game.json")[0]
        q_table_Handler.game = game
        q_table_Handler.attempts = 0
        q_table_Handler.miss_hits = 0
