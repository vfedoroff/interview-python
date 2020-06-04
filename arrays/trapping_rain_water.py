class Solution:
    def trap(self, height):
        if not height:
            return 0
        ans = 0
        size = len(height)
        left_max = [0] * size
        right_max = [0] * size
        left_max[0] = height[0]
        for i in range(1, size):
            left_max[i] = max(height[i], left_max[i - 1])
        right_max[size - 1] = height[size - 1]
        for i in reversed(range(0, size - 1)):
            right_max[i] = max(height[i], right_max[i + 1])
        for i in range(0, size-1):
            ans += min(left_max[i], right_max[i]) - height[i]
        return ans

if __name__ == "__main__":
    solution = Solution()
    assert solution.trap([0,1,0,2,1,0,1,3,2,1,2,1]) == 6
    assert solution.trap([2,0,2]) == 2
    assert solution.trap([4,2,3]) == 1
    