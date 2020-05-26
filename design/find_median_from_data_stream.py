import heapq

class MedianFinder:

    __slots__ = ["lo", "hi"]

    def __init__(self):
        """
        initialize your data structure here.
        """
        self.lo = []  # max_heap containing first half of numbers
        self.hi = []  # min_heap containing second half of numbers
        

    def addNum(self, num: int) -> None:
        heapq.heappush(self.lo, -1 * num)
        heapq.heappush(self.hi, -1 * heapq.heappop(self.lo))
        if len(self.lo) < len(self.hi):
            heapq.heappush(self.lo, -1 * heapq.heappop(self.hi))

    def findMedian(self) -> float:
        ret = 0
        if len(self.lo) > len(self.hi):
            ret = -1 * self.lo[0]
        else:
            ret = (-1 * self.lo[0] + self.hi[0]) / 2
        return ret
        

if __name__ == "__main__":
    solution = MedianFinder()
    solution.addNum(41)
    assert solution.findMedian() == 41
    solution.addNum(35)
    assert solution.findMedian() == 38
    solution.addNum(62)
    assert solution.findMedian() == 41
    solution.addNum(4)
    assert solution.findMedian() == 38    