# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return "val:{0}, next:{1}".format(self.val, self.next)

class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        a = l1
        b = l2
        carry = 0
        current = result = ListNode(0)
        while (a is not None or b is not None):
            x = a.val if a else 0
            y = b.val if b else 0
            sum = carry + x + y
            carry = sum // 10 # To get a int value
            current.next = ListNode(sum % 10)
            current = current.next 
            if a: a = a.next
            if b: b = b.next
        if carry > 0:
            current.next = ListNode(carry)
        return result.next
        
if __name__ == "__main__":
    l1 = ListNode(val=2,
        next=ListNode(val=4,
            next=ListNode(val=3, next=None)))
    l2 = ListNode(val=6,
        next=ListNode(val=6,
            next=ListNode(val=4, next=None)))
    solution = Solution()
    result = solution.addTwoNumbers(l1, l2)
    print(result)
