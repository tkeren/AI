import numpy as np
################# BOARD CLASS #################
# the board class contains the mancala Board  #
# it is 2 rows containing 6 holes in each     #
# the mancala hole is the 7th hole of a player#
#             - - - - - -                     #
# mancala <- |           | -> mancala         #
#             - - - - - -                     #
#                                             #
# The data structure contains:                #
# board - 6x2 matrix - each player's holes    #
# score - array representing mancalas         #
# PlayerMove - whose turn it is               #
# player2 array is reversed for visualization #
###############################################

class Board(object):
    def __init__(self, orig=None):
        #duplicates an existing board
        if(orig):
            s1 = [i for i in orig.board[0]]
            s2 = [i for i in orig.board[1]]
            self.board = [s1, s2]
            self.PlayerMove = orig.PlayerMove
            self.score = [orig.score[0], orig.score[1]]
            return
        #creates a new board
        else:
            self.board = [[4, 4, 4, 4 ,4, 4] for i in range(2)]
            #self.board = [[5, 5, 0, 0, 1, 1],[0, 0, 11, 1, 8, 7] ]
            self.score = [0, 0]
            self.PlayerMove = 0

    #takes index of player hole and moves marbles
    #apllies mancala rules and changes the score
    #returns state after move:
    #-1 -> move not possible
    #0 -> player gets another play (last marble in the mancala)
    #1 -> play over change player turn
    def makeMove(self, index):
        side = self.PlayerMove
        if index<0 or index>5:
            return -1
        if self.board[side][index] == 0:
            return -1

        marbles = self.board[side][index]
        self.board[side][index] = 0
        index+=1
        m = 0
        ma = marbles
        #take marbles and start iterating over the players array
        while (m<ma):
            #last marble
            if marbles == 1:
                #if it is in the mancala
                if index == 6:
                    #if its the correct mancal add to score
                    if side == self.PlayerMove:
                        self.score[side] = self.score[side]+1
                        return 0
                    #skip mancala and change side
                    else:
                        m-=1
                        index = 0
                        side = (side + 1) % 2
                #if last marble is in an empty hole and the players side
                elif self.board[side][index] == 0 and side == self.PlayerMove and self.board[(side+1)%2][abs(index-5)] != 0:
                    self.score[side] = self.score[side]+ self.board[(side+1)%2][abs(index-5)] +1
                    self.board[(side + 1) % 2][abs(index-5)] = 0
                    return 1
                else:
                    self.board[side][index] = self.board[side][index]+1
                    return 1
            #whenk it is not the last marble
            else:
                #if in mancala
                if index == 6:
                    #if it is the players mancala
                    if side == self.PlayerMove:
                        self.score[side] = self.score[side] + 1
                        marbles-=1
                    #skip mancala change side
                    else:
                        m=m-1

                    index = 0
                    side = (side+1)%2
                #add marble to hole
                else:
                    self.board[side][index] = self.board[side][index]+1
                    index+=1
                    marbles-=1
            m+=1
        return 1

    #return all available moves of the player (used by minimax mostly)
    def children(self, player):
        moves=[]
        for i in range(0,6):
            if self.board[player][i] >0:
                moves.append(i)
        return moves

    def childernBoards(self, player, Boards=False):
        moves = self.children(player)
        boards=[]
        options = []
        steps = []

        for m in moves:
            temp = Board(self)
            steps.append(temp.move(m))
            boards.append(temp)
            options.append(len(temp.children(temp.PlayerMove)))
        options = np.argsort(options)
        newBoards = [boards[i] for i in options]
        newSteps = [steps[i] for i in options]
        newMoves = [moves[i] for i in options]

        if Boards:
            return newBoards, newSteps
        else:
            return moves




    #checks if one of the sides is empty and updates the score based on the rules
    def isTerminal(self):
        moves = self.children(0)
        over = False
        if len(moves) == 0:
            self.GameOver_Update(0)
            over = True
        moves = self.children(1)
        if len(moves) == 0:
            self.GameOver_Update(1)
            over = True

        if over:
            if self.score[0] - self.score[1] > 0:
                return 1
            elif self.score[0] - self.score[1] < 0:
                return 2
            else:
                return 3
        return 0

    #adds full side to player's mancala
    def GameOver_Update(self, loser):
        winner = (loser+1)%2
        collect = sum(self.board[winner])
        self.score[winner] = self.score[winner]+collect





    #moves mancala with makeMove and updates player turn
    def move(self, index):
        result = self.makeMove(index)
        if result == -1:
            print('invalid move')
        else:
            if result:
                self.PlayerMove =(self.PlayerMove+1)%2
        return result




    def hash(self):

        power = 0
        hash = 0
        s = 0
        for row in self.board:
            # add 0 or 1 depending on piece
            for marbles in row:
                hash += marbles * (3 ** power)
                power += 1
            hash += self.score[s] * (3 ** power)
            power+=1
            s+=1

            # add a 2 to indicate end of column
            hash += 2 * (3 ** power)
            power += 1

        return hash


    #print board
    def print(self):
        print("")
        print("it is player " + str(self.PlayerMove +1) + " move")
        p2 = [i for i in self.board[1]]
        print("Mancala 1: " + str(self.score[0]))
        print("Mancala 2: " + str(self.score[1]))
        print(p2[::-1])
        print(self.board[0])


                    
                    
                    











