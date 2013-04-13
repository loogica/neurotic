import os
import sys

from neurotic.domain import TestReportRepository
from neurotic.utils import color, OK, ERROR
from coopy.base import init_persistent_system

repository = init_persistent_system(TestReportRepository,
                                    basedir="build_history")

def main():
    mod = __import__(__name__).command_line
    if len(sys.argv) == 1:
        show_last_run()
    else:
        function = getattr(mod, sys.argv[1])(sys.argv[2:])

def web(paths):
    from neurotic.wsgi_app import app
    app.run(debug=True)

def console_history(paths):
    repository.show_history()

def last_fails(paths):
    for failed in repository.last_run_failed_tests():
        print(failed)

def show_last_run():
    for report in repository.last_run_report_type():
        if report['outcome'] == "failed":
            print("%s %s\n" % (color(ERROR, color="red"),
                                     report['nodeid']))
            errors = report['longrepr']['reprtraceback']['reprentries']
            for error in errors:
                for line in error['lines']:
                    print("%s" % line)
        else:
            print("%s %s" % (color(OK, color="green"),
                             report['nodeid']))


def django_list_tests(paths):
    from neurotic.integration import (find_settings_module, find_all_tests,
                                      find_apps)
    sys.path.append(os.getcwd())
    sys.path.append(os.path.dirname(os.getcwd()))
    os.environ['DJANGO_SETTINGS_MODULE'] = find_settings_module(os.getcwd())
    names = find_all_tests(find_apps(os.getcwd()))

    for name in names:
        print(name)


def monitor(paths):
    from neurotic.file_monitor import start_monitor
    start_monitor(paths)
