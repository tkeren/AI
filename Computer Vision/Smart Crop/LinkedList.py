class node:
    def __init__(self, data):
        self.data = data
        self.nex = None
        self.prev = None


class LinkedList:

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0


    def add(self, val):
        n = node(val)
        if self.size == 0:
            self.head = n
            self.tail = n

        else:
            self.tail.nex = n
            n.prev = self.tail
            n.nex = self.head
            self.tail = n
            self.head.prev = n

        self.size+=1


    def addAt(self, val, index):
        p = True
        n = node(val)
        x = self.head
        for i in range(0, index):
            if index>self.size:
                print ('get Index out of bound')
                p = False
                break
            x = x.nex

        if p:
            n.prev = x.prev
            n.nex = x
            x.prev.nex = n
            x.prev = n
            self.size += 1

    def remove(self, index):
        if index - 1 > self.size:
            print ('Index out of bound')
            p = False
            pass

        if self.head == self.tail:
            self = LinkedList()

        else:
            back = self.size - index- 1
            p = True


            if index < back:
                x = self.head
                for i in range (0, index):
                    x = x.nex
            else:
                x = self.tail
                for i in range(0, back):
                    x = x.prev

            if p:
                x.nex.prev = x.prev
                x.prev.nex = x.nex
                self.size -= 1
            return x.data


    def dataAt(self, index):
        x = self.head
        p = True
        for i in range(0, index-1):
            if index-1 > self.size:
                print ('Index out of bound')
                p = False
                break
            x = x.nex

        if p:
            return x.data






