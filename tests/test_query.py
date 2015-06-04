import unittest
import json
import os
from ricedb.rice import util , query


class TestQuery(unittest.TestCase):
    """
    Tests for Querying available rices
    and software packages
    """

    def setUp(self):
        self.config_file = util.RDBDIR+"config"
        self.localdb = util.RDBDIR+"db2.database"

        self.test_config_data = {
            "db": "ricedb.test.test",
            "localdb": self.localdb
        }

        self.test_db_data = {
            "i3": {
                "testricei3":
                    {
                        "name": "testricei3",
                        "ricedata": "testdata"
                    }
            }
        }

        with open(self.config_file, "w") as cf:
            cf.write(json.dumps(self.test_config_data))

        with open(self.localdb, "w") as db:
            db.write(json.dumps(self.test_db_data))

    def test_get_config_data(self):
        test_query = query.Query
        self.assertEqual(test_query.get_config_data(), self.test_config_data)

    def test_query(self):
        test_query = query.Query("i3", "testricei3", True)
        self.assertEqual(
            test_query.results,
            [{"name": "testricei3", "program": "i3"}]
        )

    def tearDown(self):
        os.system("rm -rf {}".format(self.config_file))
        os.system("rm -rf {}".format(self.localdb))


if __name__ == "__main__":
    unittest.main()


