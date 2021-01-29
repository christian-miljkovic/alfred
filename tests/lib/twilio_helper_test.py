from collections import namedtuple

import pytest


class FakeClient:
    def __init__(self, **kwargs):
        self.messages = self.MessageFactory()

    class MessageFactory:
        @staticmethod
        def create(**kwargs):
            Message = namedtuple("Message", ["sid"])
            message = Message(sid="SM87105da94bff44b999e4e6eb90d8eb6a")
            return message


def test_send_direct_message_success():
    pass