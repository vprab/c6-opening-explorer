from functools import reduce


def rotate_game_90(g):
    return g.rotate_90()


def flip_game_horizontal(g):
    return g.flip_horizontal()


def flip_game_vertical(g):
    return g.flip_vertical()


def map_funcs(obj, func_list):
    return reduce(lambda o, func: func(o), func_list, obj)


class GamesSearcher:
    def __init__(self, gdm):
        self.gdm = gdm

    def find_games_by_start(self, starting_moves):
        res = [0, 0, self.gdm.games_trie]
        for move in starting_moves:
            res_next = res[2]
            if move in res_next:
                res = res_next[move]
            else:
                return [0, 0, {}]

        return res

    def find_game_ids_by_start(self, starting_moves):
        opening_subtrie = self.find_games_by_start(starting_moves)
        res = []
        queue = [opening_subtrie]
        while queue:
            d = queue.pop(0)[2]
            if "_end_" in d:
                res += d["_end_"]
            for k, v in d.items():
                if k != "_end_":
                    queue.append(v)

        return res

    def find_all_matching_game_ids_by_start(self, starting_moves):
        all_transformed_games = set(self.get_all_game_transformations(starting_moves))
        return [
            id
            for tf_game in all_transformed_games
            for id in self.find_game_ids_by_start(tf_game)
        ]

    def get_all_game_transformations(self, game):
        tfs = [
            [lambda x: x],
            [rotate_game_90],
            [rotate_game_90, rotate_game_90],
            [rotate_game_90, rotate_game_90, rotate_game_90],
            [flip_game_horizontal],
            [flip_game_vertical],
            [rotate_game_90, flip_game_vertical],
            [rotate_game_90, flip_game_horizontal],
        ]

        return [map_funcs(game, tf) for tf in tfs]

    def opening_matcher(self, starting_moves):
        # [transform: inverse transform]
        transform_manager = [
            ([lambda x: x], [lambda x: x]),
            ([rotate_game_90], [rotate_game_90, rotate_game_90, rotate_game_90]),
            ([rotate_game_90, rotate_game_90], [rotate_game_90, rotate_game_90]),
            ([rotate_game_90, rotate_game_90, rotate_game_90], [rotate_game_90]),
            ([flip_game_horizontal], [flip_game_horizontal]),
            ([flip_game_vertical], [flip_game_vertical]),
            (
                [rotate_game_90, flip_game_vertical],
                [flip_game_vertical, rotate_game_90, rotate_game_90, rotate_game_90],
            ),
            (
                [rotate_game_90, flip_game_horizontal],
                [flip_game_horizontal, rotate_game_90, rotate_game_90, rotate_game_90],
            ),
        ]

        all_transformations = [
            (map_funcs(starting_moves, tf), rev) for tf, rev in transform_manager
        ]

        num_games = 0
        black_score = 0
        next_moves = {}
        seen_transformations = set()
        for modified_starting_moves, reset_func_list in all_transformations:
            (
                num_transformation_games,
                black_transformation_score,
                next_transformation_moves,
            ) = self.find_games_by_start(modified_starting_moves)
            for move in next_transformation_moves:
                resulting_game = modified_starting_moves.add_move(move)
                adjusted_move = map_funcs(
                    resulting_game, reset_func_list
                ).get_last_move()

                if (resulting_game, adjusted_move) not in seen_transformations:
                    seen_transformations.add((resulting_game, adjusted_move))

                    if move == "_end_":
                        move_count = len(next_transformation_moves[move])
                        move_black_score = move_count * resulting_game.black_score()
                        if move not in next_moves:
                            next_moves[move] = []

                        next_moves[move] += next_transformation_moves[move]
                    else:
                        move_count, move_black_score, _ = next_transformation_moves[
                            move
                        ]
                        if adjusted_move not in next_moves:
                            next_moves[adjusted_move] = [0, 0, {}]

                        next_moves[adjusted_move][0] += move_count
                        next_moves[adjusted_move][1] += move_black_score

                    num_games += move_count
                    black_score += move_black_score

        # deduplicate equivalent results
        unique_ending_positions = set()
        keys_to_delete = set()
        for move in next_moves:
            next_move_gamestate = starting_moves.add_move(move)
            if any(
                (
                    next_move_gamestate_variant in unique_ending_positions
                    for next_move_gamestate_variant in self.get_all_game_transformations(
                        next_move_gamestate
                    )
                )
            ):
                remove_count, remove_score, _ = next_moves[move]
                num_games -= remove_count
                black_score -= remove_score
                keys_to_delete.add(move)
            else:
                unique_ending_positions.add(next_move_gamestate)

        for move in keys_to_delete:
            del next_moves[move]

        return num_games, black_score, next_moves
