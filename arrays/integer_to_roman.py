class Solution:
    def intToRoman(self, num: int) -> str:
        result = []
        romans = [
            (1,"I"),
            (4, "IV"),
            (5, "V"),
            (9, "IX"),
            (10, "X"),
            (40, "XL"),
            (50, "L"),
            (90, "XC"),
            (100, "C"),
            (400, "CD"),
            (500, "D"),
            (900, "CM"),
            (1000, "M")
        ]
        romansIter = iter(reversed(romans))
        while num:
            r = next(romansIter)
            div = num // r[0]
            num %= r[0] 
            while div: 
                result.append(r[1]) 
                div -= 1
        return "".join(result)

if __name__ == "__main__":
    solution = Solution()
    assert "MCMXCIV" == solution.intToRoman(1994)