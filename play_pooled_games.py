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
The main function of the file. Runs 20 games at once using multiprocessing
'''
def main():
	p = Pool(20)
	weights1 = [1.6793325000000001, 1.5973866250000002, 0.0815137, 0.045278125, 0.48488637500000004, 0.29009375000000004, 0.014928424999999999, 1.82054375]
	weights2 = [1.75,1.75,.1,.04,.5,.3,.01,2]
	weights3 = [1.5,1.5,.1,.04,.5,.3,.01,2]
	weights4 = [.5,.75,.07,.04,.5,.25,.015,1]
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
		gameAgents.append(False)
		agents.append(gameAgents)
	randoms.append(gameBoard)
	print(p.map(play_game.playGame, agents))
main()