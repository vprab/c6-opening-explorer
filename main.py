from games_data_manager import GamesDataManager
from games_searcher import GamesSearcher
from c6_atomics import Move, Game

tracked_player_ids = [
    58835,   # gzero_bot
    20818,   # Lomaben
    14529,   # wayne chen
    136053,  # trieste6
    11820,   # ondik
    138931,  # FancyBen
    10496,   # Andrey
    18546,   # 5466
    132373,  # Azusa
    17341,   # Ã¥Â¦Â?Ã¥Â¦Â?
    15411,   # cutecat
    17458,   # Phoenix
    137141,  # gk18
    11956,   # richu333
    14287,   # jinjinlkj
    16955,   # Hsu
    12607,   # hazy
    20115,   # trytrytry
    17637,   # crazyvvi
    1704,    # iec
    37291,   # T_O_C_H
    9400,    # Vladimir Sinitsyn
    10131,   # drozdov
    22400,   # Florian Jamain
    11936,   # euhuang
    136249,  # Thomaslai
    15965,   # Duty
    16197,   # niaufei
    140801,  # farmagnus
    14096,   # flytogame
    46121,   # swix
    15609,   # u2b
    142840,  # Misio
    14239,   # givemesix
    139373,  # vprab
    135957,  # mellendo
    20157,   # teamtodd
    36197,   # john_many_jars
    39497,   # pburka
]

gdm = GamesDataManager()

# ----------------------------------------
#    UNCOMMENT TO UPDATE SAVED GAME DATA:

# for plid in tracked_player_ids:
#     gdm.load_player_games(plid)
# gdm.save()

# ----------------------------------------

gs = GamesSearcher(gdm)


def opening_stats(starting_moves_strlist):
    starting_moves = Game(starting_moves_strlist)
    num_games, black_score, next_moves = gs.opening_matcher(starting_moves)
    next_real_moves = {k: v for k, v in next_moves.items() if k != "_end_"}
    sorted_next_moves = {
        k: v
        for k, v in sorted(
            next_real_moves.items(), key=lambda item: item[1][0], reverse=True
        )
    }
    white_score = num_games - black_score
    if num_games == 0:
        print("Opening not found")
        return

    print("Opening Summary:")
    starting_moves.prettyprint()
    print(f"# of games played: {num_games}")
    print("BLACK/WHITE")
    print(
        f"{black_score}/{white_score} ({black_score*100/num_games:.2f}%/{white_score*100/num_games:.2f}%)"
    )
    print()
    print("MOVE        # GAMES         BLACK / WHITE")
    for move in sorted_next_moves:
        move_num_games, move_black_score, _ = sorted_next_moves[move]
        move_white_score = move_num_games - move_black_score
        print(
            f"{str(move):<12}{move_num_games:<15}{move_black_score:>6} / {move_white_score:<6}"
            f"    ({move_black_score*100/move_num_games:.2f}%/{move_white_score*100/move_num_games:.2f}%)"
        )


def find_matching_games(starting_moves):
    return gs.find_all_matching_game_ids_by_start(Game(starting_moves))


## UNCOMMENT TO RUN SMOKE TESTS:
# -------------------------------------------------------------------

# assert gs.opening_matcher(Game(["j10"]))[0] == len(gdm.games_dict)
# assert (
#     gs.opening_matcher(Game(["j10", "i9k9"]))[:2]
#     == gs.opening_matcher(Game(["j10", "i11k11"]))[:2]
# )
# assert gs.opening_matcher(Game(["j10", "i9k9"]))[0] == len(
#     [
#         g
#         for g in list(gdm.games_dict.values())
#         if g[:2]
#         in (
#             ["j10", "i9k9"],
#             ["j10", "k9i9"],
#             ["j10", "i11k11"],
#             ["j10", "k11i11"],
#             ["j10", "i9i11"],
#             ["j10", "i11i9"],
#             ["j10", "k9k11"],
#             ["j10", "k11k9"],
#         )
#     ]
# )
# assert len(find_matching_games(["j10"])) == len(gdm.games_dict)

# -------------------------------------------------------------------
