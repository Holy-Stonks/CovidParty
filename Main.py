from project.Server import Server

groupId = 186994373
token = '3bf38381b151c1c77d0a92392d048981d24aa0eab788ea66df3229c486df1172cafee1f2eb1faedb82e0a'

if __name__ == '__main__':
    server = Server(groupId, token)
    server.listen()