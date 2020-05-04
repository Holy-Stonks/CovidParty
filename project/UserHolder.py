from project.User import User
from project.Database import Firebase as fb


class UserHolder:
    @staticmethod
    def createUser(sessionApi, userId):
        newUser = User(userId, sessionApi.users.get(user_ids=userId)[0]['first_name'])
        fb.createUser(newUser)
        return newUser

    @staticmethod
    def getUser(userId):
        userData = fb.getUser(userId)
        if userData is not None:
            user = User(userData['userId'], userData['firstName'])
            user.activity = userData['activity']
            user.room = userData['room']
            user.interest = userData['interest']
            user.parsedInterest = userData['parsedInterest']
            return user
