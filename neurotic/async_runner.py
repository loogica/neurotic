import os
import subprocess

def async_test(command):
    os.chdir(os.getcwd())
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate()
