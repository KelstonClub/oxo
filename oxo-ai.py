import random

import board

PLAYERS = ['O', 'X']
#
# Make sure the computer the last to play
#
COMPUTER_PLAYER = PLAYERS[-1]
N_CELLS = 3

def turns():
    #
    # This is a convenience function which will keep
    # going through the list of players (which doesn't
    # have to be only two) returning the next one each
    # time and then going back to the beginning.
    #
    while True:
        for player in PLAYERS:
            yield player

def get_computer_coord(b, player):
    run_length = len(b.dimensions[0])
    scores = {}
    for coords, data in b.runs_of_n(run_length):
        #
        # For each candidate line:
        # * If it's already full, skip
        # * If one move by us will win, score 2
        # * If one move by an opponent will win, score 1
        # * Otherwise score 0
        #
        if all(data):
            continue
        player_score = sum(1 for d in data if d == player)
        non_player_score = sum(1 for d in data if d and d != player)
        if player_score == run_length - 1:
            scores.setdefault(2, []). append(coords)
        elif non_player_score == run_length - 1:
            scores.setdefault(1, []). append(coords)
        else:
            scores.setdefault(0, []). append(coords)

    #
    # Pick the highest scoring lines and pick a random one
    # Pick the first empty cell in that line
    #
    score, lines = max(scores.items())
    line = random.choice(lines)
    for coord in line:
        if not b[coord]:
            return coord

def get_coord(b, player):
    if player == COMPUTER_PLAYER:
        return get_computer_coord(b, player)

    #
    # Get a move for the current player
    # No error checking: just get the coordinates
    # If the coord has already been used, warn and
    # ask again
    #
    while True:
        position = input("Player %s -- make a move x, y " % player)
        coord = tuple(int(i.strip()) for i in position.split(","))

        if b[coord]:
            print("%s is already taken" % (coord,))
        else:
            return coord

def has_player_won(b, player):
    #
    # Brute force: look at all the possible runs
    # of length <whatever> where <whatever> is the
    # size of the board. If any of those runs consists
    # entirely of the player character, then that
    # player has won.
    #
    # If we end up having found no runs where this player
    # is the only non-blank character, then this player
    # has not won on this round
    #
    run_length = len(b.dimensions[0])
    for coords, data in b.runs_of_n(run_length):
        if all(i == player for i in data):
            return True
    return False

if __name__ == '__main__':
    b = board.Board((N_CELLS, N_CELLS))
    for turn in turns():
        print()
        b.draw()
        coord = get_coord(b, turn)
        b[coord] = turn

        #
        # Check to see if this player has won.
        # We don't need to check all the players, because
        # you can't cause another player to win on your
        # own turn in noughts-and-crosses
        #
        if has_player_won(b, turn):
            print("%s has won!" % turn)
            break

        #
        # If no-one has won yet, check to see whether all the
        # spots on the board are filled as this means we have
        # a draw
        #
        elif len(b) == b.lendata():
            print("No-one has won :(")
            break

    #
    # Show the final state of the board
    #
    print()
    b.draw()
