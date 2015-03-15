from rice.search import search_software, search_rice
import argparse

parser = argparse.ArgumentParser(description='RiceDB cmdline cli')
parser.add_argument('program', help='program to rice')
parser.add_argument('rice', nargs='?', help='rice package')

args = parser.parse_args()
if args.rice:
  print(search_rice(args.program, args.rice))
else:
  print(search_software(args.program))
