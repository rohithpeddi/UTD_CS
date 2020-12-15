from collections import deque
import sys
import datetime

"""
Class GameState is used to identify the current state of the game.
State is uniquely identified by two parameters : [TO_MOVE, BOARD CONFIGURATION]
"""
class GameState:

    def __init__(self, to_move, board, utility, moves):
        self.to_move = to_move
        self.utility = utility
        self.board = board
        self.moves = moves

    # Two states are equal if they have same to_move and board configurations
    def __eq__(self, other):
        if isinstance(other, GameState):
            return self.to_move == other.to_move and self.board == other.board
        return False

"""
Class that represents a game
"""
class MultiPlayerGame:

    def __init__(self, to_move, board):
        utility = self.compute_utility(board)
        moves = self.compute_moves(to_move, board)
        self.initial = GameState(to_move=to_move, board=board, utility=utility, moves=moves)

    def actions(self, state):
        return state.moves

    def result(self, state, move):
        if move not in state.moves:
            return state
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
        # If a new state has no moves associated with it then it results in ZERO utility for each player
        new_utility = dict(P1=0, P2=0, P3=0, P4=0) if len(new_moves) == 0 else self.compute_utility(new_board)
        return GameState(to_move=next_player, board=new_board, utility=new_utility, moves=new_moves)

    def terminal_test(self, state):
        current_board = state.board
        return current_board['P1'] == (4, 4) or current_board['P2'] == (1, 4) \
               or current_board['P3'] == (1, 1) or current_board['P4'] == (4, 1) or len(state.moves) == 0

    def compute_utility(self, board):
        players = ['P1', 'P2', 'P3', 'P4']
        for player in players:
            if player == 'P1' and board[player] == (4, 4):
                return dict(P1=200, P2=10, P3=30, P4=10)
            elif player == 'P2' and board[player] == (1, 4):
                return dict(P1=100, P2=300, P3=150, P4=200)
            elif player == 'P3' and board[player] == (1, 1):
                return dict(P1=150, P2=200, P3=400, P4=300)
            elif player == 'P4' and board[player] == (4, 1):
                return dict(P1=220, P2=330, P3=440, P4=500)
        return dict(P1='?', P2='?', P3='?', P4='?')

    def compute_moves(self, to_move, board):
        players = ['P1', 'P2', 'P3', 'P4']
        x, y = board[to_move]
        blocked_positions = [board[other_player] for other_player in players if other_player is not to_move]
        actions = ['MOVE_LEFT', 'MOVE_RIGHT', 'MOVE_TOP', 'MOVE_BOTTOM']
        # Imposing boundary restrictions
        if x >= 4:
            actions.remove('MOVE_RIGHT')
        elif x <= 1:
            actions.remove('MOVE_LEFT')
        if y >= 4:
            actions.remove('MOVE_BOTTOM')
        elif y <= 1:
            actions.remove('MOVE_TOP')

        # Imposing blocking restrictions by other players
        possible_actions = actions.copy()
        for action in possible_actions:
            xn = x
            yn = y
            if action == 'MOVE_LEFT':
                xn = x - 1
            elif action == 'MOVE_RIGHT':
                xn = x + 1
            elif action == 'MOVE_TOP':
                yn = y - 1
            elif action == 'MOVE_BOTTOM':
                yn = y + 1
            if (xn, yn) in blocked_positions:
                actions.remove(action)
        return actions

    @staticmethod
    def new_board_config(state, move):
        current_player = state.to_move
        current_board_config = state.board.copy()
        x, y = current_board_config[current_player]
        xn = x
        yn = y
        if move == 'MOVE_LEFT':
            xn = x - 1
        elif move == 'MOVE_RIGHT':
            xn = x + 1
        elif move == 'MOVE_TOP':
            yn = y - 1
        elif move == 'MOVE_BOTTOM':
            yn = y + 1
        current_board_config[current_player] = (xn, yn)
        return current_board_config

    @staticmethod
    def is_winning_state_player(board, player):
        if player == 'P1' and board[player] == (4, 4):
            return True
        elif player == 'P2' and board[player] == (1, 4):
            return True
        elif player == 'P3' and board[player] == (1, 1):
            return True
        elif player == 'P4' and board[player] == (4, 1):
            return True
        else:
            return False


"""
Class that represents a node in the game tree
"""

class Node:

    def __init__(self, state, parent=None, action=None):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = 0
        self.children = []
        self.best_action = None
        self.is_repeated = False
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        node_string = "to_move : " + str(self.state.to_move)
        node_string += ", board : " + str(self.state.board)
        return node_string

    def expand(self, game):
        """List the nodes reachable in one step from this node."""
        for action in game.actions(self.state):
            child = self.child_node(game, action)
            self.children.append(child)
        return self.children

    def child_node(self, game, action):
        next_state = game.result(self.state, action)
        next_node = Node(next_state, self, action)
        return next_node

    def __hash__(self):
        return hash(self.state)

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

"""
Segment that finds out the game tree. 
Here inorder to find the game tree we use a breadth first simulation.
We consider all the possible actions for P1 from each state of the frontier and 
then all possible actions for P2 from new nodes reached by P1 performing an action. 
"""
def breadth_first_game_tree(game):
    initial_node = Node(game.initial)
    iteration = 0
    print_game_tree(initial_node, False, game, False, 0, iteration)
    bread_first_frontier = deque([initial_node])
    explored = []
    explored_nodes = []
    print('--------------- STARTING BREADTH FIRST SEARCH ------------------')
    while bread_first_frontier:
        node = bread_first_frontier.popleft()
        explored.append(node.state)
        explored_nodes.append(node)
        is_terminal = game.terminal_test(node.state)
        if is_terminal:
            continue
        for child in node.expand(game):
            iteration += 1
            is_terminal = game.terminal_test(child.state)
            if child.state in explored:
                child.is_repeated = True
                print_game_tree(child, True, game, is_terminal, len(bread_first_frontier), iteration)
            else:
                if child not in bread_first_frontier:
                    print_game_tree(child, False, game, is_terminal, len(bread_first_frontier), iteration)
                    bread_first_frontier.append(child)
    return explored_nodes, initial_node
    #return initial_node


def print_game_tree(node, is_repeated, game, is_terminal, frontier_length, iteration, is_minimax=False):

    if iteration % 1000 == 0:
        print('ITERATION :' + str(iteration) + ', DEPTH : ' + str(node.depth) + ', FRONTIER :' + str(frontier_length))

    # -------------------------------------- OUTPUT TO FILE ---------------------------------------------
    output = "[Current Player : " + str(node.state.to_move)
    output += " | Father Node : " + str(node.parent)
    output += " | Action : " + str(node.action)
    output += " | Current node : " + str(node)
    is_winning_state = False
    if is_repeated:
        output += " | REPEATED"
    if is_terminal:
        players = ['P1', 'P2', 'P3', 'P4']
        for player in players:
            if game.is_winning_state_player(node.state.board, player):
                output += " | WINS [ " + str(player)
                is_winning_state = True
                break
        if not is_winning_state:
            output += " | NO MOVES "
    if is_minimax:
        output += " | MINIMAX = " + str(node.state.utility)
    output += " ] \n"
    game_tree_file.write(output)


"""
Here we compute minimax values for all the nodes by performing a depth first search through game tree. 
As it is a multiplayer game, each player tries to maximize their utility values. 
Utility of every non terminal state is initialised to {P1:'?', P2: '?', P3: '?', P4: '?'}
Utility of every terminal node is initialised as given in the problem
"""


def minimax_value(node):
    player = node.state.to_move
    for child in node.children:
        child_utility = child.state.utility
        if child_utility[player] == '?':
            child_utility = minimax_value(child)
        if child_utility[player] is not '?':
            if node.state.utility[player] == '?' or (node.state.utility[player] < child_utility[player]):
                node.state.utility = child.state.utility
                node.best_action = child.action
    return node.state.utility


"""
Printing the game tree with Minimax Values associated with it.
Here we again traverse the game tree in a breadth first manner to print all nodes of the game tree.
"""

def game_tree_with_minimax_values(game, game_head):
    iteration = 0
    print_game_tree(game_head, False, game, False, 0, iteration, True)
    bread_first_frontier = deque([game_head])
    while bread_first_frontier:
        node = bread_first_frontier.popleft()
        is_terminal = game.terminal_test(node.state)
        if is_terminal:
            continue
        for child in node.children:
            iteration += 1
            is_terminal = game.terminal_test(child.state)
            if is_terminal:
                print_game_tree(child, child.is_repeated, game, is_terminal, len(bread_first_frontier), iteration, True)
            if child.is_repeated:
                print_game_tree(child, True, game, is_terminal, len(bread_first_frontier), iteration, True)
            else:
                bread_first_frontier.append(child)


print('------------------- STARTED COMPUTING GAME TREE FOR THE MULTIPLAYER GAME ---------------------')

to_move = 'P1'
board = dict(P1=(1, 1), P2=(4, 1), P3=(4, 4), P4=(1, 4))
multi_player_game = MultiPlayerGame(to_move, board)

print(datetime.datetime.now())
game_tree_file = open("game_tree_breadth.txt", "w")
game_tree_file.truncate(0)
game_tree, head = breadth_first_game_tree(multi_player_game)
game_tree_file.close()
print(datetime.datetime.now())

print('---------------------------------COMPUTE MINIMAX----------------------------------')

print(datetime.datetime.now())
minimax_value(head)
print(datetime.datetime.now())

print('--------------------------GAME TREE WITH MINIMAX VALUES------------------------------')

print(datetime.datetime.now())
game_tree_file = open("game_tree_breadth_minimax.txt", "w")
game_tree_file.truncate(0)
game_tree_with_minimax_values(multi_player_game, head)
game_tree_file.close()
print(datetime.datetime.now())


"""
EXTRA CREDIT :
Multiplayer Advanced with more actions/states available for each player incase they are blocked
"""

class MultiPlayerGameAdv:

    def __init__(self, to_move, board):
        utility = self.compute_utility(board)
        moves = self.compute_moves(to_move, board)
        self.initial = GameState(to_move=to_move, board=board, utility=utility, moves=moves)

    def actions(self, state):
        return state.moves

    def result(self, state, move):
        if move not in state.moves:
            return state
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
        # If a new state has no moves associated with it then it results in ZERO utility for each player
        new_utility = dict(P1=0, P2=0, P3=0, P4=0) if len(new_moves) == 0 else self.compute_utility(new_board)
        return GameState(to_move=next_player, board=new_board, utility=new_utility, moves=new_moves)

    def terminal_test(self, state):
        current_board = state.board
        return current_board['P1'] == (4, 4) or current_board['P2'] == (1, 4) or current_board['P3'] == (1, 1) or current_board['P4'] == (4, 1) or len(state.moves) == 0

    def compute_utility(self, board):
        players = ['P1', 'P2', 'P3', 'P4']
        for player in players:
            if player == 'P1' and board[player] == (4, 4):
                return dict(P1=200, P2=10, P3=30, P4=10)
            elif player == 'P2' and board[player] == (1, 4):
                return dict(P1=100, P2=300, P3=150, P4=200)
            elif player == 'P3' and board[player] == (1, 1):
                return dict(P1=150, P2=200, P3=400, P4=300)
            elif player == 'P4' and board[player] == (4, 1):
                return dict(P1=220, P2=330, P3=440, P4=500)
        return dict(P1='?', P2='?', P3='?', P4='?')

    def compute_moves(self, to_move, board):
        players = ['P1', 'P2', 'P3', 'P4']
        x, y = board[to_move]
        blocked_positions = [board[other_player] for other_player in players if other_player is not to_move]
        actions = ['MOVE_LEFT', 'MOVE_RIGHT', 'MOVE_TOP', 'MOVE_BOTTOM']
        # Imposing boundary restrictions
        if x >= 4:
            actions.remove('MOVE_RIGHT')
        elif x <= 1:
            actions.remove('MOVE_LEFT')

        if y >= 4:
            actions.remove('MOVE_BOTTOM')
        elif y <= 1:
            actions.remove('MOVE_TOP')

        # Imposing blocking restrictions by other players
        possible_actions = actions.copy()
        for action in possible_actions:
            xn = x
            yn = y
            if action == 'MOVE_LEFT':
                xn = x - 1
            elif action == 'MOVE_RIGHT':
                xn = x + 1
            elif action == 'MOVE_TOP':
                yn = y - 1
            elif action == 'MOVE_BOTTOM':
                yn = y + 1
            if (xn, yn) in blocked_positions:
                actions.remove(action)
                if action == 'MOVE_LEFT':
                    if x > 2 and (x - 2, y) not in blocked_positions:
                        actions.append('JUMP_LEFT')
                elif action == 'MOVE_RIGHT':
                    if x <= 2 and (x + 2, y) not in blocked_positions:
                        actions.append('JUMP_RIGHT')
                elif action == 'MOVE_TOP':
                    if y > 2 and (x, y - 2) not in blocked_positions:
                        actions.append('JUMP_TOP')
                elif action == 'MOVE_BOTTOM':
                    if y <= 2 and (x, y + 2) not in blocked_positions:
                        actions.append('JUMP_BOTTOM')
        return actions

    @staticmethod
    def new_board_config(state, move):
        current_player = state.to_move
        current_board_config = state.board.copy()
        x, y = current_board_config[current_player]
        xn = x
        yn = y
        if move == 'MOVE_LEFT':
            xn = x - 1
        elif move == 'JUMP_LEFT':
            xn = x - 2
        elif move == 'MOVE_RIGHT':
            xn = x + 1
        elif move == 'JUMP_RIGHT':
            xn = x + 1
        elif move == 'MOVE_TOP':
            yn = y - 1
        elif move == 'JUMP_TOP':
            yn = y - 2
        elif move == 'JUMP_BOTTOM':
            yn = y + 2
        elif move == 'MOVE_BOTTOM':
            yn = y + 1
        current_board_config[current_player] = (xn, yn)
        return current_board_config

    @staticmethod
    def is_winning_state_player(board, player):
        if player == 'P1' and board[player] == (4, 4):
            return True
        elif player == 'P2' and board[player] == (1, 4):
            return True
        elif player == 'P3' and board[player] == (1, 1):
            return True
        elif player == 'P4' and board[player] == (4, 1):
            return True
        else:
            return False


print('-------------------------------ADVANCED GAME TREE WITH MORE ACTIONS----------------------------------')

def depth_first_game_tree(game):
    initial_node = Node(game.initial)
    iteration = 0
    explored = []
    recursive_dfs(game, initial_node, explored, iteration)
    return initial_node

def recursive_dfs(game, node, explored, iteration):
    is_terminal = game.terminal_test(node.state)
    is_repeated = False
    if is_terminal:
        print_game_tree_dfs(node, is_repeated, game, is_terminal, iteration)
        return
    if node.state in explored:
        is_repeated = True
        print_game_tree_dfs(node, is_repeated, game, is_terminal, iteration)
        return
    explored.append(node.state)
    print_game_tree_dfs(node, False, game, is_terminal, iteration)
    cutoff = 500
    children = node.expand(game)
    for child in children:
        iteration += 1
        if child.depth < cutoff:
            iteration = recursive_dfs(game, child, explored, iteration)
    return iteration

def print_game_tree_dfs(node, is_repeated, game, is_terminal, iteration):

    if iteration % 1000 == 0:
        print('ITERATION :' + str(iteration) + ', DEPTH : ' + str(node.depth))
    st = "[Current Player : P1 | Father Node : to_move : P4, board : {'P1': (2, 2), 'P2': (2, 1), 'P3': (1, 3), 'P4': (4, 2)} | Action : MOVE_TOP | Current node : to_move : P1, board : {'P1': (2, 2), 'P2': (2, 1), 'P3': (1, 3), 'P4': (4, 1)} | WINS [ P4 ] \n"
    # -------------------------------------- OUTPUT TO FILE ---------------------------------------------
    output = "[Current Player : " + str(node.state.to_move)
    output += " | Father Node : " + str(node.parent)
    output += " | Action : " + str(node.action)
    output += " | Current node : " + str(node)
    is_winning_state = False
    if is_repeated:
        output += " | REPEATED"
    if is_terminal:
        players = ['P1', 'P2', 'P3', 'P4']
        for player in players:
            if game.is_winning_state_player(node.state.board, player):
                output += " | WINS [ " + str(player)
                is_winning_state = True
                break
        if not is_winning_state:
            output += " | NO MOVES "
    output += " ] \n"

    if iteration % 1000 == 0 and iteration > 27000:
        game_tree_file.write(st)
    game_tree_file.write(output)


def breadth_first_depth_first_combined(game):
    node = Node(game.initial)
    iteration = 0
    print_game_tree_dfs(node, False, game, False,  iteration)
    bread_first_frontier = deque([node])
    depth_first_frontier = []
    explored = []

    print('--------------- STARTING BREADTH FIRST SEARCH ------------------')
    cutoff = 38450
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
                print_game_tree_dfs(child, True, game, is_terminal,  iteration)
            else:
                if child not in bread_first_frontier:
                    print_game_tree_dfs(child, False, game, is_terminal, iteration)
                    if child.depth <= 13:
                        bread_first_frontier.append(child)
                    else:
                        depth_first_frontier.append(child)

    print('------------------- EXPLORED NODES UPTO DEPTH 14 USING BFS STRATEGY -------------')
    print('------------------- STARTED EXPLORING NODES FROM DEPTH 14 USING DEPTH FIRST SEARCH STRATEGY ------------')
    print('DEPTH FIRST FRONTIER : ' + str(len(depth_first_frontier)) + ', EXPLORED NODES :' + str(len(explored)))

    # Use depth limited search till depth 26 capturing first terminal state
    limit = 40
    while depth_first_frontier:
        if iteration > cutoff:
            return
        node = depth_first_frontier.pop()
        explored.append(node.state)
        is_terminal = game.terminal_test(node.state)
        if is_terminal:
            continue
        for child in node.expand(game):
            iteration += 1
            is_terminal = game.terminal_test(child.state)
            if child.state in explored:
                print_game_tree_dfs(child, True, game, is_terminal,  iteration)
            else:
                if child not in depth_first_frontier:
                    print_game_tree_dfs(child, False, game, is_terminal, iteration)
                    if child.depth <= limit:
                        depth_first_frontier.append(child)
    return explored

sys.setrecursionlimit(200000)
to_move = 'P1'
board = dict(P1=(1, 1), P2=(4, 1), P3=(4, 4), P4=(1, 4))
multi_player_game_adv = MultiPlayerGameAdv(to_move, board)

print(datetime.datetime.now())
game_tree_file = open("game_tree_dfs_adv.txt", "w")
game_tree_file.truncate(0)
head = breadth_first_depth_first_combined(multi_player_game_adv)
game_tree_file.close()
print(datetime.datetime.now())

print('------------------------------------------ FINISHED PROCESSING --------------------------------------')

