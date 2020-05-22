def solution(maze, n):
    # Type your solution here
    def find_path(x, y):
      if x not in range (0, n):
        return False
      if y not in range (0, n):
        return False
      if x == n-1 and y == n-1:
         return maze[x][y]==0
      if maze[x][y]>0:
        return False
      maze[x][y]=3  
      if find_path(x+1, y):
         return True
      if find_path(x, y+1):
          return True
      if find_path(x-1, y):
          return True
      if find_path(x, y-1):
          return True
      return False
    return find_path(0,0)
print(solution([[0, 1, 1], [0, 1, 1], [0, 0, 0]], 3))
print(solution([[0, 1], [0, 1]], 2))
print(solution([[0, 0], [0, 0]],2))