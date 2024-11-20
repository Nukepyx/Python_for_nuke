import nuke
from PySide2 import QtWidgets
from functools import partial

class ChannelButtonPanel(QtWidgets.QDialog):
    def __init__(self, node, parent=None):  # Fixed method name
        super(ChannelButtonPanel, self).__init__(parent)  # Fixed method name
        self.setWindowTitle("Select Channel")
        self.node = node

        # Layout setup
        self.layout = QtWidgets.QVBoxLayout()

        # Get channels and create buttons
        channels = self.get_channels()
        self.buttons = []
        for channel in channels:
            button = QtWidgets.QPushButton(channel)
            button.clicked.connect(partial(self.select_channel, channel))
            self.layout.addWidget(button)
            self.buttons.append(button)

        # Add a cancel button
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        self.layout.addWidget(self.cancel_button)

        self.setLayout(self.layout)
        self.setMinimumSize(250, 400)

    def get_channels(self):
        # Retrieve all channels from the node
        channels = self.node.channels()

        # Extract unique base layer names without individual channels (e.g., only "rgb", "alpha")
        unique_layers = list(dict.fromkeys([ch.split('.')[0] for ch in channels]))

        # Custom sort: prioritize 'rgb' and 'alpha', then sort remaining layers alphabetically
        priority_layers = ["rgb", "rgba", "alpha"]
        sorted_layers = sorted(unique_layers, key=lambda x: (x not in priority_layers, x))
        return sorted_layers

    def select_channel(self, channel):
        # Set the selected channel based on the node type
        if self.node.Class() == "Shuffle":
            self.node['in'].setValue(channel)
        elif self.node.Class() == "Shuffle2":
            self.node['in1'].setValue(channel)
        self.accept()

def select_channel_for_shuffle():
    # Ensure a Shuffle or Shuffle2 node is selected
    try:
        node = nuke.selectedNode()
        if node.Class() not in ["Shuffle", "Shuffle2"]:
            nuke.message("Please select a Shuffle or Shuffle2 node.")
            return
    except ValueError:
        nuke.message("Please select a Shuffle or Shuffle2 node.")
        return

    panel = ChannelButtonPanel(node)  # Create the dialog with the selected node
    if panel.exec_():  # Show the dialog and wait for a result
        pass
    else:
        nuke.message("No channel selected.")
#Enable below code to test
#select_channel_for_shuffle()
