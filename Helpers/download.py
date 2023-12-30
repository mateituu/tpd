import subprocess
import uuid
import glob
import os
import Helpers.binary_check
import Sites.Generic
import license_curl
import Helpers.os_check
from sys import exit


# Web Download function generic
def web_dl_generic(mpd: str = None, device: str = None, api_key: str = None, remote: bool = False):

    # Get the current operating system
    operating_system = Helpers.os_check.get_os_specific()

    # Check for folders
    Helpers.binary_check.create_folders()

    # Check for binaries
    Helpers.binary_check.create_binaries()

    # Create random download name
    download_name = str(uuid.uuid4())

    # Retrieve the keys
    if not remote:
        mp4decrypt_keys, _ = Sites.Generic.decrypt_generic(mpd_url=mpd, wvd=device, license_curl_headers=license_curl.headers)
    if remote:
        mp4decrypt_keys, _ = Sites.Generic.decrypt_generic_remotely(api_key=api_key, license_curl_headers=license_curl.headers, mpd_url=mpd)

    # Define n_m3u8dl-re download parameters
    n_m3u8dl_re_download = [
        f'{os.getcwd()}/binaries/n_m3u8dl-re.exe',
        f'{mpd}',
        '--ffmpeg-binary-path',
        f'{os.getcwd()}/binaries/ffmpeg.exe',
        '--decryption-binary-path',
        f'{os.getcwd()}/binaries/mp4decrypt.exe',
        '--tmp-dir',
        f'{os.getcwd()}/download/temp',
        '--save-dir',
        f'{os.getcwd()}/download',
        '--save-name',
        f'{download_name}',
        '--binary-merge',
        'True',
        '--mux-after-done',
        'format=mkv'
    ] + mp4decrypt_keys
    if operating_system == "Linux":
        n_m3u8dl_re_download[0] = f'{os.getcwd()}/binaries/N_m3u8DL-RE'
        n_m3u8dl_re_download[3] = f'{os.getcwd()}/binaries/ffmpeg'
        n_m3u8dl_re_download[5] = f'{os.getcwd()}/binaries/mp4decrypt'

    subprocess.run(n_m3u8dl_re_download)

    try:
        download_name = glob.glob(f'{os.getcwd()}/download/{download_name}.*')
        return download_name
    except:
        return f'Failed to download!'


# Web Download crunchyroll function
def web_dl_crunchyroll(mpd: str = None, device: str = None, api_key: str = None, remote: bool = False):

    # Get the current operating system
    operating_system = Helpers.os_check.get_os_specific()

    # Check for folders
    Helpers.binary_check.create_folders()

    # Check for binaries
    Helpers.binary_check.create_binaries()

    # Create random download name
    download_name = str(uuid.uuid4())

    # Retrieve the keys
    if not remote:
        mp4decrypt_keys, _ = Sites.Crunchyroll.decrypt_crunchyroll(mpd_url=mpd, wvd=device, license_curl_headers=license_curl.headers)
    if remote:
        mp4decrypt_keys, _ = Sites.Crunchyroll.decrypt_crunchyroll_remotely(api_key=api_key, license_curl_headers=license_curl.headers, mpd_url=mpd)

    # Define n_m3u8dl-re download parameters
    n_m3u8dl_re_download = [
        f'{os.getcwd()}/binaries/n_m3u8dl-re.exe',
        f'--header',
        f'authorization: {license_curl.headers["authorization"]}',
        f'{mpd}',
        '--ffmpeg-binary-path',
        f'{os.getcwd()}/binaries/ffmpeg.exe',
        '--decryption-binary-path',
        f'{os.getcwd()}/binaries/mp4decrypt.exe',
        '--tmp-dir',
        f'{os.getcwd()}/download/temp',
        '--save-dir',
        f'{os.getcwd()}/download',
        '--save-name',
        f'{download_name}',
        '--binary-merge',
        'True',
        '--mux-after-done',
        'format=mkv'
    ] + mp4decrypt_keys
    if operating_system == "Linux":
        n_m3u8dl_re_download[0] = f'{os.getcwd()}/binaries/N_m3u8DL-RE'
        n_m3u8dl_re_download[5] = f'{os.getcwd()}/binaries/ffmpeg'
        n_m3u8dl_re_download[7] = f'{os.getcwd()}/binaries/mp4decrypt'

    subprocess.run(n_m3u8dl_re_download)

    try:
        download_name = glob.glob(f'{os.getcwd()}/download/{download_name}.*')
        return download_name
    except:
        return f'Failed to download!'


# YouTube Download function generic
def youtube_dlp(url: str = None, device: str = None, api_key: str = None, remote: bool = False):

    # Get the current operating system
    operating_system = Helpers.os_check.get_os_specific()

    # Check for folders
    Helpers.binary_check.create_folders()

    # Check for binaries
    Helpers.binary_check.create_binaries()

    # Create random download name
    download_name = str(uuid.uuid4())

    # Retrieve the keys
    if not remote:
        mp4decrypt_keys, _ = Sites.YouTube.decrypt_youtube(wvd=device, license_curl_headers=license_curl.headers, license_curl_json=license_curl.json_data, license_curl_cookies=license_curl.cookies)
    if remote:
        mp4decrypt_keys, _ = Sites.YouTube.decrypt_youtube_remotely(api_key=api_key, license_curl_headers=license_curl.headers, license_curl_json=license_curl.json_data, license_curl_cookies=license_curl.cookies)

    # Define yt-dlp download parameters
    yt_dlp_download = [
        f'{os.getcwd()}/binaries/yt-dlp.exe',
        '-f',
        'bv*+ba/b',
        '--allow-u',
        '-o',
        f'{os.getcwd()}/download/{download_name}.%(ext)s',
        '-S',
        'ext',
        '-S',
        'res:720',
        f'{url}'
    ]
    if operating_system == "Linux":
        yt_dlp_download[0] = f'{os.getcwd()}/binaries/yt-dlp'

    # Run yt-dlp
    subprocess.run(yt_dlp_download)

    # Get the names of the newly downloaded files
    files = glob.glob(f'{os.getcwd()}/download/{download_name}.*')

    # Declare empty list for decrypted files location to be stored
    decrypted_files = []

    # Iterate through all the files and decrypt them
    for file in files:

        # Assign file name variable to be appended to decrypted files list
        file_name = str(uuid.uuid4())

        # define mp4 decrypt parameters
        mp4_decrypt = [
            f'{os.getcwd()}/binaries/mp4decrypt.exe',
            f'{file}',
            f'{os.getcwd()}/download/{file_name}',
        ] + mp4decrypt_keys
        if operating_system == "Linux":
            mp4_decrypt[0] = f'{os.getcwd()}/binaries/mp4decrypt'

        # Run mp4decrypt
        subprocess.run(mp4_decrypt)

        # Append the file to the decrypted file list
        decrypted_files.append(f'{os.getcwd()}/download/{file_name}')

    # Declare a final mux variable
    final_mux = str(uuid.uuid4())

    # Define ffmpeg parameters
    ffmpeg_merge = [
        f"{os.getcwd()}/binaries/ffmpeg.exe",
        '-i',
        f"{decrypted_files[0]}",
        '-i',
        f"{decrypted_files[1]}",
        '-vcodec',
        'copy',
        '-acodec',
        'copy',
        f"{os.getcwd()}/download/{final_mux}.mkv",
    ]
    if operating_system == "Linux":
        ffmpeg_merge[0] = f"{os.getcwd()}/binaries/ffmpeg"

    # Run ffmpeg to merge the files
    subprocess.run(ffmpeg_merge)

    # Try to get a download name and return it
    download_name = glob.glob(f'{os.getcwd()}/download/{final_mux}.*')
    if download_name:
        return download_name
    else:
        return f"Couldn't complete download!"
