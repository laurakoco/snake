
import pygame
import random
import time
# import os

# define global variables
pygame.font.init()
myfont = pygame.font.SysFont('Arial', 15)

window_size_x = 400
window_size_y = 300

# define RGB color tuples
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
pink = (255, 20, 147)
purple = (153,50,204)

filename = "score.txt"

display = pygame.display.set_mode((window_size_x, window_size_y)) # define display, set window size

frames_per_second = 10  # define how many times display updates snake position per second ~ snake speed

class food:

    def __init__(self, color):

        self.__x_pos = 0
        self.__y_pos = 0
        self.color = color

        self.__block_size = 10

    def get_food_pos(self, window_size_x, window_size_y):

        self.__x_pos = random.randrange(0, window_size_x, 10)
        self.__y_pos = random.randrange(0, window_size_y, 10)

        return self.__x_pos, self.__y_pos

    def draw_food(self):

        pygame.draw.rect(display, self.color, [self.__x_pos, self.__y_pos, self.__block_size, self.__block_size]) # draw food

    def __repr__(self):
        return self.color

class snake:

    def __init__(self, color):
        self.__snake_head_x = window_size_x / 2 # snake head starting position
        self.__snake_head_y = window_size_y / 2

        self.block_size = 10
        self.color = color

        self.direction = 'n/a'
        self.__snake_len = 1
        self.__snake_list = []
        self.__snake_head = []

    def __increase_length(self): # increase length of snake
        self.__snake_len += 1

    def draw_snake(self): # draw snake
        for x in self.__snake_list:
            pygame.draw.rect(display, self.color, [x[0], x[1], self.block_size, self.block_size])

    def update_head_pos(self):
        x_move = 0
        y_move = 0
        if self.direction == 'up':
            x_move = 0
            y_move = -self.block_size
        if self.direction == 'down':
            x_move = 0
            y_move = self.block_size
        if self.direction == 'left': # left arrow
            x_move = -self.block_size
            y_move = 0
        if self.direction == 'right': # right arrow
            x_move = self.block_size
            y_move = 0

        self.__snake_head_x += x_move
        self.__snake_head_y += y_move

        self.__snake_head = [self.__snake_head_x, self.__snake_head_y]

        self.__snake_list.append(self.__snake_head)

        if len(self.__snake_list) > self.__snake_len: # erase head from last frame
            del self.__snake_list[0]

    def got_food(self, food_x, food_y): # check if snake's head is at food position
        if (self.__snake_head_x == food_x) and (self.__snake_head_y == food_y):
            self.__increase_length()
            return True
        else:
            return False

    def off_screen(self): # check is snake is off screen
        if (self.__snake_head_x < 0) or (self.__snake_head_x > window_size_x - 1) or (self.__snake_head_y < 0) or (self.__snake_head_y > window_size_y - 1):
            return True
        else:
            return False

    def bump_into_self(self): # check is snake bumps into self
        snake_len = len(self.__snake_list)
        for pos in self.__snake_list[:-1]: # look through every position except for head
            if pos == self.__snake_head:
                return True
        return False

def display_score(score, highest_score):
    value = myfont.render("Score: " + str(score), True, pink)
    display.blit(value, [2, 0])
    value = myfont.render("Highest Score: " + str(highest_score), True, pink)
    display.blit(value, [2, 20])

def exit_game():
    pygame.quit()
    quit()

def game_lost(score, highest_score):

    msg1 = "Game Over!"
    mesg1 = myfont.render(msg1, True, blue)
    display.blit(mesg1, [window_size_x/16*6, window_size_y/2])

    msg2 = "Press 1 for Quit or 2 for Play Again"
    mesg2 = myfont.render(msg2, True, blue)
    display.blit(mesg2, [window_size_x/5, window_size_y/2+20])

    pygame.display.update()

    if score > highest_score:
        write_highest_score(score)

    play_again = True

    while play_again:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    play_again = False
                    exit_game()
                if event.key == pygame.K_2:
                    main_loop()

def check_legal_direction(event, my_snake):

    legal_direction = True

    if event.type == pygame.KEYDOWN: # if key is pressed
        if event.key == pygame.K_UP: # up arrow
            if my_snake.direction == 'down':
                legal_direction = False
        if event.key == pygame.K_DOWN: # down arrow
            if my_snake.direction == 'up':
                legal_direction = False
        if event.key == pygame.K_LEFT: # left arrow
            if my_snake.direction == 'right':
                legal_direction = False
        if event.key == pygame.K_RIGHT: # right arrow
            if my_snake.direction == 'left':
                legal_direction = False

        return legal_direction

def check_event(event, my_snake):

    if event.type == pygame.QUIT: # if close button is clicked
        exit_game()

    # check that key press is legal
    # i.e. if you are press right and you are moving left, that is not a legal move
    legal_direction = check_legal_direction(event, my_snake)

    # change snake direction
    if legal_direction == True:
        if event.type == pygame.KEYDOWN: # if key is pressed
            if event.key == pygame.K_UP: # up arrow
                my_snake.direction = 'up'
            if event.key == pygame.K_DOWN: # down arrow
                my_snake.direction = 'down'
            if event.key == pygame.K_LEFT: # left arrow
                my_snake.direction = 'left'
            if event.key == pygame.K_RIGHT: # right arrow
                my_snake.direction = 'right'

def write_highest_score(score): # store highest score in file
    f = open(filename, "w")
    f.write(str(score))
    f.close()

def read_highest_score(): # read highest score from file
    try: # try to open file to get highest score
        f = open(filename, "r")
        highest_score = int(f.read())
    except OSError: # if file doesn't exist, highest score is 0
        print(filename + ' not found!')
        highest_score = 0
    return highest_score # read highest score from file

def main_loop():

    pygame.init()

    clock = pygame.time.Clock()  # create clock object

    pygame.display.set_caption('SNAKE BY LAURA') # title on pygame window

    my_snake = snake(green) # create instance of snake object

    my_food = food(purple) # create instance of food object
    food_x, food_y = my_food.get_food_pos(window_size_x, window_size_y)

    highest_score = read_highest_score() # read highest score from file

    score = 0
    # game_over = False

    while True:

        for event in pygame.event.get(): # check for key press and quit events
            check_event(event, my_snake) # update snake direction based on key press

        my_snake.update_head_pos() # update head position of snake based on snake direction

        if my_snake.got_food(food_x, food_y): # if snake reaches food position
            score += 10 # increase score
            food_x, food_y = my_food.get_food_pos(window_size_x, window_size_y) # generate new food position

        if my_snake.off_screen() or my_snake.bump_into_self(): # if snake goes off screen or bumps into self, lose game
            game_lost(score, highest_score)

        display.fill(white) # draw background color
        my_food.draw_food() # draw food
        my_snake.draw_snake() # draw snake
        display_score(score, highest_score) # display score
        pygame.display.update()
        clock.tick(frames_per_second) # update x frames/second

    # pygame.display.update()
    # time.sleep(60)

if __name__ == "__main__":
    main_loop()