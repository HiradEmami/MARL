__author__='Hirad Emami Alagha - S3218139'


class obstacle():
    def __init__(self,argType,argWidth, argHight, argX,argY, argId):
        self.type = argType
        self.width = argWidth
        self.height = argHight
        self.x = argX
        self.y = argY
        self.id = argId

class goal():
    def __init__(self,argColor,argWidth, argHight, argX,argY, argId):
        self.color = argColor
        self.width = argWidth
        self.height = argHight
        self.x = argX
        self.y = argY
        self.id = argId
        self.num_agent= 0

    def set_new_position(self,argX,argY):
        self.x= argX
        self.y = argY

    def increment_agents(self):
        self.num_agent += 1



