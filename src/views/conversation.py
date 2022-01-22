#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    [BASE]
    Ce fichier représente une zone de conversation.
"""

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView

from src.config import config
from src.libs.bot.commands import Commands
from src.models.gen_message import Message
from src.models.connectdb import ConnectToDb
from kivy.clock import Clock
import json

Builder.load_file("{0}/conversation.kv".format(config.VIEWS_DIR))


def read(file):
    with open(file) as json_file:
        data = json.load(json_file)
        return data


def add_to_json(file, data):
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


def modify_json(file, state, server, channel):
    elements_set = []
    with open(file) as shit:
        json_file = json.load(shit)
        for i in json_file:
            if (i["server"] == server) & (i["channel"] == channel):
                elements_set.append({"server": server, "channel": channel, "state": state})
        elements_set.append(i)
    print(elements_set)
    opened_file = open(file, "wt")
    elements_set_string = json.dumps(elements_set)
    opened_file.write(elements_set_string)
    opened_file.close()


def overwrite(file, data):
    try:
        elements_set = data
        opened_file = open(file, "wt")
        elements_set_string = json.dumps(elements_set)
        opened_file.write(elements_set_string)
        opened_file.close()
    except:
        pass


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
        super(ConversationContainer, self).__init__()
        self.channel_id = channel_id
        self.server_id = server_id
        self.messages_box = self.ids.messages_container
        self.init_conversation(channel_id, server_id)

    def init_conversation(self, channel_id, server_id):
        print("INIT")
        sort_da_list = []
        messages = ConnectToDb().messages
        for message in messages.find():
            sort_da_list.append(message)
        # conv_file_path = config.PUBLIC_DIR + "/tmp_conversations/basic.json"

        sort_da_list.reverse()
        for message in sort_da_list:
            if message["room"] == channel_id:
                if message["server"] == server_id:
                    msg = MessageSent(text=message["date"] + " - " + message["user"] + "\n" + message["data"])
                    self.messages_box.add_widget(msg, len(self.messages_box.children))

    def add_message(self, msg_obj, pos="left"):
        msg = MessageSent()

        if pos == "right":
            msg = MessageReceived()

        msg.text = str(msg_obj.date) + " - " + msg_obj.user + "\n" + msg_obj.data


class Conversation(RelativeLayout):

    def __init__(self, channel_id, server_id):
        loop_list = read(config.ROOT_DIR + "\\src\\views\\loops.json")
        exist = False
        for item in loop_list:
            if (item["channel"] == channel_id) & (item["server"] == server_id):
                exist = True
        if exist:
            modify_json(config.ROOT_DIR + "\\src\\views\\loops.json", 1, server_id, channel_id)
        else:
            dict_loop = {"server": server_id, "channel": channel_id, "state": 1}
            add_to_json(config.ROOT_DIR + "\\src\\views\\loops.json", dict_loop)
        loop_list = read(config.ROOT_DIR + "\\src\\views\\loops.json")
        print(loop_list)
        for item in loop_list:
            if (item["channel"] != channel_id) | (item["server"] != server_id):
                item["state"] = 0
        overwrite(config.ROOT_DIR + "\\src\\views\\loops.json", loop_list)
        super(Conversation, self).__init__()
        self.messages_container = ConversationContainer(channel_id, server_id)
        self.inputs_container = InputsContainer()
        self.channel = channel_id
        self.server = server_id
        self.last_list = []

        self.add_widget(self.messages_container)
        self.add_widget(self.inputs_container)
        # Démarrer la mise à jour régulière de la conversation
        self.event = Clock.schedule_interval(self.constant_update, 0.5)

    def send_message(self):
        txt = self.inputs_container.ids.message_input.text

        if txt:
            msg = Message(txt, "Moi", self.channel, self.server)
            self.messages_container.add_message(msg)
            msg.send_to_db()

            if txt[0] == "/":
                bot = Commands(txt)
                response_from_bot = bot.result
                msg_res = Message(response_from_bot, "E-Bot", self.channel, self.server)
                self.messages_container.add_message(msg_res, pos="right")

            self.inputs_container.ids.message_input.text = ""

    def refresh(self):
        print("REFRESH")
        self.messages_container.messages_box.clear_widgets()
        for child in self.messages_container.messages_box.children:
            print(child)

    def constant_update(self, dt):
        loop_list = read(config.ROOT_DIR + "\\src\\views\\loops.json")
        activated = False
        for item in loop_list:
            if (item["channel"] == self.channel) & (item["server"] == self.server) & (item["state"] == 1):
                activated = True
        if activated:
            print("clock on!" + str(self.server) + str(self.channel))
            sort_da_list = []
            messages = ConnectToDb().messages
            for message in messages.find():
                sort_da_list.append(message)
            inthere = True
            for i in sort_da_list:
                if i not in self.last_list:
                    inthere = False
            if not inthere:
                self.refresh()
                self.messages_container.init_conversation(self.channel, self.server)
            self.last_list = sort_da_list
        else:
            return False
