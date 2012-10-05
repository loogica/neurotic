# coding: utf-8

import os
import time
import select
import subprocess
import glob

from select import kqueue, kevent

from coopy.base import init_persistent_system

from neurotic.async_runner import async_test

last_scan_dict = {}

def check_modifications(dirpath):
    modifications = False
    local_scan_dict = {}
    global last_scan_dict

    entries = glob.glob(os.path.join(dirpath, "*.py"))

    for dirname, dirnames, filenames in os.walk(dirpath):
        for subdirname in dirnames:
            files = glob.glob(os.path.join(os.path.abspath(subdirname), '*.py'))
            if files:
                entries.extend(files)

    entries = ((time.ctime(os.stat(path).st_mtime), path)
                for path in entries if os.path.isfile(path))

    for cdate, path in sorted(entries):
        local_scan_dict[os.path.basename(path)] = cdate

    if not local_scan_dict == last_scan_dict:
        last_scan_dict = local_scan_dict
        modifications = True

    return modifications

def start_monitor(dirs):
    files_stats = []
    current_dir = os.getcwd()

    kq = kqueue()

    source_events = []
    for dir_name in dirs:
        dir_path = current_dir + '/' + dir_name
        fd = os.open(dir_path, os.O_RDONLY)
        event = kevent(fd, filter=select.KQ_FILTER_VNODE,
                        flags=select.KQ_EV_ADD | select.KQ_EV_CLEAR,
                        fflags=select.KQ_NOTE_WRITE)
        source_events.append(event)

    while True:
        events = kq.control(source_events,  len(source_events), 2000)
        for event in events:
            if event.fflags & select.KQ_NOTE_WRITE:
                if check_modifications(current_dir):
                    try:
                        async_test(["make", "test"])
                    except:
                        pass
                    os.system('clear')
                    subprocess.Popen("neurotic")
