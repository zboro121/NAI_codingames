from easyAI import TwoPlayersGame, Human_Player, AI_Player, Negamax, SSS

# Rules: https://en.wikipedia.org/wiki/Connect_Four
# Authors: Jakub Wirkus, Maciej Sochalski
# Game: Connect 4
# Preparation instruction: install pip (command: py -m pip install) and easyAI (command: py -m pip install easyAI)


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
        """
        List of possible moves
        :returns: list of columns where disc can be placed
        """
        return [col for col in range(self.columns) if (self.board[0][col]) == 0]

    def make_move(self, column):
        """
        Places disc at the lowest possible coordinate in a column
        :param column: column where disc can be placed
        """
        row = self.rows - 1
        while row >= 0:
            if self.board[row][int(column)] == 0:
                self.board[row][int(column)] = self.nplayer
                break
            row -= 1

    def win(self):
        """
        Win conditions
        :returns: true if player scores four discs in a row vertically, horizontally or diagonally
        """
        return self.find_4(self.nplayer)

    def find_4(self, player):
        """
        Finds 4 discs in a row vertically.
        :param player: value 1 for human player, value 2 for computer player
        :returns: true if player has 4 discs in a row vertically, horizontally or diagonally
        """
        return self.find_4_vertically(player) or self.find_4_horizontally(player) or self.find_4_diagonally(player)

    def find_4_vertically(self, player):
        """
        Finds 4 discs in a row vertically.
        :param player: value 1 for human player, value 2 for computer player
        :returns: true if player has 4 discs in a row vertically
        """
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
        """
        Finds 4 discs in a row horizontally.
        :param player: value 1 for human player, value 2 for computer player
        :returns: true if player has 4 discs in a row horizontally
        """
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
        """
        Finds 4 discs in a row diagonally.
        :param player: value 1 for human player, value 2 for computer player
        :returns: true if player has 4 discs in a row diagonally
        """
        return self.find_4_diagonally_plus(player) or self.find_4_diagonally_minus(player)

    def find_4_diagonally_plus(self, player):
        """
        Finds 4 discs in a row diagonally starting from column 0. Uses predefined coordinates to start search
        :param player: value 1 for human player, value 2 for computer player
        :returns: true if player has 4 discs in a row diagonally
        """
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

    def find_4_diagonally_minus(self, player):
        """
        Finds 4 discs in a row diagonally starting from column 6. Uses predefined coordinates to start search
        :param player: value 1 for human player, value 2 for computer player
        :returns: true if player has 4 discs in a row diagonally
        """
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
        """
        Draw conditions
        :returns: true if list of possible moves is empty
        """
        return self.possible_moves() == []

    def is_over(self):
        """
        Game is over when somebody wins or draws
        """
        return self.win() or self.draw()  # Game stops when someone wins or draws.

    def show(self):
        print('board:')
        print('0  1  2  3  4  5  6 - indexes\n')
        for row in range(self.rows):
            for column in range(self.columns):
                print(self.board[row][column], end="  ")
            print()

    def scoring(self):
        return 100 if self.win() else 0  # For the AI


if __name__ == '__main__':
    # Start a match (and store the history of moves when it ends)
    ai = Negamax(5)
    ai_algo_sss = SSS(5)
    # Human Player with AI Player
    game = Connect4([Human_Player(), AI_Player(ai)])
    # AI Player with AI Player
    # game = Connect4([AI_Player(ai_algo_sss), AI_Player(ai)])
    history = game.play()

    if game.win():
        print('Player ', game.nplayer, ' wins')
    else:
        print("Draw")
