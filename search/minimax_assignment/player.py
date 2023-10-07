#!/usr/bin/env python3
from numpy import inf
import time

from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR


class PlayerControllerHuman(PlayerController):
	def player_loop(self):
		"""
		Function that generates the loop of the game. In each iteration
		the human plays through the keyboard and send
		this to the game through the sender. Then it receives an
		update of the game through receiver, with this it computes the
		next movement.
		:return:
		"""

		while True:
			# send message to game that you are ready
			msg = self.receiver()
			if msg["game_over"]:
				return


class PlayerControllerMinimax(PlayerController):
	def __init__(self):
		super(PlayerControllerMinimax, self).__init__()
		self.t = 0

	def player_loop(self):
		"""
		Main loop for the minimax next move search.
		:return:
		"""

		# Generate first message (Do not remove this line!)
		first_msg = self.receiver()

		while True:
			msg = self.receiver()

			# Create the root node of the game tree
			node = Node(message=msg, player=0)

			# Possible next moves: "stay", "left", "right", "up", "down"
			best_move = self.search_best_next_move(initial_tree_node=node)

			# Execute next action
			self.sender({"action": best_move, "search_time": None})


	def search_best_next_move(self, initial_tree_node):
		"""
		Use minimax (and extensions) to find best possible next move for player 0 (green boat)
		:param initial_tree_node: Initial game tree node
		:type initial_tree_node: game_tree.Node
			(see the Node class in game_tree.py for more information!)
		:return: either "stay", "left", "right", "up" or "down"
		:rtype: str
		"""

		# NOTE: Don't forget to initialize the children of the current node
		#       with its compute_and_get_children() method!
		children = initial_tree_node.compute_and_get_children()

		# Spend less than 75 ms executing this
		self.t = time.time() * 1000
		# Used to break out of outer loop
		timeout = False
		child_values = {}
		# Iterative deepening search
		for depth in range(1, 100):
			if timeout:
				break
			for child in children:
				try:
					value = self.minimax(node=child, depth=depth, alpha=-inf, beta=inf)
					child_values[value] = child
				except TimeoutError:
					timeout = True
					break

		best_value = max(child_values.keys())
		return ACTION_TO_STR[child_values[best_value].move]


	def minimax(self, node, depth, alpha, beta):
		if self.time_exceeded():
			raise TimeoutError

		# Player 0 is MAX and player 1 is MIN
		state = node.state
		player = state.get_player()
		children = node.compute_and_get_children()

		if depth == 0:
			return self.heuristic(state)

		elif len(children) == 0:
			scores = state.get_player_scores()
			return scores[0] - scores[1]

		else:
			if player == 0:
				# Move ordering
				order = {}
				for child in children:
					h_value = self.heuristic(child.state)
					order[child] = h_value
				order = dict(sorted(order.items(), key=lambda item: item[1], reverse=True))

				best_possible = -inf
				for child in order.keys():
					v = self.minimax(child, depth-1, alpha, beta)
					best_possible = max(best_possible, v)
					alpha = max(alpha, v)
					if beta <= alpha:
						break
				return best_possible

			elif player == 1:
				# Move ordering
				order = {}
				for child in children:
					h_value = self.heuristic(child.state)
					order[child] = h_value
				order = dict(sorted(order.items(), key=lambda item: item[1], reverse=False))

				best_possible = inf
				for child in order.keys():
					v = self.minimax(child, depth-1, alpha, beta)
					best_possible = min(best_possible, v)
					beta = min(beta, v)
					if beta <= alpha:
						break
				return best_possible


	# Evaluation function
	def heuristic(self, state):
		red_value = 0
		green_value = 0

		hook_positions = state.get_hook_positions()
		remaining_fishes = state.get_fish_positions()
		scores = state.get_player_scores()
		fish_scores = state.get_fish_scores()

		# We want the minimum sum of weighted manhattan distances
		for fish_index, fish_pos in remaining_fishes.items():
			green_value += self.manhattan_distance(hook_positions[0], fish_pos) * fish_scores[fish_index]
			red_value += self.manhattan_distance(hook_positions[1], fish_pos) * fish_scores[fish_index]

		# We want the maximum of (sum of weighted manhattan distances) * -1
		green_value *= -1
		red_value *= -1

		# We want the maximum score
		green_value += scores[0]
		red_value += scores[1]

		return green_value - red_value


	# Calculates the manhattan distance between two points
	def manhattan_distance(self, p1, p2):
		return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


	def time_exceeded(self):
		# Returns true if N milliseconds have passed since calling search_next_best_move
		N = 50	# 50 seems to be as a high as we can consistently go
		if time.time() * 1000 - self.t >= N:
			return True
		else:
			return False
