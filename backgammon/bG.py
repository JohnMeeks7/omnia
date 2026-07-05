print("Loading Game...")
import numpy as np
import time
time.sleep(1)

class dice:
    def roll(self):
        return np.random.randint(1, 7), np.random.randint(1, 7)
    def rollValues(self):
        d1, d2 = self.roll()
        if d1 == d2:
            return [d1, d1, d1, d1]
        else:
            return [d1, d2]

    def firstTurn(self):
        while True:
            d1, d2 = np.random.randint(1, 7), np.random.randint(1, 7)
            print(f"Player 1 rolled a {d1}, Player 2 rolled a {d2}")
            time.sleep(1)
            if d1 > d2:
                print(f"{d1} is higher than {d2} so Player 1 goes first!")
                time.sleep(1)
                print(f"Starting die are {d1} and {d2}")
                return 1, [d1, d2]
            elif d2 > d1:
                print(f"{d2} is higher than {d1} so Player 2 goes first!")
                time.sleep(2)
                print(f"Starting die are {d1} and {d2}")
                return -1, [d1, d2]
            print("Re-rolling, no dice is higher.")
            time.sleep(1)
           
class doublingCube:
    def __init__(self):
        self.currentValue = 1
        self.ownerValue = 0

    def double(self, playerNo):
        self.currentValue = self.currentValue * 2
        if playerNo == 1:
            self.ownerValue = -1
        if playerNo == -1:
            self.ownerValue = 1

    def proposeDouble(self, playerNo):
        if self.ownerValue == 0 or self.ownerValue == playerNo:
            print(f"Would you like to double? The current doubling cube value is {self.currentValue}")
            while True:
                try:
                    check = input("Type 'double' to propose a double, or 'roll' to roll the dice")
                    if check == "double":
                        if playerNo == 1:
                            print("Player 2, do you accept the double? Enter 'yes' or 'no'")
                            while True:
                                check2 = input("'yes' or 'no'")
                                if check2 == "yes":
                                    self.double(playerNo)
                                    return "Cube Doubled!"
                                elif check2 == "no":
                                    print("Double refused - game over")
                                    return self.currentValue
                                else:                        
                                     print("Please enter either 'yes' or 'no'")  
                        elif playerNo == -1:
                            print("Player 1, do you accept the double? Enter 'yes' or 'no'")
                            while True:
                                check2 = input("'yes' or 'no'")
                                if check2 == "yes":
                                    self.double(playerNo)
                                    return "Cube Doubled!"
                                elif check2 == "no":
                                    print("Double refused - game over")
                                    return self.currentValue
                                else:                        
                                     print("Please enter either 'yes' or 'no'")
                       
                    if check == "roll":
                        return "Rolling the dice"
                    else:
                        print("Please enter either 'double' or 'roll'.")
                except:
                    break
        else:
            print("Can't double! The other player owns the doubling cube!")  

class gameBoard:
   
    def __init__(self):
        self.board = np.zeros(24, dtype=int) #shows +x for player 1 tokens and -x for player 2 tokens
        self.bar = np.zeros(2, dtype=int) #length two array, shows +x of your tokens on bar and -x of opponent tokens on bar
        self.offBoard = np.zeros(2, dtype=int) #ibid
        self.initializeBoardPosition()
       
    def initializeBoardPosition(self):
        self.board[0] = -2
        self.board[5] = 5
        self.board[7] = 3
        self.board[11] = -5
        self.board[12] = 5
        self.board[16] = -3
        self.board[18] = -5
        self.board[23] = 2

    def regions(self):
        self.Player1Home = self.board[0:6]
        self.middleBoard = self.board[6:18]
        self.Player2Home = self.board[18:24]

    def possibleMove(self, playerNo, rollValues):
        if playerNo == 1:
            potentialMovesTurnPlayer1 = []
            for i in range(len(self.board)):
                if self.board[i] >= -1:
                    potentialMovesTurnPlayer1.append(i)
                   
            positionsWithPresencePlayer1 = []
            for i in range(len(self.board)):
                if self.board[i] >= 1:
                    positionsWithPresencePlayer1.append(i)
           
            possibleMovesPlayer1 = []
            for position in positionsWithPresencePlayer1:
                for dieValue in rollValues:
                    targetPosition = position - dieValue

                    if 0 <= targetPosition < len(self.board):
                   
                        if targetPosition in potentialMovesTurnPlayer1:
                            possibleMovesPlayer1.append((position, targetPosition, dieValue))
            return possibleMovesPlayer1
               
        elif playerNo == -1:
            potentialMovesTurnPlayer2 = []
            for i in range(len(self.board)):
                if self.board[i] <= 1:
                    potentialMovesTurnPlayer2.append(i)
               
            positionsWithPresencePlayer2 = []
            for i in range(len(self.board)):
                if self.board[i] <= -1:
                    positionsWithPresencePlayer2.append(i)

            possibleMovesPlayer2 = []
            for position in positionsWithPresencePlayer2:
                for dieValue in rollValues:
                    targetPosition = position + dieValue

                    if 0 <= targetPosition < len(self.board):
                   
                        if targetPosition in potentialMovesTurnPlayer2:
                            possibleMovesPlayer2.append((position, targetPosition, dieValue))
            return possibleMovesPlayer2
                   
    def onBar(self, playerNo, rollValues):
        barSpot = 0 if playerNo == 1 else 1
         
        if self.bar[barSpot] == 0:
                return []
        else:
            print("Must remove pieces from bar first!")
            possibleMovesBar = []
            for dieValue in rollValues:
                if playerNo == 1:
                    targetPosition = 24 - dieValue
                    if self.board[targetPosition] >= -1:
                        possibleMovesBar.append(("Bar", targetPosition, dieValue))
               
                elif playerNo == -1:
                    targetPosition = dieValue - 1
                    if self.board[targetPosition] <= 1:
                        possibleMovesBar.append(("Bar", targetPosition, dieValue))
            return possibleMovesBar
           

    def pieceCapture(self, playerNo, startingPosition, targetPosition):
        if playerNo == 1:
            if self.board[targetPosition] == -1:
                if startingPosition == "Bar":
                    self.bar[0] -= 1
                else:
                    self.board[startingPosition] -= 1
                self.board[targetPosition] = 1
                self.bar[1] -= 1  

        elif playerNo == -1:
            if self.board[targetPosition] == 1:
                if startingPosition == "Bar":
                    self.bar[1] += 1
                else:
                    self.board[startingPosition] += 1
                self.board[targetPosition] = -1
                self.bar[0] += 1
                                     

    def move(self, playerNo, startingPosition, targetPosition):
        if playerNo == 1:
            if startingPosition == "Bar":
                self.bar[0] -= 1
            else:
                self.board[startingPosition] -= 1
            if targetPosition == "Bear Off":
                self.offBoard[0] += 1
            else:
                self.board[targetPosition] += 1

        if playerNo == -1:
            if startingPosition == "Bar":
                self.bar[1] += 1
            else:
                self.board[startingPosition] += 1
            if targetPosition == "Bear Off":
                self.offBoard[1] -= 1
            else:
                self.board[targetPosition] -= 1

    def displayBoard(self, doublingCube, score1, score2):
        print()
        print(f"Match Score | Player 1: {score1}  -  Player 2: {score2}")
        print(f"Doubling Cube Value: {doublingCube.currentValue}")
        print()
        print("\033[1m" + "Player 2 Home" + "\033[0m")
        print()
        print(f"Pieces Born Off: {self.offBoard[1]}")
        print("-"*30)
        print()
        for i in range(23, 17, -1):
            print(f"{i}    -    {self.board[i]}")
        print()
        print(f"Player 1 Pieces on Bar: {self.bar[0]}")
        print()
        for i in range(17, 5, -1):
            print(f"{i}    -    {self.board[i]}")
        print()
        print(f"Player 2 Pieces on Bar: {self.bar[1]}")
        print()
        for i in range(5, -1, -1):
            print(f"{i}    -    {self.board[i]}")
        print()
        print(f"-"*30 )
        print(f"Pieces Born Off: {self.offBoard[0]}")
        print()
        print("\033[1m" + "Player 1 Home" + "\033[0m")
        print()
        print()

class players:
    def __init__(self, playerNo):
        self.playerNo = playerNo
               
class endOfGame:

    def allHome(self, gameboard, playerNo):
        gameboard.regions()
        if playerNo == 1:
            if gameboard.bar[0] == 0 and all(x <= 0 for x in gameboard.middleBoard) and all(x <= 0 for x in gameboard.Player2Home):
                return "Good to Bear Off"
               
        elif playerNo == -1:
            if gameboard.bar[1] == 0 and all(x >= 0 for x in gameboard.middleBoard) and all(x >= 0 for x in gameboard.Player1Home):
                return "Good to Bear Off"
               
    def bearingOff(self, playerNo, gameboard, rollValues):
        if self.allHome(gameboard, playerNo) == "Good to Bear Off":
            possibleBearOffMoves = []
       
            if playerNo == 1:
                for i in range(6):
                    if gameboard.board[i] >= 1:
                        for dieValue in rollValues:
                            distanceNeeded = i + 1
                            if dieValue == distanceNeeded:
                                possibleBearOffMoves.append((i, "Bear Off", dieValue))

                furthestIndex = -1
                for i in range(5, -1, -1):
                    if gameboard.board[i] >= 1:
                        furthestIndex = i
                        break
                       
                for dieValue in rollValues:
                    distanceNeeded = furthestIndex + 1
                    if furthestIndex != -1 and dieValue > distanceNeeded:
                        possibleBearOffMoves.append((furthestIndex, "Bear Off", dieValue))
   
                       
            if playerNo == -1:
                for i in range(18, 24):
                    if gameboard.board[i] <= -1:
                        for dieValue in rollValues:
                            distanceNeeded = 24 - i
                            if dieValue == distanceNeeded:
                                possibleBearOffMoves.append((i, "Bear Off", dieValue))

                furthestIndex = -1
                for i in range(18, 24):
                    if gameboard.board[i] <= -1:
                        furthestIndex = i
                        break
                       
                for dieValue in rollValues:
                    distanceNeeded = 24 - furthestIndex
                    if furthestIndex != -1 and dieValue > distanceNeeded:
                        possibleBearOffMoves.append((furthestIndex, "Bear Off", dieValue))
            return possibleBearOffMoves
               
    def endGame(self, playerNo, gameboard):
        if playerNo == 1:
            if gameboard.offBoard[0] == 15:
                return "Player 1 wins!"
        elif playerNo == -1:
            if gameboard.offBoard[1] == -15:
                return "Player 2 wins!"
               
    def score(self, playerNo, gameboard, dcube):
        if self.endGame(playerNo, gameboard) == "Player 1 wins!":
            if gameboard.offBoard[1] != 0:
                print("Normal Win!")
                return 1 * dcube.currentValue
            elif gameboard.offBoard[1] == 0 and gameboard.bar[1] == 0 and all(x >= 0 for x in gameboard.board[0:6]):
                print("Gammon!")
                return 2 * dcube.currentValue
            else:
                print("Backgammon!")
                return 3 * dcube.currentValue
               
        if self.endGame(playerNo, gameboard) == "Player 2 wins!":
            if gameboard.offBoard[0] != 0:
                print("Normal Win!")
                return 1 * dcube.currentValue
            elif gameboard.offBoard[0] == 0 and gameboard.bar[0] == 0 and all(x <= 0 for x in gameboard.board[18:24]):
                print("Gammon!")
                return 2 * dcube.currentValue
            else:
                print("Backgammon!")
                return 3 * dcube.currentValue

def startGame():
    print("Standard Backgammon Games are often played to 1, 3, 5, 7, 9, 11, or 15 points.")
    time.sleep(1)
    while True:
        try:
            scoreTotal = int(input("What score would you like to play to?"))
            if scoreTotal > 0:
                break
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Please enter an integer!")
           
    gB = gameBoard()
    dC = doublingCube()
    d = dice()
    eG = endOfGame()
    p1 = players(playerNo=1)
    p2 = players(playerNo=-1)
    firstPlayerNo, firstRoll = d.firstTurn()
    gamePlay(scoreTotal, gB, dC, d, eG, p1, p2, firstPlayerNo, firstRoll)
   
def gamePlay(scoreTotal, gB, dC, d, eG, p1, p2, firstPlayerNo, firstRoll):
    currentPlayer = p1 if firstPlayerNo == 1 else p2
    rollValues = firstRoll
    turnNumber = 0
    scorePlayer1 = 0
    scorePlayer2 = 0
    while scorePlayer1 < scoreTotal and scorePlayer2 < scoreTotal:
        while True:
            playerNo = 1 if currentPlayer == p1 else -1
            if turnNumber != 0:
                result = dC.proposeDouble(playerNo)
                if isinstance(result, int):
                    if playerNo == 1:
                        scorePlayer1 += result
                        print(f"\nPlayer 1 wins the round by forfeit! Player 1 score + {result}.")
                    else:
                        scorePlayer2 += result
                        print(f"\nPlayer 2 wins the round by forfeit! Player 2 score + {result}.")
                   
                    break
                input("Press enter to roll die")
                rollValues = d.rollValues()
                print(f"You rolled {rollValues}")
           
            print(turnNumber)
            gB.displayBoard(dC, scorePlayer1, scorePlayer2)
   
            remainingMoves = rollValues.copy()
            allMoves = []
            while remainingMoves:
                barSpot = 0 if playerNo == 1 else 1
                if gB.bar[barSpot] != 0:
                    allMoves = gB.onBar(playerNo, remainingMoves)
         
                else:
                    bearOffMoves = eG.bearingOff(playerNo, gB, remainingMoves)
                    normalMoves = gB.possibleMove(playerNo, remainingMoves)
                    allMoves = (bearOffMoves or []) + normalMoves
                if not allMoves:
                    print("No eligible moves, next turn!")
                    break
   
                allMoves = list(set(allMoves))
               
                print(f"{'Move Number':<15} {'Starting Position':<20} {'End Position':<15} {'Die Used':<10}")
                print("-" * 60)
                for i, move in enumerate(allMoves):
                    print(f"{str(i):<15} {str(move[0]):<20} {str(move[1]):<15} {str(move[2]):<10}")
                   
                while True:
                    try:
                        moveChosen = int(input("Choose an eligible move: "))
                        if 0 <= moveChosen < len(allMoves):
                            break
                        print(f"Enter a number between 0 and {len(allMoves) - 1}.")
                    except ValueError:
                        print("Invalid input. Enter a number.")
   
                startingPosition, targetPosition, dieValue = allMoves[moveChosen]
   
                if targetPosition != "Bear Off" and gB.board[int(targetPosition)] == -1 * playerNo:
                    gB.pieceCapture(playerNo, startingPosition, targetPosition)
                else:
                    gB.move(playerNo, startingPosition, targetPosition)
                       
                remainingMoves.remove(dieValue)
               
                gB.displayBoard(dC, scorePlayer1, scorePlayer2)
               
            if eG.endGame(playerNo, gB) == "Player 1 wins!" or eG.endGame(playerNo, gB) == "Player 2 wins!":
                score = eG.score(playerNo, gB, dC)
                print(f"Round over! Player {playerNo} score + {score}")
                if eG.endGame(playerNo, gB) == "Player 1 wins!":
                    scorePlayer1 += score
                else:
                    scorePlayer2 += score
                break
            else:
                currentPlayer = p1 if currentPlayer == p2 else p2
            turnNumber += 1
            print("Switching Turns...")
            time.sleep(2)
            if currentPlayer == p1:
                print("Player 1's Turn")
            else:
                print("Player 2's Turn")
   
        print(f"Match Score | Player 1: {scorePlayer1}, Player 2: {scorePlayer2}")

        if scorePlayer1 < scoreTotal and scorePlayer2 < scoreTotal:
            print("Starting next round...")
            time.sleep(2)
            gB = gameBoard()
            dC = doublingCube()
            firstPlayerNo, firstRoll = d.firstTurn()
            currentPlayer = p1 if firstPlayerNo == 1 else p2
            rollValues = firstRoll
            turnNumber = 0

    if scorePlayer1 >= scoreTotal:
        print("Player 1 wins!!!")
    else:
        print("Player 2 wins!!!")

print("Loaded!")
time.sleep(1)

### Run game
print("Starting Match...")
time.sleep(1)
   
print()
startGame()
