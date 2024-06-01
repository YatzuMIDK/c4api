class Connect4:
    ROWS = 6
    COLUMNS = 7
    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 = 2
    
    EMPTY_EMOJI = "⬛"
    PLAYER1_EMOJI = "🔴"
    PLAYER2_EMOJI = "🟡"
    
    def __init__(self):
        self.board = [[self.EMPTY for _ in range(self.COLUMNS)] for _ in range(self.ROWS)]
        self.current_player = self.PLAYER1
        self.winner = None

    def drop_piece(self, column: int) -> bool:
        if column < 0 or column >= self.COLUMNS or self.board[0][column] != self.EMPTY:
            return False
        
        for row in reversed(range(self.ROWS)):
            if self.board[row][column] == self.EMPTY:
                self.board[row][column] = self.current_player
                if self.check_winner(row, column):
                    self.winner = self.current_player
                self.current_player = self.PLAYER2 if self.current_player == self.PLAYER1 else self.PLAYER1
                return True
        return False

    def check_winner(self, row: int, column: int) -> bool:
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            for i in range(1, 4):
                r, c = row + dr * i, column + dc * i
                if 0 <= r < self.ROWS and 0 <= c < self.COLUMNS and self.board[r][c] == self.current_player:
                    count += 1
                else:
                    break
            for i in range(1, 4):
                r, c = row - dr * i, column - dc * i
                if 0 <= r < self.ROWS and 0 <= c < self.COLUMNS and self.board[r][c] == self.current_player:
                    count += 1
                else:
                    break
            if count >= 4:
                return True
        return False
    
    def get_board_with_emojis(self) -> str:
        emoji_board = ""
        for row in self.board:
            for cell in row:
                if cell == self.EMPTY:
                    emoji_board += self.EMPTY_EMOJI
                elif cell == self.PLAYER1:
                    emoji_board += self.PLAYER1_EMOJI
                elif cell == self.PLAYER2:
                    emoji_board += self.PLAYER2_EMOJI
            emoji_board += "\n"
        return emoji_board.strip()
