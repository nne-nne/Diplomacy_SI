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
q_table_Handler = QtableHandler(game, ["GERMANY"])
iterator = 0
state = 0

finish = False
while not game.is_game_done and not finish:
    saver.save_game(game, "gierka")
    iterator += 1
    #visualizer.paint_map(game)
    q_table_Handler.set_turn_info()

    # settings order
    phase = game.get_current_phase()[-1]
    if phase == 'M':
        for power_name, power in game.powers.items():
            power_orders = q_table_Handler.chose_orders(power_name)
            game.set_orders(power_name, power_orders)
    else:
        for power_name, power in game.powers.items():
            power_orders = q_table_Handler.chose_on_random(power_name)
            game.set_orders(power_name, power_orders)

    #visualizer.paint_orders(game)
    saver.save_game(game, "gierka")

    game.process()

    if phase == 'M':
        q_table_Handler.set_reward()
    adjust_influence(game)

    if iterator == 10:
        state += 1
        if state % 1000 == 0:
            q_table_Handler.save()
        if state == 10000:
            exit(0)
        iterator = 0
        print(state)
        print("Accuracy: {0}".format(q_table_Handler.get_accuracy()))
        print(game.get_centers("GERMANY").__len__())

        finish = True
        # q_table_Handler.game = game
        # game = load_saved_games_from_disk("game.json")[0]


saver.start_visualisation("gierka")
