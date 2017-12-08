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
	humans = [ags.HUMAN('Yellow', 'South', gameBoard), ags.MINIMAX('Green','West', gameBoard, 1, 1, True, 3, [1.6793325000000001, 1.5973866250000002, 0.0815137, 0.045278125, 0.48488637500000004, 0.29009375000000004, 0.014928424999999999, 1.82054375]), ags.PROBGREEDY('Red','North', gameBoard, 2, [1.6793325000000001, 1.5973866250000002, 0.0815137, 0.045278125, 0.48488637500000004, 0.29009375000000004, 0.014928424999999999, 1.82054375]), ags.EXPECTIMAX('Blue','East', gameBoard, 1, 3, True, 3, [1.6793325000000001, 1.5973866250000002, 0.0815137, 0.045278125, 0.48488637500000004, 0.29009375000000004, 0.014928424999999999, 1.82054375]), gameBoard, True]
	play_game.playGame(humans)

main()