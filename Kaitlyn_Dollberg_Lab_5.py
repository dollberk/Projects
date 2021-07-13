from collections import deque


class MyStack:
    def __init__(self):
        self.stack = []

    def push(self, other):
        return self.stack.append(other)

    def pop(self):
        if len(self.stack) < 1:
            return "Error: Cannot pop. Stack Empty!"
        else:
            return self.stack.pop()

    def top(self):
        return self.stack[len(self.stack) - 1]

    def empty(self):
        return self.stack == []


class MyQueue:

    def __init__(self):
        self.queue = deque()

    def enqueue(self, other):
        return self.queue.appendleft(other)

    def dequeue(self):
        if len(self.queue) < 1:
            return "Error: Cannot dequeue. Queue Empty!"
        else:
            return self.queue.pop()

    def front(self):
        return self.queue.__getitem__(len(self.queue) - 1)

    def empty(self):
        return self.queue == deque([])


if __name__ == "__main__":

    print("MyStack Testing")
    #stack testing
    s = MyStack()
    print(s.empty())
    s.push(5)
    s.push(8)
    print(s.pop())
    s.push(3)
    print(s.empty())
    print(s.top())
    print(s.pop())
    print(s.pop())
    print(s.pop()) #should generate error

    print("\n\n")
    print("MyQueue testing")
    #queue testing
    q = MyQueue()
    print(q.empty())
    q.enqueue(5)
    q.enqueue(8)
    print(q.dequeue())
    q.enqueue(3)
    print(q.empty())
    print(q.front())
    print(q.dequeue())
    print(q.dequeue())
    print(q.dequeue()) #should generate error