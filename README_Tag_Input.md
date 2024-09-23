
# Nuke Auto-Tag Input Node Script

This Python script for **Nuke** automates the creation of a custom `Tag_Input` node, which tags and connects to a parent node by dynamically fetching and displaying its name.
The script is designed to help compositors manage node connections more efficiently by providing quick access to node names and connections.

## Features

- **Auto-Generated Unique Names**: Every `Tag_Input` node created by this script is named dynamically (e.g., `Tag_input1`, `Tag_input2`, etc.), ensuring unique names each time the script is run.
- **Fetch Node Name**: A button (`Get Name`) allows users to fetch and display the name of the currently selected node.
- **Connect to Parent Node**: A `Connect` button is provided to automatically connect the newly created `Tag_input` node to the selected parent node.
- **Jump to Input Node**: A `Jump to Input` button allows users to zoom in on the connected parent node in the Node Graph for quick navigation.

## How to Install

To install the script and set it up with a custom menu and keyboard shortcut, follow these steps:

### 1. Place the Script in the `.nuke/python` Folder

1. Copy the Python script file into your `.nuke/python` folder. This is where Nuke will look for Python scripts.

### 2. Modify `init.py`

2. Open or create the `init.py` file in your `.nuke` directory. Add the path to your Python folder where the script is stored:


nuke.pluginAddPath('./python')


### 3. Create a New Menu Item in `menu.py`

3. In the `.nuke` directory, open or create the `menu.py` file. You'll create a new menu called `V_commands` and assign a shortcut key (`Alt+T`) to run the script. Add the following lines to `menu.py`:


import nuke
import your_script_name  # Replace with your actual script name without the .py extension

# Create a custom menu in Nuke
menubar = nuke.menu("Nuke")
v_commands = menubar.addMenu("V_commands")

# Add the command to the new menu and assign a shortcut
v_commands.addCommand("Tag Input Node", lambda: your_script_name.create_tag_input_node(), "Alt+T")


### 4. Usage

You can now use the script either by:

- **Menu**: Go to `V_commands -> Tag Input Node`.
- **Shortcut**: Press `Alt+T` to quickly run the script.

### 5. Restart Nuke

After these changes, restart Nuke for the script and menu item to appear.

## How to Use

1. **Run the Script**: Either use the menu option (`V_commands -> Tag Input Node`) or press the keyboard shortcut (`Alt+T`).
   
2. **Select a Node**: Once the `Tag_input` node is created, select any parent node in your Node Graph.

3. **Fetch Node Name**:
   - Click the `Get Name` button to fetch and display the selected node's name in the newly created `NoOp` node.

4. **Connect to Parent Node**:
   - Click the `Connect` button to automatically connect the `Tag_input` node to the parent node (the one whose name you fetched).

5. **Jump to Input**:
   - Use `Jump to Input` to zoom into the connected parent node in your Node Graph for easy navigation.

## Error Handling

- If no node is selected when you click `Get Name`, a message will prompt you to select a node.
- If an invalid or non-existing node name is provided, a message will indicate that the node was not found.

## Example

1. Create a `Tag_input` node using the script.
2. Select a node in the Node Graph, and click `Get Name` to assign its name to the `NoOp` node.
3. Click `Connect` to automatically connect the `Tag_input` to the selected node.
4. Use `Jump to Input` to zoom in on the connected parent node.

## Contributing

Contributions are welcome! If you'd like to improve the script or add new features, feel free to fork the repository and submit a pull request.


## Contact

For any questions or issues, feel free to reach out via GitHub issues or submit a pull request for improvements.
