import PySimpleGUI as sg

data = [
    {"name": "John Doe", "age": 32, "occupation": "engineer"},
    {"name": "Jane Smith", "age": 45, "occupation": "doctor"},
    {"name": "Bob Johnson", "age": 28, "occupation": "teacher"}
]

# Define the layout of the window
layout = [
    [sg.Text("Enter a search term:"), sg.Input(key="-SEARCH-"), sg.Button("Search")],
    [sg.Listbox(values=[], size=(50, 10), key="-RESULTS-")]
]

# Create the window
window = sg.Window("Search", layout)

while True:
    # Read events and values from the window
    event, values = window.read()
    
    if event == sg.WIN_CLOSED:
        # Exit the program if the user closes the window
        break
    
    if event == "Search":
        # Filter the data based on the search term
        search_term = values["-SEARCH-"].lower()
        results = [item for item in data
                   if any(search_term in str(value).lower() for value in item.values())]
        
        # Update the results listbox with the search results
        window["-RESULTS-"].update(values=results)

# Close the window
window.close()