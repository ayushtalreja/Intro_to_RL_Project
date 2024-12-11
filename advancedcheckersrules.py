class AdvancedCheckersRules:
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