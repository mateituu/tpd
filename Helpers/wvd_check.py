# Import dependencies
import os
import glob
from sys import exit


# Define WVD device check
def wvd_check():
    try:
        # Check to see if the WVDs folder exist, if not create it
        if 'WVDs' not in os.listdir(fr'{os.getcwd()}'):
            os.makedirs(f'{os.getcwd()}/WVDs')
        # Use glob to get the name of the .wvd
        extracted_device = glob.glob(f'{os.getcwd()}/WVDs/*.wvd')[0]
        # Return the device path
        return extracted_device
    except:
        # Check to see if the WVDs folder exist, if not create it
        if 'WVDs' not in os.listdir(fr'{os.getcwd()}'):
            os.makedirs(f'{os.getcwd()}/WVDs')
        # Stop the program and print out instructions
        return None
