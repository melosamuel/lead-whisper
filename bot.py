from backend import assistant
from backend import csv
from backend import messages
from backend import xlsx
import logging
import sys

CSV_FILE_PATH = "./files/contacts.csv"
XLSX_FILE_PATH = "./files/feedback.xlsx"
MESSAGES_FILE_PATH = "./files/messages.txt"

def main():
    logging.basicConfig(filename='./LOG/app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    try:
        leads = csv.run(path=CSV_FILE_PATH)
        custom_messages = messages.run(path=MESSAGES_FILE_PATH)
        xlsx_file = xlsx.run(path=XLSX_FILE_PATH)

        assistant.run(leads=leads, messages=custom_messages, xlsx=xlsx_file)
    except Exception as e:
        logging.critical(e)
        sys.exit(1)

if __name__ == "__main__":
    main()