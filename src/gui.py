import PySimpleGUI as sg
import threading

from catalog import Catalog
from callsignTracker import guiRunner

def search(query, method):
    catalog = Catalog()
    catalog.load_catalog()
    print(catalog.catalog)

def main():
    thread = None
    console_enabled = False
    stop_event = threading.Event()

    layout = [
        [sg.Text("Created by OspreyEyes")],
        [sg.Text("Run Callsign Tracker"), sg.Button("OPEN", key="-CONSOLE-")],
        [sg.Text("Search by:"), sg.Combo(["Account ID", "Callsign"], key="-SEARCHTYPE-")],
        [sg.Text("Search your catalog:"), sg.Input(key="-SEARCH-"), sg.Button("Search", bind_return_key=True)],
        [sg.Listbox(values=[], size=(50, 10), key="-RESULTS-")],
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
            print(query, method)
            results = search(query, method)
        if event == "-CONSOLE-":
            if console_enabled:
                print("Closing tracker...")
                console_enabled = False
                stop_event.set()
                thread.join()
            else:
                print("Launching tracker...")
                console_enabled = True
                stop_event.clear()
                thread = threading.Thread(target=guiRunner, args=(stop_event,))
                thread.start()
    window.close()

if __name__ in "__main__":
    main()