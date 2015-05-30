#!/bin/env python
import json
import os
import argparse
import requests
import subprocess
from ricedb.rice import package, query, render, util, installer, error


class Rice(object):
    def __init__(self):
        self.renderer = render.Renderer()
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
            This swaps out the current rice for [program]
            with the specified rice.
            USAGE: rice.py --swap or -s [program] [rice]
            """
        )

        self.parser.add_argument(
            'rice', nargs='*', type=str,
            help="""
            Optional positional argument,
            used to look for packages with specified
            keywords for a specified program.
            USAGE: rice <program_name> [keyword1, keyword2, ...]]
            """
        )

        self.parser.add_argument(
            '-S', '--sync', nargs=2, type=str,
            help="""
            Unlike the default positional argument this one won't search for a
            a package using your keywords,
            you have to specify directly the name
            of the package.
            USAGE: rice -S <program_name> <package_name>
            """
        )

        self.parser.add_argument(
            '-c', '--create', nargs=1, type=str,
            help="""
            Packages a rice for a given program into a riceDB
            rice which can be
            swapped or uploaded.
            USAGE: rice -c <program_name>
            """
        )

        self.parser.add_argument(
            '-u', '--upload', nargs=2, type=str,
            help="""
            Sends a request to the riceDB server to index the package located
            at the provided URL
            USAGE: rice -u <program_name> <rice_name>
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
            self.renderer.alert("Please specify a search term")
        elif args.create:
            # -c option used
                self.create_rice(args.create[0])
        elif args.upload:
            self.upload_package(args.upload[0], args.upload[1])
        else:
            self.renderer.alert(("RiceDB should be run with arguments. "
                                 "Try rice.py -h if you are unsure about "
                                 "how to use the program"))
            exit()

    def swap_rice(self, prog_name, rice_name):
        """
        Swaps the currently active rice for a given program
        With the rice specified by the input rice_name
        """
        search = query.Query(prog_name, rice_name, True)
        result = search.get_results()
        if result:
            rice_installer = installer.Installer(prog_name, rice_name)
            if not rice_installer.check_install():
                self.create_rice(prog_name)
                rice_installer.install()
            else:
                self.renderer.alert(("This rice you tried to install "
                                     "does not exist locally, "
                                     "please try again"))
                exit()
            self.renderer.alert("Succesfully swapped to " + rice_name)

    def install_rice(self, prog_name, rice_name, force=False):
        """
        Installs a rice specified by the user.
        This function expects a unique result
        and throws an error if more than one rice
        results from the query
        """
        search = query.Query(prog_name, rice_name)
        # results is a list of packages
        results = search.get_results()
        if len(results) == 1:
            temp_pack = results[0]
            rice_installer = installer.Installer(temp_pack.program,
                                                 temp_pack.name,
                                                 temp_pack.upstream)
            rice_installer.download()
            if not rice_installer.check_install() and not force:
                self.renderer.alert(("Warning, you have unregistered rices for ",
                                     "the specified program on your computer"))
                self.renderer.alert("Please run rice -c " + prog_name +
                                    "to save your configs for the program")
                exit()
            rice_installer.install(force)
            self.update_localdb(temp_pack.name, temp_pack.program)
        else:
            self.renderer.alert(("Error, you did not specify "
                                 "a valid rice name, please try again"))
            exit()
        self.renderer.alert("Succesfully installed " + rice_name)

    def search_rice(self, prog_name, keyword):
        """
        Searches the database for rices which
        match the keyword given, then renders
        the results to allow the user to choose
        a rice to be installed
        """
        search = query.Query(prog_name, keyword)
        results = search.get_results()
        # Render in the results and get the user selection
        selection = self.renderer.pick_packs(results)
        rice_installer = installer.Installer(selection.program,
                                             selection.name,
                                             selection.upstream)
        rice_installer.download()
        if not rice_installer.check_install():
            ans = self.renderer.prompt(("This appears to be your first time "
                                        "installing a riceDB rice for this "
                                        "program. Would you like to save "
                                        "the currently installed config "
                                        "or not?\n"
                                        "Please only select n if "
                                        "you do not have any files which "
                                        "might conflict with the rice to "
                                        "be installed. y/n"))
            while not (ans == "y" or ans == "n"):
                ans = self.renderer.prompt(("Please use either y or n "
                                            "for a response"))
            if ans == "y":
                self.create_rice(prog_name)
                rice_installer.install()
            else:
                rice_installer.install(True)
        else:
            rice_installer.install()
        self.update_localdb(selection.name, selection.program)
        self.renderer.alert("Succesfully installed " + selection.name)

    def upload_package(self, prog_name, rice_name):
        """
        Uploads a package with name <rice_name>
        for program <prog_name>.
        """
        rice_path = util.RDBDIR + "/" + prog_name + "/" + rice_name
        auto = self.renderer.prompt("""Would you like to automatically
                                    create a Github repo? y/n""")
        while not (auto == "y" or auto == "n"):
                auto = self.renderer.prompt(("Please use either y or n "
                                            "for a response"))
        if(auto == "y"):
            uname = self.renderer.prompt("Please input your Github username")
            pwd = self.renderer.get_pass("Please input your Github password:")
            req_info = '{"name":"' + rice_name + "-" + prog_name + '"}'
            print(req_info)
            r = requests.post("https://api.github.com/user/repos",
                              auth=(uname, pwd), data=req_info)
            if r.status_code != 201:
                self.renderer.alert(("Repo creation failed, ensure that "
                                     "you specified a valid repository "
                                     "name and used correct credentials"))
                self.renderer.alert(r.text)
                exit()
            upstream_url = r.json()['clone_url']
            os.chdir(rice_path)
            subprocess.call(["git", "init"])
            subprocess.call(["git", "remote", "add", "origin",
                             "https://" + uname + ":" + pwd + "@github.com/" +
                             uname + "/" + rice_name + "-" +
                             prog_name + ".git"])
        else:
            upstream_url = self.renderer.prompt("What is the URL of the repo?")
        self.create_metadata(prog_name, rice_name, upstream_url)
        if auto == "y":
            subprocess.call(["git", "add", "."])
            subprocess.call(["git", "commit", "-m",
                             "'Added in RiceDB files'"])
            subprocess.call(["git", "push", "origin", "master"])
        else:
            os.chdir(rice_path)
            subprocess.call(["git", "add", "."])
            subprocess.call(["git", "commit", "-m",
                             "'Added in RiceDB files'"])
            self.renderer.alert(("Commiting changes manually, "
                                 "please enter your credentials "
                                 "to do a git push"))
            subprocess.call(["git", "push", "origin", "master"])

        with open(util.RDBDIR + "config") as config_file:
            try:
                config = json.load(config_file)
            except Exception as e:
                raise error.corruption_error("Invalid JSON: %s" % (e))
            try:
                r = requests.post(config['db'] + '/upload/',
                                  data={'upstream': upstream_url})
            except Exception as e:
                raise error.Error("Could not connect to server %s: %s" %
                                  (config["db"], e))
        if r.reason == "OK":
            self.renderer.alert("URL was succesfully uploaded")
        else:
            self.renderer.alert(("The URL was not succesfully "
                                 "uploaded, reason: ") + r.reason)

    def create_metadata(self, prog_name, rice_name, upstream):
        """
        Checks for and creates a metadata file for
        the rice <rice_name> for program <prog_name>.
        The github URL is provided as upstream.
        """
        rice_path = util.RDBDIR + "/" + prog_name + "/" + rice_name
        if not os.path.exists(rice_path):
            raise error.Error(("The rice you chose to create "
                              "metadata for does not exist"))
        os.chdir(rice_path)
        ans = "y"
        if os.path.exists("info.json"):
            ans = self.renderer.prompt(("Do you want to overwrite "
                                        "the existing metadata? y/n"))
        while not(ans == "y" or ans == "n"):
            ans = self.renderer.prompt("Please respond with either y or n")
        if ans == "y":
            desc = self.renderer.prompt(("What is the description "
                                         "for this rice?"))
            author = self.renderer.prompt("Who is the author of this rice?")
            cover = self.renderer.prompt(("Please provide a full link "
                                          "to a screenshot of this rice"))
            version = self.renderer.prompt("What is the version of this rice?")
            quit = self.renderer.prompt(("Please verify the information "
                                         "then press enter to continue, "
                                         "or type q then hit enter to exit"))
            if quit == "q":
                exit()
            with open("./info.json", "w") as fout:
                fout.write(json.dumps({"program": prog_name, "name": rice_name,
                                       "description": desc, "author": author,
                                       "cover": cover, "version": version,
                                       "upstream": upstream}))
            self.renderer.alert("Metadata was succesfully written")

    def create_rice(self, prog_name, for_upload=False):
        """
        Enables users to register existing config files
        as a ricedb rice for a given program
        """
        directory = ""
        file_list = {}
        already_installed = False
        loc = ""
        rice_name = self.renderer.prompt("Please specify the name of the rice")
        while os.path.exists(util.RDBDIR + "/" + prog_name + "/" + rice_name):
            answer = self.renderer.prompt(("Please use a rice name "
                                           "that is not already used"))
            if answer == "q":
                exit()
            else:
                rice_name = answer
        if not os.path.exists(util.RDBDIR + '/' + prog_name):
            os.makedirs(util.RDBDIR + '/' + prog_name)
        os.chdir(util.RDBDIR + '/' + prog_name)
        if os.path.exists('./.active'):
            already_installed = True
            self.renderer.alert(("Since you already have a rice installed, "
                                 "you will need to specify where "
                                 "the files of the rice you want to create "
                                 "are located as well as the location "
                                 "where the files should be installed. "
                                 "Please ensure that the folder where you're "
                                 "storing the configuration files mimics the "
                                 "true config files location "
                                 "in structure and file names"))
            self.renderer.alert(("You should also note that upon "
                                 "creation, the files which you "
                                 "specify will be moved into "
                                 "the ~/.rdb/program-name/rice-name/ folder"))
        directory = self.renderer.prompt(("Please specify the root "
                                          "directory of your "
                                          "config files e.g. for i3 "
                                          "type in ~/.i3/"))
        while not os.path.exists(os.path.expanduser(directory)):
            answer = self.renderer.prompt(("The specified directory "
                                           "does not exist. "
                                           "Try again or use q to quit"))
            if answer == "q":
                exit()
            else:
                directory = answer
        unexpanded_directory = directory
        directory = os.path.expanduser(unexpanded_directory)
        os.chdir(directory)
        if already_installed:
            loc = self.renderer.prompt(("Please specify the folder "
                                        "where your configs are being held"))
            loc = os.path.expanduser(loc)
            while not os.path.exists(loc):
                answer = self.renderer.prompt(("The specified directory "
                                               "does not exist. "
                                               "Try again or use q to quit"))
                if answer == "q":
                    exit()
                else:
                    loc = os.path.expanduser(answer)
            directory = loc
            os.chdir(directory)
        select_files = self.renderer.prompt(("Would you like to select "
                                             "individual files in the "
                                             "config folder? Otherwise "
                                             "all files are automatically "
                                             "detected and added. y/n"))
        while not (select_files == "y" or select_files == "n"):
            select_files = self.renderer.prompt("Please respond with y or n")
        if select_files == "n":
            for path, subdirs, files in os.walk("./"):
                for name in files:
                    # This will use a ./, but this should be ok,
                    # though admittedly redundant
                    if not path == "./":
                        file_list[name] = path + "/"
                    else:
                        file_list[name] = path
        else:
            answer = ""
            while not answer == "n":
                config_file = self.renderer.prompt(("Please specify where "
                                                    "the config file is "
                                                    "within the config folder "
                                                    "starting with ./ e.g. if "
                                                    "you are specifying a "
                                                    "file called col.conf "
                                                    "in some folder 'extra' "
                                                    "in your config folder, "
                                                    "use ./extra/col.conf"))
                while not os.path.exists(config_file):
                    answer = self.renderer.prompt(("The specified file "
                                                   "does not exist. "
                                                   "Try again or use q to "
                                                   "quit, or n to continue"))
                    if answer == "q":
                        exit()
                    elif answer == "n":
                        break
                    else:
                        config_file = os.path.expanduser(answer)
                else:
                    folder_loc, name = os.path.split(config_file)
                    file_list[name] = folder_loc + "/"
                    answer = self.renderer.prompt(("Would you like "
                                                   "to select "
                                                   "another file? y/n"))
                    while not (answer == "y" or answer == "n"):
                        answer = self.renderer.prompt("Please use y/n")

        os.chdir(util.RDBDIR + "/" + prog_name)
        os.mkdir(rice_name)
        os.chdir(rice_name)
        json_data = {}
        json_data["files"] = file_list
        json_data["conf_root"] = unexpanded_directory
        with open("install.json", "w") as fout:
            json.dump(json_data, fout, ensure_ascii=False)
        self.update_localdb(rice_name, prog_name)
        for k in file_list.keys():
            if not os.path.exists(directory + file_list[k] + k):
                self.renderer.alert("Could not find " +
                                    directory + file_list[k] + k)
                raise error.corruption_error("Could not find specified files")
            os.rename(directory + file_list[k] + k, "./" + k)
        if not already_installed:
            rice_installer = installer.Installer(
                prog_name,
                rice_name
            )
            rice_installer.install(True)

    def update_localdb(self, rice_name, prog_name):
        """
        Adds the rice with name <rice_name> and parent
        program <prog_name> into the local database file
        indicating that it has been registered by ricedb
        """
        with open(util.RDBDIR + "config") as config_file:
            try:
                config = json.load(config_file)
            except Exception as e:
                raise error.corruption_error("Invalid JSON: %s" % (e))
        with open(os.path.expanduser(config["localdb"])) as local_db:
            local_rices = json.load(local_db)
            if prog_name not in local_rices:
                local_rices.update({prog_name: []})
            local_rices[prog_name].append(rice_name)
        with open(os.path.expanduser(config["localdb"]), "w") as fout:
            json.dump(local_rices, fout)

    def run(self, args=""):
        self.build_arguments()
        self.handle_args(self.parser.parse_args())

if __name__ == '__main__':
    main = Rice()
    main.run()
