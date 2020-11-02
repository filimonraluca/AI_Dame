from termcolor import colored

class Game:
    def __init__(self):
        self.board = [[1, 1, 1, 1],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [2, 2, 2, 2]]
        self.human_poz = [(3, 0), (3, 1), (3, 2), (3, 3)]
        self.ai_poz = [(0, 0), (0, 1), (0, 2), (0, 3)]
        self.turn = 2

    def is_final(self):
        if self.board[0] == [2, 2, 2, 2]:
            print("Human wins! :)")
            return 2
        if self.board[3] == [1, 1, 1, 1]:
            print("AI wins! :(")
            return 1
        return 0

    def is_valid(self, l, c):
        if 0 <= l < 4 and 0 <= c < 4 and self.board[l][c] == 0:
            return True
        return False

    def is_human_piece(self, l, c):
        if 0 <= l < 4 and 0 <= c < 4 and self.board[l][c] == 2:
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
        self.board[oldl][oldc] = 0
        self.ai_poz[self.ai_poz.index((oldl, oldc))] = (l, c)
        self.board[l][c] = 1

    def make_human_move(self, oldl, oldc, l, c):
        self.board[oldl][oldc] = 0
        self.human_poz[self.human_poz.index((oldl, oldc))] = (l, c)
        self.board[l][c] = 2

    def next_move(self):
        l = [-1, -1, -1, 0, 0, 1, 1, 1]
        c = [-1, 0, 1, -1, 1, -1, 0, 1]
        mx = -10
        best_move = None
        if self.turn == 1:
            for piece in self.ai_poz:
                for i in range(0, 8):
                    if self.is_valid(piece[0] + l[i], piece[1] + c[i]):
                        eval_result = self.euristic_function(piece, piece[0] + l[i], piece[1] + c[i])
                        if eval_result > mx:
                            mx = eval_result
                            best_move = (piece[0], piece[1], piece[0] + l[i], piece[1] + c[i])
            self.make_ai_move(best_move[0], best_move[1], best_move[2], best_move[3])
            self.turn = 2
        elif self.turn == 2:
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
        for l in self.board:
            for c in l:
                if c==1: print (colored(c, 'red'),end=' ')
                elif c == 2: print(colored(c, 'green'),end=' ')
                else: print(colored(c, 'grey'),end=' ')
            print()



if __name__ == '__main__':
    game = Game()
    print("Initial board:")
    game.print_board()
    while not game.is_final():
        game.next_move()
        game.print_board()
