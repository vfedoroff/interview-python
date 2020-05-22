class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        n = len(s)
        index = [0] * 256
        i = res = 0
        for j in range(n):
                current = ord(s[j]) # get current character
                i = max(index[current], i) # get a max index of a char
                res = max(res, j - i + 1)
                index[current] = j + 1
        return res

if __name__ == "__main__":
    solution = Solution()
    assert solution.lengthOfLongestSubstring("abcabcbb") == 3