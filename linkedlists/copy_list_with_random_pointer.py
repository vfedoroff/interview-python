class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random

    def __repr__(self):
        return str(self.__dict__)


"""
val: an integer representing Node.val
random_index: the index of the node (range from 0 to n-1)
where random pointer points to, or null if it does not point to any node.
"""
def construct_list(arr):
    if not arr:
        return None
    nodes = [None] * len(arr)
    val = arr[0][0]
    head = Node(val)
    node = head
    nodes[0] = node
    i = 1
    for v in arr[1:]:
        node.next = Node(v[0])
        node = node.next
        nodes[i] = node
        i += 1
    random_index = arr[0][1]
    if random_index:
        head.random = nodes[random_index]
    i = 1
    for v in arr[1:]:
        random_index = v[1]
        if random_index:
            nodes[i].random = nodes[random_index]
        i += 1
    return head

class Solution:

    def __init__(self):
        # Dictionary which holds old nodes as keys and new nodes as its values.
        self.visited = {}


    def copyRandomList(self, head: 'Node') -> 'Node':
        if head == None:
            return None
        if head in self.visited:
            return self.visited[head]
        # create a new node with the value same as old node.
        node = Node(head.val, None, None)
        self.visited[head] = node
        node.next = self.copyRandomList(head.next)
        node.random = self.copyRandomList(head.random)
        return node

if __name__ == "__main__":
    solution = Solution()
    print(solution.copyRandomList(construct_list([[7,None],[13,0],[11,4],[10,2],[1,0]])))
        