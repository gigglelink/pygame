import pygame
import os
import time
from random import randrange
import sys

pygame.init()
pygame.display.set_caption('Samurai\'s Survival')

# window width and height
WIDTH, HEIGHT = 600, 450

# position of the ground in game's window
GROUND_HEIGHT = 350

# player's (samurai) width and height
PLAYER_WIDTH, PLAYER_HEIGHT = 71, 50


WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# font and color for text
mainFont = pygame.font.SysFont('arial', 30)
highScoreListFont = pygame.font.SysFont('arial', 20)
MAIN_COLOR = (38, 38, 38)


FPS = 60

# level increase after (LEVEL_TIMER) sec
LEVEL_TIMER = 10

# load image
BACKGROUND = pygame.image.load(os.path.join('Assets', 'menu', 'bg.png'))
MENU = pygame.image.load(os.path.join('Assets', 'menu', 'menu.png'))
STARTBTN = pygame.image.load(os.path.join('Assets', 'menu', 'startbtn.png'))
STARTBTN_HOVER = pygame.image.load(os.path.join('Assets', 'menu', 'startbtnhover.png'))
END_MENU = pygame.image.load(os.path.join('Assets', 'menu', 'endgame.png'))
TRY_AGAIN_BTN = pygame.image.load(os.path.join('Assets', 'menu', 'tryagain.png'))
TRY_AGAIN_BTN_HOVER = pygame.image.load(os.path.join('Assets', 'menu', 'tryagainhover.png'))

PLAYER_STAND_RIGHT = pygame.image.load(os.path.join('Assets', 'samurai','sr.png'))
PLAYER_STAND_LEFT = pygame.image.load(os.path.join('Assets', 'samurai','sl.png'))
FIGHT_LEFT = [pygame.image.load(os.path.join('Assets', 'samurai','fl1.png')), pygame.image.load(os.path.join('Assets', 'samurai','fl2.png')), pygame.image.load(os.path.join('Assets', 'samurai','fl3.png')), pygame.image.load(os.path.join('Assets', 'samurai','fl3.png'))]
FIGHT_RIGHT = [pygame.image.load(os.path.join('Assets', 'samurai','fr1.png')), pygame.image.load(os.path.join('Assets', 'samurai','fr2.png')), pygame.image.load(os.path.join('Assets', 'samurai','fr3.png')), pygame.image.load(os.path.join('Assets', 'samurai','fr3.png'))]
WALK_LEFT = [pygame.image.load(os.path.join('Assets', 'samurai','l1.png')), pygame.image.load(os.path.join('Assets', 'samurai','l2.png')), pygame.image.load(os.path.join('Assets', 'samurai','l3.png')), pygame.image.load(os.path.join('Assets', 'samurai','l4.png'))]
WALK_RIGHT = [pygame.image.load(os.path.join('Assets', 'samurai','r1.png')), pygame.image.load(os.path.join('Assets', 'samurai','r2.png')), pygame.image.load(os.path.join('Assets', 'samurai','r3.png')), pygame.image.load(os.path.join('Assets', 'samurai','r4.png'))]

ARROW = pygame.image.load(os.path.join('Assets', 'arrow', 'arrow.png'))

ENEMY_GO_RIGHT = [pygame.image.load(os.path.join('Assets', 'enemy','er1.png')), pygame.image.load(os.path.join('Assets', 'enemy','er2.png')), pygame.image.load(os.path.join('Assets', 'enemy','er3.png')), pygame.image.load(os.path.join('Assets', 'enemy','er4.png'))]
ENEMY_GO_LEFT = [pygame.image.load(os.path.join('Assets', 'enemy','el1.png')), pygame.image.load(os.path.join('Assets', 'enemy','el2.png')), pygame.image.load(os.path.join('Assets', 'enemy','el3.png')), pygame.image.load(os.path.join('Assets', 'enemy','el4.png'))]

# create event name
HIT = pygame.USEREVENT + 1

ARROW_LV1 = pygame.USEREVENT + 2
ARROW_LV2 = pygame.USEREVENT + 3
ARROW_LV3 = pygame.USEREVENT + 4
ARROW_LV4 = pygame.USEREVENT + 5
ARROW_LV5 = pygame.USEREVENT + 6
ARROW_LV6 = pygame.USEREVENT + 7
SPAWN_ARROW = [ARROW_LV1, ARROW_LV2, ARROW_LV3, ARROW_LV4, ARROW_LV5, ARROW_LV6]

ENEMY_LV1 = pygame.USEREVENT + 8
ENEMY_LV2 = pygame.USEREVENT + 9
ENEMY_LV3 = pygame.USEREVENT + 10
ENEMY_LV4 = pygame.USEREVENT + 11
ENEMY_LV5 = pygame.USEREVENT + 12
ENEMY_LV6 = pygame.USEREVENT + 13
SPAWN_ENEMY = [ENEMY_LV1, ENEMY_LV2, ENEMY_LV3, ENEMY_LV4, ENEMY_LV5, ENEMY_LV6]

# class for player's character
class Samurai():
   def __init__(self, x, y, width, height): # (position x = int, position y = int, width = int, height = int)
      self.x = x
      self.y = y
      self.width = width
      self.height = height
      self.vel = 2 # character's move speed
      self.left = False # check facing left or right
      self.right = True
      self.stand = True # check standing still
      self.fight = False # check on fighting's frame
      self.walkCount = 0
      self.fightCount = 0
      self.hitbox = (self.x+23, self.y+20, 25, 25) # hitbox for character
      self.slash = (self.x+self.width//2, self.y+self.height//2, 0, 0) # hitbox for character's attack
   
   #function to draw character on game's window 
   def draw(self, WIN):
      if self.walkCount + 1 >= 24:
         self.walkCount = 0

      if self.fight:
         if self.fightCount < 12: # 4 image for fight, each image last 3 frame
            if self.right:
               WIN.blit(FIGHT_RIGHT[self.fightCount//3], (self.x, self.y))
               self.fightCount += 1
            elif self.left:
               WIN.blit(FIGHT_LEFT[self.fightCount//3], (self.x, self.y))
               self.fightCount += 1
         elif self.left: # when fight count = 12, end fight's frame, set fight = false
            WIN.blit(PLAYER_STAND_LEFT, (self.x, self.y))
            self.fight = False
            self.fightCount = 0
         else:
            WIN.blit(PLAYER_STAND_RIGHT, (self.x, self.y))
            self.fight = False
            self.fightCount = 0
      elif self.left and not self.stand: # walking: 6 image, each last 4 frame
         WIN.blit(WALK_LEFT[self.walkCount//6], (self.x, self.y))
         self.walkCount += 1
      elif self.right and not self.stand:
         WIN.blit(WALK_RIGHT[self.walkCount//6], (self.x, self.y))
         self.walkCount += 1
      elif self.left and self.stand:
         WIN.blit(PLAYER_STAND_LEFT, (self.x, self.y))
      else:
         WIN.blit(PLAYER_STAND_RIGHT, (self.x, self.y))

      self.hitbox = (self.x+23, self.y+20, 25, 25)
      self.slash = (self.x+self.width//2, self.y+self.height//2, 0, 0)
      if self.fight and self.fightCount//5 >= 2 and self.right: # attack's hitbox only appear on the last 2 image(last 6 frame of the fight's 12 frame)
         self.slash = (self.x+46, self.y+20, 25, 25)
      if self.fight and self.fightCount//5 >= 2 and self.left:
         self.slash = (self.x, self.y+20, 25, 25)

# class for spawn enemy
class Ninja():
   def __init__(self, x, y, width, height, spawnLeft): # (position x = int, position y = int, width = int, height = int, spawnLeft = boolean-True if spawn from left )
      self.x = x
      self.y = y
      self.width = width
      self.height = height
      self.vel = 1.5 # enemy's move speed
      self.left = not spawnLeft # check spawn from left or right
      self.right = spawnLeft
      self.walkCount = 0
      self.hitbox = (self.x, self.y, self.width, self.height)

   # function to draw enemy on game's window
   def draw(self, WIN):
      if self.walkCount + 1 >= 24:
         self.walkCount = 0

      if self.left:
         WIN.blit(ENEMY_GO_LEFT[self.walkCount//6], (self.x, self.y))
         self.walkCount += 1
      elif self.right:
         WIN.blit(ENEMY_GO_RIGHT[self.walkCount//6], (self.x, self.y))
         self.walkCount += 1
      self.hitbox = (self.x, self.y, self.width, self.height)

# draw game's window when game running
def draw_window(player, arrows, enemies):
   global score
   showScore = mainFont.render(f'SCORE: {score}', True, (233, 233, 233))
   
   WIN.blit(BACKGROUND, (0,0))
   WIN.blit(showScore, (WIDTH//2 - 75, 20))

   player.draw(WIN)

   for enemy in enemies:
      enemy.draw(WIN)

   for arrow in arrows:
      WIN.blit(ARROW, (arrow.x, arrow.y))

   pygame.display.update()  

# draw game's menu, before start the game
def draw_menu(highScoreList):
   sortedHighScore = sorted(highScoreList)
   printHighScore = highScoreListFont.render(f'HIGH SCORES:', True, MAIN_COLOR)
   printHighScore1 = highScoreListFont.render('1.', True, MAIN_COLOR)
   printHighScore2 = highScoreListFont.render('2.', True, MAIN_COLOR)
   printHighScore3 = highScoreListFont.render('3.', True, MAIN_COLOR)
   printHighScore4 = highScoreListFont.render('4.', True, MAIN_COLOR)
   printHighScore5 = highScoreListFont.render('5.', True, MAIN_COLOR)
   if len(sortedHighScore) > 0:
      printHighScore1 = highScoreListFont.render(f'1 - {sortedHighScore[-1]}', True, MAIN_COLOR)
   if len(sortedHighScore) > 1:
      printHighScore2 = highScoreListFont.render(f'2 - {sortedHighScore[-2]}', True, MAIN_COLOR)
   if len(sortedHighScore) > 2:
      printHighScore3 = highScoreListFont.render(f'3 - {sortedHighScore[-3]}', True, MAIN_COLOR)
   if len(sortedHighScore) > 3:
      printHighScore4 = highScoreListFont.render(f'4 - {sortedHighScore[-4]}', True, MAIN_COLOR)
   if len(sortedHighScore) > 4:
      printHighScore5 = highScoreListFont.render(f'5 - {sortedHighScore[-5]}', True, MAIN_COLOR)

   startBtnHover = False # True when mouse hover
   startBtn = pygame.Rect(WIDTH//2 - 50, HEIGHT//2 - 25, 100, 50)

   run = True
   while run:
      WIN.blit(BACKGROUND, (0, 0))
      WIN.blit(printHighScore, (20, 185))
      WIN.blit(printHighScore1, (30, 210))
      WIN.blit(printHighScore2, (30, 230))
      WIN.blit(printHighScore3, (30, 250))
      WIN.blit(printHighScore4, (30, 270))
      WIN.blit(printHighScore5, (30, 290))
      WIN.blit(MENU, (0, 0))

      (mouseLeftClick, mouseMiddle, mouseRightClick) = pygame.mouse.get_pressed()
      (mousePosX, mousePosY) = pygame.mouse.get_pos()
      
      if startBtn.x+100 > mousePosX > startBtn.x and startBtn.y+50 > mousePosY > startBtn.y:
         startBtnHover = True
         if mouseLeftClick:
            run = False
      else:
         startBtnHover = False
            
      if startBtnHover:
         WIN.blit(STARTBTN_HOVER, (startBtn.x, startBtn.y))
      else:
         WIN.blit(STARTBTN, (startBtn.x, startBtn.y))

      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()

      pygame.display.update() 
    
# draw game's over menu
def draw_end(highScoreList):
   global score

   tryAgainBtnHover = False # True when mouse hover

   highScoreList.append(score)
   newHighScoreList = sorted(highScoreList)
   while len(newHighScoreList) > 5:
      newHighScoreList.pop(0)
   save_high_score(newHighScoreList)

   tryAgainBtn = pygame.Rect(WIDTH//2 - 50, 300, 100, 20)
   highScore = mainFont.render(f'{score}', True, MAIN_COLOR)

   run = True
   while run:
      WIN.blit(BACKGROUND, (0, 0))
      WIN.blit(END_MENU, (0, 0))
      WIN.blit(highScore, (350, 240))

      (mouseLeftClick, mouseMiddle, mouseRightClick) = pygame.mouse.get_pressed()
      (mousePosX, mousePosY) = pygame.mouse.get_pos()

      if tryAgainBtn.x+100 > mousePosX > tryAgainBtn.x and tryAgainBtn.y+20 > mousePosY > tryAgainBtn.y:
         tryAgainBtnHover = True
         if mouseLeftClick:
            run = False
      else:
         tryAgainBtnHover = False
            
      if tryAgainBtnHover:
         WIN.blit(TRY_AGAIN_BTN_HOVER, (tryAgainBtn.x, tryAgainBtn.y))
      else:
         WIN.blit(TRY_AGAIN_BTN, (tryAgainBtn.x, tryAgainBtn.y))

      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()

      pygame.display.update()  
      
# spawn arrow randomly from the top of the screen
def spawn_arrow(arrows):
   arrow = pygame.Rect(randrange(501)+50, 0, 5, 20)
   arrows.append(arrow)

# spawn enemy randomly from left or right
def spawn_enemy(enemies):
   random0or1 = randrange(2)
   spawnX = -50
   fromLeft = True
   if random0or1 == 1:
      spawnX = WIDTH + 50
      fromLeft = False
   enemy = Ninja(spawnX, GROUND_HEIGHT-45, 53, 50, fromLeft)
   enemies.append(enemy)

# add 1 score when arrow hit the ground, run HIT event (game over) when hit player
def arrow_handle(arrows, player):
   global score
   for arrow in arrows:
      arrow.y += 3
      if pygame.Rect(player.hitbox).colliderect(arrow):
         arrows.remove(arrow)
         pygame.event.post(pygame.event.Event(HIT))
      if arrow.y > GROUND_HEIGHT+ 25:
         arrows.remove(arrow)
         score += 1

# add 10 score when player kill enemy, run HIT event (game over) when enemy hit player
def enemy_handle(enemies, player):
   global score
   for enemy in enemies:
      if enemy.left:
         enemy.x -= enemy.vel
      if enemy.right:
         enemy.x += enemy.vel
      if pygame.Rect(player.hitbox).colliderect(pygame.Rect(enemy.hitbox)):
         pygame.event.post(pygame.event.Event(HIT))
      if pygame.Rect(enemy.hitbox).colliderect(pygame.Rect(player.slash)):
         enemies.remove(enemy)
         score += 10

# read high score from file high_score.txt
def read_high_score():
   highScore = []
   try:
      highScoreFile = open('high_score.txt', 'r+')
      for s in highScoreFile.read().split():
         highScore.append(int(s))
      highScoreFile.close()
   except ValueError:
      highScoreFile.truncate(0) # clear file if file contain wrong type of values
      highScore = []
   except FileNotFoundError:
      pass
   return highScore

# save high score to file high_score.txt
def save_high_score(scores):
   try:
      highScoreFile = open('high_score.txt', 'w')
      highScoreToWrite = ''
      for i in scores:
         highScoreToWrite += f'{str(i)} '
      highScoreFile.write(highScoreToWrite)
      highScoreFile.close()
   except IOError:
      pass

# main function run game
def main():
   global score
   score = 0 # score=0 at the start of the game
   clock = pygame.time.Clock()

   highScoreList = read_high_score()

   draw_menu(highScoreList)
   
   timeStart = time.time() # start the clock when game start

   player = Samurai(WIDTH//2 - PLAYER_WIDTH//2, GROUND_HEIGHT-PLAYER_HEIGHT+5, PLAYER_WIDTH, PLAYER_HEIGHT)

   arrows = []
   pygame.time.set_timer(ARROW_LV1, 600) # spawn arrow faster on higher level
   pygame.time.set_timer(ARROW_LV2, 500)
   pygame.time.set_timer(ARROW_LV3, 400)
   pygame.time.set_timer(ARROW_LV4, 300)
   pygame.time.set_timer(ARROW_LV5, 200)
   pygame.time.set_timer(ARROW_LV6, 100)

   enemies = []
   pygame.time.set_timer(ENEMY_LV1, 5000) # spawn enemy faster on higher level
   pygame.time.set_timer(ENEMY_LV2, 5000)
   pygame.time.set_timer(ENEMY_LV3, 5000)
   pygame.time.set_timer(ENEMY_LV4, 4000)
   pygame.time.set_timer(ENEMY_LV5, 3000)
   pygame.time.set_timer(ENEMY_LV6, 2000)

   run = True
   while run:
      clock.tick(FPS)
      timeCurrent = time.time() - timeStart # get played time to decide on level
      if timeCurrent < LEVEL_TIMER: # select level, disable (block) other level's event
         for EVENT in SPAWN_ARROW:
            if EVENT == ARROW_LV1:
               pygame.event.set_allowed(EVENT)
            else:
               pygame.event.set_blocked(EVENT)
         for EVENT in SPAWN_ENEMY:
            if EVENT == ENEMY_LV1:
               pygame.event.set_allowed(EVENT)
            else:
               pygame.event.set_blocked(EVENT)
      elif timeCurrent < LEVEL_TIMER*2:
         for EVENT in SPAWN_ARROW:
            if EVENT == ARROW_LV2:
               pygame.event.set_allowed(EVENT)
            else:
               pygame.event.set_blocked(EVENT)
         for EVENT in SPAWN_ENEMY:
            if EVENT == ENEMY_LV2:
               pygame.event.set_allowed(EVENT)
            else:
               pygame.event.set_blocked(EVENT)
      elif timeCurrent < LEVEL_TIMER*3:
         for EVENT in SPAWN_ARROW:
            if EVENT == ARROW_LV3:
               pygame.event.set_allowed(EVENT)
            else:
               pygame.event.set_blocked(EVENT)
         for EVENT in SPAWN_ENEMY:
            if EVENT == ENEMY_LV3:
               pygame.event.set_allowed(EVENT)
            else:
               pygame.event.set_blocked(EVENT)
      elif timeCurrent < LEVEL_TIMER*4:
         for EVENT in SPAWN_ARROW:
            if EVENT == ARROW_LV4:
               pygame.event.set_allowed(EVENT)
            else:
               pygame.event.set_blocked(EVENT)
         for EVENT in SPAWN_ENEMY:
            if EVENT == ENEMY_LV4:
               pygame.event.set_allowed(EVENT)
            else:
               pygame.event.set_blocked(EVENT)
      elif timeCurrent < LEVEL_TIMER*5:
         for EVENT in SPAWN_ARROW:
            if EVENT == ARROW_LV5:
               pygame.event.set_allowed(EVENT)
            else:
               pygame.event.set_blocked(EVENT)
         for EVENT in SPAWN_ENEMY:
            if EVENT == ENEMY_LV5:
               pygame.event.set_allowed(EVENT)
            else:
               pygame.event.set_blocked(EVENT)
      else:
         for EVENT in SPAWN_ARROW:
            if EVENT == ARROW_LV6:
               pygame.event.set_allowed(EVENT)
            else:
               pygame.event.set_blocked(EVENT)
         for EVENT in SPAWN_ENEMY:
            if EVENT == ENEMY_LV6:
               pygame.event.set_allowed(EVENT)
            else:
               pygame.event.set_blocked(EVENT)

      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()
         if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: # fight event (start attack)
               player.fight = True
               player.fightCount = 0
         if event.type in SPAWN_ARROW:
            spawn_arrow(arrows)
         if event.type in SPAWN_ENEMY:
            spawn_enemy(enemies)
         if event.type == HIT: # stop loop when hit
            run = False

      keys_pressed = pygame.key.get_pressed()
      if not player.fight: # only move when not fighting  
         if keys_pressed[pygame.K_LEFT] and player.x - player.vel > 0:
            player.x -= player.vel
            player.left = True
            player.right = False
            player.stand = False
         elif keys_pressed[pygame.K_RIGHT] and player.x + player.vel + PLAYER_WIDTH < WIDTH:
            player.x += player.vel
            player.right = True
            player.left = False
            player.stand = False
         else:
            player.stand = True
            player.walkCount = 0

      enemy_handle(enemies, player)
      arrow_handle(arrows, player)
      draw_window(player, arrows, enemies)
      
   draw_end(highScoreList)
   main()

if __name__ == '__main__':
   main()