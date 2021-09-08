import csv

class Reader:
	def __init__(self, handler):
		self.handler = handler 
		self.headers = []
		self._set_headers()

	def _set_headers(self):
		self.headers = self.next()

	def get_headers(self):
		return self.headers

	def read(self):
		for row in self.handler:
			yield row

	def next(self):
		return next(self.read())

	def _skipFirstRow(self):
		self.next()

