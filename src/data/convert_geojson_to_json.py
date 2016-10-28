import json
import math


def main():
    counties = get_counties()
    write_counties(counties)


def get_counties():
    counties = []
    with open('counties.geojson', 'r') as geojson_file:
        geojson_data = json.load(geojson_file)
    for county_feature in geojson_data['features']:
        # TODO: include Alaska, Hawaii, and Puerto Rico
        if county_feature['properties']['STATEFP'] in ['02', '15', '72']:
            continue
        county = get_county(county_feature)
        counties.append(county)
    return tuple(counties)


def get_county(county_feature):
    county_path = get_path(county_feature)
    county = {
        'name': county_feature['properties']['NAME'],
        'id': county_feature['properties']['COUNTYFP'],
        'stateId': county_feature['properties']['STATEFP'],
        'path': county_path,
    }
    return county


def get_path(feature):
    path_strings = []
    geometry_type = feature['geometry']['type']
    geometry_coordinates = feature['geometry']['coordinates']
    if geometry_type == 'MultiPolygon':
        polygon_paths = [x[0] for x in geometry_coordinates]
    elif geometry_type == 'Polygon':
        polygon_paths = geometry_coordinates
    else:
        raise Exception('Unknown geometry type: ' + geometry_type)
    for polygon_path in polygon_paths:
        path_string = (
            ' '.join([
                '{} {:.3f},{:.3f}'.format(
                    'M' if index == 0 else 'L',
                    *get_albers_coordinate(latitude, longitude)
                )
                for index, (longitude, latitude, _) in enumerate(polygon_path)
            ]) + ' Z'
        )
        path_strings.append(path_string)
    return ' '.join(path_strings)


# TODO: move Alaska/Hawaii (and Puerto Rico?) into frame
def get_albers_coordinate(latitude, longitude):
    # See https://en.wikipedia.org/wiki/Albers_projection
    STANDARD_PARALLEL_2 = math.radians(29.5)
    STANDARD_PARALLEL_1 = math.radians(45.5)
    REFERENCE_LATITUDE = math.radians(39.8)
    REFERENCE_LONGITUDE = math.radians(-98.6)
    latitude = math.radians(latitude)
    longitude = math.radians(longitude)
    n = (math.sin(STANDARD_PARALLEL_1) + math.sin(STANDARD_PARALLEL_2)) / 2
    theta = n * (longitude - REFERENCE_LONGITUDE)
    c = (
        math.cos(STANDARD_PARALLEL_1) ** 2 +
        2 * n * math.sin(STANDARD_PARALLEL_1)
    )
    rho = math.sqrt(c - 2 * n * math.sin(latitude)) / n
    rho_0 = math.sqrt(c - 2 * n * math.sin(REFERENCE_LATITUDE)) / n
    x = rho * math.sin(theta)
    y = rho_0 - rho * math.cos(theta)
    x = 375 + 1100 * x
    y = 225 + 1100 * -y
    return x, y


def write_counties(counties):
    with open('counties.json', 'w+') as counties_file:
        json.dump(
            {'counties': counties}, counties_file,
            indent=2, sort_keys=True
        )


if __name__ == '__main__':
    main()
