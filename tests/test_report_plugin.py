import unittest
from neurotic.report_plugin import parse_nodeid

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
