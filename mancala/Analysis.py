from Board import Board
from player import PlayerAB, Person
from Game import Game
import numpy as np





for i in range(1,9):
    for j in range(1,9):
        board = Board()
        P1 = PlayerAB(i, True)
        P2 = PlayerAB(j, False)
        g = Game(None, P1, P2, True)
        winner, score = g.simulateLocalGame()
        if winner == 3:
            winner = "DRAW"
        elif winner == 2:
            winner = "2"
        else:
            winner = "1"

        f = open("analysis/P1-" + str(i) + "_p2-" + str(j)+".txt", "w+")
        s = ("Player 1 Depth - " + str(i) + "   |   " + "Player 2 Depth - " + str(j) + "\n"+
             "Player 1 total moves - " + str(P1.totalMoves) + "    |    " +"Player 2 total moves - " +
             str(P2.totalMoves) + "\n" +
             "Player 1 Avrage Move Time - " + str(np.average(P1.times)) + " Seconds   |   "+
             "Player 2 Avrage Move Time - " + str(np.average(P2.times)) + " Seconds \n" +
             "Player 1 Delayed Computations - " + str(P1.DelayedComputation_Detections)+ "   |   " +
             "Player 2 Delayed Computations - " + str(P2.DelayedComputation_Detections) + "\n"+
             "Player 1 Dynamic Programming - " + str(P1.DP_Detections) + "   |   " +
             "Player 2 Dynamic Programming - " + str(P2.DP_Detections) + "\n" +
             "Player 1 Dynamic Depth uses - " + str(P1.DD_Increase) + "   |   " +
             "Player 2 Dynamic Depth uses - " + str(P2.DD_Increase) + "\n" +
             "Player 1 Score - " + str(score[0]) + "   |   " + "Player 2 Score - " + str(score[1]) + "\n"+
             "WINNER IS: PLAYER" + winner)
        f.write(s)
        f.close()







