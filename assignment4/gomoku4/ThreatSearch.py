import simple_board


def opponent(player):
    if player == 1:
        return 2
    else:
        return 1

class TSearch:
    #initializes the dictionaries containing threat patterns
    def __init__(self, player):
        #Each threat is a list containing either the player, 0, or the opponent as it's elements.
        #The pattern matches if each consecutive position in a given line on the board matches each
        #element of the pattern list.
        #The _play lists contain each possible move the player can make to enforce the threat/win.
        #The number represent the distance from the first element of the list wheree the player should play
        #The _cost lists contain lists for each possible player move in _play that respresent the opponents possible
        #counter moves that they can play to prevent the player from winning. The numbers in these lists also represent
        #the distance from the first element of the list.
        #Example:
        #test_pattern = [0, 0, player, 0, 0]
        #test_pattern_play = [1, 3]
        #test_pattern_cost = [[0, 3], [1, 4]]
        #Then after the player plays the line would look like either 0, player, player, 0, 0 or 0, 0, player, player, 0
        #And after the opponent countermoves: op, player, player, op, 0 or 0, op, player, player, op
        #According to the threat search we always play all possible opponent counter moves
        #A pattern not having a cost means that it doesn't matter what the opponent plays the player will always win
        op = opponent(player)
        #Immediate threats, attacker wins immediately
        straight_four = [0, player, player, player, player, 0]
        straight_four_play = [0, 5]
        four = [op, player, player, player, player, 0]
        four_play = [5]
        four_reverse = [0, player, player, player, player, op]
        four_reverse_play = [0]
        broken_four_1 = [player, 0, player, player, player]
        broken_four_1_play = [1]
        broken_four_2 = [player, player, 0, player, player]
        broken_four_2_play = [2]
        broken_four_3 = [player, player, player, 0, player]
        broken_four_3_play = [3]
        #Immediate threats, attacker wins next turn
        open_three = [0, 0, player, player, player, 0, 0]
        open_three_play = [1, 5]
        three = [op, 0, player, player, player, 0, 0]
        three_play = [5]
        three_reverse = [0, 0, player, player, player, 0, op]
        three_reverse_play = [1]
        broken_three = [0, player, player, 0, player, 0]
        broken_three_play = [3]
        broken_three_reverse = [0, player, 0, player, player, 0]
        broken_three_reverse_play = [2]
        #Positions that go into immediate threats
        into_open_three_1 = [0, 0, player, player, 0, 0, 0]
        into_open_three_1_play = [1, 4, 5]
        into_open_three_1_cost = [[0, 4, 5], [1, 5], [1, 4, 6]]
        into_open_three_2 = [0, 0, player, 0, player, 0, 0]
        into_open_three_2_play = [1, 3, 5]
        into_open_three_2_cost = [[0, 3, 5], [1, 5], [1, 3, 6]]
        into_open_three_3 = [0, 0, 0, player, player, 0, 0]
        into_open_three_3_play = [1, 2, 5]
        into_open_three_3_cost = [[0, 2, 5], [1, 5], [1, 2, 6]]
        into_three_1 = [op, 0, player, player, 0, 0, 0]
        into_three_1_play = [4, 5]
        into_three_1_cost = [[1, 5, 6], [1, 4, 6]]
        into_three_2 = [op, 0, player, 0, player, 0, 0]
        into_three_2_play = [3, 5]
        into_three_2_cost = [[1, 5, 6], [1, 3, 6]]
        into_three_3 = [op, 0, 0, player, player, 0, 0]
        into_three_3_play = [1, 5]
        into_three_3_cost = [[1, 5, 6], [1, 2, 6]]
        into_three_1_reverse = [0, 0, player, player, 0, 0, op]
        into_three_1_reverse_play = [1, 4]
        into_three_1_reverse_cost = [[0, 4, 5], [0, 1, 5]]
        into_three_2_reverse = [0, 0, player, 0, player, 0, op]
        into_three_2_reverse_play = [1, 3]
        into_three_2_reverse_cost = [[0, 3, 5], [0, 1, 5]]
        into_three_3_reverse = [0, 0, 0, player, player, 0, op]
        into_three_3_reverse_play = [1, 2]
        into_three_3_reverse_cost = [[0, 2, 5], [0, 1, 5]]
        into_four_1 = [op, 0, player, player, player, 0, op]
        into_four_1_play = [1, 5]
        into_four_1_cost = [[5], [1]]
        into_four_2 = [op, player, 0, player, player, 0]
        into_four_2_play = [2, 5]
        into_four_2_cost = [[5], [2]]
        into_four_3 = [op, player, player, 0, player, 0]
        into_four_3_play = [3, 5]
        into_four_3_cost = [[5], [3]]
        into_four_4 = [op, player, player, player, 0, 0]
        into_four_4_play = [4, 5]
        into_four_4_cost = [[5], [4]]
        into_four_2_reverse = [0, player, player, 0, player, op]
        into_four_2_reverse_play = [0, 3]
        into_four_2_reverse_cost = [[3], [0]]
        into_four_3_reverse = [0, player, 0, player, player, op]
        into_four_3_reverse_play = [0, 2]
        into_four_3_reverse_cost = [[2], [0]]
        into_four_4_reverse = [0, 0, player, player, player, op]
        into_four_4_reverse_play = [0, 1]
        into_four_4_reverse_cost = [[1], [0]]
        into_broken_four_1 = [player, player, 0, 0, player]
        into_broken_four_1_play = [2, 3]
        into_broken_four_1_cost = [[3], [2]]
        into_broken_four_2 = [player, 0, player, 0, player]
        into_broken_four_2_play = [1, 3]
        into_broken_four_2_cost = [[3], [1]]
        into_broken_four_3 = [player, 0, 0, player, player]
        into_broken_four_3_play = [1, 2]
        into_broken_four_3_cost = [[2], [1]]

        self.patterns = {'four': four, 'four_reverse': four_reverse, 'straight_four': straight_four, 'broken_four_1': broken_four_1, 'broken_four_2': broken_four_2, 'broken_four_3': broken_four_3, 'open_three': open_three, \
                    'three': three, 'three_reverse': three_reverse, 'broken_three': broken_three, 'broken_three_reverse': broken_three_reverse, \
                    'into_open_three_1': into_open_three_1, 'into_open_three_2': into_open_three_2, 'into_open_three_3': into_open_three_3, \
                    'into_three_1': into_three_1, 'into_three_2': into_three_2, 'into_three_3': into_three_3, \
                    'into_three_1_reverse': into_three_1_reverse, 'into_three_2_reverse': into_three_2_reverse, 'into_three_3_reverse': into_three_3_reverse, \
                    'into_four_1': into_four_1, 'into_four_2': into_four_2, 'into_four_3': into_four_3, 'into_four_4': into_four_4,  \
                    'into_four_2_reverse': into_four_2_reverse, 'into_four_3_reverse': into_four_3_reverse, 'into_four_4_reverse': into_four_4_reverse, \
                    'into_broken_four_1': into_broken_four_1, 'into_broken_four_2': into_broken_four_2, 'into_broken_four_3': into_broken_four_3}

        self.play = {'four': four_play, 'four_reverse': four_reverse_play, 'straight_four': straight_four_play, 'broken_four_1': broken_four_1_play, 'broken_four_2': broken_four_2_play, 'broken_four_3': broken_four_3_play, 'open_three': open_three_play, \
                    'three': three_play, 'three_reverse': three_reverse_play, 'broken_three': broken_three_play, 'broken_three_reverse': broken_three_reverse_play, \
                    'into_open_three_1': into_open_three_1_play, 'into_open_three_2': into_open_three_2_play, 'into_open_three_3': into_open_three_3_play, \
                    'into_three_1': into_three_1_play, 'into_three_2': into_three_2_play, 'into_three_3': into_three_3_play, \
                    'into_three_1_reverse': into_three_1_reverse_play, 'into_three_2_reverse': into_three_2_reverse_play, 'into_three_3_reverse': into_three_3_reverse_play, \
                    'into_four_1': into_four_1_play, 'into_four_2': into_four_2_play, 'into_four_3': into_four_3_play, 'into_four_4': into_four_4_play,  \
                    'into_four_2_reverse': into_four_2_reverse_play, 'into_four_3_reverse': into_four_3_reverse_play, 'into_four_4_reverse': into_four_4_reverse_play, \
                    'into_broken_four_1': into_broken_four_1_play, 'into_broken_four_2': into_broken_four_2_play, 'into_broken_four_3': into_broken_four_3_play}

        self.cost = {'into_open_three_1': into_open_three_1_cost, 'into_open_three_2': into_open_three_2_cost, 'into_open_three_3': into_open_three_3_cost, \
                    'into_three_1': into_three_1_cost, 'into_three_2': into_three_2_cost, 'into_three_3': into_three_3_cost, \
                    'into_three_1_reverse': into_three_1_reverse_cost, 'into_three_2_reverse': into_three_2_reverse_cost, 'into_three_3_reverse': into_three_3_reverse_cost, \
                    'into_four_1': into_four_1_cost, 'into_four_2': into_four_2_cost, 'into_four_3': into_four_3_cost, 'into_four_4': into_four_4_cost,  \
                    'into_four_2_reverse': into_four_2_reverse_cost, 'into_four_3_reverse': into_four_3_reverse_cost, 'into_four_4_reverse': into_four_4_reverse_cost, \
                    'into_broken_four_1': into_broken_four_1_cost, 'into_broken_four_2': into_broken_four_2_cost, 'into_broken_four_3': into_broken_four_3_cost}

        # self.isImmediate = {'five': True, 'four': True, 'four_reverse': True, 'straight_four': True, 'broken_four_1': True, 'broken_four_2': True, \
        #                     'broken_four_3': True, 'open_three': True, 'three': True, 'three_reverse': True, 'broken_three': True, \
        #                     'broken_three_reverse': True, 'into_open_three_1': False, 'into_open_three_2': False, 'into_open_three_3': False, \
        #                     'into_three_1': False, 'into_three_2': False, 'into_three_3': False, 'into_three_1_reverse': False, \
        #                     'into_three_2_reverse': False, 'into_three_3_reverse': False, 'into_four_1': False, 'into_four_2': False, 'into_four_3': False, \
        #                     'into_four_4': False, 'into_four_2_reverse': False, 'into_four_3_reverse': False, 'into_four_4_reverse': False}

        self.threat_num = 0

    def get_color(self, board, i, j):
        return board.board[board.pt(i, j)]

    def set_color(self, board, i, j, color):
        board.board[board.pt(i, j)] = color

    #Returns the name of any threat that lies on the line starting at (i, j) moving in xdir and ydir
    def is_threat(self, board, player, i, j, xdir, ydir):
        #out of bounds
        if i < 0 or j < 0 or i > board.size + 1 or j > board.size + 1:
            return []

        #Possible threat names
        names = ['four', 'four_reverse', 'straight_four', 'broken_four_1', 'broken_four_2', 'broken_four_3', 'open_three', 'three', 'three_reverse', 'broken_three', \
                'broken_three_reverse', 'into_open_three_1', 'into_open_three_2', 'into_open_three_3', 'into_three_1', \
                'into_three_2', 'into_three_3', 'into_three_1_reverse', 'into_three_2_reverse', 'into_three_3_reverse', \
                'into_four_1', 'into_four_2', 'into_four_3', 'into_four_4', 'into_four_2_reverse', 'into_four_3_reverse', \
                'into_four_4_reverse', 'into_broken_four_1', 'into_broken_four_2', 'into_broken_four_3']

        op = opponent(player)

        #Search the line for threats
        for x in range(7):
            to_remove = []
            #For all patterns not yet eliminated
            for pattern in names:
                lst = self.patterns[pattern]
                #This check is for replacing the initial 'op' with the edge of the board
                #Only applies for pattern starting with 'op' and lines starting outside the
                #board boundries
                if x == 0 and (i < 1 or j < 1 or i > board.size):
                    if lst[0] == op:
                        continue
                    else:
                        to_remove.append(pattern)
                        continue
                #Continue if the whole line has already been checked
                if len(lst) <= x:
                    continue
                #This check is the same as the one for the initial 'op' except its for a trailing 'op'
                if i > board.size or i < 1 or j > board.size:
                    if not (x == len(lst) - 1 and lst[-1] == op):
                        to_remove.append(pattern)
                    continue
                #Check if the board actually matches the pattern
                if self.patterns[pattern][x] != self.get_color(board, i, j):
                    to_remove.append(pattern)
            #Remove any non-matching patterns
            for pattern in to_remove:
                names.remove(pattern)
            if len(names) == 0 or j > board.size:
                break
            #Progress along the line
            i += xdir
            j += ydir

        return names

    #Takes a _play list and converts it into actual coordinates based on the line that was looked at
    def plays_to_coords(self, plays, i, j, xdir, ydir):

        coords = []
        for play in plays:
            coords.append((i + xdir * play, j + ydir * play))
        return coords

    #Check a single (i, j) position on the board for any threats that could involve it
    #For any threat it finds i calls threat_sequence on to see if there is a winning threat sequence
    #If a winning threat sequence is found return the coordinates of the play that would win for the player
    def threat_spot_check(self, board, player, i, j, threat_lst=None, threat_points=None):
        for y in range(5):
            name = self.is_threat(board, player, i - y, j, 1, 0)
            if len(name) > 0:
                self.threat_num += 1
                returned = self.threat_sequence(board, player, i - y, j, 1, 0, name[0], threat_lst, threat_points)
                if returned[0] != None:
                    return returned
            name = self.is_threat(board, player, i, j - y, 0, 1)
            if len(name) > 0:
                self.threat_num += 1
                returned = self.threat_sequence(board, player, i, j - y, 0, 1, name[0], threat_lst, threat_points)
                if returned[0] != None:
                    return returned
            name = self.is_threat(board, player, i - y, j - y, 1, 1)
            if len(name) > 0:
                self.threat_num += 1
                returned = self.threat_sequence(board, player, i - y, j - y, 1, 1, name[0], threat_lst, threat_points)
                if returned[0] != None:
                    return returned
            name = self.is_threat(board, player, i + y, j - y, -1, 1)
            if len(name) > 0:
                self.threat_num += 1
                returned = self.threat_sequence(board, player, i + y, j - y, -1, 1, name[0], threat_lst, threat_points)
                if returned[0] != None:
                    return returned
        return None, 3

    #Checks if there is a winning threat sequence based on a given threat
    #Returns the coordinates the player should play to win if a winning threat sequence is found
    def threat_sequence(self, board, player, i, j, xdir, ydir, name, threat_lst=None, threat_points=None, is_immediate=False):
        #Winning threat was found
        if name not in self.cost:
            if is_immediate:
                if name in ['straight_four', 'four', 'four_reverse', 'broken_four_1', 'broken_four_2', 'broken_four_3']:
                    return self.plays_to_coords(self.play[name], i, j, xdir, ydir)[0], 1
                else:
                    return self.plays_to_coords(self.play[name], i, j, xdir, ydir)[0], 2
            return self.plays_to_coords(self.play[name], i, j, xdir, ydir)[0], 3
        play_coords = self.plays_to_coords(self.play[name], i, j, xdir, ydir)
        op = opponent(player)

        #For all possible plays of the player
        for x in range(len(play_coords)):
            new_board = board.copy() #TODO: can undo moves rather than copy a board to improve performance
            # if threat_lst != None:
            #     if threat_points == None:
            #         new_threat_points = {'gain': [], 'cost': []}
            #     else:
            #         new_threat_points = threat_points.copy()
            # else:
            #     new_threat_points = None
            #Play the player's move
            self.set_color(new_board, play_coords[x][0], play_coords[x][1], player)

            # if threat_lst != None:
            #     new_threat_points['gain'].append((play_coords[x][0], play_coords[x][1]))

            cost_coords = self.plays_to_coords(self.cost[name][x], i, j, xdir, ydir)
            #Play all the opponent's possible counter moves
            # new_threat_points['cost'].append([])
            for cost in cost_coords:
                self.set_color(new_board, cost[0], cost[1], op)
                # if threat_lst != None:
                #     new_threat_points['cost'][-1].append((cost[0], cost[1]))

            # if threat_lst != None:
            #     threat_lst.append(new_threat_points)
            #Check if there's a winning threat sequence from this played position


            returned = self.threat_spot_check(new_board, player, play_coords[x][0], play_coords[x][1])
            #If there is a winning threat sequence return the coordinates of the play made
            if returned[0] != None:
                return play_coords[x], 3
        return None, 3

    #Wrapper function to check if there's a threat
    def start_threat_sequence(self, board, player, i, j, xdir, ydir, threat_lst):
        name = self.is_threat(board, player, i, j, xdir, ydir)
        if len(name) > 0:
            self.threat_num += 1
            return self.threat_sequence(board, player, i, j, xdir, ydir, name[0], is_immediate=True) #, threat_lst
        return None, 3

    def pop(self, board):
        self.set_color(board, 1, 1, 1)
        self.set_color(board, 1, 2, 1)
        self.set_color(board, 1, 3, 1)
        self.set_color(board, 2, 6, 1)
        self.set_color(board, 3, 7, 1)
        self.set_color(board, 3, 9, 2)
        self.set_color(board, 6, 9, 1)
        self.set_color(board, 6, 10, 2)
        self.set_color(board, 7, 9, 1)
        self.set_color(board, 10 , 9, 1)

    #print the names of all of the threats on the board; debugging function
    def print_threats(self, board, player):
        n = []
        n += self.is_threat(board, player, 0, 0, 1, 1)
        n += self.is_threat(board, player, board.size + 1, 0, -1, 1)
        for i in range(1, board.size + 1):
            n += self.is_threat(board, player, i, 0, 1, 1)
            n += self.is_threat(board, player, i, 0, 0, 1)
            n += self.is_threat(board, player, i, 0, -1, 1)
        for j in range(1, board.size + 1):
            n += self.is_threat(board, player, 0, j, 1, 0)
            n += self.is_threat(board, player, board.size + 1, j, -1, 1)
            n += self.is_threat(board, player, 0, j, 1, 1)
        for i in range(1, board.size + 1):
            for j in range(1, board.size + 1):
                n += self.is_threat(board, player, i, j, 1, 0)
                n += self.is_threat(board, player, i, j, 1, 1)
                n += self.is_threat(board, player, i, j, 0, 1)
                n += self.is_threat(board, player, i, j, -1, 1)
        print(n)


    def threat_search(self, board, player, recurse=True):
        self.threat_num = 0
        #c contains the coordinates of any play that makes a winning threat sequence
        c = []

        #Only append to c if there are coordinates
        def non_none(c, x):
            if x[0] != None:
                c.append(x)

        #List of threats to possibly combine
        threat_lst = []

        #Check all the possible lines of the board for threats
        non_none(c, self.start_threat_sequence(board, player, 0, 0, 1, 1, threat_lst))
        non_none(c, self.start_threat_sequence(board, player, board.size + 1, 0, -1, 1, threat_lst))
        for i in range(1, board.size + 1):
            non_none(c, self.start_threat_sequence(board, player, i, 0, 1, 1, threat_lst))
            non_none(c, self.start_threat_sequence(board, player, i, 0, 0, 1, threat_lst))
            non_none(c, self.start_threat_sequence(board, player, i, 0, -1, 1, threat_lst))
        for j in range(1, board.size + 1):
            non_none(c, self.start_threat_sequence(board, player, 0, j, 1, 0, threat_lst))
            non_none(c, self.start_threat_sequence(board, player, 0, j, 1, 1, threat_lst))
            non_none(c, self.start_threat_sequence(board, player, board.size + 1, j, -1, 1, threat_lst))
        for i in range(1, board.size + 1):
            for j in range(1, board.size + 1):
                non_none(c, self.start_threat_sequence(board, player, i, j, 1, 0, threat_lst))
                non_none(c, self.start_threat_sequence(board, player, i, j, 1, 1, threat_lst))
                non_none(c, self.start_threat_sequence(board, player, i, j, 0, 1, threat_lst))
                non_none(c, self.start_threat_sequence(board, player, i, j, -1, 1, threat_lst))


        if len(c) > 0:
            for x in range(len(c)):
                if c[x][1] == 1:
                    return board.pt(c[x][0][0], c[x][0][1]), c[x][1]
            for x in range(len(c)):
                if c[x][1] == 2:
                    return board.pt(c[x][0][0], c[x][0][1]), c[x][1]
            return board.pt(c[0][0][0], c[x][0][1]), c[0][1]


        # print("LST", threat_lst)
        # print(recurse)
        # if recurse:
        #     conflicting_threats = []
        #     checked_threats = []
        #     while True:
        #         new_board = board.copy()
        #         new_conflicting_threats = []
        #         for threat in conflicting_threats:
        #             conflicting = False
        #             for x in range(len(threat['gain'])):
        #                 if self.get_color(new_board, threat['gain'][x][0], threat['gain'][x][1]) != 0:
        #                     conflicting = True
        #                     break
        #                 for y in threat['cost'][x]:
        #                     if self.get_color(new_board, y[0], y[1]) != 0:
        #                         conflicting = True
        #                         break
        #                 if conflicting:
        #                     break
        #             if conflicting:
        #                 if threat not in checked_threats:
        #                     checked_threats.append(threat)
        #                     new_conflicting_threats.append(threat)
        #             else:
        #                 for x in range(len(threat['gain'])):
        #                     self.set_color(new_board, threat['gain'][x][0], threat['gain'][x][1], player)
        #                     for y in threat['cost'][x]:
        #                         self.set_color(new_board, y[0], y[1], opponent(player))
        #
        #         for threat in threat_lst:
        #             conflicting = False
        #             for x in range(len(threat['gain'])):
        #                 if self.get_color(new_board, threat['gain'][x][0], threat['gain'][x][1]) != 0:
        #                     conflicting = True
        #                     break
        #                 for y in threat['cost'][x]:
        #                     if self.get_color(new_board, y[0], y[1]) != 0:
        #                         conflicting = True
        #                         break
        #                 if conflicting:
        #                     break
        #             if conflicting:
        #                 if threat not in checked_threats:
        #                     checked_threats.append(threat)
        #                     new_conflicting_threats.append(threat)
        #             else:
        #                 for x in range(len(threat['gain'])):
        #                     self.set_color(new_board, threat['gain'][x][0], threat['gain'][x][1], player)
        #                     for y in threat['cost'][x]:
        #                         self.set_color(new_board, y[0], y[1], opponent(player))
        #
        #         returned = self.threat_search(new_board, player, False)
        #         if returned != None:
        #             return returned
        #
        #         if len(new_conflicting_threats) == 0:
        #             break
        #         conflicting_threats = new_conflicting_threats

        return None, False
