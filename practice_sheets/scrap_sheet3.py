import numpy as np




def take_patch(argBoard):
    marginx=(int)((visionX-1)/2)
    marginY=(int)((visionY-1)/2)

    y0=max(0,positionY-marginY)
    y1=min(len(argBoard), positionY + marginY+1)
    x0=max(0,positionX-marginx)
    x1=min(len(argBoard[0]), positionX + marginx+1)
    print(marginx,marginY)
    print(y0,y1,x0,x1)

    return argBoard[y0:y1,x0:x1]

a =np.zeros((10,10),dtype=int)
count=1
for i in range(len(a)):
    for j in range(len(a[0])):
        a[i][j]=count
        count +=1

positionX=5
positionY=5

visionX=3
visionY=5

print(a)

print(take_patch(a))


#Test 2 - Size of flatten board


visionY=10
visionX=10

positionX=4
positionY=4

print(take_patch(a))



mode = "init"
state = "jav"

if not(mode=="testing") and (state=="jav"):
    print("kir")