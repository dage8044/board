class Min_heap:
    def __init__(self):
        self.heap = []
        self.heap.append(0)
    def size(self): return len(self.heap) - 1
    def isEmpty(self) : return self.size() == 0
    def Parent(self, i) : return self.heap[i//2]
    def Left(self, i) : return self.heap[i*2]
    def Right(self, i) : return self.heap[i*2+1]
    def display(self, msg = '힙 트리: '):
        print(msg, self.heap[1:])
    def insert(self, Node):
        self.heap.append(Node)
        i = self.size()
        while (i != 1 and Node.freq < self.Parent(i).freq):
            self.heap[i] = self.Parent(i)
            i = i // 2
        self.heap[i] = Node
    

    def delete(self):
        parent = 1
        child = 2
        if not self.isEmpty():
            hroot = self.heap[1]
            last = self.heap[self.size()]
            while child <= self.size():
                if child < self.size() and self.Left(parent).freq > self.Right(parent).freq:
                    child += 1
                if last.freq <= self.heap[child].freq:
                    break
                self.heap[parent] = self.heap[child]
                parent = child
                child *= 2

            self.heap[parent] = last
            self.heap.pop(-1)
            return hroot
   
class Node:
    def __init__(self, freq, data, depth = 0, left = None, right = None):
        self.freq = freq
        self.data = data
        self.depth = depth
        self.left = left
        self.right = right
        
def make_tree(label):
    heap = Min_heap()
    for n in label:
        heap.insert(n)
    for i in range(1, len(label)):
        e1 = heap.delete()
        e2 = heap.delete()
        if e1.depth < e2.depth:
            new_node = Node(e1.freq+e2.freq, e2.data + e1.data, e2.depth +1 , e2, e1)
        else:  
            new_node = Node(e1.freq+e2.freq, e1.data + e2.data,e1.depth+1, e1, e2)
        heap.insert(new_node)
    root = heap.delete()
    return root

def preorder(n, code = "''"):
    if n is not None:
        print(f"({n.freq}, '{n.data}', {code})", end=' ')
        preorder(n.left, code = 1)
        preorder(n.right, code = 0)

def preorder_syb(n, symbol):
    result = []
    if n is not None:
        if n.left is None and n.right is None:
            result.append("'{0}':'{1}'".format(n.data, symbol))
        else:
            result.extend(preorder_syb(n.left, symbol=symbol + '1'))
            result.extend(preorder_syb(n.right, symbol=symbol + '0'))
    return result

label = [Node(15, 'E'), Node(12, 'T'), Node(8, 'N'), Node(6, 'I'), Node(4, 'S')]
first_label = make_tree(label)
result = preorder_syb(first_label,'')
print("Nodes by PreOrder:",end='')
preorder(first_label)
print('symbols with Codes {',end='')
print(*result,sep=',',end='')
print('}')
print()
label = [Node(45, 'A'), Node(13, 'B'), Node(12, 'C'), Node(16, 'D'), Node(9, 'E'), Node(5, 'F')]
second_label = make_tree(label)
result = preorder_syb(second_label,'')
print("Nodes by PreOrder:",end='')
preorder(second_label)
print()
print('symbols with Codes {',end='')
print(*result,sep=',',end='')
print('}')