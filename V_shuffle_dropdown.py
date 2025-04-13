import nuke
from PySide2 import QtWidgets, QtCore

def get_available_channel_layers(node):
    """Get unique channel layers from the node's input."""
    if not node.input(0):
        return []
    channels = nuke.channels(node.input(0))
    layers = sorted(list(set([ch.split('.')[0] for ch in channels if '.' in ch])))
    return layers

def is_new_shuffle(node):
    """Check if the node is a new-style Shuffle (Nuke 13+)."""
    return 'in1' in node.knobs()

def create_shuffle_ui():
    """Build a UI to select channel layers for old or new Shuffle nodes."""
    # Check if a Shuffle node is selected
    try:
        shuffle_node = nuke.selectedNode()
        if shuffle_node.Class() not in ["Shuffle", "Shuffle2"]:
            nuke.message("Please select a Shuffle node!")
            return
    except ValueError:
        nuke.message("Please select a Shuffle node!")
        return

    # Get available channel layers from input
    layers = get_available_channel_layers(shuffle_node)
    if not layers:
        nuke.message("No input connected to the Shuffle node or no channels found!")
        return

    # Determine if it's a new or old Shuffle node
    is_new = is_new_shuffle(shuffle_node)
    current_in = shuffle_node['in1' if is_new else 'in'].value()
    current_out = shuffle_node['out1' if is_new else 'out'].value()

    # Create a Qt dialog
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    dialog = QtWidgets.QDialog()
    dialog.setWindowTitle("Shuffle Channel Selector")
    dialog.setFixedWidth(300)

    # Main layout with padding
    layout = QtWidgets.QVBoxLayout()
    layout.setContentsMargins(10, 10, 10, 10)
    layout.setSpacing(15)

    # Style sheet
    dialog.setStyleSheet("""
        QLabel { font-size: 12px; font-weight: bold; color: #999; }
        QComboBox, QLineEdit { padding: 5px; border: 1px solid #ccc; border-radius: 3px; }
        QPushButton { padding: 5px; background-color: #4CAF50; color: white; border: none; border-radius: 3px; }
        QPushButton:hover { background-color: #45a049; }
    """)

    # Input channel dropdown
    in_label = QtWidgets.QLabel("Select Input Channel (in):")
    in_label.setAlignment(QtCore.Qt.AlignLeft)
    in_channel_list = QtWidgets.QComboBox()
    in_channel_list.addItems(layers)
    if current_in in layers:
        in_channel_list.setCurrentText(current_in)  # Default to current 'in' or 'in1'
    layout.addWidget(in_label)
    layout.addWidget(in_channel_list)

    # Output channel dropdown, include current 'out' even if custom
    out_label = QtWidgets.QLabel("Select Output Channel (out):")
    out_label.setAlignment(QtCore.Qt.AlignLeft)
    out_channel_list = QtWidgets.QComboBox()
    # Add current out to the list if not already in layers
    out_layers = layers.copy()
    if current_out and current_out not in out_layers:
        out_layers.insert(0, current_out)  # Add current out at the top
    out_channel_list.addItems(out_layers)
    if current_out:
        out_channel_list.setCurrentText(current_out)  # Default to current 'out' or 'out1'
    elif 'rgba' in out_layers:
        out_channel_list.setCurrentText('rgba')  # Fallback to 'rgba' if no current value
    layout.addWidget(out_label)
    layout.addWidget(out_channel_list)

    # Custom output channel
    custom_label = QtWidgets.QLabel("Custom Output Channel (optional):")
    custom_label.setAlignment(QtCore.Qt.AlignLeft)
    custom_channel_input = QtWidgets.QLineEdit()
    custom_channel_input.setText("M_customChannel")  # Default text
    layout.addWidget(custom_label)
    layout.addWidget(custom_channel_input)

    # Apply button
    apply_btn = QtWidgets.QPushButton("Apply")
    apply_btn.setFixedWidth(100)
    layout.addWidget(apply_btn, alignment=QtCore.Qt.AlignCenter)

    # Stretch to keep content neat
    layout.addStretch()

    def apply_selection():
        in_channel = in_channel_list.currentText()
        out_channel = out_channel_list.currentText()
        custom_channel = custom_channel_input.text().strip()

        # Set the input knob based on node type
        if is_new:
            shuffle_node['in1'].setValue(in_channel)
        else:
            shuffle_node['in'].setValue(in_channel)

        # Handle custom channel
        if custom_channel and custom_channel != "M_customChannel":
            if custom_channel not in nuke.layers():
                # Create a new layer with RGBA sub-channels
                new_c = [f"{custom_channel}.red", f"{custom_channel}.green", 
                         f"{custom_channel}.blue", f"{custom_channel}.alpha"]
                nuke.Layer(custom_channel, new_c)
                print(f"Created new channel '{custom_channel}'.")
            else:
                print(f"Channel '{custom_channel}' already exists.")
            # Set the output knob based on node type
            if is_new:
                shuffle_node['out1'].setValue(custom_channel)
            else:
                shuffle_node['out'].setValue(custom_channel)
        else:
            # Use dropdown value
            if is_new:
                shuffle_node['out1'].setValue(out_channel)
            else:
                shuffle_node['out'].setValue(out_channel)

        # Update UI
        nuke.updateUI()
        dialog.accept()

    apply_btn.clicked.connect(apply_selection)
    dialog.setLayout(layout)
    dialog.exec_()

