from collections import namedtuple
from collections import deque
import numpy as np

#GameState = namedtuple('GameState', 'to_move, utility, board, moves')

# ------------------------------------ GAME STATE ---------------------------------------------

class GameState:

    def __init__(self, to_move, utility, board, moves):
        self.to_move = to_move
        self.utility = utility
        self.board = board
        self.moves = moves


# ------------------------------------ GAME CLASS ----------------------------------------------
class Game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement actions,
    result, utility, and terminal_test. You may override display and
    successors or you can inherit their default methods. You will also
    need to set the .initial attribute to the initial state; this can
    be done in the constructor."""

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        raise NotImplementedError

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        raise NotImplementedError

    def utility(self, state):
        """Return the value of this final state to player."""
        raise NotImplementedError

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        return not self.actions(state)

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    def display(self, state):
        """Print or otherwise display the state."""
        print(state)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def play_game(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.initial
        while True:
            for player in players:
                move = player(self, state)
                state = self.result(state, move)
                if self.terminal_test(state):
                    self.display(state)
                    return self.utility(state, self.to_move(self.initial))


# ------------------------------------------ NODE CLASS ------------------------------------------------------

class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state. Also includes the action that got us to this state"""

    def __init__(self, state, parent=None, action=None):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        node_string = "Node: "
        node_string += "to_move : " + str(self.state.to_move)
        node_string += ", board : " + str(self.state.board)
        return node_string

    def expand(self, game):
        """List the nodes reachable in one step from this node."""
        return [self.child_node(game, action) for action in game.actions(self.state)]

    def child_node(self, game, action):
        """[Figure 3.10]"""
        next_state = game.result(self.state, action)
        next_node = Node(next_state, self, action)
        return next_node

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def __hash__(self):
        return hash(self.state)

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state


""" -------------------------------------------------------------------------------------------
---------------------------------------- P1 GAME ----------------------------------------------
------------------------------------------------------------------------------------------- """

Utility = namedtuple('Utility', 'P1, P2, P3, P4')


class MultiPlayerGame(Game):

    def __init__(self, to_move, board):
        utility = self.compute_utility(board)
        moves = self.compute_moves(to_move, board)
        self.initial = GameState(to_move=to_move, utility=utility, board=board, moves=moves)

    def actions(self, state):
        """Legal moves are amongst {L, R, T, B}"""
        return state.moves

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        if move not in state.moves:
            return state  # Illegal move has no effect

        # Finding the next player
        current_player = state.to_move
        if current_player == 'P1':
            next_player = 'P2'
        elif current_player == 'P2':
            next_player = 'P3'
        elif current_player == 'P3':
            next_player = 'P4'
        elif current_player == 'P4':
            next_player = 'P1'

        new_board = self.new_board_config(state, move)
        new_moves = self.compute_moves(next_player, new_board)
        new_utility = self.compute_utility(new_board)

        return GameState(to_move=next_player, utility=new_utility, board=new_board, moves=new_moves)

    def utility(self, state, player):
        """Return the value of this final state to player."""
        return state.utility

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        return self.is_winning_state(state) or len(state.moves) == 0

    def compute_utility(self, board):
        players = ['P1', 'P2', 'P3', 'P4']
        for player in players:
            if self.is_winning_state_player(board, player):
                if player == 'P1':
                    return Utility(200, 10, 30, 10)
                elif player == 'P2':
                    return Utility(100, 300, 150, 200)
                elif player == 'P3':
                    return Utility(150, 200, 400, 300)
                elif player == 'P4':
                    return Utility(220, 330, 440, 500)
        return Utility(0, 0, 0, 0)

    @staticmethod
    def new_board_config(state, move):
        current_player = state.to_move
        current_board_config = state.board.copy()
        x, y = current_board_config[current_player]
        xn = x
        yn = y
        if move == 'L':
            xn = x - 1
        elif move == 'R':
            xn = x + 1
        elif move == 'T':
            yn = y - 1
        elif move == 'B':
            yn = y + 1
        current_board_config[current_player] = (xn, yn)
        return current_board_config

    def is_winning_state(self, state):
        players = ['P1', 'P2', 'P3', 'P4']
        for player in players:
            if self.is_winning_state_player(state.board, player):
                return True
        return False

    @staticmethod
    def is_winning_state_player(board, player):
        x, y = board[player]
        if player == 'P1':
            if x == 4 and y == 4:
                return True
        elif player == 'P2':
            if x == 1 and y == 4:
                return True
        elif player == 'P3':
            if x == 1 and y == 1:
                return True
        elif player == 'P4':
            if x == 4 and y == 1:
                return True
        else:
            return False

    @staticmethod
    def compute_moves(to_move, board):
        x, y = board[to_move]
        players = ['P1', 'P2', 'P3', 'P4']
        other_players = players.copy()
        other_players.remove(to_move)
        blocked_positions = [board[other_player] for other_player in other_players]
        actions = ['L', 'R', 'T', 'B']
        # Imposing boundary restrictions
        if x >= 4:
            actions.remove('R')
        elif x <= 1:
            actions.remove('L')
        if y >= 4:
            actions.remove('B')
        elif y <= 1:
            actions.remove('T')

        # Imposing blocking restrictions by other players
        possible_actions = actions.copy()
        for action in possible_actions:
            xn = x
            yn = y
            if action == 'L':
                xn = x - 1
            elif action == 'R':
                xn = x + 1
            elif action == 'T':
                yn = y - 1
            elif action == 'B':
                yn = y + 1
            if (xn, yn) in blocked_positions:
                actions.remove(action)
        return actions


""" -------------------------------------------------------------------------------------------
---------------------------------------- GAME TREE GENERATION ---------------------------------
------------------------------------------------------------------------------------------- """


def breadth_first_game_tree(game):
    """
    Note that this function can be implemented in a
    single line as below: return graph_search(problem, FIFOQueue())
    """
    node = Node(game.initial)
    is_terminal = game.terminal_test(node.state)
    iteration = 0
    print_game_tree(node, False, game, is_terminal, 0, iteration)
    if is_terminal:
        return node
    frontier = deque([node])
    repeated = set()
    while frontier:
        node = frontier.popleft()
        repeated.add(node.state)
        for child in node.expand(game):
            iteration += 1
            is_terminal = game.terminal_test(child.state)
            if child.state in repeated:
                print_game_tree(child, True, game, is_terminal, len(frontier), iteration)
            else:
                if child not in frontier:
                    print_game_tree(child, False, game, is_terminal, len(frontier), iteration)
                    if not is_terminal:
                        frontier.append(child)
    return None


def print_game_tree(node, is_repeated, game, is_terminal, frontier_length, iteration):
    state = node.state
    current_player = state.to_move
    parent = node.parent
    action = node.action
    current_node = node
    if iteration % 1000 == 0:
        print('ITERATION :' + str(iteration))
        print('DEPTH : ' + str(node.depth))
    if node.depth <= 3 or is_terminal:
        print('----------------------------------------------------------------------------')
        if is_terminal:
            players = ['P1', 'P2', 'P3', 'P4']
            for player in players:
                if game.is_winning_state_player(state.board, player):
                    print("WINS : " + str(player))
                    return
            print("TERMINAL STATE WITH NO MOVES")
        print('CURRENT PLAYER : ' + str(current_player))
        print('PARENT : ' + str(parent))
        print('ACTION : ' + str(action))
        print('CURRENT NODE:' + str(current_node))
        print('REPEATED : ' + str(is_repeated))
        print('DEPTH : ' + str(node.depth))
        print('FRONTIER LENGTH : ' + str(frontier_length))

# ----------------------------------- DEPTH FIRST GAME TREE ----------------------------------------


def depth_first_game_tree(game):
    node = Node(game.initial)
    is_terminal = game.terminal_test(node.state)
    iteration = 0
    print_game_tree(node, False, game, is_terminal, 0, iteration)
    frontier = [(Node(game.initial))]  # Stack
    repeated = set()
    while frontier:
        node = frontier.pop()
        is_terminal = game.terminal_test(node.state)
        if is_terminal:
            continue
        repeated.add(node.state)
        for child in node.expand(game):
            iteration += 1
            if child.state in repeated:
                print_game_tree(child, True, game, is_terminal, len(frontier), iteration)
            else:
                if child not in frontier:
                    print_game_tree(child, False, game, is_terminal, len(frontier), iteration)
                    frontier.append(child)
    return None


# ____________________________________MULTI PLAYER MINIMAX SEARCH__________________________________________


explored = set()


def minimax_value(game, state):
    if state in explored:
        return state.utility
    explored.add(state)
    if game.terminal_test(state):
        return game.utility(state)

    player = state.to_move
    best_action = 'None'
    current_state_utility = Utility(0, 0, 0, 0)
    for action in game.actions(state):
        next_state_utility = minimax_value(game, game.result(state, action))
        if current_state_utility[player] < next_state_utility[player]:
            current_state_utility = next_state_utility
            best_action = action
    state.utility = current_state_utility
    print_node_minimax(state, best_action)
    return current_state_utility


def print_node_minimax(state, action):
    print('----------------------------------------------------------------------------')
    print('CURRENT PLAYER : ' + str(state.to_move))
    print('BOARD : ' + str(state.board))
    print('ACTION : ' + str(action))
    print('UTILITY : ' + str(state.utility))



to_move = 'P1'
board = dict(P1=(1, 1), P2=(4, 1), P3=(4, 4), P4=(1, 4))
multi_player_game = MultiPlayerGame(to_move, board)
#breadth_first_game_tree(multi_player_game)
depth_first_game_tree(multi_player_game)
#minimax_value(multi_player_game, multi_player_game.initial)



# -----------------------------------------------------------------------------------------------------


def depth_limited_search_modified(game, limit=50):
    frontier = [(Node(game.initial))]  # Stack
    counter = 0
    explored = []
    is_cutoff = False
    while frontier:
        node = frontier.pop()
        explored.append(node)
        counter += 1
        if game.terminal_test(node.state):
            #print_dls(limit, counter, node, frontier)
            continue
        elif node.depth == limit:
            is_cutoff = True
            #print_dls(limit, counter, node, frontier)
            continue
        for child in node.expand(game):
            if child not in explored and child not in frontier:
                frontier.append(child)
        #print_dls(limit, counter, node, frontier)
    return is_cutoff, explored


def print_dls(depth, counter, node, frontier):
    print('--------------------------------------------------------------------------------')
    print('Depth : ' + str(depth) + ', Step : ' + str(counter))
    print('1. Current Node : ' + str(node))
    print('2. Frontier length : ' + str(len(frontier)))


def iterative_deepening_search_modified(game):
    for depth in range(50):
        result = depth_limited_search_modified(game, depth)
        if not result[0]:
            return result[1]
        else:
            print('CUTOFF AT DEPTH ' + str(depth))


def breadth_first_depth_first_combined(game):
    node = Node(game.initial)
    iteration = 0
    print_game_tree(node, False, game, False, 0, iteration)
    bread_first_frontier = deque([node])
    depth_first_frontier = []
    explored = []
    print('--------------- STARTING BREADTH FIRST SEARCH ------------------')
    while bread_first_frontier:
        node = bread_first_frontier.popleft()
        explored.append(node.state)
        is_terminal = game.terminal_test(node.state)
        if is_terminal:
            continue
        for child in node.expand(game):
            iteration += 1
            is_terminal = game.terminal_test(child.state)
            if child.state in explored:
                print_game_tree(child, True, game, is_terminal, len(bread_first_frontier), iteration)
            else:
                if child not in bread_first_frontier:
                    print_game_tree(child, False, game, is_terminal, len(bread_first_frontier), iteration)
                    if child.depth <= 11:
                        bread_first_frontier.append(child)
                    else:
                        depth_first_frontier.append(child)

    print('------------------- EXPLORED NODES UPTO DEPTH 12 USING BFS STRATEGY -------------')
    print('------------------- STARTED EXPLORING NODES FROM DEPTH 12 USING DEPTH LIMITED SEARCH STRATEGY ------------')
    print('DEPTH FIRST FRONTIER : ' + str(len(depth_first_frontier)) + ', EXPLORED NODES :' + str(len(explored)))

    # Use depth limited search till depth 26 capturing first terminal state
    limit = 26
    depth_limited_search_frontier = depth_first_frontier.copy()
    explored_till_now = explored.copy()
    is_cutoff = False
    bread_first_frontier_adv = deque([])
    while depth_limited_search_frontier:
        node = depth_limited_search_frontier.pop()
        explored_till_now.append(node)
        is_terminal = game.terminal_test(node.state)
        if is_terminal:
            print_game_tree(node, False, game, is_terminal, len(depth_limited_search_frontier), iteration)
            continue
        elif node.depth == limit:
            is_cutoff = True
            continue
        for child in node.expand(game):
            iteration += 1
            is_terminal = game.terminal_test(child.state)
            if child.state in explored_till_now:
                print_game_tree(node, True, game, is_terminal, len(depth_limited_search_frontier), iteration)
            else:
                if child not in depth_limited_search_frontier:
                    print_game_tree(node, True, game, is_terminal, len(depth_limited_search_frontier), iteration)
                    if child.depth <= limit:
                        depth_limited_search_frontier.append(child)
                    else:
                        bread_first_frontier_adv.append(child)

    print('------------------- EXPLORED NODES UPTO DEPTH 26 USING BFS STRATEGY -------------')
    print('------------------- STARTED EXPLORING NODES FROM DEPTH 26 USING BREADTH FIRST SEARCH STRATEGY ------------')
    print('BREADTH FIRST ADV FRONTIER : ' + str(len(bread_first_frontier_adv)) + ', EXPLORED NODES :' + str(len(explored_till_now)))

    explored_adv = explored_till_now.copy()
    while bread_first_frontier_adv:
        node = bread_first_frontier_adv.popleft()
        explored_adv.append(node.state)
        is_terminal = game.terminal_test(node.state)
        if is_terminal:
            continue
        for child in node.expand(game):
            iteration += 1
            is_terminal = game.terminal_test(child.state)
            if child.state in explored_adv:
                print_game_tree(child, True, game, is_terminal, len(bread_first_frontier_adv), iteration)
            else:
                if child not in bread_first_frontier_adv:
                    print_game_tree(child, False, game, is_terminal, len(bread_first_frontier_adv), iteration)
                    bread_first_frontier_adv.append(child)

    return explored, explored_till_now, explored_adv

