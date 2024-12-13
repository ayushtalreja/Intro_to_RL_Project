import tkinter as tk
import numpy as np
from checkers_env import checkers_env
from LearningAgent import LearningAgent

class CheckersGUI:
    def __init__(self, master, mode='human_vs_computer'):
        self.master = master
        self.master.title("Advanced Checkers RL")
        
        self.env = checkers_env()
        self.mode = mode
        self.selected_piece = None
        
        # Game state tracking
        self.game_over = False
        self.current_player = 1
        
        # Agents for computer modes
        if mode == 'computer_vs_computer':
            self.agent_1 = LearningAgent(env=self.env)
            self.agent_2 = LearningAgent(env=self.env)
        elif mode == 'human_vs_computer':
            self.computer_agent = LearningAgent(env=self.env)
        
        self.create_board()
        self.status_label = tk.Label(master, text="Player 1's Turn", font=('Arial', 12))
        self.status_label.grid(row=6, columnspan=6)
    
    def create_board(self):
        self.squares = []
        for row in range(6):
            row_squares = []
            for col in range(6):
                square = tk.Button(
                    self.master, width=5, height=2,
                    command=lambda r=row, c=col: self.square_clicked(r, c)
                )
                square.grid(row=row, column=col)
                row_squares.append(square)
            self.squares.append(row_squares)
        
        self.update_board()
    
    def update_board(self):
        for row in range(6):
            for col in range(6):
                piece = self.env.board[row][col]
                bg_color = 'light gray' if (row + col) % 2 == 0 else 'dark gray'
                text_color = 'blue' if piece > 0 else 'red'
                
                if piece == 1:
                    text = '🔵'
                elif piece == -1:
                    text = '🔴'
                else:
                    text = ''
                
                self.squares[row][col].configure(
                    text=text, 
                    fg=text_color, 
                    bg=bg_color,
                    state='normal'
                )
    
    def validate_move(self, start, end):
        """
        Check if move is valid according to game rules
        """
        valid_moves = self.env.valid_moves(self.current_player)
        proposed_move = [start[0], start[1], end[0], end[1]]
        return proposed_move in valid_moves
    
    def square_clicked(self, row, col):
        if self.game_over:
            return
        
        # Human player logic
        if self.selected_piece is None:
            # Select piece
            if self.env.board[row][col] == self.current_player:
                self.selected_piece = (row, col)
                self.squares[row][col].configure(bg='yellow')
        else:
            # Attempt move
            if self.validate_move(self.selected_piece, (row, col)):
                # Perform move
                move = [*self.selected_piece, row, col]
                self.env.step(move, self.current_player)
                
                # Switch players
                self.current_player *= -1
                self.selected_piece = None
                
                self.update_board()
                self.check_game_end()
            else:
                # Reset selection if invalid
                self.squares[self.selected_piece[0]][self.selected_piece[1]].configure(bg='light gray')
                self.selected_piece = None
    
    def check_game_end(self):
        """
        Check for game termination
        """
        winner = self.env.game_winner(self.env.board)
        if winner != 0:
            self.game_over = True
            message = f"Player {winner} wins!" if winner != 0 else "Draw"
            tk.Message("Game Over", message)

def main():
    root = tk.Tk()
    game = CheckersGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()