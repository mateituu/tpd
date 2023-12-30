import os
import subprocess
import zipfile
import shutil
import requests
import tarfile
import stat
from Helpers import os_check
from tqdm import tqdm
from sys import exit


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

    # Check which OS the host is
    operating_system = os_check.get_os_specific()

    # Set binary dictionaries for Windows / Linux
    windows_binaries = ["n_m3u8dl-re.exe", "mp4decrypt.exe", "ffmpeg.exe", "yt-dlp.exe"]
    linux_binaries = ["N_m3u8DL-RE", "mp4decrypt", "ffmpeg", "yt-dlp"]
    if operating_system == "Windows":
        binary_list = windows_binaries
    if operating_system == "Linux":
        binary_list = linux_binaries

    # Check if the required binaries exist, if not, download them.

    # Iterate through required binaries
    for binary in binary_list:

        # Perform checks for each binary
        if not os.path.isfile(f"{os.getcwd()}/binaries/{binary}"):

            # FFmpeg
            if binary == "ffmpeg.exe" or binary =="ffmpeg":

                # Download windows zip file for FFmpeg
                if operating_system == "Windows":
                    ffmpeg_download = requests.get(
                        "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip",
                        stream=True)
                if operating_system == "Linux":
                    ffmpeg_download = requests.get(
                        "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.tar.xz",
                        stream=True)
                total_size = int(ffmpeg_download.headers.get('content-length', 0))
                if operating_system == "Windows":
                    with open(f"{os.getcwd()}/download/temp/ffmpeg.zip", 'wb') as download:
                        with tqdm(total=total_size, unit='B', unit_scale=True,
                                  desc="Downloading ffmpeg.zip") as progress_bar:
                            for data in ffmpeg_download.iter_content(chunk_size=1024):
                                download.write(data)
                                progress_bar.update(len(data))
                if operating_system == "Linux":
                    with open(f"{os.getcwd()}/download/temp/ffmpeg.tar.xz", 'wb') as download:
                        with tqdm(total=total_size, unit='B', unit_scale=True,
                                  desc="Downloading ffmpeg.tar.xz") as progress_bar:
                            for data in ffmpeg_download.iter_content(chunk_size=1024):
                                download.write(data)
                                progress_bar.update(len(data))

                # Unzip FFmpeg if Windows
                if operating_system == "Windows":
                    with zipfile.ZipFile(f"{os.getcwd()}/download/temp/ffmpeg.zip", "r") as ffmpeg_zip:
                        file_count = len(ffmpeg_zip.infolist())
                        with tqdm(total=file_count, unit='file', desc="Extracting ffmpeg.zip") as unzip_progress_bar:
                            for file in ffmpeg_zip.infolist():
                                ffmpeg_zip.extract(file, path=f"{os.getcwd()}/download/temp")
                                unzip_progress_bar.update(1)

                # Untar FFmpeg if Linux
                if operating_system == "Linux":
                    with tarfile.open(f"{os.getcwd()}/download/temp/ffmpeg.tar.xz", 'r:xz') as ffmpeg_tar_xz:
                        file_count = len(ffmpeg_tar_xz.getmembers())
                        with tqdm(total=file_count, unit='file', desc=f"Extracting ffmpeg.tar.xz") as untar_xz_progress_bar:
                            for file in ffmpeg_tar_xz:
                                ffmpeg_tar_xz.extract(file, path=f"{os.getcwd()}/download/temp")
                                untar_xz_progress_bar.update(1)

                # Copy ffmpeg binary to binaries if Windows
                if operating_system == "Windows":
                    shutil.copy2(f"{os.getcwd()}/download/temp/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe",
                                 f"{os.getcwd()}/binaries")

                # Copy ffmpeg binary to binaries if linux
                if operating_system == "Linux":
                    shutil.copy2(f"{os.getcwd()}/download/temp/ffmpeg-master-latest-linux64-gpl/bin/ffmpeg",
                                 f"{os.getcwd()}/binaries")
                    os.chmod(f"{os.getcwd()}/binaries/ffmpeg", stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

                # Remove the zip if Windows
                if operating_system == "Windows":
                    os.remove(f"{os.getcwd()}/download/temp/ffmpeg.zip")

                # Remove the .tar.xz and .tar if linux
                if operating_system == "Linux":
                    os.remove(f"{os.getcwd()}/download/temp/ffmpeg.tar.xz")

                # Remove the folder if windows
                if operating_system == "Windows":
                    shutil.rmtree(f"{os.getcwd()}/download/temp/ffmpeg-master-latest-win64-gpl")

                # Remove the folder if linux
                if operating_system == "Linux":
                    shutil.rmtree(f"{os.getcwd()}/download/temp/ffmpeg-master-latest-linux64-gpl")

                # Print a new line
                print()

            # MP4 Decrypt
            elif binary == "mp4decrypt.exe" or binary == "mp4decrypt":

                # Download mp4decrypt zip file
                if operating_system == "Windows":
                    mp4decrypt_download = requests.get(
                        "https://www.bok.net/Bento4/binaries/Bento4-SDK-1-6-0-639.x86_64-microsoft-win32.zip", stream=True)
                if operating_system == "Linux":
                    mp4decrypt_download = requests.get(
                        "https://www.bok.net/Bento4/binaries/Bento4-SDK-1-6-0-641.x86_64-unknown-linux.zip",
                        stream=True)
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

                # Copy mp4decrypt binary to binaries if windows
                if operating_system == "Windows":
                    shutil.copy2(
                        f"{os.getcwd()}/download/temp/Bento4-SDK-1-6-0-639.x86_64-microsoft-win32/bin/mp4decrypt.exe",
                        f"{os.getcwd()}/binaries")

                # Copy mp4decrypt binary to binaries if Linux
                if operating_system == "Linux":
                    shutil.copy2(
                        f"{os.getcwd()}/download/temp/Bento4-SDK-1-6-0-641.x86_64-unknown-linux/bin/mp4decrypt",
                        f"{os.getcwd()}/binaries")
                    os.chmod(f"{os.getcwd()}/binaries/mp4decrypt", stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

                # Deleting the zip file
                os.remove(f"{os.getcwd()}/download/temp/mp4decrypt.zip")

                # Deleting the directory if Windows
                if operating_system == "Windows":
                    shutil.rmtree(f"{os.getcwd()}/download/temp/Bento4-SDK-1-6-0-639.x86_64-microsoft-win32")

                # Deleting the directory if Linux
                if operating_system == "Linux":
                    shutil.rmtree(f"{os.getcwd()}/download/temp/Bento4-SDK-1-6-0-641.x86_64-unknown-linux")

                # Print a new line
                print()

            # n_m3u8dl-re
            elif binary == "n_m3u8dl-re.exe" or binary == "N_m3u8DL-RE":

                # Download n_m3u8dl-re zip file
                if operating_system == "Windows":
                    n_m3u8dl_re_download = requests.get(
                        "https://github.com/nilaoda/N_m3u8DL-RE/releases/download/v0.2.0-beta/N_m3u8DL-RE_Beta_win-x64_20230628.zip",
                        stream=True)
                if operating_system == "Linux":
                    n_m3u8dl_re_download = requests.get(
                        "https://github.com/nilaoda/N_m3u8DL-RE/releases/download/v0.2.0-beta/N_m3u8DL-RE_Beta_linux-x64_20230628.tar.gz",
                        stream=True)
                total_size = int(n_m3u8dl_re_download.headers.get('content-length', 0))
                if operating_system == "Windows":
                    with open(f"{os.getcwd()}/download/temp/n_m3u8dl-re.zip", 'wb') as download:
                        with tqdm(total=total_size, unit='B', unit_scale=True,
                                  desc="Downloading n_m3u8dl-re.zip") as progress_bar:
                            for data in n_m3u8dl_re_download.iter_content(chunk_size=1024):
                                download.write(data)
                                progress_bar.update(len(data))
                if operating_system == "Linux":
                    with open(f"{os.getcwd()}/download/temp/n_m3u8dl-re.tar.gz", 'wb') as download:
                        with tqdm(total=total_size, unit='B', unit_scale=True,
                                  desc="Downloading n_m3u8dl-re.tar.gz") as progress_bar:
                            for data in n_m3u8dl_re_download.iter_content(chunk_size=1024):
                                download.write(data)
                                progress_bar.update(len(data))

                # Unzip n_m3u8dl-re if Windows
                if operating_system == "Windows":
                    with zipfile.ZipFile(f"{os.getcwd()}/download/temp/n_m3u8dl-re.zip", "r") as nm3u8dl_re_zip:
                        file_count = len(nm3u8dl_re_zip.infolist())
                        with tqdm(total=file_count, unit='file', desc="Extracting n_m3u8dl-re.zip") as unzip_progress_bar:
                            for file in nm3u8dl_re_zip.infolist():
                                nm3u8dl_re_zip.extract(file, path=f"{os.getcwd()}/download/temp")
                                unzip_progress_bar.update(1)

                # Untar n_m3u8dl-re if Linux
                if operating_system == "Linux":
                    with tarfile.open(f"{os.getcwd()}/download/temp/n_m3u8dl-re.tar.gz", 'r:gz') as n_m3u8dl_re_tar_gz:
                        file_count = len(n_m3u8dl_re_tar_gz.getmembers())
                        with tqdm(total=file_count, unit='file',
                                  desc=f"Extracting n_m3u8dl-re.tar.gz") as untar_gz_progress_bar:
                            for file in n_m3u8dl_re_tar_gz:
                                n_m3u8dl_re_tar_gz.extract(file, path=f"{os.getcwd()}/download/temp")
                                untar_gz_progress_bar.update(1)

                # Copy n_m3u8dl-re binary to binaries if Windows
                if operating_system == "Windows":
                    shutil.copy2(f"{os.getcwd()}/download/temp/N_m3u8DL-RE_Beta_win-x64/N_m3u8DL-RE.exe",
                                 f"{os.getcwd()}/binaries")

                # Copy n_m3u8dl-re to binaries if Linux
                if operating_system == "Linux":
                    shutil.copy2(f"{os.getcwd()}/download/temp/N_m3u8DL-RE_Beta_linux-x64/N_m3u8DL-RE",
                                 f"{os.getcwd()}/binaries")
                    subprocess.run(['chmod', '+x', f"{os.getcwd()}/binaries/N_m3u8DL-RE"])

                # Delete zip file if Windows
                if operating_system == "Windows":
                    os.remove(f"{os.getcwd()}/download/temp/n_m3u8dl-re.zip")

                # Deleter .tar.gz and .tar file if Linux
                if operating_system == "Linux":
                    os.remove(f"{os.getcwd()}/download/temp/n_m3u8dl-re.tar.gz")

                # Delete directory if Windows
                if operating_system == "Windows":
                    shutil.rmtree(f"{os.getcwd()}/download/temp/N_m3u8DL-RE_Beta_win-x64")

                if operating_system == "Linux":
                    shutil.rmtree(f"{os.getcwd()}/download/temp/N_m3u8DL-RE_Beta_linux-x64")

                # Print a new line
                print()

            # YT-DLP
            elif binary == "yt-dlp.exe" or binary == "yt-dlp":

                # Download yt-dlp exe if windows
                if operating_system == "Windows":
                    yt_dlp_download = requests.get(
                        "https://github.com/yt-dlp/yt-dlp/releases/download/2023.11.16/yt-dlp_x86.exe",
                        stream=True)
                if operating_system == "Linux":
                    yt_dlp_download = requests.get(
                        "https://github.com/yt-dlp/yt-dlp/releases/download/2023.11.16/yt-dlp.tar.gz",
                        stream=True)
                total_size = int(yt_dlp_download.headers.get('content-length', 0))
                if operating_system == "Windows":
                    with open(f"{os.getcwd()}/download/yt-dlp.exe", 'wb') as download:
                        with tqdm(total=total_size, unit='B', unit_scale=True,
                                  desc="Downloading yt-dlp") as progress_bar:
                            for data in yt_dlp_download.iter_content(chunk_size=1024):
                                download.write(data)
                                progress_bar.update(len(data))
                if operating_system == "Linux":
                    with open(f"{os.getcwd()}/download/temp/yt-dlp.tar.gz", 'wb') as download:
                        with tqdm(total=total_size, unit='B', unit_scale=True,
                                  desc="Downloading yt-dlp") as progress_bar:
                            for data in yt_dlp_download.iter_content(chunk_size=1024):
                                download.write(data)
                                progress_bar.update(len(data))

                # Untar yt-dlp if Linux
                if operating_system == "Linux":
                    with tarfile.open(f"{os.getcwd()}/download/temp/yt-dlp.tar.gz", 'r:gz') as yt_dlp_tar_gz:
                        file_count = len(yt_dlp_tar_gz.getmembers())
                        with tqdm(total=file_count, unit='file',
                                  desc=f"Extracting yt-dlp.tar.gz") as untar_gz_progress_bar:
                            for file in yt_dlp_tar_gz:
                                yt_dlp_tar_gz.extract(file, path=f"{os.getcwd()}/download/temp")
                                untar_gz_progress_bar.update(1)

                # Copy yt-dlp binary to binaries if Windows
                if operating_system == "Windows":
                    shutil.copy2(f"{os.getcwd()}/download/yt-dlp.exe",
                                 f"{os.getcwd()}/binaries")

                # Copy yt-dlp binary to binaries if Linux
                if operating_system == "Linux":
                    shutil.copy2(f"{os.getcwd()}/download/temp/yt-dlp/yt-dlp",
                                 f"{os.getcwd()}/binaries")
                    subprocess.run(['chmod', '+x', f"{os.getcwd()}/binaries/yt-dlp"])

                # Remove binary from download folder if Windows
                if operating_system == "Windows":
                    os.remove(f"{os.getcwd()}/download/yt-dlp.exe")

                # Remove binary from download folder if Linux
                if operating_system == "Linux":
                    os.remove(f"{os.getcwd()}/download/temp/yt-dlp.tar.gz")
                    shutil.rmtree(f"{os.getcwd()}/download/temp/yt-dlp")

                # Print a new line
                print()
