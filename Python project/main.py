# Snake and Apple Game
# Created by: [Subhranil Banerjee]
# Date: [17.08.2024]

import pygame
from pygame.locals import *
import time
import random

# Variables with values 
TILE_SIZE = 50
BACKGROUND_COLOR = (110, 110, 5) #  Basic colour combination from google colour picker

# Creating a apple class where we will use an apple picture 
class Apple:
    def __init__(self, game_surface):
        self.game_surface = game_surface
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))  #  Scale function is for scalling the image according to the background.
        self.position = [TILE_SIZE * 3, TILE_SIZE * 3]  # Starting position(line where the apple will first appear)

    def draw(self):
        self.game_surface.blit(self.image, self.position)
        pygame.display.flip()  # It is to use the draw function to make the apple appear

    def move(self):
        self.position[0] = random.randint(1, 19) * TILE_SIZE
        self.position[1] = random.randint(1, 14) * TILE_SIZE

# Creating a snake class where we will use an yellow block picture 

class Snake:
    def __init__(self, game_surface, length=1):         #length of the snake , that means how many blocs are there at the starting position
        self.game_surface = game_surface
        self.image = pygame.image.load("resources/snake_body.jpg").convert()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.length = length
        self.positions = [[TILE_SIZE] * length, [TILE_SIZE] * length]
        self.direction = 'down'

    def change_direction(self, new_direction):
        if new_direction in ['left', 'right', 'up', 'down']:
            self.direction = new_direction

    def move(self):                                            # It is to move the block which is the snake from one direction to another directions
        for i in range(self.length - 1, 0, -1):
            self.positions[0][i] = self.positions[0][i-1]
            self.positions[1][i] = self.positions[1][i-1]

        if self.direction == 'left':
            self.positions[0][0] -= TILE_SIZE
        elif self.direction == 'right':
            self.positions[0][0] += TILE_SIZE
        elif self.direction == 'up':
            self.positions[1][0] -= TILE_SIZE
        elif self.direction == 'down':
            self.positions[1][0] += TILE_SIZE

        self.draw()                                             # each time using draw function because without it program cannot bring the picture it meant to show

    def draw(self):
        self.game_surface.fill(BACKGROUND_COLOR)
        for i in range(self.length):
            self.game_surface.blit(self.image, (self.positions[0][i], self.positions[1][i]))
        pygame.display.flip()                                  # flip is used for drawing the particular thing for this part it is background

    def grow(self):
        self.length += 1                                       #after absorbing a apple block the chain of yellow block will increase by 1
        self.positions[0].append(-1)        
        self.positions[1].append(-1)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake and Apple Game")

        # Adding audio
        pygame.mixer.init()
        self.play_background_music()

        # Game display
        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface, length=1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def play_background_music(self):
        pygame.mixer.music.load('resources/bg_music_1.mp3')
        pygame.mixer.music.play(-1, 0)

    def play_sound_effect(self, sound_name):
        sound = None
        if sound_name == "crash":
            sound = pygame.mixer.Sound("resources/crash.mp3")
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound("resources/ding.mp3")
        if sound:
            pygame.mixer.Sound.play(sound)

    def reset_game(self):
        self.snake = Snake(self.surface, length=1)
        self.apple = Apple(self.surface)

    def check_collision(self, x1, y1, x2, y2):      #checkiing if the block is colliding with the other block or not
        return x1 >= x2 and x1 < x2 + TILE_SIZE and y1 >= y2 and y1 < y2 + TILE_SIZE

    def render_background(self):     # Basically adding a background  image
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0, 0))

    def play(self):  # In this play function we will incorporate all the previous separate classes like render , move, display_score etc.
        self.render_background()
        self.snake.move()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()


        # This is a condition for the chain of blocks as a snake to hit the end screen then showing game over
        if (self.snake.positions[0][0] < 0 or self.snake.positions[0][0] >= self.surface.get_width() or
            self.snake.positions[1][0] < 0 or self.snake.positions[1][0] >= self.surface.get_height()):
            self.play_sound_effect('crash')
            raise Exception("Oops! The snake collided with the boundary.")

        # Here we are checking apple collision 
        if self.check_collision(self.snake.positions[0][0], self.snake.positions[1][0], self.apple.position[0], self.apple.position[1]):
            self.play_sound_effect("ding")
            self.snake.grow()
            self.apple.move()

        # If the chain of blocks collide with one another then it will show game over. 
        for i in range(3, self.snake.length):
            if self.check_collision(self.snake.positions[0][0], self.snake.positions[1][0], self.snake.positions[0][i], self.snake.positions[1][i]):
                self.play_sound_effect('crash')
                raise Exception("Oops! The snake collided with itself.")

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score_text = font.render(f"Score: {self.snake.length}", True, (200, 200, 200))
        self.surface.blit(score_text, (850, 10))

    def show_game_over(self):       # After crashing with own body it will show us a messege game over
        self.render_background()    # Here we are using back ground music
        font = pygame.font.SysFont('arial', 30)  # a custom gesture of maintaing font we can use any number we wish for
        line1 = font.render(f"Game over! Your score: {self.snake.length}", True, (255, 255, 255))       # draw one surface onto other
        self.surface.blit(line1, (200, 300))
        line2 = font.render("Press Enter to play again or Escape to exit.", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.change_direction('left')
                        elif event.key == K_RIGHT:
                            self.snake.change_direction('right')
                        elif event.key == K_UP:
                            self.snake.change_direction('up')
                        elif event.key == K_DOWN:
                            self.snake.change_direction('down')

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset_game()

            # How fast the block will move
            time.sleep(0.1)

if __name__ == '__main__':
    game = Game()
    game.run()
