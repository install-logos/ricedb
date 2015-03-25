#!/bin/env python
from rice import package, query
import argparse

class Rice(object):
	def __init__(self):

		self.parser = argparse.ArgumentParser(
		    description="""
		    RiceDB is an universal configuration file manager designed to make
		    it easy to obtain configurations for any application that fit your
		    individual needs.
		    """
		)

	def build_arguments(self):
		"""
		Adds the appropriate arguments to the Rice arg parser
		"""
		self.parser.add_argument(
		    '-s', '--swap', nargs=2, type=str,
		        help="""
		        This swaps out the current rice for [program] with the specified rice.
		        USAGE: rice.py --swap or -s [program] [rice]
		        """
		)

		self.parser.add_argument(
		    'rice', nargs='*', type=str,
		    help="""
		    Optionnal positionnal argument, used to look for packages with specified
		    keywords for a specified program.
		    USAGE: rice <program_name> [keyword1, keyword2, ...]]
		    """
		)

		self.parser.add_argument(
		    '-S', '--sync', nargs=2, type=str,
		    help="""
		    Unlike the default positional argument this one won't search for a
		    a package using your keywords, you have to specify directly the name
		    of the package.
		    USAGE: rice -S <program_name> <package_name>
		    """
		)

	def handle_args(self, args):
		"""
		Determines the appropriate APIs to invoke based
		on user input
		"""
		if args.sync:
		    # -S option used,
		    query.Query(args.sync)
		elif args.swap:
		    # -s option used,
		   pass
		elif len(args.rice) > 1:
		    # Program name + keyword specified
		    results = query.Query(args.rice[1:])
		    # RENDER will handle this
		    for result in results:
		    	print(result.name)
		elif len(args.rice) == 1:
		    # Only the program name is mentionned
		    # This returns to the user popular software
		    # TODO: implement this later
		    print("Please specify a search term")
		else:
		    print("You must run rice.py with inputs. Try rice.py -h if you're unsure how to use the program")
		    exit()

	def run(self):
		self.build_arguments()
		self.handle_args(self.parser.parse_args())

if __name__ == '__main__':
	main = Rice()
	main.run()


