from project.Chat import Room


class User:
    MAIN = 0
    CHAT = 1
    TRAIN = 2

    EMPTY = Room(0)

    def __init__(self, userId, sessionApi):
        self.userId = userId
        self.firstName = sessionApi.users.get(user_ids=self.userId)[0]['first_name']
        self.activity = User.MAIN
        self.room = User.EMPTY
