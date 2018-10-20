def pad_grid( argboard, width_board, height_board):
    left_right = "center"
    top_bottom = "center"
    if positionX == 0:
        left_right = "left"
        argboard = pad_left(argboard)
    elif positionX == width_board - 1:
        left_right = "right"
        argboard = pad_right(argboard)
    if positionY == 0:
        top_bottom = "top"
        argboard = pad_top(argboard)

    elif positionY == height_board - 1:
        top_bottom = "bottom"
        argboard = pad_bottom(argboard)
    return argboard


def pad_grid_seven( argboard, width_board, height_board):
    left_right = "center"
    top_bottom = "center"
    if positionX == 0:
        left_right = "left_3"
        argboard = pad_left(argboard)
        argboard = pad_left(argboard)
        argboard = pad_left(argboard)
    elif positionX ==  1:
        left_right = "left_2"
        argboard = pad_left(argboard)
        argboard = pad_left(argboard)
    elif positionX == 2:
        left_right = "left_1"
        argboard = pad_left(argboard)
    elif positionX == width_board - 1:
        left_right = "right_3"
        argboard = pad_right(argboard)
        argboard = pad_right(argboard)
        argboard = pad_right(argboard)
    elif positionX == width_board - 2:
        left_right = "right_2"
        argboard = pad_right(argboard)
        argboard = pad_right(argboard)
    elif positionX == width_board - 3:
        left_right = "right_1"
        argboard = pad_right(argboard)

    if positionY == 0:
        top_bottom = "top_3"
        argboard = pad_top(argboard)
        argboard = pad_top(argboard)
        argboard = pad_top(argboard)
    elif positionY == 1:
        top_bottom = "top_2"
        argboard = pad_top(argboard)
        argboard = pad_top(argboard)
    elif positionY == 2:
        top_bottom = "top_1"
        argboard = pad_top(argboard)
    elif positionY == height_board - 1:
        top_bottom = "bottom_3"
        argboard = pad_bottom(argboard)
        argboard = pad_bottom(argboard)
        argboard = pad_bottom(argboard)
    elif positionY == height_board - 2:
        top_bottom = "bottom_2"
        argboard = pad_bottom(argboard)
        argboard = pad_bottom(argboard)
    elif positionY == height_board - 3:
        top_bottom = "bottom_1"
        argboard = pad_bottom(argboard)
    print(left_right,top_bottom)
    return argboard


def pad_left( argboard):
    new_board = []
    for i in range(len(argboard)):
        new_col = []
        new_col.append(pad_value)
        for j in range(len(argboard[0])):
            new_col.append(argboard[i][j])
        new_board.append(new_col)
    return new_board


def pad_top( argboard):
    new_board = []
    top_row = []
    for i in range(vision_x):
        top_row.append(pad_value)
    new_board.append(top_row)
    for i in range(len(argboard)):
        new_row = []
        for j in range(len(argboard[0])):
            new_row.append(argboard[i][j])
        new_board.append(new_row)
    return new_board


def pad_bottom( argboard):
    new_board = []
    bottom_row = []
    for i in range(vision_x):
        bottom_row.append(pad_value)

    for i in range(len(argboard)):
        new_row = []
        for j in range(len(argboard[0])):
            new_row.append(argboard[i][j])
        new_board.append(new_row)
    new_board.append(bottom_row)
    return new_board


def pad_right( argboard):
    new_board = []
    for i in range(len(argboard)):
        new_col = []
        for j in range(len(argboard[0])):
            new_col.append(argboard[i][j])
        new_col.append(pad_value)
        new_board.append(new_col)
    return new_board

def set_margines():
    marginx = (int)((vision_x - 1) / 2)
    marginY = (int)((vision_y - 1) / 2)
    return  marginx,marginY

# update_the vision of player
def get_observable_board(argBoard):
    # if we are using developer mode we only return the entire board
    if mode =="developer":
        return argBoard
    else:
        # calculating the boundaries
        y0 = max(0, positionY - marginY)
        y1 = min(len(argBoard), positionY + marginY + 1)
        x0 = max(0, positionX - marginx)
        x1 = min(len(argBoard[0]), positionX + marginx + 1)
        # calculating the boundaries
        observed= slice_list(arglist=argBoard,x0=x0,x1=x1,y0=y0,y1=y1)
        if vision_x == 3:
            observed = pad_grid(argboard=observed, width_board=len(argBoard[0]), height_board=len(argBoard))
        else:
            observed = pad_grid_seven(argboard=observed, width_board=len(argBoard[0]), height_board=len(argBoard))
        return observed

def slice_list(arglist,x0,x1,y0,y1):
    sliced_list=[]
    for i in range(y0,y1):
        new_row=[]
        for j in range(x0,x1):
            new_row.append(arglist[i][j])
        sliced_list.append(new_row)
    return sliced_list


def print_grid(gr):
    for i in range(len(gr)):
        p=[]
        for j in range(len(gr[0])):
            p.append(gr[i][j])
        print(p)


width = 10
height = 10

Grid = []
for i in range(height):
    temp = []
    for j in range(width):
        temp.append(0)
    Grid.append(temp)

mode ="notdeveloper"
vision_y=vision_x =7
marginx, marginY= set_margines()
pad_value = -8
positionX =width-4
positionY = height-4




print("Grid:")


Grid[positionY][positionX]= 1

Grid[2][2]= 2

print_grid(Grid)

t = get_observable_board(Grid)
print_grid(t)
print(len(t),len(t[0]))



for i in range(1,11):
    print(i)