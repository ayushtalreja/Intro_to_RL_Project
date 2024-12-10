import tkinter as tk
import numpy as np
from checkers_env import checkers_env
from LearningAgent import LearningAgent

class CheckersGUI:
    def __init__(self, master, mode='human_vs_computer'):
        self.master = master
        self.master.title("Checkers RL")
        
        self.env = checkers_env()
        self.mode = mode
        
        # If computer vs computer, initialize learning agents
        if mode == 'computer_vs_computer':
            self.agent_1 = LearningAgent(step_size=0.1, epsilon=0.1, env=self.env)
            self.agent_2 = LearningAgent(step_size=0.1, epsilon=0.1, env=self.env)
        
        self.create_board()
    
    def create_board(self):
        self.squares = []
        for row in range(6):
            row_squares = []
            for col in range(6):
                square = tk.Button(self.master, width=5, height=2,
                                   command=lambda r=row, c=col: self.square_clicked(r, c))
                square.grid(row=row, column=col)
                row_squares.append(square)
            self.squares.append(row_squares)
        
        self.update_board()
    
    def update_board(self):
        for row in range(6):
            for col in range(6):
                piece = self.env.board[row][col]
                color = 'white'
                text = ' '
                
                if piece == 1:
                    color = 'blue'
                    text = 'O'
                elif piece == -1:
                    color = 'red'
                    text = 'X'
                
                self.squares[row][col].configure(
                    bg=color, text=text, 
                    state='normal' if piece * self.env.player > 0 else 'disabled'
                )
    
    def square_clicked(self, row, col):
        # Human player move logic here
        pass
    
    def computer_move(self):
        # Computer move logic here based on mode
        pass

def main():
    root = tk.Tk()
    game = CheckersGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()