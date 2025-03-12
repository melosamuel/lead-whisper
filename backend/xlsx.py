from pandas import DataFrame
import pandas as pd
import zipfile

def run(path: str) -> DataFrame:
    """Handle the .xlsx file data

    Args:
        path (str): File path to the .xlsx file containing the contacts' data

    Returns:
        DataFrame: The .xlsx file
    """

    try:
        df = pd.read_excel(path, dtype={'Name': str, 'Number': str}, engine='openpyxl')
    except FileNotFoundError:
        raise Exception(f"\nFile Not Found: {path}\n")
    except zipfile.BadZipFile:
        raise Exception(f"\nThe file '{path}' is empty (without keys) or even corrupted\n")

    return df