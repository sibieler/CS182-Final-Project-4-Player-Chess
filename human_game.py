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
	humans = [ags.HUMAN('Yellow', 'South', gameBoard), ags.HUMAN('Green', 'West', gameBoard), ags.HUMAN('Red', 'North', gameBoard), ags.HUMAN('Blue', 'East', gameBoard), gameBoard, True]
	play_game.playGame(humans)

main()