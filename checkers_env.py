
import numpy as np


class checkers_env:

    def __init__(self, board=None, player=None):

        self.board = self.initialize_board()
        self.player = 1


    def initialize_board(self):
        board = np.array([[1, 0, 1, 0, 1, 0],
                      [0, 1, 0, 1, 0, 1],
                      [0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0],
                      [-1, 0, -1, 0, -1, 0],
                      [0, -1, 0, -1, 0, -1]])
        return board


    def reset(self):
        self.board = np.array([[1, 0, 1, 0, 1, 0],
                      [0, 1, 0, 1, 0, 1],
                      [0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0],
                      [-1, 0, -1, 0, -1, 0],
                      [0, -1, 0, -1, 0, -1]])
        self.player = 1

    def valid_moves(self, player):
        """
        Generate valid moves for a given player. 
        Returns list of possible actions: [start_row, start_col, end_row, end_col]
        """
        valid_actions = []
        board = self.board
        directions = [(1, -1), (1, 1)] if player == 1 else [(-1, -1), (-1, 1)]
        
        for row in range(6):
            for col in range(6):
                if board[row][col] == player:
                    # Check regular moves
                    for dx, dy in directions:
                        new_row, new_col = row + dx, col + dy
                        if 0 <= new_row < 6 and 0 <= new_col < 6:
                            if board[new_row][new_col] == 0:
                                valid_actions.append([row, col, new_row, new_col])
                    
                    # Check capture moves
                    for dx, dy in directions:
                        jump_row, jump_col = row + 2*dx, col + 2*dy
                        mid_row, mid_col = row + dx, col + dy
                        
                        if (0 <= jump_row < 6 and 0 <= jump_col < 6 and
                            board[mid_row][mid_col] == -player and 
                            board[jump_row][jump_col] == 0):
                            valid_actions.append([row, col, jump_row, jump_col])
        
        return valid_actions    

    def capture_piece(self, action):
        """
        Remove captured piece from the board and assign 0 to the positions of captured pieces.
        """
        start_row, start_col, end_row, end_col = action
        
        # Check if it's a capture move (jumped over a piece)
        if abs(start_row - end_row) == 2:
            mid_row = (start_row + end_row) // 2
            mid_col = (start_col + end_col) // 2
            self.board[mid_row][mid_col] = 0
        
    def game_winner(self, board):
        """
        Determine game winner
        Returns: 1 (player 1 wins), -1 (player -1 wins), 0 (game continues)
        """
        player1_pieces = np.sum(board > 0)
        player2_pieces = np.sum(board < 0)
        
        # Check if either player has no pieces
        if player1_pieces == 0:
            return -1
        if player2_pieces == 0:
            return 1
        
        # Check if either player has no valid moves
        p1_moves = self.valid_moves(1)
        p2_moves = self.valid_moves(-1)
        
        if len(p1_moves) == 0:
            return -1
        if len(p2_moves) == 0:
            return 1
        
        return 0


    def step(self, action, player):
        '''
        The transition of board and incurred reward after player performs an action. Be careful about King
        '''

        return [self.board, reward]

    
    def render(self):
        for row in self.board:
            for square in row:
                if square == 1:
                    piece = "|0"
                elif square == -1:
                    piece = "|X"
                elif square == 2:
                    piece = "|K"
                else:
                    piece = "| "
                print(piece, end='')
            print("|")