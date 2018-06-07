import numpy as np
from tkinter import *
import system_utility


test= np.zeros((15,15),dtype=int)
argWorldName="sr"
outputDirect =str(argWorldName)+" "+str(argWorldName)+"s "
splited=outputDirect.split(" ")
print(splited)
print(splited[1])

counter=0;
for i in range(len(test)):
    for j in range(len(test[0])):
        test[i,j]=counter
        counter+=1

print(test)
print(test[0:2,0:2])
s=sum(sum(test[0:2,0:2]))
print(s)
print("fuck")


#       List[a:b] gives you all elements from a to b in List, but not including b
#       List[:4] gives you all elements up to the fifth
#       List[:-1] gives you everything in the list except the last one
#       This is because List[-1] gives you the last element in the list, List[-2] gives you the second last element and so on
#       List[:] just gives you all the elements in the list


def render():
    for i in range(height):
        for j in range(width):
            print("fart")

            frame.create_rectangle(i *height, j * width, (i + 1) * height, (j + 1) * width,
                                        fill="white", width=1)

master = Tk()
height = 10
width = 10
frame_widthScale, frame_heightScale = system_utility.calculateTheScale(height,width)
frame = Canvas(master, width=width * frame_widthScale,height=height * frame_heightScale)
render()
frame.grid(row=0, column=0)
master.mainloop()


