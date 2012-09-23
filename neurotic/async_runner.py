import os
import subprocess

def async_test(command):
    os.chdir(os.getcwd())
    print("Running %s on %s" % (command, os.getcwd()))
    subprocess.call(command)
