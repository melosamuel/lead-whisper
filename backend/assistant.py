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

def add_lead_to_xlsx(name: str, phone_number: str, xlsx: DataFrame):
    """Add the name and number of the contact to the excel file

    Args:
        name (str): The name of the contact
        phone_number (str): The phone number of the contact
        xlsx (DataFrame): The excel file
    """

    PATH = "./files/feedback.xlsx"

    new_row = pd.DataFrame({'Name': [name], 'Number': [phone_number], 'Send Message': ["Yes"]})
    df = pd.concat([xlsx, new_row], ignore_index=True)

    df.to_excel(PATH, index=False)

    logging.info("Lead added to excel")

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
    for name, number in leads.items():
        try:
            lead_exists, send = verify_existing_lead(name, number, xlsx)
        except Exception as e:
            raise Exception(f"There is no column named {e}")
        
        if send != "No":
            send_message(messages, name, number)

            if not lead_exists:
                add_lead_to_xlsx(name, number, xlsx)