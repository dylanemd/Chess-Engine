import copy

class Piece:
    def __init__(self, color, type, position, has_moved, image):
        self.color = color
        self.type = type
        self.position = position 
        self.has_moved = has_moved
        self.image = image

    def __deepcopy__(self, memo):
        new_piece = self.__class__(
            self.color,
            self.type,
            copy.deepcopy(self.position, memo),
            self.has_moved,
            self.image
        )
        return new_piece

    def checkIsOpponent(self, board, x, y):
        piece = board[y][x]
        if piece == None:
            return False
        if self.color != piece.color:
            return True
        else:
            return False
            
    def outOfBounds(self, x, y):
        if x > 7 or x < 0 or y > 7 or y < 0:
            return True
        else:
            return False
    def checkIfOccupied(self, board, x, y):
        if board[y][x] == None:
            return False
        else:
            return True
  
# Subclasses
class Rook(Piece):
    def __init__(self,color, type, position, has_moved, image):
        super().__init__(color, type, position, has_moved, image)
    
    def possibleMoves(self, board, en_passant_target=None):
        x = self.position[0]
        y = self.position[1]
        valid_moves = []
        # Checks moves right of Rook 
        for i in range(1,8):
            out_of_bound = self.outOfBounds(x+i,y)
            if out_of_bound == True:
                break
            is_occupied = self.checkIfOccupied(board,x+i,y)
            is_opponent = self.checkIsOpponent(board,x+i,y)
            if is_occupied == True and is_opponent == True:
                valid_moves.append((x+i,y))
                break
            elif is_occupied == True and is_opponent == False:
                break
            else:
                valid_moves.append((x+i,y))
        # Check moves left of Rook
        for i in range(1,8):
            out_of_bound = self.outOfBounds(x-i,y)
            if out_of_bound == True:
                break
            is_occupied = self.checkIfOccupied(board,x-i,y)
            is_opponent = self.checkIsOpponent(board,x-i,y)
            if is_occupied == True and is_opponent == True: 
                valid_moves.append((x-i,y))
                break
            elif is_occupied == True and is_opponent == False:
                break
            else:
                valid_moves.append((x-i,y))
        # Check moves up from Rook
        for i in range(1,8):
            out_of_bound = self.outOfBounds(x, y + i)
            if out_of_bound == True:
                break
            is_occupied = self.checkIfOccupied(board,x,y+i)
            is_opponent = self.checkIsOpponent(board,x,y+i)
            if is_occupied == True and is_opponent == True:
                valid_moves.append((x, y + i))
                break
            elif is_occupied == True and is_opponent == False:
                break
            else:
                valid_moves.append((x,y+i))
        # Check moves down from Rook
        for i in range(1,8):
            out_of_bound = self.outOfBounds(x,y-i)
            if out_of_bound == True:
                break
            is_occupied = self.checkIfOccupied(board,x,y-i)
            is_opponent = self.checkIsOpponent(board,x,y-i)
            if is_occupied == True and is_opponent == True: 
                valid_moves.append((x,y-i))
                break
            elif is_occupied == True and is_opponent == False:
                break
            else:
                valid_moves.append((x,y-i))
        return valid_moves
    
class Knight(Piece):
    def __init__(self,color, type, position, has_moved, image):
        super().__init__(color, type, position, has_moved, image)
    def possibleMoves(self,board, en_passant_target=None):
        x = self.position[0]
        y = self.position[1]
        valid_moves = []
        for i in range(-1,2,2):
            for j in range(-2,3,4):
                out_of_bounds = self.outOfBounds(x+i,y+j)
                if out_of_bounds == True:
                    continue
                is_occupied = self.checkIfOccupied(board,x+i,y+j)
                is_opponent = self.checkIsOpponent(board,x+i,y+j)
                if is_occupied == True and is_opponent == True:
                    valid_moves.append((x+i,y+j))
                elif is_occupied == True and is_opponent == False:
                    continue
                else:
                    valid_moves.append((x+i,y+j))

        for i in range(-1,2,2):
            for j in range(-2,3,4):
                out_of_bounds = self.outOfBounds(x+j,y+i)
                if out_of_bounds == True:
                    continue
                is_occupied = self.checkIfOccupied(board,x+j,y+i)
                is_opponent = self.checkIsOpponent(board,x+j,y+i)
                if is_occupied == True and is_opponent == True:
                    valid_moves.append((x+j,y+i))
                elif is_occupied == True and is_opponent == False:
                    continue
                else:
                    valid_moves.append((x+j,y+i))
        return valid_moves

class Queen(Piece):
    def __init__(self,color, type, position, has_moved, image):
        super().__init__(color, type, position, has_moved, image)
    def possibleMoves(self, board, en_passant_target=None):
        x = self.position[0]
        y = self.position[1]
        valid_moves = []
        # Top right
        for i in range(1,8):
            out_of_bounds = self.outOfBounds(x+i,y+i)
            if out_of_bounds == True:
                break
            is_occupied = self.checkIfOccupied(board,x+i,y+i)
            is_opponent = self.checkIsOpponent(board,x+i,y+i)
            if is_occupied == True and is_opponent == True:
                valid_moves.append((x+i,y+i))
                break
            elif is_occupied == True and is_opponent == False:
                break
            else:
                valid_moves.append((x+i,y+i))
        # Top left
        for i in range(1,8):
            out_of_bounds = self.outOfBounds(x-i,y+i)
            if out_of_bounds == True:
                break
            is_occupied = self.checkIfOccupied(board,x-i,y+i)
            is_opponent = self.checkIsOpponent(board,x-i,y+i)
            if is_occupied == True and is_opponent == True:
                valid_moves.append((x-i,y+i))
                break
            elif is_occupied == True and is_opponent == False:
                break
            else:
                valid_moves.append((x-i,y+i))
        # Bottom right
        for i in range(1,8):
            out_of_bounds = self.outOfBounds(x+i,y-i)
            if out_of_bounds == True:
                break
            is_occupied = self.checkIfOccupied(board,x+i,y-i)
            is_opponent = self.checkIsOpponent(board,x+i,y-i)
            if is_occupied == True and is_opponent == True:
                valid_moves.append((x+i,y-i))
                break
            elif is_occupied == True and is_opponent == False:
                break
            else:
                valid_moves.append((x+i,y-i))
        # Bottom left
        for i in range(1,8):
            out_of_bounds = self.outOfBounds(x-i,y-i)
            if out_of_bounds == True:
                break
            is_occupied = self.checkIfOccupied(board,x-i,y-i)
            is_opponent = self.checkIsOpponent(board,x-i,y-i)
            if is_occupied == True and is_opponent == True:
                valid_moves.append((x-i,y-i))
                break
            elif is_occupied == True and is_opponent == False:
                break
            else:
                valid_moves.append((x-i,y-i))
        # Right
        for i in range(1,8):
            out_of_bound = self.outOfBounds(x+i,y)
            if out_of_bound == True:
                break
            is_occupied = self.checkIfOccupied(board,x+i,y)
            is_opponent = self.checkIsOpponent(board,x+i,y)
            if is_occupied == True and is_opponent == True:
                valid_moves.append((x+i,y))
                break
            elif is_occupied == True and is_opponent == False:
                break
            else:
                valid_moves.append((x+i,y))
        # Left
        for i in range(1,8):
            out_of_bound = self.outOfBounds(x-i,y)
            if out_of_bound == True:
                break
            is_occupied = self.checkIfOccupied(board,x-i,y)
            is_opponent = self.checkIsOpponent(board,x-i,y)
            if is_occupied == True and is_opponent == True: 
                valid_moves.append((x-i,y))
                break
            elif is_occupied == True and is_opponent == False:
                break
            else:
                valid_moves.append((x-i,y))
        # Up
        for i in range(1,8):
            out_of_bound = self.outOfBounds(x,y+i)
            if out_of_bound == True:
                break
            is_occupied = self.checkIfOccupied(board,x,y+i)
            is_opponent = self.checkIsOpponent(board,x,y+i)
            if is_occupied == True and is_opponent == True:
                valid_moves.append((x,y+i))
                break
            elif is_occupied == True and is_opponent == False:
                break
            else:
                valid_moves.append((x,y+i))
        # Down
        for i in range(1,8):
            out_of_bound = self.outOfBounds(x,y-i)
            if out_of_bound == True:
                break
            is_occupied = self.checkIfOccupied(board,x,y-i)
            is_opponent = self.checkIsOpponent(board,x,y-i)
            if is_occupied == True and is_opponent == True: 
                valid_moves.append((x,y-i))
                break
            elif is_occupied == True and is_opponent == False:
                break
            else:
                valid_moves.append((x,y-i))
        return valid_moves
    
class King(Piece):
    def __init__(self,color, type, position, has_moved, image):
        super().__init__(color, type, position, has_moved, image)
    def possibleMoves(self, board, en_passant_target=None):
        x = self.position[0]
        y = self.position[1]
        valid_moves = []
        # upper right, upper left, lower right, lower left
        for i in range(-1,2,2):
            for j in range(-1,2,2):
                out_of_bound = self.outOfBounds(x+j,y+i)
                if out_of_bound == True:
                    continue
                is_occupied = self.checkIfOccupied(board,x+j,y+i)
                is_opponent = self.checkIsOpponent(board,x+j,y+i)
                if is_occupied == True and is_opponent == True: 
                    valid_moves.append((x+j,y+i))
                elif is_occupied == True and is_opponent == False:
                    continue
                else:
                    valid_moves.append((x+j,y+i))
        # Up and down
        for i in range(-1,2,2):
            out_of_bound = self.outOfBounds(x,y+i)
            if out_of_bound == True:
                continue
            is_occupied = self.checkIfOccupied(board,x,y+i)
            is_opponent = self.checkIsOpponent(board,x,y+i)
            if is_occupied == True and is_opponent == True: 
                valid_moves.append((x,y+i))
            elif is_occupied == True and is_opponent == False:
                continue
            else:
                valid_moves.append((x,y+i))
        # left and right
        for i in range(-1,2,2):
            out_of_bound = self.outOfBounds(x+i,y)
            if out_of_bound == True:
                continue
            is_occupied = self.checkIfOccupied(board,x+i,y)
            is_opponent = self.checkIsOpponent(board,x+i,y)
            if is_occupied == True and is_opponent == True: 
                valid_moves.append((x+i,y))
            elif is_occupied == True and is_opponent == False:
                continue
            else:
                valid_moves.append((x+i,y))
        return valid_moves
                
class Bishop(Piece):
    def __init__(self,color, type, position, has_moved, image):
        super().__init__(color, type, position, has_moved, image)
    def possibleMoves(self, board, en_passant_target=None):
        x = self.position[0]
        y = self.position[1]
        valid_moves = []
        # Top right
        for i in range(1,8):
            out_of_bounds = self.outOfBounds(x+i,y+i)
            if out_of_bounds == True:
                break
            is_occupied = self.checkIfOccupied(board,x+i,y+i)
            is_opponent = self.checkIsOpponent(board,x+i,y+i)
            if is_occupied == True and is_opponent == True:
                valid_moves.append((x+i,y+i))
                break
            elif is_occupied == True and is_opponent == False:
                break
            else:
                valid_moves.append((x+i,y+i))
        # Top left
        for i in range(1,8):
            out_of_bounds = self.outOfBounds(x-i,y+i)
            if out_of_bounds == True:
                break
            is_occupied = self.checkIfOccupied(board,x-i,y+i)
            is_opponent = self.checkIsOpponent(board,x-i,y+i)
            if is_occupied == True and is_opponent == True:
                valid_moves.append((x-i,y+i))
                break
            elif is_occupied == True and is_opponent == False:
                break
            else:
                valid_moves.append((x-i,y+i))
        # Bottom right
        for i in range(1,8):
            out_of_bounds = self.outOfBounds(x+i,y-i)
            if out_of_bounds == True:
                break
            is_occupied = self.checkIfOccupied(board,x+i,y-i)
            is_opponent = self.checkIsOpponent(board,x+i,y-i)
            if is_occupied == True and is_opponent == True:
                valid_moves.append((x+i,y-i))
                break
            elif is_occupied == True and is_opponent == False:
                break
            else:
                valid_moves.append((x+i,y-i))
        # Bottom left
        for i in range(1,8):
            out_of_bounds = self.outOfBounds(x-i,y-i)
            if out_of_bounds == True:
                break
            is_occupied = self.checkIfOccupied(board,x-i,y-i)
            is_opponent = self.checkIsOpponent(board,x-i,y-i)
            if is_occupied == True and is_opponent == True:
                valid_moves.append((x-i,y-i))
                break
            elif is_occupied == True and is_opponent == False:
                break
            else:
                valid_moves.append((x-i,y-i))
        return valid_moves
    
class Pawn(Piece):
    def __init__(self,color, type, position, has_moved, image):
        super().__init__(color, type, position, has_moved, image)
    def possibleMoves(self, board, en_passant_target=None):
        x = self.position[0]
        y = self.position[1]
        valid_moves = [] 
        if self.color == "White":
            direction = -1
        else:
            direction = 1
        # Foward
        out_of_bound = self.outOfBounds(x,y+direction)
        is_occupied = self.checkIfOccupied(board,x,y+direction)
        if out_of_bound == False:
            if is_occupied == False:
                valid_moves.append((x,y+direction))
        # For inital two foward movment
        if self.has_moved == False:
            new_direction = direction *2
            out_of_bound = self.outOfBounds(x,y+new_direction)
            is_occupied = self.checkIfOccupied(board,x,y+new_direction)
            is_occupied_front = self.checkIfOccupied(board,x,y+direction)
            if out_of_bound == False:
                if is_occupied == False and is_occupied_front == False:
                    valid_moves.append((x,y+new_direction))
        # Capturing 
        for i in range(-1,2,2):
            out_of_bound = self.outOfBounds(x+i,y+direction)
            if out_of_bound == True:
                continue
            is_occupied = self.checkIfOccupied(board,x+i,y+direction)
            is_opponent = self.checkIsOpponent(board,x+i,y+direction)
            if is_occupied == True and is_opponent == True: 
                valid_moves.append((x+i,y+direction))
            elif is_occupied == False and (x+i, y+direction) == en_passant_target:
                valid_moves.append((x+i,y+direction))
        return valid_moves