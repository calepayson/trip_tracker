from typing import Dict
import h5py
import pandas as pd
import numpy as np

class Rectangle:
    def __init__(self, x_min: int, y_min: int, x_max: int, y_max: int):
        self.x_min: int = x_min
        self.y_min: int = y_min
        self.x_max: int = x_max
        self.y_max: int = y_max

# The name of the h5 file containing the mouse tracking coordinates
DATA_FILE_NAME = 'mouse_trip.h5'

# The name of video-file with the recording of the mouse trip
VIDEO_FILE_NAME = 'mouse_trip.avi'

# The fps of the video (and data)
FRAMES_PER_SECOND = 30

# The minimum viable likelihood for coordinates (any coordinates with a
# probability less than this will be interpolated)
LIKELIHOOD_THRESHOLD = 0.95

# The dimensions of the center rectangle
CENTER_RECT = Rectangle(
        x_min=475,
        y_min=305,
        x_max=845,
        y_max=680,)

# The labels for each body part in the data set (NOTE: order matters!)
BODY_PART_LABELS = [
        'nose', 
        'head', 
        'neck', 
        'leftear', 
        'rightear', 
        'body', 
        'tailbase']

# The labels for each coordinate column in the data set (NOTE: order matters!)
COORDINATE_LABELS = [
        'x', 
        'y', 
        'likelihood']

'''
Takes the name of an h5 file, loads the data into a pandas DataFrame, and 
returns that DataFrame.

Assumes: A specific file structure.
'''
def load_h5_data_into_dataframe(file_name: str) -> pd.DataFrame:
    # Open the file
    with h5py.File(file_name) as file:
        # Read the data
        data = file['df_with_missing']['table']
        # Convert the data to a DataFrame
        df = pd.DataFrame({
            'values_block_0': [list(row) for row in data['values_block_0']]
        })
    return df

'''
Takes a DataFrame of the raw data extracted from the h5 file and cleans it.

Assumes: a specific data structure.
'''
def clean_raw_df(df: pd.DataFrame) -> pd.DataFrame:
    # Break values_block_0 into multiple columns
    df = pd.DataFrame(
            df['values_block_0'].tolist(),
            index=df.index)

    # Create a DataFrame with the lables
    columns = pd.MultiIndex.from_product(
            [BODY_PART_LABELS, COORDINATE_LABELS],
            names=['body_part', 'coordinates'])

    # Add the column labels to the DataFrame
    df = pd.DataFrame(
            df.values.reshape(
                len(df),
                len(BODY_PART_LABELS) * len(COORDINATE_LABELS)),
            columns=columns)

    # Interpolate coordinates if likelihood is below LIKELIHOOD_THRESHOLD
    for part in BODY_PART_LABELS:
        # Map low likelihood coordinates to a dataframe
        low_likelihood = df[(part, 'likelihood')] < LIKELIHOOD_THRESHOLD
        # Interpolate values for the points indicated by the map
        df.loc[low_likelihood, (part, 'x')] = df[(part, 'x')].interpolate(limit_direction='both')
        df.loc[low_likelihood, (part, 'y')] = df[(part, 'y')].interpolate(limit_direction='both')

    return df

'''
Represents the data associated with a mouse over the course of an experiment.
Initialize it by passing in a cleaned DataFrame.
Depends on global variables.
'''
class MouseMetadata:
    def __init__(self, df: pd.DataFrame):
        # A DataFrame representing the mouse over time
        self.data = df

        # Specific metadata that may be desirable to know. Each is initialized
        # to None but can be calculated with a method. Each method returns a
        # dictionary containing the desired attribute for each body part
        self.time_in_center: Dict[str, float] | None = None
        self.time_on_outside: Dict[str, float] | None = None
        self.average_velocity: Dict[str, float] | None = None
        self.total_distance: Dict[str, float] | None = None

    def calculate_time_in_center(self):
        self.time_in_center = {}
        # For each body part...
        for part in BODY_PART_LABELS:
            # Create a map of valid rows
            within_center = (
                    (self.data[(part, 'x')] >= CENTER_RECT.x_min) &
                    (self.data[(part, 'x')] <= CENTER_RECT.x_max) &
                    (self.data[(part, 'y')] >= CENTER_RECT.y_min) &
                    (self.data[(part, 'y')] <= CENTER_RECT.y_max))
            # Add up all the rows in the map and divide by frames per second
            self.time_in_center[part] = float(within_center.sum() / FRAMES_PER_SECOND)

    def calculate_time_on_outside(self):
        self.time_on_outside = {}
        # For each body part...
        for part in BODY_PART_LABELS:
            # Create a map of valid rows
            within_center = (
                    (self.data[(part, 'x')] <= CENTER_RECT.x_min) |
                    (self.data[(part, 'x')] >= CENTER_RECT.x_max) |
                    (self.data[(part, 'y')] <= CENTER_RECT.y_min) |
                    (self.data[(part, 'y')] >= CENTER_RECT.y_max))
            # Add up all the rows in the map and divide by frames per second
            self.time_on_outside[part] = float(within_center.sum() / FRAMES_PER_SECOND)

    def calculate_total_distance(self):
        self.total_distance = {}
        # For each body part...
        for part in BODY_PART_LABELS:
            # Get the difference between frames for each distance dimension
            dx = self.data[(part, 'x')].diff()
            dy = self.data[(part, 'y')].diff()
            # Calculate the difference in distance for each frame
            distance = np.sqrt(dx**2 + dy**2)
            # Add up the differences in distance for every frame
            self.total_distance[part] = float(distance.sum())

    def calculate_average_velocity(self):
        self.average_velocity = {}
        # Make sure total_distance is calculated
        if self.total_distance == None:
            self.calculate_total_distance()
        # For each body part...
        for part in BODY_PART_LABELS:
            total_distance = self.total_distance[part]
            frames = len(self.data)
            self.average_velocity[part] = total_distance / (frames / FRAMES_PER_SECOND)

    def calculate_meta_data(self):
        self.calculate_time_in_center()
        self.calculate_time_on_outside()
        self.calculate_total_distance()
        self.calculate_average_velocity()

















