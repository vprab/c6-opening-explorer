# Connect6 Opening Explorer
## _A Python REPL-based environment to study Connect6 openings_

## Features

- Get winrates and recommended next moves for Connect6 openings, based on results from nearly 35000 games played on LittleGolem
- Accounts for all possible transformations of an opening via rotation/reflection when searching game data, but results are always presented to match the input 'reference frame' for maximum ease of use
- A trie-based implementation ensures that all queries complete near-instantly

## Installation
This code requires Python 3.6+ to run.

To get started, simply clone this repository and run `python3 -i main.py`

## Usage
Once inside the REPL, use the `opening_stats` and `find_matching_games` functions to start exploring.

`opening_stats` will present statistics from saved games matching this opening, as well as a breakdown of possible next moves and their respective statistics:
```
>>> opening_stats(['j10', 'i9k9', 'h9j8', 'j7k10'])
Opening Summary:
➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕
➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕
➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕
➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕
➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕
➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕
➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕
➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕
➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕
➕➕➕➕➕➕➕➕➕🔵⚪➕➕➕➕➕➕➕➕
➕➕➕➕➕➕➕🔵⚪➕⚪➕➕➕➕➕➕➕➕
➕➕➕➕➕➕➕➕➕🔵➕➕➕➕➕➕➕➕➕
➕➕➕➕➕➕➕➕➕⚪➕➕➕➕➕➕➕➕➕
➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕
➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕
➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕
➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕
➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕
➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕➕
# of games played: 6
BLACK/WHITE
5/1 (83.33%/16.67%)

MOVE        # GAMES         BLACK / WHITE
k8l9        2                   1 / 1         (50.00%/50.00%)
h11k8       1                   1 / 0         (100.00%/0.00%)
k7l9        1                   1 / 0         (100.00%/0.00%)
i8k8        1                   1 / 0         (100.00%/0.00%)
j11k8       1                   1 / 0         (100.00%/0.00%)
```

`find_matching_games` will return the LittleGolem IDs of all saved games matching this opening:
```
>>> find_matching_games(['j10', 'i9k9', 'h9j8', 'j7k10'])
['1821136', '1038315', '775616', '2272189', '1584170', '919237']
```

## Advanced
- To update the locally saved game data, uncomment lines 52-54 in `main.py` before starting the REPL. Depending on how recent the last update was, this process can take some time, so be patient. Be sure to re-comment these lines out for regular use.
- To save game data locally for a player not included in the list, simply add their LittleGolem player ID to the `tracked_player_ids` list in `main.py` and follow the instructions above.
