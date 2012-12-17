# coding: utf-8

import os
import time
import select
import subprocess
import glob

from neurotic.async_runner import async_test, NeuroticError

last_scan_dict = {}
LIMIT = 1

def check_modifications(dirpath, paths):
    modifications = False
    local_scan_dict = {}
    global last_scan_dict

    entries = glob.glob(os.path.join(dirpath, "*.py"))

    for dirname, dirnames, filenames in os.walk(dirpath):
        if dirname in paths:
            files = glob.glob(os.path.join(os.path.abspath(dirname), '*.py'))
            if files:
                entries.extend(files)

    entries = ((time.ctime(os.stat(path).st_mtime), path)
                for path in entries if os.path.isfile(path))

    entries = set(entries)

    for cdate, path in sorted(entries):
        local_scan_dict[os.path.basename(path)] = cdate

    if not local_scan_dict == last_scan_dict:
        last_scan_dict = local_scan_dict
        modifications = True

    return modifications

if os.uname()[0] == "Linux":
    from neurotic.file_monitor import linux_file_monitor as lfm
    start_monitor = lfm.start_monitor
else:
    from neurotic.file_monitor import osx_file_monitor as ofm
    start_monitor = ofm.start_monitor
