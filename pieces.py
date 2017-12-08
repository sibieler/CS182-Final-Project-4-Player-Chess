import random
import math
import os
import time
import numpy as np
import copy
from multiprocessing import Pool
'''
High level piece class containing the attributes that every piece will share.
Pieces must be given a start position, color, direction, board and x(row) and 
y(column) locations.
'''
class PIECE():
	def __init__(self, color, direction, board, x, y):
		self.x = y
		self.y = x
		self.color = color
		self.direction = direction
		self.board = board
		self.hasMoved = False
		self.score = 0
	'''
	Every piece must have a function to get its possible moves
	but it will be different for every piece type
	'''
	def getPossibleActions(self):
		raiseNotDefined()
	'''
	Internally ove the piece from its old location to its new one.
	'''
	def move(self,x,y):
		self.x = x
		self.y = y
		self.hasMoved = True

'''
Pawn piece class which has a different move function than other pieces
in order to keep track of whether or not it has become a queen.
'''
class PAWN(PIECE):
	def __init__(self, color, direction, board, x, y):
		PIECE.__init__(self, color, direction, board, x, y)
		self.score = 1
		self.moves = 0
	def move(self,x,y):
		self.moves += abs(self.y - y)
		self.x = x
		self.y = y
		self.hasMoved = True
		if self.moves >= 6:
			self.board.board[self.x][self.y] = QUEEN(self.color, self.direction, self.board, self.x, self.y, 1)
	def __str__(self):
		return "P" + self.color[0]
	'''
	Get pawns possible actions which include moving forward 2 if it has not moved,
	moving forward 1 and capturing diagonally forward 1 in the direction it is going.
	'''
	def getPossibleActions(self):
		actionList = []
		if not self.hasMoved:
			if self.direction == 'North':
				if self.board.empty(self.x-2, self.y) and self.board.empty(self.x-1, self.y):
					actionList.append((self.x-2, self.y,False))
			elif self.direction == 'South':
				if self.board.empty(self.x+2, self.y) and self.board.empty(self.x+1, self.y):
					actionList.append((self.x+2, self.y,False))
			elif self.direction == 'East':
				if self.board.empty(self.x, self.y+2) and self.board.empty(self.x, self.y+1):
					actionList.append((self.x, self.y+2,False))
			else:
				if self.board.empty(self.x, self.y-2) and self.board.empty(self.x, self.y-1):
					actionList.append((self.x, self.y-2,False))
		if self.direction == 'North':
			if self.board.empty(self.x-1, self.y):
				actionList.append((self.x-1, self.y,False))
		elif self.direction == 'South':
			if self.board.empty(self.x+1, self.y):
				actionList.append((self.x+1, self.y,False))
		elif self.direction == 'East':
			if self.board.empty(self.x, self.y+1):
				actionList.append((self.x, self.y+1,False))
		else:
			if self.board.empty(self.x, self.y-1):
				actionList.append((self.x , self.y-1,False))
		if self.direction == 'North':
			if not self.board.empty(self.x-1, self.y - 1) and not self.board.unusable(self.color, self.x-1, self.y - 1):
				if not self.board.ownPiece(self.color, self.x-1, self.y - 1):
					actionList.append((self.x-1, self.y - 1, False))
				else:
					actionList.append((self.x-1, self.y - 1, True))
			elif not self.board.unusable(self.color, self.x-1, self.y - 1):
				actionList.append((self.x-1, self.y - 1, True))
			if not self.board.empty(self.x-1, self.y + 1) and not self.board.unusable(self.color, self.x-1, self.y + 1):
				if not self.board.ownPiece(self.color, self.x-1, self.y + 1):
					actionList.append((self.x-1, self.y + 1,False))
				else:
					actionList.append((self.x-1, self.y + 1,True))
			elif not self.board.unusable(self.color, self.x-1, self.y +1):
				actionList.append((self.x-1, self.y + 1, True))
		elif self.direction == 'South':
			if not self.board.empty(self.x+1, self.y-1) and not self.board.unusable(self.color, self.x+1, self.y-1):
				if not self.board.ownPiece(self.color, self.x+1, self.y-1):
					actionList.append((self.x+1, self.y - 1,False))
				else:
					actionList.append((self.x+1, self.y - 1,True))
			elif not self.board.unusable(self.color, self.x+1, self.y-1):
				actionList.append((self.x+1, self.y - 1,True))
			if not self.board.empty(self.x+1, self.y + 1) and not self.board.unusable(self.color, self.x+1, self.y+1):
				if not self.board.ownPiece(self.color, self.x+1, self.y+1):
					actionList.append((self.x+1, self.y + 1,False))
				else:
					actionList.append((self.x+1, self.y + 1,True))
			elif not self.board.unusable(self.color, self.x+1, self.y+1):
				actionList.append((self.x+1, self.y + 1,True))
		elif self.direction == 'East':
			if not self.board.empty(self.x-1, self.y + 1) and not self.board.unusable(self.color, self.x-1, self.y + 1):
				if not self.board.ownPiece(self.color, self.x-1, self.y + 1):
					actionList.append((self.x-1, self.y + 1,False))
				else:
					actionList.append((self.x-1, self.y + 1,True))
			elif not self.board.unusable(self.color, self.x-1, self.y + 1):
				actionList.append((self.x-1, self.y + 1,True))
			if not self.board.empty(self.x+1, self.y + 1) and not self.board.unusable(self.color, self.x+1, self.y + 1):
				if not self.board.ownPiece(self.color, self.x+1, self.y + 1):
					actionList.append((self.x+1, self.y + 1,False))
				else:
					actionList.append((self.x+1, self.y + 1,True))
			elif not self.board.unusable(self.color, self.x+1, self.y + 1):
				actionList.append((self.x+1, self.y + 1,True))
		else:
			if not self.board.empty(self.x+1, self.y - 1) and not self.board.unusable(self.color, self.x+1, self.y - 1):
				if not self.board.ownPiece(self.color, self.x+1, self.y - 1):
					actionList.append((self.x+1, self.y -1, False))
				else:
					actionList.append((self.x+1, self.y -1, True))
			elif not self.board.unusable(self.color, self.x+1, self.y - 1):
				actionList.append((self.x+1, self.y -1, True))
			if not self.board.empty(self.x-1, self.y - 1) and not self.board.unusable(self.color, self.x-1, self.y - 1):
				if not self.board.ownPiece(self.color, self.x-1, self.y - 1):
					actionList.append((self.x-1, self.y - 1, False))
				else:
					actionList.append((self.x-1, self.y - 1, True))
			elif not self.board.unusable(self.color, self.x-1, self.y - 1):
				actionList.append((self.x-1, self.y - 1, True))
		return actionList
'''
Rook piece class that can move horizontally and vertically.
'''
class ROOK(PIECE):
	def __init__(self, color, direction, board, x, y):
		PIECE.__init__(self, color, direction, board, x, y)
		self.deltas = [(1,0),(0,1),(-1,0),(0,-1)]
		self.score = 5

	def __str__(self):
		return "R" + self.color[0]

	def getPossibleActions(self):
		actionList = []
		for delta in self.deltas:
			for i in range(1,13,1):
				if self.board.empty(self.x + delta[0] * i, self.y + delta[1] * i):
					actionList.append((self.x + delta[0] * i, self.y + delta[1] * i, False))
				elif self.board.unusable(self.color, self.x + delta[0] * i, self.y + delta[1] * i):
					break
				elif self.board.ownPiece(self.color, self.x + delta[0] * i, self.y + delta[1] * i):
					actionList.append((self.x + delta[0] * i, self.y + delta[1] * i,True))
					break
				else:
					actionList.append((self.x + delta[0] * i, self.y + delta[1] * i, False))
					break
		return actionList

'''
Knight piece class that can move in L shaped jumps with side lengths 2 and 1.
'''
class KNIGHT(PIECE):
	def __init__(self, color, direction, board, x, y):
		PIECE.__init__(self, color, direction, board, x, y)
		self.deltas = [(1,2),(2,1),(1,-2),(-2,1),(-2,-1),(-1,-2),(-1,2),(2,-1)]
		self.score = 3

	def __str__(self):
		return "N" + self.color[0]
		
	def getPossibleActions(self):
		actionList = []
		for delta in self.deltas:
			if self.board.empty(self.x + delta[0], self.y + delta[1]):
				actionList.append((self.x + delta[0], self.y + delta[1], False))
			elif self.board.unusable(self.color, self.x + delta[0], self.y + delta[1]):
				continue
			elif self.board.ownPiece(self.color, self.x + delta[0], self.y + delta[1]):
				actionList.append((self.x + delta[0], self.y + delta[1], True))
			else:
				actionList.append((self.x + delta[0], self.y + delta[1], False))
		return actionList

'''
Bishop piece that can move diagonally in any direciton.
'''
class BISHOP(PIECE):
	def __init__(self, color, direction, board, x, y):
		PIECE.__init__(self, color, direction, board, x, y)
		self.deltas = [(1,1),(-1,1),(-1,-1),(1,-1)]
		self.score = 3

	def __str__(self):
		return "B" + self.color[0]

	def getPossibleActions(self):
		actionList = []
		for delta in self.deltas:
			for i in range(1,13,1):
				if self.board.empty(self.x + delta[0] * i, self.y + delta[1] * i):
					actionList.append((self.x + delta[0] * i, self.y + delta[1] * i, False))
				elif self.board.unusable(self.color, self.x + delta[0] * i, self.y + delta[1] * i):
					break
				elif self.board.ownPiece(self.color, self.x + delta[0] * i, self.y + delta[1] * i):
					actionList.append((self.x + delta[0] * i, self.y + delta[1] * i, True))
					break
				else:
					actionList.append((self.x + delta[0] * i, self.y + delta[1] * i, False))
					break
		return actionList

'''
Queen piece that can move straight in any direction. Additionally it 
takes a score argument unlike other pieces because when you queen
a pawn in 4 player chess, capturing that queen only rewards you
1 point, as opposed to the 9 from the original queen.
'''
class QUEEN(PIECE):
	def __init__(self, color, direction, board, x, y, score = 9):
		PIECE.__init__(self, color, direction, board, x, y)
		self.deltas = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,1),(-1,-1),(1,-1)]
		self.score = score

	def __str__(self):
		return "Q" + self.color[0]

			
	def getPossibleActions(self):
		actionList = []
		for delta in self.deltas:
			for i in range(1,13,1):
				if self.board.empty(self.x + delta[0] * i, self.y + delta[1] * i):
					actionList.append((self.x + delta[0] * i, self.y + delta[1] * i, False))
				elif self.board.unusable(self.color, self.x + delta[0] * i, self.y + delta[1] * i):
					break
				elif self.board.ownPiece(self.color, self.x + delta[0] * i, self.y + delta[1] * i):
					actionList.append((self.x + delta[0] * i, self.y + delta[1] * i, True))
					break
				else:
					actionList.append((self.x + delta[0] * i, self.y + delta[1] * i, False))
					break
		return actionList

'''
King piece that can move 1 square in any direction. It cannot be checkmated,
it actually has to be captured. Castling is commented out from its possible
moves as it has a different form than other moves and messes with our 
dynamic feature calculation.
'''
class KING(PIECE):
	def __init__(self, color, direction, board, x, y):
		PIECE.__init__(self, color, direction, board, x, y)
		self.deltas = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,1),(-1,-1),(1,-1)]
		self.score = 20

	def __str__(self):
		return "K" + self.color[0]


	def getPossibleActions(self):
		actionList = []
		for delta in self.deltas:
			if self.board.empty(self.x + delta[0], self.y + delta[1]):
				actionList.append((self.x + delta[0], self.y + delta[1],False))
			elif self.board.unusable(self.color, self.x + delta[0], self.y + delta[1]):
				continue
			elif self.board.ownPiece(self.color, self.x + delta[0], self.y + delta[1]):
				actionList.append((self.x + delta[0], self.y + delta[1],True))
			else:
				actionList.append((self.x + delta[0], self.y + delta[1],False))
		'''
		if not self.hasMoved:
			if self.direction == 'North':
				if self.board.empty(self.x, self.y - 1) and self.board.empty(self.x, self.y - 2) and self.board.empty(self.x, self.y - 3) and not self.board.empty(self.x, self.y-4):
					if not self.board.board[self.x][self.y-4].hasMoved and str(self.board.board[self.x][self.y-4])[0] == "R":
						actionList.append(('Castle Queenside', self.x, self.y - 2, self.x, self.y-4, self.x, self.y-1))
				if self.board.empty(self.x, self.y + 1) and self.board.empty(self.x, self.y + 2) and not self.board.empty(self.x, self.y+3):
					if not self.board.board[self.x][self.y+3].hasMoved and str(self.board.board[self.x][self.y+3])[0] == "R":
						actionList.append(('Castle Kingside', self.x, self.y + 2, self.x, self.y+3, self.x, self.y+1))
			elif self.direction == 'South':
				if self.board.empty(self.x, self.y + 1) and self.board.empty(self.x, self.y + 2) and self.board.empty(self.x, self.y + 3) and not self.board.empty(self.x, self.y+4):
					if not self.board.board[self.x][self.y+4].hasMoved and str(self.board.board[self.x][self.y+4])[0] == "R":
						actionList.append(('Castle Queenside', self.x, self.y + 2, self.x, self.y+4, self.x, self.y+1))
				if self.board.empty(self.x, self.y - 1) and self.board.empty(self.x, self.y - 2) and not self.board.empty(self.x, self.y-3):
					if not self.board.board[self.x][self.y-3].hasMoved and str(self.board.board[self.x][self.y-3])[0] == "R":
						actionList.append(('Castle Kingside', self.x, self.y - 2, self.x, self.y-3, self.x, self.y-1))
			elif self.direction == 'East':
				if self.board.empty(self.x+1, self.y) and self.board.empty(self.x+2, self.y) and self.board.empty(self.x+3, self.y) and not self.board.empty(self.x+4, self.y):
					if not self.board.board[self.x+4][self.y].hasMoved and str(self.board.board[self.x+4][self.y])[0] == "R":
						actionList.append(('Castle Queenside', self.x+2, self.y, self.x+4, self.y, self.x+1, self.y))
				if self.board.empty(self.x-1, self.y) and self.board.empty(self.x-2, self.y) and not self.board.empty(self.x-3, self.y):
					if not self.board.board[self.x-3][self.y].hasMoved and str(self.board.board[self.x-3][self.y])[0] == "R":
						actionList.append(('Castle Kingside', self.x-2, self.y, self.x-3, self.y, self.x-1, self.y))
			elif self.direction == 'West':	
				if self.board.empty(self.x-1, self.y) and self.board.empty(self.x-2, self.y) and self.board.empty(self.x-3, self.y) and not self.board.empty(self.x-4, self.y):
					if not self.board.board[self.x-4][self.y].hasMoved and str(self.board.board[self.x-4][self.y])[0] == "R":
						actionList.append(('Castle Queenside', self.x-2, self.y, self.x-4, self.y, self.x-1, self.y))
				if self.board.empty(self.x+1, self.y) and self.board.empty(self.x+2, self.y) and not self.board.empty(self.x+3, self.y):
					if not self.board.board[self.x+3][self.y].hasMoved and str(self.board.board[self.x+3][self.y])[0] == "R":
						actionList.append(('Castle Kingside', self.x+2, self.y, self.x+3, self.y, self.x+1, self.y))
		'''
		return actionList
