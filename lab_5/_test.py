import pytest
from unittest.mock import MagicMock, patch
from code_to_fix import FullArgSpec, _GetArgSpecInfo, Py3GetFullArgSpec, IsNamedTuple, IsCoroutineFunction, GetFileAndLine, Info

# 1.
def test_fullargspec_init():
    spec = FullArgSpec(args=['a', 'b'], varargs='args', varkw='kwargs', defaults=(1,), kwonlyargs=['c'], kwonlydefaults={'c': 2}, annotations={'a': int})
    assert spec.args == ['a', 'b']
    assert spec.varargs == 'args'
    assert spec.varkw == 'kwargs'
    assert spec.defaults == (1,)
    assert spec.kwonlyargs == ['c']
    assert spec.kwonlydefaults == {'c': 2}
    assert spec.annotations == {'a': int}

# 2.
def test_getargspecinfo_function():
    def sample_function(a, b):
        return a + b

    fn, skip_arg = _GetArgSpecInfo(sample_function)
    assert fn is sample_function
    assert not skip_arg

# 3.
def test_py3getfullargspec_simple_function():
    def test_func(x, y=1):
        return x + y

    spec = Py3GetFullArgSpec(test_func)
    assert spec.args == ['x', 'y']
    assert spec.defaults == (1,)
    assert spec.varargs is None
    assert spec.varkw is None

# 4.
def test_is_namedtuple():
    from collections import namedtuple

    Point = namedtuple('Point', ['x', 'y'])
    p = Point(1, 2)
    t = (1, 2)

    assert IsNamedTuple(p) is True
    assert IsNamedTuple(t) is False

# 5.
def test_is_coroutine_function():
    async def async_func():
        pass

    def regular_func():
        pass

    assert IsCoroutineFunction(async_func) is True
    assert IsCoroutineFunction(regular_func) is False

# 6.
@patch('code_to_fix.inspect.getsourcefile', return_value='example.py')
@patch('code_to_fix.inspect.findsource', return_value=([], 10))
def test_getfileandline(mock_getsourcefile, mock_findsource):
    def mock_function():
        pass

    filename, lineno = GetFileAndLine(mock_function)
    assert filename == 'example.py'
    assert lineno == 11

# 7.
@patch('code_to_fix.inspect.getdoc', return_value='Sample docstring')
def test_info_with_mock(mock_getdoc):
    def mock_function():
        pass

    info = Info(mock_function)
    assert info['docstring'] == 'Sample docstring'
    assert 'type_name' in info
    assert 'string_form' in info

if __name__ == "__main__":
    pytest.main(['-q', '--disable-warnings', '--maxfail=1', 'tests.py'])
