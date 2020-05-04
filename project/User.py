class User:
    MAIN = 0
    CHAT = 1
    TRAIN = 2

    EMPTY = ''

    def __init__(self, userId, firstName):
        self.userId = userId
        self.firstName = firstName
        self.activity = User.MAIN
        self.room = User.EMPTY
