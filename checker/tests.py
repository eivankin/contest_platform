import pytest
from checker.main import calc_score


def test_empty_path():
    with pytest.raises(ValueError, match='".*" is not a file'):
        calc_score('column', '', '', '')


def test_wrong_path():
    with pytest.raises(ValueError, match='".*" is not a file'):
        calc_score('column', '../checker', '../checker', '../checker')


def test_invalid_extension():
    with pytest.raises(ValueError, match='extension ".*" is not supported'):
        calc_score('column', 'main.py', 'main.py', 'main.py')


def test_different_crs():
    with pytest.raises(AssertionError, match='coordinate system doesn\'t match'):
        calc_score(
            'class', 'tests_data/classes_1_other_crs.shp',
            'tests_data/validation_points_1.shp', 'tests_data/roi_1.shp')


def test_missed_column():
    with pytest.raises(AssertionError, match='column ".*" is missing'):
        calc_score(
            'wrong_column', 'tests_data/classes_1.shp',
            'tests_data/validation_points_1.shp', 'tests_data/roi_1.shp')


def test_wrong_classes():
    with pytest.raises(AssertionError, match='set of classes doesn\'t match'):
        calc_score('class', 'tests_data/wrong_classes.shp',
                   'tests_data/validation_points_1.shp', 'tests_data/roi_1.shp')


def test_maximum_accuracy():
    assert calc_score(
        'class', 'tests_data/classes_1.shp', 'tests_data/validation_points_1.shp',
        'tests_data/roi_1.shp') == 1.0


def test_zero_accuracy():
    assert calc_score(
        'class', 'tests_data/classes_2.shp', 'tests_data/validation_points_1.shp',
        'tests_data/roi_1.shp') == 0.0


def test_good_accuracy():
    result = calc_score(
        'class', 'tests_data/classes_3.shp', 'tests_data/validation_points_1.shp',
        'tests_data/roi_1.shp')
    assert f'{result:.5f}' == '0.81641'
