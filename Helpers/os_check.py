import os
from sys import exit


def get_os_specific():
    if os.name == 'nt':  # 'nt' stands for Windows
        return "Windows"
    elif os.name == 'posix':  # 'posix' stands for Linux/Unix
        return "Linux"
    else:
        return "Unknown"