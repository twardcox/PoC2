# stacks push/pop LIFO
# queues enqueue/dequeue FIFO

"""
Queue class
"""

class Queue:
    """
    A simple implementation of a FIFO queue.
    """

    def __init__(self):
        """ 
        Initialize the queue.
        """
        self._items = []

    def __len__(self):
        """
        Return the number of items in the queue.
        """
        return len(self._items)
    
    def __iter__(self):
        """
        Create an iterator for the queue.
        """
        for item in self._items:
            yield item

    def __str__(self):
        """
        Return a string representation of the queue.
        """
        return str(self._items)

    def enqueue(self, item):
        """
        Add item to the queue.
        """        
        self._items.append(item)

    def dequeue(self):
        """
        Remove and return the least recently inserted item.
        """
        return self._items.pop(0)

    def clear(self):
        """
        Remove all items from the queue.
        """
        self._items = []

queue = Queue()
print (len(queue))
queue.enqueue(37)
queue.enqueue(14)
print (len(queue))

for item in queue:
    print(item)

print(queue)


# ---------------------------------

"""
Stack class
"""

class Stack:
    """
    A simple implementation of a FILO stack.
    """

    def __init__(self):
        """ 
        Initialize the stack.
        """
        self._items = []

    def __len__(self):
        """
        Return number of items in the stack.
        """
        return len(self._items)

    def __str__(self):
        """
        Returns a string representation of the stack.
        """
        return str(self._items)

    def push(self, item):
        """
        Push item onto the stack.
        """        
        self._items.append(item)

    def pop(self):
        """
        Pop an item off of the stack
        """
        return self._items.pop()

    def clear(self):
        """
        Remove all items from the stack.
        """
        self._items = []


