import math
import random
# inf = math.inf

class board:
    
  def __init__(self, human):

    self.end = False
    self.human = human
    self.ai = "O" if human == "X" else "X"
    self.players = ["X", "O"]
    self.rows = 4
    self.cols = 4
    self.board = [["_","_","_","_"],["-","-","-","-"],["-","-","-","-"],["-","-","-","-"]]

  def print_board(self):

    for row in range(len(self.board)):
      for col in range(len(self.board[row])):
        print(self.board[len(self.board[row])-1-row][col], end = " " )
      print()
    print()

  def has_won(self):

    # Vertical win |
    for i in self.players:
      for row in range(len(self.board)):
        for col in range(len(self.board[row])):
          if self.board[row][col] != i:
            break
          if col == len(self.board[row])-1:
            self.end = True
            return True
      
      # Horizontal win --
      for row in range(len(self.board)):
        for col in range(len(self.board[row])):
          if self.board[col][row] != i:
            break
          if col == len(self.board)-1:
            self.end = True
            return True
      
      # diagnonal win (top left to bottom right) \
      for row in range(len(self.board)):
        if self.board[row][row] != i:
          break
        if row == len(self.board)-1:
          self.end = True
          return True

      # diagnonal win (bottom left to top right) /
      for row in range(len(self.board)):
        if self.board[row][len(self.board) - 1 - row] != i:
          break
        if row == len(self.board)-1:
          self.end = True
          return True

    return False

  def is_empty(self):

    for row in range(len(self.board)):
      for col in range(len(self.board[row])):
        if self.board[row][col] == "_" or self.board[row][col] == "-":
          return False

    self.end = True
    return True

  def insert(self, row, col, player):

    if self.board[row][col] == "_":
      self.board[row][col] = player
      self.board[row+1][col] = "_"

  def play(self):

    if self.human == "X":
      self.human_move()
      self.ai_move()

    else:
      self.ai_move()
      self.human_move()

    self.play()
  
  def human_move(self):

    return 0

  def ai_move(self):

    positions = []

    for row in range(len(self.board)):
      for col in range(len(self.board[row])):
        if self.board[row][col] == "_":
          positions.append([row,col])

    coords = random.choice(positions)

    self.insert(self, coords[0], coords[1], self.ai)



play_as = input("Choose X or O ... ")
game = board(play_as)
game.print_board()
game.insert(0,0,"X")
game.print_board()
          