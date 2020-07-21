import pygame
from random import randint
from random import choice
from pygame.locals import *
pygame.init()
pygame.font.init()
 
## Initialise window
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
screen = pygame.display.set_mode(monitor_size,pygame.FULLSCREEN)


quitgame = False
winner = False

pygame.mouse.set_visible(False)


## Paddle measurements
paddlewidth = int(monitor_size[0]/9)
paddleheight = int(monitor_size[1]/60)
constanty = int(monitor_size[1]*0.8)
startx = int(monitor_size[0]/2-paddlewidth/2)

##ball measurements
ballwidth = int(monitor_size[0]/47)
ballheight = int(monitor_size[0]/47)

##block measurements
blockwidth = int(monitor_size[0]*0.045)
blockheight = int(monitor_size[1]*0.035)
currentx = int(monitor_size[0]*0.105)
currenty = int(monitor_size[1]*0.15)


colours = [(255,0,0),(255,140,0),(255,255,0),(0,255,0),(0,0,255),(75,0,130),(148,0,211),(255,0,128)]

xvalues = []
yvalues = []

score = 0
lives = 3

for i in range(16):
    xvalues.append(currentx)
    currentx = round((currentx+blockwidth+monitor_size[0]*0.005))

for i in range(8):
    yvalues.append(currenty)
    currenty = round((currenty+blockheight+monitor_size[1]*0.01))

class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        
        ## Pass in the color of the paddle, and its x and y position, width and height.
        self.image = pygame.Surface([width, height])
        self.image.fill((0,0,0))
        self.image.set_colorkey((0,0,0))
 
        ## Draw the paddle
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        
        ## Fetch the rectangle object that has the dimensions of the paddle.
        self.rect = self.image.get_rect()

    def moveLeft(self, pixels):
        self.rect.x -= pixels
        #Check that you are not going too far (off the screen)
        if self.rect.x < paddlewidth:
          self.rect.x = paddlewidth
          
    def moveRight(self, pixels):
        self.rect.x += pixels
        #Check that you are not going too far (off the screen)
        if self.rect.x > monitor_size[0]-paddlewidth*2:
          self.rect.x = monitor_size[0]-paddlewidth*2
            

class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        
        ## Pass in the color of the ball, and its x and y position, width and height.
        self.image = pygame.Surface([width, height])
        self.image.fill((0,0,0))
        self.image.set_colorkey((0,0,0))
 
        # Draw the ball as a rect
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        
        self.velocity = [randint(3,6),randint(-6,6)]
        
        self.velocity[0] = randint(3,6)
        self.velocity[1] = choice([i for i in range(-6,6) if i not in [0]])
        
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        
    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = choice([i for i in range(-6,6) if i not in [0]])

class Brick(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
 
        # Pass in the color of the brick, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill((0,0,0))
        self.image.set_colorkey((0,0,0))
 
        # Draw the brick (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
 
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

## Initialise sprite list
all_sprites_list = pygame.sprite.Group()
 
## Create the Paddle
paddle = Paddle((255,255,255), paddlewidth, paddleheight)
paddle.rect.x = startx
paddle.rect.y = constanty

#Create the ball
ball = Ball((255,255,255),ballwidth,ballheight)
ball.rect.x = int(monitor_size[0]/2-ballwidth/2)
ball.rect.y = int(monitor_size[1]*0.6)


## Create the bricks
all_bricks = pygame.sprite.Group()
for i in range (8):
    for j in range (16):
        brick = Brick(colours[i],blockwidth,blockheight)
        brick.rect.x = xvalues[j]
        brick.rect.y = yvalues[i]
        all_sprites_list.add(brick)
        all_bricks.add(brick)


## Add the paddle to the list of sprites
all_sprites_list.add(paddle)
all_sprites_list.add(ball)

running = True
clock = pygame.time.Clock()
clock.tick(60)

while running:
        
    mx,my = pygame.mouse.get_pos()
    
    for event in pygame.event.get(): 
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                quitgame = True
                running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.moveLeft(15)
    if keys[pygame.K_RIGHT]:
        paddle.moveRight(15)

     
    # --- Game logic should go here
    all_sprites_list.update()


        #Check if the ball is bouncing against any of the 4 walls:
    if ball.rect.x>=monitor_size[0]-ballwidth*6:
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.x<=ballwidth*5:
        ball.velocity[0] = -ball.velocity[0]
    ##bottom
    if ball.rect.y>=monitor_size[1]-ballwidth:
        ball.velocity[1] = -ball.velocity[1]
        lives -= 1
        if lives == 0:
            #Display Game Over Message for 3 seconds
            ball.kill()
            running = False
        else:
            #Kill old ball and create new one
            ball.kill()
            ball = Ball((255,255,255),ballwidth,ballheight)
            ball.rect.x = int(monitor_size[0]/2-ballwidth/2)
            ball.rect.y = int(monitor_size[1]*0.6)
            all_sprites_list.add(ball)
        
    ##top
    if ball.rect.y<ballwidth*3:
        ball.velocity[1] = -ball.velocity[1]

    #Detect collisions between the ball and the paddles
    if pygame.sprite.collide_mask(ball, paddle):
      ball.rect.x -= ball.velocity[0]
      ball.rect.y -= ball.velocity[1]
      ball.bounce()

    #Check if there is a car collision
    brick_collision_list = pygame.sprite.spritecollide(ball,all_bricks,False)
    for brick in brick_collision_list:
      ball.bounce()
      score += 1
      brick.kill()
      if len(all_bricks)==0:
        winner = True
        running = False
    # --- Drawing code should go here
    screen.fill((0,0,0))

    #Display the score and the number of lives at the top of the screen
    font = pygame.font.SysFont('Calibri', 32)
    text = font.render("Score: " + str(score), 1, (255,255,255))
    screen.blit(text, (int (monitor_size[0]/9),int(monitor_size[1]/9)))
    text = font.render("Lives: " + str(lives), 1, (255,255,255))
    screen.blit(text, (int(monitor_size[0]-monitor_size[0]/6.5),int(monitor_size[1]/9)))
    
    ## Draw all sprites to the screen
    all_sprites_list.draw(screen)
    
    ## Update display
    pygame.display.update()


if quitgame == True or lives == 0 or score == 128:
    pygame.quit()


    



    


