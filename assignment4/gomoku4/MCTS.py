import random
import SimulationPlayer

class MCTSObject(object):

    def __init__(self):
        self.scores = {} #Store the number of games and the number of games won. board: [num, won]
        self.SIM_NUM = 10
        self.sim = SimulationPlayer.GomokuSimulationPlayer(playout_policy = 'rule_based')
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
        for a in range(20):
            print(a)
            board = org_board.copy()
            player = org_player
            b_code = self.code(board, player)
            back_prop = [] #contains the backlog of board states which should be updated
            #While traversing the known tree
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
                code = self.ucb_selection(codes)
                b_code = code[0]
                board.board[code[1]] = player
                #Switch the current player
                player = op
            #The search has found a new board state to run simulations on
            self.scores[b_code] = [self.SIM_NUM, 0]
            wins = 0
            losses = 0
            #Run simulations
            for x in range(self.SIM_NUM):
                result = self.sim._do_playout(board, player)
                if result == 1:
                    self.scores[b_code][1] += 1
                    wins += 1
                elif result == -1:
                    losses += 1

            #Update the tree based on the simulations
            cur_player = opponent(player)
            for code in back_prop:
                self.scores[code][0] += self.SIM_NUM
                if cur_player == player:
                    self.scores[code][1] += wins
                else:
                    self.scores[code][1] += losses
                cur_player = opponent(cur_player)


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
                wins = self.scores[code][1]
                if wins > most_wins:
                    most_wins = wins
                    best_move = move
        if best_move == None:
            best_move = self.sim._random_moves(board, player)[0]
        board.board[best_move] = player
