import requests


class LittlegolemReader:
    def __init__(self):
        pass

    def game_finished(self, id):
        r = requests.get(f"https://littlegolem.net/jsp/game/game.jsp?gid={id}")
        return "(game finished)" in r.text

    def get_game(self, id):
        r = requests.get(f"https://littlegolem.net/servlet/sgf/{id}/game{id}.txt")
        return [i.split("[")[1].split("]")[0] for i in r.text.split(";")[2:]]

    def get_player_game_ids(self, plid):
        r = requests.get(
            f"https://littlegolem.net/jsp/info/player_game_list.jsp?gtid=connect6&plid={plid}"
        )
        return [
            i.split("gid=")[1].split('"')[0]
            for i in r.text.splitlines()
            if "/jsp/game/game.jsp?gid=" in i
        ]
