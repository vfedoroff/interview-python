class Solution:
    def twoSum(self, nums, target):
        ret = []
        elements = dict()
        for i in range(len(nums)):
            remainder = target - nums[i]
            if remainder in elements:
                ret = [elements[remainder], i]
                break
            elements[nums[i]] = i
        return ret

if __name__ == "__main__":
    solution = Solution()
    assert solution.twoSum([2, 7, 11, 15], 9) == [0,1]