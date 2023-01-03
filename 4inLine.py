import pygame
from pygame.locals import *
import logging
 
logger = logging.getLogger()
pygame.init()
pygame.display.set_caption("4 en rayas")
cols, rows = 10, 6
width = 800
radioW = (width/cols)//2
height = (1+rows)*radioW*2
radioH = (height/(1+rows))//2
screen = pygame.display.set_mode((width,int(height)), pygame.RESIZABLE, pygame.SRCALPHA)

board = [[0 for _ in range(cols)] for i in range(rows)]
fontsizeGameOver = width//15
fontsizeEndText = width//(3*10)
fontsizeText = int(width*0.09)
font = pygame.font.Font(None, fontsizeText)
widthFinalRect, heightFinalRect = width*0.5, height*0.5

YELLOW, RED = 1, 2
color, turn = YELLOW, YELLOW
winner = None
run = True
gameOver = False

def ResetBoard():
    global board
    board = [[0 for _ in range(cols)] for _ in range(rows)]

def GetColumn(col):
    return [board[i][col] for i in range(rows)]

def CheckFullBoard():
    return all([board[i][j] != 0 for j in range(cols) for i in range(rows)])

def DrawBoard():
    for i in range(rows):
        for j in range(cols):
            if board[i][j]==0:
                pygame.draw.ellipse(screen, (255,255,255), (2*j*radioW,2*(i+1)*radioH,2*radioW,2*radioH))
            if board[i][j]==1:
                pygame.draw.ellipse(screen, (255,233,0), (2*j*radioW,2*(i+1)*radioH,2*radioW,2*radioH))
            if board[i][j]==2:
                pygame.draw.ellipse(screen, (255,0,0), (2*j*radioW,2*(i+1)*radioH,2*radioW,2*radioH))

def CheckPygameExitAndResize(events):
    global run, fontsizeGameOver, fontsizeEndText, font, fontsizeText, radioW, radioH, widthFinalRect, heightFinalRect    
    for event in events:
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.VIDEORESIZE:
            width = event.w
            height = event.h
            widthFinalRect = width*0.4
            heightFinalRect = height*0.6

            radioW = (width/cols)/2
            radioH = (height/(rows+1))/2
            fontsizeGameOver = int(event.w/15)
            fontsizeEndText = int(event.w/(10*3))
            print(fontsizeText)
            fontsizeText = int(event.w*0.09)
            font = pygame.font.Font(None, fontsizeText)

def GetColumnOfMouse():
    mouse = pygame.mouse.get_pos()
    mouseX = mouse[0]
    return int(mouseX/(2*radioW))

def DrawGuideNumbers(ellipseList):
    for i,ellipse in enumerate(ellipseList):
        number_image = font.render(f'{i+1}', True, (0, 0, 0))
        number_rect = number_image.get_rect()
        number_rect.center = ellipse.center
        screen.blit(number_image,number_rect)
        
def DrawFirstToken(endGame=False):
    listEll = [pygame.draw.ellipse(screen,(50, 100, 255), ((2*i*radioW,0,2*radioW,2*radioH))) for i in range(cols)]
    colMouse = GetColumnOfMouse()
    if(not endGame):
        if turn == YELLOW:
            pygame.draw.ellipse(screen, (255,233,0), ((colMouse*2)*radioW,0,2*radioW,2*radioH))
        elif turn == RED:
            pygame.draw.ellipse(screen, (255,0,0), ((colMouse*2)*radioW,0,2*radioW,2*radioH))

    DrawGuideNumbers(listEll)
    
def GetLastRowWithoutToken(column):
    for i in range(rows-1,-1,-1):
        if board[i][column] == 0 :
            return i
    return None

def AddNewToken(events):
    global turn, gameOver, winner
    for event in events:
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            colMouse = GetColumnOfMouse()
            lastRowToken = GetLastRowWithoutToken(colMouse)
            
            if lastRowToken == None:
                return
            
            board[lastRowToken][colMouse] = YELLOW if turn == YELLOW else RED
            CheckWinner((lastRowToken,colMouse))    
            if winner != None or CheckFullBoard():
                gameOver = True
            turn = RED if turn == YELLOW else YELLOW           

def CheckWinner(position):
    CheckRowWinner(position[0])
    CheckColumnWinner(position[1])
    CheckIncreasingDiagonalWinner(position)
    CheckDecreasingDiagonalWinner(position)

def CheckRowWinner(row):
    global winner
    try:
        for i in range(cols-3):
            if board[row][i:i+4].count(turn) == 4:
                winner = turn
                return
    except Exception as error:
         logger.exception(error)

def CheckColumnWinner(column):
    global winner

    try:
        col = GetColumn(column)
        for i in range(len(col)-3):
            if col[i:i+4].count(turn) == 4:
                winner = turn
                return
    except Exception as error:
         logger.exception(error)

def CheckIncreasingDiagonalWinner(pos):
    global winner
    try:
        increasingDiagonalOfLastToken = [(i,j) for i in range(2,rows) for j in range(cols-3) if i+j == pos[0]+pos[1]]
        for element in increasingDiagonalOfLastToken:
            if (board[element[0]][element[1]] != 0 and
            board[element[0]][element[1]] == board[element[0]-1][element[1]+1] and
            board[element[0]][element[1]] == board[element[0]-2][element[1]+2] and
            board[element[0]][element[1]] == board[element[0]-3][element[1]+3]):
                winner = turn
                return
    except Exception as error:
         logger.exception(error)

def CheckDecreasingDiagonalWinner(pos):
    global winner
    try:
        decreasingDiagonalOfLastToken = [(i,j) for i in range(rows-3) for j in range(cols-3) if i-j == pos[0]-pos[1]]
        for element in decreasingDiagonalOfLastToken:
            if (board[element[0]][element[1]] != 0 and
            board[element[0]][element[1]] == board[element[0]+1][element[1]+1] and
            board[element[0]][element[1]] == board[element[0]+2][element[1]+2] and
            board[element[0]][element[1]] == board[element[0]+3][element[1]+3]):
                winner = turn
                return
    except Exception as error:
         logger.exception(error)

def DrawEndGame():
    global winner, widthFinalRect, heightFinalRect
    fontGameOver = pygame.font.Font(None, fontsizeGameOver)
    fontText = pygame.font.Font(None, fontsizeEndText)
    screen_rect= screen.get_rect()
    
    rectTexto = pygame.Rect(0,0,widthFinalRect,heightFinalRect)
    rectBorde = pygame.Rect(0,0,widthFinalRect+10,heightFinalRect+10)
    rectTexto.center, rectBorde.center = screen_rect.center, screen_rect.center

    pygame.draw.rect(screen, (255,0,0), rectBorde)
    pygame.draw.rect(screen, (0,0,0), rectTexto)

    colorWin = (255,253,0) if winner == YELLOW else (255,0,0)
    textGameOver = fontGameOver.render("GAME OVER", True, (255,255,255))
    textInstructions = fontText.render("Press SPACE or CLICK to restart", True, (255,255,255))

    screen.blit(textGameOver, (rectTexto.center[0]-textGameOver.get_rect()[2]/2, rectTexto.center[1]-textGameOver.get_rect()[3]*2))
    screen.blit(textInstructions, (rectTexto.center[0]-textInstructions.get_rect()[2]/2, rectTexto.center[1]+textGameOver.get_rect()[3]))
    
    if winner != None:
        textVictory = fontText.render("PLAYER {} WINS!!".format("YELLOW" if winner == 1 else "RED"), True, colorWin)
        screen.blit(textVictory, (rectTexto.center[0]-textVictory.get_rect()[2]/2, rectTexto.center[1]))
    else:            
        textDraw = fontText.render("DRAW", True, (255,255,255))
        screen.blit(textDraw, (rectTexto.center[0]-textDraw.get_rect()[2]/2, rectTexto.center[1]))

def GameLoop():
    global winner, gameOver, run
    try:
        if cols < 4 or rows < 4:
            raise Exception("ERROR: Columns or Rows lower than 4. Not possible 4 in line")
        
        while run:
            screen.fill((0,0,255))
            events = pygame.event.get()
            CheckPygameExitAndResize(events)
            if not gameOver:
                DrawBoard()
                DrawFirstToken()
                AddNewToken(events)
            else:
                DrawBoard()
                DrawFirstToken(True)
                DrawEndGame()
                for event in events:
                    if ((pygame.key.get_pressed()[pygame.K_SPACE]) 
                    or (event.type == pygame.MOUSEBUTTONUP and event.button == 1)):
                        gameOver = False
                        winner = None
                        ResetBoard()
                        GameLoop()
            
            pygame.display.update()


    except Exception as error:
         logger.exception(error)

    finally:
        pygame.quit

if __name__ == "__main__":
    GameLoop()













