import PySimpleGUI as sg

import assets.images
import Sites
import ast
import webbrowser


def clean_dict(dict: str = None):
    header_string = f"'''" \
                    f"{dict}" \
                    f"'''"
    cleaned_string = '\n'.join(line for line in header_string.split('\n') if not line.strip().startswith('#'))
    clean_dict = ast.literal_eval(cleaned_string)
    return clean_dict


def start_gui(wvd: str = None, api_key: str = None):

    sg.theme('Dark Black')  # Add theme

    # the layout
    left_frame_normal = sg.Col([
              [sg.Text('PSSH:'), sg.Text(key='-PSSH_TEXT-')],
              [sg.Input(key="-PSSH-")],
              [sg.VPush()],
              [sg.Text(text='License URL:'), sg.Text(key='-LIC_URL_TEXT-')],
              [sg.Input(key='-LIC_URL-')],
              [sg.VPush()],
              [sg.Text('Keys:')],
              [sg.Output(key='-OUTPUT-', expand_y=True, expand_x=True)],
              [sg.Button('Decrypt'), sg.Button('Reset')]
        ], expand_x=True, expand_y=True)

    right_frame = [
        [sg.Text('headers =', key='-HEADERS_TEXT-')],
        [sg.Multiline(key='-HEADERS-', expand_x=True, expand_y=True, tooltip=f"Paste headers dictionary starting with the first curly brace '{{' and ending with the last curly brace '}}'")],
        [sg.Text('json =', key='-JSON_TEXT-', visible=False)],
        [sg.Multiline(key='-JSON-', visible=False, expand_x=True, expand_y=True, tooltip=f"Paste json dictionary starting with the first curly brace '{{' and ending with the last curly brace '}}'")],
        [sg.Text('cookies =', key='-COOKIES_TEXT-', visible=False)],
        [sg.Multiline(key='-COOKIES-', visible=False, expand_x=True, expand_y=True, tooltip=f"Paste cookies dictionary starting with the first curly brace '{{' and ending with the last curly brace '}}'")],
        [sg.Text('releasePid:', key='-PID_TEXT-', visible=False)],
        [sg.Input(key='-PID-', visible=False, expand_x=True, expand_y=False)],
        [sg.Combo(values=['Generic', 'Crunchyroll', 'YouTube', 'RTE'], default_value='Generic', key='-OPTIONS-',
                  enable_events=True), sg.Push(), sg.Checkbox(text="Use CDM-Project API", key='-USE_API-')]
    ]

    if wvd is None:
        right_frame[6] = [sg.Combo(values=['Generic', 'Crunchyroll', 'YouTube', 'RTE'], default_value='Generic', key='-OPTIONS-',
                  enable_events=True), sg.Push(), sg.Checkbox(text="Use CDM-Project API", key='-USE_API-', default=True, disabled=True)]
    if api_key is None:
        right_frame[6] = [sg.Combo(values=['Generic', 'Crunchyroll', 'YouTube', 'RTE'], default_value='Generic', key='-OPTIONS-',
                     enable_events=True), sg.Push(), sg.Checkbox(text="Use CDM-Project API", key='-USE_API-', default=False, disabled=True)]

    right_frame_normal = sg.Col(right_frame, expand_x=True, expand_y=True)

    window_layout = [
        [sg.MenubarCustom([['About', ['Discord', 'CDM-Project', 'CDRM-Project', 'Source Code', 'Version']]],  k='-MENUBAR-')],
        [left_frame_normal, right_frame_normal]
    ]

    # the window
    window = sg.Window('TPD-Keys', layout=window_layout, resizable=True, size=(800, 800), icon=assets.images.taskbar)

    # the event loop
    while True:
        if wvd is None and api_key is None:
            sg.popup(title="TPD-Keys", custom_text="No CDM or API key found!")
            break

        event, values = window.read()

        # Action for window close event
        if event == sg.WIN_CLOSED:
            break

        # Action for Decrypt for Generic decrypt if fields are filled out
        if event == 'Decrypt':

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
                        if api_key is None:
                            window['-OUTPUT-'].update(f"No API key")
                        if api_key is not None:
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
                        if api_key is None:
                            window['-OUTPUT-'].update(f"No API key")
                        if api_key is not None:
                            try:
                                _, key_out = Sites.Generic.decrypt_generic_remotely(api_key=api_key,
                                                                                    in_pssh=values['-PSSH-'],
                                                                                    in_license_url=values['-LIC_URL-'],
                                                                                    license_curl_headers=ast.literal_eval(clean_dict(dict=values['-HEADERS-'])))
                                window['-OUTPUT-'].update(f"{key_out}")
                            except Exception as error:
                                window['-OUTPUT-'].update(f"{error}")

            # Error for no license URL - Generic
            if values['-PSSH-'] != '' and values['-LIC_URL-'] == '' and values['-OPTIONS-'] == 'Generic':
                window['-OUTPUT-'].update(f"No License URL provided")

            # Error for no PSSH - Generic
            if values['-LIC_URL-'] != '' and values['-PSSH-'] == '' and values['-OPTIONS-'] == 'Generic':
                window['-OUTPUT-'].update(f"No PSSH provided")

            # Error for no PSSH or License URL - Generic
            if values['-PSSH-'] == '' and values['-LIC_URL-'] == '' and values['-OPTIONS-'] == 'Generic':
                window['-OUTPUT-'].update(f"No PSSH or License URL provided")

            # Action for Decrypt for Crunchyroll decrypt if fields are filled out
            if values['-PSSH-'] != '' and values['-OPTIONS-'] == 'Crunchyroll' and values['-HEADERS-'] != '':
                if not values['-USE_API-']:
                    try:
                        _, key_out = Sites.Crunchyroll.decrypt_crunchyroll(wvd=wvd, in_pssh=values['-PSSH-'],
                                                                           license_curl_headers=ast.literal_eval(clean_dict(dict=values['-HEADERS-'])))
                        window['-OUTPUT-'].update(f"{key_out}")
                    except Exception as error:
                        window['-OUTPUT-'].update(f"{error}")
                if values['-USE_API-']:
                    if api_key is None:
                        window['-OUTPUT-'].update(f"No API key")
                    if api_key is not None:
                        try:
                            _, key_out = Sites.Crunchyroll.decrypt_crunchyroll_remotely(api_key=api_key, in_pssh=values['-PSSH-'],
                                                                           license_curl_headers=ast.literal_eval(clean_dict(dict=values['-HEADERS-'])))
                            window['-OUTPUT-'].update(f"{key_out}")
                        except Exception as error:
                            window['-OUTPUT-'].update(f"{error}")

            # Error for no Headers - Crunchyroll
            if values['-PSSH-'] != '' and values['-OPTIONS-'] == 'Crunchyroll' and values['-HEADERS-'] == '':
                window['-OUTPUT-'].update(f"No Headers provided")

            # Error for no PSSH - Crunchyroll
            if values['-PSSH-'] == '' and values['-OPTIONS-'] == 'Crunchyroll':
                window['-OUTPUT-'].update(f"No PSSH provided")

            # Action for Decrypt for YouTube decrypt if fields are filled out
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
                    if api_key is None:
                        window['-OUTPUT-'].update(f"No API key")
                    if api_key is not None:
                        try:
                            _, key_out = Sites.YouTube.decrypt_youtube_remotely(api_key=api_key, in_license_url=values['-LIC_URL-'],
                                                                       license_curl_headers=ast.literal_eval(clean_dict(dict=values['-HEADERS-'])),
                                                                       license_curl_json=ast.literal_eval(clean_dict(dict=values['-JSON-'])),
                                                                       license_curl_cookies=ast.literal_eval(clean_dict(dict=values['-COOKIES-'])))
                            window['-OUTPUT-'].update(f"{key_out}")
                        except Exception as error:
                            window['-OUTPUT-'].update(f"{error}")

            # Error for no Headers - YouTube
            if values['-LIC_URL-'] != '' and values['-OPTIONS-'] == 'YouTube' and values['-HEADERS-'] == '' and values['-JSON-'] != '' and values['-COOKIES-'] != '':
                window['-OUTPUT-'].update(f"No Headers provided")

            # Error for no JSON - YouTube
            if values['-LIC_URL-'] != '' and values['-OPTIONS-'] == 'YouTube' and values['-JSON-'] == '' and values['-HEADERS-'] != '' and values['-COOKIES-'] != '':
                window['-OUTPUT-'].update(f"No JSON provided")

            # Error for no Cookies - YouTube
            if values['-LIC_URL-'] != '' and values['-OPTIONS-'] == 'YouTube' and values['-COOKIES-'] == '' and values['-HEADERS-'] != '' and values['-JSON-'] != '':
                window['-OUTPUT-'].update(f"No Cookies provided")

            # Error if Headers, Cookies and JSON are empty - YouTube
            if values['-LIC_URL-'] != '' and values['-OPTIONS-'] == 'YouTube' and values['-HEADERS-'] == '' and values['-JSON-'] == '' and values['-COOKIES-'] == '':
                window['-OUTPUT-'].update(f"Not all dictionaries provided")

            # Error if no license URL - YouTube
            if values['-LIC_URL-'] == '' and values['-OPTIONS-'] == 'YouTube':
                window['-OUTPUT-'].update(f"No license URL provided")

            # Action for decrypt if RTE is selected
            if values['-PSSH-'] != '' and values['-LIC_URL-'] != '' and values['-PID-'] != '' and values['-OPTIONS-'] == 'RTE':
                if not values['-USE_API-']:
                    try:
                        _, key_out = Sites.RTE.decrypt_rte(wvd=wvd, in_pssh=values['-PSSH-'],
                                                            in_license_url=values['-LIC_URL-'], release_pid=values['-PID-'])
                        window['-OUTPUT-'].update(f"{key_out}")
                    except Exception as error:
                        window['-OUTPUT-'].update(f"{error}")
                if values['-USE_API-']:
                    try:
                        _, key_out = Sites.RTE.decrypt_rte_remotely(api_key=api_key, in_pssh=values['-PSSH-'],
                                                            in_license_url=values['-LIC_URL-'], release_pid=values['-PID-'])
                        window['-OUTPUT-'].update(f"{key_out}")
                    except Exception as error:
                        window['-OUTPUT-'].update(f"{error}")

            # Error if no values - RTE
            if values['-PSSH-'] == '' and values['-LIC_URL-'] == '' and values['-PID-'] == '' and values['-OPTIONS-'] == 'RTE':
                window['-OUTPUT-'].update(f"No fields provided!")

            # Error if no PSSH - RTE
            if values['-PSSH-'] == '' and values['-LIC_URL-'] != '' and values['-PID-'] != '' and values['-OPTIONS-'] == 'RTE':
                window['-OUTPUT-'].update(f"No PSSH provided")

            # Error if no License URL - RTE
            if values['-PSSH-'] != '' and values['-LIC_URL-'] == '' and values['-PID-'] != '' and values['-OPTIONS-'] == 'RTE':
                window['-OUTPUT-'].update(f"No license URL provided")

            # Error if no PID - RTE
            if values['-PSSH-'] != '' and values['-LIC_URL-'] != '' and values['-PID-'] == '' and values['-OPTIONS-'] == 'RTE':
                window['-OUTPUT-'].update(f"No PID provided")


        # Actions for reset button
        if event == 'Reset':
            window['-PSSH-'].update(value="", disabled=False)
            window['-LIC_URL-'].update(value="", disabled=False)
            window['-OUTPUT-'].update(value="", disabled=False)
            window['-HEADERS_TEXT-'].update(visible=True)
            window['-HEADERS-'].update(value="", visible=True)
            window['-OPTIONS-'].update(value="Generic", disabled=False)
            window['-JSON-'].update(visible=False)
            window['-JSON_TEXT-'].update(visible=False)
            window['-COOKIES-'].update(visible=False)
            window['-COOKIES_TEXT-'].update(visible=False)
            window['-PID_TEXT-'].update(visible=False)
            window['-PID-'].update(visible=False, value="")

        # Actions for Crunchyroll selector
        if event == '-OPTIONS-' and values['-OPTIONS-'] == 'Crunchyroll':
            window['-PSSH-'].update(value="", disabled=False)
            window['-LIC_URL-'].update(value="", disabled=True)
            window['-HEADERS_TEXT-'].update(visible=True)
            window['-HEADERS-'].update(value="", visible=True)
            window['-JSON-'].update(value="", visible=False)
            window['-JSON_TEXT-'].update(visible=False)
            window['-COOKIES-'].update(value="", visible=False)
            window['-COOKIES_TEXT-'].update(visible=False)
            window['-PID_TEXT-'].update(visible=False)
            window['-PID-'].update(visible=False, value="")

        # Actions for Generic selector
        if event == '-OPTIONS-' and values['-OPTIONS-'] == 'Generic':
            window['-PSSH-'].update(value="", disabled=False)
            window['-LIC_URL-'].update(value="", disabled=False)
            window['-HEADERS_TEXT-'].update(visible=True)
            window['-HEADERS-'].update(visible=True)
            window['-JSON-'].update(value="", visible=False)
            window['-JSON_TEXT-'].update(visible=False)
            window['-COOKIES-'].update(value="", visible=False)
            window['-COOKIES_TEXT-'].update(visible=False)
            window['-PID_TEXT-'].update(visible=False)
            window['-PID-'].update(visible=False, value="")

        # Actions for RTE selector
        if event == '-OPTIONS-' and values['-OPTIONS-'] == 'RTE':
            window['-PSSH-'].update(value="", disabled=False)
            window['-LIC_URL-'].update(value="", disabled=False)
            window['-HEADERS_TEXT-'].update(visible=False)
            window['-HEADERS-'].update(value="", visible=False)
            window['-JSON-'].update(value="", visible=False)
            window['-JSON_TEXT-'].update(visible=False)
            window['-COOKIES-'].update(value="", visible=False)
            window['-COOKIES_TEXT-'].update(visible=False)
            window['-PID_TEXT-'].update(visible=True)
            window['-PID-'].update(visible=True, value="")

        # Actions for YouTube selector
        if event == '-OPTIONS-' and values['-OPTIONS-'] == 'YouTube':
            window['-PSSH-'].update(value="", disabled=True)
            window['-LIC_URL-'].update(value="", disabled=False)
            window['-HEADERS_TEXT-'].update(visible=True)
            window['-HEADERS-'].update(value="", visible=True)
            window['-JSON-'].update(visible=True)
            window['-JSON_TEXT-'].update(visible=True)
            window['-COOKIES-'].update(visible=True)
            window['-COOKIES_TEXT-'].update(visible=True)
            window['-PID_TEXT-'].update(visible=False)
            window['-PID-'].update(visible=False, value="")

        # Actions for MenuBar
        if event == 'Discord':
            webbrowser.open(url='https://discord.gg/cdrm-project')
        if event == 'CDM-Project':
            webbrowser.open(url='https://cdm-project.com')
        if event == 'CDRM-Project':
            webbrowser.open(url='https://cdrm-project.com')
        if event == 'Source Code':
            webbrowser.open(url='https://cdm-project.com/Decryption-Tools/TPD-Keys')
        if event == 'Version':
            sg.popup('Version 1.3', custom_text='Close', grab_anywhere=True)

    # 4 - the close
    window.close()
