# Buried Archaeology
Buried Archaeology consists of two PyBossa projects: one that uses [Bing Maps bird's-eye](https://www.bing.com/api/maps/sdkrelease/mapcontrol/isdk/birdseyev2) imagery and another one that uses [Sentinel-2](https://sentinel.esa.int/web/sentinel/missions/sentinel-2) optical imagery. The purpose of the crowdsourcing projects are to systematically document the abundant cropmarks over two selected areas in the UK and Italy.

How cropmarks are caused by underlying archaeology ([image source](https://www.slideshare.net/fruittingles2605/archaeological-survey-techniques)):
![How Cropmarks are Caused by Underlying Archaelogy](https://raw.githubusercontent.com/ESA-PhiLab/buried-archaeology/master/img/how-cropmarks-are-caused-by-underlying-archaeology.png)

## Background
This work has been carried out by researchers based in the newly created [Phi-Lab](http://blogs.esa.int/philab/) of the [European Space Agency](https://www.esa.int/ESA). The two projects have been published in the web-based service ***Crowdcrafting***, which uses the [PYBOSSA](https://pybossa.com/) Open Source framework for crowdsourcing.

### UK
Over the UK, advantage is taken of the exceptionally dry summer of 2018, when many cropmarks were revealed. Here users of the crowdsourcing app would view time series of Sentinel-2 imagery over a large part of the south of England to detect cropmarks through their evolution over the summer period.

### Italy
Over Italy, users view single images of very high resolution oblique air photos available in Bing Maps, to detect the abundant crop marks in the rapidly disappearing countryside surrounding the city of Rome, up to a 25 kilometer radius from the city centre. Archaeological crop marks in the Lazio area are usually of ancient Roman origin. They tend to have clear geometric patterns, revealing the foundations of buildings. Roman roads can be distinguished as very straight lines of parched vegetation (overlying ancient paving stones), with strips of greener vegetation on either side, where ditches used to be.

![Buried Archaeology - Lazio Example](https://raw.githubusercontent.com/ESA-PhiLab/buried-archaeology/master/img/buried-archaeology-all-lazio-examples.png)

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
- All tasks with at least 3 positive answers.

**Note:** This is currently only implemented for the Bing Maps bird's-eye imagery project.

## Task Run Navigator
A simple HTML page to visually navigate through the Task results and filter them based on confidence thresholds.

Can be accessed here:
https://esa-philab.github.io/buried-archaeology/task-run-navigator.html

**Note:** This is currently only implemented for the Bing Maps bird's-eye imagery project.
