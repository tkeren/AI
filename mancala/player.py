from Board import Board
import time

class Player:

    def __init__(self, depthLimit, isPlayerOne):

        self.isPlayerOne = isPlayerOne
        self.depthLimit = depthLimit
        self.pastMoves = {}
        self.pastHeuristics = {}

        ###########For Analysis###############
        self.totalMoves = 0
        self.times = []
        self.DP_Detections = 0
        self.DelayedComputation_Detections = 0
        self.DD_Increase = 0


    #heuristics is simply the difference in score
    def heuristic(self, board):
        #side = board.PlayerMove
        #score = board.score[side]-board.score[(side+1)%2]
        s1 = sum(board.board[0])
        s2 = sum(board.board[1])
        s3 = s1+s2
        total = s1+s2
        marbles = 0

        if self.isPlayerOne:
            #if s1<10 or s2<10:
            #if s3 < 20:
            marbles = s1 - s2
            score = board.score[0]-board.score[1]
        else:
            #if s1<10 or s2<10:
            #if s3<20:
            marbles = s2-s1
            score = board.score[1] - board.score[0]
        return (1.5*score) + marbles



# player that chooses best move using minimax algorithm
class PlayerAB(Player):

    def __init__(self, depthLimit, isPlayerOne):
        super().__init__(depthLimit, isPlayerOne)



    def findMove(self, board):
        start_time = time.time()
        self.totalMoves+=1
        moves = board.children(board.PlayerMove)


        m = moves[0]
        alpha = -1000
        beta = 1000

        for move in moves:
            temp = Board(board)
            change = temp.move(move)
            term = temp.isTerminal()
            if term!=0:
                if term == 1:
                    if self.isPlayerOne:
                        return move
                    else:
                        continue
                elif term == 2:
                    if not self.isPlayerOne:
                        return move
                    else:
                        continue

            else:
                if change == 1:
                    val = self.minimax(temp,alpha, beta, False, 1)
                else:
                    val = self.minimax(temp,alpha, beta, True, 0)


               # print(val)

                ##########Delayed Computation############
                if val == 100:
                    self.DelayedComputation_Detections += 1
                    return move
                #########################################
                if val >= alpha:
                    m = move
                    alpha = val

        #self.pastMoves[(board.hash(), self.depthLimit)] = m
        self.times.append(time.time() - start_time)
        return m


    #minimax algorith - return best score for a move looking depth plays down
    def minimax(self,board, alpha, beta, max, depth):
        if (board.hash(), depth, max) in self.pastHeuristics:
            self.DP_Detections += 1
            return self.pastHeuristics[(board.hash(), depth, max)]
        terminal = board.isTerminal()
        if terminal!=0:
            if terminal == 1:
                if self.isPlayerOne:
                    return 100
                else:
                    return self.heuristic(board)

            elif terminal == 2:
                if self.isPlayerOne:
                    return self.heuristic(board)
                else:
                    return 100


            elif terminal == 3:
                self.pastHeuristics[(board.hash(), depth, max)] = 0
                return 0
        else:
            #############Dynamic Depth #####################
            if depth >= self.depthLimit:
                if (len(board.children(board.PlayerMove))>2):
                    h = self.heuristic(board)
                    self.pastHeuristics[(board.hash(), depth, max)] = h
                    return h
                else:
                    self.DD_Increase+=1
            ################################################

            #maximizing score
            if max:
                m = -1000
                moves, steps = board.childernBoards(board.PlayerMove, Boards=True)


                for temp, step in zip(moves, steps):

                    if step == 1:
                        val = self.minimax(temp,alpha, beta, False, depth+1)
                        #print("max")
                    else:
                        val = self.minimax(temp,alpha, beta, True, depth)
                        #print("min")

            ######################Delayed Computation ##################
                    if val == 100:
                        self.pastHeuristics[(board.hash(), depth, max)] = val
                        return val
            ############################################################
                    if val > m:
                        m = val
                        if val > alpha:
                            alpha = val
                        if alpha >= beta:
                            break

                self.pastHeuristics[(board.hash(), depth, max)] = m
                return m

            #minimizing the score
            else:
                m = 1000
                moves, steps = board.childernBoards(board.PlayerMove, Boards=True)

                for temp, step in zip(moves, steps):
                    #temp = Board(board)
                    #step = temp.move(move)
                    if step ==1 :
                        val = self.minimax(temp,alpha, beta, True, depth+1)
                        #print("max")

                    else:
                        val = self.minimax(temp,alpha, beta, False, depth)
                        #print("min")


                    if val == -100:
                        self.pastHeuristics[(board.hash(), depth, max)] = val
                        return val
                    if val < m:
                        m = val
                        if val < beta:
                            beta = val
                        if alpha >= beta:
                            break

                self.pastHeuristics[(board.hash(), depth, max)] = m
                return m


class Person():
    def __init__(self, isPlayerOne):
        self.isPlayerOne=isPlayerOne

    def findMove(self, board):
        move = input("Enter index of move from 0-5: ")
        return int(move)



