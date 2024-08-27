import h5py
import pandas as pd

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

# The minimum viable likelihood for coordinates (any coordinates with a
# probability less than this will be interpolated)
LIKELIHOOD_THRESHOLD = 0.95

# The dimensions of the center rectangle
CENTER_RECT = Rectangle(
        x_min=475,
        y_min=305,
        x_max=845,
        y_max=680,
        )

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

