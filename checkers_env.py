
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
        Generate valid moves for a given player including king moves. 
        Returns list of possible actions: [start_row, start_col, end_row, end_col]
        """
        valid_actions = []
        board = self.board
        
        for row in range(6):
            for col in range(6):
                piece = board[row][col]
                
                # Skip empty squares or opponent pieces
                if piece == 0 or (piece * player) < 0:
                    continue
                
                # Handle regular pieces
                if abs(piece) == 1:
                    directions = [(1, -1), (1, 1)] if player == 1 else [(-1, -1), (-1, 1)]
                    valid_actions.extend(self._get_piece_moves(row, col, directions))
                
                # Handle king pieces
                elif abs(piece) == 2:
                    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
                    valid_actions.extend(self._get_piece_moves(row, col, directions))
        
        return valid_actions

    def _get_piece_moves(self, row, col, directions):
        """
        Helper method to get valid moves for a piece in given directions
        """
        valid_actions = []
        player = 1 if self.board[row][col] > 0 else -1
        
        for dx, dy in directions:
            # Check regular moves
            new_row, new_col = row + dx, col + dy
            if 0 <= new_row < 6 and 0 <= new_col < 6:
                if self.board[new_row][new_col] == 0:
                    valid_actions.append([row, col, new_row, new_col])
            
            # Check capture moves
            jump_row, jump_col = row + 2*dx, col + 2*dy
            mid_row, mid_col = row + dx, col + dy
            
            if (0 <= jump_row < 6 and 0 <= jump_col < 6 and
                self.board[mid_row][mid_col] * player < 0 and 
                self.board[jump_row][jump_col] == 0):
                valid_actions.append([row, col, jump_row, jump_col])
        
        return valid_actions
    
    def _calculate_reward(self, action, player, piece_type):
        """
        Helper method to calculate rewards for moves
        """
        start_row, start_col, end_row, end_col = action
        reward = 0
        
        # Reward for capturing
        if abs(start_row - end_row) == 2:
            reward += 1
        
        # Reward for moving forward (regular pieces)
        if abs(piece_type) == 1:
            if player == 1 and end_row > start_row:
                reward += 0.5
            elif player == -1 and end_row < start_row:
                reward += 0.5
        
        # Extra reward for king moves
        if abs(piece_type) == 2:
            reward += 0.2  # Small bonus for using kings
        
        # Check if piece was promoted to king
        if abs(self.board[end_row][end_col]) == 2 and abs(piece_type) == 1:
            reward += 2  # Bonus for getting a king
        
        # Game outcome rewards
        winner = self.game_winner(self.board)
        if winner == player:
            reward += 10
        elif winner == -player:
            reward -= 10
        
        return reward

    def promote_to_king(self, board, row, col):
        """
        Promote piece to king if it reaches opposite end
        Preserves the sign of the piece (player)
        """
        piece = board[row][col]
        if piece == 1 and row == 5:  # Player 1 king
            board[row][col] = 2
        elif piece == -1 and row == 0:  # Player -1 king
            board[row][col] = -2
        return board

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
        
        # Store piece type before move
        piece_type = self.board[start_row][start_col]
        
        # Capture piece if it's a jump move
        self.capture_piece(action)
        
        # Move the piece
        self.board[end_row][end_col] = piece_type
        self.board[start_row][start_col] = 0
        
        # Promote piece to king if it reaches opposite end
        self.board = self.promote_to_king(self.board, end_row, end_col)
        
        # Switch player
        self.player *= -1
        
        # Calculate reward
        reward = self._calculate_reward(action, player, piece_type)
        
        return [self.board, reward]
        
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