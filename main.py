from termcolor import colored


class Game:
    def __init__(self):
        self.human_poz = [(3, 0), (3, 1), (3, 2), (3, 3)]
        self.ai_poz = [(0, 0), (0, 1), (0, 2), (0, 3)]
        self.turn = 2
        self.game_over = False

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

    def euristic_function(self, oldpiece, l, c):
        f = 0
        copy_ai_poz = self.ai_poz.copy()
        copy_ai_poz[copy_ai_poz.index(oldpiece)] = (l, c)
        for piece in copy_ai_poz:
            f += piece[0]
        for piece in self.human_poz:
            f -= 3 - piece[0]
        return f

    def make_ai_move(self, oldl, oldc, l, c):
        self.ai_poz[self.ai_poz.index((oldl, oldc))] = (l, c)

    def make_human_move(self, oldl, oldc, l, c):
        self.human_poz[self.human_poz.index((oldl, oldc))] = (l, c)

    def next_move(self):
        l = [-1, -1, -1, 0, 0, 1, 1, 1]
        c = [-1, 0, 1, -1, 1, -1, 0, 1]
        mx = -10
        best_move = None
        valid_moves = 0
        if self.turn == 1:
            for piece in self.ai_poz:
                for i in range(0, 8):
                    if self.is_valid(piece[0] + l[i], piece[1] + c[i]):
                        valid_moves += 1
                        eval_result = self.euristic_function(piece, piece[0] + l[i], piece[1] + c[i])
                        if eval_result > mx:
                            mx = eval_result
                            best_move = (piece[0], piece[1], piece[0] + l[i], piece[1] + c[i])
            if valid_moves == 0:
                self.game_over = True
            else:
                self.make_ai_move(best_move[0], best_move[1], best_move[2], best_move[3])
                self.turn = 2
        elif self.turn == 2:
            for piece in self.human_poz:
                for i in range(0, 8):
                    if self.is_valid(piece[0] + l[i], piece[1] + c[i]):
                        valid_moves += 1
            if valid_moves == 0:
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
    game = Game()
    print("Initial board:")
    game.print_board()
    while not game.is_final():
        game.next_move()
        game.print_board()
