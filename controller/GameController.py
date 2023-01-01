from controller.HumanRoundController import HumanRoundController
import time

from controller.ComputerController import ComputerController
from controller.EndingGameController import EndingGameController
from controller.MinimaxController import MinimaxController
from controller.MovementController import MovementController
from controller.MovementValidationController import MovementValidationController
from model.Move import Move
from model.State import State
from view.BoardViewer import BoardViewer
from view.GameViewer import GameViewer
from model.Board import Board
from controller.HumanRoundController import HumanRoundController
import pygame as p


DIMENSION_X = 9
DIMENSION_Y = 7
SQUARE_SIZE = 80
BOARD_WIDTH = SQUARE_SIZE * DIMENSION_Y
BOARD_HEIGHT = SQUARE_SIZE * DIMENSION_X
MAX_FPS = 28
IMAGES = {}

def loadImages():
    imagesNames = ['M1', 'C1', 'D1', 'W1', 'P1', 'T1', 'L1', 'E1', 'M2', 'C2', 'D2', 'W2', 'P2', 'T2', 'L2', 'E2', 'trap',
              'den', 'grass', 'water']
    for image in imagesNames:
        IMAGES[image] = p.transform.scale(p.image.load("Images/" + image + ".png"), (SQUARE_SIZE, SQUARE_SIZE))


class GameController:
    p.init()
    loadImages()
    music = p.mixer.Sound('Media/Music.mp3')
    music.play()
    screen = p.display.set_mode((BOARD_HEIGHT, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("black"))

    humanRoundController = HumanRoundController()
    movementValidationController = MovementValidationController()
    computerController = ComputerController()
    endingGameController = EndingGameController()
    minMaxController = MinimaxController()
    gameViewer = GameViewer()
    movementController = MovementController()
    minMaxController = MinimaxController()

    def chooseGameMode(self):
        running = True
        bg_img = p.transform.scale(p.image.load('Images/Wallpaper.png'), (800, 600))
        screen = p.display.set_mode((800, 600))
        screen.fill(p.Color("black"))

        while running:
            for event in p.event.get():
                if event.type == p.QUIT:
                    running = False

            screen.blit(bg_img,
                        p.Rect(0, 0, BOARD_HEIGHT, BOARD_HEIGHT))
            p.display.update()
            mode = self.gameViewer.showChoosingGameModeMenu()
            print("\n")
            if mode == 1:
                screen = p.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
                self.PlayerVsPlayer()
                running = False

            elif mode == 2:
                screen = p.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
                self.PlayerVsComputer()
                running = False

            elif mode == 3:
                screen = p.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
                self.ComputerVsComputer()
                running = False

            elif mode == 4:
                screen = p.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
                self.researchMode()
                running = False

    def PlayerVsPlayer(self):
        print("Now you can play on the Application Game!")
        board = Board(False, False)
        actual = board.getPlayer1()
        #boardViewer = BoardViewer(board)
        #boardViewer.showBoard()

        running = True
        isGameFinished = False
        sqSelected = ()
        anSelected = None
        viableMoves = None
        playerClicks = []

        while running == True:
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                elif e.type == p.MOUSEBUTTONDOWN:
                    if not isGameFinished:
                        location = p.mouse.get_pos()
                        x = location[1] // SQUARE_SIZE
                        y = location[0] // SQUARE_SIZE
                        if sqSelected == (x, y):
                            sqSelected = ()
                            playerClicks = []
                            break
                        else:
                            sqSelected = (x, y)
                        #print(x, y);
                        if len(playerClicks) == 0:
                            if self.movementValidationController.isValidStartingPoint(actual, board, x, y):
                                #print("select 1 valid!")
                                anSelected = board.matrix[x][y].animal
                                viableMoves = self.movementController.listOfPossibleMoves(board, anSelected)
                                playerClicks.append(sqSelected)
                        elif len(playerClicks) == 1:
                            actMove = Move(playerClicks[0][0], playerClicks[0][1], x, y, anSelected)
                            for v in viableMoves:
                                if self.movementValidationController.isValidEndingPoint(anSelected, board, x, y, playerClicks[0][0], playerClicks[0][1]) and self.movementController.areEqual(actMove, v):
                                    #print("movement done!")
                                    #print(anSelected.fieldName, actual.number, x, y, playerClicks[0][0], playerClicks[0][1])
                                    self.movementController.moveAnimal(anSelected, board, x, y)
                                    if actual == board.getPlayer1():
                                        actual = board.getPlayer2()
                                    else:
                                        actual = board.getPlayer1()
                                    if not self.endingGameController.noPossibleMoveForPlayer(actual, board):
                                        actual.alive = 0
                                    if self.endingGameController.testFinalGame(board.getPlayer1(), board.getPlayer2(), board, True):
                                        isGameFinished = True;
                                    sqSelected = ()
                                    playerClicks = []
                                    break
                elif e.type == p.KEYDOWN:
                    if not isGameFinished:
                        if e.key == p.K_h:
                            print("Help requested. Wait a moment!")
                            if actual == board.getPlayer1():
                                move = self.minMaxController.alpha_beta_cutoff_search(
                                    State(board, board.getPlayer1(), board.getPlayer2(), board.getPlayer1(),
                                          board.getPlayer2()), 2, 3)
                                self.movementController.moveAnimal(move.animal, board, move.endingX, move.endingY)
                                actual = board.getPlayer2()
                            else:
                                move = self.minMaxController.alpha_beta_cutoff_search(
                                    State(board, board.getPlayer2(), board.getPlayer1(), board.getPlayer2(),
                                          board.getPlayer1()), 2, 3)
                                self.movementController.moveAnimal(move.animal, board, move.endingX, move.endingY)
                                actual = board.getPlayer1()
                            if not self.endingGameController.noPossibleMoveForPlayer(actual, board):
                                actual.alive = 0
                            if self.endingGameController.testFinalGame(board.getPlayer1(), board.getPlayer2(), board,
                                                                       True):
                                isGameFinished = True;
                            sqSelected = ()
                            playerClicks = []
                            break

            drawGameState(self.screen, board, viableMoves, sqSelected, actual)
            if (isGameFinished == True):
                if board.getPlayer1().alive == 0:
                    drawText(self.screen, 'Player 2 won the game!')
                else:
                    drawText(self.screen, 'Player 1 won the game!')

            p.display.update()

            self.clock.tick(MAX_FPS)

    def PlayerVsComputer(self):
        board = Board(False, True)
        actual = board.getPlayer1()

        running = True
        isGameFinished = False
        sqSelected = ()
        anSelected = None
        viableMoves = None
        playerClicks = []

        #boardViewer = BoardViewer(board)
        board.player2.difficulty = self.gameViewer.showChoosingDifficultyMenu()
        board.player2.depth = self.gameViewer.showChoosingDepthMenu()
        #boardViewer.showBoard()
        state = State(board, board.player1, board.player2, board.player1, board.player2)
        print("Now you can play on the Application Game!")

        while running == True:
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                elif e.type == p.MOUSEBUTTONDOWN:
                    if not isGameFinished and actual == board.player1:
                        location = p.mouse.get_pos()
                        x = location[1] // SQUARE_SIZE
                        y = location[0] // SQUARE_SIZE
                        if sqSelected == (x, y):
                            sqSelected = ()
                            playerClicks = []
                            break
                        else:
                            sqSelected = (x, y)
                        #print(x, y);
                        if len(playerClicks) == 0:
                            if self.movementValidationController.isValidStartingPoint(actual, board, x, y):
                                #print("select 1 valid!")
                                anSelected = board.matrix[x][y].animal
                                viableMoves = self.movementController.listOfPossibleMoves(board, anSelected)
                                playerClicks.append(sqSelected)
                        elif len(playerClicks) == 1:
                            actMove = Move(playerClicks[0][0], playerClicks[0][1], x, y, anSelected)
                            for v in viableMoves:
                                if self.movementValidationController.isValidEndingPoint(anSelected, board, x, y, playerClicks[0][0], playerClicks[0][1]) and self.movementController.areEqual(actMove, v):
                                    #print("movement done!")
                                    #print(anSelected.fieldName, actual.number, x, y, playerClicks[0][0], playerClicks[0][1])
                                    self.movementController.moveAnimal(anSelected, board, x, y)
                                    actual = board.getPlayer2()
                                    state.currentPlayer = state.board.getPlayer2()
                                    state.opponentPlayer = state.board.getPlayer1()
                                    state.playerWhoMoves = state.currentPlayer
                                    state.playerWhoNotMoves = state.opponentPlayer
                                    sqSelected = ()
                                    playerClicks = []
                                    break
                elif e.type == p.KEYDOWN:
                    if not isGameFinished and actual == board.player1:
                        if e.key == p.K_h:
                            print("Help requested. Wait a moment!")
                            if actual == board.getPlayer1():
                                move = self.minMaxController.alpha_beta_cutoff_search(
                                    State(board, board.getPlayer1(), board.getPlayer2(), board.getPlayer1(),
                                          board.getPlayer2()), 2, 3)
                                self.movementController.moveAnimal(move.animal, board, move.endingX, move.endingY)
                                actual = board.getPlayer2()
                                state.currentPlayer = state.board.getPlayer2()
                                state.opponentPlayer = state.board.getPlayer1()
                                state.playerWhoMoves = state.currentPlayer
                                state.playerWhoNotMoves = state.opponentPlayer
                            if not self.endingGameController.noPossibleMoveForPlayer(actual, board):
                                actual.alive = 0
                            if self.endingGameController.testFinalGame(board.getPlayer1(), board.getPlayer2(), board,
                                                                       True):
                                isGameFinished = True;
                            sqSelected = ()
                            playerClicks = []
                            break

            if(actual == board.player2):
                    move = self.minMaxController.alpha_beta_cutoff_search(state, state.currentPlayer.difficulty, state.currentPlayer.depth)
                    state.currentPlayer.lastMoves.addValue(move)
                    self.computerController.round(state.board, move)
                    state.currentPlayer = state.board.getPlayer1()
                    state.opponentPlayer = state.board.getPlayer2()
                    state.playerWhoMoves = state.currentPlayer
                    state.playerWhoNotMoves = state.opponentPlayer
                    actual = board.getPlayer1()
            if not self.endingGameController.noPossibleMoveForPlayer(state.playerWhoMoves, state.board):
                state.playerWhoMoves.alive = 0
            if self.endingGameController.testFinalGame(board.getPlayer1(), board.getPlayer2(), board, True):
                isGameFinished = True

            drawGameState(self.screen, board, viableMoves, sqSelected, actual)
            if (isGameFinished == True):
                if board.getPlayer1().alive == 0:
                    drawText(self.screen, 'Player 2 won the game!')
                else:
                    drawText(self.screen, 'Player 1 won the game!')

            p.display.update()

            self.clock.tick(MAX_FPS)
        while self.endingGameController.testFinalGame(board.getPlayer1(), board.getPlayer2(), board, True) == False:
            print("Turn of player" + str(state.currentPlayer.number))
            if state.currentPlayer.isABot:
                move = self.minMaxController.alpha_beta_cutoff_search(state, state.currentPlayer.difficulty, state.currentPlayer.depth)
                state.currentPlayer.lastMoves.addValue(move)
                self.computerController.round(state.board, move)
            else:
                self.humanRoundController.round(state.currentPlayer, state.board)
            if state.currentPlayer == state.board.getPlayer1():
                state.currentPlayer = state.board.getPlayer2()
                state.opponentPlayer = state.board.getPlayer1()
                state.playerWhoMoves = state.currentPlayer
                state.playerWhoNotMoves = state.opponentPlayer
            else:
                state.currentPlayer = state.board.getPlayer1()
                state.opponentPlayer = state.board.getPlayer2()
                state.playerWhoMoves = state.currentPlayer
                state.playerWhoNotMoves = state.opponentPlayer
            #boardViewer.showBoard()
            if not self.endingGameController.noPossibleMoveForPlayer(state.currentPlayer, board):
                state.currentPlayer.alive = 0
        return

    def ComputerVsComputer(self):
        running = True
        isGameFinished = False

        board = Board(True, True)
        #boardViewer = BoardViewer(board)
        board.player1.difficulty = self.gameViewer.showChoosingDifficultyMenu("1")
        board.player1.depth = self.gameViewer.showChoosingDepthMenu("1")
        board.player2.difficulty = self.gameViewer.showChoosingDifficultyMenu("2")
        board.player2.depth = self.gameViewer.showChoosingDepthMenu("2")
        #boardViewer.showBoard()
        state = State(board, board.player1, board.player2, board.player1, board.player2)
        print("Now you can see the game on the Application Game!")
        turns = 0

        while running == True:
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
            #print("Turn of player" + str(state.currentPlayer.number))
            if not isGameFinished:
                turns += 1
                tic = time.perf_counter()
                move = self.minMaxController.alpha_beta_cutoff_search(state, state.currentPlayer.difficulty,
                                                                      state.currentPlayer.depth)
                toc = time.perf_counter()
                print(f"The computer has calculated the move in {toc - tic:0.4f} seconds!")
                state.currentPlayer.clock += (toc - tic)
                state.currentPlayer.nclock += 1
                self.computerController.round(board, move)
                state.currentPlayer.lastMoves.addValue(move)
                if state.currentPlayer == state.board.getPlayer1():
                    state.currentPlayer = state.board.getPlayer2()
                    state.opponentPlayer = state.board.getPlayer1()
                    state.playerWhoMoves = state.currentPlayer
                    state.playerWhoNotMoves = state.opponentPlayer
                else:
                    state.currentPlayer = state.board.getPlayer1()
                    state.opponentPlayer = state.board.getPlayer2()
                    state.playerWhoMoves = state.currentPlayer
                    state.playerWhoNotMoves = state.opponentPlayer
                #boardViewer.showBoard()
                if not self.endingGameController.noPossibleMoveForPlayer(state.playerWhoMoves, state.board):
                    state.playerWhoMoves.alive = 0
                if self.endingGameController.testFinalGame(board.getPlayer1(), board.getPlayer2(), board, True):
                    isGameFinished = True
                    print(str(turns))
                    state.currentPlayer.showTimeInfo()
                    state.opponentPlayer.showTimeInfo()

            drawGameStateCPU(self.screen, board)
            if (isGameFinished == True):
                if board.getPlayer1().alive == 0:
                    drawText(self.screen, 'Player 2 won the game!')
                else:
                    drawText(self.screen, 'Player 1 won the game!')

            p.display.update()

            self.clock.tick(MAX_FPS)
        return

    # In researchMode changing n we can change the number of games to test. In this way we can analyse much faster different difficulties/depths. At the end of the games the software gives us a
    # brief description of the games describing us number of wins, average number of rounds per game and average time for player 1 and for player 2.
    def researchMode(self):
        n = 100
        actual = 0
        nwins1 = 0
        nwins2 = 0
        avgTime1 = 0
        avgTime2 = 0
        avgTurns = 0
        difficultyp1 = self.gameViewer.showChoosingDifficultyMenu("1")
        depthp1 = self.gameViewer.showChoosingDepthMenu("1")
        difficultyp2 = self.gameViewer.showChoosingDifficultyMenu("2")
        depthp2 = self.gameViewer.showChoosingDepthMenu("2")
        print("Now you can see the games on the Application Game!")
        while actual != n:
            running = True
            isGameFinished = False

            board = Board(True, True)
            boardViewer = BoardViewer(board)
            board.player1.difficulty = difficultyp1
            board.player2.difficulty = difficultyp2
            board.player1.depth = depthp1
            board.player2.depth = depthp2
            boardViewer.showBoard()
            state = State(board, board.player1, board.player2, board.player1, board.player2)
            turns = 0

            while running == True:
                for e in p.event.get():
                    if e.type == p.QUIT:
                        running = False
                # print("Turn of player" + str(state.currentPlayer.number))
                if not isGameFinished:
                    turns += 1
                    tic = time.perf_counter()
                    move = self.minMaxController.alpha_beta_cutoff_search(state, state.currentPlayer.difficulty,
                                                                          state.currentPlayer.depth)
                    toc = time.perf_counter()
                    print(f"The computer has calculated the move in {toc - tic:0.4f} seconds!")
                    state.currentPlayer.clock += (toc - tic)
                    state.currentPlayer.nclock += 1
                    self.computerController.round(board, move)
                    state.currentPlayer.lastMoves.addValue(move)
                    if state.currentPlayer == state.board.getPlayer1():
                        state.currentPlayer = state.board.getPlayer2()
                        state.opponentPlayer = state.board.getPlayer1()
                        state.playerWhoMoves = state.currentPlayer
                        state.playerWhoNotMoves = state.opponentPlayer
                    else:
                        state.currentPlayer = state.board.getPlayer1()
                        state.opponentPlayer = state.board.getPlayer2()
                        state.playerWhoMoves = state.currentPlayer
                        state.playerWhoNotMoves = state.opponentPlayer
                    # boardViewer.showBoard()
                    if not self.endingGameController.noPossibleMoveForPlayer(state.playerWhoMoves, state.board):
                        state.playerWhoMoves.alive = 0
                    if self.endingGameController.testFinalGame(board.getPlayer1(), board.getPlayer2(), board, True):
                        isGameFinished = True
                        print(str(turns))
                        state.currentPlayer.showTimeInfo()
                        state.opponentPlayer.showTimeInfo()
                        running = False
                        actual += 1
                        if state.currentPlayer.number == 1:
                            avgTime1 += (state.currentPlayer.clock / state.currentPlayer.nclock);
                            avgTime2 += (
                                    state.opponentPlayer.clock / state.opponentPlayer.nclock);
                        else:
                            avgTime2 += (state.currentPlayer.clock / state.currentPlayer.nclock);
                            avgTime1 += (
                                    state.opponentPlayer.clock / state.opponentPlayer.nclock);
                        avgTurns += turns
                        if state.currentPlayer.victories == 1:
                            if state.currentPlayer.number == 1:
                                nwins1 += 1
                            else:
                                nwins2 += 1
                        if state.opponentPlayer.victories == 1:
                            if state.opponentPlayer.number == 1:
                                nwins1 += 1
                            else:
                                nwins2 += 1

                drawGameStateCPU(self.screen, board)
                if (isGameFinished == True):
                    if board.getPlayer1().alive == 0:
                        drawText(self.screen, 'Player 2 won the game!')
                    else:
                        drawText(self.screen, 'Player 1 won the game!')

                p.display.update()

                self.clock.tick(MAX_FPS)
        avgTime1 = avgTime1 / n
        avgTime2 = avgTime2 / n
        avgTurns = turns
        print("Games played: " + str(actual))
        print("Games won by player 1: " + str(nwins1))
        print("Average time for moving player 1: " + str(avgTime1))
        print("Games won by player 2: " + str(nwins2))
        print("Average time for moving player 2: " + str(avgTime2))
        print("Average number of turns in a game: " + str(avgTurns))

        return

def drawGameState(screen, board: Board, viableMoves, squareSelected, actualPlayer):
    drawBoard(screen)
    drawPieces(screen, board)
    highlightSquares(screen, board, viableMoves, squareSelected, actualPlayer)

def drawGameStateCPU(screen, board):
    drawBoard(screen)
    drawPieces(screen, board)

def drawBoard(screen):
    for r in range(DIMENSION_X):
        for c in range(DIMENSION_Y):
            p.draw.rect(screen, p.Color("ivory2"), p.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            screen.blit(IMAGES['grass'],
                        p.Rect((c * SQUARE_SIZE) + 2, (r * SQUARE_SIZE) + 2, SQUARE_SIZE - 2, SQUARE_SIZE - 2))

            if r in [3, 4, 5] and c in [1, 2, 4, 5]:
                    p.draw.rect(screen, p.Color("ivory2"),
                                p.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                    screen.blit(IMAGES['water'],
                                p.Rect((c * SQUARE_SIZE) + 2, (r * SQUARE_SIZE) + 2, SQUARE_SIZE - 2, SQUARE_SIZE - 2))

            if (r in [0, 8] and c in [2, 4]) or (r in [1, 7] and c in [3]):
                    screen.blit(IMAGES['trap'], p.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            if r in [0, 8] and c in [3]:
                    screen.blit(IMAGES['den'], p.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION_X):
        for c in range(DIMENSION_Y):
            cell = board.matrix[r][c]
            if cell.thereIsAnimal():
                screen.blit(IMAGES[cell.animal.fieldName],
                            p.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def highlightSquares(screen, board, viableMoves, square_selected, actualPlayer):
        mvc = MovementValidationController()
        if square_selected != ():
            r, c = square_selected
            if board.matrix[r][c].thereIsAnimal() and board.matrix[r][c].animal.player == actualPlayer:
                s = p.Surface((SQUARE_SIZE, SQUARE_SIZE))
                s.set_alpha(150)
                s.fill(p.Color('darkslateblue'))
                screen.blit(s, (c * SQUARE_SIZE, r * SQUARE_SIZE))
                s.fill(p.Color('antiquewhite3'))
                for move in viableMoves:
                    if move.startingX == r and move.startingY == c and mvc.isValidEndingPoint(move.animal, board, move.endingX, move.endingY, move.startingX, move.startingY):
                        screen.blit(s, (move.endingY * SQUARE_SIZE, move.endingX * SQUARE_SIZE))

def drawText(screen, text):
        font = p.font.SysFont("bodonicondensedgrassettocorsivo", 65, True, True)
        text_object = font.render(text, False, p.Color("ivory2"))
        text_location = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - text_object.get_width() / 2,
                                                                     BOARD_HEIGHT / 2 - text_object.get_height() / 2)
        screen.blit(text_object, text_location)
        text_object = font.render(text, False, p.Color('black'))
        screen.blit(text_object, text_location.move(2, 2))