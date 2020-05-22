def solution(matrix):
    n = len(matrix[0])
    for i in range(n // 2):
        for j in range(i, n - i - 1): 
            temp = matrix[i][j] 
            matrix[i][j] = matrix[n - 1 - j][i] 
            matrix[n - 1 - j][i] = matrix[n - 1 - i][n - 1 - j] 
            matrix[n - 1 - i][n - 1 - j] = matrix[j][n - 1 - i] 
            matrix[j][n - 1 - i] = temp 
    return matrix