from Board import Board
from player import PlayerAB, Person

class Game:
    def __init__(self, startBoard, player1, player2, Analysis=False):
        self.startBoard = startBoard
        self.player1 = player1
        self.player2 = player2
        self.finalBoard = startBoard
        self.Analysis = Analysis


    def simulateLocalGame(self):
        board = Board(orig=self.startBoard)
        if not self.Analysis:
            board.print()

        while(True):

            if self.player1.isPlayerOne:
                if 0 == board.PlayerMove:
                    move = self.player1.findMove(board)
                else:
                    move = self.player2.findMove(board)

            else:
                if 0 == board.PlayerMove:
                    move = self.player2.findMove(board)
                else:
                    move = self.player1.findMove(board)

            if not self.Analysis:
                print ('MOVE IS: ' + str(move))
            board.move(move)
            if not self.Analysis:
                board.print()

            isOver = board.isTerminal()
            #print("FINAL SCORE:" + str(board.score))
            if isOver == 3:
                if not self.Analysis:
                    print("It is a draw!")
                return (3, board.score)
            elif isOver == 1:
                if not self.Analysis:
                    print("Player 1 wins!")
                return (1, board.score)
            elif isOver == 2:
                if not self.Analysis:
                    print("Player 2 wins!")
                return (2, board.score)




if __name__ == "__main__":
    board = Board()
    P1 = PlayerAB(7,True)
    #P1 = Person(True)
    #P2 = Person(False)
    P2 = PlayerAB(4, False)
    g = Game(None,P1,P2)
    g.simulateLocalGame()





