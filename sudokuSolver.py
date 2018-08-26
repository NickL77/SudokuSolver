import sys

#used to map each 3x3 square to their numbers 0-8
sqInd = [[[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]],
	 [[0,3], [0,4], [0,5], [1,3], [1,4], [1,5], [2,3], [2,4], [2,5]],
	 [[0,6], [0,7], [0,8], [1,6], [1,7], [1,8], [2,6], [2,7], [2,8]],
	 [[3,0], [3,1], [3,2], [4,0], [4,1], [4,2], [5,0], [5,1], [5,2]],
	 [[3,3], [3,4], [3,5], [4,3], [4,4], [4,5], [5,3], [5,4], [5,5]],
	 [[3,6], [3,7], [3,8], [4,6], [4,7], [4,8], [5,6], [5,7], [5,8]],
	 [[6,0], [6,1], [6,2], [7,0], [7,1], [7,2], [8,0], [8,1], [8,2]],
	 [[6,3], [6,4], [6,5], [7,3], [7,4], [7,5], [8,3], [8,4], [8,5]],
	 [[6,6], [6,7], [6,8], [7,6], [7,7], [7,8], [8,6], [8,7], [8,8]]]

class game:

	#board is a 9x9 array of ints with -1 representing an empty square
	def __init__(self, board):
		self.board = board

	#row and column go form 1-9
	#[1,1] represents the top left corner
	def setSquare (self, r, c, num):
		self.board[r-1][c-1] = num

	def printBoard(self):
		for i in self.board:
			print i

	def getRowNums(self, row):
		l = [False, False, False, False, False, False, False, False, False, False]
		for i in range(9):
			if self.board[row-1][i] > 0:
				l[self.board[row-1][i]] = True
		return l
	def getColNums(self, col):
		l = [False, False, False, False, False, False, False, False, False, False]
		for i in range(9):
			if self.board[i][col-1] > 0:
				l[self.board[i][col-1]] = True
		return l
	def getSquareNums(self, square):
		global sqInd
		l = [False, False, False, False, False, False, False, False, False, False]
		for coord in sqInd[square]:
			if self.board[coord[0]][coord[1]] > 0:
				l[self.board[coord[0]][coord[1]]] = True
		return l

class solver:

	def __init__(self, game):
		self.g = game
		self.solverBoard = []

		#initialize 9x9x10 array of whether a number is possible
		#index 0 of the 3rd dimension is whether or not that square has been solved
		for i in range(9):
			newa = []
			for j in range(9):
				newb = [False]
				for k in range(9):
					newb.append(True)
				newa.append(newb)
			self.solverBoard.append(newa)

		#check off given squares
		for row in range(9):
			for col in range(9):
				if game.board[row][col] > 0:
					self.solverBoard[row][col][0] = True


	#prints out which squares are solved (for debugging)
	def printWhatSolved(self):
		for i in self.solverBoard:
			for j in i:
				sys.stdout.write(str(int(j[0])) + ' ')
			print " "


	#loop through solverboard to look for arrays with only 1 possible solution
	#and enter them (in both the solverboard and actual game board)
	def updateNums(self):
		for row in range(9):
			for col in range(9):
				if not self.solverBoard[row][col][0]:
					count = 0
					num = 0
					for i in range (1,10):
						if self.solverBoard[row][col][i]:
							count += 1
							num = i
					if count == 1:
						self.solverBoard[row][col][0] = True
						game.setSquare(row + 1, col + 1, num)
	#check off what values cannot exist based on the row
	def updateRowPos(self):
		for row in range(9):
			for col in range(9):
				rowNums = self.g.getRowNums(row + 1)
				for i in range(1,10):
					if rowNums[i]:
						self.solverBoard[row][col][i] = False

	#check off what values cannot exist based on the column
	def updateColPos(self):
		for row in range(9):
			for col in range(9):
				colNums = self.g.getColNums(col + 1)
				for i in range(1,10):
					if colNums[i]:
						self.solverBoard[row][col][i] = False

	#check off what values cannot exist based on the square
	def updateSqPos(self):
		global sqInd
		for row in range(9):
			for col in range(9):
				#need to reverse find what square the point is in
				for s in range(9):
					if [row, col] in sqInd[s]:
						sq = s
				sqNums = self.g.getSquareNums(sq)
				for i in range(1,10):
					if sqNums[i]:
						self.solverBoard[row][col][i] = False

	def test(self):
		self.printWhatSolved()
		for i in range(10):
			self.updateRowPos()
			self.updateColPos()
			self.updateSqPos()
			self.updateNums()
		print " "
		self.printWhatSolved()

if __name__ == '__main__':
	b = [[ 9,  3,- 1, -1, -1, -1, -1, -1,  4],
	     [-1, -1, -1, -1,  9,  4,  5,  3,  7],
	     [ 4,  5,  1, -1,  3, -1, -1,  2,  9],
	     [ 1,  4, -1,  9, -1, -1,  6,  5, -1],
	     [-1, -1,  5,  3, -1,  1,  2,  9,  8],
	     [-1,  9,  3,  6, -1,  8, -1, -1,  1],
	     [-1,  8,  9, -1,  1, -1, -1,  4, -1],
	     [ 6,  7, -1, -1, -1,  9,  3,  1, -1],
	     [ 3, -1,  4, -1,  6, -1,  9, -1,  2]]
	
	game = game(b)	
	s = solver(game)
	s.test()
	game.printBoard()
