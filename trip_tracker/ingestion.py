import h5py
import pandas as pd
from variables import BODY_PART_LABELS, COORDINATE_LABELS, LIKELIHOOD_THRESHOLD

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
