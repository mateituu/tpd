import requests
import re


# Define MPD / m3u8 PSSH parser
def parse_pssh(manifest_url):
    manifest = manifest_url
    try:
        response = requests.get(manifest)
    except:
        pssh = input("Couldn't retrieve manifest, please input PSSH: ")
        return pssh
    try:
        matches = re.finditer(r'<cenc:pssh(?P<any>(.*))>(?P<pssh>(.*))</cenc:pssh>', response.text)
        pssh_list = []

        for match in matches:
            if match.group and not match.group("pssh") in pssh_list and len(match.group("pssh")) < 300:
                pssh_list.append(match.group("pssh"))

        if len(pssh_list) < 1:
            matches = re.finditer(r'URI="data:text/plain;base64,(?P<pssh>(.*))"', response.text)
            for match in matches:
                if match.group("pssh") and match.group("pssh").upper().startswith("A") and len(match.group("pssh")) < 300:
                    pssh_list.append(match.group("pssh"))
        return f'{pssh_list[0]}'
    except:
        return None