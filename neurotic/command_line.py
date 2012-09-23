import os
import sys

from neurotic.domain import TestReportRepository
from coopy.base import init_persistent_system

repository = init_persistent_system(TestReportRepository,
                                    basedir="build_history")

def main():
    print("Searching build history on %s" % (os.getcwd()))
    mod = __import__(__name__).command_line
    if len(sys.argv) == 1:
        console_history()
    else:
        import pdb; pdb.set_trace()
        function = getattr(mod, sys.argv[1])(*sys.argv[2:])

def web():
    from neurotic.wsgi_app import app
    app.run(debug=True)

def console_history():
    repository.show_history()
