def main():
    from neurotic.domain import TestReportRepository
    from coopy.base import init_persistent_system

    repository = init_persistent_system(TestReportRepository,
                                        basedir="build_history")

    import os
    print("Searching build history on %s" % (os.getcwd()))
    repository.show_history()
