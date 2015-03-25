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
                    self.install_rice(args.sync[0], args.sync[1])
		elif args.swap:
		    # -s option used,
                    self.swap_rice(args.swap[0], args.swap[1])
		elif len(args.rice) > 1:
		    # Program name + keyword specified
                    self.search_rice(args.rice[0], args.rice[1])
		elif len(args.rice) == 1:
		    # Only the program name is mentionned
		    # This returns to the user popular software
		    # TODO: implement this later
		    print("Please specify a search term")
		else:
		    print("You must run rice.py with inputs. Try rice.py -h if you're unsure how to use the program")
		    exit()
                    
        def swap_rice(prog_name, rice_name):
            search = Query(prog_name, rice_name)
            result = search.get_local_results()
            if result:
                installer = installer.Installer(result.program, result.name)
                installer.install()
            else:
                print("This rice you tried to install does not exist locally, please try again")
                exit()

        # Takes a program and rice name, queries for results. If there is more than one it exits and gives an error
        def install_rice(prog_name, rice_name):
            search = Query(prog_name, rice_name)
            # results is a list of packages
	    results = search.get_results() 
            if len(results) == 1:
                temp_pack = results[0]
                installer = installer.Installer(temp_pack.program, temp_pack.name, temp_pack.url)
                installer.download()
                installer.install()
            else:
                print("Error, you did not specify a valid rice name, please try again")
                exit()

        def search_rice(prog_name, keyword):
            search = Query(prog_name, keyword)
            results = search.get_results()
            #Do something with Render
            renderer = render.Render(results) 
            selection = renderer.prompt()
            installer = installer.Installer(selection.program, selection.name, selection.url)
            installer.download()
            installer.install()

	def run(self):
		self.build_arguments()
		self.handle_args(self.parser.parse_args())

if __name__ == '__main__':
	main = Rice()
	main.run()


