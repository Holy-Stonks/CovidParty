from random import random


class Methods:
    @staticmethod
    def sendMessage(sessionApi, user_id, message=None, attachment=None, keyboard=None):
        sessionApi.messages.send(user_id=user_id, message=message, attachment=attachment,
                                 keyboard=keyboard, random_id=random())

    @staticmethod
    def broadcast(sessionApi, user_ids, message=None, attachment=None, keyboard=None):
        if user_ids != []:
            sessionApi.messages.send(user_ids=user_ids, message=message, attachment=attachment,
                                 keyboard=keyboard, random_id=random())
