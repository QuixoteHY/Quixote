
def a():
    def b():
        print('b')
        return

    b()
    print('a')
    return


a()

