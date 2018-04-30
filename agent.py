__author__ = 'Hirad Emami Alagha - s3218139'

from copy import copy
import numpy as np
import network as network
import sys, random

class agent():
    def __init__(self,argId):
        self.positionX=0
        self.positionY=0
        self.id = argId
        self.mode="train"
        #the State of the player can be:
        #   1) "Finished"
        self.state=""

