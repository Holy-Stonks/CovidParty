from project.User import User
from project.Chat import Room
from random import randint


class ChatHolder:
    def __init__(self):
        self.createRoom()

    def addUser(self, sessionApi, user):
        user.activity = User.CHAT
        self.room.users.append(user)
        room = self.room
        if len(self.room.users) == self.room.size:
            self.room.start(sessionApi)
            self.createRoom()
        user.room = room

    def disconnect(self, sessionApi, user):
        user.room.reply(sessionApi, user.userId, user.firstName + ' покидает чат.')
        user.room.users.remove(user)

    def removeUser(self, sessionApi, user):
        self.disconnect(sessionApi, user)
        user.activity = User.MAIN
        user.room = User.EMPTY

    def findNext(self, sessionApi, user):
        self.disconnect(sessionApi, user)
        self.addUser(sessionApi, user)

    def createRoom(self):
        self.room = Room(randint(2, 4))
