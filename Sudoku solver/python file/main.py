import pygame
import sys

pygame.init()
pygame.display.set_caption('Sudoku solver')

CELL_HEIGHT, CELL_WIDTH = 40, 40
BORDER = 10
WIDTH, HEIGHT = CELL_WIDTH*9 + BORDER*2, CELL_HEIGHT*9 + BORDER*2 + 60

WHITE = (255, 255, 255)
GREY = (90, 90, 90)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

mainFont = pygame.font.SysFont('arial', CELL_HEIGHT)
smallFont = pygame.font.SysFont('arial', CELL_HEIGHT//2)
(FONT_WIDTH, FONT_HEIGHT) = mainFont.size('0')

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

cells = [] # create cells in grid (9*9)
for y in range(9):
   cells.append([])
   for x in range(9):
      cell = pygame.Rect(x*CELL_WIDTH+BORDER, y*CELL_HEIGHT+BORDER, CELL_WIDTH, CELL_HEIGHT)
      cells[y].append(cell)

class SudokuGrid():
   def __init__(self):
      self.grid = [] # create grid (9*9) start with number 0
      for x in range(9):
         self.grid.append([])
         for y in range(9):
            self.grid[x].append(0)

   def draw_grid(self, WIN=WIN, cells=cells): # draw number on screen
      for i in range(len(self.grid)):
         for o in range(len(self.grid[i])):
            if self.grid[i][o] > 0:
               showNum = mainFont.render(f'{int(self.grid[i][o])}', True, BLACK if type(self.grid[i][o]) is float else RED)
               WIN.blit(showNum, (cells[i][o].x + (CELL_WIDTH-FONT_WIDTH)//2, cells[i][o].y + (CELL_HEIGHT-FONT_HEIGHT)//2))

   def check(self, row, col, val): # check for valid insert
      for i in range(len(self.grid[row])): # check valid in row
         if self.grid[row][i]==val and i!=col:
            return False
      for i in range(len(self.grid)): # check valid in column
         if self.grid[i][col]==val and i!=row:
            return False
      for x in range((row//3)*3, (row//3)*3+3): # check valid in subgrid (3*3)
         for y in range((col//3)*3, (col//3)*3+3):
            if self.grid[x][y]==val and x!=row and y!=col:
               return False
      return True

   def find_empty(self): # return position of the next empty cell
      for row in range(len(self.grid)):
         for col in range(len(self.grid[0])):
            if self.grid[row][col]==0:
               return (row,col)
      return None

   def solve(self, WIN=WIN, cells=cells): # backtracking algorithm
      emptyCell=self.find_empty() # get next empty cell, if not exist => solved
      if emptyCell==None:
         return True
      else:
         row,col=emptyCell
      for i in range(1,10): # try input value into empty cell
         if self.check(row, col, i): # input value if check as valid
            self.grid[row][col]=i
            draw_window(cells, cells[row][col], self, True)
            pygame.time.delay(20)
            if self.solve(): # keep running with the next empty cell
               return True
            self.grid[row][col]=0 # if next cell dont have a valid input return this cell value back to 0 and try again with the next i value
            draw_window(cells, cells[row][col], self, True)
            pygame.time.delay(20)
      return False # return false when cant find value to input


def draw_window(cells, selectedCell, sudokuGrid, solving, solved=None):
   WIN.fill(WHITE)
   
   for y in range(3):
      for x in range(3):
         subGrid = pygame.Rect(x*CELL_WIDTH*3+BORDER, y*CELL_WIDTH*3+BORDER, CELL_WIDTH*3, CELL_HEIGHT*3)
         pygame.draw.rect(WIN, BLACK, subGrid, 2)

   for row in cells:
      for cell in row:
         if cell == selectedCell:
            if not solving:
               pygame.draw.rect(WIN, BLUE, cell, 3)
            else:
               pygame.draw.rect(WIN, GREEN, cell, 3)
         else:
            pygame.draw.rect(WIN, GREY, cell, 1)
   
   sudokuGrid.draw_grid()

   if solved == True:
      announcement = mainFont.render('SOLVED', True, BLACK)
      WIN.blit(announcement, ((WIDTH-FONT_WIDTH*6)//2-BORDER, WIDTH+(60-FONT_HEIGHT)//2))
   if solved == False:
      announcement = mainFont.render('UNSOLVABLE', True, BLACK)
      WIN.blit(announcement, ((WIDTH-FONT_WIDTH*10)//2-BORDER, WIDTH+(60-FONT_HEIGHT)//2))
   if solved == None:
      textDeleteKey = smallFont.render('BACKSPACE: DELETE', True, BLACK)
      textStartKey = smallFont.render('PRESS 0 TO START SOLVING', True, BLACK)
      WIN.blit(textDeleteKey, (BORDER, WIDTH))
      WIN.blit(textStartKey, (BORDER, WIDTH+FONT_HEIGHT//2))
   
   pygame.display.update()

def main():
   sudokuGrid = SudokuGrid()
   selectedCell = None
   selectedRow = None
   selectedCol = None
   typing = False
   solved = None

   run = True
   while run:

      (mousePosX, mousePosY) = pygame.mouse.get_pos()
      (mouseLeftClick, mouseMiddle, mouseRightClick) = pygame.mouse.get_pressed()

      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()
         if mouseLeftClick and BORDER<mousePosX<BORDER+CELL_WIDTH*9 and BORDER<mousePosY<BORDER+CELL_HEIGHT*9:
            selectedRow = (mousePosY-BORDER)//CELL_WIDTH
            selectedCol = (mousePosX-BORDER)//CELL_HEIGHT
            selectedCell = cells[selectedRow][selectedCol]
            typing = True
         if typing:
            if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_1:
                  sudokuGrid.grid[selectedRow][selectedCol] = 1.0
                  typing = False
                  selectedCell = None
                  selectedRow = None
                  selectedCol = None
               if event.key == pygame.K_2:
                  sudokuGrid.grid[selectedRow][selectedCol] = 2.0
                  typing = False
                  selectedCell = None
                  selectedRow = None
                  selectedCol = None
               if event.key == pygame.K_3:
                  sudokuGrid.grid[selectedRow][selectedCol] = 3.0
                  typing = False
                  selectedCell = None
                  selectedRow = None
                  selectedCol = None
               if event.key == pygame.K_4:
                  sudokuGrid.grid[selectedRow][selectedCol] = 4.0
                  typing = False
                  selectedCell = None
                  selectedRow = None
                  selectedCol = None
               if event.key == pygame.K_5:
                  sudokuGrid.grid[selectedRow][selectedCol] = 5.0
                  typing = False
                  selectedCell = None
                  selectedRow = None
                  selectedCol = None
               if event.key == pygame.K_6:
                  sudokuGrid.grid[selectedRow][selectedCol] = 6.0
                  typing = False
                  selectedCell = None
                  selectedRow = None
                  selectedCol = None
               if event.key == pygame.K_7:
                  sudokuGrid.grid[selectedRow][selectedCol] = 7.0
                  typing = False
                  selectedCell = None
                  selectedRow = None
                  selectedCol = None
               if event.key == pygame.K_8:
                  sudokuGrid.grid[selectedRow][selectedCol] = 8.0
                  typing = False
                  selectedCell = None
                  selectedRow = None
                  selectedCol = None
               if event.key == pygame.K_9:
                  sudokuGrid.grid[selectedRow][selectedCol] = 9.0
                  typing = False
                  selectedCell = None
                  selectedRow = None
                  selectedCol = None
               if event.key == pygame.K_BACKSPACE:
                  sudokuGrid.grid[selectedRow][selectedCol] = 0
                  typing = False
                  selectedCell = None
                  selectedRow = None
                  selectedCol = None
         elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
               solved = sudokuGrid.solve()

      
      draw_window(cells, selectedCell, sudokuGrid, False, solved)
      

if __name__ == "__main__":
   main()