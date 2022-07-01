session_file = 'session.txt'
path_session = './server/session/'


def user(token):
    with open(path_session + session_file, 'r') as f:
        data = f.readlines()
    for line in data:
        if line.split(':')[0] == token:
            return eval(line.split(':')[1])


if __name__ == '__main__':
    print(user('c04b2264657614d582de7bda2db5f8aaf8c42f52c37bcea0ee8262ea'))
д