# Centralized and Decentralized Multi-Agent Reinforcement Learning (MARL)

This project is intended for the Master's final thesis - the University of Groningen - Artificial Intelligence and Robotic.

```
__author__ = 'Hirad Emami Alagha - s3218139'

```
##World
```
def __init__(self,argCreationMode)

def loadWolrd(self,argName)

def saveWorld(self,argWorldName)

def generate_random_world(self)

def createWorld(self,argWidth,argHeigth, argObstacleList, argAgentList, goalList,argAgent_Location_Constraint=True)

def place_agents(self,argMargine_constraint=True)

def move_up(self,argPlayer)
def move_down(self,argPlayer)
def move_left(self,argPlayer)
def move_right(self,argPlayer)
def find_object_index(self,object,list)


```