import json

INDEX_FILE_NAME = 'index/index.json'
 
class RiceDBSearchManager:

	def __init__(self):
		pass


	def program_search(self, search_key):
		with open(INDEX_FILE_NAME, 'r') as f:
			index_file = json.loads(f.read())

		for program in index_file:
			if search_key == program['Name']:
				return True
		return False

	def search(self, program, config=None):
		if not self.program_search(program):
			print "%s not found in riceDB index" % (program)
