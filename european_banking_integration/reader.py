import csv

class Reader:
	def __init__(self, path):
		self.path =  path
		self.headers = []
		self._set_headers()

	def _set_headers(self):
		self.headers = self.next()

	def get_headers(self):
		return self.headers

	def read(self):
		for row in open(self.path, 'r'):
			yield row

	def next(self):
		return next(self.read())
	
	def _skipFirstRow(self):
		self.next()

