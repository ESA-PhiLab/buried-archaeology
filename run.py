from pyproj import Proj, transform
import csv
import furl

x_dimension = 1600
y_dimension = 800
resolution = 25 # meters.

lat_bounds = [51.72, 52.22]
lng_bounds = [-2.28, -1.21]

# Upper left hand corner coords.
ulhc_coords = [lat_bounds[1], lng_bounds[0]]

# Lower right hand corner coords.
lrhc_coords = [lat_bounds[0], lng_bounds[1]]

#lat_step = 0.01
#lng_step = 0.02

times = ['2018-05-15', '2018-06-26', '2018-06-29', '2018-07-06']

#zoom = 16

#preset = '1_TRUE_COLOR'
#data_source = 'Sentinel-2%20L2A'

#url_template = 'https://apps.sentinel-hub.com/eo-browser/?lat={}&lng={}&zoom={}&time=TIME_TOKEN&preset={}&datasource={}'

api_key = ''

url = 'http://services.sentinel-hub.com/ogc/wms/' + api_key

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
    'time': times[0],
    'srs': 'EPSG%3A3857', 
    'bbox': '{},{},{},{}' #xmin, ymin, xmax, ymax.
}


f = furl.furl('')


def main():

    in_proj = Proj(init='epsg:4326')
    out_proj = Proj(init='epsg:3857')

    ulhc_x, ulhc_y = transform(in_proj, out_proj, ulhc_coords[0], ulhc_coords[1])
    #print ulhc_x, ulhc_y

    lrhc_x, lrhc_y = transform(in_proj, out_proj, lrhc_coords[0], lrhc_coords[1])
    #print lrhc_x, lrhc_y

    # Init the bounds for the first task (on the upper left hand corner of the AOI).
    x_bounds_current = [int(ulhc_x), int(ulhc_x - x_dimension)]
    y_bounds_current = [int(ulhc_y), int(ulhc_y + y_dimension)]

    # Redefining bounds so that we traverse the AOI row by row.
    while y_bounds_current[1] <= lrhc_y:
        while x_bounds_current[1] >= lrhc_x:
        
            # Shift to the next x bounds
            x_bounds_current = [x_bounds_current[1], x_bounds_current[1] - x_dimension]

            #print x_bounds_current
            #print y_bounds_current

            params['bbox'] = params['bbox'].format(
                x_bounds_current[0], y_bounds_current[0],
                x_bounds_current[1], y_bounds_current[1])

            f.args = params

            print url + f.url
            print
            break
        break

        # Completed the row on the x axis:
        # 1. Shift the y bounds to cover the next row.
        y_bounds_current = [y_bounds_current[1], y_bounds_current[1] + y_dimension]

        # 2. Shift the x bounds back to the beginning for the new row.
        x_bounds_current = [int(ulhc_x), int(ulhc_x - x_dimension)]


    #print ''
    #print ulhc_x, ulhc_y
    #print lrhc_x, lrhc_y

    '''
    field_names = ['img_url', 'lat', 'lng', 'zoom', 'time1', 'time2', 'time3', 'time4']
    with open('tasks.csv', mode='w') as tasks_csv_file:

        # Create CSV Writer and writer header.
        writer = csv.DictWriter(tasks_csv_file, fieldnames=field_names)
        writer.writeheader()
        
        # Initialize lower bounds.
        lat = lat_bounds[0]
        lng = lng_bounds[0]

        # Write task rows.
        while lat <= lat_bounds[1]:
            while lng <= lng_bounds[1]:

                # Build image url.
                img_url = url_template.format(lat, lng, zoom, preset, data_source)

                # Write task row in CSV file.     
                writer.writerow({
                    'img_url': img_url, 
                    'lat': lat,
                    'lng': lng,
                    'zoom': zoom,
                    'time1': times[0],
                    'time2': times[1],
                    'time3': times[2],
                    'time4': times[3]})

                lng = lng + lng_step

            lat = lat + lat_step
            lng = lng_bounds[0]
    '''

if __name__ == "__main__":
    main()