import pytest
from checker.main import calc_score
from contest_platform.settings import BASE_DIR

CURRENT_DIR = BASE_DIR / 'checker'


def test_empty_path():
    with pytest.raises(ValueError, match='".*" is not a file'):
        calc_score('column', '', '', '')


def test_wrong_path():
    with pytest.raises(ValueError, match='".*" is not a file'):
        calc_score('column', *[BASE_DIR / 'checker'] * 3)


def test_invalid_extension():
    with pytest.raises(ValueError, match='extension ".*" is not supported'):
        calc_score('column', *[BASE_DIR / 'checker/main.py'] * 3)


def test_different_crs():
    with pytest.raises(AssertionError, match='coordinate system doesn\'t match'):
        calc_score(
            'class', CURRENT_DIR / 'tests_data/classes_1_other_crs.shp',
            CURRENT_DIR / 'tests_data/validation_points_1.shp',
            CURRENT_DIR / 'tests_data/roi_1.shp')


def test_missed_column():
    with pytest.raises(AssertionError, match='column ".*" is missing'):
        calc_score(
            'wrong_column', CURRENT_DIR / 'tests_data/classes_1.shp',
            CURRENT_DIR / 'tests_data/validation_points_1.shp',
            CURRENT_DIR / 'tests_data/roi_1.shp')


def test_wrong_classes():
    with pytest.raises(AssertionError, match='set of classes doesn\'t match'):
        calc_score('class', CURRENT_DIR / 'tests_data/wrong_classes.shp',
                   CURRENT_DIR / 'tests_data/validation_points_1.shp',
                   CURRENT_DIR / 'tests_data/roi_1.shp')


def test_maximum_accuracy():
    assert calc_score(
        'class', CURRENT_DIR / 'tests_data/classes_1.shp',
        CURRENT_DIR / 'tests_data/validation_points_1.shp',
        CURRENT_DIR / 'tests_data/roi_1.shp') == 1.0


def test_zero_accuracy():
    assert calc_score(
        'class', CURRENT_DIR / 'tests_data/classes_2.shp',
        CURRENT_DIR / 'tests_data/validation_points_1.shp',
        CURRENT_DIR / 'tests_data/roi_1.shp') == 0.0


def test_good_accuracy():
    result = calc_score(
        'class', CURRENT_DIR / 'tests_data/classes_3.shp',
        CURRENT_DIR / 'tests_data/validation_points_1.shp',
        CURRENT_DIR / 'tests_data/roi_1.shp')
    assert f'{result:.5f}' == '0.81641'
