import random

class RedBlackTree:

	class Node:
		def __init__(self, data, is_red, left=None, right=None):
			self.data = data
			self.is_red = is_red
			self.left = left
			self.right = right

	def __init__(self):
		self.size = 0
		self.root = None

	def rotate_left(self, root):
		new_root = root.left
		temp = new_root.right
		new_root.right = root
		new_root.right.left = temp
		return new_root

	def rotate_right(self, root):
		new_root = root.right
		temp = new_root.left
		new_root.left = root
		new_root.left.right = temp
		return new_root


	def left_left(self, root):
		if (root.right and root.right.is_red):
			# Uncle is red: recolor only, no rotation
			root.left.is_red = False
			root.right.is_red = False
			root.is_red = True
			return root
		else:
			root.is_red = True
			root.left.is_red = False
			return self.rotate_left(root)

	def left_right(self, root):
		if (root.right and root.right.is_red):
			# Uncle is red: recolor only, no rotation
			root.left.is_red = False
			root.right.is_red = False
			root.is_red = True
			return root
		else:
			root.left.right.is_red = False
			root.is_red = True
			root.left = self.rotate_right(root.left)
			return self.rotate_left(root)

	def right_left(self, root):
		if (root.left and root.left.is_red):
			# Uncle is red: recolor only, no rotation
			root.right.is_red = False
			root.left.is_red = False
			root.is_red = True
			return root
		else:
			root.right.left.is_red = False
			root.is_red = True
			root.right = self.rotate_left(root.right)
			return self.rotate_right(root)

	def right_right(self, root):
		if (root.left and root.left.is_red):
			# Uncle is red: recolor only, no rotation
			root.right.is_red = False
			root.left.is_red = False
			root.is_red = True
			return root
		else:
			root.is_red = True
			root.right.is_red = False
			return self.rotate_right(root)

	"""
	bottom-up insertion
	find the place to insert, then insert a red node ()
	"""
	def insert(self, data):
		must_rotate = None # set to either "left" or "right"

		def helper(root):
			nonlocal data, must_rotate
			if (not root):
				return self.Node(data, True)


			if (data < root.data):
				root.left = helper(root.left)
				if (must_rotate is not None):
					# perform rotation left, must_rotate
					if (must_rotate == "left"):
						root = self.left_left(root)
					else:
						root = self.left_right(root)
					must_rotate = None
					return root
				# violation
				elif (root.is_red and root.left.is_red):
					# handle violation in the parent. signal parent.
					must_rotate = "left"
					return root
			else:
				root.right = helper(root.right)
				if (must_rotate is not None):
					# perform rotation left, must_rotate
					if (must_rotate == "left"):
						root = self.right_left(root)
					else:
						root = self.right_right(root)
					must_rotate = None
					return root
				# violation
				elif (root.is_red and root.right.is_red):
					# handle violation in the parent. signal parent.
					must_rotate = "right"
					return root

			return root


		if (self.contains(data)):
			raise Exception("Cannot insert {} because it already exists".format(data))
		self.root = helper(self.root)
		self.root.is_red = False
		self.size += 1


	def find_min(self, root):
		if (not root.left):
			return root.data
		return self.find_min(root.left)

	def find_max(self, root):
		if (not root.right):
			return root.data
		return self.find_max(root.right)

	# def remove(self, data):

	# 	def helper(root):
	# 		nonlocal data
	# 		if (not root):
	# 			return None
	# 		# found data
	# 		if (root.data == data):
	# 			# no children, so just remove it
	# 			if (not root.left and not root.right):
	# 				return None
	# 			# replace with minimum element in right subtree
	# 			if (root.right):
	# 				root.data = self.find_min(root.right)
	# 			# replace with maximum element in left subtree
	# 			else:
	# 				root.data = self.find_max(root.right)


	# 		# we have either replaced the deleted value or it is still to be found
	# 		# in either case, we still must remove a node from the tree (the logical
	# 		# target or the replacement)

	# 		# X is the next node, T is its sibling
	# 		X = T = None
	# 		if (data > root.data or (data == root.data and root.right)):
	# 			X = root.right
	# 			T = root.left
	# 		else:
	# 			X = root.left
	# 			T = root.right

	# 		# X is nonempty, T may be empty
	# 		root.is_red = False
	# 		X.is_red = True

	# 		# first main case: X has two black children
	# 		if ((not X.left or not X.left.is_red) and (not X.right or not X.right.is_red)):

	# 			# T is empty or does not have a red child
	# 			if (not T or ((not T.left or not T.left.is_red) and (not T.right or not T.right.is_red))):
	# 				pass

	# 			# T is nonempty and has a left red child
	# 			elif (T.left and T.left.is_red):
	# 				pass

	# 			# T is nonempty and has a right red child
	# 			else:
	# 				pass

	# 		# second main case: X has at least one red child
	# 		else:
				







	# 	if (not self.contains(data)):
	# 		raise Exception("Cannot remove {} because it does not exist".format(data))

	# 	if (self.root):
	# 		self.root.is_red = True
	# 	self.root = helper(self.root)
	# 	self.size -= 1


	"""
	is this a valid red black tree
	"""
	def is_valid(self):
		# cond1: each red node must not have a red node as a child
		# cond2: each path from a node to its leaves must have the same number of black nodes
		# cond3: root is always black
		# cond4: BST properties

		# do a preorder traversal
		def cond1(root):
			if (not root):
				return True
			if (root.is_red and (root.left and root.left.is_red or root.right and root.right.is_red)):
				return False
			return cond1(root.left) and cond1(root.right)

		def cond2(root):
			violation = False
			def helper(root):
				nonlocal violation
				if (not root):
					return 0

				left_count = helper(root.left)
				right_count = helper(root.right)

				if (left_count != right_count):
					violation = True

				return left_count + (not root.is_red)

			helper(self.root)
			return not violation

		def cond3():
			if not self.root:
				return True
			return not self.root.is_red

		def cond4(root):
			if (not root):
				return True
			if (root.left and root.left.data > root.data):
				return False
			if (root.right and root.right.data < root.data):
				return False
			return cond4(root.left) and cond4(root.right)
	
		return cond1(self.root) and cond2(self.root) and cond3() and cond4(self.root)

	def contains(self, data):
		
		def helper(root):
			nonlocal data
			if (not root):
				return False
			elif (data == root.data):
				return True
			elif (data < root.data):
				return helper(root.left)
			return helper(root.right)

		return helper(self.root)

	def __len__(self):
		return self.size

	def __repr__(self):
		return ""



if __name__ == "__main__":
	t = RedBlackTree()
	nums = list(range(-1000, 1000))
	while (nums):
		t.insert(nums.pop(random.randint(0, len(nums) - 1)))
		if not t.is_valid():
			print("invalid")
			exit(1)

	print("valid")
