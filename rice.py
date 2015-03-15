from rice.search import search_keywords, search_packages, get_package, get_software
import argparse

parser = argparse.ArgumentParser(description='RiceDB cmdline cli')
parser.add_argument('program', help='program to rice')
parser.add_argument('rice', nargs='?', help='rice package')
parser.add_argument('-S', '--sync',
                    help='Install a package directly.')


args = parser.parse_args()
if args.sync:
    print(search_packages(args.program, args.sync, get_package))

elif args.rice:
    print(search_packages(args.program, args.rice, search_keywords))

else:
    print(get_software(args.program))
