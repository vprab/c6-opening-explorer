import re
from copy import deepcopy


class Move:
    def __init__(self, move):
        if move == "_end_":
            self.indmoves = [move]
        else:
            self.indmoves = re.split("(\w\d+)", move)[1::2]

    def is_end(self):
        return self.indmoves == ["_end_"]

    @staticmethod
    def rotate_individual_move_90(m):
        x, y = m[0], int(m[1:])
        dx = ord(x) - ord("j")
        dy = y - 10
        newx = chr(ord("j") + dy)
        newy = 10 - dx
        return "{}{}".format(newx, newy)

    @staticmethod
    def flip_individual_move_horizontal(m):
        x, y = m[0], int(m[1:])
        dx = ord(x) - ord("j")
        newx = chr(ord("j") - dx)
        return "{}{}".format(newx, y)

    @staticmethod
    def flip_individual_move_vertical(m):
        x, y = m[0], int(m[1:])
        dy = y - 10
        newy = 10 - dy
        return "{}{}".format(x, newy)

    def apply_transformation(self, f):
        if len(self.indmoves) == 1:
            return deepcopy(self)

        return Move("".join(map(f, self.indmoves)))

    def rotate_90(self):
        return self.apply_transformation(self.rotate_individual_move_90)

    def flip_horizontal(self):
        return self.apply_transformation(self.flip_individual_move_horizontal)

    def flip_vertical(self):
        return self.apply_transformation(self.flip_individual_move_vertical)

    def get_coordinates(self):
        return [(19 - int(m[1:]), ord(m[0]) - ord('a')) for m in self.indmoves]

    def __eq__(self, other):
        return str(self) == str(other)

    def __str__(self):
        return "".join(sorted(self.indmoves))

    def __hash__(self):
        return hash(str(self))


class Game:
    def __init__(self, movelist):
        self.movelist = [m if isinstance(m, Move) else Move(m) for m in movelist]

    def black_score(self):
        if len(self.movelist) == 150:
            # littlegolem games appear to default to a tie at move 150
            return 0.5
        else:
            # the last player who moved won
            last_mover = len(self.movelist) % 2
            if self.get_last_move().is_end():
                last_mover = 1 - last_mover
            return last_mover == 1

    def prettyprint(self):
        black_moves = [c for i, m in enumerate(self.movelist) if i % 2 == 0 for c in m.get_coordinates()]
        white_moves = [c for i, m in enumerate(self.movelist) if i % 2 == 1 for c in m.get_coordinates()]
        for i in range(19):
            s = ''
            for j in range(19):
                if (i, j) in black_moves:
                    s += chr(0x1f535)
                elif (i, j) in white_moves:
                    s += chr(0x26aa)
                else:
                    s += chr(0x2795)
            print(s)

    def get_last_move(self):
        return self.movelist[-1]

    def get_num_moves(self):
        return len(self.movelist)

    def add_move(self, m):
        return Game(self.movelist + [m])

    def rotate_90(self):
        return Game([move.rotate_90() for move in self.movelist])

    def flip_horizontal(self):
        return Game([move.flip_horizontal() for move in self.movelist])

    def flip_vertical(self):
        return Game([move.flip_vertical() for move in self.movelist])

    def __eq__(self, other):
        if isinstance(other, Game):
            if len(self.movelist) == len(other.movelist):
                return all(
                    [
                        self.movelist[i] == other.movelist[i]
                        for i in range(len(self.movelist))
                    ]
                )
        return False

    def __str__(self):
        return str([str(move) for move in self.movelist])

    def __hash__(self):
        return hash(str(self))

    def __iter__(self):
        return iter(self.movelist)
