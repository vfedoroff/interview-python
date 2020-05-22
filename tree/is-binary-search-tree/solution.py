class Node:
    def __init__(self, data): 
        self.data = data  
        self.left = None  
        self.right = None 

    def __str__(self):
        return str(self.data) 

class BinarySearchTree:
    def __init__(self): 
        self.root = None

    def create(self, val):  
        if self.root == None:
            self.root = Node(val)
        else:
            current = self.root
         
            while True:
                if val < current.data:
                    if current.left:
                        current = current.left
                    else:
                        current.left = Node(val)
                        break
                elif val > current.data:
                    if current.right:
                        current = current.right
                    else:
                        current.right = Node(val)
                        break
                else:
                    break

"""
Node is defined as
self.left (the left child of the node)
self.right (the right child of the node)
self.info (the value of the node)
"""
def inOrder(root):
    result = []
    if not root:
        return result
    if root.left:
        result = result + inOrder(root.left)
    result.append(root.data)
    if root.right:
        result = result + inOrder(root.right)
    return result

"""
We know that the inorder traversal of 
a binary search tree gives a sorted order of its elements.
"""
def check_binary_search_tree_(root):
    arr = inOrder(root)
    # Lets check if arr is in sorted order or not
    for i in range(1, len(arr)):
        if arr[i] < arr[i-1]:
            return False
    return True

tree = BinarySearchTree()
t = int(input())

arr = list(map(int, input().split()))

for i in range(t):
    tree.create(arr[i])

print(check_binary_search_tree_(tree.root))

