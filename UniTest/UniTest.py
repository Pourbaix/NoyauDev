from src.models.connectdb import *
from src.models.gen_message import *
import unittest


class TestGenMessage(unittest.TestCase):

    def test_init(self):
        with self.assertRaises(ParamNotStrException):
            Message(8, 10, 13, 87)
            Message("Message", 10, 13, 87)
            Message(10, "User17899", 13, 87)

    def test_db_formating(self):
        self.assertTrue(isinstance(Message("Message", "User17899", "Room2", "Server41").db_formatting(), dict))


class TestConnectDb(unittest.TestCase):

    def test_number_message(self):
        self.assertTrue(isinstance(ConnectToDb().number_message(), int))
