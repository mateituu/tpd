# Import dependencies
import os
import Helpers
import Sites
import license_curl
import argparse

# Get device and api key
device, api_key = Helpers.capability_check.capability_check()

# Database check, if it doesn't exist, create it.
Helpers.database_check.database_check()

# Initialize argparse and set variable
parser = argparse.ArgumentParser(description="Options for decryption")

# Create mutually exclusive groups for switches
services = parser.add_mutually_exclusive_group()

# Add switches to the mutually exclusive groups
services.add_argument('--crunchyroll', action='store_true', help="Decrypt Crunchyroll")
services.add_argument('--crunchyroll-remote', action='store_true', help="Decrypt Crunchyroll remotely")
services.add_argument('--youtube', action='store_true', help="Decrypt YouTube")
services.add_argument('--youtube-remote', action='store_true', help="Decrypt YouTube remotely")
services.add_argument('--generic-remote', action='store_true', help="Decrypt generic services remotely")

# Add web download switch
parser.add_argument('--web-dl', help="Web download", action='store_true')

# Assign the switches a variable
switches = parser.parse_args()


# Based on the selected switch within the mutually exclusive group, perform actions
if switches.crunchyroll:
    # Perform action for --crunchyroll
    if switches.web_dl:
        mpd = input("MPD URL: ")
        file = Helpers.download.web_dl_crunchyroll(mpd=mpd, device=device)
        print(f'Saved at {file[0]}')
    else:
        Sites.Crunchyroll.decrypt_crunchyroll(wvd=device, license_curl_headers=license_curl.headers)


elif switches.crunchyroll_remote:
    # Perform action for --crunchyroll-remote
    if switches.web_dl:
        mpd = input("MPD URL: ")
        file = Helpers.download.web_dl_crunchyroll(mpd=mpd, api_key=api_key, remote=True)
        print(f'Saved at {file[0]}')
    else:
        Sites.Crunchyroll.decrypt_crunchyroll_remotely(api_key=api_key, license_curl_headers=license_curl.headers)

elif switches.youtube:
    # Perform action for --YouTube
    if switches.web_dl:
        url = input("YouTube URL: ")
        file = Helpers.download.youtube_dlp(url=url, device=device)
        print(f'Saved at {file}')
    else:
        Sites.YouTube.decrypt_youtube(wvd=device, license_curl_headers=license_curl.headers, license_curl_json=license_curl.json_data, license_curl_cookies=license_curl.cookies)


elif switches.youtube_remote:
    # Perform action for --youtube-remote
    if switches.web_dl:
        url = input("YouTube URL: ")
        file = Helpers.download.youtube_dlp(url=url, api_key=api_key, remote=True)
        print(f'Saved at {file}')
    else:
        Sites.YouTube.decrypt_youtube_remotely(api_key=api_key, license_curl_headers=license_curl.headers, license_curl_json=license_curl.json_data, license_curl_cookies=license_curl.cookies)


elif switches.generic_remote:
    # Perform action for --generic-remote
    if switches.web_dl:
        mpd = input("MPD URL: ")
        file = Helpers.download.web_dl_generic(mpd=mpd, api_key=api_key, remote=True)
        print(f'Saved at {file[0]}')
    else:
        Sites.Generic.decrypt_generic_remotely(api_key=api_key, license_curl_headers=license_curl.headers)


else:
    # If no switch is provided, perform a default action
    if switches.web_dl:
        mpd = input("MPD URL: ")
        file = Helpers.download.web_dl_generic(mpd=mpd, device=device)
        print(f'Saved at {file[0]}')
    else:
        Sites.Generic.decrypt_generic(wvd=device, license_curl_headers=license_curl.headers)
