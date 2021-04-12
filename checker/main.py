import os
import warnings
import argparse
import geopandas as gpd

warnings.filterwarnings('ignore')
VALID_EXTENSIONS = {'.zip', '.shp'}


def validate_path(path: str):
    if not os.path.isfile(path):
        raise ValueError(f'"{path}" is not a file')
    ext = os.path.splitext(path)[1]
    if ext not in VALID_EXTENSIONS:
        raise ValueError(f'extension "{ext}" is not supported')


def calc_score(column: str, file_for_verification: str,
               validation_points_path: str, region_of_interest: str) -> float:
    validate_path(file_for_verification)
    validate_path(validation_points_path)
    validate_path(region_of_interest)

    data_for_validation = gpd.read_file(file_for_verification)
    validation_points = gpd.read_file(validation_points_path)
    roi = gpd.read_file(region_of_interest)

    assert data_for_validation.crs == validation_points.crs == roi.crs, \
        'coordinate system doesn\'t match'
    assert column in data_for_validation.columns and column in validation_points.columns, \
        f'column "{column}" is missing'

    classes = set(validation_points[column])
    classes_2 = set(data_for_validation[column])
    assert 0 <= len(classes) - len(classes_2) < 2 and \
           classes.intersection(classes_2) == classes_2, 'set of classes doesn\'t match'

    roi_area = roi.geometry.area[0]
    del roi

    empty_class = classes.difference(classes_2).pop() \
        if len(classes) > len(classes_2) else None

    data_for_validation['area'] = data_for_validation.geometry.area
    area_proportions = data_for_validation.groupby(column)['area'].sum() / roi_area
    if empty_class is not None:
        area_proportions[empty_class] = 1 - area_proportions.sum()

    error_matrix = gpd.GeoDataFrame(0, columns=classes, index=classes)
    for class_name, point in zip(validation_points[column], validation_points.geometry):
        for predicted_name, poly in zip(data_for_validation[column], data_for_validation.geometry):
            if point.within(poly):
                error_matrix[class_name][predicted_name] += 1
                break
        else:
            if empty_class is not None:
                error_matrix[class_name][empty_class] += 1

    # print(error_matrix)
    return sum([area_proportions.loc[col] * error_matrix[col][col] /
                error_matrix.loc[col].sum() for col in classes])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('column')
    parser.add_argument('for_validation')
    parser.add_argument('validation_points')
    parser.add_argument('region_of_interest')
    args = parser.parse_args()

    result = calc_score(args.column, args.for_validation,
                        args.validation_points, args.region_of_interest)
    print(f'Score: {result:.5f}')
