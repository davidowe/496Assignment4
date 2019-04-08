import random
import SimulationPlayer
import math
from board_util import GoBoardUtil

class MCTSObject(object):

    def __init__(self):
        self.scores = {} #Store the number of games and the number of games won. board: [num, won]
        self.SIM_NUM = 5
        self.sim = SimulationPlayer.GomokuSimulationPlayer(playout_policy = 'random')
        self.INFINITY = 10000000000

    def ucb(self, sum, n, total):
        return sum / n + 0.25 * math.sqrt(math.log(total)/n)

    #Select a board code by their ucb scores
    def ucb_selection(self, codes):
        for code in codes:
            if code[0] not in self.scores:
                return code
        total = 0
        for code in codes:
            total += self.scores[code[0]][0]
        maxScore = -self.INFINITY
        maxCode = None
        for code in codes:
            score = self.scores[code[0]]
            ucb_score = self.ucb(score[1], score[0], total)
            if ucb_score > maxScore:
                maxScore = ucb_score
                maxCode = code
        return maxCode

    #Create a code from the board and player
    def code(self, board, player):
        return str(board.board) + str(player)

    def opponent(self, player):
        if player == 1:
            return 2
        return 1

    def get_color(self, board, i, j):
        return board.board[board.pt(i, j)]

    def set_color(self, board, i, j, color):
        board.board[board.pt(i, j)] = color

    #Update the score tree
    #TODO currently needs to do simulations on every possible new state encountered,
    #should be initializing the states scores with heuristics as simulations are much too slow
    def update_tree(self, board, player):
        org_board = board.copy()
        org_player = player
        #Do a number of updating iterations, should be based on a timer TODO
        for a in range(300):
            print(a)
            board = org_board.copy()
            player = org_player
            b_code = self.code(board, player)
            back_prop = [] #contains the backlog of board states which should be updated
            #While traversing the known tree
            # print('one')
            while b_code in self.scores:
                #Add the board state to back_prop
                back_prop.append(b_code)
                moves = self.sim._random_moves(board, player)
                op = self.opponent(player)
                codes = []
                #Get all the possible moves of the current player
                for move in moves:
                    board.board[move] = player
                    codes.append((self.code(board, op), move))
                    board.board[move] = 0
                #Select the move with the best ucb score (or a new move)
                # print('two')
                code = self.ucb_selection(codes)
                b_code = code[0]
                board.board[code[1]] = player
                #Switch the current player
                player = op
                # print('three')
            #The search has found a new board state to run simulations on
            # print('four')
            if len(back_prop) > 0:
                del back_prop[0]
            self.scores[b_code] = [self.SIM_NUM, 0]
            wins = 0
            losses = 0
            #Run simulations
            for x in range(self.SIM_NUM):
                # print("hmmm", x)
                result = self.sim._do_playout(board, player)
                if result == 1:
                    self.scores[b_code][1] += 1
                    wins += 1
                elif result == -1:
                    losses += 1

            # print('five')
            #Update the tree based on the simulations
            cur_player = self.opponent(player)
            for code in back_prop:
                self.scores[code][0] += self.SIM_NUM
                if cur_player == player:
                    self.scores[code][1] += wins
                else:
                    self.scores[code][1] += losses
                cur_player = self.opponent(cur_player)

            # print('six')


    #Make the move that has the most simulation wins in the score tree
    def make_move(self, board, player):
        best_move = None
        most_wins = 0
        op = self.opponent(player)
        for move in board.get_empty_points():
            board.board[move] = player
            code = self.code(board, op)
            board.board[move] = 0
            if code in self.scores:
                wins = self.scores[code][1] / self.scores[code][0]
                if wins > most_wins:
                    most_wins = wins
                    best_move = move
        if best_move == None:
            best_move = self.sim._random_moves(board, player)[0]
        board.board[best_move] = player

    def print_tree(self, board, player):
        op = self.opponent(player)
        for move in board.get_empty_points():
            board.board[move] = player
            b_code = self.code(board, op)
            if b_code in self.scores:
                if self.scores[b_code][0] > 5:
                    print('\n', str(GoBoardUtil.get_twoD_board(board)))
                print(self.scores[b_code])
                self.print_tree(board, op)
            board.board[move] = 0

def opponent(player):
    if player == 1:
        return 2
    return 1

def ucb(sum, n, total):
    return sum / n + 0.25 * math.sqrt(math.log(total)/n)

class Node:
    def __init__(self, parent, move, board, player):
        self.wins = 0
        self.visits = 0
        self.parent_node = parent
        self.child_nodes = []
        self.move = move #The last move that was played
        self.board = board.copy() #The current board state
        self.unexplored_moves = list(self.board.get_empty_points())
        self.player = player #The player to play next

    def select_child(self):
        maxScore = -100
        maxChild = None
        for child in self.child_nodes:
            score = ucb(child.wins, child.visits, self.visits)
            if score > maxScore:
                maxScore = score
                maxChild = child
        return maxChild

class NEW_MCTS:
    def __init__(self, board, player):
        self.board = board.copy()
        self.player = player
        self.root_node = Node(None, None, board, player)
        self.sim = SimulationPlayer.GomokuSimulationPlayer(playout_policy = 'random')

    def game_result(self, board, player):
        game_end, winner = board.check_game_end_gomoku()
        if game_end:
            if winner == player:
                return 1
            elif winner == opponent(player):
                return -1
            else:
                print("ERROR ERROR ERROR ERROR ERROR ERROR ERROR ERROR")
        moves = board.get_empty_points()
        if len(moves) == 0:
            return 0
        return None

    def playout(self, board, player):
        board = board.copy()
        cur = player
        res = self.game_result(board, player)
        while res == None:
            move = board.get_empty_points()[random.randint(0, len(board.get_empty_points()) - 1)]
            board.board[move] = cur
            cur = opponent(cur)
            res = self.game_result(board, player)
        return res

    def update_tree(self):
        #SELECT
        node = self.root_node
        while len(node.unexplored_moves) == 0 and len(node.child_nodes) > 0:
            node = node.select_child()
            self.board.board[node.move] = opponent(node.player)

        #EXPAND
        if len(node.unexplored_moves) > 0:
            move = node.unexplored_moves[random.randint(0, len(node.unexplored_moves) - 1)]
            self.board.board[move] = node.player
            new_node = Node(node, move, self.board, opponent(node.player))
            node.unexplored_moves.remove(move)
            node.child_nodes.append(new_node)
            node = new_node

        #SIMULATE
        result = self.playout(node.board, node.player)
        print(result)

        #UPDATE
        while True:
            node.visits += 1
            if result == 1:
                node.wins += 1
            parent = node.parent_node
            if parent == None:
                break
            node = parent
            result *= -1

    def get_move(self):
        maxScore = -1
        maxChild = None
        for child in self.root_node.child_nodes:
            if child.visits > maxScore:
                maxScore = child.visits
                maxChild = child
        return maxChild.move
