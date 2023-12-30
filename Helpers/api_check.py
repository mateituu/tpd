# Import dependencies
import os
from sys import exit


# Define api key check
def api_check():
    # Create Config directory if it doesn't exist
    if 'Config' not in os.listdir(fr'{os.getcwd()}'):
        os.makedirs(f'{os.getcwd()}/Config')
    # Create api-key.txt if it doesn't exist
    if not os.path.isfile(f'{os.getcwd()}/Config/api-key.txt'):
        with open(f'{os.getcwd()}/Config/api-key.txt', 'w') as api_key_text:
            api_key_text.write("Place your API key on this line")
            return "First run"
    # Grab API Key from the text file
    with open(f'{os.getcwd()}/Config/api-key.txt') as API_Key_Text:
        api_key = API_Key_Text.readline()
        if api_key != "Place your API key on this line":
            return api_key
        else:
            return None
