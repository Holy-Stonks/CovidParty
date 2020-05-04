from project.Server import Server

groupId = 194976607
token = '8dce15d3ade174dff6387d3d9507a959a9433d3e1298db3b6f507dc91ccfb723c70661f9ec119b5f93b8b'

if __name__ == '__main__':
    server = Server(groupId, token)
    server.listen()