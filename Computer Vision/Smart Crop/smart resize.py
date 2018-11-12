import math
import numpy as np
from LinkedList import LinkedList
from PIL import Image
from pylab import *
from scipy.ndimage import filters
import matplotlib.pyplot as plt
from scipy.misc import imread, imsave
import numpy
from copy import copy, deepcopy


class SmartResize:

    def __init__(self, image, X, Y):
        self.x = X
        self.Y = Y


        test = Image.open(image).convert('L')
        test1 = Image.open(image)
        test1.show()

        self.imgRGB = array(test1)
        self.img = matrix(test)
        self.energy = self.getenerg()


        self.lsimg = LinkedList()
        self.lsenergy = LinkedList()
        self.rgb = LinkedList()

        self.WIDTH = self.energy.shape[1]
        self.HEIGHT = self.energy.shape[0]

        self.driver(X, Y)


    #Converts matrices to linked list structure
    #links the data by rows
    #Image RGB will contain an array of the red green and blue respectively
    def getls(self):
        print('initializing linked list...')
        r = self.imgRGB[:,:,0]
        g = self.imgRGB[:, :, 1]
        b = self.imgRGB[:, :, 2]
        width = self.energy.shape[1]
        height = self.energy.shape[0]
        ls = LinkedList()
        lsE = LinkedList()
        lsRGB = LinkedList()
        minpos = 0
        print(width)
        for i in range(0, height):
            inside = LinkedList()
            insideE = LinkedList()
            insideRGB = LinkedList()
            for j in range(0, width):
                inside.add(self.img[i,j])
                insideE.add(self.energy[i, j])
                insideRGB.add([r[i,j],g[i,j],b[i,j]])
            ls.add(inside)
            lsE.add(insideE)
            lsRGB.add(insideRGB)

        self.lsenergy = lsE
        self.lsimg = ls
        self.rgb = lsRGB


    #same as above but links by colomns
    def getlsX(self):
        print('initializing linked list...')
        r = self.imgRGB[:,:,0]
        g = self.imgRGB[:, :, 1]
        b = self.imgRGB[:, :, 2]
        width = self.img.shape[1]
        height = self.img.shape[0]
        ls = LinkedList()
        lsE = LinkedList()
        lsRGB = LinkedList()
        minpos = 0
        for j in range(0, width):
            inside = LinkedList()
            insideE = LinkedList()
            insideRGB = LinkedList()
            for i in range(0, height):
                inside.add(self.img[i,j])
                insideE.add(self.energy[i, j])
                insideRGB.add([r[i,j],g[i,j],b[i,j]])
            ls.add(inside)
            lsE.add(insideE)
            lsRGB.add(insideRGB)
        self.lsenergy = lsE
        self.lsimg = ls
        self.rgb = lsRGB


    #finds minimum vertical seam
    #removes that minimum at every colomn from all the LinkedLists
    def findY(self):
        print('BEGIN CALCULATING Y')
        width = self.lsenergy.dataAt(0).size
        height = self.lsenergy.size
        dp = numpy.matrix(numpy.zeros(shape=(height, width)))
        minpos = 0

        x = self.lsenergy.head
        for i in range(0,height):
            y = x.data.head
            for j in range (0,width):
                if i == 0:
                    dp[i, j] = y.data
                else:
                    if j == 0:
                        dp[i, j] = min(dp[(i-1), j], dp[(i-1), (j+1)]) + y.data
                    elif j == width-1:
                        dp[i, j] = min(dp[i-1, j], dp[(i-1), (j-1)]) + y.data
                    else:
                        dp[i, j] = min(dp[(i-1), j], dp[(i-1),(j-1)], dp[(i-1),(j+1)]) + y.data
                    if i == height-1:
                        if j == 0:
                            m = dp[i, j]
                        elif dp[i, j] < m:
                            m = dp [i, j]
                            minpos = j
                y = y.nex
            x = x.nex
        i = height -1
        j = minpos
        n = self.lsimg.tail
        n1 = self.lsenergy.tail
        n2 = self.rgb.tail
        while i>=0:

            n.data.remove(j)
            n1.data.remove(j)
            n2.data.remove(j)
            n = n.prev
            n1 = n1.prev
            n2=n2.prev

            if j == 0:
                if dp[(i-1), j]>dp[(i-1), (j+1)]:
                    j+=1
            elif j == width-1:
                if dp[(i-1),j] > dp[(i-1), (j-1)]:
                    j-=1
            else:
                save =  min(dp[(i-1), j], dp[(i-1), (j-1)], dp[(i-1), (j+1)])
                if save == dp[(i-1), (j-1)]:
                    j-=1
                elif save == dp[(i-1), (j+1)]:
                    j+=1
            i-=1
        print('Y')
        return m / self.lsenergy.size

    #same as above for horizontal seam
    def findX(self):
        print('BEGIN CALCULATING X')
        height = self.lsenergy.dataAt(0).size
        width = self.lsenergy.size
        dp = numpy.matrix(numpy.zeros(shape=(height, width)))
        minpos = 0
        m = 0
        x = self.lsenergy.head
        for j in range(0,width):
            y = x.data.head
            for i in range (0, height):
                if j == 0:
                    dp[i, j] = y.data
                else:
                    if i == 0:
                        dp[i, j] = min(dp[(i+1), (j-1)], dp[i, (j-1)]) + y.data
                    elif i == height-1:
                        dp[i, j] = min(dp[(i-1), (j-1)], dp[i, (j-1)]) + y.data
                    else:
                        dp[i, j] = min(dp[(i-1), (j-1)], dp[(i+1),(j-1)], dp[i, (j-1)]) + y.data
                    if j == width-1:
                        if i == 0:
                            m = dp[i, j]
                        elif dp[i, j] < min:
                            m = dp [i, j]
                            minpos = i
                y = y.nex
            x = x.nex
        j = width -1
        i = minpos
        n = self.lsimg.tail
        n1 = self.lsenergy.tail
        n2 = self.rgb.tail

        while j>=0:
            n.data.remove(i)
            n1.data.remove(i)
            n2.data.remove(i)
            n = n.prev
            n1 = n1.prev
            n2 = n2.prev

            if i == 0:
                if dp[i, (j-1)]>dp[(i+1), (j-1)]:
                    i+=1
            elif i == height-1:
                if dp[i, (j-1)] > dp[(i - 1), (j - 1)]:
                    i-=1
            else:
                save =  min(dp[i, (j-1)], dp[(i - 1), (j - 1)], dp[(i + 1),(j - 1)])
                if save == dp[(i - 1), (j-1)]:
                    i-=1
                elif save == dp[(i-1), (j+1)]:
                    i+=1

            j-=1
        return m/ self.lsenergy.dataAt(0).size



    #updates matrices from the linked list on vertical seam
    def lsToMatrix(self):
        width = self.lsenergy.dataAt(0).size
        height = self.lsenergy.size
        newImg = numpy.array(numpy.zeros((height, width, 3), 'uint8'))
        newImgG = numpy.array(numpy.zeros(shape=(height, width)))
        newEnergy = numpy.array(numpy.zeros(shape=(height, width)))

        x = self.rgb.head
        n = self.lsimg.head
        n1 = self.lsenergy.head
        print('BEGIN REFORMAT IMAGE...')

        for i in range(0, height):
            y = x.data.head
            y2 = n.data.head
            y3 = n1.data.head
            for j in range(0, width):
                newImgG[i, j] = y2.data
                newImg[i,j,0] = y.data[0]
                newImg[i, j, 1] = y.data[1]
                newImg[i, j, 2] = y.data[2]
                newEnergy[i,j] = y3.data
                y = y.nex
                y2 = y2.nex
                y3 = y3.nex
            x = x.nex
            n = n.nex
            n1 = n1.nex

        self.img = newImgG
        return newImg

    #Same as above for horizontal seam
    def lsToMatrixX(self):
        height = self.lsenergy.dataAt(0).size
        width = self.lsenergy.size
        newImg = numpy.array(numpy.zeros((height, width, 3), 'uint8'))
        newImgG = numpy.array(numpy.zeros(shape=(height, width)))

        x = self.rgb.head
        n = self.lsimg.head
        print('BEGIN REFORMAT IMAGE...')
        for j in range(0, width):
            y = x.data.head
            y2 = n.data.head
            for i in range(0, height):
                newImgG[i,j] = y2.data
                newImg[i,j,0] = y.data[0]
                newImg[i, j, 1] = y.data[1]
                newImg[i, j, 2] = y.data[2]
                y = y.nex
            x = x.nex

        self.img = newImgG
        return newImg




    #get energy from grayscale image
    def getenerg(self):
        width = self.img.shape[1]
        height = self.img.shape[0]
        energy = numpy.matrix(numpy.zeros(shape=(height, width)))
        imageX  = numpy.matrix(numpy.zeros(shape=(height, width)))
        imageY = numpy.matrix(numpy.zeros(shape = (height, width)))
        filters.sobel(self.img, 1, imageX)
        filters.sobel(self.img, 0, imageY)
        for i in range(0, self.img.shape[0]):
            for j in range(0,self.img.shape[1]):
                energy[i, j] = math.sqrt((imageX[i ,j]**2)+ (imageY[i, j]**2))
        return energy


    #runs findX and findY based on desired reformation (X, Y values)
    def driver(self, height, width):
        X =  height
        Y = width
        print("height = " + str(self.img.shape[0]) + " width= " + str(self.img.shape[1]))
        if Y != 0:
            self.getls()
            while Y !=  0:
                minY = self.findY()
                Y -= 1
                print(Y)
            self.imgRGB=self.lsToMatrix()

        if X != 0:
            self.lsimg = LinkedList()
            self.lsenergy = LinkedList()
            self.rgb = LinkedList()

            self.getlsX()
            while X != 0:
                minX = self.findX()
                X -= 1
                print(X)
            self.imgRGB = self.lsToMatrixX()





x = SmartResize('input3.jpg', 2, 2)
test = Image.fromarray(x.imgRGB)
test = Image.fromarray(uint8(test))
img = test.convert("RGB")
test.show(test)
