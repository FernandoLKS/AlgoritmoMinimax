from Minimax import criaArvore, Minimax, JogHumano, EstadoObjetivo

import pygame
import sys
import os
import traceback
import random
import numpy as np
import copy

class GameConstants:
    #                  R    G    B
    ColorWhite     = (255, 255, 255)
    ColorBlack     = (  0,   0,   0)
    ColorRed       = (255,   0,   0)
    ColorGreen     = (  0, 255,   0)
    ColorBlue     = (  0, 0,   255)
    ColorDarkGreen = (  0, 155,   0)
    ColorDarkGray  = ( 40,  40,  40)
    BackgroundColor = ColorBlack
    
    screenScale = 1
    screenWidth = screenScale*600
    screenHeight = screenScale*600
    
    # grid size in units
    gridWidth = 3
    gridHeight = 3
    
    # grid size in pixels
    gridMarginSize = 5
    gridCellWidth = screenWidth//gridWidth - 2*gridMarginSize
    gridCellHeight = screenHeight//gridHeight - 2*gridMarginSize
    
    randomSeed = 0
    
    FPS = 30
    
    fontSize = 20

class Game:
    class GameState:
        # 0 empty, 1 X, 2 O
        grid = np.zeros((GameConstants.gridHeight, GameConstants.gridWidth))
        currentPlayer = 0
    
    def __init__(self, expectUserInputs=True):
        self.expectUserInputs = expectUserInputs
        
        # Game state list - stores a state for each time step (initial state)
        gs = Game.GameState()
        self.states = [gs]
        
        # Determines if simulation is active or not
        self.alive = True
        
        self.currentPlayer = 1
        
        # Journal of inputs by users (stack)
        self.eventJournal = []
        
        
    def checkObjectiveState(self, gs):
        # Complete line?
        for i in range(3):
            s = set(gs.grid[i, :])
            if len(s) == 1 and min(s) != 0:
                return s.pop()
            
        # Complete column?
        for i in range(3):
            s = set(gs.grid[:, i])
            if len(s) == 1 and min(s) != 0:
                return s.pop()
            
        # Complete diagonal (main)?
        s = set([gs.grid[i, i] for i in range(3)])
        if len(s) == 1 and min(s) != 0:
            return s.pop()
        
        # Complete diagonal (opposite)?
        s = set([gs.grid[-i-1, i] for i in range(3)])
        if len(s) == 1 and min(s) != 0:
            return s.pop()
            
        # nope, not an objective state
        return 0
    
    
    # Implements a game tick
    # Each call simulates a world step
    def update(self):  
        # If the game is done or there is no event, do nothing
        if not self.alive or len(self.eventJournal) < 2:
            return
        
        # Get the current (last) game state
        gs = copy.copy(self.states[-1])
            
        # Mark the cell clicked by this player if it's an empty cell
        x,y = self.eventJournal.pop()

        # Check if in bounds
        if x < 0 or y < 0 or x >= GameConstants.gridCellHeight or y >= GameConstants.gridCellWidth:
            return

        # Check if cell is empty
        if gs.grid[x][y] == 0:
            gs.grid[x][y] = gs.currentPlayer
        else: # invalid move
            return
        # Switch player turn
        if gs.currentPlayer == 0:
            gs.currentPlayer = 1
        elif gs.currentPlayer == 1:
            gs.currentPlayer = 2
        elif gs.currentPlayer == 2:
            gs.currentPlayer = 1
        # Add the new modified state
        self.states += [gs]

       

def drawGrid(screen, game):
    rects = []

    rects = [screen.fill(GameConstants.BackgroundColor)]
    
    # Get the current game state
    gs = game.states[-1]
    grid = gs.grid
 
    # Draw the grid
    for row in range(GameConstants.gridHeight):
        for column in range(GameConstants.gridWidth):
            color = GameConstants.ColorWhite
            
            if grid[row][column] == 1:
                color = GameConstants.ColorRed
            elif grid[row][column] == 2:
                color = GameConstants.ColorBlue
            
            m = GameConstants.gridMarginSize
            w = GameConstants.gridCellWidth
            h = GameConstants.gridCellHeight
            rects += [pygame.draw.rect(screen, color, [(2*m+w) * column + m, (2*m+h) * row + m, w, h])]    
    
    return rects


def draw(screen, font, game):
    rects = []
            
    rects += drawGrid(screen, game)

    return rects


def initialize():
    random.seed(GameConstants.randomSeed)
    pygame.init()
    game = Game()
    font = pygame.font.SysFont('Courier', GameConstants.fontSize)
    fpsClock = pygame.time.Clock()

    # Create display surface
    screen = pygame.display.set_mode((GameConstants.screenWidth, GameConstants.screenHeight), pygame.DOUBLEBUF)
    screen.fill(GameConstants.BackgroundColor)
        
    return screen, font, game, fpsClock


def handleEvents(game, Raiz, J):
    gs = game.states[-1]     
    for event in pygame.event.get():
        board = gs.grid 
        Estadoo = EstadoObjetivo(board)    
        if(Estadoo != 2):
            if(Estadoo == 1): print("--------------\nVERMELHO VENCEDOR\n--------------\n")
            elif(Estadoo == -1): print("--------------\nAZUL VENCEDOR\n--------------\n")
            elif(Estadoo == 0): print("--------------\nEMPATE\n--------------\n")
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            if(gs.currentPlayer == 0):
                game.eventJournal.append((1,1))
                gs.currentPlayer = 1
            if(gs.currentPlayer == 1):
                if(J == '3' or J == '4'):
                    x, y = Minimax(Raiz, board)
                    game.eventJournal.append((x, y))
                else:
                    pos = pygame.mouse.get_pos()            
                    col = pos[0] // (GameConstants.screenWidth // GameConstants.gridWidth)
                    row = pos[1] // (GameConstants.screenHeight // GameConstants.gridHeight)
                    game.eventJournal.append((row, col))
                    if(J == '2' and board[row][col] == 0):
                        JogHumano(Raiz, row, col)
            elif(gs.currentPlayer == 2):
                if(J == '2' or J == '4'):
                    x, y = Minimax(Raiz, board)
                    game.eventJournal.append((x, y))
                else:
                    pos = pygame.mouse.get_pos()            
                    col = pos[0] // (GameConstants.screenWidth // GameConstants.gridWidth)
                    row = pos[1] // (GameConstants.screenHeight // GameConstants.gridHeight)
                    game.eventJournal.append((row, col))
                    if(J == '3' and board[row][col] == 0):
                        JogHumano(Raiz, row, col) 
            
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
            
def mainGamePlayer(Raiz, J):
    try:
        # Initialize pygame and etc.
        screen, font, game, fpsClock = initialize()              
        # Main game loop
        while game.alive:
            # Handle events
            handleEvents(game, Raiz, J)            
            # Update world
            game.update()            
            # Draw this world frame
            rects = draw(screen, font, game)     
            pygame.display.update(rects)            
            # Delay for required FPS
            fpsClock.tick(GameConstants.FPS)
            
        # close up shop
        pygame.quit()
    except SystemExit:
        pass
    except Exception as e:
        #print("Unexpected error:", sys.exc_info()[0])
        traceback.print_exc(file=sys.stdout)
        pygame.quit()
        #raise Exception from e
    
    
if __name__ == "__main__":
    # Set the working directory (where we expect to find files) to the same
    # directory this .py file is in. You can leave this out of your own
    # code, but it is needed to easily run the examples using "python -m"
    file_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(file_path)

    print("\nSelecione o modo de jogo\n1 - Player VS Player\n2 - Player VS IA\n3 - IA VS Player \n4 - IA VS IA")
    J = input()
	
    if(J != '1'):
        Arv = criaArvore()
        mainGamePlayer(Arv, J)	
    else:
        mainGamePlayer(None, J)
