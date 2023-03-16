from json import load
import PySimpleGUI as sg
import threading

from fuzzywuzzy import fuzz
import textwrap

from callsigns import parseCallsigns, loadCallsignFile
from callsignTracker import guiRunner

def search(query, method):
    threshold = 50
    results = []
    error, callsignData = loadCallsignFile()
    if error:
        return error, None
    for entry in callsignData:
        if method == "Account ID":
            ratio = fuzz.token_set_ratio(query, entry["acid"])
            if ratio >= threshold:
                results.append(f"Account ID: {entry['acid']} | Current Callsign: {entry['cur_callsign']} | History: {entry['callsigns']}")
        elif method == "Callsign":
            cur_callsigns = list(entry["callsigns"].keys())
            candidate = False
            for callsign in cur_callsigns:
               ratio = fuzz.token_set_ratio(query, callsign)
               if ratio >= threshold:
                   candidate = True
            if candidate:
                lines = textwrap.fill(f"Account ID: {entry['acid']} | Current Callsign: {entry['cur_callsign']} | History: {entry['callsigns']}", 200).split("\n")
                for item in lines:
                    results.append(item)

    return None, results
def main():
    thread = None
    console_enabled = False
    stop_event = threading.Event()

    layout = [
        [sg.Text("Created by OspreyEyes")],
        [sg.Text("Run Callsign Tracker"), sg.Button("OPEN", key="-CONSOLE-")],
        [sg.Text("Search by:"), sg.Combo(["Account ID", "Callsign"], key="-SEARCHTYPE-", default_value="Callsign")],
        [sg.Text("Search your catalog:"), sg.Input(key="-SEARCH-"), sg.Button("Search", bind_return_key=True)],
        [sg.Listbox(values=[], size=(200, 10), key="-RESULTS-")],
        [sg.Exit()],
    ]
    window = sg.Window(title="Callsign Tracker GUI", layout=layout)
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Exit"):
            break
        if event == "Search":
            method = values["-SEARCHTYPE-"]
            query = values["-SEARCH-"].lower()
            error, results = search(query, method)

            if error == 1:
                sg.popup_error("There is not a callsigns.jsonl file in the same program's directory. Please generate one with the Callsign Tracker.")
            elif values["-SEARCHTYPE-"] not in ("Account ID", "Callsign"):
                sg.popup_error("Invalid search method. Please select an option from the dropdown menu.") 
            elif values["-SEARCH-"] == "":
                sg.popup_error("You have not entered a search term.")
            window['-RESULTS-'].update(values=results)

        if event == "-CONSOLE-":
            if console_enabled:
                print("Closing tracker...")
                console_enabled = False
                stop_event.set()
                thread.join()
                window['-CONSOLE-'].update("OPEN")
            else:
                print("Launching tracker...")
                console_enabled = True
                stop_event.clear()
                thread = threading.Thread(target=guiRunner, args=(stop_event,))
                thread.start()
                window['-CONSOLE-'].update("CLOSE")
    window.close()

if __name__ in "__main__":
    main()