# Trip Tracker

Trip tracker processes mouse tracking data and computes metadata.

## Usage

Trip tracker contains a number of small but useful libraries and a main.py file that is meant to be tinkered with. This should allow new users to get up to speed quickly without having to learn the libraries relevant to each file type and data structure used. 

**Basic adjustment of this program is done with the global variables in variables.py**

This program revolves around the MouseMetadata object which has the following structure:
- data: A pandas DataFrame containing all the mouse tracking data
- time_in_center: A dictionary containing the time each limb spent in the center (in seconds)
- time_on_outside: A dictionary containing the time each limb spent on the outside (in seconds)
- total_distance: A dictionary containing the total distance travelled by each limb (in pixels)
- average_velocity: A dictionary containing the average velocity of each limb (in pixels/second)

Any further analysis can be calculated from the data variable.

The user must handle output. For example, if they want to write the metadata to a file they'll have to write that program.

## Structure

**main.py** - The main workspace. 
**ingestion.py** - Data ingestion. Contains functions to read and process data from an h5 file.
**mouse.py** - Defines the MouseMetadata class. This is a good library to read through if you want to understand the program.
**rectangle.py** - This has a rectangle class.
**variables.py** - Contains all the global variables used to adjust the program.
**video.py** - Handles reading and annotating the mouse videos.
