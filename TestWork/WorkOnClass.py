MOD = 10**9 + 7

class Node: #Класс узла
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.size_val = 1

    def print_tree(self):
        print(self.value)
        if self.left != None:
            self.left.print_tree()
        if self.right != None:
            self.right.print_tree()

class Combinatorics:
    def __init__(self, n):
        self.n = n
        self.fac = [1] * (n + 1)
        self.invfac = [1] * (n + 1)
        for i in range(1, n + 1):
            self.fac[i] = self.fac[i-1] * i % MOD
        self.invfac[n] = pow(self.fac[n], MOD - 2, MOD)
        for i in range(n, 0, -1):
            self.invfac[i-1] = self.invfac[i] * i % MOD

    def C(self, n, k):
        if k < 0 or k > n:
            return 0
        return self.fac[n] * self.invfac[k] % MOD * self.invfac[n-k] % MOD

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

class CartesianTree:
    def __init__(self, arr):
        self.arr = arr
        self.comb = Combinatorics(len(arr))

    def build(self):
        stk = Stack()
        for x in self.arr:
            node = Node(x)
            last = None
            while stk.is_empty() == False and stk.top().value > x:
                last = stk.pop()
            node.left = last
            if stk.is_empty() == False:
                stk.top().right = node
            stk.push(node)
        return stk.body[0]
    
    def count(self, root):
        stack = [root]
        order = []
        result = 1

        while stack:
            node = stack.pop()
            if node:
                order.append(node)
                stack.append(node.left)
                stack.append(node.right)

        for node in reversed(order):
            L = node.left.size_val if node.left else 0
            R = node.right.size_val if node.right else 0
            node.size_val = 1 + L + R
            

        for node in order:
            L = node.left.size_val if node.left else 0
            R = node.right.size_val if node.right else 0
            result *= self.comb.C(L+R, L)
        return result

# N = int(input())        
# arr = list(map(int, input().split()))
# ct = CartesianTree(arr)
# root = ct.build()
# print(ct.count(root)%(10**9 + 7))

arr = [3, 1, 4, 2]
ct = CartesianTree(arr)
root = ct.build()
root.print_tree()