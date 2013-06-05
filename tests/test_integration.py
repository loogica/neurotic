import sys
import pytest

def test_find_settings_module():
    from neurotic.integration import find_settings_module
    import os
    from os.path import dirname, abspath, join

    original_dir = dirname(__file__)

    # scenario 1 - current_dir/settings.py
    scenario1_path = join(join(dirname(__file__), "fixtures"), "proj1")
    assert "settings" == find_settings_module(scenario1_path)

    # scenario 2 - current_dir/django_prod/settings.py
    scenario2_path = join(join(dirname(__file__), "fixtures"), "proj2")
    assert "django_proj.settings" == find_settings_module(scenario2_path)

    # scenario 3 - current_dir/django_prod/settings/__int__.py
    scenario3_path = join(join(dirname(__file__), "fixtures"), "proj3")
    assert "django_proj.settings" == find_settings_module(scenario3_path)

    with pytest.raises(Exception):
        find_settings_module(original_dir)

    os.chdir(original_dir)


def test_find_apps():
    from neurotic.integration import find_apps
    import os
    from os.path import dirname, abspath, join

    original_dir = dirname(__file__)

    # scenario 1 - app1/models.py
    scenario1_path = join(join(dirname(__file__), "fixtures"), "proj1")
    assert ["app1"] == list(find_apps(scenario1_path))

    # scenario 2 - app1/models/__init__.py
    scenario2_path = join(join(dirname(__file__), "fixtures"), "proj2")
    assert ["app2"] == list(find_apps(scenario2_path))

    os.chdir(original_dir)


def test_find_all_tests():
    coverage = '--cov' in sys.argv
    import subprocess
    if not coverage:
        command = ["python", "t_find_all_isolated_proj1.py"]
    else:
        command = ["coverage", "run", "t_find_all_isolated_proj1.py"]
    assert "find_all_isolated_proj1 == OK\n" == subprocess.check_output(command)

def test_find_all_tests2():
    coverage = '--cov' in sys.argv
    import subprocess
    if not coverage:
        command = ["python", "t_find_all_isolated_proj2.py"]
    else:
        command = ["coverage", "run", "t_find_all_isolated_proj2.py"]
    assert "find_all_isolated_proj2 == OK\n" == subprocess.check_output(command)

def test_find_all_tests3():
    coverage = '--cov' in sys.argv
    import subprocess
    if not coverage:
        command = ["python", "t_find_all_isolated_proj3.py"]
    else:
        command = ["coverage", "run", "t_find_all_isolated_proj3.py"]
    assert "No module named app1\nfind_all_isolated_proj3 == OK\n" == \
           subprocess.check_output(command)
