from project.User import User


class UserHolder:
    def __init__(self):
        self.users = []

    def createUser(self, userId, sessionApi):
        newUser = User(userId, sessionApi)
        self.users.append(newUser)
        return newUser

    def getUser(self, userId):
        for user in self.users:
            if user.userId == userId:
                return user
