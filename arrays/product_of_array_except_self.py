class Solution:
    def productExceptSelf(self, nums):
        result = []
        length = len(nums)
        l = [0] * length
        l[0] = 1
        for i in range(1, length):
            l[i] = l[i-1] * nums[i-1]
        r = [0] * length
        r[length - 1] = 1
        for i in reversed(range(length-1)):
            r[i] = r[i+1] * nums[i+1]
        for i in range(length):
            result.append(l[i] * r[i])
        return result

if __name__ == "__main__":
    solution = Solution()
    result = solution.productExceptSelf([1,2,3,4])
    assert [24,12,8,6] == result