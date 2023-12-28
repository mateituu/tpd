import PySimpleGUI as sg
import Sites
import ast


def clean_dict(dict: str = None):
    header_string = f"'''" \
                    f"{dict}" \
                    f"'''"
    cleaned_string = '\n'.join(line for line in header_string.split('\n') if not line.strip().startswith('#'))
    clean_dict = ast.literal_eval(cleaned_string)
    return clean_dict


def start_gui(wvd: str = None, api_key: str = None):

    sg.theme('Dark Amber')    # Add theme

    # 1- the layout
    left_frame_normal = sg.Col([
              [sg.Text('PSSH:'), sg.Text(size=(15, 1), key='-PSSH_TEXT-')],
              [sg.Input(key="-PSSH-")],
              [sg.Text(text='License URL:'), sg.Text(size=(15, 1), key='-LIC_URL_TEXT-')],
              [sg.Input(key='-LIC_URL-')],
              [sg.Text('Keys:')],
              [sg.Output(size=(45, 6), key='-OUTPUT-')],
              [sg.Button('Decrypt'), sg.Button('Reset')]
        ], p=0)

    right_frame_normal = sg.Col([
        [sg.Text('Headers:')],
        [sg.Multiline(key='-HEADERS-', size=(50, 10))],
        [sg.Text('JSON:', key='-JSON_TEXT-', visible=False)],
        [sg.Multiline(key='-JSON-', size=(50, 10), visible=False)],
        [sg.Text('Cookies:', key='-COOKIES_TEXT-', visible=False)],
        [sg.Multiline(key='-COOKIES-', size=(50, 10), visible=False)],
        [sg.Combo(values=['Generic', 'Crunchyroll', 'YouTube'], default_value='Generic', key='-OPTIONS-', enable_events=True),sg.Push(), sg.Checkbox(text="Use CDM-Project API", key='-USE_API-')]
    ], p=0)

    window_layout = [
        [left_frame_normal, right_frame_normal]
    ]

    # 2 - the window
    window = sg.Window('TPD-Keys', layout=window_layout)

    # 3 - the event loop
    while True:

        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == 'Decrypt':

            if values['-PSSH-'] != '' and values['-LIC_URL-'] == '' and values['-OPTIONS-'] == 'Generic':
                window['-OUTPUT-'].update(f"No License URL provided")

            if values['-LIC_URL-'] != '' and values['-PSSH-'] == '' and values['-OPTIONS-'] == 'Generic':
                window['-OUTPUT-'].update(f"No PSSH provided")

            if values['-PSSH-'] == '' and values['-LIC_URL-'] == '' and values['-OPTIONS-'] == 'Generic':
                window['-OUTPUT-'].update(f"No PSSH or License URL provided")

            if values['-PSSH-'] != '' and values['-LIC_URL-'] != '' and values['-OPTIONS-'] == 'Generic':
                if values['-HEADERS-'] == '':
                    if not values['-USE_API-']:
                        try:
                            _, key_out = Sites.Generic.decrypt_generic(wvd=wvd, in_pssh=values['-PSSH-'],
                                                               in_license_url=values['-LIC_URL-'])
                            window['-OUTPUT-'].update(f"{key_out}")
                        except Exception as error:
                            window['-OUTPUT-'].update(f"{error}")
                    if values['-USE_API-']:
                        try:
                            _, key_out = Sites.Generic.decrypt_generic_remotely(api_key=api_key, in_pssh=values['-PSSH-'],
                                                              in_license_url=values['-LIC_URL-'])
                            window['-OUTPUT-'].update(f"{key_out}")
                        except Exception as error:
                            window['-OUTPUT-'].update(f"{error}")

                if values['-HEADERS-'] != '':
                    if not values['-USE_API-']:
                        try:
                            _, key_out = Sites.Generic.decrypt_generic(wvd=wvd, in_pssh=values['-PSSH-'],
                                                                       in_license_url=values['-LIC_URL-'],
                                                                       license_curl_headers=ast.literal_eval(clean_dict(dict=values['-HEADERS-'])))
                            window['-OUTPUT-'].update(f"{key_out}")
                        except Exception as error:
                            window['-OUTPUT-'].update(f"{error}")
                    if values['-USE_API-']:
                        try:
                            _, key_out = Sites.Generic.decrypt_generic_remotely(api_key=api_key,
                                                                                in_pssh=values['-PSSH-'],
                                                                                in_license_url=values['-LIC_URL-'],
                                                                                license_curl_headers=ast.literal_eval(clean_dict(dict=values['-HEADERS-'])))
                            window['-OUTPUT-'].update(f"{key_out}")
                        except Exception as error:
                            window['-OUTPUT-'].update(f"{error}")

            if values['-PSSH-'] != '' and values['-OPTIONS-'] == 'Crunchyroll' and values['-HEADERS-'] != '':
                if not values['-USE_API-']:
                    try:
                        _, key_out = Sites.Crunchyroll.decrypt_crunchyroll(wvd=wvd, in_pssh=values['-PSSH-'],
                                                                           license_curl_headers=ast.literal_eval(clean_dict(dict=values['-HEADERS-'])))
                        window['-OUTPUT-'].update(f"{key_out}")
                    except Exception as error:
                        window['-OUTPUT-'].update(f"{error}")
                if values['-USE_API-']:
                    try:
                        _, key_out = Sites.Crunchyroll.decrypt_crunchyroll_remotely(api_key=api_key, in_pssh=values['-PSSH-'],
                                                                           license_curl_headers=ast.literal_eval(clean_dict(dict=values['-HEADERS-'])))
                        window['-OUTPUT-'].update(f"{key_out}")
                    except Exception as error:
                        window['-OUTPUT-'].update(f"{error}")

            if values['-PSSH-'] != '' and values['-OPTIONS-'] == 'Crunchyroll' and values['-HEADERS-'] == '':
                window['-OUTPUT-'].update(f"No Headers provided")

            if values['-PSSH-'] == '' and values['-OPTIONS-'] == 'Crunchyroll':
                window['-OUTPUT-'].update(f"No PSSH provided")

            if values['-LIC_URL-'] != '' and values['-OPTIONS-'] == 'YouTube' and values['-HEADERS-'] != '' and values['-JSON-'] != '' and values['-COOKIES-'] != '':
                if not values['-USE_API-']:
                    try:
                        _, key_out = Sites.YouTube.decrypt_youtube(wvd=wvd, in_license_url=values['-LIC_URL-'],
                                                                   license_curl_headers=ast.literal_eval(clean_dict(dict=values['-HEADERS-'])),
                                                                   license_curl_json=ast.literal_eval(clean_dict(dict=values['-JSON-'])),
                                                                   license_curl_cookies=ast.literal_eval(clean_dict(dict=values['-COOKIES-'])))
                        window['-OUTPUT-'].update(f"{key_out}")
                    except Exception as error:
                        window['-OUTPUT-'].update(f"{error}")
                if values['-USE_API-']:
                    try:
                        _, key_out = Sites.YouTube.decrypt_youtube_remotely(api_key=api_key, in_license_url=values['-LIC_URL-'],
                                                                   license_curl_headers=ast.literal_eval(clean_dict(dict=values['-HEADERS-'])),
                                                                   license_curl_json=ast.literal_eval(clean_dict(dict=values['-JSON-'])),
                                                                   license_curl_cookies=ast.literal_eval(clean_dict(dict=values['-COOKIES-'])))
                        window['-OUTPUT-'].update(f"{key_out}")
                    except Exception as error:
                        window['-OUTPUT-'].update(f"{error}")

            if values['-LIC_URL-'] != '' and values['-OPTIONS-'] == 'YouTube' and values['-HEADERS-'] == '' and values['-JSON-'] != '' and values['-COOKIES-'] != '':
                window['-OUTPUT-'].update(f"No Headers provided")

            if values['-LIC_URL-'] != '' and values['-OPTIONS-'] == 'YouTube' and values['-JSON-'] == '' and values['-HEADERS-'] != '' and values['-COOKIES-'] != '':
                window['-OUTPUT-'].update(f"No JSON provided")

            if values['-LIC_URL-'] != '' and values['-OPTIONS-'] == 'YouTube' and values['-COOKIES-'] == '' and values['-HEADERS-'] != '' and values['-JSON-'] != '':
                window['-OUTPUT-'].update(f"No Cookies provided")

            if values['-LIC_URL-'] != '' and values['-OPTIONS-'] == 'YouTube' and values['-HEADERS-'] == '' and values['-JSON-'] == '' and values['-COOKIES-'] == '':
                window['-OUTPUT-'].update(f"All fields empty!")

            if values['-LIC_URL-'] == '' and values['-OPTIONS-'] == 'YouTube':
                window['-OUTPUT-'].update(f"No license URL provided")


        if event == 'Reset':
            window['-PSSH-'].update(value="", disabled=False)
            window['-LIC_URL-'].update(value="", disabled=False)
            window['-OUTPUT-'].update(value="", disabled=False)
            window['-HEADERS-'].update(value="", disabled=False)
            window['-OPTIONS-'].update(value="Generic", disabled=False)

        if event == '-OPTIONS-' and values['-OPTIONS-'] == 'Crunchyroll':
            window['-PSSH-'].update(value="", disabled=False)
            window['-LIC_URL-'].update(value="", disabled=True)
            window['-JSON-'].update(visible=False)
            window['-JSON_TEXT-'].update(visible=False)
            window['-COOKIES-'].update(visible=False)
            window['-COOKIES_TEXT-'].update(visible=False)

        if event == '-OPTIONS-' and values['-OPTIONS-'] == 'Generic':
            window['-PSSH-'].update(value="", disabled=False)
            window['-LIC_URL-'].update(value="", disabled=False)
            window['-JSON-'].update(visible=False)
            window['-JSON_TEXT-'].update(visible=False)
            window['-COOKIES-'].update(visible=False)
            window['-COOKIES_TEXT-'].update(visible=False)

        if event == '-OPTIONS-' and values['-OPTIONS-'] == 'YouTube':
            window['-PSSH-'].update(value="", disabled=True)
            window['-LIC_URL-'].update(value="", disabled=False)
            window['-JSON-'].update(visible=True)
            window['-JSON_TEXT-'].update(visible=True)
            window['-COOKIES-'].update(visible=True)
            window['-COOKIES_TEXT-'].update(visible=True)




    # 4 - the close
    window.close()
