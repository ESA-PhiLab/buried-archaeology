# PyBossa EO Browser Imagery Task Generator
There are twp PyBossa projects: one that uses Bing Maps bird's-eye imagery and another one that uses Sentinel optical imagery.

## Task Generators
The task generator scripts produce CSV files in which each row corresponds to a microtask. A CSV file is to be imported into a [PyBossa](https://pybossa.com/) project instance in order to create the tasks within that platform.

- `task_generator_bing_birdseye.py`: Generates the microtask CSV file that utilizes Bing Maps bird's-eye imagery. 
- `task_generator_sentinel.py`: Generates the microtask CSV file that utilizes Sentinel optical imagery.

The imagery URLs are generated based on the following inputs:
- Bounding box of the project's area of interest (latitude and longitude bounds).
- Imagery dimensions for a task (i.e. x and y lengths).

## Task Presenters
The user interface that presents the task to the crowdsourced users. These are crowdsourcing project specific HTML files that are copied into PyBossa when creating the project.

- `task_presenter_bing_birdseye.html`: Task Presenter for the PyBossa project that uses Bing Maps bird's-eye imagery. 
- `task_presenter_sentinel.html`: Task Presenter for the PyBossa project that uses Sentinel optical imagery. 

## Task Run Processors
Completed tasks are called ***Task Runs***. Task Runs can be downloaled from PyBossa as CSV files. The `process_task_runs.py` script processes those Task Run CSV files into results files, also in CSV. These result files group the task results based on following confidence thresholds:
- All tasks with 1 positive answer.
- All tasks with 2 positive answers.
- All tasks with at least 3 positive anwers.

**Note:** This is currently only implemented for the Bing Maps bird's-eye imagery project.

## Task Run Navigator
A simple HTML page to visually navigate through the Task results and filter them based on confidence thresholds.

Can be accessed here:
https://esa-philab.github.io/buried-archaeology/task-run-navigator.html

**Note:** This is currently only implemented for the Bing Maps bird's-eye imagery project.
