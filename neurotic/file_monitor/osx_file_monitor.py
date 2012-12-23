# coding: utf-8

import os
import time
import select
import subprocess
import glob

from select import kqueue, kevent

from neurotic.async_runner import async_test, NeuroticError
from neurotic.file_monitor import check_modifications

LIMIT = 1

def start_monitor(dirs):
    last_run = time.time()
    files_stats = []
    paths = []
    current_dir = os.getcwd()

    kq = kqueue()

    source_events = []
    for dir_name in dirs:
        dir_path = current_dir + '/' + dir_name
        paths.append(dir_path)
        fd = os.open(dir_path, os.O_RDONLY)
        event = kevent(fd, filter=select.KQ_FILTER_VNODE,
                        flags=select.KQ_EV_ADD | select.KQ_EV_CLEAR,
                        fflags=select.KQ_NOTE_WRITE)
        source_events.append(event)

    while True:
        events = kq.control(source_events,  len(source_events), 2000)
        if any(map(lambda e: e.fflags & select.KQ_NOTE_WRITE, events)):
            if (time.time() - last_run) < LIMIT:
                continue
            if check_modifications(current_dir, paths):
                try:
                    async_test(["make", "test"])
                    os.system('clear')
                    subprocess.Popen("neurotic")
                except NeuroticError as ne:
                    os.system('clear')
                    if b"ERROR" in ne.content[0]:
                        print(ne.content[0])
                    else:
                        subprocess.Popen("neurotic")
                last_run = time.time()
