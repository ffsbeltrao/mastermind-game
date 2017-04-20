# noinspection PyInterpreter
from curses import wrapper
import curses
import random

GW_WIDTH = 77
GW_HEIGHT = 32
GW_TITLE = "M A S T E R M I N D"
BOARD_WIDTH = 26
BOARD_HEIGHT = 25
DELETE = 'd'
GO = 'g'
COMMAND_INPUTS = [GO, DELETE]
PIN_VALUES = ['1', '2', '3', '4', '5', '6', '7']
VALID_INPUTS = PIN_VALUES + COMMAND_INPUTS
PASSWORD = ['1', '2', '3', '4']


def generatePassword():
    global PASSWORD
    PASSWORD = random.sample(PIN_VALUES, 4)


def revealPassword(boardWindow):
    moveToPassword(boardWindow)
    for pin in PASSWORD:
        printPin(boardWindow, pin)
        boardWindow.addstr("  ")
    boardWindow.refresh()


def printPin(window, pin, y=None, x=None):
    if y and x:
        window.move(y, x)
    window.addstr(pin, curses.A_BOLD | curses.color_pair(int(pin)))


def setBackground(standardScreen):
    if curses.can_change_color():
        curses.init_color(0, 0, 0, 0)
    standardScreen.refresh()


def titleOffSet(titleLength, windowWidth):
    return windowWidth // 2 - titleLength // 2


def setWindowTitle(window, title):
    window.addstr(0, titleOffSet(len(title), window.getmaxyx()[1]), title)


def moveToPassword(boardWindow):
    boardWindow.move(BOARD_HEIGHT - 23, 11)


def moveToTip(boardWindow, line):
    boardWindow.move(BOARD_HEIGHT - 3 - (2 * line), 5)


def moveToPin(boardWindow, line, pin):
    boardWindow.move(BOARD_HEIGHT - 3 - (2 * line), 11 + (3 * pin))


def drawBlankTips(boardWindow):
    for line in range(0, 10):
        moveToTip(boardWindow, line)
        boardWindow.addstr("....")


def drawBlankPins(boardWindow):
    for line in range(0, 10):
        for pin in range(0, 4):
            moveToPin(boardWindow, line, pin)
            boardWindow.addstr(".")


def drawBlankPassword(boardWindow):
    moveToPassword(boardWindow)
    boardWindow.addstr("?  ?  ?  ?")


def initBoard():
    boardWindow = curses.newwin(BOARD_HEIGHT, BOARD_WIDTH, 3, 40)
    boardWindow.box()
    setWindowTitle(boardWindow, "Board")
    drawBlankTips(boardWindow)
    drawBlankPins(boardWindow)
    drawBlankPassword(boardWindow)
    boardWindow.refresh()
    return boardWindow


def createGameWindow():
    gameWindow = curses.newwin(GW_HEIGHT, GW_WIDTH, 0, 0)
    gameWindow.box()
    setWindowTitle(gameWindow, GW_TITLE)
    return gameWindow


def drawInstructions(gameWindow):
    gameWindow.addstr(3, 3, "Instructions")
    baseY = 14
    for pin in range(1, 8):
        printPin(gameWindow, str(pin), baseY + pin, 33)


def initGame(standardScreen):
    setBackground(standardScreen)
    gameWindow = createGameWindow()
    drawInstructions(gameWindow)
    generatePassword()
    gameWindow.refresh()
    return gameWindow


def initColors():
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)


def getTips(attempt):
    tips = []
    for position, pin in enumerate(attempt):
        if pin in PASSWORD:
            if position == PASSWORD.index(pin):
                tips.append('*')
            else:
                tips.append('-')
        else:
            tips.append(" ")
    return sorted(tips)


def drawTips(boardWindow, line, tips):
    moveToTip(boardWindow, line)
    boardWindow.addstr("".join(tips))


def getUserInput(window):
    input = window.getkey()
    while input not in VALID_INPUTS:
        input = window.getkey()
    return input


def positionToReadPin(boardWindow, line, pin):
    moveToPin(boardWindow, line, pin)
    boardWindow.addstr(" ")
    moveToPin(boardWindow, line, pin)
    boardWindow.refresh()


def readUserAttempt(boardWindow, line):
    attempt = []
    positionToReadPin(boardWindow, line, len(attempt))
    keyStroke = getUserInput(boardWindow)
    while len(attempt) is not 4 or keyStroke is not GO:
        if keyStroke in PIN_VALUES and len(attempt) is not 4:
            attempt.append(keyStroke)
            printPin(boardWindow, keyStroke)
        elif keyStroke is DELETE and len(attempt) is not 0:
            if len(attempt) is not 4:
                boardWindow.addstr(".")
            attempt.pop()

        positionToReadPin(boardWindow, line, len(attempt))
        keyStroke = getUserInput(boardWindow)

    return attempt


def runGame(boardWindow):
    for line in range(0, 10):
        attempt = readUserAttempt(boardWindow, line)
        tips = getTips(attempt)
        drawTips(boardWindow, line, tips)
        if attempt == PASSWORD:
            return


def endGame(boardWindow):
    revealPassword(boardWindow)


def main(standardScreen):
    initColors()
    gameWindow = initGame(standardScreen)
    boardWindow = initBoard()
    runGame(boardWindow)
    endGame(boardWindow)
    gameWindow.getkey()


wrapper(main)
