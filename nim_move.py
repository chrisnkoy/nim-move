# Lane, Nkoy, O'Brien

import sys
import re
import random

# These are just indexing nodes that help with readability.
# You might see them used like this:
# ~ state[i][PILES] (the number of piles with unique pile height i)
# ~ state[i][OBJECTS] (the number of objects in unique pile height i)
PILES = 0
OBJECTS = 1


# This function simply calls other functions
# and prints the program output:
def nim_move(state_file, patterns_file):
    state, patterns = read(state_file, patterns_file)
    move = move_search(state, patterns)
    response = "Take {} objects from a pile of {}".format(move[1], state[move[0]][OBJECTS])
    print(response)


# The top level of recursion.
# Once a good move is found, we stop, since we
# consider all good moves to be equally good:
def move_search(state, patterns):
    # First we follow Nim Sum strategy,
    # hoping it provides a good move:
    balanced_moves = get_nim_balanced_moves(state)
    if balanced_moves:
        for move in balanced_moves:
            if recursive_search(create_state(move[PILES], move[OBJECTS], state), patterns):
                return move
        balanced_states = []
        # If all Nim-Sum-balanced moves prove to be bad,
        # we try moves that are one object away from Nim-Sum Balanced,
        # hoping that the opponent will "take the bait:"
        for move in balanced_moves:
            if move[OBJECTS] > 1:
                if recursive_search(create_state(move[PILES], move[OBJECTS] - 1, state), patterns):
                    return move[PILES], move[OBJECTS] - 1
                balanced_states.append(create_state(move[PILES], move[OBJECTS] - 1, state))
            balanced_states.append(create_state(move[PILES], move[OBJECTS], state))
        # Otherwise, all other possible moves are searched:
        return bad_moves_search(state, patterns, balanced_states)
    else:
        return bad_moves_search(state, patterns)


# This function just checks every move
# that moves_search skipped over:
def bad_moves_search(state, patterns, extra_patterns=None):
    for pile in range(len(state)):
        for take_away in range(1, state[pile][OBJECTS] + 1):
            new_state = create_state(pile, take_away, state)
            if not extra_patterns:
                if recursive_search(new_state, patterns):
                    return pile, take_away
            elif not is_pattern(state, extra_patterns):
                if recursive_search(new_state, patterns):
                    return pile, take_away
    # When no good moves are found, we play randomly,
    # since we consider all bad moves to be equally bad:
    piles = random.randint(0, len(state) - 1)
    take_away = random.randint(1, state[piles][OBJECTS])
    print(piles, take_away)
    return piles, take_away


# The recursive aspect of the algorithm.
def recursive_search(state, patterns):
    if state: # Empty states are terminal nodes, and thus bad moves.
        if is_pattern(state, patterns): # We want to avoid "lose" patterns.
            return False
        else:
            # First we follow Nim Sum strategy,
            # hoping it provides a good move:
            balanced_moves = get_nim_balanced_moves(state)
            if balanced_moves:
                for move in balanced_moves:
                    if recursive_search(create_state(move[PILES], move[OBJECTS], state), patterns):
                        return False
                balanced_states = []
                # If all Nim-Sum-balanced moves prove to be bad,
                # we try moves that are one object away from Nim-Sum Balanced,
                # hoping that the opponent will "take the bait:"
                for move in balanced_moves:
                    if move[OBJECTS] > 1:
                        if recursive_search(create_state(move[PILES], move[OBJECTS] - 1, state), patterns):
                            return False
                        balanced_states.append(create_state(move[PILES], move[OBJECTS] - 1, state))
                    balanced_states.append(create_state(move[PILES], move[OBJECTS], state))
                    # Otherwise, all other possible moves are searched:
                    return recursive_bad_moves_search(state, patterns, balanced_states)
            else:
                return recursive_bad_moves_search(state, patterns)
    else:
        return False


# This function just checks every move
# that recursive_moves_search skipped over:
def recursive_bad_moves_search(state, patterns, extra_patterns=None):
    for i in range(len(state)):
        for j in range(1, state[i][OBJECTS] + 1):
            new_state = create_state(i, j, state)
            if not extra_patterns:
                if recursive_search(new_state, patterns):
                    return False
            elif not is_pattern(state, extra_patterns):
                if recursive_search(new_state, patterns):
                    return False
    return True


# This function calculates the Nim Sum for a given state:
def get_nim_sum(state):
    nim_sum = 0
    for pile in state:
        # We can speed up calculations by only
        # xor-ing unique pile heights of odd counts:
        if pile[PILES] % 2 == 1:
            nim_sum = nim_sum ^ pile[OBJECTS]
    return nim_sum


# This function finds all moves that produce
# a game state of Nim Sum zero:
def get_nim_balanced_moves(state):
    nim_sum = get_nim_sum(state)
    # States whose Nim Sum is already zero
    # have no such moves:
    if nim_sum == 0:
        return None
    else:
        moves = []
        # There may be multiple such moves,
        # so we check each unique pile height:
        for pile in range(len(state)):
            xor = state[pile][OBJECTS] ^ nim_sum
            if xor < state[pile][OBJECTS]:
                moves.append([pile, state[pile][OBJECTS] - xor])
        return moves


# This function detects if a given state
# is equivalent to a given list of patterns.
# It's uses are to avoid lose patterns and to avoid
# checking the same move twice in some cases:
def is_pattern(state, patterns):
    for pattern in patterns:
        if len(state) == len(pattern):
            same = True
            # Since all game states are kept sorted,
            # we can check each pattern in linear time:
            for pile in range(len(state)):
                if state[pile][PILES] != pattern[pile][PILES] or state[pile][OBJECTS] != pattern[pile][OBJECTS]:
                    same = False
                    break
            if same:
                return True
    return False


# This function create a new state,
# given an original state and an amount of objects
# to take away from a given pile:
def create_state(pile, take_away, state):
    new_state = []
    # First we copy the original data into a new state item:
    for i in range(len(state)):
        new_state.append([state[i][PILES], state[i][OBJECTS]])
    # We need to adjust the new state based on
    # the new pile height we've created:
    remaining_count = new_state[pile][OBJECTS] - take_away
    # We can delete the given pile if there was only one left:
    if new_state[pile][PILES] == 1:
        del new_state[pile]
    else:
        new_state[pile][PILES] -= 1
    if remaining_count > 0:
        not_found = True
        # We find the right position in the list to place the new pile
        # so that the state remains sorted by pile height:
        for i in range(pile, len(new_state)):
            if remaining_count == new_state[i][OBJECTS]:
                new_state[i][PILES] += 1
                not_found = False
                break
            elif remaining_count > new_state[i][OBJECTS]:
                new_state.insert(i, [1, remaining_count])
                not_found = False
                break
        if not_found:
            new_state.append([1, remaining_count])
    return new_state


# This function reads in the input files
# and stores the data within:
def read(state_file, patterns_file):
    state = []
    next_pile = state_file.readline().rstrip('\n')
    while next_pile:
        data = next_pile.split("p")
        state.append([int(data[PILES]), int(data[OBJECTS])])
        next_pile = state_file.readline().rstrip('\n')
    state = sorted(state, key=lambda s: -s[OBJECTS])
    patterns = []
    next_pattern = patterns_file.readline().rstrip('\n')
    while next_pattern:
        pattern = []
        data = re.split('p| ', next_pattern)
        i = 0
        while True:
            pattern.append([int(data[i]), int(data[i+1])])
            if i+2 == len(data):
                break
            i += 2
        pattern = sorted(pattern, key=lambda s: -s[OBJECTS])
        patterns.append(pattern)
        next_pattern = patterns_file.readline().rstrip('\n')
    return state, patterns


# This simply passes the opened files to
# the nim_move function above:
def main(argv):
    state_file = open(argv[0], "r")
    patterns_file = open(argv[1], "r")
    nim_move(state_file, patterns_file)


if __name__ == '__main__':
    main(sys.argv[1:])
