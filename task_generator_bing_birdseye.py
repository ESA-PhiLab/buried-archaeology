import json
import requests
import math
import time
import csv

metadata_url_template = 'https://dev.virtualearth.net/REST/V1/Imagery/Metadata/Birdseye/{},{}?zl={}&orientation={}&o=json&key={}'
BING_API_KEY = 'XXXX'

EARTH_RADIUS = 6378137


# Imagery request parameters
ZOOM_LEVEL = 19

# A double value between 0 to 360,
# Where 0 = North [default], 90 = East, 180 = South, 270 = West.
ORIENTATION = 0

DEFAULT_TILE_X = 3
DEFAULT_TILE_Y = 3
DEFAULT_IMG_WIDTH = 512
DEFAULT_IMG_HEIGHT = 512

# Define boundary box.
# Upper left hand corner lat/lng coords.
ulhc_coords = [42.03, 12.20]

# Lower right hand corner lat/lng coords.
lrhc_coords = [41.66, 12.84]

def get_ground_resolution(latitude):
    ground_resolution = (math.cos(latitude * math.pi/180) * 2 * math.pi * EARTH_RADIUS) / (256 * 2**ZOOM_LEVEL)
    return ground_resolution

def main():

    # Open CSV file to write task rows into.
    with open('tasks_bing_birdseye.csv', mode='w') as tasks_csv_file, open('tasks_bing_no_birdseye_available.csv', mode='w') as tasks_no_birdseye_csv_file:
        # Create CSV Writer and write header.
        task_field_names = ['img_url', 'img_url_subdomain', 'lat', 'lng', 'tiles_x', 'tiles_y', 'img_height', 'img_width', 'start_date', 'end_date']
        task_writer = csv.DictWriter(tasks_csv_file, fieldnames=task_field_names, lineterminator = '\n')
        task_writer.writeheader()

        task_no_birdseye_field_names = ['metadata_url', 'lat', 'lng']
        task_writer_no_birdseye = csv.DictWriter(tasks_no_birdseye_csv_file, fieldnames=task_no_birdseye_field_names, lineterminator = '\n')
        task_writer_no_birdseye.writeheader()

        # Init first lat/lng to check against
        current_lat = ulhc_coords[0]
        current_lng = ulhc_coords[1]

        task_counter = 0
        task_no_birdseye_counter = 0
        
        while current_lat >= lrhc_coords[0]:
            print 'Processing new row at latitude ' + str(current_lat) + '.'

            while current_lng <= lrhc_coords[1]:
                # reset values
                img_url_template = None
                img_height = None
                img_width = None
                tiles_x = None 
                tiles_y = None
                img_url_subdomain = None
                vintage_start = None 
                vintage_end = None

                metadata_url = metadata_url_template.format(
                    current_lat, current_lng, ZOOM_LEVEL, ORIENTATION, BING_API_KEY)

                response = requests.get(metadata_url)
                metadata_json = json.loads(response.text)

                # Check if Birdseye images are available for the current area.
                if (len(metadata_json['resourceSets']) == 0) or (len(metadata_json['resourceSets']) > 0 and metadata_json['resourceSets'][0]['estimatedTotal'] == 0):
                    print 'No Birdseye images available for coordinates {},{}'.format(current_lat, current_lng)

                    # Caculate next current_lng.
                    dx = DEFAULT_TILE_X * DEFAULT_IMG_WIDTH * get_ground_resolution(current_lat)
                    current_lng = current_lng + (dx / EARTH_RADIUS) * (180 / math.pi) / math.cos(current_lat * math.pi / 180);

                    ## Track where there is no birdseye to create a task.
                    task_writer_no_birdseye.writerow({
                        'metadata_url': metadata_url.replace(BING_API_KEY, 'BING_API_KEY'),
                        'lat': current_lat,
                        'lng': current_lng
                        })

                    task_no_birdseye_counter = task_no_birdseye_counter + 1

                else:
                    img_url_template = metadata_json['resourceSets'][0]['resources'][0]['imageUrl']
                    img_height = metadata_json['resourceSets'][0]['resources'][0]['imageHeight']
                    img_width = metadata_json['resourceSets'][0]['resources'][0]['imageWidth']
                    tiles_x = metadata_json['resourceSets'][0]['resources'][0]['tilesX']
                    tiles_y = metadata_json['resourceSets'][0]['resources'][0]['tilesY']
                    img_url_subdomain = metadata_json['resourceSets'][0]['resources'][0]['imageUrlSubdomains'][0]
                    vintage_start = metadata_json['resourceSets'][0]['resources'][0]['vintageStart']
                    vintage_end = metadata_json['resourceSets'][0]['resources'][0]['vintageEnd']

                    # Write row in CSV
                    task_writer.writerow({
                        'img_url': img_url_template.replace(BING_API_KEY, 'BING_API_KEY'),
                        'img_url_subdomain': img_url_subdomain, 
                        'lat': current_lat,
                        'lng': current_lng,
                        'tiles_x': tiles_x,
                        'tiles_y': tiles_y,
                        'img_height': img_height,
                        'img_width': img_width,
                        'start_date': vintage_start,
                        'end_date': vintage_end})

                    task_counter = task_counter + 1

                    # Caculate next current_lng based on current image width and number of x tiles.
                    dx = min(tiles_x, tiles_y) * img_width * get_ground_resolution(current_lat)
                    current_lng = current_lng + (dx / EARTH_RADIUS) * (180 / math.pi) / math.cos(current_lat * math.pi / 180);
                
                # Allow enough time between each requests to not trigger any DDoS or scraping alerts.
                time.sleep(0.5)

            # Caculate next current_lat for the next row.
            # However, it could be that that tiles_x, tiles_y, and img_height variables were not set
            # if the previous row had not birdseye imagery. So check for that here.
            if tiles_x is None or tiles_y is None:
                min_tile_nums = DEFAULT_TILE_X
                img_height = DEFAULT_IMG_HEIGHT
            else:
                min_tile_nums = min(tiles_x, tiles_y)

            dy = min_tile_nums * img_height * get_ground_resolution(current_lat)
            current_lat = current_lat - (dy / EARTH_RADIUS) * (180 / math.pi);

            # Reset current_lng so we restart at the beginning of the new current_lat row.
            current_lng = ulhc_coords[1]
         
        print 'Number of tasks created: ' + str(task_counter)
        print 'Number of tasks skipped (no birdseye available): ' + str(task_no_birdseye_counter)

if __name__ == "__main__":
    main()
