from src.libs.chat.connectdb import ConnectToDb
from datetime import *


class ParamNotStrException(Exception):
    pass


class Message:
    """Represents a Message sent in the chatroom.
    PRE: -
    POST: Formats and sends message to database.
    """
    def __init__(self, data, user, room, server):
        """Initializes with the current time & date, the data, room and server.
        PRE: -
        POST: Initializes current time & date, the data, room and server"""

        if type(data) != str or type(user) != str:
            raise ParamNotStrException("One of the argument is not a string.")
        self.data = data
        now = datetime.now()
        msg_date = now.strftime("%d/%m/%Y %H:%M")
        self.date = msg_date
        self.user = user
        self.room = room
        self.server = server

    def db_formatting(self):
        """Returns a dictionary with the correct format for the databse.
        PRE: Having a database
        POST: Formats the data.
        """

        return {
            "room": self.room,
            "timestamp": str(self.date),
            "msg": self.data,
            "sender": self.user
        }

    def send_to_db(self):
        """Sends the data (message) to the database.
        PRE: Having a database.
        POST: Inserts data into database.
        """

        message = {
            "server": self.server,
            "room": self.room,
            "data": self.data,
            "date": self.date,
            "user": self.user
        }
        ConnectToDb().messages.insert_one(message)
