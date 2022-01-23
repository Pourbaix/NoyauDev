#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Ce fichier représente une zone de conversation.
"""

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView

from src.config import config
from src.libs.bot.commands import Commands
from src.libs.chat.gen_message import Message
from src.libs.chat.connectdb import ConnectToDb
from kivy.clock import Clock
import json

Builder.load_file("{0}/conversation.kv".format(config.VIEWS_DIR))


class ErrorWhileOpening(Exception):
    pass


class ErrorWhileWriting(Exception):
    pass


def get_username(file):
    """
    :param file: the corresponding json file
    Fetches the username from the json file.
    PRE: Having the json file with the username inside
    POST: Returns the username.
    """

    try:
        with open(file) as json_file:
            data = json.load(json_file)
            for i in data:
                return i["user_name"]
    except ErrorWhileOpening():
        print("An error has occurred while opening the username json file.")


def read(file):
    """
    :param file: the corresponding json file
    Reads and returns the data from the json file
    PRE: Having the correct json file.
    POST: Returns the data from the json file.
    """
    try:
        with open(file) as json_file:
            data = json.load(json_file)
            return data
    except ErrorWhileOpening():
        print("An error has occurred while opening the json file.")


def add_to_json(file, data):
    """
    :param file: json file
    :param data: data to be added in json file
    Opens the json file (1st parameter) and adds the data (2nd parameter) into it.
    PRE: Having existing json file and data.
    POST: Writes the data in the json file.
    """

    try:
        elements_set = []
        with open(file) as shit:
            json_file = json.load(shit)
            for i in json_file:
                elements_set.append(i)
        opened_file = open(file, "wt")
        elements_set.append(data)
        elements_set_string = json.dumps(elements_set)
        opened_file.write(elements_set_string)
        opened_file.close()
    except ErrorWhileWriting():
        print("An error has occurred while adding an element to the json file.")


def modify_json(file, state, server, channel):
    """
    :param file: the corresponding json file
    :param state: the state of the loop
    :param server: the server id
    :param channel: the channel id

    If the channel and server IDs are the current ones, it changes the state of the loop (clock) so that it can start
    or stop.
    PRE: Having the correct data format in the json file
    POST: Modifies the state of the loop.
    """
    try:
        elements_set = []
        with open(file) as shit:
            json_file = json.load(shit)
            for i in json_file:
                if (i["server"] == server) & (i["channel"] == channel):
                    elements_set.append({"server": server, "channel": channel, "state": state})
            elements_set.append(i)
        opened_file = open(file, "wt")
        elements_set_string = json.dumps(elements_set)
        opened_file.write(elements_set_string)
        opened_file.close()
    except ErrorWhileWriting():
        print("An error has occurred while modifying an element in the json file.")


def overwrite(file, data):
    """
        :param file: the json file
        :param data:
    """
    try:
        elements_set = data
        opened_file = open(file, "wt")
        elements_set_string = json.dumps(elements_set)
        opened_file.write(elements_set_string)
        opened_file.close()
    except ErrorWhileWriting():
        print("An error has occurred while modifying the json file.")


class InputsContainer(BoxLayout):
    pass


class MessageLabel(Label):
    pass


class MessageSent(MessageLabel):
    pass


class MessageReceived(MessageLabel):
    pass


class ConversationContainer(ScrollView):
    def __init__(self, channel_id, server_id):
        """
        :param channel_id: the id of the current channel
        :param server_id: the id of the current server
        Initialises the class with the channel and server id as well as the conversation and its container.
        PRE: -
        POST: Initialises the conversation
        """
        super(ConversationContainer, self).__init__()
        self.channel_id = channel_id
        self.server_id = server_id
        self.messages_box = self.ids.messages_container
        self.init_conversation(channel_id, server_id)

    def init_conversation(self, channel_id, server_id):
        """
        :param channel_id: the id of the current channel
        :param server_id: the id of the current server
        Takes the messages from the database and adds displays them in the msg container.
        PRE: Calling the function with the channel and server ID
        POST: Displays messages
        """
        print("INIT")
        message_list = []
        messages = ConnectToDb().messages
        for message in messages.find():
            message_list.append(message)

        message_list.reverse()
        for message in message_list:
            if message["room"] == channel_id:
                if message["server"] == server_id:
                    msg = MessageSent(text=message["date"] + " - " + message["user"] + "\n" + message["data"])
                    self.messages_box.add_widget(msg, len(self.messages_box.children))

    def add_message(self, msg_obj, pos="left"):
        """

        """
        msg = MessageSent()

        if pos == "right":
            msg = MessageReceived()

        msg.text = str(msg_obj.date) + " - " + msg_obj.user + "\n" + msg_obj.data


class Conversation(RelativeLayout):

    def __init__(self, channel_id, server_id):
        """
        :param channel_id: the id of the current channel
        :param server_id: the id of the current server
        Checks json file "loops" for the state of each look. If the loop's channel and server ID are the same as the
        current chat room, it puts its state at 1 and allows the loop to run and refresh the page.
        If not, the state is put at 0 and the loop stops.
        Here we also initialize the server/channel ID, the username and the widgets (to be added) in the msg box,
        as well as the Clock (loop)

        PRE:Having a json file called loops in the correct place
        POST: Starts / stops loops (clocks)
        """
        loop_list = read(config.ROOT_DIR + "\\public\\all_loops\\loops.json")
        exist = False
        for item in loop_list:
            if (item["channel"] == channel_id) & (item["server"] == server_id):
                exist = True
        if exist:
            modify_json(config.ROOT_DIR + "\\public\\all_loops\\loops.json", 1, server_id, channel_id)
        else:
            dict_loop = {"server": server_id, "channel": channel_id, "state": 1}
            add_to_json(config.ROOT_DIR + "\\public\\all_loops\\loops.json", dict_loop)
        loop_list = read(config.ROOT_DIR + "\\public\\all_loops\\loops.json")
        for item in loop_list:
            if (item["channel"] != channel_id) | (item["server"] != server_id):
                item["state"] = 0
        overwrite(config.ROOT_DIR + "\\public\\all_loops\\loops.json", loop_list)
        super(Conversation, self).__init__()
        self.messages_container = ConversationContainer(channel_id, server_id)
        self.inputs_container = InputsContainer()
        self.channel = channel_id
        self.server = server_id
        self.last_list = []
        # Here we get the username that will be attach to the message
        self.username = get_username(config.ROOT_DIR + "\\public\\user_info\\user_info.json")

        self.add_widget(self.messages_container)
        self.add_widget(self.inputs_container)
        # Begin the regular conversation update.
        self.event = Clock.schedule_interval(self.constant_update, 1.5)

    def send_message(self):
        """ If there is a message and it is not starting with "/", it adds the message and sends it to the databse.
        PRE: Having written a message
        POST: Sends the message to the database
        """
        txt = self.inputs_container.ids.message_input.text

        if txt:
            msg = Message(txt, str(self.username), self.channel, self.server)
            self.messages_container.add_message(msg)
            msg.send_to_db()

            if txt[0] == "/":
                bot = Commands(txt)
                response_from_bot = bot.result
                msg_res = Message(response_from_bot, "E-Bot", self.channel, self.server)
                self.messages_container.add_message(msg_res, pos="right")

            self.inputs_container.ids.message_input.text = ""

    def refresh(self):
        """ Refreshes the screen by deleting all the widgets.
            PRE: -
            POST: Clears screen.
        """
        print("REFRESH")
        self.messages_container.messages_box.clear_widgets()

    def constant_update(self, dt):
        """
            :param dt: needed for this operation

            If the chat is open (id & state) it loops through all messages in the database, stores them temporarily and refreshes the screen and
            reinitializes the conversation.

            PRE : Having a valid json file "loops"
            POST: Updates the conversation.
        """
        loop_list = read(config.ROOT_DIR + "\\public\\all_loops\\loops.json")
        activated = False
        for item in loop_list:
            if (item["channel"] == self.channel) & (item["server"] == self.server) & (item["state"] == 1):
                activated = True
        if activated:
            print("clock on!" + str(self.server) + str(self.channel))
            message_list = []
            messages = ConnectToDb().messages
            for message in messages.find():
                message_list.append(message)
            inthere = True
            for i in message_list:
                if i not in self.last_list:
                    inthere = False
            if not inthere:
                self.refresh()
                self.messages_container.init_conversation(self.channel, self.server)
            self.last_list = message_list
        else:
            return False
