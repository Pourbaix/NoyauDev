def read():
    try:
        with open("test.txt") as file:
            for i in file:
                return i
    except:
        pass


def write(data):
    try:
        file = open("test.txt", "wt")
        file.write(data)
        file.close()
    except:
        pass


write("0")
print(read())
