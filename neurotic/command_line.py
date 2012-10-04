import os
import sys

from neurotic.domain import TestReportRepository
from neurotic.utils import color, OK, ERROR
from coopy.base import init_persistent_system

repository = init_persistent_system(TestReportRepository,
                                    basedir="build_history")

def main():
    print("Searching build history on %s" % (os.getcwd()))
    mod = __import__(__name__).command_line
    if len(sys.argv) == 1:
        show_last_run()
    else:
        function = getattr(mod, sys.argv[1])(sys.argv[2:])

def web():
    from neurotic.wsgi_app import app
    app.run(debug=True)

def console_history():
    repository.show_history()

def last_fails():
    for failed in repository.last_run_failed_tests():
        print(failed)

def show_last_run():
    for report in repository.last_run_report_type():
        if report['outcome'] == "failed":
            print("%s - %s" % (color(ERROR, color="red"),
                                   report['nodeid']))
        else:
            print("%s- %s" % (color(OK, color="green"),
                              report['nodeid']))


def monitor(paths):
    from neurotic.file_monitor import start_monitor
    start_monitor(paths)
