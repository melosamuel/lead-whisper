from datetime import datetime
from pandas import DataFrame
import logging
import pandas as pd
import pywhatkit as kit
import random
import time

class NotAValidContactError(Exception):
    """Fires when the column B of the .xlsx file is not a cellphone number or email"""

    def __init__(self, message):
        super().__init__(message)

def add_lead_to_xlsx(data_frame: DataFrame, xlsx: DataFrame) -> DataFrame:
    """Add the contacts from the provided DataFrame to the existing Excel file.

    Args:
        data_frame (DataFrame): A DataFrame containing the contacts to be added.
        xlsx (DataFrame): The existing DataFrame read from the Excel file.

    Returns:
        DataFrame: The updated DataFrame after adding the new contacts.
    """

    PATH = "./files/feedback.xlsx"

    df = pd.concat([xlsx, data_frame], ignore_index=True)

    try:
        df.to_excel(PATH, index=False)
        logging.info("Lead added to excel")
    except Exception as ex:
        logging.error(f"Error saving lead to excel: {ex}")

    return df

def get_daytime() -> str:
    """Returns the daytime

    Returns:
        str: The daytime ('morning', 'afternoon' or 'evening')
    """

    current_hour = datetime.now().hour

    if 5 <= current_hour < 12:
        return "morning"
    elif 12 <= current_hour < 18:
        return "afternoon"
    else:
        return "evening"

def filter_messages_by_daytime(messages: list) -> list:
    """Returns only the messages that fits the daytime

    Args:
        messages (list): A list with all custom messages

    Returns:
        list: Filtered messages
    """

    daytime = get_daytime()
    filtered_messages = []

    for message in messages:
        if message.lower().startswith("any") or daytime in message.lower():
            filtered_messages.append(message.strip().split(':', 1))

    return filtered_messages

def send_message(custom_messages: list, name: str, phone_number: str):
    """Whatsapp the lead a custom message

    Args:
        custom_messages (list): A list containing all the custom messages
        name (str): The name of the contact
        phone_number (str): The phone number of the contact
        log (Logger): Configured log
    """

    first_name = name.split()[0]
    
    filtered_messages = filter_messages_by_daytime(custom_messages)

    raw_message = random.choice(filtered_messages)[1]
    message = raw_message.replace(r'{nome}', first_name)

    wait = 15

    try:
        kit.sendwhatmsg_instantly(str(phone_number), str(message), wait_time=wait, tab_close=True)
        logging.info(f"Message sent to {name}")
    except Exception as e:
        logging.error(f"Error while trying to send message to {name}: {e}")
    finally:
        time.sleep(30)

def verify_existing_lead(name: str, phone_number: str, xlsx: DataFrame) -> bool:
    """Verifies if the name and number are already registered in the xlsx file

    Args:
        name (str): The name of te contact
        phone_number (str): The phone number of the contact
        xlsx (DataFrame): The excel file

    Returns:
        bool | bool: Returns True if the name and number exists in the excel file, or False otherwise. And if the user can send message to that contact
    """

    existing_lead = (name, phone_number)

    for _, row in xlsx.iterrows():
        contact_name = row['Name']
        contact_number = row['Number']
        
        combination = (contact_name, contact_number)

        if existing_lead == combination:
            can_send_message = row['Send Message']

            return True, can_send_message
        
    return False, True

def run(leads: dict, messages: list, xlsx: DataFrame):
    leads_to_add = {
        "Name": [],
        "Number": [],
        "Send Message": []
    }

    for name, number in leads.items():
        try:
            lead_exists, send = verify_existing_lead(name, number, xlsx)
        except Exception as e:
            raise Exception(f"There is no column named {e}")
        
        if send != "No":
            send_message(messages, name, number)

            if not lead_exists:
                leads_to_add["Name"].append(name)
                leads_to_add["Number"].append(number)
                leads_to_add["Send Message"].append("Yes")

    if leads_to_add["Name"]:
        leads_df = pd.DataFrame(leads_to_add)
        xlsx = add_lead_to_xlsx(leads_df, xlsx)

    return xlsx