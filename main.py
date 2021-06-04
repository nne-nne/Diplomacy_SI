from statistics import mean

from Qtable import *
from diplomacy import Game, Power
from diplomacy.utils.export import to_saved_game_format, load_saved_games_from_disk
from GameSaver import *

def save_stat(stats,turn_number,label):
    for power_name, _ in game.powers.items():
        stats["influence"][power_name] = mean(stats["influence"][power_name])
        stats["centers"][power_name] = mean(stats["centers"][power_name])
    try:
        with open(f"Stats/{turn_number}.json", "r") as a_file:
            root = json.load(a_file)
    except FileNotFoundError:
        root = []

    with open(f"Stats/{turn_number}.json", "w") as a_file:
        root.append(label)
        root.append(stats)
        json.dump(root,a_file)



def play_game(game: Game, save_game: bool, agent_nation: list, label="", turn_number = 3, repeat_number= 1000):
    set_starting_influence(game)
    if save_game:
        saver = GameSaver()
    q_table_Handler = QtableHandler(game, agent_nation)
    iterator = 0
    state = 0
    finish = False
    stats = {"centers":defaultdict(list), "influence":defaultdict(list)}
    while not game.is_game_done and not finish:
        iterator += 1
        q_table_Handler.set_turn_info()

        # settings order
        phase = game.get_current_phase()[-1]
        for power_name, power in game.powers.items():
            power_orders = q_table_Handler.chose_orders(power_name)
            game.set_orders(power_name, power_orders)


        #visualizer.paint_orders(game)
        if save_game:
            saver.save_game(game, "gierka")

        game.process()

        if phase == 'M':
            q_table_Handler.set_reward()
        adjust_influence(game)

        if iterator == turn_number:
            state += 1
            if state % repeat_number == 0:
                q_table_Handler.save()
            if state == repeat_number:
                save_stat(stats,turn_number,label)
                game = load_saved_games_from_disk("game.json")[0]
                return
            iterator = 0
            print("State: ", state)
            print("Accuracy: {0}".format(q_table_Handler.get_accuracy()))
            print("Number of Germany centers: ", game.get_centers("GERMANY").__len__(),  game.get_power("GERMANY").influence.__len__())
            for power_name, _ in game.powers.items():
                stats["influence"][power_name].append(game.get_power(power_name).influence.__len__())
                stats["centers"][power_name].append(game.get_centers(power_name).__len__())
            game = load_saved_games_from_disk("game.json")[0]
            q_table_Handler.game = game
            q_table_Handler.attempts = 0
            q_table_Handler.miss_hits = 0


def play_best(game: Game, save_game: bool,agent_nation: list, turn_number = 3, repeat_number= 1000):
    set_starting_influence(game)
    if save_game:
        saver = GameSaver()
    q_table_Handler = QtableHandler(game, agent_nation)
    iterator = 0
    state = 0
    while not game.is_game_done:
        iterator += 1
        q_table_Handler.set_turn_info()

        # settings order
        for power_name, power in game.powers.items():
            if power_name in agent_nations:
                power_orders = q_table_Handler.chose_best(power_name)
            else:
                power_orders = q_table_Handler.chose_orders(power_name)
            game.set_orders(power_name, power_orders)

        if save_game:
            saver.save_game(game, "gierka")

        game.process()
        adjust_influence(game)
        if iterator == turn_number:
            return


game = load_saved_games_from_disk("game.json")[0]
agent_nations = list(game.get_map_power_names())
agent_nations.remove("GERMANY")
play_best(game, True, ["GERMANY"], 40, 1)
