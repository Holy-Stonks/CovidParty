from project.Methods import Methods

class Room:
    def __init__(self, size):
        self.size = size
        self.users = []
        self.isActive = False

    def start(self, sessionApi):
        self.names = [i['first_name'] for i in sessionApi.users.get(user_ids=self.users)]
        text = 'В общем чате: ' + ', '.join(self.names) + '. Приятного общения!'
        Methods.broadcast(sessionApi, self.users, text)

    def reply(self, sessionApi, user, text):
        self.names = [i['first_name'] for i in sessionApi.users.get(user_ids=self.users)]
        Methods.broadcast(sessionApi, [i for i in self.users if i != user.userId],
                          self.names[[j.userId for j in self.users].index(user.userId)] + ': ' + text)
