import json
import gzip
from c6_atomics import Game
from lg_reader import LittlegolemReader


class GamesDataManager:
    def __init__(self, lg_reader=LittlegolemReader()):
        self.games_dict = self.load_from_file("data/games_dict")
        self.games_trie = self.load_from_file("data/games_trie")
        self.lg_reader = lg_reader

    def load_from_file(self, filename):
        with gzip.open(filename, "r") as f:
            return json.loads(f.read().decode('utf-8'))

    def dump_to_file(self, obj, filename):
        with gzip.open(filename, "w") as f:
            f.write(json.dumps(obj).encode('utf-8'))

    def save(self):
        self.dump_to_file(self.games_dict, "data/games_dict")
        self.dump_to_file(self.games_trie, "data/games_trie")

    # trie format:
    # {"j10": [# games, # black wins, remaining trie dict]
    def add_game_to_trie(self, id, game):
        current_dict = self.games_trie
        game = Game(game)
        score_for_black = game.black_score()
        for move in game:
            if move not in current_dict:
                # we have to use str(move) here to ensure that the
                # actual string is the key, even though we can
                # equivalently reference by the Move object later
                current_dict[str(move)] = [0, 0, {}]

            current_dict[move][0] += 1
            current_dict[move][1] += score_for_black
            current_dict = current_dict[move][2]

        if "_end_" not in current_dict:
            current_dict["_end_"] = []

        current_dict["_end_"].append(id)

    def load_game(self, id):
        if id not in self.games_dict:
            if self.lg_reader.game_finished(id):
                game = self.lg_reader.get_game(id)
                self.games_dict[id] = game
                self.add_game_to_trie(id, game)

    def load_player_games(self, plid):
        for gid in self.lg_reader.get_player_game_ids(plid):
            self.load_game(gid)
