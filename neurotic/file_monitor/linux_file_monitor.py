# coding: utf-8

import os
import time
import subprocess
import glob
import struct

from ctypes.util import find_library
from ctypes import *

from neurotic.async_runner import async_test, NeuroticError
from neurotic.file_monitor import check_modifications

LIMIT = 1

def _ctypes_inotify_configure():
    inotify = CDLL(find_library("c"), use_errno=True)

    inotify.inotify_init.argtypes = []
    inotify.inotify_init.restype = c_int

    inotify.inotify_add_watch.argtypes = [c_int, c_char_p, c_uint]
    inotify.inotify_add_watch.restype = c_int

    inotify.inotify_rm_watch.argtypes = [c_int, c_int]
    inotify.inotify_rm_watch.restype = c_int

    return inotify

def _unpack_inotify_data(data):
    wd, mask, cookie, _len = struct.unpack('iIII', data[:16])
    fname = struct.unpack('%ds' % _len, data[16:])
    return (wd, mask, cookie, fname)

def start_monitor(dirs):
    inotify = _ctypes_inotify_configure()

    last_run = time.time()
    files_stats = []
    paths = []
    current_dir = os.getcwd()

    inotify_fd = inotify.inotify_init()
    if inotify_fd == -1:
        raise Exception("Error trying to create Inotify Handler")

    source_events = []
    for dir_name in dirs:
        dir_path = current_dir + '/' + dir_name
        paths.append(dir_path)
        path_inotify_fd = inotify.inotify_add_watch(inotify_fd,
                                                    c_char_p(dir_path),
                                                    c_uint(2))
    while True:
        data = os.read(inotify_fd, 512)
        if data:
            info = _unpack_inotify_data(data)
            if (time.time() - last_run) < LIMIT:
                continue
            if check_modifications(current_dir, paths):
                try:
                    async_test(["make", "test"])
                    os.system('clear')
                    subprocess.Popen("neurotic")
                except NeuroticError as ne:
                    os.system('clear')
                    if "ERROR" in ne.content[0]:
                        print(ne.content[0])
                    else:
                        subprocess.Popen("neurotic")
                last_run = time.time()
