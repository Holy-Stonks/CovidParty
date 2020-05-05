from  random import shuffle
from project.User import User
from project.Methods import Methods
from project.Keyboard import Keyboard
from project.UserHolder import UserHolder
from project.ChatHolder import ChatHolder
from project.ConvHolder import ConvHolder
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api


class Server():
    massive = list(range(457239120, 457239196))
    music = list(range(456239442, 456239839))
    shuffle(music)
    shuffle(massive)

    def __init__(self, groupId, token):
        print('Начинаю инициализацию')
        self.vkSession = vk_api.VkApi(token=token)
        self.sessionApi = self.vkSession.get_api()
        self.longpoll = VkBotLongPoll(self.vkSession, groupId)
        self.chatHolder = ChatHolder()
        self.convHolder = ConvHolder()
        print('Соединение установлено')

    def listen(self):
        for event in self.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                print(event)
                self.response = event.message.text.lower()
                user = UserHolder.getUser(event.message['from_id'])
                if user is None:
                    user = UserHolder.createUser(self.sessionApi, event.message['from_id'])
                if self.SecretChatLogic(event, user):
                    print('Событие в чате: ', event.message)
                elif self.SportLogic(user):
                    print('Беседа по интересам: ', event.message)
                elif self.SportChatLogic(event, user):
                    print('Спортивное событие: ', event.message)

    def SecretChatLogic(self, event, user):

        def roomInfo(user):
            room = ChatHolder.getRoom(user.room)
            if len(room.users) == 1:
                Methods.sendMessage(self.sessionApi, user.userId, 'Создана комната на ' + str(room.size)+ ' места.')
            elif len(room.users) < room.size:
                Methods.sendMessage(self.sessionApi, user.userId, 'Вы как раз вовремя! Ждем остальных.')

        result = True
        if self.response == 'чат':
            print(user)
            if user.activity != User.CHAT:
                self.chatHolder.addUser(self.sessionApi, user)
                roomInfo(UserHolder.getUser(user.userId))
            else:
                room = ChatHolder.getRoom(user.room)
                if room.isActive:
                    room.reply(self.sessionApi, user, event.message.text)
                else:
                    Methods.sendMessage(self.sessionApi, user.userId, "Подождите, скоро подтянутся остальные.")
        elif user.activity == User.CHAT and ChatHolder.getRoom(user.room).isActive:
            if self.response == 'вернуться':
                self.chatHolder.removeUser(self.sessionApi, user)
            elif self.response == 'найти далее':
                self.chatHolder.findNext(self.sessionApi, user)
                roomInfo(UserHolder.getUser(user.userId))
            else:
                ChatHolder.getRoom(user.room).reply(self.sessionApi, user, event.message.text)
        else:
            result = False
        return result

    def SportLogic(self, user):
        result = True
        if self.response == 'тренировка':
            Methods.sendMessage(self.sessionApi, user.userId, message='Выбери тренировку из списка:',
                                keyboard=Keyboard.createKeyboard(Keyboard.TRAIN))
        elif self.response in ['зарядка', 'йога']:
            self.convHolder.addUser(self.sessionApi, user, self.response)
        else:
            result = False
        return result

    def SportChatLogic(self, event, user):
        result = True
        if event.message.text == 'разработчики лохи':
            Methods.removeChatUser(self.sessionApi, chat_id=event.message['peer_id'] - 2_000_000_000,
                                   user_id=user.userId)
        if event.message.text == '[club186994373|@holy_stonks] Случайная музыка':
            Methods.sendChatMessage(sessionApi=self.sessionApi,
                                    attachment="audio" + "102976651" + "_" + (str)(self.music[0]),
                                    chat_id=(str)(event.message['peer_id'] - 2_000_000_000), message='',
                                    keyboard=Keyboard.createKeyboard(Keyboard.EXERCISE))
            print(event.message['peer_id'])
            self.music.pop(0)
        if event.message.text.lower() == 'гоу':
            Methods.sendChatMessage(self.sessionApi, chat_id=event.message['peer_id'] - 2_000_000_000,
                                    message='жми на кнопку:',
                                    keyboard=Keyboard.createKeyboard(Keyboard.EXERCISE))
        print(event.message.text)
        if event.message.text == '[club186994373|@holy_stonks] Упражнение':
            Methods.sendChatMessage(sessionApi=self.sessionApi,
                                    attachment="photo" + "-186994373" + "_" + (str)(self.massive[0]),
                                    chat_id=(str)(event.message['peer_id'] - 2_000_000_000), message='Just do it',
                                    keyboard=Keyboard.createKeyboard(Keyboard.EXERCISE))
            self.massive.pop(0)
        else:
            result = False
        return result
