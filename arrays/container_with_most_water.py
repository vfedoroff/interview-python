class Solution:
    def maxArea(self, height):
        l = 0
        r = len(height) - 1
        maxarea = 0
        while (l < r):
            width = r - l
            area = min(height[l],height[r]) * width
            maxarea = max(maxarea, area)
            if height[l] < height[r]:
                l += 1
            else:
                r -= 1
        return maxarea

if __name__ == "__main__":
    solution = Solution()
    assert solution.maxArea([1,8,6,2,5,4,8,3,7]) == 49