class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
 

class LinkedList:
    def __init__(self):
        self.head = None
        self.count = 0

    def append(self, data):
        newNode = Node(data)
        if self.head is None:
            self.head = newNode
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = newNode
        self.count = self.count + 1

    def get(self, index):
        if index < 0 or index >= self.count:
            return None
        current = self.head
        for i in range(index):
            current = current.next
        return current.data

    def size(self):
        return self.count

    def splitFrom(self, index):
        # cuts the list & returns the cut part as a new list
        newList = LinkedList()
        if index < 0 or index >= self.count:
            return newList
        if index == 0:
            newList.head = self.head
            newList.count = self.count
            self.head = None
            self.count = 0
            return newList
        current = self.head
        for i in range(index - 1):
            current = current.next
        newList.head = current.next
        newList.count = self.count - index
        current.next = None
        self.count = index
        return newList

    def toList(self):
        result = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result