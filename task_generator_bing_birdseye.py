import json
import requests
import math
import time
import csv

metadata_url_template = 'https://dev.virtualearth.net/REST/V1/Imagery/Metadata/Birdseye/{},{}?zl={}&orientation={}&o=json&key={}'
BING_API_KEY = 'XXXX'

EARTH_RADIUS = 6378137

# Imagery request parameters
LAT_BOUNDS = [51.72, 52.22]
LNG_BOUNDS = [-2.28, -1.21]
ZOOM_LEVEL = 19
ORIENTATION = 0

DEFAULT_TILE_X = 3
DEFAULT_TILE_Y = 3
DEFAULT_IMG_WIDTH = 512
DEFAULT_IMG_HEIGHT = 512

# Upper left hand corner lat/lng coords.
ulhc_coords = [LAT_BOUNDS[1], LNG_BOUNDS[0]]

# Lower right hand corner lat/lng coords.
lrhc_coords = [LAT_BOUNDS[0], LNG_BOUNDS[1]]

def get_ground_resolution(latitude):
    ground_resolution = (math.cos(latitude * math.pi/180) * 2 * math.pi * EARTH_RADIUS) / (256 * 2**ZOOM_LEVEL)
    return ground_resolution

def main():

    # Open CSV file to write task rows into.
    with open('tasks_bing_birdseye.csv', mode='w') as tasks_csv_file, open('tasks_bing_no_birdseye_available.csv', mode='w') as tasks_no_birdseye_csv_file:
        # Create CSV Writer and write header.
        task_field_names = ['img_url', 'lat', 'lng', 'tiles_x', 'tiles_y', 'tile_id', 'img_height', 'img_width', 'start_date', 'end_date']
        task_writer = csv.DictWriter(tasks_csv_file, fieldnames=task_field_names)
        task_writer.writeheader()

        task_no_birdseye_field_names = ['metadata_url', 'lat', 'lng']
        task_writer_no_birdseye = csv.DictWriter(tasks_no_birdseye_csv_file, fieldnames=task_no_birdseye_field_names)
        task_writer_no_birdseye.writeheader()

        # Init first lat/lng to check against
        current_lat = ulhc_coords[0]
        current_lng = ulhc_coords[1]

        task_counter = 0
        task_no_birdseye_counter = 0
        
        while current_lat >= lrhc_coords[0]:
            print 'Processing new row at latitude ' + str(current_lat) + '.'
            while current_lng <= lrhc_coords[1]:
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

                    # Create a task for each tile image.
                    tiled_id = 0
                    for y in range(0, tiles_y):
                        for x in range(0, tiles_x):

                            # Build the URL. Make sure not to save the API key into the tasks CSV file.
                            img_url = img_url_template.format(
                                subdomain=img_url_subdomain,
                                tileId=tiled_id).replace(BING_API_KEY, 'BING_API_KEY') 

                            # Write row in CSV
                            task_writer.writerow({
                                'img_url': img_url, 
                                'lat': current_lat,
                                'lng': current_lng,
                                'tiles_x': tiles_x,
                                'tiles_y': tiles_y,
                                'tile_id': tiled_id,
                                'img_height': img_height,
                                'img_width': img_width,
                                'start_date': vintage_start,
                                'end_date': vintage_end})

                            # Increment tile id for next image url.
                            tiled_id = tiled_id + 1 
                            task_counter = task_counter + 1

                    # Caculate next current_lng based on current image width and number of x tiles.
                    dx = min(tiles_x, tiles_y) * img_width * get_ground_resolution(current_lat)
                    current_lng = current_lng + (dx / EARTH_RADIUS) * (180 / math.pi) / math.cos(current_lat * math.pi / 180);
                
                # Allow enough time between each requests to not trigger any DDoS or scraping alerts.
                time.sleep(0.5)

            # Caculate next current_lat.
            dy = min(tiles_x, tiles_y) * img_height * get_ground_resolution(current_lat)
            current_lat = current_lat - (dy / EARTH_RADIUS) * (180 / math.pi);

            # Reset current_lng so we restart at the beginning of the new current_lat row.
            current_lng = ulhc_coords[1]
         
        print 'Number of tasks created: ' + task_counter
        print 'Number of tasks skipped (no birdseye available): ' + task_no_birdseye_counter

if __name__ == "__main__":
    main()
