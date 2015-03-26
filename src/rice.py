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
                    
        def swap_rice(self, prog_name, rice_name):
            search = Query(prog_name, rice_name)
            result = search.get_local_results()
            if result:
                installer = installer.Installer(result.program, result.name)
                installer.install()
            else:
                print("This rice you tried to install does not exist locally, please try again")
                exit()

        # Takes a program and rice name, queries for results. If there is more than one it exits and gives an error
        def install_rice(self, prog_name, rice_name):
            search = Query(prog_name, rice_name)
            # results is a list of packages
            results = search.get_results() 
            if len(results) == 1:
                temp_pack = results[0]
                installer = installer.Installer(temp_pack.program, temp_pack.name, temp_pack.url)
                installer.download()
                installer.install()
                self.update_localdb(temp_pack.name, temp_pack.program)
            else:
                print("Error, you did not specify a valid rice name, please try again")
                exit()

        def search_rice(self, prog_name, keyword):
            search = Query(prog_name, keyword)
            results = search.get_results()
            #Do something with Render
            selection = self.renderer.pick_packs(results) 
            installer = installer.Installer(selection.program, selection.name, selection.url)
            installer.download()
            if not installer.check_install():
                self.create_rice(prog_name)
            installer.install()
            self.update_localdb(selection.name, selection.program)

        def create_rice(self, prog_name):
            directory = ""
            file_list = {}
            rice_name = self.renderer.prompt("Please specify the name of the rice")
            while os.path.exists(util.RBDIR + "/" + prog_name + "/" + rice_name):
                answer = self.renderer.prompt("Please use a rice name that is not already used")
                if answer == "q":
                    exit()
                else:
                    rice_name = answer
            os.chdir(RBDIR + '/' + prog_name)
            with open('./.active','w') as fout:
                fout.write(rice_name)
            directory = os.expanduser(self.renderer.prompt("Please specify the root directory of your config files e.g. for i3 type in ~/.i3/"))
            while not os.path.exists(directory):
                answer = self.renderer.prompt("The specified directory does not exist. Try again or use q to quit")
                if answer == "q":
                    exit()
                else:
                    directory = os.expanduser(answer)
            os.chdir(directory)
            for path, subdirs, files in os.walk("./"):
                for name in files:
                    # This will use a ./, but this will be ok, though admittedly sketchy
                    file_list[name] = path
            os.chdir(util.RDBDIR + "/" + prog_name)
            os.mkdir(rice_name)
            os.chdir(rice_name)
            install_data = open("install.json")
            json.load(install_data)
            json_data.write(json.JSONEncoder().encode("files":file_list))
            json_data.write(json.JSONEncoder().encode({"path":directory}))
            json_data.close()
            self.update_localdb(rice_name, prog_name)

        def update_localdb(self, rice_name, prog_name):
            with open(util.RDBDIR + "config") as config_file:
                try:
                    config = json.load(config_file)
                except Exception as e:
                    raise error.corruption_error("Invalid JSON: %s" %(e))
            with open(config["localdb"]) as local_db:
                local_rices = json.load(local_db)
                local_rices.update({rice_name:{"name":rice_name,"program":prog_name}})
            with open(config["localdb"],"w") as fout:
                json.dump(local_rices,fout)

        def run(self):
            self.renderer = render.Render()
            self.build_arguments()
            self.handle_args(self.parser.parse_args())

if __name__ == '__main__':
    main = Rice()
    main.run()


