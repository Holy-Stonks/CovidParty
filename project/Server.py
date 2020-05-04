from project.User import User
from project.Methods import Methods
from project.Keyboard import Keyboard
from project.UserHolder import UserHolder
from project.ChatHolder import ChatHolder
from project.ConvHolder import ConvHolder
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api


class Server():
    def __init__(self, groupId, token):
        self.vkSession = vk_api.VkApi(token=token)
        self.sessionApi = self.vkSession.get_api()
        self.longpoll = VkBotLongPoll(self.vkSession, groupId)
        self.userHolder = UserHolder()
        self.chatHolder = ChatHolder()
        self.convHolder = ConvHolder()

    def listen(self):
        for event in self.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                #print(event.message)
                user = self.userHolder.getUser(event.message['from_id'])
                if user is None:
                    user = self.userHolder.createUser(event.message['from_id'], self.sessionApi)
                if self.SecretChatLogic(event, user):
                    print('Событие в чате: ', event.message)
                elif self.SportLogic(event, user):
                    print('Спортивное событие: ', event.message)

    def SecretChatLogic(self, event, user):

        def roomInfo(user):
            if len(user.room.users) == 1:
                Methods.sendMessage(self.sessionApi, user.userId, "Создана комната на " + str(user.room.size))
            elif len(user.room.users) < user.room.size:
                Methods.sendMessage(self.sessionApi, user.userId, "Вы как раз вовремя! Ждем остальных.")

        result = True
        if event.message.text.lower() == 'чат':
            if user.activity != User.CHAT:
                self.chatHolder.addUser(self.sessionApi, user)
                roomInfo(user)
            else:
                Methods.sendMessage(self.sessionApi, user.userId, "Подождите, скоро подтянутся остальные.")
        elif user.activity == User.CHAT and user.room.isActive:
            if event.message.text.lower() == 'вернуться':
                self.chatHolder.removeUser(self.sessionApi, user)
            elif event.message.text.lower() == 'найти далее':
                self.chatHolder.findNext(self.sessionApi, user)
                roomInfo(user)
            else:
                user.room.reply(self.sessionApi, user, event.message.text)
        else:
            result = False
        return result

    def SportLogic(self, event, user):
        result = True
        if event.message.text.lower() == 'тренировка':
            Methods.sendMessage(self.sessionApi, user.userId, message='Выбери тренировку из списка:',
                                keyboard=Keyboard.createKeyboard(Keyboard.TRAIN))
        elif event.message.text.lower() in ['зарядка', 'йога']:
            self.convHolder.addUser(self.sessionApi, user, event.message.text.lower())
        else:
            result = False
        return result
