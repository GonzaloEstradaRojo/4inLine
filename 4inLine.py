import pygame
from pygame.locals import *

pygame.init()
cols, rows = 10, 6
width = 800
radioW = (width/cols)//2
height = (1+rows)*radioW*2
radioH = (height/(1+rows))//2

board = [[0 for _ in range(cols)] for i in range(rows)]

screen = pygame.display.set_mode((width,int(height)), pygame.RESIZABLE)
pygame.display.set_caption("4 en rayas")
fontsizeGameOver = width//15
fontsizeR = width//(3*10)

YELLOW, RED = 1, 2
color, turn = YELLOW, YELLOW
winner = None
gameOver = False


def resetBoard():
    # print("resetBoard")
    global board
    board = [[0 for _ in range(cols)] for _ in range(rows)]

def getColumn(col):
    return [board[i][col] for i in range(rows)]

def checkFullBoard():
    # print("checkFullBoard")
    global board
    return all([board[i][j] != 0 for j in range(cols) for i in range(cols)])


def drawBoard():
    # print("drawBoard")
    for i in range(rows):
        for j in range(cols):
            if board[i][j]==0:
                pygame.draw.ellipse(screen, (255,255,255), (2*j*radioW,2*(i+1)*radioH,2*radioW,2*radioH))
            if board[i][j]==1:
                pygame.draw.ellipse(screen, (255,233,0), (2*j*radioW,2*(i+1)*radioH,2*radioW,2*radioH))
            if board[i][j]==2:
                pygame.draw.ellipse(screen, (255,0,0), (2*j*radioW,2*(i+1)*radioH,2*radioW,2*radioH))


def checkPygameExitAndResize(events):
    global gameOver, fontsizeGameOver, fontsizeR, radioW
    # print("checkPygameEvents")
    
    for event in events:
        if event.type == pygame.QUIT:
            gameOver = True
        
        if event.type == pygame.VIDEORESIZE:
            width = event.w
            radioW = (width/cols)/2
            height = (1+rows)*radioH*2
            fontsizeGameOver = int(event.w/15)
            fontsizeR = int(event.w/(10*3))
            screen = pygame.display.set_mode((width,height),pygame.RESIZABLE)
            screen.fill((0,0,255))


def getColumnOfMouse():
    global radioW
    # print("getColumnOfMouse")

    mouse = pygame.mouse.get_pos()
    mouseX = mouse[0]
    return int(mouseX/(2*radioW))


def drawFirstToken():
    # print("drawFirstToken")
    colMouse = getColumnOfMouse()
    if turn == YELLOW:
        pygame.draw.ellipse(screen, (255,233,0), ((colMouse*2)*radioW,0,2*radioW,2*radioH))
    elif turn == RED:
        pygame.draw.ellipse(screen, (255,0,0), ((colMouse*2)*radioW,0,2*radioW,2*radioH))


def getLastRowWithoutToken(column):
    for i in range(rows-1,-1,-1):
        if board[i][column] == 0 :
            return i
    return None


def insertToken(events):
    global turn
    for event in events:
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            colMouse = getColumnOfMouse()
            lastRowToken = getLastRowWithoutToken(colMouse)
            
            if lastRowToken == None:
                return #Column full
            
            board[lastRowToken][colMouse] = YELLOW if turn == YELLOW else RED
            checkWinner((lastRowToken,colMouse)) 
            turn = RED if turn == YELLOW else YELLOW

def checkWinner(position):
    print(f"Turno es {turn}")
    checkRowWinner(position[0])
    checkColumnWinner(position[1])
    checkIncreasingDiagonalWinner(position)
    checkDecreasingDiagonalWinner(position)

def checkRowWinner(row):
    try:
        for i in range(cols-3):
            if board[row][i:i+4].count(turn) == 4:
                print("ROW GANADOR")
                winner == turn
                return
            print("ROW NOT YET")
    except Exception as error:
        print(error)

def checkColumnWinner(column):
    try:
        col = getColumn(column)
        for i in range(len(col)-3):
            if col[i:i+4].count(turn) == 4:
                print("COL GANADOR")
                winner == turn
                return
            print("COL NOT YET")
    except Exception as error:
        print(error)


def checkIncreasingDiagonalWinner(pos):
    try:
        increasingDiagonalOfLastToken = [(i,j) for i in range(2,rows) for j in range(cols-3) if i-j == pos[0]+pos[1]]
        print("Inc diag ", increasingDiagonalOfLastToken)
        for element in increasingDiagonalOfLastToken:
            if (board[element[0]][element[1]] != 0 and
            board[element[0]][element[1]] == board[element[0]-1][element[1]+1] and
            board[element[0]][element[1]] == board[element[0]-2][element[1]+2] and
            board[element[0]][element[1]] == board[element[0]-3][element[1]+3]):
                print("INCREASING DIAGONAL GANADOR")
                winner == turn
                return
        print("INCREASING DIAGONAL NOT YET")
    except Exception as error:
        print(error)


def checkDecreasingDiagonalWinner(pos):
    try:
        decreasingDiagonalOfLastToken = [(i,j) for i in range(rows-3) for j in range(cols-3) if i-j == pos[0]-pos[1]]
        print("Dec diag ", decreasingDiagonalOfLastToken)
        print("DECREASING DIAGONAL")
        for element in decreasingDiagonalOfLastToken:
            if (board[element[0]][element[1]] != 0 and
            board[element[0]][element[1]] == board[element[0]+1][element[1]+1] and
            board[element[0]][element[1]] == board[element[0]+2][element[1]+2] and
            board[element[0]][element[1]] == board[element[0]+3][element[1]+3]):
                print("DECREASING DIAGONAL GANADOR")
                winner == turn
                return
        print("DECREASING DIAGONAL NOT YET")
    except Exception as error:
        print(error)


if __name__ == "__main__":
    try:
        if cols < 4 or rows < 4:
            raise Exception("ERROR: Columns or Rows lower than 4. Not possible 4 in line")
        
        while not gameOver:
            screen.fill((0,0,255))
            events = pygame.event.get()
            checkPygameExitAndResize(events)
            drawBoard()
            drawFirstToken()
            insertToken(events)
            # checkFullBoard()
            pygame.display.update()
    
    except Exception as error:
        print(error)

    finally:
        pygame.quit

















