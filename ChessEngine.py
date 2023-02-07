class Game():
    def __init__(self):
        #first initialize the game board with all the pieces on it 
        self.board = [
        #col  0     1     2     3     4     5     6     7
            ["br", "bn", "bb", "bk", "bq", "bb", "bn", "br"], #row 0
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"], #row 1
            ["--", "--", "--", "--", "--", "--", "--", "--"], #row 2
            ["--", "--", "--", "--", "--", "--", "--", "--"], #row 3
            ["--", "--", "--", "--", "--", "--", "--", "--"], #row 4
            ["--", "--", "--", "--", "--", "--", "--", "--"], #row 5
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"], #row 6
            ["wr", "wn", "wb", "wk", "wq", "wb", "wn", "wr"]] #row 7
        self.move_functions = {'p': self.getPawnMove, 'r': self.getRookMove, 'n': self.getKnightMove, 'b': self.getBishopMove,'q': self.getQueenMove, 'k': self.getKingMove}
        self.white_to_move = True
        self.move_log = []
        self.white_king_pos = (7,4)
        self.black_king_pos = (0,4)

    def makeMove(self, move):
        self.board[move.start_row][move.start_col] = '--'
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move
        if move.piece_moved == 'wk':
            self.white_king_pos = (move.end_row, move.end_col)
        elif move.piece_moved == 'bk':
            self.black_king_pos  = (move.end_row, move.end_col)

    def undoMove(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move
            if move.piece_moved == 'wk':
                self.white_king_pos = (move.start_row, move.start_col)
            elif move.piece_moved == 'bk':
                self.black_king_pos  = (move.start_row, move.start_col)
    def Reset(self):
        if len(self.move_log) != 0:
            self.move_log = []
            self.board = [
            ["br", "bn", "bb", "bk", "bq", "bb", "bn", "br"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wr", "wn", "wb", "wk", "wq", "wb", "wn", "wr"]]
            self.black_king_pos = (0,4)
            self.white_king_pos = (7,4)

    def getValidMoves(self):
        return self.getAllMoves()

    def getAllMoves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    piece = self.board[row][col][1]
                    self.move_functions[piece](row, col, moves)   
        return moves      

    def getPawnMove(self, row, col, moves):
        #white pawn moves
        if self.white_to_move:
            if self.board[row - 1][col] == "--":
                moves.append(Move((row, col), (row - 1, col), self.board))
                if (row == 6 and self.board[row - 2][col]) == '--':
                    moves.append(Move((row, col), (row - 2, col), self.board))
            if col - 1 >= 0 and self.board[row - 1][col - 1][0] == 'b':
                    moves.append(Move((row, col), (row - 1, col - 1), self.board))
            if col + 1 <= 7 and self.board[row - 1][col + 1][0] == 'b':
                    moves.append(Move((row, col), (row - 1, col + 1), self.board))
        #black pawn moves
        else:
            if self.board[row + 1][col] == "--":
                moves.append(Move((row,col), (row + 1, col), self.board))
                if (row == 1 and self.board[row + 2][col]) == '--':
                    moves.append(Move((row, col), (row + 2, col), self.board))
            if col - 1 >= 0 and self.board[row + 1][col - 1][0] == 'w':
                moves.append(Move((row, col), (row + 1, col - 1), self.board))
            if col + 1 <= 7 and self.board[row + 1][col + 1][0] == 'w':
                    moves.append(Move((row, col), (row + 1, col + 1), self.board))

    def getRookMove(self, row, col, moves):
        directions = ((-1,0),(0,-1),(1,0),(0,1))
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            for i in range(1,8):
                end_row = row + d[0] * i
                end_col = col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKnightMove(self, row, col, moves):
        knight_moves = ((-2, 1),(2, 1),(-2, -1),(2, -1),(1, 2),(1, -2),(-1, 2),(-1, -2))
        ally_color = 'w' if self.white_to_move else 'b'
        for move in knight_moves:
            end_row = row + move[0]
            end_col = col + move[1]
            if 0 <= end_row < 8 and 0<= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color :
                    moves.append(Move((row,col), (end_row, end_col), self.board))

    def getBishopMove(self, row, col, moves):
        directions = ((-1,1),(1,-1),(1,1),(-1,-1))
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            for i in range(1,8):
                end_row = row + d[0] * i
                end_col = col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getQueenMove(self, row, col, moves):
        self.getBishopMove(row,col,moves)
        self.getRookMove(row,col,moves)
        
    def getKingMove(self, row, col, moves):
        king_moves = [(0, 1),(0, -1),(1, 0),(-1, 0),(1, 1),(1, -1),(-1, 1),(-1, -1)]
        ally_color = 'w' if self.white_to_move else 'b'
        for i in range(8):
            end_row = row + king_moves[i][0]
            end_col = col + king_moves[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    moves.append(Move((row, col),(end_row, end_col), self.board))

class Move():
    rank_to_row = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
    row_to_rank = {v: k for k, v in rank_to_row.items()}
    file_to_col = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    col_to_file = {v: k for k, v in file_to_col.items()}

    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.move_ID = (self.start_row * 1000) + (self.start_col * 100) + (self.end_row * 10) + self.end_col

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_ID == other.move_ID
        else:
            return False

    def getChessNotation(self):
        return self.getRankFile(self.start_row, self.start_col) + self.getRankFile(self.end_row, self.end_col)
    
    def getRankFile(self, row, col):
        return self.col_to_file[col] + self.row_to_rank[row]