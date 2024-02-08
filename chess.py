
from random import randint
from copy import deepcopy


def combineDicts(d1,d2):
    d3 = {}
    for key,item in d1.items():
        d3[key] = item
    for key,item in d2.items():
        if key in d3.keys():
            d3[key] += item
        else:
            d3[key] = item
    return d3


class chess():
    board = [[None for i in range(8)] for i in range(8)]
    # analysisBoard = board.copy()
    whitePieces = [] #kings are at index 0.
    blackPieces = []

    def isEmpty(self,loc):
        x = loc[0]
        y = loc[1]
        if (x>=0 and x <= 7) and (y >= 0 and y <= 7) and self.board[x][y] is None:
            return True
        else:
            return False
    
    def hasEnded(self,isWhite):
        if isWhite:
            pieces = self.whitePieces
        else:
            pieces = self.blackPieces
        for piece in pieces:
            if piece.moves()+piece.captures() != []:
                return 1
        else:
            if pieces[0].hasCheck():
                return -1
            else:
                return 0
            
    def allCaptures(self,isWhite):
        captures = {}
        if isWhite:
            for piece in self.whitePieces:
                Pmoves = piece.captures()
                if len(Pmoves) != 0:
                    captures[piece] = Pmoves
        else:
            for piece in self.blackPieces:
                Pmoves = piece.captures()
                if len(Pmoves) != 0:
                    captures[piece] = Pmoves
        return captures
    
    def allMoves(self,isWhite):
        moves = {}
        if isWhite:
            for piece in self.whitePieces:
                Pmoves = piece.moves()
                if len(Pmoves) != 0:
                    moves[piece] = Pmoves
        else:
            for piece in self.blackPieces:
                Pmoves = piece.moves()
                if len(Pmoves) != 0:
                    moves[piece] = Pmoves
        return moves
    
    def maxCapture(self,captures):
        pieces = list(captures.keys())
        maxThing = []
        for piece in pieces:
            for capture in captures[piece]:
                enemyThing = self.board[capture[0]][capture[1]]
                if len(maxThing) == 0:
                    maxThing = [piece,enemyThing]
                elif enemyThing.value > maxThing[1].value:
                    maxThing[0] = piece
                    maxThing[1] = enemyThing
        # print(maxThing)
        return maxThing
    
    def boardEval(self):
        current = 0
        for wPiece in self.whitePieces:
            if wPiece.location[0] == 0:
                current -= 0.02
            elif wPiece.location[0] == 1:
                current -= 0.01
            current += wPiece.value
            # if wPiece.location[0] == 0:
            #     current -= 0.02
        for bPiece in self.blackPieces:
            if bPiece.location[0] == 7:
                current += 0.02
            elif bPiece.location[0] == 6:
                current += 0.01
            current -= bPiece.value
        return round(current,2)

    def boardAnalysis(self,piece,move,stopNow = 1):
        depth = 1
        isWhite = piece.isWhite
        # print(isWhite)
        # oldboard = self.board.copy()
        pieceLocs = {p:p.location for p in self.whitePieces+self.blackPieces}
        kingCastles = {k:k.canCastle for k in self.whitePieces+self.blackPieces if type(k) == king}
        pawnLongs = {p:p.hasLong for p in self.whitePieces+self.blackPieces if type(p) == pawn}
        # print(pieceLocs)
        elims = []

        def reset(complete = False):
            # print(self.board)
            for p in self.whitePieces+self.blackPieces+elims:
                # if len(elims) > 0:
                #     print(elims)
                p.move(pieceLocs[p])
            # for p in elims:
            #     p.move(pieceLocs[p])
            for k in self.whitePieces+self.blackPieces:
                if type(k) == king:
                    k.canCastle = kingCastles[k]
            for p in self.whitePieces+self.blackPieces:
                if type(p) == pawn:
                    p.hasLong = pawnLongs[p]
            piece.updatePieces()
            if not complete:
                if self.board[move[0]][move[1]] is None:
                    piece.move(move)
                else:
                    elims.append(self.board[move[0]][move[1]])
                    piece.capture(move)
            # print(self.board)
        

        current = None

        #beginning exploration
        if self.board[move[0]][move[1]] is None:
            piece.move(move)
            # capture = False
        else:
            elims.append(self.board[move[0]][move[1]])
            piece.capture(move)
            # capture = True
            # print(piece,move,self.boardEval())
        # tst = self.allMoves(not isWhite).items()
        # if len(list(tst)) == 0:
        #     self.printBoard()
        # for deep in range(depth):
        for p,newlocs in self.allCaptures(not isWhite).items():
            for loc in newlocs:
                elims.append(self.board[loc[0]][loc[1]])
                p.capture(loc)
                # eval = self.boardEval()
                # efEval = -eval*(-1)**isWhite

                if stopNow > 0:
                    # efEval = -100000000000
                    efEval = -game.boardAnalysis(p,loc,stopNow-1)*(-1)**isWhite
                else:
                    efEval = -self.boardEval()*(-1)**isWhite
                if current is None:
                    current = efEval
                else:
                    current = min(efEval,current)
                # print(efEval,current)

                # if capture:
                    # print(piece,move,p,loc,-eval*(-1)**isWhite,current)
                # if piece.value == 3.45 and move == (5,7):
                #     print(current)
                reset()
                # elims = []
                # print(self.board)
        for p,newlocs in self.allMoves(not isWhite).items():
            for loc in newlocs:
                p.move(loc)
                # eval = self.boardEval()
                # efEval = -eval*(-1)**isWhite
                if stopNow > 0:
                    # efEval = -100000000000
                    efEval = -1*game.boardAnalysis(p,loc,stopNow-1)*((-1)**isWhite)
                else:
                    efEval = -self.boardEval()*(-1)**isWhite
                # current = min(efEval,current)
                if current is None:
                    current = efEval
                else:
                    current = min(efEval,current)
                # print(efEval,current)
                # current = min(-eval*(-1)**isWhite,current)
                # print(piece,move,p,newlocs,-eval*(-1)**isWhite,current)
                reset()
        #resetting everything to beginning
        # game.printBoard()
        # print()
        # if current == -3.46:
        #     game.printBoard()
        #     print(piece,move,game.boardEval())

        reset(True)
        # game.printBoard()
        # print(piece,move,current)
        # if current is None:
        #     self.printBoard()
        #     print(tst)
        
        if current is None:
            current = -10000000
        return current
    
    def convertCoord(self,coord):
        letters = {1:"a",2:"b",3:"c",4:"d",5:"e",6:"f",7:"g",8:"h"}
        x = letters[coord[1]+1]
        y = str(coord[0]+1)
        return x+y
    
    def convertToCoord(self,coord):
        letters = {"a":1,"b":2,"c":3,"d":4,"e":5,"f":6,"g":7,"h":8}
        x = letters[coord[0]] - 1
        y = int(coord[1]) - 1
        return (y,x)
    
    def getKing(self,isWhite):
        if isWhite:
            for p in self.whitePieces:
                if type(p) == king:
                    return p
        else:
            for p in self.blackPieces:
                if type(p) == king:
                    return p
                
    def printBoard(self):
        for row in self.board[::-1]:
            currentRow = ""
            for square in row:
                if square is None:
                    currentRow += "_"
                elif type(square) == pawn:
                    currentRow += "P"
                elif type(square) == king:
                    currentRow += "K"
                elif type(square) == queen:
                    currentRow += "Q"
                elif type(square) == rook:
                    currentRow += "R"
                elif type(square) == knight:
                    currentRow += "N"
                elif type(square) == bishop:
                    currentRow += "B"
                currentRow += " "
            print(currentRow)
        print()
        
                

class piece(chess):
    def __init__(self,location,isWhite):
        self.location = location
        self.isWhite = isWhite
        # self.board[location[0]][location[1]] = 
        self.updateLoc(location)
        self.updatePieces()

    def updateLoc(self,newloc):
        self.board[self.location[0]][self.location[1]] = None
        self.location = newloc
        self.board[self.location[0]][self.location[1]] = self
    
    def updatePieces(self):
        # print(self.board)
        for row in self.board:
            for square in row:
                if square is not None:
                    if square.isWhite and square not in self.whitePieces:
                        self.whitePieces.append(square)
                    elif not square.isWhite and square not in self.blackPieces:
                        # print("HI")
                        self.blackPieces.append(square)

    def removePieces(self):
        for piece in self.blackPieces + self.whitePieces:
            for row in self.board:
                if piece in row:
                    break
            else:
                if piece.isWhite:
                    self.whitePieces.remove(piece)
                else:
                    self.blackPieces.remove(piece)

    def move(self,newloc):
        # self.location = newloc
        # self.board[newloc[0]][newloc[1]] = self
        self.updateLoc(newloc)
        # self.board = 

    def capture(self,newloc):
        self.updateLoc(newloc)
        # print(self.board)
        # print(self.blackPieces)
        self.removePieces()
        # print(self.blackPieces)
    
    def occupy(self,newloc):
        if self.board[newloc[0]][newloc[1]] is None:
            self.move(newloc)
        else:
            self.capture(newloc)
    # def 

    def isEnemy(self,loc):
        x = loc[0]
        y = loc[1]
        if (x>=0 and x <= 7) and (y >= 0 and y <= 7) and not self.isEmpty(loc) and self.board[x][y].isWhite != self.isWhite:
            return True
        else:
            return False
        
    def inCheck(self,newPlace=None):
        if newPlace is None:
            newPlace = self.location
        lastPlace = self.location
        tmp = self.board[newPlace[0]][newPlace[1]]
        self.capture(newPlace)
        # print(self.blackPieces)
        isCheck = False
        if self.isWhite and self.getKing(True).hasCheck():
            isCheck = True
        elif not self.isWhite and self.getKing(False).hasCheck():
            isCheck = True
        self.move(lastPlace)
        self.board[newPlace[0]][newPlace[1]] = tmp
        self.updatePieces()
        return isCheck

class pawn(piece):
    value = 1
    hasLong = True
    def moves(self):
        empty = []
        x = self.location[1]
        y = self.location[0]
        if self.isWhite:
            if self.isEmpty((y+1,x)):
                if not self.inCheck((y+1,x)):
                    empty.append((y+1,x))
                if self.hasLong and self.isEmpty((y+2,x)) and not self.inCheck((y+2,x)):
                    self.hasLong = False
                    empty.append((y+2,x))
        else:
            if self.isEmpty((y-1,x)):
                if not self.inCheck((y-1,x)):
                    empty.append((y-1,x))
                if self.hasLong and self.isEmpty((y-2,x)) and not self.inCheck((y-2,x)):
                    self.hasLong = False
                    empty.append((y-2,x))
        return empty
    
    def captures(self,checkMatters = True):
        enemy = []
        x = self.location[1]
        y = self.location[0]
        if self.isWhite:
            if self.isEnemy((y+1,x+1)):
                if checkMatters and not self.inCheck((y+1,x+1)):
                    enemy.append((y+1,x+1))
                elif not checkMatters:
                    enemy.append((y+1,x+1))
            if self.isEnemy((y+1,x-1)):
                if checkMatters and not self.inCheck((y+1,x-1)):
                    enemy.append((y+1,x-1))
                elif not checkMatters:
                    enemy.append((y+1,x-1))
        else:
            if self.isEnemy((y-1,x+1)):
                if checkMatters and not self.inCheck((y-1,x+1)):
                    enemy.append((y-1,x+1))
                elif not checkMatters:
                    enemy.append((y-1,x+1))
            if self.isEnemy((y-1,x-1)):
                if checkMatters and not self.inCheck((y-1,x-1)):
                    enemy.append((y-1,x-1))
                elif not checkMatters:
                    enemy.append((y-1,x-1))
        return enemy
    
    # def captureNoCheck(self):

    
    def __str__(self):
        return "Pawn"

class knight(piece):
    value = 3.45
    def moves(self):
        empty = []
        x = self.location[0]
        y = self.location[1]
        for isPlusX in range(2):
            for isPlusY in range(2):
                for s in range(1,3):
                    coord = (x+(-1)**isPlusX*s,y+(-1)**isPlusY*(3-s))
                    if self.isEmpty(coord) and not self.inCheck(coord):
                        empty.append(coord)
        return empty
    
    def captures(self,checkMatters = True):
        enemy = []
        x = self.location[0]
        y = self.location[1]
        for isPlusX in range(2):
            for isPlusY in range(2):
                for s in range(1,3):
                    coord = (x+(-1)**isPlusX*s,y+(-1)**isPlusY*(3-s))
                    if self.isEnemy(coord):
                        if checkMatters and not self.inCheck(coord):
                            enemy.append(coord)
                        elif not checkMatters:
                            enemy.append(coord)
        return enemy
    
    def __str__(self):
        return "Knight"

class bishop(piece):
    value = 3.55
    def moves(self):
        empty = []
        x = self.location[1]
        y = self.location[0]
        for dir in range(4):
            for d in range(1,9):
                c = (y+(-1)**int((dir-dir%2)/2)*d,x+(-1)**(dir%2)*d)
                if self.isEmpty(c) and not self.inCheck(c):
                    empty.append(c)
                else:
                    # print(c)
                    break
        return empty
    
    def captures(self,checkMatters = True):
        enemy = []
        x = self.location[1]
        y = self.location[0]
        for dir in range(4):
            for d in range(1,8):
                c = (y+(-1)**int((dir-dir%2)/2)*d,x+(-1)**(dir%2)*d)
                if self.isEnemy(c):
                    if checkMatters and not self.inCheck(c):
                        enemy.append(c)
                        break
                    elif not checkMatters:
                        enemy.append(c)
                        break
                elif not self.isEmpty(c):
                    break
        return enemy
    
    def __str__(self):
        return "Bishop"

class rook(piece):
    value = 5.25
    def moves(self):
        empty = []
        x = self.location[1]
        y = self.location[0]
        # print(self.location)
        for dir in range(4):
            for d in range(1,9):
                c = (y+(-1)**(dir%2)*d*(int(dir/2)),x+(-1)**(dir%2)*d*(1-int(dir/2)))
                # print(c)
                if self.isEmpty(c) and not self.inCheck(c):
                    empty.append(c)
                else:
                    # print(c)
                    break
        return empty
    
    def captures(self,checkMatters=True):
        enemy = []
        x = self.location[1]
        y = self.location[0]
        for dir in range(4):
            for d in range(1,9):
                c = (y+(-1)**(dir%2)*d*(int(dir/2)),x+(-1)**(dir%2)*d*(1-int(dir/2)))
                if self.isEnemy(c):
                    if checkMatters and not self.inCheck(c):
                        enemy.append(c)
                        break
                    elif not checkMatters:
                        enemy.append(c)
                        break
                elif not self.isEmpty(c):
                    break
        return enemy
    
    def __str__(self):
        return "Rook"

class queen(piece):
    value = 10
    def moves(self):
        return rook.moves(self)+bishop.moves(self)
    
    def captures(self,checkMatters=True):
        return rook.captures(self,checkMatters)+bishop.captures(self,checkMatters)
    
    def __str__(self):
        return "Queen"

class king(piece):
    value = 1000000000
    canCastle = True
    def moves(self):
        empty = []
        x = self.location[0]
        y = self.location[1]
        c1 = (x+1,y)
        c2 = (x+1,y-1)
        c3 = (x,y-1)
        c4 = (x-1,y-1)
        c5 = (x-1,y)
        c6 = (x-1,y+1)
        c7 = (x,y+1)
        c8 = (x+1,y+1)
        possibles = [c1,c2,c3,c4,c5,c6,c7,c8]
        for i in possibles:
            if self.isEmpty(i) and not self.inCheck(i):
                empty.append(i)
        return empty
    
    def captures(self,checkMatters=True):
        enemy = []
        x = self.location[0]
        y = self.location[1]
        c1 = (x+1,y)
        c2 = (x+1,y-1)
        c3 = (x,y-1)
        c4 = (x-1,y-1)
        c5 = (x-1,y)
        c6 = (x-1,y+1)
        c7 = (x,y+1)
        c8 = (x+1,y+1)
        possibles = [c1,c2,c3,c4,c5,c6,c7,c8]
        for i in possibles:
            if self.isEnemy(i):
                if checkMatters and not self.inCheck(i):
                    enemy.append(i)
                elif not checkMatters:
                    enemy.append(i)
        return enemy
    
    def hasCheck(self):
        if self.isWhite:
            pieces = self.blackPieces
        else:
            pieces = self.whitePieces
        # print(self.location)
        # print(pieces)
        for piece in pieces:
            # print(piece)
            # print(piece.captures())
            # print(piece)
            if self.location in piece.captures(False):
                return True
        else:
            return False
    
    def __str__(self):
        return "King"

game = chess()
# analysisGame = game
# k2 = king((7,5),False)
# k1 = king((0,0),True)
# b2 = bishop((3,3),False)
# b1 = bishop((1,1),True)


#DEFAULT BOARD:

k1 = king((0,4),True)
q1 = queen((0,3),True)
b1 = bishop((0,2),True)
b2 = bishop((0,5),True)
n1 = knight((0,1),True)
n2 = knight((0,6),True)
r1 = rook((0,0),True)
r2 = rook((0,7),True)
pawns1 = [pawn((1,i),True) for i in range(8)]
# p1 = pawn((1,4),True)
# p2 = pawn((1,3),True)
# p3 = pawn((1,5),True)

k2 = king((7,4),False)
q2 = queen((7,3),False)
b3 = bishop((7,2),False)
b4 = bishop((7,5),False)
n3 = knight((7,1),False)
n4 = knight((7,6),False)
r3 = rook((7,0),False)
r4 = rook((7,7),False)
pawns2 = [pawn((6,i),False) for i in range(8)]

# print(b3.moves())

turn = 1
youAreWhite = True
# print(game.board)
# analy = deepcopy(game)
# print(game.blackPieces)
# print(game.board)
# print(analy.blackPieces)
# print(game.blackPieces)

# pawns1[4].move((3,4))
# n3.move((5,0))
# print(game.boardEval())

# exit()
# n1.move((2,2))
# print(game.boardEval())

if youAreWhite is not None:
    while True:
        # print(turn)
        whiteTurn = (turn%2 == 1)
        if whiteTurn == youAreWhite:
            inp = input(str(turn)+". ").split()
            og = game.convertToCoord(inp[0])
            # og = tuple(map(int,input().split()))
            new = game.convertToCoord(inp[1])
            p = game.board[og[0]][og[1]]
            if game.board[new[0]][new[1]] is None:
                p.move(new)
            else:
                p.capture(new)
            if game.hasEnded(not whiteTurn) == 0:
                print("Stalemate!")
                break
            elif game.hasEnded(not whiteTurn) == -1:
                print(whiteTurn, "YOU WON!")
                break
        else:
            # print(game.board)
            captures = game.allCaptures(whiteTurn)
            moves = game.allMoves(whiteTurn)
            allMoves = combineDicts(captures,moves)
            # print(allMoves)
            bestMove = None
            # print(moves)
            # if turn == 8:
            #     print(n3.moves())
            #     print(allMoves)
            #     print(moves)
            # print(list(allMoves.keys())[2])
            for P,M in allMoves.items():
                for move in M:
                    # print(P,P.location,move)
                    eval = game.boardAnalysis(P,move,1)
                    # if turn == 8:
                    #     print(P,move,eval)
                    # print(eval)
                    # if P.value == 3.45 and move == (5,7):
                    # print(P,move,eval)
                    # print(P,move,game.boardEval())
                    if bestMove is None:
                        bestMove = [eval,P,move]
                    elif eval > bestMove[0]:
                        bestMove = [eval,P,move]
                    # elif -eval*youAreWhite == bestMove[0] and randint(0,10) == 0:
                    #     bestMove = [-eval*youAreWhite,P,move]

            # print(bestMove[1].location,bestMove[2])
            print(str(turn)+".",game.convertCoord(bestMove[1].location),game.convertCoord(bestMove[2]))
            bestMove[1].occupy(bestMove[2])
            game.printBoard()
            if game.hasEnded(not whiteTurn) == 0:
                print("Stalemate!")
                break
            elif game.hasEnded(not whiteTurn) == -1:
                print("COMPUTER WON!")
                break
            
        turn += 1
else:
    while True:
        whiteTurn = (turn%2 == 1)
        captures = game.allCaptures(whiteTurn)
        moves = game.allMoves(whiteTurn)
        if len(captures.values()) != 0:
            thing,attack = game.maxCapture(captures)
            print(thing.location,attack.location)
            thing.capture(attack.location)
        elif len(moves.values()) != 0:
            k = list(moves.keys())
            index = randint(0,len(k)-1)
            thing = k[index]
            newLoc = moves[thing][randint(0,len(moves[thing])-1)]
            print(thing.location,newLoc)
            thing.move(newLoc)
        else:
            if game.hasEnded(whiteTurn) == 0:
                print("Stalemate!")
            else:
                print(whiteTurn, "LOST!")
            break
        turn +=1
