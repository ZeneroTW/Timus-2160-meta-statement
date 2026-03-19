class Node: #Класс узла
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def print_tree(self):
        print(self.value)
        if self.left != None:
            self.left.print_tree()
        if self.right != None:
            self.right.print_tree()

    def size(self):
        left_size = self.left.size() if self.left != None else 0
        right_size = self.right.size() if self.right != None else 0
        counter = 1 + left_size + right_size
        return counter

class Combinatorics: #Класс Комбинаторики
    def __init__(self, N):
        self.N = N
        self.fac = list(range(self.N+1))
        self.fac[0] = 1
        for i in range(1, N+1):
            self.fac[i] *= int(self.fac[i-1])

    def C(self, n, k):
        self.n = n
        self.k = k
        return (self.fac[n])//((self.fac[n-k])*(self.fac[k]))

class Stack: #Класс Стэка
    def __init__(self):
        self.body = []

    def push(self, value: int):
        self.body.append(value)

    def pop(self):
        top = self.body[len(self.body)-1]
        self.body = self.body[:-1]
        return top
        

    def is_empty(self):
        if self.body == []:
            return True
        else:
            return False

    def top(self):
        if len(self.body) != 0:
            return self.body[len(self.body)-1]
        else:
            return None



arr = [3, 1, 2]
stk = Stack()

# Декартово дерево 
for x in arr:
    node = Node(x)
    last = None
    while stk.is_empty() == False and stk.top().value > x:
        last = stk.pop()
    node.left = last
    if stk.is_empty() == False:
        stk.top().right = node
    stk.push(node)
root = stk.body[0]
root.print_tree()


