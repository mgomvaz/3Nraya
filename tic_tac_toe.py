class TicTacToe:
    def __init__(self):
        self.board = [' '] * 9
        self.current_player = 'X'

    def print_board(self):
        for i in range(0, 9, 3):
            print(self.board[i], '|', self.board[i + 1], '|', self.board[i + 2])
            if i < 6:
                print('---------')

    def make_move(self, position):
        if self.board[position] == ' ':
            self.board[position] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        else:
            print("Invalid move. Try again.")
            return False

    def check_winner(self):
        # Check rows, columns, and diagonals for a win
        
        win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6)]
        for condition in win_conditions:
            a, b, c = condition
            if self.board[a] == self.board[b] == self.board[c] != ' ':
                return self.board[a]
        return None

    def play_game(self):
        while True:
            self.print_board()
            move = int(input(f"Player {self.current_player}, enter your move (0-8): "))
            if 0 <= move < 9:
                if self.make_move(move):
                    winner = self.check_winner()
                    if winner:
                        self.print_board()
                        print(f"Player {winner} wins!")
                        break
            else:
                print("Invalid input. Please enter a number between 0 and 8.")


if __name__ == "__main__":
    game = TicTacToe()
    game.play_game()
