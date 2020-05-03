from project.User import User
from project.Methods import Methods
from project.UserHolder import UserHolder
from project.RoomHolder import RoomHolder
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import vk_api


class Server():
    def __init__(self,groupId,token):
        self.vkSession = vk_api.VkApi(token=token)
        self.sessionApi = self.vkSession.get_api()
        self.longpoll = VkBotLongPoll(self.vkSession, groupId)
        self.userHolder = UserHolder()
        self.roomHolder = RoomHolder()

    def listen(self):
        for event in self.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                #print(event.message)
                user = self.userHolder.getUser(event.message['from_id'])
                if user is None:
                    user = self.userHolder.createUser(event.message['from_id'], self.sessionApi)
                self.MessageLogic(event, user)

    def roomInfo(self, user):
        # print(user.room.size)
        if len(user.room.users) == 1:
            Methods.sendMessage(self.sessionApi, user.userId, "Создана комната на " + str(user.room.size))
        elif len(user.room.users) < user.room.size:
            Methods.sendMessage(self.sessionApi, user.userId, "Вы как раз вовремя! Ждем остальных.")

    def MessageLogic(self, event, user):
        if event.message.text == 'чат' and user.activity != User.CHAT:
            self.roomHolder.addUser(self.sessionApi, user)
            self.roomInfo(user)
        elif user.activity == User.CHAT and user.room.isActive:
            if event.message.text == 'вернуться':
                self.roomHolder.removeUser(self.sessionApi, user)
            elif event.message.text == 'найти далее':
                self.roomHolder.findNext(self.sessionApi, user)
                self.roomInfo(user)
            elif user.room.isActive:
                user.room.reply(self.sessionApi, user.userId, event.message.text)
            else:
                Methods.sendMessage(self.sessionApi, user.userId, "Подождите, скоро подтянутся остальные.")
