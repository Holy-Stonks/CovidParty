import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

'''
# ref = db.collection('employee').document('empdoc')
# ref.set({
#     'name':'somename',
#     'lname':'somelast',
#     'age': 24
# })
#
# ref = db.collection('employee')
# docs = ref.stream()
#
# for doc in docs:
#     print('{} -> {}'.format(doc.id, doc.to_dict()))
#
# ref=db.collection('employee')
# ref.document('BDoc').set({
#     'name':'somename',
#     'lname':'somelast',
#     'salary':10000,
#      'age': 24
# })
#
# ref=db.collection('employee')
# ref.document('BDoc').set({
#     'name':'ame',
#     'lname':'elast',
#     'salary':100,
#      'age': 25
# })
#
# docs = db.collection('employee').where('age', '>', 20).stream()
# for doc in docs:
#     print('{} -> {}'.format(doc.id, doc.to_dict()))
'''

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
        response = Firebase.db.collection('rooms').document(roomId).get()
        room = response.to_dict()
        room['roomId'] = response.id
        return room

    @staticmethod
    def addUserToRoom(user, room):
        room.users.append(user.userId)
        print('Список участников получен')
        response = Firebase.db.collection('rooms').document(str(user.roomId)).update({
            'users': room.users
        })
        if response is not None:
            return room.users, room.size

    @staticmethod
    def removeUserFromRoom(user, room):
        room.users.remove(user.userId)
        print('Список участников получен')
        response = Firebase.db.collection('rooms').document(str(user.roomId)).update({
            'users': room.users
        })
        if response is not None:
            return room.users, room.size