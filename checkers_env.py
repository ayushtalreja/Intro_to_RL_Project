import numpy as np

class checkers_env:
    def __init__(self, board=None, player=None):
        self.board = self.initialize_board()
        self.player = 1
        self.moves_without_capture = 0
        self.moves_without_king = 0
        self.last_positions = []  # Store last 40 positions for draw detection

        # New dictionary to store multiple-jump paths
        # Key: tuple(action) -> (start_row, start_col, end_row, end_col)
        # Value: list of sub-jumps, e.g. [[sr, sc, mr, mc], [mr, mc, er, ec], ...]
        self.multijump_paths = {}

    def initialize_board(self):
        board = np.array([[ 1,  0,  1,  0,  1,  0],
                          [ 0,  1,  0,  1,  0,  1],
                          [ 0,  0,  0,  0,  0,  0],
                          [ 0,  0,  0,  0,  0,  0],
                          [-1,  0, -1,  0, -1,  0],
                          [ 0, -1,  0, -1,  0, -1]])
        return board

    def reset(self):
        self.board = np.array([[ 1,  0,  1,  0,  1,  0],
                               [ 0,  1,  0,  1,  0,  1],
                               [ 0,  0,  0,  0,  0,  0],
                               [ 0,  0,  0,  0,  0,  0],
                               [-1,  0, -1,  0, -1,  0],
                               [ 0, -1,  0, -1,  0, -1]])
        self.player = 1
        self.moves_without_capture = 0
        self.moves_without_king = 0
        self.last_positions = []
        self.multijump_paths.clear()

    def is_draw(self):
        """Check for draw conditions"""
        # Draw if no captures in last 40 moves
        if self.moves_without_capture >= 40:
            return True

        # Draw if no king promotion in last 40 moves
        if self.moves_without_king >= 40:
            return True

        return False

    def valid_moves(self, player):
        """
        Generate valid moves for a given player including king moves.
        Returns list of possible actions: [start_row, start_col, end_row, end_col]
        """
        valid_actions = []
        self.multijump_paths.clear()  # Clear from any previous move
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
        Enhanced helper method to get valid moves for a piece including multiple sequential jumps.
        Also stores full jump paths in self.multijump_paths for later capture.
        """
        valid_actions = []
        player = 1 if self.board[row][col] > 0 else -1

        def find_sequential_jumps(current_row, current_col, current_path=None, captured_positions=None):
            if current_path is None:
                current_path = []
            if captured_positions is None:
                captured_positions = set()

            found_jumps = []

            for dx, dy in directions:
                jump_row = current_row + 2 * dx
                jump_col = current_col + 2 * dy
                mid_row = current_row + dx
                mid_col = current_col + dy

                # Check if jump is valid and hasn't already captured this piece
                if (0 <= jump_row < 6 and 0 <= jump_col < 6 and
                        self.board[mid_row][mid_col] * player < 0 and
                        self.board[jump_row][jump_col] == 0 and
                        (mid_row, mid_col) not in captured_positions):
                    # Create new path including this jump
                    new_path = current_path + [[current_row, current_col, jump_row, jump_col]]
                    new_captured = captured_positions | {(mid_row, mid_col)}

                    found_jumps.append(new_path)

                    # Recursively find additional jumps from new position
                    additional_jumps = find_sequential_jumps(jump_row, jump_col, new_path, new_captured)
                    found_jumps.extend(additional_jumps)

            return found_jumps

        # First check for any possible jumps
        all_jumps = find_sequential_jumps(row, col)

        # If jumps are available, they are mandatory
        if all_jumps:
            # For each sequence of jumps, create a single move from start to final position
            for jump_sequence in all_jumps:
                if jump_sequence:  # Make sure sequence isn't empty
                    start_pos = [row, col]
                    end_pos = jump_sequence[-1][2:]  # Last jump's [end_row, end_col]
                    final_action = start_pos + end_pos  # [row, col, end_row, end_col]

                    valid_actions.append(final_action)

                    # Store the full multi-jump sequence so we can remove all captured pieces
                    self.multijump_paths[tuple(final_action)] = jump_sequence
        else:
            # If no jumps are available, add regular moves
            for dx, dy in directions:
                new_row, new_col = row + dx, col + dy
                if 0 <= new_row < 6 and 0 <= new_col < 6:
                    if self.board[new_row][new_col] == 0:
                        valid_actions.append([row, col, new_row, new_col])

        return valid_actions

    def _calculate_reward(self, action, player, piece_type):
        """
        Helper method to calculate rewards for moves
        """
        start_row, start_col, end_row, end_col = action
        reward = 0

        # Reward for capturing (at least one jump)
        if abs(start_row - end_row) >= 2:
            reward += 3

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

    def capture_piece(self, action, board=None):
        """
        Enhanced capture method to handle multiple jumps and remove all captured pieces.
        Looks up the stored path in self.multijump_paths if it's a multi-jump.
        """
        if board is None:
            board = self.board

        start_row, start_col, end_row, end_col = action

        # If this action corresponds to a multi-jump path, remove all jumped-over pieces
        if tuple(action) in self.multijump_paths:
            jump_sequence = self.multijump_paths[tuple(action)]
            for seg in jump_sequence:
                sr, sc, er, ec = seg
                mid_row = (sr + er) // 2
                mid_col = (sc + ec) // 2
                board[mid_row][mid_col] = 0
        # Otherwise, handle single jump if needed
        elif abs(start_row - end_row) == 2:
            mid_row = (start_row + end_row) // 2
            mid_col = (start_col + end_col) // 2
            board[mid_row][mid_col] = 0

    def step(self, action, player):
        """
        Enhanced step method with draw condition tracking.
        Executes the move, captures pieces, promotes kings, and returns the new board + reward.
        """
        start_row, start_col, end_row, end_col = action

        # Store piece type before move
        piece_type = self.board[start_row][start_col]

        # Check if move is a capture (any jump >= 2 squares)
        is_capture = abs(start_row - end_row) >= 2
        if is_capture:
            self.moves_without_capture = 0
            self.capture_piece(action)
        else:
            self.moves_without_capture += 1

        # Move the piece
        self.board[end_row][end_col] = piece_type
        self.board[start_row][start_col] = 0

        # Check for king promotion
        old_piece = self.board[end_row][end_col]
        self.board = self.promote_to_king(self.board, end_row, end_col)
        if self.board[end_row][end_col] != old_piece:
            self.moves_without_king = 0
        else:
            self.moves_without_king += 1

        # Calculate reward
        reward = self._calculate_reward(action, player, piece_type)

        # Switch player
        self.player *= -1

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
