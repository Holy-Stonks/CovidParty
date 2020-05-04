from project.User import User
from project.Chat import Room
from random import randint
from project.Database import Firebase as fb


class ChatHolder:
    activeRoom = 'VVl9oC8uwhAohqF3Rb2i'

    @staticmethod
    def addUser(sessionApi, user):
        fb.userUpdate(user, 'activity', User.CHAT)
        users, size = fb.addUserToRoom(user, ChatHolder.getRoom(ChatHolder.activeRoom))
        room = ChatHolder.activeRoom
        if len(users) == size:
            Room.start(sessionApi, ChatHolder.activeRoom)
            ChatHolder.createRoom()
        fb.userUpdate(user, 'room', room)

    @staticmethod
    def getRoom(roomId):
        room = fb.getRoom(roomId)
        newRoom = Room(room['size'])
        newRoom.roomId = room['roomId']
        newRoom.users = room['users']
        newRoom.isActive = room['isActive']
        return newRoom

    @staticmethod
    def disconnect(sessionApi, user):
        room = ChatHolder.getRoom(user.room)
        room.reply(sessionApi, user.userId, user.firstName + ' покидает чат.')
        fb.removeUserFromRoom(user, ChatHolder.getRoom(user.room))

    @staticmethod
    def removeUser(sessionApi, user):
        ChatHolder.disconnect(sessionApi, user)
        fb.userUpdate(user, 'activity', User.MAIN)

    @staticmethod
    def findNext(self, sessionApi, user):
        ChatHolder.disconnect(sessionApi, user)
        ChatHolder.addUser(sessionApi, user)

    @staticmethod
    def createRoom():
        ChatHolder.activeRoom = fb.createRoom(randint(2, 4))
