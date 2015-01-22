import argparse
from search import RiceDBSearchManager


class RiceDBConfigManager:
	"""
	Base class for handling searching for, and retrieving
	configurations
	"""
	def __init__(self):
		self.arg_parser = argparse.ArgumentParser()
		self.arg_parser.add_argument("package_name")
		self.arg_parser.add_argument("configuration", nargs="?")

		self.search_manager = RiceDBSearchManager()

	def run(self):
		self.args = self.arg_parser.parse_args()

		self.search_manager.search(
			self.args.package_name,
			self.args.configuration
		)


if __name__ == '__main__':
	search_class = RiceDBConfigManager()
	search_class.run()
