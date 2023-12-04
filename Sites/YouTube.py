# Import dependencies
import json

from pywidevine import PSSH
from pywidevine import Cdm
from pywidevine import Device
import Helpers.cache_key
import requests
import base64


# Defining decrypt function for YouTube
def decrypt_youtube(wvd: str = None, license_curl_headers: dict = None, license_curl_cookies: dict = None, license_curl_json: dict = None):

    # prepare pssh
    pssh = PSSH("AAAAQXBzc2gAAAAA7e+LqXnWSs6jyCfc1R0h7QAAACEiGVlUX01FRElBOjZlMzI4ZWQxYjQ5YmYyMWZI49yVmwY=")
    license_url = input("License URL: ")
    print("\n")

    # load device
    device = Device.load(wvd)

    # load CDM from device
    cdm = Cdm.from_device(device)

    # open CDM session
    session_id = cdm.open()

    # Generate challenge
    challenge = cdm.get_license_challenge(session_id, pssh)

    # Insert the challenge into the JSON data
    license_curl_json["licenseRequest"] = base64.b64encode(challenge).decode()

    # send license challenge
    license = requests.post(
        url=license_url,
        headers=license_curl_headers,
        cookies=license_curl_cookies,
        json=license_curl_json
    )

    if license.status_code != 200:
        print(license.content)
        exit("Could not complete license challenge")

    # Extract license from json dict
    licence = license.json()["license"].replace("-", "+").replace("_", "/")

    # parse license challenge
    cdm.parse_license(session_id, licence)

    # assign variable for returned keys
    returned_keys = ""
    for key in cdm.get_keys(session_id):
        if key.type != "SIGNING":
            returned_keys += f"{key.kid.hex}:{key.key.hex()}\n"

    # close session, disposes of session data
    cdm.close(session_id)

    # Cache the keys
    Helpers.cache_key.cache_keys(pssh="YouTube", keys=returned_keys)

    # Print out the keys
    print(f'Keys:\n{returned_keys}')

    # Return the keys for future ripper use.
    return returned_keys


# Defining remote decrypt function for Crunchyroll
def decrypt_youtube_remotely(api_key: str = None, license_curl_headers: dict = None, license_curl_json: dict = None, license_curl_cookies: dict = None):

    # Set CDM Project API URL
    api_url = "https://api.cdm-project.com"

    # Set API device
    api_device = "CDM"

    # Ask for PSSH
    input_license_url = input("License URL: ")
    print("\n")

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
        "init_data": "AAAAQXBzc2gAAAAA7e+LqXnWSs6jyCfc1R0h7QAAACEiGVlUX01FRElBOjZlMzI4ZWQxYjQ5YmYyMWZI49yVmwY="
    }

    # Generate the license challenge
    generate_challenge = requests.post(url=f'{api_url}/{api_device}/get_license_challenge/AUTOMATIC', headers=api_key_headers, json=generate_challenge_json)

    # Retrieve the challenge and base64 decode it
    challenge = base64.b64decode(generate_challenge.json()["data"]["challenge_b64"])

    # Insert the challenge into the JSON data
    license_curl_json["licenseRequest"] = base64.b64encode(challenge).decode()

    # Send the challenge to the widevine license server
    license = requests.post(
        url=input_license_url,
        headers=license_curl_headers,
        json=license_curl_json,
        cookies=license_curl_cookies
    )

    # Retrieve the license message
    license = license.json()["license"].replace("-", "+").replace("_", "/")

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

    # Cache the keys
    Helpers.cache_key.cache_keys(pssh="YouTube", keys=returned_keys)

    # Print out keys
    print(f'Keys:\n{returned_keys}')

    # Close session
    requests.get(url=f'{api_url}/{api_device}/close/{session_id}', headers=api_key_headers)