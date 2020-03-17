import math
import random
import sys
import copy
inf = math.inf

sys.setrecursionlimit(7500)

class board:
    
  def __init__(self, human):

    self.game_end = False
    self.human = human
    self.ai = "O" if human == "X" else "X"
    self.players = ["X", "O"]
    self.player_won = "_"
    self.rows = 4
    self.cols = 4
    self.ai_best_pos = [-1,-1]
    self.ai_positions = []
    self.board = [["_","_","_","_"],["-","-","-","-"],["-","-","-","-"],["-","-","-","-"]]
    self.evaluations = 0

  def print_board(self):

    for row in range(len(self.board)):
      for col in range(len(self.board[row])):
        print(self.board[len(self.board[row])-1-row][col], end = " " )
      print()
    print()

  def positions_available(self):

    positions = []

    for row in range(len(self.board)):
      for col in range(len(self.board[row])):
        if self.board[row][col] == "_":
          positions.append([row,col])

    return positions
  
  def is_full(self):

    for row in range(len(self.board)):
      for col in range(len(self.board[row])):
        if self.board[row][col] == "_" or self.board[row][col] == "-":
          self.game_end = False
          return False

    self.game_end = True
    return True

  def insert(self, row, col, player):

    if self.board[row][col] == "_":
      self.board[row][col] = player

      if row+1 < len(self.board):
        self.board[row+1][col] = "_"

  def has_won(self):

    self.game_end = False #reset
    self.player_won = "-"

    # horizontal win |
    for i in self.players:
      for row in range(len(self.board)):
        for col in range(len(self.board[row])):
          if self.board[row][col] != i:
            break
          if col == len(self.board[row])-1:
            self.game_end = True
            self.player_won = i
            return True
      
      # vertical win --
      for row in range(len(self.board)):
        for col in range(len(self.board[row])):
          if self.board[col][row] != i:
            break
          if col == len(self.board)-1:
            self.game_end = True
            self.player_won = i
            return True
      
      # diagnonal win (top left to bottom right) \
      for row in range(len(self.board)):
        if self.board[row][row] != i:
          break
        if row == len(self.board)-1:
          self.game_end = True
          self.player_won = i
          return True

      # diagnonal win (bottom left to top right) /
      for row in range(len(self.board)):
        if self.board[row][len(self.board) - 1 - row] != i:
          break
        if row == len(self.board)-1:
          self.game_end = True
          self.player_won = i
          return True

    if self.is_full() and self.game_end == False:
      self.player_won = "-"

    return False

  def play(self):

    if self.human == "X":
      self.human_move()

      if self.game_end:
        self.print_board()
        return 0

      self.ai_move()

    else:
      self.ai_move()

      if self.game_end:
        self.print_board()
        return 0

      self.human_move()

    if not self.game_end:
      self.play()

  
  def human_move(self):

    self.print_board()

    row = int(input("choose row ... "))
    col = int(input("choose col ... "))

    if self.board[row][col] == "_":
      self.insert(row, col, self.human)

    self.has_won()

  def ai_move(self):

    self.ai_positions = []

    positions = self.positions_available()
    score = self.minimax(positions, 1, -inf, inf, True)

    print(score)
    # print(self.ai_best_pos)
    # print(self.ai_positions)

    self.is_full()
    self.has_won()  

    largest_score = -inf
    for i in self.ai_positions:
      if i[0] > largest_score:
        largest_score = i[0]

    ran_pos = random.choice([x for x in self.ai_positions if x[0] >= largest_score]) # random position from set of best positions

    # self.insert(self.ai_positions[0], self.ai_best_pos[1], self.ai)
    self.insert(ran_pos[1][0], ran_pos[1][1], self.ai)

  def insert_undo(self, row, col):

    self.board[row][col] = "_"

    if row + 1 < len(self.board):
      self.board[row+1][col] = "-"

  def score(self):

    if self.player_won == self.human: # human won - minimizer
      return -1
    elif self.player_won == self.ai: # AI won - maximizer
      return 1
    elif self.is_full:  # A draw
      return 0
    
  def minimax(self, positions, depth, alpha, beta, isMax):
    
    self.evaluations += 1
    self.has_won()
    # print(self.player_won)
    if self.game_end:
      # print(self.score())
      # print("__________________________")
      return self.score()
    
    if isMax == True:
      best_score = -inf
      for i in range(len(positions)):

        self.insert(positions[i][0], positions[i][1], self.ai)

        old_positions = copy.deepcopy(positions)
        if positions[i][0] + 1 < len(self.board):
          positions[i][0] = positions[i][0] + 1
        else:
          popped = positions.pop(i)

        score = self.minimax(positions, depth+1, alpha, beta, False)

        positions = old_positions
        self.insert_undo(positions[i][0], positions[i][1])

        if depth == 1:
          if best_score < score:
            self.ai_best_pos = copy.deepcopy(positions[i])
            self.ai_positions.append([score, self.ai_best_pos])
          elif best_score == score:
            self.ai_positions.append([score, copy.deepcopy(positions[i])])

        best_score = max(best_score, score)
        
        # Pruning
        alpha = max(alpha, score)
        if alpha > beta:
          break

      return best_score

    else:
      best_score = inf
      for i in range(len(positions)):

        self.insert(positions[i][0], positions[i][1], self.human)

        old_positions = copy.deepcopy(positions)
        if positions[i][0] + 1 < len(self.board):
          positions[i][0] = positions[i][0] + 1
        else:
          popped = positions.pop(i)

        score = self.minimax(positions, depth+1, alpha, beta, True)

        positions = old_positions
        self.insert_undo(positions[i][0], positions[i][1])

        if depth == 1:
          if best_score > score:
            self.ai_best_pos = copy.deepcopy(positions[i])
            self.ai_positions.append([score, self.ai_best_pos])
          elif best_score == score:
            self.ai_positions.append([score, copy.deepcopy(positions[i])])

        best_score = min(best_score, score)

        beta = min(score, beta)
        if alpha > beta:
          break
      
      return best_score

  def ai_move_random(self):

    positions = []

    for row in range(len(self.board)):
      for col in range(len(self.board[row])):
        if self.board[row][col] == "_":
          positions.append([row,col])

    coords = random.choice(positions)

    self.insert(coords[0], coords[1], self.ai)

    self.has_won()



play_as = input("Choose X or O ... ")
game = board(play_as)
game.play()
          