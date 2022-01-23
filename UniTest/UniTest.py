from src.config import config
from src.libs.chat.gen_message import *
from src.views.conversation import *
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


class TestConversation(unittest.TestCase):

    def test_get_username(self):
        with self.assertRaises(ErrorWhileOpening):
            # Those files don't exist
            get_username("test.txt")
            get_username("letstry.json")
        self.assertTrue(isinstance(get_username(config.ROOT_DIR + "\\public\\user_info\\user_info.json"), str))

    def test_read(self):
        with self.assertRaises(ErrorWhileOpening):
            # Those files don't exist
            read("test.txt")
            read("letstry.json")
        self.assertTrue(isinstance(read(config.ROOT_DIR + "\\public\\user_info\\loops.json"), list))

    def test_add_to_json(self):
        with self.assertRaises(ErrorWhileWriting):
            # Those files don't exist
            read("test.txt")
            read("letstry.json")

    def test_modify_json(self):
        with self.assertRaises(ErrorWhileWriting):
            # Those files don't exist
            read("test.txt")
            read("letstry.json")

    def test_overwrite(self):
        with self.assertRaises(ErrorWhileWriting):
            # Those files don't exist
            read("test.txt")
            read("letstry.json")
