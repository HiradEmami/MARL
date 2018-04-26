__author__ = 'Hirad Emami Alagha - s3218139'

class agent():
    def __init__(self,argId):
        self.positionX=0
        self.positionY=0
        self.id = argId
        #the State of the player can be:
        #   1) "Finished"
        self.state=""