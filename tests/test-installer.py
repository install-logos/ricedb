from ricedb.rice import installer
import unittest, os

class testInstaller(unittest.TestCase):
    """
    Testing the Rice download and installer methods
    """
    def setUp(self):
        self.test_prog = "i3"
        self.test_package = "test1"
        self.test_url = "http://github.com/install-logos/example-repo/archive/master.zip"


    def test_download(self):
        i3_test = installer.Installer(
            self.test_prog, 
            self.test_package,
            self.test_url 
        )

        i3_test.download()
        self.assertTrue(os.path.exists(os.path.expanduser("~/.rdb/i3/test1")))
        self.assertTrue(os.path.isdir(os.path.expanduser("~/.rdb/i3/test1")))

    def test_install(self):
        i3_test = installer.Installer(
            self.test_prog, 
            self.test_package, 
            self.test_url
        )
        i3_test.download()
        i3_test.install()
        self.assertFalse(os.path.exists(os.path.expanduser("~/.rdb/i3/test1/config")))
        self.assertTrue(os.path.exists(os.path.expanduser("~/.rdb/i3/test1/install.json")))

    def tearDown(self):
        os.system("rm -rf ~/.rdb/i3/test1/")
# Add in Query Return Test

# Add in Package Initialization Test

# Entire Pipeline should be tested

if __name__=="__main__":
    unittest.main()

