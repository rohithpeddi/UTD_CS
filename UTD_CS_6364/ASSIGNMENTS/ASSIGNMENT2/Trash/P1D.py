from collections import deque
"""
State maintenance :
1. ('P1', [(), (), (), ()]) or ('P1', [1,2,3,4]) / (0, [(), (), (), ()])
2. Utility : [0,0,0,0]
3. Moves : ['L', 'R', 'B', 'T']
"""


class GameState:

    def __init__(self, to_move, board, utility, moves):
        self.to_move = to_move
        self.utility = utility
        self.board = board
        self.moves = moves

    def __eq__(self, other):
        return isinstance(other, GameState) and self.to_move == other.to_move and self.utility == other.utility and self.board == other.board and self.moves == other.moves


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
        if len(new_moves) == 0:
            new_utility = dict(P1=0, P2=0, P3=0, P4=0)
        else:
            new_utility = self.compute_utility(new_board)
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
        if len(new_moves) == 0:
            new_utility = dict(P1=0, P2=0, P3=0, P4=0)
        else:
            new_utility = self.compute_utility(new_board)
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
                    if x > 2 and (x-2, y) not in blocked_positions:
                        actions.append('JUMP_LEFT')
                elif action == 'MOVE_RIGHT':
                    if x <= 2 and (x+2, y) not in blocked_positions:
                        actions.append('JUMP_RIGHT')
                elif action == 'MOVE_TOP':
                    if y > 2 and (x, y-2) not in blocked_positions:
                        actions.append('JUMP_TOP')
                elif action == 'MOVE_BOTTOM':
                    if y <= 2 and (x, y+2) not in blocked_positions:
                        actions.append('JUMP_BOTTOM')
        return actions


class Node:

    def __init__(self, state, parent=None, action=None):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = 0
        self.children = []
        self.best_action = None
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


def depth_first_game_tree(game):
    initial_node = Node(game.initial)
    is_terminal = game.terminal_test(initial_node.state)
    iteration = 0
    print_game_tree(initial_node, False, game, is_terminal, 0, iteration)
    frontier = [(Node(game.initial))]  # Stack
    explored = []
    explored_nodes = []
    while frontier:
        node = frontier.pop()
        is_terminal = game.terminal_test(node.state)
        if is_terminal:
            continue
        explored.append(node.state)
        explored_nodes.append(node)
        for child in node.expand(game):
            iteration += 1
            is_terminal = game.terminal_test(child.state)
            if child.state in explored:
                print_game_tree(child, True, game, is_terminal, len(frontier), iteration)
            else:
                if child not in frontier:
                    print_game_tree(child, False, game, is_terminal, len(frontier), iteration)
                    frontier.append(child)
    return explored_nodes, initial_node


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
                    if child.depth <= 14:
                        bread_first_frontier.append(child)
                    else:
                        depth_first_frontier.append(child)

    print('------------------- EXPLORED NODES UPTO DEPTH 12 USING BFS STRATEGY -------------')
    print('------------------- STARTED EXPLORING NODES FROM DEPTH 12 USING DEPTH LIMITED SEARCH STRATEGY ------------')
    print('DEPTH FIRST FRONTIER : ' + str(len(depth_first_frontier)) + ', EXPLORED NODES :' + str(len(explored)))

    # Use depth limited search till depth 26 capturing first terminal state
    limit = 25
    bread_first_frontier_adv = deque([])
    while depth_first_frontier:
        node = depth_first_frontier.pop()
        explored.append(node.state)
        is_terminal = game.terminal_test(node.state)
        if is_terminal:
            continue
        for child in node.expand(game):
            iteration += 1
            is_terminal = game.terminal_test(child.state)
            if child.state in explored:
                print_game_tree(child, True, game, is_terminal, len(depth_first_frontier), iteration)
            else:
                if child not in depth_first_frontier:
                    print_game_tree(child, False, game, is_terminal, len(depth_first_frontier), iteration)
                    if child.depth <= limit:
                        depth_first_frontier.append(child)
                    else:
                        bread_first_frontier_adv.append(child)

    print('------------------- EXPLORED NODES UPTO DEPTH 26 USING BFS STRATEGY -------------')
    print('------------------- STARTED EXPLORING NODES FROM DEPTH 26 USING BREADTH FIRST SEARCH STRATEGY ------------')
    print('BREADTH FIRST ADV FRONTIER : ' + str(len(bread_first_frontier_adv)) + ', EXPLORED NODES :' + str(len(explored)))

    while bread_first_frontier_adv:
        node = bread_first_frontier_adv.popleft()
        explored.append(node.state)
        is_terminal = game.terminal_test(node.state)
        if is_terminal:
            continue
        for child in node.expand(game):
            iteration += 1
            is_terminal = game.terminal_test(child.state)
            if child.state in explored:
                print_game_tree(child, True, game, is_terminal, len(bread_first_frontier_adv), iteration)
            else:
                if child not in bread_first_frontier_adv:
                    print_game_tree(child, False, game, is_terminal, len(bread_first_frontier_adv), iteration)
                    bread_first_frontier_adv.append(child)

    return explored


def print_game_tree(node, is_repeated, game, is_terminal, frontier_length, iteration, is_minimax=False):

    if iteration % 1000 == 0:
        print('ITERATION :' + str(iteration) + ', DEPTH : ' + str(node.depth) + ', FRONTIER :' + str(frontier_length))
    if node.depth <= 3 or is_terminal:
        print('----------------------------------------------------------------------------')
        print('CURRENT PLAYER : ' + str(node.state.to_move))
        print('PARENT : ' + str(node.parent))
        print('ACTION : ' + str(node.action))
        print('CURRENT NODE:' + str(node))
        print('REPEATED : ' + str(is_repeated))
        print('DEPTH : ' + str(node.depth))
        print('FRONTIER LENGTH : ' + str(frontier_length))
        is_winning_state = False
        if is_minimax:
            print('MINIMAX : ' + str(node.state.utility))
        if is_terminal:
            players = ['P1', 'P2', 'P3', 'P4']
            for player in players:
                if game.is_winning_state_player(node.state.board, player):
                    is_winning_state = True
                    print("WINS : " + str(player))
                    break
            if not is_winning_state:
                print("TERMINAL STATE WITH NO MOVES")

    # -------------------------------------- OUTPUT TO FILE ---------------------------------------------
    # output = "[Current Player : " + str(node.state.to_move)
    # output += " | Father Node : " + str(node.parent)
    # output += " | Action : " + str(node.action)
    # output += " | Current node : " + str(node)
    # is_winning_state = False
    # if is_repeated:
    #     output += " | REPEATED"
    # if is_terminal:
    #     players = ['P1', 'P2', 'P3', 'P4']
    #     for player in players:
    #         if game.is_winning_state_player(node.state.board, player):
    #             output += " | WINS [ " + str(player)
    #             is_winning_state = True
    #             break
    #     if not is_winning_state:
    #         output += " | NO MOVES "
    # if is_minimax:
    #     output += " | MINIMAX = " + str(node.state.utility)
    # output += " ] \n"
    # game_tree_file.write(output)


def compute_minimax(game_tree):
    game_tree_copy = game_tree.copy()
    while game_tree_copy:
        child_node = game_tree_copy.pop()
        parent_node = child_node.parent
        if parent_node:
            parent_player = parent_node.state.to_move
            if child_node.state.utility[parent_player] is not '?':
                if parent_node.state.utility[parent_player] == '?' or (parent_node.state.utility[parent_player] < child_node.state.utility[parent_player]):
                    parent_node.state.utility = child_node.state.utility
                    parent_node.best_action = child_node.action


def game_tree_with_minimax_values(game, game_head):
    iteration = 0
    print_game_tree(game_head, False, game, False, 0, iteration, True)
    bread_first_frontier = deque([game_head])
    explored = []
    while bread_first_frontier:
        node = bread_first_frontier.popleft()
        explored.append(node.state)
        is_terminal = game.terminal_test(node.state)
        if is_terminal:
            continue
        for child in node.children:
            iteration += 1
            is_terminal = game.terminal_test(child.state)
            if child.state in explored:
                print_game_tree(child, True, game, is_terminal, len(bread_first_frontier), iteration, True)
            else:
                if child not in bread_first_frontier:
                    print_game_tree(child, False, game, is_terminal, len(bread_first_frontier), iteration, True)
                    bread_first_frontier.append(child)

to_move = 'P1'
board = dict(P1=(1, 1), P2=(4, 1), P3=(4, 4), P4=(1, 4))
multi_player_game_adv = MultiPlayerGameAdv(to_move, board)
# multi_player_game = MultiPlayerGame(to_move, board)
# breadth_first_depth_first_combined(multi_player_game)
breadth_first_depth_first_combined(multi_player_game_adv)

# game_tree_file = open("game_tree_depth.txt", "w")
# game_tree_file.truncate(0)
# game_tree, head = depth_first_game_tree(multi_player_game)
# game_tree_file.close()
#
# print('---------------------------------COMPUTE MINIMAX----------------------------------')
#
# compute_minimax(game_tree)
#
# print('--------------------------GAME TREE WITH MINIMAX VALUES------------------------------')
#
# game_tree_file = open("game_tree_depth_minimax.txt", "w")
# game_tree_file.truncate(0)
# game_tree_with_minimax_values(multi_player_game, head)
# game_tree_file.close()
#
# print('-------------------------------ADVANCED GAME TREE WITH MORE ACTIONS----------------------------------')
#
# to_move = 'P1'
# board = dict(P1=(1, 1), P2=(4, 1), P3=(4, 4), P4=(1, 4))
# multi_player_game_adv = MultiPlayerGameAdv(to_move, board)
#
# game_tree_file = open("game_tree_depth_adv.txt", "w")
# game_tree_file.truncate(0)
# game_tree, head = depth_first_game_tree(multi_player_game_adv)
# game_tree_file.close()
#
# print('---------------------------------COMPUTE MINIMAX----------------------------------')
#
# compute_minimax(game_tree)
#
# print('--------------------------GAME TREE WITH MINIMAX VALUES------------------------------')
#
# game_tree_file = open("game_tree_depth_minimax_adv.txt", "w")
# game_tree_file.truncate(0)
# game_tree_with_minimax_values(multi_player_game_adv, head)
# game_tree_file.close()