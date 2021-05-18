from diplomacy import Game
from diplomacy.utils.export import to_saved_game_format, load_saved_games_from_disk
from GameVisualizer import *
import threading

class GameSaver:
    def __init__(self):
        self.save_frame = 0
        self.read_frame = 0
        self.visualizer = None
        self.game = None

    def save_game(self, game:Game, name):
        to_saved_game_format(game, output_path = 'game_' + name + str(self.save_frame) + '.json')
        self.save_frame += 1

    def start_visualisation(self, name):
        self.read_frame = 0
        self.visualizer = GameVisualizer()
        window_thread = threading.Thread(target=mantain_window, args=())
        window_thread.start()
        self.game = load_saved_games_from_disk('game_' + name + str(self.read_frame) + '.json')[0]
        self.visualizer.paint_map(self.game)


