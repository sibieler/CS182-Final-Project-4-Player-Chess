import random
import math
import os
import time
import numpy as np
import copy
from multiprocessing import Pool
import board
import agents as ags
import play_game

'''
The main function of the file. Runs a random game.
'''
def main():
	p = Pool(20)
	weights1 = [.8,1,.017,.025,.4,.25,.028,2]
	weights2 = [.6,.67,.083,.125,1,1.25,.14,1.5]
	weights3 = [.6,1.33,.017,.025,.07,.25,.028,2.5]
	weights4 = [.6,1,.033,.05,.8,.5,.057,2]
	weights = [weights1,weights2,weights3,weights4]
	gameBoard = board.BOARD()
	#expectimaxes = [EXPECTIMAX('Yellow','South', gameBoard,1,0,True,3,weights), EXPECTIMAX('Green','West', gameBoard,1,1,True,3,weights), EXPECTIMAX('Red','North', gameBoard,1,2,True,3,weights), EXPECTIMAX('Blue','East', gameBoard,1,3,True,3,weights)]
	#minimaxes = [MINIMAX('Yellow','South', gameBoard,1,0,True,3,weights), MINIMAX('Green','West', gameBoard,1,1,True,3,weights), MINIMAX('Red','North', gameBoard,1,2,True,3,weights), MINIMAX('Blue','East', gameBoard,1,3,True,3,weights)]
	randoms = [ags.RANDOM('Yellow', 'South', gameBoard), ags.RANDOM('Green', 'West', gameBoard), ags.RANDOM('Red', 'North', gameBoard), ags.RANDOM('Blue', 'East', gameBoard)]
	agents = []
	for i in range(20):
		gameAgents = []
		random.shuffle(weights)
		for j in range(4):
			gameAgents.append(ags.MINIMAX(gameBoard.colors[j],gameBoard.directions[j], gameBoard, 1, j, True, 3, weights[j]))
		gameAgents.append(copy.deepcopy(gameBoard))
		agents.append(gameAgents)
	randoms.append(gameBoard)
	randoms.append(True)
	print(p.map(play_game.playGame, [randoms]))
main()