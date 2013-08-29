import unittest
from neurotic.report_plugin import parse_nodeid, extract_docstr

def test_parse_pytest_nodeid_func():
    nodeid = 'tests/test_report_plugin.py::test_pytest_report_teststatus'

    blocks = parse_nodeid(nodeid)
    assert 'tests/test_report_plugin.py' == blocks['test_module']
    assert 'test_pytest_report_teststatus' == blocks['func']

def test_parse_pytest_nodeid():
    nodeid = 'tests/test_report_plugin.py::DummyTestCase::test_assert'

    blocks = parse_nodeid(nodeid)
    assert 'tests/test_report_plugin.py' == blocks['test_module']
    assert 'DummyTestCase' == blocks['test_case']
    assert 'test_assert' == blocks['func']


def test_check_func_docstring():
    '''docstring value
    '''

    blocks = dict(test_module='tests/test_report_plugin.py',
                  test_case=None,
                  func='test_check_func_docstring')

    assert dict(func_docstr='docstring value\n    ',
                class_docstr=None) == extract_docstr(blocks)

def test_check_class_docstring():
    '''docstring value
    '''

    blocks = dict(test_module='tests/test_report_plugin.py',
                  test_case='DummyTestCase',
                  func='test_assert')

    assert dict(func_docstr='docstring metodo\n    ',
                class_docstr='Docstring de classe\n    ') == extract_docstr(blocks)

def test_pytest_report_teststatus():
    assert 1 == 1

def test_pytest_report_teststatus_error():
    '''Uma docstring na funcao de teste
    '''
    assert 0 == 1

class DummyTestCase(unittest.TestCase):
    '''Docstring de classe
    '''

    def test_assert(self):
        '''docstring metodo
        '''
        self.assertEquals(1, 0)
