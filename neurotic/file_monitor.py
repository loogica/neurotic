import os
import time
import select

from select import kqueue, kevent

from coopy.base import init_persistent_system

from neurotic.async_runner import async_test

last_scan_dict = {}

def check_modifications(dirpath):
    modifications = False
    local_scan_dict = {}
    global last_scan_dict

    entries = (os.path.join(dirpath, fn) for fn in os.listdir(dirpath))
    entries = ((time.ctime(os.stat(path).st_mtime), path)
                for path in entries if os.path.isfile(path))

    for cdate, path in sorted(entries):
        local_scan_dict[os.path.basename(path)] = cdate

    if not local_scan_dict == last_scan_dict:
        last_scan_dict = local_scan_dict
        modifications = True

    return modifications

def start_monitor():
    files_stats = []
    current_dir = os.getcwd() + '/tests/'

    print('Watching %s dir' % (current_dir))

    fd = os.open(current_dir, os.O_RDONLY)
    kq = kqueue()

    event = kevent(fd, filter=select.KQ_FILTER_VNODE,
                       flags=select.KQ_EV_ADD | select.KQ_EV_CLEAR,
                       fflags=select.KQ_NOTE_WRITE)

    while True:
        events = kq.control([event], 1, 2000)
        for event in events:
            if event.fflags & select.KQ_NOTE_WRITE:
                if check_modifications(current_dir):
                    try:
                        async_test(["make", "test"])
                    except:
                        pass
