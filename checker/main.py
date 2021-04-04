import os
import argparse
import geopandas as gpd
from decimal import Decimal

VALID_EXTENSIONS = {'.zip', '.shp'}


def validate_path(path: str):
    if not os.path.isfile(path):
        raise ValueError(f'"{path}" is not a file')
    ext = os.path.splitext(path)[1]
    if ext not in VALID_EXTENSIONS:
        raise ValueError(f'extension "{ext}" is not supported')


def calc_score(column: str, file_for_verification: str,
               validation_points_path: str, region_of_interest: str) -> Decimal:
    validate_path(file_for_verification)
    validate_path(validation_points_path)
    validate_path(region_of_interest)

    data_for_validation = gpd.read_file(file_for_verification)
    validation_points = gpd.read_file(file_for_verification)
    roi = gpd.read_file(file_for_verification)

    assert data_for_validation.crs == validation_points.crs == roi.crs, \
        'coordinate system doesn\'t match'
    assert column in data_for_validation.columns and column in validation_points.columns, \
        f'column "{column}" is missing'

    classes = set(validation_points[column])
    assert classes == set(data_for_validation[column]), f'set of classes doesn\'t match'
    # TODO
    return Decimal(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('column')
    parser.add_argument('for_validation')
    parser.add_argument('validation_points')
    parser.add_argument('region_of_interest')
    args = parser.parse_args()

    print('Score:', calc_score(args.column, args.for_validation,
                               args.validation_points, args.region_of_interest))
