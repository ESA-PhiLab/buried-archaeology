from pyproj import Proj, transform
import csv
import furl

wms_service_user_id = 'USER_ID_TOKEN'
wms_url = 'https://services.sentinel-hub.com/ogc/wms/' + wms_service_user_id

x_dimension = 1600 # meters.
y_dimension = 800 # meters.

lat_bounds = [51.72, 52.22]
lng_bounds = [-2.28, -1.21]

# Upper left hand corner coords.
ulhc_coords = [lng_bounds[0], lat_bounds[1]]

# Lower right hand corner coords.
lrhc_coords = [lng_bounds[1], lat_bounds[0]]

times = ['2018-05-15', '2018-06-26', '2018-06-29', '2018-07-06']

params = {
    'service': 'WMS',
    'request': 'GetMap',
    'layers': 'TRUE_COLOR',
    'styles': '',
    'format': 'image/png',
    'transparent': 'false',
    'version': '1.1.1',
    'showlogo': 'false',
    'height': y_dimension,
    'width': x_dimension,
    'maxcc': 1,
    'time': 'TIME_TOKEN',
    'srs': 'EPSG%3A3857'
}

furl = furl.furl('')

def main():

    # Define projections.
    in_proj = Proj(init='epsg:4326')
    out_proj = Proj(init='epsg:3857')

    # Get x and y coordinates for upper left hand corner and lower right hand corner coords.
    ulhc_x, ulhc_y = transform(in_proj, out_proj, ulhc_coords[0], ulhc_coords[1])
    lrhc_x, lrhc_y = transform(in_proj, out_proj, lrhc_coords[0], lrhc_coords[1])


    # Open CSV file to write task rows into.
    with open('../tasks/tasks_sentinel.csv', mode='w') as tasks_csv_file:

        # Create CSV Writer and write header.
        field_names = ['img_url', 'xmin', 'ymin', 'xmax', 'ymax', 'lat', 'lng', 'time1', 'time2', 'time3', 'time4']
        writer = csv.DictWriter(tasks_csv_file, fieldnames=field_names)
        writer.writeheader()

        # Init the bounds for the first task (on the upper left hand corner of the AOI).
        x_bounds_current = [int(ulhc_x), int(ulhc_x + x_dimension)]
        y_bounds_current = [int(ulhc_y), int(ulhc_y - y_dimension)]

        # Task counter
        task_counter = 0

        # Redefining bounds so that we traverse the AOI row by row.
        while y_bounds_current[1] >= lrhc_y:
            while x_bounds_current[1] <= lrhc_x:

                x_min = x_bounds_current[0]
                x_max = x_bounds_current[1]
                y_min = y_bounds_current[0]
                y_max = y_bounds_current[1]
                x_center = (x_min + x_max) / 2
                y_center = (y_min + y_max) / 2

                # Define bounding box's xmin, ymin, xmax, and ymax values.
                params['bbox'] = '{},{},{},{}'.format(
                    x_min, y_min,
                    x_max, y_max)

                # Get center lat/lng coordinates
                lng, lat = transform(out_proj, in_proj, x_center, y_center)

                # Build image url.
                furl.args = params
                img_url = wms_url + furl.url

                # Write task row in CSV file.
                writer.writerow({
                    'img_url': img_url,
                    'xmin': x_min,
                    'ymin': y_min,
                    'xmax': x_max,
                    'ymax': y_max,
                    'lat': lat,
                    'lng': lng,
                    'time1': times[0],
                    'time2': times[1],
                    'time3': times[2],
                    'time4': times[3]})

                # Shift to the next x bounds
                x_bounds_current = [x_max, x_max + x_dimension]

                task_counter = task_counter + 1

            # Completed the row on the x axis:
            # 1. Shift the y bounds to cover the next row.
            y_bounds_current = [y_max, y_max - y_dimension]

            # 2. Shift the x bounds back to the beginning for the new row.
            x_bounds_current = [int(ulhc_x), int(ulhc_x + x_dimension)]

    print 'Total tasks created: ' + str(task_counter)


if __name__ == "__main__":
    main()
