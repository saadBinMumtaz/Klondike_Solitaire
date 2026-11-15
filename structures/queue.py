class Queue:
    def __init__(self):
        self.items = []
        self.head = 0      # index of the front item 

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if self.isEmpty():
            return None
        item = self.items[self.head]
        self.head = self.head + 1
        return item

    def isEmpty(self):
        return self.head >= len(self.items)

    def size(self):
        return len(self.items) - self.head