import unittest
import database


class DatabaseTest(unittest.TestCase):
    def test_save_request_data(self):
        pass

    def test_get_request_count(self):
        self.assertIsInstance(database.get_request_count(), int)

    def test_get_successful_request_count(self):
        self.assertIsInstance(database.get_successful_request_count(), int)
