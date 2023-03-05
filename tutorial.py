from pathlib import Path

import pandas as pd
import PySimpleGUI as sg


def display_ec

def convert_to_csv(excel_file_path, output_folder, sheet_name, seperator, decimal):
    df = pd.read_excel(excel_file_path, sheet_name)
    filename = Path(excel_file_path).stem
    outputfile = Path(output_folder) / f"{filename}.csv"
    df.to_csv(outputfile, sep=seperator, decimal=decimal, index=False)
    sg.popup_no_titlebar("Done! :)")



layout = [
    [sg.Text("Input File:"), sg.Input(key="-IN-"), sg.FileBrowse(file_types=(("Excel Files", "*.xls"),))],
    [sg.Text("Output Folder:"), sg.Input(key="-OUT-"), sg.FileBrowse()],
    [sg.Exit(), sg.Button("Display Excel File"), sg.Button("Convert To CSV")],
]

window = sg.Window("Excel to CSV Converter", layout)

while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, "Exit"):
        break
    if event == "Display Excel File":
        pass
    if event == "Convert To CSV":
        convert_to_csv(
            excel_file_path=values["-IN-"],
            output_folder=values["-OUT-"],
            sheet_name="Sheet1",
            seperator="|",
            decimal=".",
        )

window.close()