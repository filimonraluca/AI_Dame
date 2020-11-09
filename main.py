from termcolor import colored


class Game:
    def __init__(self, turn):
        self.human_poz = [(3, 0), (3, 1), (3, 2), (3, 3)]
        self.ai_poz = [(0, 0), (0, 1), (0, 2), (0, 3)]
        self.turn = turn
        self.game_over = False
        self.depth = 2

    def is_final(self):
        h_result = len(list(filter(lambda e: e[0] == 0, self.human_poz)))
        ai_result = len(list(filter(lambda e: e[0] == 3, self.ai_poz)))
        if self.game_over == True:
            if h_result == ai_result:
                print("Nobody wins")
                return -1
            elif h_result > ai_result:
                print("Human wins! :)")
                return 2
            else:
                print("AI wins! :(")
                return 1
        if h_result == 4:
            print("Human wins! :)")
            return 2
        if ai_result == 4:
            print("AI wins! :(")
            return 1
        return 0

    def is_valid(self, l, c):
        if 0 <= l < 4 and 0 <= c < 4 and (l, c) not in self.ai_poz and (l, c) not in self.human_poz:
            return True
        return False

    def is_human_piece(self, l, c):
        if 0 <= l < 4 and 0 <= c < 4 and (l, c) in self.human_poz:
            return True
        return False

    def is_logical_move(self, oldl, oldc, l, c):
        if (abs(oldl - l) + abs(oldc - c) == 1) or (abs(oldl - l) == 1 and abs(oldc - c) == 1):
            return True
        return False

    def euristic_function(self, ai_poz):
        f = 0
        for piece in ai_poz:
            f += piece[0]
        for piece in self.human_poz:
            f -= 3 - piece[0]
        return f

    def make_ai_move(self, oldl, oldc, l, c):
        self.ai_poz[self.ai_poz.index((oldl, oldc))] = (l, c)

    def make_human_move(self, oldl, oldc, l, c):
        self.human_poz[self.human_poz.index((oldl, oldc))] = (l, c)

    def actiuni(self, current_ai_poz):
        valid_moves = []
        l = [-1, -1, -1, 0, 0, 1, 1, 1]
        c = [-1, 0, 1, -1, 1, -1, 0, 1]
        for piece in current_ai_poz:
            for i in range(0, 8):
                if self.is_valid(piece[0] + l[i], piece[1] + c[i]):
                    valid_moves.append((piece[0], piece[1], piece[0] + l[i], piece[1] + c[i]))
        return valid_moves

    def valid_moves_for_human(self):
        valid_moves = 0
        l = [-1, -1, -1, 0, 0, 1, 1, 1]
        c = [-1, 0, 1, -1, 1, -1, 0, 1]
        for piece in self.human_poz:
            for i in range(0, 8):
                if self.is_valid(piece[0] + l[i], piece[1] + c[i]):
                    valid_moves += 1
        if valid_moves == 0:
            return False
        return True

    '''
    #Euristic function
    
    def next_move(self):
        mx = -10
        best_move = None
        if self.turn == 1:
            valid_moves = self.actiuni(self.ai_poz)
            print(valid_moves)
            for move in valid_moves:
                copy_ai_poz = self.ai_poz.copy()
                copy_ai_poz[copy_ai_poz.index((move[0], move[1]))] = (move[2], move[3])
                eval_result = self.euristic_function(copy_ai_poz)
                if eval_result > mx:
                    mx = eval_result
                    best_move = move
            if not valid_moves:
                self.game_over = True
            else:
                self.make_ai_move(best_move[0], best_move[1], best_move[2], best_move[3])
                self.turn = 2
        elif self.turn == 2:
            if not self.valid_moves_for_human():
                self.game_over = True
            else:
                x, y = map(int, input("Enter x and y for piece you want to move:").split())
                while not self.is_human_piece(x, y):
                    x, y = map(int, input("Enter VALID x and y for piece you want to move:").split())
                next_x, next_y = map(int, input("Enter x and y for new position:").split())
                while not self.is_valid(next_x, next_y):
                    next_x, next_y = map(int, input("Enter VALID x and y for new position:").split())
                while not self.is_logical_move(x, y, next_x, next_y):
                    print("The move you want to make is forbidden! (too far)")
                    x, y = map(int, input("Enter x and y for piece you want to move:").split())
                    while not self.is_human_piece(x, y):
                        x, y = map(int, input("Enter VALID x and y for piece you want to move:").split())
                    next_x, next_y = map(int, input("Enter x and y for new position:").split())
                    while not self.is_valid(next_x, next_y):
                        next_x, next_y = map(int, input("Enter VALID x and y for new position:").split())
                self.make_human_move(x, y, next_x, next_y)
                self.turn = 1
    '''

    '''
    #MIN MAX
    def min_max(self, current_ai_poz, maximazing_player, current_depth):
        if current_depth == 0:
            return None, self.euristic_function(current_ai_poz)
        if maximazing_player:
            maxEval = -10
            bestMove = None
            valid_moves = self.actiuni(current_ai_poz)
            for move in valid_moves:
                copy_ai_poz = current_ai_poz.copy()
                copy_ai_poz[copy_ai_poz.index((move[0], move[1]))] = (move[2], move[3])
                x, eval = self.min_max(copy_ai_poz, False, current_depth - 1)
                if eval > maxEval:
                    maxEval = eval
                    bestMove = move
            print("Maximizant:", bestMove, maxEval)
            return bestMove, maxEval
        else:
            minEval = 10
            bestMove = None
            valid_moves = self.actiuni(current_ai_poz)
            for move in valid_moves:
                copy_ai_poz = current_ai_poz.copy()
                copy_ai_poz[copy_ai_poz.index((move[0], move[1]))] = (move[2], move[3])
                x, eval = self.min_max(copy_ai_poz, True, current_depth - 1)
                if eval < minEval:
                    minEval = eval
                    bestMove = move
            print("Minimizant:", bestMove, minEval)
            return bestMove, minEval
    
    def next_move_min_max(self):
        mx = -10
        best_move = None
        if self.turn == 1:
            best_move, eval = self.min_max(self.ai_poz, True, 2)
            if not best_move:
                self.game_over = True
            self.make_ai_move(best_move[0], best_move[1], best_move[2], best_move[3])
            self.turn = 2
    
        elif self.turn == 2:
            if not self.valid_moves_for_human():
                self.game_over = True
            else:
                x, y = map(int, input("Enter x and y for piece you want to move:").split())
                while not self.is_human_piece(x, y):
                    x, y = map(int, input("Enter VALID x and y for piece you want to move:").split())
                next_x, next_y = map(int, input("Enter x and y for new position:").split())
                while not self.is_valid(next_x, next_y):
                    next_x, next_y = map(int, input("Enter VALID x and y for new position:").split())
                while not self.is_logical_move(x, y, next_x, next_y):
                    print("The move you want to make is forbidden! (too far)")
                    x, y = map(int, input("Enter x and y for piece you want to move:").split())
                    while not self.is_human_piece(x, y):
                        x, y = map(int, input("Enter VALID x and y for piece you want to move:").split())
                    next_x, next_y = map(int, input("Enter x and y for new position:").split())
                    while not self.is_valid(next_x, next_y):
                        next_x, next_y = map(int, input("Enter VALID x and y for new position:").split())
                self.make_human_move(x, y, next_x, next_y)
                self.turn = 1
    '''

    def alpha_beta(self, current_ai_poz, alpha, beta, maximazing_player, current_depth):
        if current_depth == 0:
            return None, self.euristic_function(current_ai_poz)
        if maximazing_player:
            maxEval = -10
            bestMove = None
            valid_moves = self.actiuni(current_ai_poz)
            for move in valid_moves:
                copy_ai_poz = current_ai_poz.copy()
                copy_ai_poz[copy_ai_poz.index((move[0], move[1]))] = (move[2], move[3])
                x, eval = self.alpha_beta(copy_ai_poz, alpha, beta, False, current_depth - 1)
                if eval > maxEval:
                    maxEval = eval
                    bestMove = move
                if maxEval >= beta:
                    #print("BREAK")
                    return bestMove, maxEval
                #print(alpha,maxEval)
                alpha = max(alpha, maxEval)
            # print("Maximizant:", bestMove, maxEval, alpha, beta)
            return bestMove, maxEval
        else:
            minEval = 10
            bestMove = None
            valid_moves = self.actiuni(current_ai_poz)
            for move in valid_moves:
                copy_ai_poz = current_ai_poz.copy()
                copy_ai_poz[copy_ai_poz.index((move[0], move[1]))] = (move[2], move[3])
                x, eval = self.alpha_beta(copy_ai_poz, alpha, beta, True, current_depth - 1)
                if eval < minEval:
                    minEval = eval
                    bestMove = move
                #print(alpha,minEval)
                if alpha >= minEval:
                    #print("BREAK MIN", alpha, minEval)
                    return bestMove, minEval
                beta = min(beta, minEval)
            # print("Minimizant:", bestMove, minEval, alpha, beta)
            return bestMove, minEval

    def next_move_alpha_beta(self):
        mx = -10
        best_move = None
        if self.turn == 1:
            best_move, eval = self.alpha_beta(self.ai_poz, -10, 10, True, 2)
            if not best_move:
                self.game_over = True
            self.make_ai_move(best_move[0], best_move[1], best_move[2], best_move[3])
            self.turn = 2

        elif self.turn == 2:
            if not self.valid_moves_for_human():
                self.game_over = True
            else:
                x, y = map(int, input("Enter x and y for piece you want to move:").split())
                while not self.is_human_piece(x, y):
                    x, y = map(int, input("Enter VALID x and y for piece you want to move:").split())
                next_x, next_y = map(int, input("Enter x and y for new position:").split())
                while not self.is_valid(next_x, next_y):
                    next_x, next_y = map(int, input("Enter VALID x and y for new position:").split())
                while not self.is_logical_move(x, y, next_x, next_y):
                    print("The move you want to make is forbidden! (too far)")
                    x, y = map(int, input("Enter x and y for piece you want to move:").split())
                    while not self.is_human_piece(x, y):
                        x, y = map(int, input("Enter VALID x and y for piece you want to move:").split())
                    next_x, next_y = map(int, input("Enter x and y for new position:").split())
                    while not self.is_valid(next_x, next_y):
                        next_x, next_y = map(int, input("Enter VALID x and y for new position:").split())
                self.make_human_move(x, y, next_x, next_y)
                self.turn = 1

    def print_board(self):
        print("Starea curenta:")
        for i in range(0, 4):
            for j in range(0, 4):
                if (i, j) in self.human_poz:
                    print(colored('H', 'green'), end=' ')
                elif (i, j) in self.ai_poz:
                    print(colored('C', 'red'), end=' ')
                else:
                    print(colored(0, 'grey'), end=' ')
            print()


if __name__ == '__main__':
    game = None
    turn = input("Who starts? (H or C)\n")
    if turn == "H":
        game = Game(2)
    else:
        game = Game(1)
    print("Initial board:")
    game.print_board()
    while not game.is_final():
        # game.next_move()
        # game.next_move_min_max()
        game.next_move_alpha_beta()
        game.print_board()
