import nuke
from PySide2 import QtWidgets
from functools import partial
class ChannelButtonPanel(QtWidgets.QDialog):
   def _init_(self, node, parent=None):
       super(ChannelButtonPanel, self)._init_(parent)
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
       # Try to retrieve channels in the same order as Nuke's Viewer
       metadata_channels = self.node.metadata("input/metadata/channel")
       # If metadata is available, extract unique layers in the correct order
       if metadata_channels:
           unique_layers = list(dict.fromkeys([ch.split('.')[0] for ch in metadata_channels]))
       else:
           # Fallback to using node.channels() if metadata isn't available, without sorting
           layers = self.node.channels()
           unique_layers = list(dict.fromkeys([ch.split('.')[0] for ch in layers]))
       
       return unique_layers
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
   panel = ChannelButtonPanel(node)
   if panel.exec_():  # This will return True if accept() is called
       pass
   else:
       nuke.message("No channel selected.")
# Execute the function
#select_channel_for_shuffle()