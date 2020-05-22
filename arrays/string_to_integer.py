class Solution:
    def myAtoi(self, str: str) -> int:
        if not str:
            return 0
        # Python integers are unbound
        INT_MAX=pow(2,31) - 1
        INT_MIN=pow(-2,31)
        ZERO = ord("0")
        NINE = ord("9")
        ALLOWED_CHARACTERS = set("+-0123456789")
        SIGNS = set("+-")
        n = len(str)
        # let find a beginning of a digit
        start = 0
        for i in range(n):
            if str[i] != " ":
                start = i
                break
        # now try that a first char is a one of allowed characters
        if str[start] not in ALLOWED_CHARACTERS:
            return 0
        is_sign_set = False
        sign = 1
        if str[start] in SIGNS:
           is_sign_set = True
           sign = 1 if str[start] == "+" else -1
           start = start + 1
        # now we're expecting digits only
        ret = 0
        for i in range(start, len(str)):
            char = ord(str[i])
            if ZERO <= char <= NINE: # It is a digit
                digit = char - ZERO
                ret = 10 * ret + digit
            else:
                break
        ret = sign * ret
        if ret < INT_MIN:
            return INT_MIN
        if ret >= INT_MAX:
            return INT_MAX
        return ret

if __name__ == "__main__":
    solution = Solution()
    assert solution.myAtoi("42") == 42
    assert solution.myAtoi(" 42") == 42
    assert solution.myAtoi("words and 987") == 0
    assert solution.myAtoi("4193 with words") == 4193
    assert solution.myAtoi("-42") == -42
    assert solution.myAtoi("4-2") == 4
    assert solution.myAtoi("--42") == 0
    assert solution.myAtoi("-91283472332") == -2147483648
    assert solution.myAtoi("   +0 123") == 0
    assert solution.myAtoi("2147483648") == 2147483647