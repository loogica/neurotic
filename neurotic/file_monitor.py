import os
import select
from select import kqueue, kevent

from neurotic.async_runner import async_test

def start_monitor():
    current_dir = os.getcwd() + '/tests/'
    print('Watching %s dir' % (current_dir))
    fd = os.open(current_dir, os.O_RDONLY)
    kq = kqueue()

    event = kevent(fd, filter=select.KQ_FILTER_VNODE,
                       flags=select.KQ_EV_ADD |
                             select.KQ_EV_ENABLE |
                             select.KQ_EV_CLEAR,
                       fflags=select.KQ_NOTE_WRITE |
                              select.KQ_NOTE_EXTEND)

    while True:
        events = kq.control([event], 1, None)
        for event in events:
            if event.fflags & select.KQ_NOTE_EXTEND or \
               event.fflags & select.KQ_NOTE_WRITE:
                async_test(["make", "test"])

start_monitor()
