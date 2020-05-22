class Solution:
    """
    https://www.geeksforgeeks.org/heaps-algorithm-for-generating-permutations/
    https://en.wikipedia.org/wiki/Heap%27s_algorithm#cite_note-3
    http://ruslanledesma.com/2016/06/17/why-does-heap-work.html
    """
    def permute(self, nums):
        ret = []
        def swap(nums, i, j):
            nums[i], nums[j] = nums[j], nums[i]
        def permute(nums, start, end):
            if start == end:
                ret.append(nums[:]) # Clone array
                return
            for i in range(start, end):
                # place i-th integer first in the current permutation
                swap(nums, start, i)
                # use next integers to complete the permutations
                permute(nums, start + 1, end)
                swap(nums, start, i) #backtrack
        permute(nums, 0, len(nums))
        return ret


if __name__ == "__main__":
    solution = Solution()
    print(solution.permute([1,2,3]))