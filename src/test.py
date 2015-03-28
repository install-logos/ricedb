import rice_start
from rice import installer
import unittest

class testInstaller(unittest.TestCase):

    def test_download(self):
        i3_test = installer.Installer(i3, test1, http://someurl)
        i3_test.download()
        self.assertTrue(os.path.exists(os.expanduser("~/.rdb/i3/test1")))
        self.assertTrue(os.path.isdir(os.expanduser("~/.rdb/i3/test1")))

    def test_install(self):
        i3_test = installer.Installer(i3, test1, http://someurl)
        i3_test.download()
        i3_test.install()
        self.assertFalse(os.path.exists(os.expanduser("~/.rdb/i3/test1/config")))
        self.assertTrue(os.path.exists(os.expanduser("~/.rdb/i3/test1/install.json")))

# Add in Query Return Test

# Add in Package Initialization Test

# Entire Pipeline should be tested

if __name=="main"__:
    unittest.main()

