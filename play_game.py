import random
import math
import os
import time
import numpy as np
import copy
from multiprocessing import Pool
import board
import agents as ags

'''
This function can be called on any set of 4 agents with proper color and direction ordering. 
It will play out an entire game up to 50 moves each with those agents.
'''
def playGame(agents):
	#print agents
	startTime = time.time()
	moves = 0
	gameBoard = copy.deepcopy(agents[4])
	debug = agents[5]
	agents = agents[:4]
	while sum(gameBoard.kingCapped) <= 2:
		print moves
		moves += 1
		for i in range(len(agents)):
			#print i
			if gameBoard.kingCapped[i] == 0:
				time.sleep(0)
				#os.system('cls' if os.name == 'nt' else 'clear')
				#print "Yellow Score: " + str(gameBoard.scores[0])
				#print "Green Score: " + str(gameBoard.scores[1])
				#print "Red Score: " + str(gameBoard.scores[2])
				#print "Blue Score: " + str(gameBoard.scores[3])
				#print gameBoard.closestPawn
				#print gameBoard.totalPawnMoves
				#print gameBoard.legalMoveCount
				#print gameBoard.piecesAttacked
				#print gameBoard.undefendedPiecesAttacked
				if debug:
					gameBoard.printBoard()
				sorted_scores = list(reversed(sorted(gameBoard.scores)))
				#print sorted_scores
				agents[i].updateBoard(gameBoard)
				toMove = agents[i].getMove(gameBoard)
				gameBoard.move(toMove,i)
				if sum(gameBoard.kingCapped) >= 3 or (sum(gameBoard.kingCapped) == 2 and (sorted_scores[0] - sorted_scores[1]) > 20) or moves > 50:
					endTime = time.time()
					#os.system('cls' if os.name == 'nt' else 'clear')
					#print "Final Board:"
					#gameBoard.printBoard()
					#print "Final Score:"
					#print "   Yellow Score: " + str(gameBoard.scores[0])
					#print "   Green Score: " + str(gameBoard.scores[1])
					#print "   Red Score: " + str(gameBoard.scores[2])
					#print "   Blue Score: " + str(gameBoard.scores[3])
					maxScore = 0
					maxColor = ""
					maxAgent = None
					for j in range(len(gameBoard.scores)):
						if gameBoard.scores[j] >= maxScore:
							maxScore = gameBoard.scores[j]
							maxColor = gameBoard.colors[j]
							maxAgent = agents[j]
					#print "Winner, Winner, Chicken Dinner: " + maxColor
					if isinstance(maxAgent, ags.RANDOM):
						return (maxColor, gameBoard.scores, agents, moves, endTime - startTime)
					else:
						return (maxColor, gameBoard.scores, agents, maxAgent.weights, moves, endTime - startTime)