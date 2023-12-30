# Import dependencies
import Helpers
import os
from sys import exit


def capability_check():
    # Check for .WVD and API Key, exit program if neither exist.
    Device = Helpers.wvd_check.wvd_check()
    if Device is None:
        API_Key = Helpers.api_check.api_check()
        if API_Key == "First run" or API_Key == None:
            exit(f"No CDM or API key found, please place a CDM in {os.getcwd()}/WVDs or an API key in {os.getcwd()}/Config/api-key.txt")
        else:
            print("No local device found, remote decryption only.")
            print(f'Using API Key: {API_Key}\n')
            return None, API_Key
    elif Device is not None:
        API_Key = Helpers.api_check.api_check()
        if API_Key == "First run" or API_Key == None:
            print("No API key found, local decryption only.")
            print(f'Using device at {Device}\n')
            return Device, None
        else:
            print(f'Local and remote decryption available.')
            print(f'Using device at {Device}')
            print(f'Using API Key: {API_Key}\n')
            return Device, API_Key
