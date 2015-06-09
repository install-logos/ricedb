from os import system


class GitManager(object):
    """
    Adapter API for making system calls to git
    """

    def __init__(self):
        #check if git is installed by return code
        git_check = system("git > /dev/null 2>&1")

        if git_check == 32512 or git_check == 127:
            raise Exception("Git is not installed! "
                            "Git is required to upload a package")

    def init(self):
        """
        equivalent command to git init
        """
        system("git init > /dev/null 2>&1")

    def remote_add(self, remote_name, url):
        """
        Adds a new git remote
        """
        cmd = "git remote add {} {} > /dev/null 2>&1".format(remote_name, url)
        system(cmd)

    def push(self, repo, branch):
        """
        Pushes changes to a git repository
        """
        cmd = "git push {} {} > /dev/null 2>&1".format(repo, branch)
        system(cmd)

    def add(self, file="."):
        """
        Adds files to a git repository.
        adds the current directory by default
        """
        cmd = "git add {} > /dev/null 2>&1".format(file)
        system(cmd)

    def commit_all(self, message):
        """
        Commits all files changed in
        the git repository
        """
        cmd = 'git commit -am "{}" > /dev/null 2>&1'.format(message)
        system(cmd)

    def clone(self, repo, location=""):
        cmd = 'git clone {} {}'.format(repo, location)
        system(cmd)