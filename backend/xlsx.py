from pandas import DataFrame
import logging
import pandas as pd
import re
import zipfile

def is_phone_number(data: str) -> bool:
    """Tell if the given data is a valid phone number or not

    Args:
        data (str): The possible phone number

    Returns:
        bool: Returns True if the given data is a valid phone number, or False otherwise
    """

    phone_regex = r'^\+?\d{1,3}?\s?\(?\d{1,4}?\)?[\s.-]?\d{1,4}[\s.-]?\d{1,4}[\s.-]?\d{1,9}$'

    filtered_data = re.sub(r'[() ]', '', data)

    return re.match(phone_regex, filtered_data) is not None

def is_email(data: str) -> bool:
    """Tell if the given data is a valid email or not

    Args:
        data (str): The possible email

    Returns:
        bool: Returns True if the given data is a valid email, or False otherwise
    """

    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, data) is not None

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
        raise Exception(f"File Not Found: {path}")
    except zipfile.BadZipFile:
        raise Exception(f"The file '{path}' is empty (without keys) or even corrupted")
    
    for index, row in df.iterrows():
        contact = str(row['Number'])

        if not (is_phone_number(contact) or is_email(contact)):
            logging.warning(f"The contact at line {index} has not a valid contact number or email! Please, verify and fix it!")

    return df