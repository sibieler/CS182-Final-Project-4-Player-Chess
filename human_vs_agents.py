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
	gameBoard = board.BOARD()
	humans = [ags.HUMAN('Yellow', 'South', gameBoard), ags.MINIMAX('Green','West', gameBoard, 1, 1, True, 3, [.8,1,.017,.025,.4,.25,.028,2]), ags.RANDOM('Red', 'North', gameBoard), ags.EXPECTIMAX('Blue','East', gameBoard, 1, 3, True, 3, [.8,1,.017,.025,.4,.25,.028,2]), gameBoard, True]
	play_game.playGame(humans)

main()