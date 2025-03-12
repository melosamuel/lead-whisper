from pandas import DataFrame
import pandas as pd
import pywhatkit as kit
import random
import re
import time

class NotAValidContactError(Exception):
    """Fires when the column B of the .xlsx file is not a cellphone number or email"""

    def __init__(self, message):
        super().__init__(message)

def add_lead_to_xlsx(name: str, number: str, xlsx: DataFrame):
    """Add the name and number of the contact to the excel file

    Args:
        name (str): The name of the contact
        number (str): The phone number of the contact
        xlsx (DataFrame): The excel file
    """

    new_row = pd.DataFrame({'A': [name], 'B': [number]})
    df = pd.concat([xlsx, new_row], ignore_index=True)

    df.to_excel()

def send_message(custom_messages: list, name: str, number: str):
    """Whatsapp the lead a custom message

    Args:
        custom_messages (list): A list containing all the custom messages
        name (str): The name of the contact
        number (str): The phone number of the contact
    """

    first_name = name.split()[0]
    raw_message = random.choice(custom_messages)
    message = raw_message.replace(r'{nome}', first_name)

    try:
        kit.sendwhatmsg_instantly(number, message, 15, tab_close=True)
        print(f"\n### Message sent to {name}")

    except Exception as e:
        print(f"\n### Error while trying to send message to {name}")
    finally:
        time.sleep(30)

def is_phone_number(data: str) -> bool:
    """Tell if the given data is a valid phone number or not

    Args:
        data (str): The possible phone number

    Returns:
        bool: Returns True if the given data is a valid phone number, or False otherwise
    """

    phone_regex = r'^\+?\d{1,3}?\s?\(?\d{1,4}?\)?[\s.-]?\d{1,4}[\s.-]?\d{1,4}[\s.-]?\d{1,9}$'

    return re.match(phone_regex, data) is not None

def is_email(data: str) -> bool:
    """Tell if the given data is a valid email or not

    Args:
        data (str): The possible email

    Returns:
        bool: Returns True if the given data is a valid email, or False otherwise
    """

    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, data) is not None

def verify_existing_lead(name: str, number: str, xlsx: DataFrame) -> bool:
    """Verifies if the name and number are already registered in the xlsx file

    Args:
        name (str): The name of te contact
        number (str): The phone number of the contact
        xlsx (DataFrame): The excel file

    Returns:
        bool: Returns True if the name and number exists in the excel file, or False otherwise
    """

    existing_lead = (name, number)

    for index, row in xlsx.iterrows():
        name = row['Name']
        contact = row['Number']

        if not (is_phone_number(contact) or is_email(contact)): 
            print(f"\nThe contact at line {index} has not a valid contact number or email! Please, verify and try again!\n")
        
        combination = (name, contact)

        if existing_lead == combination:
            return True
        
    return False

def run(leads: dict, messages: list, xlsx: DataFrame):
    for name, number in leads.items():
        try:
            lead_exists = verify_existing_lead(name, number, xlsx)
        except Exception as e:
            raise Exception(f"\nThere is no column named {e}\n")
        
        send_message(messages, name, number)

        if not lead_exists:
            add_lead_to_xlsx(name, number, xlsx)