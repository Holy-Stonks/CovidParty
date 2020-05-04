from project.User import User
from project.Сonversation import Conv


class ConvHolder:

    SIZE = 1

    def __init__(self):
        self.rooms = {}

    def addUser(self, sessionApi, user, topic):
        user.activity = User.TRAIN
        if topic not in self.rooms:
            self.rooms[topic] = Conv(topic, ConvHolder.SIZE)
        self.rooms[topic].users.append(user)
        if len(self.rooms[topic].users) == self.rooms[topic].size:
            self.rooms[topic].start(sessionApi)
            self.rooms[topic] = Conv(topic, ConvHolder.SIZE)
