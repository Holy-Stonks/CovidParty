from random import random


class Methods:
    @staticmethod
    def sendMessage(sessionApi, user_id, message):
        sessionApi.messages.send(user_id=user_id, message=message, random_id=random())