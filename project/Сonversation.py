from project.Methods import Methods


class Conv:
    def __init__(self, topic, size):
        self.topic = topic
        self.size = size
        self.users = []
        self.isActive = False

    def start(self, sessionApi):
        print([i.userId for i in self.users])
        self.chatId = sessionApi.messages.createChat(title=self.topic)
        link = sessionApi.messages.getInviteLink(peer_id=2_000_000_000 + self.chatId)
        Methods.broadcast(sessionApi, user_ids=[i.userId for i in self.users], message=link)
        self.isActive = True
