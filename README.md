# TPD-Keys
#### Created by @TPD94

## Based on [pywidevine](https://cdm-project.com/Decryption-Tools/pywidevine "pywidevine")

How to use:
1. Create `TPD-Keys` folder.

2. Download and extract `TPD-Keys.py`, `requirements.txt` and `License_curl.py` into the newly created `TPD-Keys` directory

3. Install the requirements with `pip install -r requirements.txt`

4. Crete a WVD with pywidevine; `pywidevine create-device -k "/PATH/TO/device_private_key" -c "/PATH/TO/device_client_id_blob" -t "ANDROID" -l 3`

5. Place your .wvd in `/WVDs` directory, if you do not have this directory, create it or run the program with `python TPD-Keys.py` and it will be created for you

6. Place your API key (if wanted) in `/Config/api-key.txt` if you do not have this file or directory, create it or run the program with `python TPD-Keys.py` and it will be created for you. If you don't have an API key, you can request one via [discord](https://discord.gg/cdrm-project "CDRM-Project")

7. Paste dictionaries from license request curl post request into `License_curl.py`

8. Run with `python tpd-keys.py` for just decryption keys or `python tpd-keys.py --web-dl` to get decryption keys plus download the content 

To view additional options you can use `python tpd-keys.py -h`