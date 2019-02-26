from pydispatch import dispatcher

SIGNAL = 'aa'
SIGNAL1 = 'bb'


def handle_event(sender):
    print('signal aa is send by', sender)


def handle_event1(sender):
    print('signal bb is send by', sender)


dispatcher.connect(handle_event, signal=SIGNAL, sender=dispatcher.Any)
dispatcher.connect(handle_event1, signal=SIGNAL1, sender=dispatcher.Any)

if __name__ == '__main__':
    first_send = ()

    dispatcher.send(signal=SIGNAL, sender=first_send)
