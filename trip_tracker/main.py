########
# MAIN #
########
'''
See the README for an overview of the libraries.
@author: calepayson
'''

from variables import *
from mouse import MouseMetadata
from ingestion import load_h5_data_into_dataframe, clean_raw_df
from video import test_program_with_video

def main():
    # Read in the data
    h5_df = load_h5_data_into_dataframe(DATA_FILE_NAME)
    clean_df = clean_raw_df(h5_df)

    # Calculate all the metadata
    mouse = MouseMetadata(clean_df)
    mouse.calculate_metadata()

    # YOUR CODE HERE...

    # Comment/uncomment this line to annotate the video with the mouse metadata
    # test_program_with_video(VIDEO_FILE_NAME, mouse)

if __name__ == "__main__":
    main()
