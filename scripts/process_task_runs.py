import csv

ANSWER_YES = 'Yes'
ANSWER_NO = 'No'
ANSWER_BAD_IMAGE = 'Bad Image'

KEY_YES = 'yes'
KEY_NO = 'no'
KEY_BAD_IMAGE = 'bad'

KEY_ID = 'id'
KEY_TASK_ID = 'task_id'
KEY_INFO = 'info'
KEY_IMG_URL = 'img_url'
KEY_IMG_URL_SUBDOMAIN = 'img_url_subdomain'
KEY_LAT = 'lat'
KEY_LNG = 'lng'
KEY_TILES_X = 'tiles_x'
KEY_TILES_Y = 'tiles_y'

def main():
    # These files need to be downloaded from the admin dashboard of the PyBossa project.
    task_info_filename = "../task_runs/Archaeology_task_info_only.csv"
    task_runs_filename = "../task_runs/Archaeology_task_run.csv"

    #####################################
    # Prepare the task info dictionary. #
    #####################################
    task_info_dict = {}
    with open(task_info_filename, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # Get values of interest
            task_id = row[KEY_TASK_ID]
            img_url_subdomain = row[KEY_IMG_URL_SUBDOMAIN]

            # Build task info dictionary to lookup the image url.
            task_info_dict[task_id] = {}
            task_info_dict[task_id][KEY_IMG_URL] = row[KEY_IMG_URL]
            task_info_dict[task_id][KEY_LAT] = float(row[KEY_LAT])
            task_info_dict[task_id][KEY_LNG] = float(row[KEY_LNG])
            task_info_dict[task_id][KEY_TILES_X] = int(row[KEY_TILES_X])
            task_info_dict[task_id][KEY_TILES_Y] = int(row[KEY_TILES_Y])


    #################################
    # Process the user submissions. #
    #################################
    print("\nProcessing the user submissions...")

    # Collect all the task Ids where a Yes answer was given
    task_run_dict = {}
    with open(task_runs_filename, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:

            # Fetch values of interest.
            task_id = row[KEY_TASK_ID]
            task_run_id = row[KEY_ID]
            answer = row[KEY_INFO]

            # If the task has already been processed in previous task runs, then just add to the previous result.
            if task_id in task_run_dict:
                if answer == ANSWER_YES:
                    task_run_dict[task_id][KEY_YES] = task_run_dict[task_id][KEY_YES] + 1

                elif answer == ANSWER_NO:
                    task_run_dict[task_id][KEY_NO] = task_run_dict[task_id][KEY_NO] + 1

                elif answer == ANSWER_BAD_IMAGE:
                    task_run_dict[task_id][KEY_BAD_IMAGE] = task_run_dict[task_id][KEY_BAD_IMAGE] + 1

                else:
                    print("Unexpected answer for input " + task_run_id  + " in task " +  task_id + ": " + answer)

            # If we are dealing with a task run for a first time process task, initialize the task object.
            else:
                # Set the task info values retrieved from the task info only CSV.
                task_run_dict[task_id] = {}
                task_run_dict[task_id][KEY_INFO] = {}
                task_run_dict[task_id][KEY_INFO][KEY_IMG_URL] = task_info_dict[task_id][KEY_IMG_URL]
                task_run_dict[task_id][KEY_INFO][KEY_LAT] = task_info_dict[task_id][KEY_LAT]
                task_run_dict[task_id][KEY_INFO][KEY_LNG] = task_info_dict[task_id][KEY_LNG]
                task_run_dict[task_id][KEY_INFO][KEY_TILES_X] = task_info_dict[task_id][KEY_TILES_X]
                task_run_dict[task_id][KEY_INFO][KEY_TILES_Y] = task_info_dict[task_id][KEY_TILES_Y]

                if answer == ANSWER_YES:
                    task_run_dict[task_id][KEY_YES] = 1
                    task_run_dict[task_id][KEY_NO] = 0
                    task_run_dict[task_id][KEY_BAD_IMAGE] = 0

                elif answer == ANSWER_NO:
                    task_run_dict[task_id][KEY_YES] = 0
                    task_run_dict[task_id][KEY_NO] = 1
                    task_run_dict[task_id][KEY_BAD_IMAGE] = 0

                elif answer == ANSWER_BAD_IMAGE:
                    task_run_dict[task_id][KEY_YES] = 0
                    task_run_dict[task_id][KEY_NO] = 0
                    task_run_dict[task_id][KEY_BAD_IMAGE] = 1

                else:
                    print("Unexpected answer for input " + task_run_id  + " in task " +  task_id + ": " + answer)

    ########################
    # Present the results. #
    ########################
    # Get task runs with at least 0 YES
    task_runs_yes_0 = {k: v for k, v in task_run_dict.items() if v[KEY_YES] == 0}

    # Get task runs with at least 1 YES
    task_runs_yes_1 = {k: v for k, v in task_run_dict.items() if v[KEY_YES] == 1}

    # Get task runs with at least 2 YES
    task_runs_yes_2 = {k: v for k, v in task_run_dict.items() if v[KEY_YES] == 2}

    # Get task runs with at least 3 YES
    task_runs_yes_3 = {k: v for k, v in task_run_dict.items() if v[KEY_YES] >= 3}

    print("\nResults:")
    print(" + " + str(len(task_runs_yes_0)) + " tasks with 0 positive answers.")
    print(" + " + str(len(task_runs_yes_1)) + " tasks with 1 positive answer.")
    print(" + " + str(len(task_runs_yes_2)) + " tasks with 2 positive answers.")
    print(" + " + str(len(task_runs_yes_3)) + " tasks with 3 or more positive answers.")

    #######################
    # Export the results. #
    #######################
    BING_URL = "https://www.bing.com/maps?cp="
    BING_ZOOM_LEVEL = 17
    BING_URL_PARAMS = "&lvl=" + str(BING_ZOOM_LEVEL) + "&style=h&v=2&sV=2"

    print("\nExporting results...")

    with open('../results/locations_with_1_positive.txt', 'w') as result_file:
        for key, task_run in task_runs_yes_1.items():
            bing_url = BING_URL + str(task_run[KEY_INFO][KEY_LAT]) + "~" + str(task_run[KEY_INFO][KEY_LNG]) + BING_URL_PARAMS
            result_file.write(bing_url + "\n")

    with open('../results/locations_with_2_positives.txt', 'w') as result_file:
        for key, task_run in task_runs_yes_2.items():
            bing_url = BING_URL + str(task_run[KEY_INFO][KEY_LAT]) + "~" + str(task_run[KEY_INFO][KEY_LNG]) + BING_URL_PARAMS
            result_file.write(bing_url + "\n")

    with open('../results/locations_with_3_or_more_positives.txt', 'w') as result_file:
        for key, task_run in task_runs_yes_3.items():
            bing_url = BING_URL + str(task_run[KEY_INFO][KEY_LAT]) + "~" + str(task_run[KEY_INFO][KEY_LNG]) + BING_URL_PARAMS
            result_file.write(bing_url + "\n")

    print("\nAll done.\n")

if __name__ == "__main__":
    main()
