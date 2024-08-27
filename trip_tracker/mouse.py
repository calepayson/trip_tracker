import pandas as pd
import numpy as np
from variables import BODY_PART_LABELS, CENTER_RECT, FRAMES_PER_SECOND

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
        self.time_in_center: dict[str, float] | None = None
        self.time_on_outside: dict[str, float] | None = None
        self.average_velocity: dict[str, float] | None = None
        self.total_distance: dict[str, float] | None = None

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

    def calculate_metadata(self):
        self.calculate_time_in_center()
        self.calculate_time_on_outside()
        self.calculate_total_distance()
        self.calculate_average_velocity()
