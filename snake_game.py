import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGRD_COLOR = (245,66,120)

class Apple:
    def __init__ (self,parent_screen):
        self.apple = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE*3
        self.y = SIZE*3

    def draw(self):
        #self.parent_screen.fill(BACKGRD_COLOR)         #if enabled; the screen will only show apple
        self.parent_screen.blit(self.apple,(self.x,self.y))
        #pygame.display.flip()

    def move(self):
        self.x = random.randint(0,24)*SIZE
        self.y = random.randint(0,19)*SIZE
        self.draw()


class Snake:
    def __init__(self,parent_screen,length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'down'


    def draw(self):
        #self.parent_screen.fill(BACKGRD_COLOR)                 #so that previous block doesnot remain
        for i in range (self.length):
            self.parent_screen.blit(self.block,(self.x[i],self.y[i]))
        #pygame.display.flip()                                   

    def move_left(self):
        self.direction = 'left'
    
    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def auto_walk(self):

        for i in range (self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'left':
            self.x[0] -= SIZE

        if self.direction == 'right':
            self.x[0] += SIZE

        if self.direction == 'up':
            self.y[0] -= SIZE

        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()
        

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game")
        pygame.mixer.init()

        self.surface = pygame.display.set_mode((1000,800))
        self.surface.fill(BACKGRD_COLOR)

        self.snake = Snake(self.surface,1)
        self.snake.draw()

        self.apple = Apple(self.surface)
        self.apple.draw()


    def Iscollision(self,x1,y1,x2,y2):
        if(abs(x2-x1)<SIZE and abs(y1-y2)<SIZE):
            return True
        return False

    def play_sound(self,sound):
        sound = pygame.mixer.Sound(f"resources/1_snake_game_resources_{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def background_music(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play()

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg,(0,0))

    def play(self):
        self.render_background()
        self.snake.auto_walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()                         #ensures changes are displayed

        #snake colliding with apple
        if(self.Iscollision(self.snake.x[0],self.snake.y[0],self.apple.x, self.apple.y)):
            self.apple.move()
            self.snake.increase_length()
            self.play_sound("ding")

        #snake colliding with itself
        for i in range(1,self.snake.length):
            if(self.Iscollision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i])):
                self.play_sound("crash")
                raise "Game over"
        
        if self.snake.x[0]<0 or self.snake.x[0] >1000 or self.snake.y[0]<0 or self.snake.y[0]>800:
            self.play_sound("crash")
            raise "Game over"

    def display_score(self):
        font = pygame.font.SysFont('arial',25)
        score = font.render(f"Score: {self.snake.length}", True, (255,255,255))
        self.surface.blit(score,(900,5))
        #pygame.display.flip()

    def game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial',25)
        line1 = font.render(f"GAME OVER!!! Score: {self.snake.length}", True, (255,255,255))
        self.surface.blit(line1,(350,400))
        line1 = font.render("Press Enter to play again. To Exit press Escape", True, (255,255,255))
        self.surface.blit(line1,(250,430))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.surface,1)
        self.apple = Apple(self.surface)
        

    def run(self):
        self.background_music()
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type==KEYDOWN:
                    
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if event.key == K_ESCAPE:
                        running = False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()
                    
                elif event.type==QUIT:
                    running=False
            
            try:
                if not pause:
                    self.play()

            except Exception as e:
                self.game_over()
                pause = True
                self.reset()
            
            time.sleep(max(0.25-0.01*self.snake.length,0.1))

if __name__ == "__main__":
    game = Game()
    game.run()