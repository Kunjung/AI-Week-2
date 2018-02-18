## solve 8 puzzle game

import sys
#import resource
import time


MOVES = ['Up', 'Down', 'Left', 'Right']

GOAL = [
	['1', '2', '3'],
	['4', '5', '6'],
	['7', '8', '0']
]


GOAL = [
	['0', '1', '2'],
	['3', '4', '5'],
	['6', '7', '8']
]

class Node(object):
	def __init__(self, board_state, parent_node=None, move=None, cost=0):
		self.board_state = board_state
		self.parent_node = parent_node
		self.move = move
		self.cost = cost

	def __eq__(self, other):
		return self.board_state == other.board_state

	def get_move_list(self):
		moves = []
		prev_node = self.parent_node
		move = self.move
		moves.append(move)
		while(prev_node is not None):
			move = prev_node.move
			moves.append(move)
			prev_node = prev_node.parent_node
		moves = moves[:-1]
		return moves[::-1]	





def find_zero_position(board3x3):
	for i in range(3):
		for j in range(3):
			if board3x3[i][j] == '0':
				return (i, j)
	return False


def calculate_manhattan_distance(board3x3):
	global GOAL
	error = 0
	for i in range(3):
		for j in range(3):
			if board3x3[i][j] != GOAL[i][j]:
				error += 1
	return error



def print_board(board):
	print('**********')
	for row in board:
		for col in row:
			print(col + ' ', end='')
		print()
	print('***********')

def find_the_move(current_board, prev_board):
### find UP, down, left, right for the path using prev and current board position
	### take the difference in their 0's positions and do the math
	current_zero_pos = find_zero_position(current_board)
	i, j = current_zero_pos
	prev_zero_pos = find_zero_position(prev_board)
	pi, pj = prev_zero_pos


	row_diff = i - pi
	col_diff = j - pj

	move = None

	if col_diff == 1:
		move = 'Right'
	elif col_diff == -1:
		move = 'Left'
	elif row_diff == 1:
		move = 'Down'
	elif row_diff == -1:
		move = 'Up'

	return move


def breadth_first_search(board3x3):
	return graph_search(board3x3, 'bfs')


def depth_first_search(board3x3):
	return graph_search(board3x3, 'dfs')


#######################################
def find_new_board(board3x3, new_pos):
	### move is board3x3)
	zero_pos = find_zero_position(board3x3)
	i, j = zero_pos
	new_i, new_j = new_pos

	new_board = [x[:] for x in board3x3]
	value_to_swap = new_board[new_i][new_j]
	new_board[i][j] = value_to_swap
	new_board[new_i][new_j] = '0'

	return new_board


#### i is row and j is column so think of it like that and you'll understand
def find_all_new_board(board3x3, method):	
	i, j = find_zero_position(board3x3)
	
	candidates = [  
					(i-1, j),	#UP
					(i+1, j),	#DOWWN
					(i, j-1),	#LEFT
					(i, j+1)	#RIGHT
				]

	if method == 'dfs':
		candidates = candidates[::-1]

	new_positions = [(i, j) for (i, j) in candidates if (i >=0 and i < 3 and j >=0 and j < 3)]

	new_boards = []
	for new_pos in new_positions:
		new_boards.append(find_new_board(board3x3, new_pos))

	return new_boards
		

def remove_choice(method, frontier):
	if method == 'bfs':
		return frontier[0], frontier[1:]
	elif method == 'dfs':
		return frontier[-1], frontier[:-1]

#### working on right now #####
def graph_search(board3x3, method):
	zero_state = find_zero_position(board3x3)
	if zero_state:
		#print(zero_state)
		initial_board_state = [x[:] for x in board3x3]
		initial_node = Node(board_state=initial_board_state)
		frontier = [initial_node]
		frontier_and_explored = set()

		count = 0
		max_search_depth = 0
		while True:

			if len(frontier) == 0: return False
			### inefficient removing and updating frontier
			##current_node, frontier = remove_choice(method, frontier)
			

			## hopefully efficient frontier update
			if method == 'bfs':
				current_node = frontier.pop(0)
			elif method == 'dfs':
				current_node = frontier.pop()
			#print_board(current_node.board_state)			
			max_search_depth = max(max_search_depth, current_node.cost)
			### explored
			hash_board = find_hash_board(current_node.board_state)
			frontier_and_explored.add(hash_board)

			### check if goal is reached 
			### here goal test is done by checking for 0 sum of distance
			error = calculate_manhattan_distance(current_node.board_state)
			if error == 0:
				### WOHOO! END OF LOOP
				### GOAL Reached
				move_path = current_node.get_move_list()
				return move_path, max_search_depth, count

			### find the new board states
			new_boards = find_all_new_board(current_node.board_state, method)
			new_nodes = []
			for new_board in new_boards:
				move = find_the_move(current_board=new_board, prev_board=current_node.board_state)
				cost = current_node.cost + 1
				max_search_depth = max(max_search_depth, cost)
				new_node = Node(board_state=new_board, parent_node=current_node, move=move, cost=cost)
				new_nodes.append(new_node) 

			for new_node in new_nodes:
				# if (new_node not in frontier) and (find_hash_board(new_node.board_state) not in explored):
				if find_hash_board(new_node.board_state) not in frontier_and_explored:
					frontier.append(new_node)
					
					### set for comparison only
					hash_board = find_hash_board(new_node.board_state)
					frontier_and_explored.add(hash_board)
		
			count = count + 1
			print(count)

		
	else:
		print('0 not found')


def find_hash_board(board3x3):
	board = []
	for i in range(3):
		for j in range(3):
			board.append(board3x3[i][j])
	return tuple(board)

###########################

##################################################
### A * Search Algorithm

###################################################

def find_board_location(board, piece):
	for i in range(3):
		for j in range(3):
			if board[i][j] == piece:
				return (i, j)


def find_manhattan_distance(piece_board_location, piece_goal_location):
	bi, bj = piece_board_location
	gi, gj = piece_goal_location

	return abs(bi-gi) + abs(bj-gj)


def find_a_star_heuristic(board3x3):
	global GOAL
	heuristic = 0
	for i in range(3):
		for j in range(3):
			piece = board3x3[i][j]

			if piece != '0':
				piece_board_location = find_board_location(board3x3, piece)
				piece_goal_location = find_board_location(GOAL, piece)
				manhattan_distance = find_manhattan_distance(piece_board_location, piece_goal_location)
			
			else:
				manhattan_distance = 0
			heuristic += manhattan_distance

	return heuristic



import heapq

### A * Search ##############
### The Finale ##############
#### working on right now #####
def a_star_search(board3x3):
	zero_state = find_zero_position(board3x3)
	if zero_state:
		#print(zero_state)
		initial_board_state = [x[:] for x in board3x3]
		initial_node = Node(board_state=initial_board_state)
		initial_cost = 0 + find_a_star_heuristic(initial_board_state)
		frontier = [(initial_cost, initial_node)]
		frontier_and_explored = set()

		count = 0
		max_search_depth = 0
		while True:

			if len(frontier) == 0: return False
			
			a_star_cost, current_node = heapq.heappop(frontier)
			#print_board(current_node.board_state)			
			max_search_depth = max(max_search_depth, current_node.cost)
			### explored
			hash_board = find_hash_board(current_node.board_state)
			frontier_and_explored.add(hash_board)

			### check if goal is reached 
			### here goal test is done by checking for 0 sum of distance
			error = calculate_manhattan_distance(current_node.board_state)
			if error == 0:
				### WOHOO! END OF LOOP
				### GOAL Reached
				move_path = current_node.get_move_list()
				return move_path, max_search_depth, count

			### find the new board states
			new_boards = find_all_new_board(current_node.board_state, method)
			new_nodes = []
			for new_board in new_boards:
				move = find_the_move(current_board=new_board, prev_board=current_node.board_state)
				cost = 1 + current_node.cost
				max_search_depth = max(max_search_depth, cost)
				new_node = Node(board_state=new_board, parent_node=current_node, move=move, cost=cost)
				new_nodes.append(new_node) 

			for new_node in new_nodes:
				# if (new_node not in frontier) and (find_hash_board(new_node.board_state) not in explored):
				if find_hash_board(new_node.board_state) not in frontier_and_explored:
					
					a_star_cost = new_node.cost + find_a_star_heuristic(new_node.board_state)
					########## Push to the frontier using heappush and try to use key cost + sum of distance (error)
					heapq.heappush(frontier, (a_star_cost, new_node))
					
					### set for comparison only
					hash_board = find_hash_board(new_node.board_state)
					frontier_and_explored.add(hash_board)
		
			count = count + 1
			print(count)

		
	else:
		print('0 not found')



#########################################
### End of A * Search
###################################






if __name__ == '__main__':

#	f = open("output.txt", "wr")
	t1 = time.time()


	method = sys.argv[1]
	board = sys.argv[2]
	board = list(board.split(','))
	board3x3 = []
	board3x3.append(board[0 : 3])
	board3x3.append(board[3 : 6])
	board3x3.append(board[6 : 9])
	#print(board)
	print_board(board3x3)
	# print('NEW BOARDS')
	# for new_board in find_all_new_board(board3x3):
	# 	print_board(new_board)

	# print('NEW BOARDS')
	# print('********************')
	# new_pos = (2,0)
	# new_board = find_new_board(board3x3, new_pos)
	# print_board(new_board)
	#sys.exit('yo')


	path = None
	max_search_depth = 0
	count = 0

	if method == 'bfs':
		print('bfs')
		path, max_search_depth, count = graph_search(board3x3, 'bfs')

	elif method == 'dfs':
		print('dfs')
		path, max_search_depth, count = graph_search(board3x3, 'dfs')
	elif method == 'ast':
		path, max_search_depth, count = a_star_search(board3x3)

	t2 = time.time()
	time_taken = t2 - t1

	if path:
		print("path_to_goal: " + str(path))
		print("cost_of_path: " + str(len(path)))
		print("nodes_expanded: " + str(count))
		print("search_depth: " + str(len(path)))
		print("max_search_depth: " + str(max_search_depth))		
		print("running_time: " + str(time_taken))
		print("max_ram_usage: ")
		#print(resource.ru_maxrss)
		print("**********************")
	#for ex in explored:
	#	print(ex.move)

	

	print('Time Taken: ' + str(time_taken))

