from easyAI import TwoPlayersGame, Human_Player, AI_Player, Negamax, SSS

# Authors: Jakub Wirkus, Maciej Sochalski
# Game: Connect 4
# Rules: https://en.wikipedia.org/wiki/Connect_Four


class Connect4(TwoPlayersGame):
    """ In turn, the players place discs at the lowest possible point on the board.
    Player who scores 4 discs in a row horizontally, vertically or diagonally wins"""

    def __init__(self, players):
        self.players = players
        self.columns, self.rows = 7, 6
        # board[row][col]
        self.board = [[0 for i in range(self.columns)] for j in range(self.rows)]
        self.nplayer = 1  # player 1 starts

    def possible_moves(self):
        return [col for col in range(self.columns) if (self.board[0][col]) == 0]

    def make_move(self, column):
        row = self.rows - 1
        while row >= 0:
            if self.board[row][int(column)] == 0:
                self.board[row][int(column)] = self.nplayer
                break
            row -= 1

    def win(self):
        return self.find_4(self.nplayer)

    def find_4(self, player):
        return self.find_4_vertically(player) or self.find_4_horizontally(player) or self.find_4_diagonally(player)

    def find_4_vertically(self, player):
        for column in range(self.columns):
            count = 0
            for row in range(self.rows):
                if self.board[row][column] == player:
                    count += 1
                    if count == 4:
                        return True
                else:
                    count = 0
        return False

    def find_4_horizontally(self, player):
        for row in range(self.rows):
            count = 0
            for column in range(self.columns):
                if self.board[row][column] == player:
                    count += 1
                    if count == 4:
                        return True
                else:
                    count = 0
        return False

    def find_4_diagonally(self, player):
        return self.find_4_diagonally_plus(player) or self.find_4_diagonally_minus(player)

    # search for four discs in a row in positive direction (from column 0 to 6)
    def find_4_diagonally_plus(self, player):
        start_pos = [[3, 0], [4, 0], [5, 0], [5, 1], [5, 2], [5, 3]]
        for i in start_pos:
            row = i[0]
            column = i[1]
            count = 0
            while row >= 0 and column <= 6:
                if self.board[row][column] == player:
                    count += 1
                    if count == 4:
                        return True
                else:
                    count = 0
                row -= 1
                column += 1
        return False

    # search for four discs in a row in negative direction (from column 6 to 0)
    def find_4_diagonally_minus(self, player):
        start_pos = [[3, 6], [4, 6], [5, 6], [5, 5], [5, 4], [5, 3]]
        for i in start_pos:
            row = i[0]
            column = i[1]
            count = 0
            while row >= 0 and column >= 0:
                if self.board[row][column] == player:
                    count += 1
                    if count == 4:
                        return True
                else:
                    count = 0
                row -= 1
                column -= 1
        return False

    def draw(self):
        return self.possible_moves() == []

    def is_over(self):
        return self.win() or self.draw()  # Game stops when someone wins or draws.

    def show(self):
        print('board:')
        for row in range(self.rows):
            for column in range(self.columns):
                print(self.board[row][column], end=" ")
            print()

    def scoring(self):
        return 100 if self.win() else 0  # For the AI


if __name__ == '__main__':
    # Start a match (and store the history of moves when it ends)
    ai = Negamax(5)
    ai_algo_sss = SSS(5)
    game = Connect4([Human_Player(), AI_Player(ai)])
    # game = Connect4([AI_Player(ai_algo_sss), AI_Player(ai)])
    history = game.play()

    if game.win():
        print('Player ', game.nplayer, ' wins')
    else:
        print("Draw")
