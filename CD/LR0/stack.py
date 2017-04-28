class MyStack(object):
	def __init__(self):
		self.items = []

	def push(self, item):
		self.items.append(item)
	
	def pop(self):
		self.items.pop()
	
	def isEmpty(self):
		return self.items == []

	def size(self):
		return len(self.items)

	def top(self):
		return self.items[-1]

	def show(self):
		print self.items