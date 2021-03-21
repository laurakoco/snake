
import pygame
import random
import time
# import os

# define global variables
pygame.font.init()
myfont = pygame.font.SysFont('Arial', 15)

window_size_x = 400
window_size_y = 300

# define RGB colors
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

    def __init__(self):

        self.x_pos = 0
        self.y_pos = 0
        self.color = purple

        self.block_size = 10

    def get_food_pos(self, window_size_x, window_size_y):

        self.x_pos = random.randrange(0, window_size_x, 10)
        self.y_pos = random.randrange(0, window_size_y, 10)

        return self.x_pos, self.y_pos

    def draw_food(self):

        pygame.draw.rect(display, self.color, [self.x_pos, self.y_pos, self.block_size, self.block_size]) # draw food

class snake:

    def __init__(self):

        self.snake_head_x = window_size_x / 2 # snake head starting position
        self.snake_head_y = window_size_y / 2

        self.block_size = 10
        self.snake_len = 1
        self.color = green

        self.snake_list = []

        self.snake_head = []

    def increase_length(self): # increase length of snake
        self.snake_len += 1

    def draw_snake(self): # draw snake
        for x in self.snake_list:
            pygame.draw.rect(display, self.color, [x[0], x[1], self.block_size, self.block_size])

    def update_head_pos(self, x_delta, y_delta):

        self.snake_head_x += x_delta
        self.snake_head_y += y_delta

        self.snake_head = [self.snake_head_x, self.snake_head_y]

        self.snake_list.append(self.snake_head)

        if len(self.snake_list) > self.snake_len: # erase head from last frame
            del self.snake_list[0]

    def got_food(self, food_x, food_y): # check if snake's head is at food position
        if (self.snake_head_x == food_x) and (self.snake_head_y == food_y):
            return True
        else:
            return False

    def off_screen(self): # check is snake is off screen
        if (self.snake_head_x < 0) or (self.snake_head_x > window_size_x) or (self.snake_head_y < 0) or (self.snake_head_y > window_size_y):
            return True
        else:
            return False

    def bump_into_self(self): # check is snake bumps into self
        for x in self.snake_list[:-1]:
            if x == self.snake_head:
                return True
        return False

def display_score(score, highest_score):
    value = myfont.render("Your Score: " + str(score), True, pink)
    display.blit(value, [2, 0])
    value = myfont.render("Highest Score: " + str(highest_score), True, pink)
    display.blit(value, [2, 20])

def exit_game():
    pygame.quit()
    quit()

def game_lost(score, highest_score):

    msg1 = "Game Over"
    mesg1 = myfont.render(msg1, True, red)
    display.blit(mesg1, [window_size_x/16*6, window_size_y/2])

    msg2 = "Press Q-Quit or C-Play Again"
    mesg2 = myfont.render(msg2, True, red)
    display.blit(mesg2, [window_size_x/4, window_size_y/2+20])

    pygame.display.update()

    if score > highest_score:
        write_highest_score(score)

    play_again = True

    while play_again:

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    play_again = False
                    exit_game()
                if event.key == pygame.K_c:
                    main_loop()

def check_event(event, my_snake, x_delta, y_delta):

    # print(event) # print out events

    if event.type == pygame.QUIT: # if close button is clicked
        exit_game()

    if event.type == pygame.KEYDOWN: # if key is pressed
        if event.key == pygame.K_UP: # up arrow
            x_delta = 0
            y_delta = -my_snake.block_size
        if event.key == pygame.K_DOWN: # down arrow
            x_delta = 0
            y_delta = my_snake.block_size
        if event.key == pygame.K_LEFT: # left arrow
            x_delta = -my_snake.block_size
            y_delta = 0
        if event.key == pygame.K_RIGHT: # right arrow
            x_delta = my_snake.block_size
            y_delta = 0

    return x_delta, y_delta

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

    pygame.display.set_caption('SNAKE') # title on pygame window

    my_snake = snake() # create instance of snake object

    my_food = food() # create instance of food object
    food_x, food_y = my_food.get_food_pos(window_size_x, window_size_y)

    highest_score = read_highest_score() # read highest score from file

    x_delta = 0
    y_delta = 0
    score = 0
    # game_over = False

    while True:

        for event in pygame.event.get(): # check for key press and quit events
            x_delta, y_delta = check_event(event, my_snake, x_delta, y_delta)

        my_snake.update_head_pos(x_delta, y_delta) # update head position of snake based on event

        if my_snake.got_food(food_x, food_y): # if snake reaches food position
            my_snake.increase_length() # increase length
            score += 10 # increase score
            food_x, food_y = my_food.get_food_pos(window_size_x, window_size_y) # generate new food position

        if my_snake.off_screen() or my_snake.bump_into_self(): # if snake goes off screen or bumps into self, lose game
            # game_over = True
            game_lost(score, highest_score)

        display.fill(white) # draw background color
        my_food.draw_food() # draw food
        my_snake.draw_snake() # draw snake
        display_score(score, highest_score) # display score
        pygame.display.update()
        clock.tick(frames_per_second) # update x frames/second

    # pygame.display.update()
    # time.sleep(60)

main_loop()