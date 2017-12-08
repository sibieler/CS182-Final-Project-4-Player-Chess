import random
import math
import os
import time
import numpy as np
import copy
import pieces
from pieces import ROOK
from pieces import KNIGHT
from pieces import BISHOP
from pieces import QUEEN
from pieces import KING
from pieces import PAWN
from multiprocessing import Pool
'''
Board class. This is where a majority of the information about the game is explored
and how the agents are able to evaluate their positions. Boards contain
dynamically updated arrays of all of the relevant features of the position.
These include the scores of the players, the players remaining, the points remaining
for each player, a dictionary of each players pieces to the number of pieces protecting it
and their value, the distance of the closest pawn to queening, the total distance of pawns
from queening and the number of pawns left, the number of legal moves, the number of 
undefended pieces attacked and their values and the number of pieces attacked and their
values.
'''
class BOARD:
	def __init__(self):
		self.scores = [0,0,0,0]
		self.colors = ["Yellow", "Green", "Red", "Blue"]
		self.directions = ["South", "West", "North", "East"]
		self.kingCapped = [0, 0, 0, 0]
		self.pointsRemaining = [59,59,59,59]
		self.pointsNotProtected = {"Blue": {}, "Red": {}, "Green": {}, "Yellow": {}}
		self.closestPawn = [6,6,6,6]
		self.totalPawnMoves = [(8,48),(8,48),(8,48),(8,48)]
		self.legalMoveCount = [20,20,20,20]
		self.undefendedPiecesAttacked = [(0,0),(0,0),(0,0),(0,0)]
		self.piecesAttacked = [(0,0),(0,0),(0,0),(0,0)]
		'''
		The row functions are designed to initialize the correct board 
		for a four player chess game.
		'''
		def createBackRow(direction, row):
			if direction == 'North':
				return [-1,-1,-1,-1,-1,ROOK('Red','North',self,5,row), KNIGHT('Red','North',self,6,row), BISHOP('Red','North',self,7,row), QUEEN('Red','North',self,8,row), KING('Red','North',self,9,row), BISHOP('Red','North',self,10,row), KNIGHT('Red','North',self,11,row),ROOK('Red','North',self,12,row),-1,-1,-1,-1,-1]
			else: 
				return [-1,-1,-1,-1,-1,ROOK('Yellow','South',self,5,row), KNIGHT('Yellow','South',self,6,row), BISHOP('Yellow','South',self,7,row), KING('Yellow','South',self,8,row), QUEEN('Yellow','South',self,9,row), BISHOP('Yellow','South',self,10,row), KNIGHT('Yellow','South',self,11,row),ROOK('Yellow','South',self,12,row),-1,-1,-1,-1,-1]
		def createFrontRow(color, direction, row2):
			row = []
			for i in range(5):
				row.append(-1)
			for i in range(8):
				row.append(PAWN(color, direction, self, i + 5, row2))
			for i in range(5):
				row.append(-1)
			return row
		def createMidRow(color1, direction1, color2, direction2, piece1, piece2, row2):
			row = [-1,-1]
			if piece1 == 'Rook':
				row.append(ROOK(color1, direction1, self, 2, row2))
			elif piece1 == 'Knight':
				row.append(KNIGHT(color1, direction1, self, 2, row2))
			elif piece1 == 'Bishop':
				row.append(BISHOP(color1, direction1, self, 2, row2))
			elif piece1 == 'Queen':
				row.append(QUEEN(color1, direction1, self, 2, row2))
			elif piece1 == 'King':
				row.append(KING(color1, direction1, self, 2, row2))
			row.append(PAWN(color1, direction1, self, 3, row2))
			for i in range(10):
				row.append(0)
			row.append(PAWN(color2, direction2, self, 14, row2))
			if piece2 == 'Rook':
				row.append(ROOK(color2, direction2, self, 15, row2))
			elif piece2 == 'Knight':
				row.append(KNIGHT(color2, direction2, self, 15, row2))
			elif piece2 == 'Bishop':
				row.append(BISHOP(color2, direction2, self, 15, row2))
			elif piece2 == 'Queen':
				row.append(QUEEN(color2, direction2, self, 15, row2))
			elif piece2 == 'King':
				row.append(KING(color2, direction2, self, 15, row2))
			row.append(-1)
			row.append(-1)
			return row

		self.board = [[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]]
		self.board.append([-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1])
		self.board.append(createBackRow('South',2))
		self.board.append(createFrontRow('Yellow', 'South',3))
		self.board.append([-1,-1,-1,-1,-1,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1])
		self.board.append(createMidRow('Blue', 'East', 'Green', 'West','Rook', 'Rook',5))
		self.board.append(createMidRow('Blue', 'East', 'Green', 'West','Knight', 'Knight',6))
		self.board.append(createMidRow('Blue', 'East', 'Green', 'West','Bishop', 'Bishop',7))
		self.board.append(createMidRow('Blue', 'East', 'Green', 'West','King', 'Queen',8))
		self.board.append(createMidRow('Blue', 'East', 'Green', 'West','Queen', 'King',9))
		self.board.append(createMidRow('Blue', 'East', 'Green', 'West','Bishop', 'Bishop',10))
		self.board.append(createMidRow('Blue', 'East', 'Green', 'West','Knight', 'Knight',11))
		self.board.append(createMidRow('Blue', 'East', 'Green', 'West','Rook', 'Rook',12))
		self.board.append([-1,-1,-1,-1,-1,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1])
		self.board.append(createFrontRow('Red', 'North',14))
		self.board.append(createBackRow('North',15))
		self.board.append([-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1])
		self.board.append([-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1])
		self.legalMoves = {}
		'''
		These following three loops initialize the features of the board so that they
		can later be dynamically updated.
		'''
		for i in range(18):
			for j in range(18):
				if self.board[i][j] == -1 or self.board[i][j] == 0:
					continue
				else:
					color = self.board[i][j].color
					if color in self.legalMoves:
						self.legalMoves[color][(i,j)] = self.board[i][j].getPossibleActions()
					else:
						self.legalMoves[color] = {}
						self.legalMoves[color][(i,j)] = self.board[i][j].getPossibleActions()
		self.piecesAttackDict = {}
		for color, pieces in self.legalMoves.iteritems():
			for piece, attacked in pieces.iteritems():
				for square in attacked:
					if (square[0],square[1]) in self.piecesAttackDict:
						self.piecesAttackDict[(square[0],square[1])].append((piece,color))
					else:
						self.piecesAttackDict[(square[0],square[1])] = [(piece,color)]
		for color, pieces in self.legalMoves.iteritems():
			for piece, attacked in pieces.iteritems():
				if piece in self.piecesAttackDict:
					pieceAttackers = self.piecesAttackDict[piece]
					attacking = 0
					for attacker in pieceAttackers:
						if color == attacker[1]:
							attacking += 1
						else:
							attacking -= 1
					self.pointsNotProtected[color][piece] = (attacking, self.board[piece[0]][piece[1]].score)
		self.pointsNotProtected["Yellow"][(2,5)] = (0, 5)
		self.pointsNotProtected["Yellow"][(2,12)] = (0, 5)
		self.pointsNotProtected["Green"][(5,15)] = (0, 5)
		self.pointsNotProtected["Green"][(12,15)] = (0, 5)
		self.pointsNotProtected["Red"][(15,12)] = (0, 5)
		self.pointsNotProtected["Red"][(15,5)] = (0, 5)
		self.pointsNotProtected["Blue"][(12,2)] = (0, 5)
		self.pointsNotProtected["Blue"][(5,2)] = (0, 5)
	'''
	Adds squares that a piece attacks to the dictionary of
	pieces and what they are attacked by.
	'''
	def legalMovesToAttack(self, xy, attacked, color):
		for square in attacked:
			if (square[0],square[1]) in self.piecesAttackDict:
				self.piecesAttackDict[(square[0],square[1])].append((xy,color))
			else:
				self.piecesAttackDict[(square[0],square[1])] = [(xy,color)]
	'''
	Checks if a given square contains a piece in it.
	'''
	def hasPiece(self,x,y):
		if not (self.board[x][y] == 0 or self.board[x][y] == -1):
			return True
		else:
			return False
	'''
	Gets the possible actions for a given color. Was used prior to our dynamic
	updating.
	'''
	def getPossibleActions(self, agentColor):
		actionList = {}
		for i in range(18):
			for j in range(18):
				if self.hasPiece(i,j):
					if self.pieceOwnership(i,j) == agentColor:
						if not self.board[i][j].getPossibleActions() == []:
							actionList[(i,j)] = self.board[i][j].getPossibleActions()
		return actionList
	'''
	If a piece is removed this function updates how many 
	points a given color now has left/
	'''
	def changePointsRemaining(self, color, value):
		for i in range(len(self.colors)):
			if self.colors[i] == color:
				self.pointsRemaining[i] -= value
	'''
	Evaluates the board based on some weighting of all the features
	'''
	def evalBoard(self, weights):
		evals = copy.deepcopy(self.scores)
		for i in range(len(evals)):
			evals[i] = evals[i] * weights[0]
			evals[i] += self.pointsRemaining[i] * weights[1]
			evals[i] += self.legalMoveCount[i] * weights[2]
			evals[i] += self.piecesAttacked[i][1] * weights[3]
			evals[i] += self.undefendedPiecesAttacked[i][1] * weights[4]
			evals[i] += (6-self.closestPawn[i]) * weights[5]
			evals[i] += (self.totalPawnMoves[i][0] * 6 - self.totalPawnMoves[i][1]) * weights[6]
			for piece, entry in self.pointsNotProtected[self.colors[i]].iteritems():
				if entry[0] < 0:
					evals[i] -= entry[1] * weights[7]
		return evals
	'''
	Checks which color owns a given square.
	'''
	def pieceOwnership(self,x,y):
		if self.hasPiece(x,y):
			return self.board[x][y].color
		else:
			return None
	'''
	Checks if the square is not in the board.
	'''
	def unusable(self,color, x, y):
		if self.board[x][y] == -1:
			return True
		else:
			return False
	'''
	Checks if a square has the same color as the given color.
	'''
	def ownPiece(self,color,x,y):
		if self.hasPiece(x,y):
			if self.pieceOwnership(x,y) == color:
				return True
		else:
			return False
	'''
	Checks if a square is empty.
	'''
	def empty(self,x,y):
		if self.board[x][y] == 0:
			return True
		else:
			return False
	'''
	Takes a board and a move and returns a copy of the old board with the
	new move on it and all of the updates done to the features.
	'''
	def generateSuccessor(self, movelst, agentNum):
		newBoard = copy.deepcopy(self)
		newBoard.move(movelst, agentNum)
		return newBoard
	'''
	Updates the move feature for any piece that was moved
	and the other related features.
	'''
	def updatePieceMovedMoves(self, xy_old, xy_new, color):
		oldMoves = copy.deepcopy(self.legalMoves[color][xy_old])
		for move in oldMoves:
			self.piecesAttackDict[(move[0],move[1])].remove((xy_old, color))
			if not self.empty(move[0],move[1]):
				affectedColor = self.board[move[0]][move[1]].color
				if (move[0], move[1]) in self.pointsNotProtected[affectedColor]:
					if affectedColor == color:
						self.pointsNotProtected[affectedColor][(move[0], move[1])] = (self.pointsNotProtected[affectedColor][(move[0], move[1])][0] - 1, self.pointsNotProtected[affectedColor][(move[0], move[1])][1])
					else:
						self.pointsNotProtected[affectedColor][(move[0], move[1])] = (self.pointsNotProtected[affectedColor][(move[0], move[1])][0] + 1, self.pointsNotProtected[affectedColor][(move[0], move[1])][1])
		del self.legalMoves[color][xy_old]
		newMoves = self.board[xy_new[0]][xy_new[1]].getPossibleActions()
		self.legalMoves[color][xy_new] = newMoves
		self.legalMovesToAttack(xy_new, newMoves, color)
		for move in newMoves:
			if not self.empty(move[0],move[1]):
				affectedColor = self.board[move[0]][move[1]].color
				if (move[0], move[1]) in self.pointsNotProtected[affectedColor]:
					if affectedColor == color:
						self.pointsNotProtected[affectedColor][(move[0], move[1])] = (self.pointsNotProtected[affectedColor][(move[0], move[1])][0] + 1, self.pointsNotProtected[affectedColor][(move[0], move[1])][1])
					else:
						self.pointsNotProtected[affectedColor][(move[0], move[1])] = (self.pointsNotProtected[affectedColor][(move[0], move[1])][0] - 1, self.pointsNotProtected[affectedColor][(move[0], move[1])][1])
	'''
	Returns the elements in lst1 that are not in lst2.
	'''
	def lstDiff(self, lst1, lst2):
		lst2 = set(lst2)
		return [x for x in lst1 if x not in lst2]
	'''
	Dynamically updates the features for all pieces that were affected by a piece
	moving from the xy square.
	'''
	def updateSquareFromAttackedMoves(self, xy):
		if xy in self.piecesAttackDict:
			piecesAffected = copy.deepcopy(self.piecesAttackDict[xy])
			for piece in piecesAffected:
				piececolor = piece[1]
				oldMoves = self.legalMoves[piececolor][(piece[0][0],piece[0][1])]
				xy2 = (piece[0][0],piece[0][1])
				for move in oldMoves:
					self.piecesAttackDict[(move[0],move[1])].remove((xy2, piececolor))
				newMoves = self.board[piece[0][0]][piece[0][1]].getPossibleActions()
				changedMoves = self.lstDiff(newMoves, oldMoves)
				for move in changedMoves:
					if not move[0] == "Castle Kingside" and not move[0] == "Castle Queenside":
						if not self.empty(move[0],move[1]):
							affectedColor = self.board[move[0]][move[1]].color
							if affectedColor == piececolor:
								if (move[0],move[1]) in self.pointsNotProtected[affectedColor]:
									self.pointsNotProtected[affectedColor][(move[0],move[1])] = (self.pointsNotProtected[affectedColor][(move[0],move[1])][0] + 1, self.pointsNotProtected[affectedColor][(move[0],move[1])][1])
								else:
									self.pointsNotProtected[affectedColor][(move[0],move[1])] = (1, self.board[move[0]][move[1]].score)
							else:
								if (move[0],move[1]) in self.pointsNotProtected[affectedColor]:
									self.pointsNotProtected[affectedColor][(move[0],move[1])] = (self.pointsNotProtected[affectedColor][(move[0],move[1])][0] - 1, self.pointsNotProtected[affectedColor][(move[0],move[1])][1])
								else:
									self.pointsNotProtected[affectedColor][(move[0],move[1])] = (-1, self.board[move[0]][move[1]].score)
				changedMoves2 = self.lstDiff(oldMoves, newMoves)
				for move in changedMoves2:
					if not move[0] == "Castle Kingside" and not move[0] == "Castle Queenside":
						if not self.empty(move[0],move[1]):
							affectedColor = self.board[move[0]][move[1]].color
							if affectedColor == piececolor:
								if (move[0],move[1]) in self.pointsNotProtected[affectedColor]:
									self.pointsNotProtected[affectedColor][(move[0],move[1])] = (self.pointsNotProtected[affectedColor][(move[0],move[1])][0] - 1, self.pointsNotProtected[affectedColor][(move[0],move[1])][1])
							else:
								if (move[0],move[1]) in self.pointsNotProtected[affectedColor]:
									self.pointsNotProtected[affectedColor][(move[0],move[1])] = (self.pointsNotProtected[affectedColor][(move[0],move[1])][0] + 1, self.pointsNotProtected[affectedColor][(move[0],move[1])][1])
				self.legalMoves[piececolor][(piece[0][0],piece[0][1])] = newMoves
				self.legalMovesToAttack(xy2, newMoves, piececolor)
		#else:
			#del self.pointsNotProtected[self.board[xy[0]][xy[1]].color][xy]
	'''
	Dynamically updates the features for all pieces that were affected by a piece
	moving to the xy square.
	'''
	def updateSquareToAttackedMoves(self, xy, xy_old):
		if xy in self.piecesAttackDict:
			piecesAffected = copy.deepcopy(self.piecesAttackDict[xy])
			for piece in piecesAffected:
				if not piece == xy_old:
					piececolor = piece[1]
					oldMoves = self.legalMoves[piececolor][(piece[0][0],piece[0][1])]
					xy2 = (piece[0][0],piece[0][1])
					for move in oldMoves:
						self.piecesAttackDict[(move[0],move[1])].remove((xy2, piececolor))
					newMoves = self.board[piece[0][0]][piece[0][1]].getPossibleActions()
					self.legalMoves[piececolor][(piece[0][0],piece[0][1])] = newMoves
					#print self.legalMoves[piececolor][(piece[0][0],piece[0][1])]
					self.legalMovesToAttack(xy2, newMoves, piececolor)
					#print oldMoves
					#print newMoves
					changedMoves = self.lstDiff(oldMoves, newMoves)
					changedMoves2 = self.lstDiff(newMoves, oldMoves)
					#print changedMoves
					for move in changedMoves:
						if not move[0] == "Castle Kingside" and not move[0] == "Castle Queenside":
							if not self.empty(move[0],move[1]):
								affectedColor = self.board[move[0]][move[1]].color
								if affectedColor == piececolor:
									if (move[0],move[1]) in self.pointsNotProtected[affectedColor]:
										self.pointsNotProtected[affectedColor][(move[0],move[1])] = (self.pointsNotProtected[affectedColor][(move[0],move[1])][0] - 1, self.pointsNotProtected[affectedColor][(move[0],move[1])][1])
								else:
									if (move[0],move[1]) in self.pointsNotProtected[affectedColor]:
										self.pointsNotProtected[affectedColor][(move[0],move[1])] = (self.pointsNotProtected[affectedColor][(move[0],move[1])][0] + 1, self.pointsNotProtected[affectedColor][(move[0],move[1])][1])
				else:
					print "Oops"
		else:
			self.pointsNotProtected[self.board[xy[0]][xy[1]].color][xy] = (0, self.board[xy[0]][xy[1]].score)

	'''
	Updates the protected pieces feature for the piece that was moved.
	'''
	def updateProtection(self, xy_old, xy_new, color):
		if xy_old in self.pointsNotProtected[color]:
			del self.pointsNotProtected[color][xy_old]
		pieceAttackers = self.piecesAttackDict[xy_new]
		attacking = 0
		for attacker in pieceAttackers:
			if color == attacker[1]:
				attacking += 1
			else:
				attacking -= 1
		self.pointsNotProtected[color][xy_new] = (attacking, self.board[xy_new[0]][xy_new[1]].score)

	'''
	Updates all necessary features when a piece is removed from the game.
	'''
	def removeCapturedPieces(self, xy, color):
		oldMoves = copy.deepcopy(self.legalMoves[color][xy])
		for move in oldMoves:
			self.piecesAttackDict[(move[0],move[1])].remove((xy, color))
			if not self.empty(move[0],move[1]):
				affectedColor = self.board[move[0]][move[1]].color
				if (move[0],move[1]) in self.pointsNotProtected[affectedColor]:
					if affectedColor == color:
						self.pointsNotProtected[affectedColor][(move[0],move[1])] = (self.pointsNotProtected[affectedColor][(move[0],move[1])][0]-1,self.pointsNotProtected[affectedColor][(move[0],move[1])][1])
					else:
						self.pointsNotProtected[affectedColor][(move[0],move[1])] = (self.pointsNotProtected[affectedColor][(move[0],move[1])][0]+1,self.pointsNotProtected[affectedColor][(move[0],move[1])][1])
		del self.legalMoves[color][xy]
	'''
	Perform a move on the board and update all features.
	'''
	def move(self,movelst,i):
		if not self.empty(movelst[2], movelst[3]):
			removedColor = self.board[movelst[2]][movelst[3]].color
			self.removeCapturedPieces((movelst[2],movelst[3]), removedColor)
			removedIndex = None
			self.changePointsRemaining(removedColor, self.board[movelst[2]][movelst[3]].score)
			del self.pointsNotProtected[removedColor][(movelst[2],movelst[3])]
			for j in range(len(self.colors)):
				if self.colors[j] == removedColor:
					removedIndex = j
			if str(self.board[movelst[2]][movelst[3]])[0] == "K":
				self.kingCapped[removedIndex] = 1
				self.scores[i] += self.board[movelst[2]][movelst[3]].score
			if str(self.board[movelst[0]][movelst[1]])[0] =="P":
				pawnDist = self.board[movelst[0]][movelst[1]].moves
				self.totalPawnMoves[removedIndex] = (self.totalPawnMoves[removedIndex][0]-1, self.totalPawnMoves[removedIndex][1]-(6-pawnDist))
			if self.kingCapped[removedIndex] == 0:
				self.scores[i] += self.board[movelst[2]][movelst[3]].score
		if str(self.board[movelst[0]][movelst[1]])[0] =="P":
			pawnColor = self.board[movelst[0]][movelst[1]].color
			pawnInd = None
			for j in range(len(self.colors)):
				if self.colors[j] == pawnColor:
					pawnInd = j
			pawnDist = self.board[movelst[0]][movelst[1]].moves
			deltaX = abs(movelst[0]-movelst[2])
			deltaY = abs(movelst[1]-movelst[3])
			distMoved = max([deltaX,deltaY])
			self.totalPawnMoves[pawnInd] = (self.totalPawnMoves[pawnInd][0], self.totalPawnMoves[pawnInd][1]-distMoved)
			if (8-pawnDist-distMoved) < self.closestPawn[pawnInd]:
				self.closestPawn[pawnInd] = 8 - pawnDist - distMoved
		self.board[movelst[2]][movelst[3]] = self.board[movelst[0]][movelst[1]]
		self.board[movelst[2]][movelst[3]].move(movelst[2],movelst[3])
		self.board[movelst[0]][movelst[1]] = 0
		self.updatePieceMovedMoves((movelst[0],movelst[1]),(movelst[2],movelst[3]), self.board[movelst[2]][movelst[3]].color)
		self.updateProtection((movelst[0],movelst[1]),(movelst[2],movelst[3]), self.board[movelst[2]][movelst[3]].color)
		self.updateSquareFromAttackedMoves((movelst[0],movelst[1]))
		self.updateSquareToAttackedMoves((movelst[2],movelst[3]), (movelst[0],movelst[1]))

		for i in range(len(self.colors)):
			legMovs = self.legalMoves[self.colors[i]]
			moveCount = 0
			piecesAttackCount = 0
			piecesAttackScore = 0
			undPiecesAttackCount = 0
			undPiecesAttackScore = 0
			for piece, moves in legMovs.iteritems():
				moveCount += len(moves)
				for j in range(len(self.colors)):
					if not i == j:
						piecesAttacking = [self.pointsNotProtected[self.colors[j]][(move[0],move[1])] for move in moves if (move[0],move[1]) in self.pointsNotProtected[self.colors[j]]]
						undefendedPiecesAttacked = [attacked[1] for attacked in piecesAttacking if attacked[0] < 0]
						piecesAttackCount += len(piecesAttacking)
						piecesAttackScore += sum([attacked[1] for attacked in piecesAttacking])
						undPiecesAttackCount += len(undefendedPiecesAttacked)
						undPiecesAttackScore += sum(undefendedPiecesAttacked)
			self.legalMoveCount[i] = moveCount
			self.piecesAttacked[i] = (piecesAttackCount, piecesAttackScore)
			self.undefendedPiecesAttacked[i] = (undPiecesAttackCount, undPiecesAttackScore)

		if len(movelst) == 8:
			self.board[movelst[6]][movelst[7]] = self.board[movelst[4]][movelst[5]]
			self.board[movelst[6]][movelst[7]].move(movelst[6],movelst[7])
			self.board[movelst[4]][movelst[5]] = 0
			self.updatePieceMovedMoves((movelst[4],movelst[5]),(movelst[6],movelst[7]), self.board[movelst[6]][movelst[7]].color)
			self.updateSquareFromAttackedMoves((movelst[4],movelst[5]))
			self.updateSquareToAttackedMoves((movelst[6],movelst[7]))

	'''
	Print the board in a fashion that makes it understandable.
	'''
	def printBoard(self):
		print("-" * 94)
		y_inds = "   |  "
		for i in range(18):
			if i < 9:
				y_inds += str(i) + " |  "
			else:
				y_inds += str(i) + " | "
		print(y_inds)
		print("-" * 94)
		for i in range(18):
			line = ""
			if i < 10:
				line += str(i) + "  | "
			else:
				line += str(i) + " | "
			for j in range(18):
				if self.board[i][j] == 0:
					line += "  " + " | "
				elif self.board[i][j] == -1:
					line += "  " + " | "
				else:
					line += str(self.board[i][j]) + " | "
			print(line)
			print("-" * 94)