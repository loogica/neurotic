import os
import subprocess

class NeuroticError(Exception):
    def __init__(self, content):
        self.content = content
    def __str__(self):
        return repr(self.content)

def async_test(command):
    os.chdir(os.getcwd())
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate()

    if not p.returncode == 0:
        raise NeuroticError((out, err))
