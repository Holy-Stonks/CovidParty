from project.Methods import Methods


class Room:
    def __init__(self, size):
        self.size = size
        self.users = []
        self.isActive = False

    def start(self, sessionApi):
        self.names = [i.firstName for i in self.users]
        self.isActive = True
        text = 'В общем чате: ' + ', '.join(self.names) + '. Приятного общения!'
        for i in self.users:
            Methods.sendMessage(sessionApi, i.userId, text)

    def reply(self, sessionApi, from_id, text):
        for i in self.users:
            if i.userId != from_id:
                Methods.sendMessage(sessionApi, i.userId,
                                    self.names[[j.userId for j in self.users].index(from_id)] + ': ' + text)
