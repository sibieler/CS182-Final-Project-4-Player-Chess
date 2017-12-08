import random
import math
import os
import time
import numpy as np
import copy
from multiprocessing import Pool
'''
Generic agent class. Used to populate the chess board with players and get their moves.
All agents must have access to their own color and direction, as well as the board that they 
are playing on.
'''
class AGENT():
	def __init__(self, color, direction, board):
		self.color = color
		self.direction = direction
		self.board = board
	def getPossibleActions(self):
		return self.board.legalMoves[self.color]

	def updateBoard(self, gameBoard):
		self.board = gameBoard
	
'''
Human Agent. Allows a human player to input moves into the game and play against any
combination of engines.
'''
class HUMAN(AGENT):
	def __init__(self, color, direction, board):
		AGENT.__init__(self, color, direction, board)
	'''
	Prompt input from the Human player and then use that as a move if it is legal.
	Otherwise re-prompt the player.
	'''
	def getMove(self,gameBoard):
		while(True):	
			#valid = True
			castle = raw_input("Are you castling (Y/N)?")
			if castle == "Y":
				king_x = int(input("What is King row?"))
				king_y = int(input("What is King column?"))
				side = raw_input("Kingside or Queenside (K/Q)?")
				possActs = self.getPossibleActions()
				if (king_x,king_y) in possActs:
					pieceActs = possActs[(king_x,king_y)]
					if side == "K":
						for act in pieceActs:
							if act[0] == "Castle Kingside":
								return [king_x, king_y, act[1], act[2], act[3], act[4], act[5], act[6]]
						valid = False
					elif side == "Q":
						for act in pieceActs:
							if act[0] == "Castle Queenside":
								return [king_x, king_y, act[1], act[2], act[3], act[4], act[5], act[6]]
			else:
				X1 = int(input("What is start row?"))
				Y1 = int(input("What is start column?"))
				X2 = int(input("What is end row?"))
				Y2 = int(input("What is end column?"))
				possActs = self.getPossibleActions()
				if (X1,Y1) in possActs:
					pieceActs = possActs[(X1,Y1)]
					if (X2,Y2,False) in pieceActs:
						return [X1,Y1,X2,Y2]

'''
Random agent designed for testing the legal moves features.
'''
class RANDOM(AGENT):
	def __init__(self, color, direction, board):
		AGENT.__init__(self, color, direction, board)

	'''
	Randomly pick a move from all of the agents legal moves.
	'''
	def getMove(self,gameBoard):
		while(True):
			possActs = self.getPossibleActions()
			randKey = random.choice(list(possActs))
			if len(possActs[randKey]) > 0:
				randAct = random.choice(possActs[randKey])
				if randAct[0] == "Castle Kingside" or randAct[0] == "Castle Queenside":
					return [randKey[0], randKey[1], randAct[1], randAct[2], randAct[3], randAct[4], randAct[5], randAct[6]]
				else:
					if not randAct[2]:
						return [randKey[0], randKey[1], randAct[0], randAct[1]]

'''
Minimax agent that has an additional boolean input that turns its minimax search into a beam
search in which it only expands the best beamsize nodes at every layer of the tree. It also
can take in an array of length 8 of weights that determines how important each factor of
the board evaluation function is.
'''
class MINIMAX(AGENT):
	def __init__(self, color, direction, board, depth, index, beam, beamsize, weights):
		AGENT.__init__(self, color, direction, board)
		self.depth = depth
		self.index = index
		self.colorlist = ["Yellow", "Green", "Red", "Blue"]
		self.beam = beam
		self.beamsize = beamsize
		self.weights = weights


	def getMove(self, gameBoard):
		'''
		High level Minimax recursion function, which calls the max value everytime
		because our evaluation is not zero sum and thus every player is simply maximizing
		their own score at a given board position.
		'''
		def value(self, gameBoard, depth, agentNum, action, curAgent):
			if depth == self.depth and agentNum == curAgent:
				return(gameBoard.evalBoard(self.weights), action)
			else:
				return max_value(self, gameBoard, depth, agentNum, curAgent)

		'''
		Iterate through all possible moves and order them by evaluation.
		If it is a beam search pick the topN moves and have the next opponent do the same.
		Return the max value of your moves.
		'''
		def max_value(self, gameBoard, depth, agentNum, curAgent):
			action = None
			val2 = [-1000,-1000,-1000,-1000]
			agentColor = self.colorlist[agentNum]
			agentActions = gameBoard.legalMoves[agentColor]
			if len(agentActions) == 0:
				return (gameBoard.evalBoard(self.weights), None)
			successorList = []
			for startPos, endPoses in agentActions.iteritems():
				for endPos in endPoses:
					if not endPos[2]:
						if not (endPos[0] == "Castle Kingside" or endPos[0] == "Castle Queenside"):
							successor = gameBoard.generateSuccessor([startPos[0],startPos[1],endPos[0],endPos[1]], agentNum)
							successorScore = successor.evalBoard(self.weights)[agentNum]
							successorAct = [startPos[0],startPos[1],endPos[0],endPos[1]]
							#print str(startPos) +"  " + str(endPos) + "  " + str(successorScore)
							successorList.append((successor, successorScore, successorAct))
			topN = list(reversed(sorted(successorList, key=lambda s: s[1])))
			if self.beam:
				topN = topN[:self.beamsize]
			for successor in topN:
				if agentNum == 3 and curAgent == 0:
					newVal = value(self, successor[0], depth+1, 0, successor[2], curAgent)[0]
				elif agentNum == 3:
					newVal = value(self, successor[0], depth, 0, successor[2], curAgent)[0]
				elif agentNum == curAgent-1:
					newVal = value(self, successor[0], depth+1, agentNum + 1, successor[2], curAgent)[0]
				else:
					newVal = value(self, successor[0], depth, agentNum + 1, successor[2], curAgent)[0]
				if val2[agentNum] < newVal[agentNum]:
					val2 = newVal
					action = successor[2]
				elif val2[agentNum] == newVal[agentNum] and random.random() < .5:
					val2 = newVal
					action = successor[2]
			return (val2, action)
		return value(self, gameBoard, 0, self.index, None, self.index)[1]

'''
Expectimax agent that has an additional boolean input that turns its expectimax search into a beam
search in which it only expands the best beamsize nodes at every layer of the tree. It also
can take in an array of length 8 of weights that determines how important each factor of
the board evaluation function is.
'''
class EXPECTIMAX(AGENT):
	def __init__(self, color, direction, board, depth, index, beam, beamsize, weights):
		AGENT.__init__(self, color, direction, board)
		self.depth = depth
		self.index = index
		self.colorlist = ["Yellow", "Green", "Red", "Blue"]
		self.beam = beam
		self.beamsize = beamsize
		self.weights = weights

	def getMove(self, gameBoard):
		'''
		High level Expectimax recursion function, which calls the max value for the agent playing
		and then exp value for the other players.
		'''
		def value(self, gameBoard, depth, agentNum, action, curAgent):
			if depth == self.depth and agentNum == curAgent:
				return(gameBoard.evalBoard(self.weights)[curAgent], action)
			elif agentNum == curAgent:
				return max_value(self, gameBoard, depth, agentNum, curAgent)
			else:
				return exp_value(self, gameBoard, depth, agentNum, curAgent)
		'''
		Iterate through all possible moves and order them by evaluation.
		If it is a beam search pick the topN moves and have the next opponent
		calculate the exp value of randomly picking between their moves.
		Return the max value of your moves.
		'''
		def max_value(self, gameBoard, depth, agentNum, curAgent):
			action = None
			val2 = -100000
			agentColor = self.colorlist[agentNum]
			agentActions = gameBoard.legalMoves[agentColor]
			if len(agentActions) == 0:
				return (gameBoard.evalBoard(self.weights)[curAgent], None)
			successorList = []
			for startPos, endPoses in agentActions.iteritems():
				for endPos in endPoses:
					if not endPos[2]:
						if not (endPos[0] == "Castle Kingside" or endPos[0] == "Castle Queenside"):
							successor = gameBoard.generateSuccessor([startPos[0],startPos[1],endPos[0],endPos[1]], agentNum)
							successorScore = successor.evalBoard(self.weights)[agentNum]
							successorAct = [startPos[0],startPos[1],endPos[0],endPos[1]]
							#print str(startPos) +"  " + str(endPos) + "  " + str(successorScore)
							successorList.append((successor, successorScore, successorAct))
			topN = list(reversed(sorted(successorList, key=lambda s: s[1])))
			if self.beam:
				topN = topN[:self.beamsize]
			for successor in topN:
				if agentNum == 3 and curAgent == 0:
					newVal = value(self, successor[0], depth+1, 0, successor[2], curAgent)[0]
				elif agentNum == 3:
					newVal = value(self, successor[0], depth, 0, successor[2], curAgent)[0]
				elif agentNum == curAgent-1:
					newVal = value(self, successor[0], depth+1, agentNum + 1, successor[2], curAgent)[0]
				else:
					newVal = value(self, successor[0], depth, agentNum + 1, successor[2], curAgent)[0]
				if val2 < newVal:
					val2 = newVal
					action = successor[2]
				elif val2 == newVal and random.random() < .5:
					val2 = newVal
					action = successor[2]
			return (val2, action)
		'''
		Iterate through all possible moves and order them by evaluation.
		If it is a beam search pick the topN moves and have the next opponent
		calculate the exp value of randomly picking between their moves or maximize value.
		Return the expected value of your moves.
		''' 
		def exp_value(self, gameBoard, depth, agentNum, curAgent):
			action = None
			val2 = [-1000,-1000,-1000,-1000]
			agentColor = self.colorlist[agentNum]
			agentActions = gameBoard.legalMoves[agentColor]
			if len(agentActions) == 0:
				return (gameBoard.evalBoard(self.weights)[curAgent], None)
			successorList = []
			for startPos, endPoses in agentActions.iteritems():
				for endPos in endPoses:
					if not endPos[2]:
						if not (endPos[0] == "Castle Kingside" or endPos[0] == "Castle Queenside"):
							successor = gameBoard.generateSuccessor([startPos[0],startPos[1],endPos[0],endPos[1]], agentNum)
							successorScore = successor.evalBoard(self.weights)[agentNum]
							successorAct = [startPos[0],startPos[1],endPos[0],endPos[1]]
							#print str(startPos) +"  " + str(endPos) + "  " + str(successorScore)
							successorList.append((successor, successorScore, successorAct))
			topN = list(reversed(sorted(successorList, key=lambda s: s[1])))
			expVal = 0.0
			if self.beam:
				topN = topN[:self.beamsize]
			for successor in topN:
				if agentNum == 3 and curAgent == 0:
					newVal = value(self, successor[0], depth+1, 0, successor[2], curAgent)[0]
				elif agentNum == 3:
					newVal = value(self, successor[0], depth, 0, successor[2], curAgent)[0]
				elif agentNum == curAgent-1:
					newVal = value(self, successor[0], depth+1, agentNum + 1, successor[2], curAgent)[0]
				else:
					newVal = value(self, successor[0], depth, agentNum + 1, successor[2], curAgent)[0]
				expVal += newVal
				action = successor[2]
			expVal /= len(topN)
			return (expVal, action)
		
		return value(self, gameBoard, 0, self.index, None, self.index)[1]

class GREEDY(AGENT):
	def __init__(self, color, direction, board, index, weights):
		AGENT.__init__(self, color, direction, board)
		self.index = index
		self.colorlist = ["Yellow", "Green", "Red", "Blue"]
		self.weights = weights


	def getMove(self, gameBoard):

		'''
		Iterate through all possible moves and order them by evaluation.
		If it is a beam search pick the topN moves and have the next opponent do the same.
		Return the max value of your moves.
		'''
		def value(self, gameBoard, agentNum):
			agentColor = self.colorlist[agentNum]
			agentActions = gameBoard.legalMoves[agentColor]
			successorList = []
			for startPos, endPoses in agentActions.iteritems():
				for endPos in endPoses:
					if not endPos[2]:
						if not (endPos[0] == "Castle Kingside" or endPos[0] == "Castle Queenside"):
							successor = gameBoard.generateSuccessor([startPos[0],startPos[1],endPos[0],endPos[1]], agentNum)
							successorScore = successor.evalBoard(self.weights)[agentNum]
							successorAct = [startPos[0],startPos[1],endPos[0],endPos[1]]
							#print str(startPos) +"  " + str(endPos) + "  " + str(successorScore)
							successorList.append((successor, successorScore, successorAct))
			topN = list(reversed(sorted(successorList, key=lambda s: s[1])))
			return (topN[0][2])
		return value(self, gameBoard, self.index)

class PROBGREEDY(AGENT):
	def __init__(self, color, direction, board, index, weights):
		AGENT.__init__(self, color, direction, board)
		self.index = index
		self.colorlist = ["Yellow", "Green", "Red", "Blue"]
		self.weights = weights


	def getMove(self, gameBoard):

		'''
		Iterate through all possible moves and order them by evaluation.
		If it is a beam search pick the topN moves and have the next opponent do the same.
		Return the max value of your moves.
		'''
		def value(self, gameBoard, agentNum):
			agentColor = self.colorlist[agentNum]
			agentActions = gameBoard.legalMoves[agentColor]
			successorList = []
			for startPos, endPoses in agentActions.iteritems():
				for endPos in endPoses:
					if not endPos[2]:
						if not (endPos[0] == "Castle Kingside" or endPos[0] == "Castle Queenside"):
							successor = gameBoard.generateSuccessor([startPos[0],startPos[1],endPos[0],endPos[1]], agentNum)
							successorScore = successor.evalBoard(self.weights)[agentNum]
							successorAct = [startPos[0],startPos[1],endPos[0],endPos[1]]
							#print str(startPos) +"  " + str(endPos) + "  " + str(successorScore)
							successorList.append((successor, successorScore, successorAct))
			topN = list(reversed(sorted(successorList, key=lambda s: s[1])))
			rand = random.random()
			if rand < .5:
				return (topN[0][2])
			elif rand >= .5 and rand < .75:
				return (topN[1][2])
			elif rand >= .75 and rand < .9:
				return (topN[2][2])
			elif rand >= .9 and rand < .975:
				return (topN[3][2])
			else:
				return (topN[4][2])
		return value(self, gameBoard, self.index)
