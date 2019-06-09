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

def main():
    task_runs_filename = "task_runs/archaeology_task_run.csv"

    # Collect all the task Ids where a Yes answer was given
    task_run_dict = {}
    with open(task_runs_filename, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:

            # Cast task id to String so that we can use it as a dictionary key.
            task_id = str(row[KEY_TASK_ID])

            # Get other values of interest
            task_run_id = row[KEY_ID]

            # User answer to the task can be Yes, No, or Bad Image.
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
                if answer == ANSWER_YES:
                    task_run_dict[task_id][KEY_YES] = 1
                    task_run_dict[task_id][KEY_NO] = 0
                    task_run_dict[task_id][KEY_BAD_IMAGE] = 0

                elif answer== ANSWER_NO:
                    task_run_dict[task_id][KEY_YES] = 0
                    task_run_dict[task_id][KEY_NO] = 1
                    task_run_dict[task_id][KEY_BAD_IMAGE] = 0

                elif answer == ANSWER_BAD_IMAGE:
                    task_run_dict[task_id][KEY_YES] = 0
                    task_run_dict[task_id][KEY_NO] = 0
                    task_run_dict[task_id][KEY_BAD_IMAGE] = 1

                else:
                    print("Unexpected answer for input " + task_run_id  + " in task " +  task_id + ": " + answer)


    task_run_dict
if __name__ == "__main__":
    main()
