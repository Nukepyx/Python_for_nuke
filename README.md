
# **Shuffle Shift: Nuke Channel Selector for Shuffle Nodes**

A Python script leveraging PySide2 to simplify channel selection for `Shuffle` and `Shuffle2` nodes in Nuke. This tool enhances workflow efficiency by providing an intuitive GUI for channel selection.

---

## **Features**

- **Dynamic Channel Retrieval**: Automatically lists all available channels in the selected node.
- **Prioritized Sorting**: Channels like `rgb`, `rgba`, and `alpha` appear first, followed by others alphabetically.
- **Interactive GUI**: Buttons for each channel and a "Cancel" option for easy navigation.
- **Supports Multiple Node Types**: Compatible with both `Shuffle` and `Shuffle2` nodes.

---

## **Installation**

### **Step 1: Clone or Download the Repository**
Clone or download this repository:
```bash
git clone https://github.com/your-username/shuffle_shift.git
```

### **Step 2: Copy Script to the Nuke Directory**
1. Move the script (`shuffle_shift.py`) to your `.nuke/python` directory:
   - **Windows**: `C:\Users\<YourUsername>\.nuke\python`
   - **Linux**: `/home/<YourUsername>/.nuke/python`

2. If the `python` folder doesn’t exist, create it manually.

---

### **Step 3: Update `menu.py`**

To install the script into Nuke's menu with your preferred setup:

1. Open (or create) your `menu.py` file in the `.nuke` directory:
   - **Windows**: `C:\Users\<YourUsername>\.nuke\menu.py`
   - **Linux**: `/home/<YourUsername>/.nuke/menu.py`

2. Add the following code to include the tool in Nuke's menu:

```python
import nuke
import shuffle_shift

# Create a custom menu in Nuke
menubar = nuke.menu("Nuke")
v_commands = menubar.addMenu("V_commands")

# Add the Shuffle Shift command to the menu
v_commands.addCommand("Shuffle Shift", lambda: shuffle_shift.select_channel_for_shuffle(), "Alt+`")
```

3. Save the file and restart Nuke.

---

## **Usage**

1. **Select a Node**:
   - Select a `Shuffle` or `Shuffle2` node in Nuke's Node Graph.

2. **Launch the Tool**:
   - Access **Shuffle Shift** from the **"V_commands"** menu in Nuke's toolbar.
   - Or use the shortcut "Alt+`".

3. **Choose a Channel**:
   - A dialog with buttons for each channel appears.
   - Click a button to assign the channel to the node.

4. **Cancel Operation**:
   - Click "Cancel" to close the dialog without making changes.

---

## **Requirements**

- **Nuke**: Version 11 and above.
- **Python**: Version 2.7+ or 3.7+ (depends on your Nuke version).
- **PySide2**: Install using:
  ```bash
  pip install PySide2
  ```

---

## **How It Works**

### **Key Components**
- **Channel Retrieval**:
  The `get_channels()` method extracts all unique base layer names from the node's channels.

- **Custom Sorting**:
  Channels are sorted with `rgb`, `rgba`, and `alpha` prioritized, followed by others alphabetically.

- **Interactive GUI**:
  The `ChannelButtonPanel` class creates a dialog with buttons for each channel.

---

## **Preview**

![Channel Selector Screenshot](assets/screenshots/shuffle_shift_snip.png)


---

## **Future Enhancements**

- Add search functionality for large channel lists.
- Extend support for additional node types.
- Allow customization of priority channels.

---

## **Contributing**

Contributions are welcome! Follow these steps:

1. Fork this repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

Thanks!



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

```python
nuke.pluginAddPath('./python')
```

### 3. Create a New Menu Item in `menu.py`

3. In the `.nuke` directory, open or create the `menu.py` file. You'll create a new menu called `V_commands` and assign a shortcut key (`Alt+T`) to run the script. Add the following lines to `menu.py`:

```python
import nuke
import your_script_name  # Replace with your actual script name without the .py extension e.g. Tag_input.py

# Create a custom menu in Nuke
menubar = nuke.menu("Nuke")
v_commands = menubar.addMenu("V_commands")

# Add the command to the new menu and assign a shortcut
v_commands.addCommand("Tag Input Node", lambda: your_script_name.create_tag_input_node(), "Alt+T")
```

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


# V_backdrop_inator

**V_backdrop_inator** is a Nuke Python script that provides an interactive UI with buttons and a color picker for creating and managing backdrops efficiently.

## Features
- Creates backdrops with customizable colors.
- Uses Qt widgets for an intuitive UI.
- Provides quick interaction through buttons.

## Installation
### Windows
1. Locate your `.nuke` directory, usually found at:
   - `C:\Users\YourUsername\.nuke`
2. Copy `V_backdrop_inator.py` into the `.nuke/python` folder (create the folder if it doesn’t exist).
3. Update `init.py` (or create it if missing) inside `.nuke` with:

   ```python
   import os
   import nuke
   nuke.pluginAddPath(os.path.expanduser("~/.nuke/python"))
   ```
4. Modify `menu.py` in the `.nuke` folder:

   ```python
   import nuke
   import V_backdrop_inator
   
   menubar = nuke.menu('Nuke')
   v_commands = menubar.addMenu('V_commands')
   v_commands.addCommand('Create Backdrop', 'V_backdrop_inator.launch_backdrop_creator()', 'ctrl+alt+B')
   ```

### macOS & Linux
1. Open Terminal and navigate to your home directory:
   ```sh
   cd ~/.nuke
   ```
2. Create a `python` folder if it doesn’t exist:
   ```sh
   mkdir -p ~/.nuke/python
   ```
3. Move `V_backdrop_inator.py` into this folder.
4. Add the following to `~/.nuke/init.py`:
   ```python
   import os
   import nuke
   nuke.pluginAddPath(os.path.expanduser("~/.nuke/python"))
   ```
5. Modify `~/.nuke/menu.py`:
   ```python
   import nuke
   import V_backdrop_inator
   
   menubar = nuke.menu('Nuke')
   v_commands = menubar.addMenu('V_commands')
   v_commands.addCommand('Create Backdrop', 'V_backdrop_inator.launch_backdrop_creator()', 'ctrl+alt+B')
   ```

## Usage
- Open Nuke.
- Press `ctrl+alt+B` or use the `V_commands` menu to launch **V_backdrop_inator**.
- Interact with the UI to create and modify backdrops effortlessly.

## Screenshot
![V_backdrop_inator UI](assets/screenshots/Backdrop_inator_snip.png)

## Author
Developed by **Vikas Kaushal**.

## License
This project is licensed under the MIT License.

## Contributions
Feel free to submit issues or feature requests to improve this tool!

