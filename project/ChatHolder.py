from project.User import User
from project.Chat import Room
from random import randint
from project.Database import Firebase as fb
from project.Methods import Methods


class ChatHolder:

    activeRoom = ''

    def __init__(self):
        ChatHolder.activeRoom = fb.initActiveRoom()
        if ChatHolder.activeRoom is None:
            ChatHolder.createRoom()

    @staticmethod
    def addUser(sessionApi, user):
        fb.userUpdate(user, 'activity', User.CHAT)
        activeRoom = ChatHolder.getRoom(ChatHolder.activeRoom)
        users, size = fb.addUserToRoom(user, activeRoom)
        room = ChatHolder.activeRoom
        if len(users) == size:
            activeRoom.start(sessionApi)
            fb.roomUpdate(ChatHolder.activeRoom, 'isActive', True)
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
        Methods.broadcast(sessionApi, [i for i in room.users if i != user.userId], user.firstName + ' покидает чат.')
        fb.removeUserFromRoom(user, ChatHolder.getRoom(user.room))

    @staticmethod
    def removeUser(sessionApi, user):
        ChatHolder.disconnect(sessionApi, user)
        fb.userUpdate(user, 'activity', User.MAIN)

    @staticmethod
    def findNext(sessionApi, user):
        ChatHolder.disconnect(sessionApi, user)
        ChatHolder.addUser(sessionApi, user)

    @staticmethod
    def createRoom():
        ChatHolder.activeRoom = fb.createRoom(randint(2, 4))
