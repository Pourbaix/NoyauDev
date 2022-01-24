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
    print("TestGenMessage done")


class TestConnectDb(unittest.TestCase):

    def test_number_message(self):
        self.assertTrue(isinstance(ConnectToDb().number_message, int))
    print("TestConnectDb done")


class TestConversation(unittest.TestCase):

    def test_get_username(self):
        wrong_path1 = config.ROOT_DIR + "\\public\\all_loop\\test.txt"
        wrong_path2 = config.ROOT_DIR + "\\public\\ll_loops\\lets_try.json"
        with self.assertRaises(FileNotFoundError):
            # Those files don't exist
            get_username(wrong_path1)
            get_username(wrong_path2)
        self.assertTrue(isinstance(get_username(config.ROOT_DIR + "\\public\\user_info\\user_info.json"), str))

    def test_read(self):
        wrong_path1 = config.ROOT_DIR + "\\public\\allloops\\test.txt"
        wrong_path2 = config.ROOT_DIR + "\\public\\al_loops\\lets_try.json"
        with self.assertRaises(FileNotFoundError):
            # Those files don't exist
            read(wrong_path1)
            read(wrong_path2)
        self.assertTrue(isinstance(read(config.ROOT_DIR + "\\public\\all_loops\\loops.json"), list))

    def test_add_to_json(self):
        data1 = {"server": "504", "channel": "1", "state": 1}
        data2 = "ok"
        data3 = 45
        right_path = config.ROOT_DIR + "\\public\\all_loops\\loops.json"
        wrong_path1 = config.ROOT_DIR + "\\public\\all_loops\\test.txt"
        wrong_path2 = config.ROOT_DIR + "\\pulic\\all_lops\\lets_try.json"
        with self.assertRaises(FileNotFoundError):
            # Those files don't exist
            add_to_json(wrong_path1, data1)
            add_to_json(wrong_path2, data1)
        with self.assertRaises(WrongTypeError):
            # Data not valid
            add_to_json(right_path, data2)
            add_to_json(right_path, data3)

    def test_modify_json(self):
        data1 = {"server": "504", "channel": "1", "state": 1}
        right_path = config.ROOT_DIR + "\\public\\all_loops\\loops.json"
        wrong_path1 = config.ROOT_DIR + "\\pulic\\all_loops\\test.txt"
        wrong_path2 = config.ROOT_DIR + "\\public\\all_lops\\lets_try.json"
        with self.assertRaises(FileNotFoundError):
            # Those files don't exist
            modify_json(wrong_path1, data1["state"], data1["server"], data1["channel"])
            modify_json(wrong_path2, data1["state"], data1["server"], data1["channel"])
        with self.assertRaises(WrongTypeError):
            # Data not valid
            modify_json(right_path, "hello", "504", "1")
            modify_json(right_path, 1, 504, "1")
            modify_json(right_path, 1, "504", 1)

    def test_overwrite(self):
        right_path = config.ROOT_DIR + "\\public\\all_loops\\loops.json"
        wrong_path1 = config.ROOT_DIR + "\\pblic\\all_loops\\test.txt"
        wrong_path2 = config.ROOT_DIR + "\\public\\all_lops\\lets_try.json"
        datas = []
        data1 = {"server": "504", "channel": "1", "state": 1}
        datas.append(data1)
        with self.assertRaises(FileNotFoundError):
            # Those files don't exist
            overwrite(wrong_path1, datas)
            overwrite(wrong_path2, datas)
        with self.assertRaises(WrongTypeError):
            # Data not valid
            overwrite(right_path, 1)
            overwrite(right_path, "blabla")
            overwrite(right_path, data1)

    print("TestConversation done")


if __name__ == "__main__":
    unittest.main()
