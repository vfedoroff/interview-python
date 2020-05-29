import string
import collections
class Solution:
    def mostCommonWord(self, paragraph, banned):
        banset = set(banned)
        punctuation = r"!?',;."
        table = str.maketrans(punctuation, " " * len(punctuation))
        words = paragraph.lower().translate(table).split()
        words = [w for w in words if w not in banset]
        counter = collections.Counter(words)
        arr = counter.most_common()[0]
        return arr[0]


if __name__ == "__main__":
    s = Solution()
    assert s.mostCommonWord(
        "Bob hit a ball, the hit BALL flew far after it was hit.",
        ["hit"]) == "ball"
    assert s.mostCommonWord(
        "a, a, a, a, b,b,b,c, c",
        ["a"]) == "b"
