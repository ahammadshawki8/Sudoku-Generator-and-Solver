# In this series we will use backtracking problem to solve a very common and popular game sudoku.
# We will first learn what backtracing is, how that works and why it is very powerful algorithm?
# And then we will write the main code and also implement GUI using pygame.

# suppose we have a sudoku
# the common way to solve this is to use every pssible combination for each place.
# that is very much time-killing. It is called naive algorithm.

# but backtracking is fast enough.
# what we need to do is that-
    # 1. pick empty place
    # 2. try all numbers
    # 3. find a suitable number 
    # if success:
        # 4. repeat
    # else:
        # 4. backtrack
            # 4_A. Erase current and previous place
            # 4_B. continue from previous place



# Now lets code
# First we have here an initial board with is a multi-dimentional array (list)
board = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]

# First we will have a function that will give a nice representation of the board
def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")

print_board(board)

# Then we will have another function which will find empty places for us.
def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col

    return None