from variables import *
from mouse import MouseMetadata
from ingestion import load_h5_data_into_dataframe, clean_raw_df
from video import test_program_with_video

def main():
    h5_df = load_h5_data_into_dataframe(DATA_FILE_NAME)
    clean_df = clean_raw_df(h5_df)

    mouse = MouseMetadata(clean_df)
    mouse.calculate_metadata()

if __name__ == "__main__":
    main()
