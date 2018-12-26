import hashlib


def get_md5(file):
    m1 = hashlib.md5()
    m1.update(file.encode("utf-8"))
    token = m1.hexdigest()
    return token


# if __name__ == '__main__':
#     t = get_md5('Jhone')
#     print(t)
