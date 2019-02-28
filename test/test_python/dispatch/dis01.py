from pydispatch import dispatcher
import logging
from quixote.signals.singalmanager import SignalManager

SIGNAL = 'aa'
SIGNAL1 = 'bb'


def c():
    pass


def handle_event(sender):
    print('signal aa is send by', sender)


def handle_event1(sender):
    print('signal bb is send by', sender)


# dispatcher.connect(handle_event, signal=SIGNAL, sender=dispatcher.Any)
# dispatcher.connect(handle_event1, signal=SIGNAL1, sender=dispatcher.Any)
# dispatcher.connect(handle_event, signal=SIGNAL, sender=dispatcher.Anonymous)
# dispatcher.connect(handle_event1, signal=SIGNAL1, sender=dispatcher.Anonymous)

if __name__ == '__main__':
    first_send = ()

    # dispatcher.send(signal=SIGNAL, sender=first_send)

    sm = SignalManager()
    sm.connect(handle_event, signal=SIGNAL)
    sm.connect(handle_event1, signal=SIGNAL1)
    # sm.sender(SIGNAL, sender=first_send)
    dispatcher.send(signal=SIGNAL, sender=first_send)
