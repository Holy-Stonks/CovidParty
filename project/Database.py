import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class Firebase:

    cred = credentials.Certificate('project/firebase-sdk.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    @staticmethod
    def createUser(user):
        response = Firebase.db.collection('users').document(str(user.userId)).set({
            'userId': user.userId,
            'firstName': user.firstName,
            'activity': 0,
            'room': 0,
            'interest': '',
            'parsedInterest': []
        })
        print(response)

    @staticmethod
    def getUser(userId):
        response = Firebase.db.collection('users').document(str(userId)).get().to_dict()
        print(response)
        return response

    @staticmethod
    def userUpdate(user, field, value):
        response = Firebase.db.collection('users').document(str(user.userId)).update({
            field: value
        })
        print(response)
        return response

    @staticmethod
    def createRoom(size):
        response = Firebase.db.collection('rooms').add({
            'size': size,
            'users': [],
            'isActive': False
        })
        return response[1].id

    @staticmethod
    def roomUpdate(roomId, field, value):
        response = Firebase.db.collection('rooms').document(roomId).update({
            field: value
        })
        print(response)
        return response

    @staticmethod
    def getRoom(roomId):
        print('used')
        response = Firebase.db.collection('rooms').document(roomId).get()
        room = response.to_dict()
        room['roomId'] = response.id
        return room

    @staticmethod
    def initActiveRoom():
        response = Firebase.db.collection('rooms').where('isActive', '==', False).stream()
        roomId = [doc.id for doc in response]
        print(roomId)
        if len(roomId) == 1:
            return roomId[0]

    @staticmethod
    def addUserToRoom(user, room):
        room.users.append(user.userId)
        print('Список участников получен')
        response = Firebase.db.collection('rooms').document(room.roomId).update({
            'users': room.users
        })
        print(response)
        if response is not None:
            return room.users, room.size

    @staticmethod
    def removeUserFromRoom(user, room):
        room.users.remove(user.userId)
        print('Список участников получен')
        response = Firebase.db.collection('rooms').document(str(user.room)).update({
            'users': room.users
        })
        if response is not None:
            return room.users, room.size