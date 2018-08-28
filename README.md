# PyBossa EO Browser Imagery Task Generator
Generate a CSV file listing imagery URLs. The CSV file is to be imported into a [PyBossa](https://pybossa.com/) instance for crowdsourcing purposes.  Each row in the CSV files is associated to a microtask.

This particular script was developed for a crowdsourcing project hosted in [crowdcrafting.org](https://crowdcrafting.org/).

The list of imagery URLs are generated based on the following inputs:

 - Bounding box of the project's area of interest (latitude and longitude bounds).
 - Imagery dimensions for a task (i.e. x and y lengths)
