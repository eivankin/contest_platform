import pytest
from checker.main import calc_score


def test_empty_path():
    with pytest.raises(ValueError, match=r'".*" is not a file'):
        calc_score('', '')


def test_wrong_path():
    with pytest.raises(ValueError, match=r'".*" is not a file'):
        calc_score('../checker', '../checker')


def test_invalid_extension():
    with pytest.raises(ValueError, match=r'extension ".*" is not supported'):
        calc_score('main.py', 'main.py')
