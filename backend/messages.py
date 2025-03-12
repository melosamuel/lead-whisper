class EmptyFileError(Exception):
    """Fires when a file is empty"""

    def __init__(self, message):
        super().__init__(message)

def run(path: str) -> list:
    """Handle the .txt file data

    Args:
        path (str): File path to the .txt file containing the custom messages to send

    Returns:
        list: A dict fullfield by all the custom messages
    """

    lines = []

    try:
        with open(path, 'r', encoding='UTF-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise Exception(f"\nFile Not Found: {path}\n")

    if not lines:
        raise EmptyFileError(f"\nThe file '{path}' is empty!\n") 

    return lines