import csv

lat_bounds = [51.72, 52.22]
lng_bounds = [-2.28, -1.21]
lat_step = 0.01
lng_step = 0.02
times = ['2018-05-15', '2018-06-26', '2018-06-29', '2018-07-06']
zoom = 16
preset = '1_TRUE_COLOR'
data_source = 'Sentinel-2%20L2A'

url_template = 'https://apps.sentinel-hub.com/eo-browser/?lat={}&lng={}&zoom={}&time=TIME_TOKEN&preset={}&datasource={}'

def main():

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

if __name__ == "__main__":
    main()