MAX_QSIZE = 20
class CircularQueue:
    def __init__(self):
        self.front = 0
        self.rear = 0
        self.items = [None] * MAX_QSIZE
    def isEmpty(self): return self.front == self.rear
    def isFull(self): return self.front == (self.rear+1)%MAX_QSIZE
    def enqueue(self, item):
        if not self.isFull():
            self.rear = (self.rear+1)%MAX_QSIZE
            self.items[self.rear] = item
    def dequeue(self):
        if not self.isEmpty():
            self.front = (self.front+1)%MAX_QSIZE
            return self.items[self.front]

class TNode:
    def __init__(self, data, left, right):
        self.data = data
        self.left = left
        self.right = right

def levelorder(root):
    queue = CircularQueue()
    queue.enqueue(root)
    while not queue.isEmpty():
        n = queue.dequeue()
        if n is not None:
            print(f'[{n.data}]', end=' ')
            queue.enqueue(n.left)
            queue.enqueue(n.right)

def path_length(root):
    if root is None:
        return 0

    queue = CircularQueue()
    queue.enqueue((root, 0))
    result = 0

    while not queue.isEmpty():
        node, cnt = queue.dequeue()
        result += cnt

        if node.left is not None:
            queue.enqueue((node.left, cnt + 1))
        if node.right is not None:
            queue.enqueue((node.right, cnt + 1))

    return result
def reverse(root):
    if root is None:
        return

    root.left, root.right = root.right, root.left

    reverse(root.left)
    reverse(root.right)
    
c = TNode('C',None, None)
d = TNode('D',None, None)
b = TNode('B',c,d)
f = TNode('F',None,None)
e = TNode('E',None,f)
root = TNode('A',b,e)
print('levelorder: ',end='')
levelorder(root)
print()
length = path_length(root)
print(f'전체 경로의 길이는 {length}입니다.')
print("트리의 좌우를 교환합니다")
reverse(root)
print('levelorder: ',end='')
levelorder(root)

