#!/bin/env python
from rice import package, query
import argparse

parser = argparse.ArgumentParser(
    description="""
    RiceDB is an universal configuration file manager designed to make
    it easy to obtain configurations for any application that fit your
    individual needs.
    """
)

parser.add_argument(
    '-s', '--swap', nargs=2, type=str,
        help="""
        This swaps out the current rice for [program] with the specified rice.
        USAGE: rice.py --swap or -s [program] [rice]
        """
)

parser.add_argument(
    'rice', nargs='*', type=str,
    help="""
    Optionnal positionnal argument, used to look for packages with specified
    keywords for a specified program.
    USAGE: rice <program_name> [keyword1, keyword2, ...]]
    """
)

parser.add_argument(
    '-S', '--sync', nargs=2, type=str,
    help="""
    Unlike the default positionnal argument this one won't search for a
    a package using your keywords, you have to specify directly the name
    of the package.
    USAGE: rice -S <program_name> <package_name>
    """
)

args = parser.parse_args()
if args.sync:
    # -S option used,
    pkgdata = #somehow get data
    pkg = package.Package(pkgdata)
    pkg.download().install()

elif args.swap:
    # -s option used,
    swap.swap(args.swap[0], args.swap[1])
elif len(args.rice) > 1:
    # Program name + keyword specified
    search_return = search.search_packages(args.rice[0],
                                           args.rice[1:],
                                           search.search_keywords)
    new_rice.install(search_return, args.rice[0])
elif len(args.rice) == 1:
    # Only the program name is mentionned
    # Trying to get the package list of the specified program name
    search_return = search.get_software(args.rice[0])
    new_rice.install(search_return, args.rice[0])
else:
    print("You must run rice.py with inputs. Try rice.py -h if you're unsure how to use the program")
    exit()
