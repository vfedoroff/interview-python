"""
Given the root node of a binary search tree,
return the sum of values of all nodes with value between L and R (inclusive).

The binary search tree is guaranteed to have unique values.
"""
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def __init__(self):
        self.result = 0

    def rangeSumBST(self, root: TreeNode, L: int, R: int) -> int:
        def dfs(node: TreeNode):
            if node is None:
                return
            if L <= node.val <= R:
                self.result = self.result + node.val
            if L <= node.val:
                dfs(node.left)
                pass
            if node.val <= R:
                dfs(node.right)
        dfs(root)
        return self.result

if __name__ == "__main__":
    root: TreeNode = TreeNode(10)
    root.left: TreeNode = TreeNode(5)
    root.right: TreeNode = TreeNode(15)
    root.left.left: TreeNode = TreeNode(3)
    root.left.right: TreeNode = TreeNode(7)
    root.right.right: TreeNode = TreeNode(18)
    print(Solution().rangeSumBST(root=root, L=7, R=15))