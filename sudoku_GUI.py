# Importing some important libraries
import pygame
from solver import *   
import time
import generator as gen

# Initialising pygame window
pygame.init()
win = pygame.display.set_mode((540,600))

# Loading Images and Musics.
poster = pygame.image.load("resources/poster.jpg")
code_loop = pygame.image.load("resources/code_loop.jpg")
thanks = pygame.image.load("resources/thanks.jpg")
the_as8_org = pygame.image.load("resources/the_as8_org.jpg")
solved = pygame.image.load("resources/solved.jpg")

buzz = pygame.mixer.Sound("resources/buzzer.wav")
music = pygame.mixer.music.load("resources/music.mp3")
pygame.mixer.music.play(-1)


# A function to display pictures in the screen for certain time.
def screen_timer(win,time,slide,clock):
    i = 0
    while i < time+1:
        clock.tick(60)
        win.blit(slide, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        i += 1
        pygame.display.update()

# Grid class represents the board
class Grid:
    # Initial board 
    board = gen.gen()
    solved_board = solve_extreme(board)

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]


    # finally, place the probable number to the board
    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if valid(self.model, val, (row,col)) and solve(self.model):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    # sketch the propbable number to the board
    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    # Draw the board
    def draw(self, win):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (27,73,179), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(win, (27, 73, 179), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)


    # Select the cube
    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    # clear the sketched number
    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    # return the cubes position after mouse click
    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    # return True if the board is finished
    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True


# Represent Each cube
class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width ,height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    # Draw the cube
    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)

    # set the value
    def set(self, val):
        self.value = val

    # set the value temporarily
    def set_temp(self, val):
        self.temp = val


# redraw the game window after each iteration of the main loop
def redraw_window(win, board, time, strikes):
    win.fill((225,225,225))
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(time), 1, (0,0,0))
    win.blit(text, (540 - 160, 560))
    # Draw Strikes
    text = fnt.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 560))
    # Draw grid and board
    board.draw(win)

# format the time for timer
def format_time(secs):
    sec = secs%60
    minute = secs//60

    mat = " " + str(minute) + ":" + str(sec)
    return mat



# Main loop
def main():
    pygame.display.set_caption("SUDOKU")
    clock = pygame.time.Clock()
    screen_timer(win,100,poster,clock)
    board = Grid(9, 9, 540, 540)
    key = None
    run = True
    start = time.time()
    strikes = 0
    while run:

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                            buzz.play()
                        key = None

                        if board.is_finished():
                            print("Game over")
                            time.sleep(1)
                            screen_timer(win,100,solved,clock)
                            screen_timer(win,100,thanks,clock)
                            screen_timer(win,150,code_loop,clock)
                            screen_timer(win,200,the_as8_org,clock)
                            screen_timer(win,150,poster,clock)
                            pygame.quit()
                            run = False
                            break 

                if event.key == pygame.K_SPACE: # For Cheat in the game
                    i, j = board.selected
                    key = board.solved_board[i][j]
                           



            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()


main()
pygame.quit()
