import os
import zipfile
import shutil
import requests
from tqdm import tqdm


# Create / Check folders function
def create_folders():
    # Check for required directories
    for directory in ['binaries', 'download']:
        # Create them if they don't exist
        if directory not in os.listdir(os.getcwd()):
            os.makedirs(f'{os.getcwd()}/{directory}')
            # If they do exist, check for temp, create if it doesn't exist
            if 'temp' not in f'{os.listdir(os.getcwd())}/download':
                os.makedirs(f'{os.getcwd()}/download/temp')


# Create / Check binaries function
def create_binaries():
    # Check if the required binaries exist, if not, download them.

    # Iterate through required binaries
    for binary in ["n_m3u8dl-re.exe", "mp4decrypt.exe", "ffmpeg.exe", "yt-dlp.exe"]:

        # Perform checks for each binary
        if not os.path.isfile(f"{os.getcwd()}/binaries/{binary}"):

            # FFmpeg
            if binary == "ffmpeg.exe":

                # Download windows zip file for FFmpeg
                ffmpeg_download = requests.get(
                    "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip",
                    stream=True)
                total_size = int(ffmpeg_download.headers.get('content-length', 0))
                with open(f"{os.getcwd()}/download/temp/ffmpeg.zip", 'wb') as download:
                    with tqdm(total=total_size, unit='B', unit_scale=True,
                              desc="Downloading ffmpeg.zip") as progress_bar:
                        for data in ffmpeg_download.iter_content(chunk_size=1024):
                            download.write(data)
                            progress_bar.update(len(data))

                # Unzip FFmpeg
                with zipfile.ZipFile(f"{os.getcwd()}/download/temp/ffmpeg.zip", "r") as ffmpeg_zip:
                    file_count = len(ffmpeg_zip.infolist())
                    with tqdm(total=file_count, unit='file', desc="Extracting ffmpeg.zip") as unzip_progress_bar:
                        for file in ffmpeg_zip.infolist():
                            ffmpeg_zip.extract(file, path=f"{os.getcwd()}/download/temp")
                            unzip_progress_bar.update(1)

                # Copy ffmpeg binary to binaries
                shutil.copy2(f"{os.getcwd()}/download/temp/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe",
                             f"{os.getcwd()}/binaries")

                # Remove the zip
                os.remove(f"{os.getcwd()}/download/temp/ffmpeg.zip")

                # Remove the folder
                shutil.rmtree(f"{os.getcwd()}/download/temp/ffmpeg-master-latest-win64-gpl")

                # Print a new line
                print()

            # MP4 Decrypt
            elif binary == "mp4decrypt.exe":

                # Download mp4decrypt zip file
                mp4decrypt_download = requests.get(
                    "https://www.bok.net/Bento4/binaries/Bento4-SDK-1-6-0-639.x86_64-microsoft-win32.zip", stream=True)
                total_size = int(mp4decrypt_download.headers.get('content-length', 0))
                with open(f"{os.getcwd()}/download/temp/mp4decrypt.zip", 'wb') as download:
                    with tqdm(total=total_size, unit='B', unit_scale=True,
                              desc="Downloading mp4decrypt.zip") as progress_bar:
                        for data in mp4decrypt_download.iter_content(chunk_size=1024):
                            download.write(data)
                            progress_bar.update(len(data))

                # Unzip mp4decrypt
                with zipfile.ZipFile(f"{os.getcwd()}/download/temp/mp4decrypt.zip", "r") as mp4decrypt_zip:
                    file_count = len(mp4decrypt_zip.infolist())
                    with tqdm(total=file_count, unit='file', desc="Extracting mp4decrypt.zip") as unzip_progress_bar:
                        for file in mp4decrypt_zip.infolist():
                            mp4decrypt_zip.extract(file, path=f"{os.getcwd()}/download/temp")
                            unzip_progress_bar.update(1)

                # Copy mp4decrypt binary to binaries
                shutil.copy2(
                    f"{os.getcwd()}/download/temp/Bento4-SDK-1-6-0-639.x86_64-microsoft-win32/bin/mp4decrypt.exe",
                    f"{os.getcwd()}/binaries")

                # Deleting the zip file
                os.remove(f"{os.getcwd()}/download/temp/mp4decrypt.zip")

                # Deleting the directory
                shutil.rmtree(f"{os.getcwd()}/download/temp/Bento4-SDK-1-6-0-639.x86_64-microsoft-win32")

                # Print a new line
                print()

            # n_m3u8dl-re
            elif binary == "n_m3u8dl-re.exe":

                # Download n_m3u8dl-re zip file
                n_m3u8dl_re_download = requests.get(
                    "https://github.com/nilaoda/N_m3u8DL-RE/releases/download/v0.2.0-beta/N_m3u8DL-RE_Beta_win-x64_20230628.zip",
                    stream=True)
                total_size = int(n_m3u8dl_re_download.headers.get('content-length', 0))
                with open(f"{os.getcwd()}/download/temp/n_m3u8dl-re.zip", 'wb') as download:
                    with tqdm(total=total_size, unit='B', unit_scale=True,
                              desc="Downloading n_m3u8dl-re.zip") as progress_bar:
                        for data in n_m3u8dl_re_download.iter_content(chunk_size=1024):
                            download.write(data)
                            progress_bar.update(len(data))

                # Unzip n_m3u8dl-re
                with zipfile.ZipFile(f"{os.getcwd()}/download/temp/n_m3u8dl-re.zip", "r") as nm3u8dl_re_zip:
                    file_count = len(nm3u8dl_re_zip.infolist())
                    with tqdm(total=file_count, unit='file', desc="Extracting n_m3u8dl-re.zip") as unzip_progress_bar:
                        for file in nm3u8dl_re_zip.infolist():
                            nm3u8dl_re_zip.extract(file, path=f"{os.getcwd()}/download/temp")
                            unzip_progress_bar.update(1)

                # Copy n_m3u8dl-re binary to binaries
                shutil.copy2(f"{os.getcwd()}/download/temp/N_m3u8DL-RE_Beta_win-x64/N_m3u8DL-RE.exe",
                             f"{os.getcwd()}/binaries")

                # Delete zip file
                os.remove(f"{os.getcwd()}/download/temp/n_m3u8dl-re.zip")

                # Delete directory
                shutil.rmtree(f"{os.getcwd()}/download/temp/N_m3u8DL-RE_Beta_win-x64")

                # Print a new line
                print()

            # YT-DLP
            elif binary == "yt-dlp.exe":

                # Download yt-dlp exe
                yt_dlp_download = requests.get(
                    "https://github.com/yt-dlp/yt-dlp/releases/download/2023.11.16/yt-dlp_x86.exe",
                    stream=True)
                total_size = int(yt_dlp_download.headers.get('content-length', 0))
                with open(f"{os.getcwd()}/download/yt-dlp.exe", 'wb') as download:
                    with tqdm(total=total_size, unit='B', unit_scale=True,
                              desc="Downloading yt-dlp") as progress_bar:
                        for data in yt_dlp_download.iter_content(chunk_size=1024):
                            download.write(data)
                            progress_bar.update(len(data))

                # Copy yt-dlp binary to binaries
                shutil.copy2(f"{os.getcwd()}/download/yt-dlp.exe",
                             f"{os.getcwd()}/binaries")

                # Remove binary from download folder
                os.remove(f"{os.getcwd()}/download/yt-dlp.exe")

                # Print a new line
                print()
