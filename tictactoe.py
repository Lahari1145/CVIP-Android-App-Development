import tkinter as tk
from tkinter import messagebox
import random

SIZE = 3

class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(SIZE)] for _ in range(SIZE)]
        self.current_player = 'X'

    def make_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            return True
        else:
            return False

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_winner(self):
        for i in range(SIZE):
            # Check rows
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return self.board[i][0]
            # Check columns
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                return self.board[0][i]

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]

        # Check for draw
        if all(self.board[i][j] != ' ' for i in range(SIZE) for j in range(SIZE)):
            return 'draw'

        # No winner yet
        return None

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.mode = None
        self.game = None
        self.buttons = []
        self.score_label = None  # Add a score_label attribute
        self.scores = {'X': 0, 'O': 0}
        self.create_menu()

    def create_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        menu_label = tk.Label(self.root, text='Select Game Mode:', font=('Arial', 14))
        menu_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        pvp_button = tk.Button(self.root, text='Player vs Player', font=('Arial', 12), command=self.start_pvp_game)
        pvp_button.grid(row=1, column=0, padx=10, pady=10)

        pve_button = tk.Button(self.root, text='Player vs Bot', font=('Arial', 12), command=self.start_pve_game)
        pve_button.grid(row=2, column=0, padx=10, pady=10)

    def back_to_menu(self):
        self.clear_game()
        self.create_menu()

    def create_board(self):
        for i in range(SIZE):
            row = []
            for j in range(SIZE):
                button = tk.Button(self.root, text='', width=10, height=5,
                                   command=lambda row=i, col=j: self.make_move(row, col))
                button.grid(row=i + 2, column=j, padx=5, pady=5)
                row.append(button)
            self.buttons.append(row)

        reset_button = tk.Button(self.root, text='Reset', font=('Arial', 12), command=self.reset_game)
        reset_button.grid(row=SIZE + 2, column=0, padx=10, pady=10)

        back_to_menu_button = tk.Button(self.root, text='Back to Menu', font=('Arial', 12), command=self.back_to_menu)
        back_to_menu_button.grid(row=SIZE + 2, column=1, padx=10, pady=10)

        self.game_mode_label = tk.Label(self.root, text=f'Game Mode: {self.mode}', font=('Arial', 12))
        self.game_mode_label.grid(row=0, column=0, columnspan=SIZE, padx=10, pady=10)

        # Create a label for both players' scores in the same row
        self.score_label = tk.Label(self.root, text=f'Scores: X= {self.scores["X"]}  O= {self.scores["O"]}', font=('Arial', 12))
        self.score_label.grid(row=1, column=0, columnspan=SIZE, padx=10, pady=10)

    def make_move(self, row, col):
        if self.game.make_move(row, col):
            self.buttons[row][col].configure(text=self.game.current_player)
            winner = self.game.check_winner()
            if winner:
                self.display_winner(winner)
            else:
                self.game.switch_player()
                if self.mode == 'Player vs Bot' and self.game.current_player == 'O':
                    self.bot_move()

    def bot_move(self):
        available_positions = []
        for i in range(SIZE):
            for j in range(SIZE):
                if self.game.board[i][j] == ' ':
                    available_positions.append((i, j))
        row, col = random.choice(available_positions)
        self.make_move(row, col)

    def display_winner(self, winner):
        if winner == 'draw':
            result = 'The game ended in a draw!'
        else:
            result = f'Player {winner} wins!'
            self.scores[winner] += 1  # Update the score for the winning player

        # Update the scores on the scoreboard
        self.update_scoreboard()

        play_again = messagebox.askyesno('Game Over', result + '\nDo you want to play again?')
        if play_again:
            self.reset_game()
        else:
            self.back_to_menu()

    def update_scoreboard(self):
        # Update the combined score label for both players
        self.score_label.config(text=f'X: {self.scores["X"]}  O: {self.scores["O"]}')

    def reset_game(self):
        for row in self.buttons:
            for button in row:
                button.configure(text='')
        self.game = TicTacToe()

    def start_pvp_game(self):
        self.mode = 'Player vs Player'
        self.clear_menu()
        self.game = TicTacToe()
        self.create_board()

    def start_pve_game(self):
        self.mode = 'Player vs Bot'
        self.clear_menu()
        self.game = TicTacToe()
        self.create_board()

        if self.game.current_player == 'O':
            self.bot_move()

    def clear_menu(self):
        for widget in self.root.winfo_children():
            widget.grid_forget()

    def clear_game(self):
        self.clear_board()
        self.mode = None
        self.game = None

    def clear_board(self):
        for row in self.buttons:
            for button in row:
                button.destroy()
        self.buttons = []

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Tic Tac Toe')

    gui = TicTacToeGUI(root)
    root.mainloop()
