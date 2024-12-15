import pytest
from unittest.mock import MagicMock, patch
from code_to_fix import FullArgSpec, _GetArgSpecInfo, Py3GetFullArgSpec

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

if __name__ == "__main__":
    pytest.main(['-q', '--disable-warnings', '--maxfail=1', 'tests.py'])
