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


def main():
	p = Pool(20)
	weights = [1.6793325000000001, 1.5973866250000002, 0.0815137, 0.045278125, 0.48488637500000004, 0.29009375000000004, 0.014928424999999999, 1.82054375]
	gameBoard = board.BOARD()
	agentTypes = ["Minimax", "Expectimax", "Greedy", "ProbGreedy"]
	#expectimaxes = [EXPECTIMAX('Yellow','South', gameBoard,1,0,True,3,weights), EXPECTIMAX('Green','West', gameBoard,1,1,True,3,weights), EXPECTIMAX('Red','North', gameBoard,1,2,True,3,weights), EXPECTIMAX('Blue','East', gameBoard,1,3,True,3,weights)]
	#minimaxes = [MINIMAX('Yellow','South', gameBoard,1,0,True,3,weights), MINIMAX('Green','West', gameBoard,1,1,True,3,weights), MINIMAX('Red','North', gameBoard,1,2,True,3,weights), MINIMAX('Blue','East', gameBoard,1,3,True,3,weights)]
	agents = []
	for i in range(20):
		gameAgents = []
		random.shuffle(agentTypes)
		for j in range(4):
			if agentTypes[j] == "Minimax":
				gameAgents.append(ags.MINIMAX(gameBoard.colors[j],gameBoard.directions[j], gameBoard, 1, j, True, 3, weights))
			elif agentTypes[j] == "Expectimax":
				gameAgents.append(ags.EXPECTIMAX(gameBoard.colors[j],gameBoard.directions[j], gameBoard, 1, j, True, 3, weights))
			elif agentTypes[j] == "ProbGreedy":
				gameAgents.append(ags.PROBGREEDY(gameBoard.colors[j],gameBoard.directions[j], gameBoard, j, weights))
			else:
				gameAgents.append(ags.GREEDY(gameBoard.colors[j],gameBoard.directions[j], gameBoard, j, weights))
		gameAgents.append(copy.deepcopy(gameBoard))
		gameAgents.append(False)
		agents.append(gameAgents)
	print(p.map(play_game.playGame, agents))
main()