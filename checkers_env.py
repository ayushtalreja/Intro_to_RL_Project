
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
        The transition of board and incurred reward after player performs an action.
        
        :param action: List [start_row, start_col, end_row, end_col] representing the move
        :param player: Current player (1 or -1)
        :return: [next_board, reward]
        '''
        start_row, start_col, end_row, end_col = action
        
        # Validate the move
        valid_moves = self.valid_moves(player)
        if action not in valid_moves:
            raise ValueError(f"Invalid move {action} for player {player}")
        
        # Capture piece if it's a jump move
        self.capture_piece(action)
        
        # Move the piece
        self.board[end_row][end_col] = self.board[start_row][start_col]
        self.board[start_row][start_col] = 0
        
        # Promote piece to king if it reaches opposite end
        self.board = self.promote_to_king(self.board, end_row, end_col)
        
        # Switch player
        self.player *= -1
        
        # Basic reward calculation (can be expanded)
        reward = 0
        
        # Reward for capturing a piece
        if abs(start_row - end_row) == 2:
            reward += 1  # Reward for capturing
        
        # Reward for moving forward
        if player == 1 and end_row > start_row:
            reward += 0.5
        elif player == -1 and end_row < start_row:
            reward += 0.5
        
        # Check game winner for additional rewards/penalties
        winner = self.game_winner(self.board)
        if winner == player:
            reward += 10
        elif winner == -player:
            reward -= 10
        
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

    @staticmethod
    def promote_to_king(board, row, col):
        """
        Promote piece to king if it reaches opposite end
        """
        if board[row][col] == 1 and row == 5:  # Player 1 king
            board[row][col] = 2
        elif board[row][col] == -1 and row == 0:  # Player -1 king
            board[row][col] = -2
        return board
    
    @staticmethod
    def king_valid_moves(board, row, col):
        """
        Generate valid moves for king pieces (can move in all directions)
        """
        valid_moves = []
        player = board[row][col]
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dx, dy in directions:
            new_row, new_col = row + dx, col + dy
            
            # Check simple move
            if 0 <= new_row < 6 and 0 <= new_col < 6 and board[new_row][new_col] == 0:
                valid_moves.append([row, col, new_row, new_col])
            
            # Check capture move
            jump_row, jump_col = row + 2*dx, col + 2*dy
            mid_row, mid_col = row + dx, col + dy
            
            if (0 <= jump_row < 6 and 0 <= jump_col < 6 and
                board[mid_row][mid_col] * player < 0 and 
                board[jump_row][jump_col] == 0):
                valid_moves.append([row, col, jump_row, jump_col])
        
        return valid_moves