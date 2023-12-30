# Import dependencies

from pywidevine import PSSH
from pywidevine import Cdm
from pywidevine import Device
import requests
import base64
import os
import Helpers
from sys import exit


# Defining decrypt function for canal plus
def decrypt_canal_plus(wvd: str = None, license_curl_headers: dict = None, license_curl_json: dict = None, mpd_url: str = None):

    # Exit if no device
    if wvd is None:
        exit(f"No CDM! to use local decryption place a .wvd in {os.getcwd()}/WVDs")

    # Try getting pssh via MPD URL if web-dl
    if mpd_url is not None:
        input_pssh = Helpers.mpd_parse.parse_pssh(mpd_url)
        if input_pssh is not None:
            print(f'\nPSSH found: {input_pssh}')
        else:
            input_pssh = input(f"\nPSSH not found! Input PSSH: ")

    # Ask for PSSH if just keys function
    if mpd_url is None:
        # Ask for PSSH if web-dl not selected:
        input_pssh = input(f"\nPSSH: ")


    # prepare pssh
    pssh = PSSH(input_pssh)

    # Ask for license URL
    license_url = "https://ltv.slc-app-aka.prod.bo.canal.canalplustech.pro/ottlivetv/api/V4/zones/cpfra/locations/FR/devices/11/apps/1/jobs/GetLicence"

    # load device
    device = Device.load(wvd)

    # load CDM from device
    cdm = Cdm.from_device(device)

    # open CDM session
    session_id = cdm.open()


    challenge = cdm.get_license_challenge(session_id, pssh)

    # Set the challenge in the json data
    license_curl_json['ServiceRequest']['InData']['ChallengeInfo'] = base64.b64encode(challenge).decode()

    # send license challenge
    license = requests.post(
        url=license_url,
        headers=license_curl_headers,
        json=license_curl_json
    )

    if license.status_code != 200:
        print(license.content)
        exit("Could not complete license challenge")

    # Extract license from json dict
    license = license.json()['ServiceResponse']['OutData']['LicenseInfo']

    # parse license challenge
    cdm.parse_license(session_id, license)

    # assign variable for returned keys
    returned_keys = ""
    for key in cdm.get_keys(session_id):
        if key.type != "SIGNING":
            returned_keys += f"{key.kid.hex}:{key.key.hex()}\n"

    # assign variable for mp4decrypt keys
    mp4decrypt_keys = []
    for key in cdm.get_keys(session_id):
        if key.type != "SIGNING":
            mp4decrypt_keys.append('--key')
            mp4decrypt_keys.append(f'{key.kid.hex}:{key.key.hex()}')

    # close session, disposes of session data
    cdm.close(session_id)

    # Cache the keys
    Helpers.cache_key.cache_keys(pssh=input_pssh, keys=returned_keys)

    # Print out the keys
    print(f'\nKeys:\n{returned_keys}')

    # Return the keys for future ripper use.
    return mp4decrypt_keys


# Defining remote decrypt function for generic services
def decrypt_generic_remotely(api_key: str = None, license_curl_headers: dict = None, mpd_url: str = None):

    # Exit if no API key
    if api_key is None:
        exit(f"No API Key! to use remote decryption place an API key in {os.getcwd()}/Config/api-key.txt")

    # Set CDM Project API URL
    api_url = "https://api.cdm-project.com"

    # Set API device
    api_device = "CDM"

    # Try getting pssh via MPD URL if web-dl
    if mpd_url is not None:
        input_pssh = Helpers.mpd_parse.parse_pssh(mpd_url)
        if input_pssh is not None:
            print(f'\nPSSH found: {input_pssh}')
        else:
            input_pssh = input(f"\nPSSH not found! Input PSSH: ")

    # Ask for PSSH if just keys function
    if mpd_url is None:
        # Ask for PSSH if web-dl not selected:
        input_pssh = input(f"\nPSSH: ")

    # Ask for license URL
    input_license_url = input(f"\nLicense URL: ")

    # Set headers for API key
    api_key_headers = {
        "X-Secret-Key": api_key
    }

    # Open CDM session
    open_session = requests.get(url=f'{api_url}/{api_device}/open', headers=api_key_headers)

    # Get the session ID from the open CDM session
    session_id = open_session.json()["data"]["session_id"]

    # Set JSON required to generate a license challenge
    generate_challenge_json = {
        "session_id": session_id,
        "init_data": input_pssh
    }

    # Generate the license challenge
    generate_challenge = requests.post(url=f'{api_url}/{api_device}/get_license_challenge/AUTOMATIC', headers=api_key_headers, json=generate_challenge_json)

    # Retrieve the challenge and base64 decode it
    challenge = base64.b64decode(generate_challenge.json()["data"]["challenge_b64"])

    # Send the challenge to the widevine license server
    license = requests.post(
        url=input_license_url,
        headers=license_curl_headers,
        data=challenge
    )

    # Retrieve the license message
    license = base64.b64encode(license.content).decode()

    # Set JSON required to parse license message
    license_message_json = {
        "session_id": session_id,
        "license_message": license
    }

    # Parse the license
    requests.post(url=f'{api_url}/{api_device}/parse_license', headers=api_key_headers, json=license_message_json)

    # Retrieve the keys
    get_keys = requests.post(url=f'{api_url}/{api_device}/get_keys/ALL',
                             json={"session_id": session_id},
                             headers=api_key_headers)

    # Iterate through the keys, ignoring signing key
    returned_keys = ''
    for key in get_keys.json()["data"]["keys"]:
        if not key["type"] == "SIGNING":
            returned_keys += f"{key['key_id']}:{key['key']}\n"

    # assign variable for mp4decrypt keys
    mp4decrypt_keys = []
    for key in get_keys.json()["data"]["keys"]:
        if not key["type"] == "SIGNING":
            mp4decrypt_keys.append('--key')
            mp4decrypt_keys.append(f"{key['key_id']}:{key['key']}")

    # Cache the keys
    Helpers.cache_key.cache_keys(pssh=input_pssh, keys=returned_keys)

    # Print out keys
    print(f'\nKeys:\n{returned_keys}')

    # Close session
    requests.get(url=f'{api_url}/{api_device}/close/{session_id}', headers=api_key_headers)

    # Return mp4decrypt keys
    return mp4decrypt_keys
