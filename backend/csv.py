from pandas.errors import EmptyDataError
import pandas as pd

def run(path: str) -> dict:
    """Handle the .csv file data

    Args:
        path (str): File path to the .csv file containing the contacts' name and number

    Returns:
        dict: A dict fullfield by the name and number of each contact in the list
    """

    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        raise Exception(f"\nFile Not Found: {path}\n")
    except EmptyDataError:
        raise Exception(f"\nEmpty File: {path}\n")

    contacts = {}

    try:
        for _, row in df.iterrows():
            number = f"+{row['Number']}"
            name = row['Name']

            contacts[name] = number
    except KeyError:
        raise Exception(f"\nERROR: The .csv file must have the following keys: Name and Number\n")

    return contacts