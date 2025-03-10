import nuke
from PySide2 import QtWidgets, QtGui, QtCore
from functools import partial
import colorsys

class BackdropCreator(QtWidgets.QDialog):
    def __init__(self):
        super(BackdropCreator, self).__init__()

        self.setWindowTitle("Enhanced Backdrop Creator")
        self.setMinimumWidth(400)

        # Initialize variables
        self.label_text = None
        self.backdrop_color = None
        self.font_color = 0xFFFFFFFFFF
        self.padding = 30
        self.color_saturation = 0.35  # Saturation value
        self.color_value = 0.35       # Value (brightness)
        self.font_size = 100  # Default font size

        # Preset label-color mappings with adjusted colors
        self.label_color_presets = self.generate_muted_colors({
            "Keying": (120, 1),        # Green
            "Color Correction": (220, 1),  # Blue
            "Despill": (180, 1),       # Cyan
            "Roto": (0, 1),            # Red
            "Plate Fix": (60, 1),      # Yellow
            "Temp Fix": (45, 1),       # Orange-yellow
            "Edge Fix": (15, 1),       # Burnt orange
            "Projection": (270, 1),    # Purple
            "Temp Grade": (240, 1),  # Soft blue
            "Cleanup": (150, 1)        # Teal
        })

        # Preset categories with color-coded options
        self.preset_categories = {
            "Compositing": [
                ("Keying", self.label_color_presets["Keying"]),
                ("Despill", self.label_color_presets["Despill"]), 
                ("Temp Fix", self.label_color_presets["Temp Fix"]),
                ("Edge Fix", self.label_color_presets["Edge Fix"]),
                ("Projection", self.label_color_presets["Projection"])
            ],
            "Color": [
                ("Color Correction", self.label_color_presets["Color Correction"]), 
                ("Temp Grade", self.label_color_presets["Temp Grade"])
            ],
            "Cleanup": [
                ("Plate Fix", self.label_color_presets["Plate Fix"]), 
                ("Roto", self.label_color_presets["Roto"]), 
                ("Cleanup", self.label_color_presets["Cleanup"])
            ]
        }

        # Generate color options
        self.color_options = self.generate_color_options()
        
        self.setup_ui()

    def color_to_hex(self, color_value):
        """Converts integer color to hex string"""
        return "#{:06x}".format(color_value >> 8)

    def generate_muted_colors(self, base_colors):
        """
        Generate muted colors with consistent saturation and value
        
        Args:
            base_colors (dict): Dictionary of color names with (hue, saturation) tuples
        
        Returns:
            dict: Dictionary of color names with muted color values
        """
        muted_colors = {}
        for name, (hue, sat) in base_colors.items():
            # Modify value for specific colors
            if name in ["Red", "Green", "Blue", "Yellow"]:
                value = 0.6  # Higher brightness for these colors
            else:
                value = self.color_value  # Default value
            # Convert HSV to RGB, then to Nuke's color format
            rgb = colorsys.hsv_to_rgb(hue/360, self.color_saturation, self.color_value)
            # Convert RGB to Nuke's color format (0-255 scaled to hex with alpha)
            color_value = (int(rgb[0]*255) << 24) + \
                          (int(rgb[1]*255) << 16) + \
                          (int(rgb[2]*255) << 8) + \
                          0xFF
            muted_colors[name] = color_value
        return muted_colors

    def generate_color_options(self):
        """Generate muted color options with 12 colors"""
        color_specs = [
            ("Red", (0, 1)),              # Red
            ("Green", (120, 0.8)),        # Green
            ("Yellow", (50, 1)),          # Yellow
            ("Blue", (220, 1)),           # Blue
            ("Coral", (16, 1)),           # Coral/Salmon
            ("Olive", (75, 1)),           # Olive green
            ("Teal", (180, 1)),           # Teal
            ("Indigo", (240, 1)),         # Indigo
            ("Lavender", (270, 1)),       # Lavender
            ("Magenta", (300, 1)),        # Magenta
            ("Maroon", (330, 1)),         # Maroon
            ("Brown", (30, 1))            # Brown
        ]
        
        return {
            color_name: self.generate_muted_colors({color_name: hue_sat}) 
            for color_name, hue_sat in color_specs
        }
    
    def get_text_color(self, bg_color):
        """Returns black or white text color for contrast."""
        r = (bg_color >> 24) & 0xFF
        g = (bg_color >> 16) & 0xFF
        b = (bg_color >> 8) & 0xFF
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        return "black" if luminance > 0.5 else "white"


    def setup_ui(self):
        # Clear existing layout if it exists
        if hasattr(self, 'layout'):
            QtWidgets.QWidget().setLayout(self.layout())
        
        main_layout = QtWidgets.QVBoxLayout()

        # Label input
        self.label_input = QtWidgets.QLineEdit()
        self.label_input.setPlaceholderText("Enter backdrop label...")
        main_layout.addWidget(self.label_input)

        # Create scrollable area for labels
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QtWidgets.QWidget()
        self.label_layout = QtWidgets.QVBoxLayout(scroll_widget)

        # Modified preset buttons with color-coded options
        for category, names in self.preset_categories.items():
            group = QtWidgets.QGroupBox(category)
            group_layout = QtWidgets.QVBoxLayout()

            for name, color in names:
                btn = QtWidgets.QPushButton(name)
                
                # Apply color styling
                text_color = self.get_text_color(color)
                btn.setStyleSheet(
                    f"background-color: {self.color_to_hex(color)}; "
                    f"color: {text_color}; "
                    "border: 1px solid #555;"
                )
                # Create backdrop immediately on click
                btn.clicked.connect(partial(self.set_label_and_create, name, color))
                
                group_layout.addWidget(btn)

            group.setLayout(group_layout)
            self.label_layout.addWidget(group)

        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)

        # Color selection grid with muted colors
        color_group = QtWidgets.QGroupBox("Colors")
        color_layout = QtWidgets.QGridLayout()
        row = 0
        col = 0
        max_cols = 4

        for color_name, color_dict in self.color_options.items():
            # Use the first (and only) color in the dictionary
            color_value = list(color_dict.values())[0]
            
            color_btn = QtWidgets.QPushButton(color_name)
            color_btn.setFixedSize(80, 30)
            color_btn.setStyleSheet(
                f"background-color: {self.color_to_hex(color_value)}; "
                "color: white; "
                "border: 1px solid #555;"
            )
            color_btn.clicked.connect(partial(self.set_color_and_create, color_value))
            color_layout.addWidget(color_btn, row, col)

            col += 1
            if col >= max_cols:
                col = 0
                row += 1

        color_group.setLayout(color_layout)
        main_layout.addWidget(color_group)
        # Custom color button
        custom_color_btn = QtWidgets.QPushButton("Custom Color")
        custom_color_btn.clicked.connect(self.pick_custom_color)
        color_layout.addWidget(custom_color_btn, row + 1, 0)  # Adjust row as needed

        # Padding adjustment
        padding_layout = QtWidgets.QHBoxLayout()
        padding_layout.addWidget(QtWidgets.QLabel("Padding:"))
        self.padding_spinner = QtWidgets.QSpinBox()
        self.padding_spinner.setRange(0, 200)
        self.padding_spinner.setValue(self.padding)
        self.padding_spinner.valueChanged.connect(self.update_padding)
        padding_layout.addWidget(self.padding_spinner)

        # Font size adjustment
        font_size_layout = QtWidgets.QHBoxLayout()
        font_size_layout.addWidget(QtWidgets.QLabel("Font Size:"))
        self.font_size_spinner = QtWidgets.QSpinBox()
        self.font_size_spinner.setRange(10, 200)  # Set a reasonable range
        self.font_size_spinner.setValue(self.font_size)  # Default font size
        font_size_layout.addWidget(self.font_size_spinner)
        #self.font_size_spinner.valueChanged.connect(self.update_font_size)
        self.font_size_spinner.valueChanged.connect(lambda value: setattr(self, 'font_size', value))

        main_layout.addLayout(padding_layout)
        main_layout.addLayout(font_size_layout)  # Add to main layout

        self.setLayout(main_layout)
        
        # Set focus on label input
        self.label_input.setFocus()

    def pick_custom_color(self):
        """Opens a color dialog and sets the backdrop color."""
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            # Convert Qt color to Nuke's color format
            r = int(color.redF() * 255)
            g = int(color.greenF() * 255)
            b = int(color.blueF() * 255)
            a = int(color.alphaF() * 255)
            self.backdrop_color = (r << 24) + (g << 16) + (b << 8) + a
            self.create_backdrop()  # Create backdrop with custom color

    def set_label_and_create(self, name, color):
        """Sets the label and color, then creates backdrop immediately"""
        self.label_text = name
        self.label_input.setText(name)
        self.backdrop_color = color
        self.create_backdrop()

    

    def create_backdrop(self):
        """Creates a backdrop around selected nodes"""
        try:
            selected_nodes = nuke.selectedNodes()

            if not selected_nodes:
                nuke.message("No nodes selected!")
                return

            min_x = min(n.xpos() for n in selected_nodes) - self.padding
            min_y = min(n.ypos() for n in selected_nodes) - self.padding
            max_x = max(n.xpos() + n.screenWidth() for n in selected_nodes) + self.padding
            max_y = max(n.ypos() + n.screenHeight() for n in selected_nodes) + self.padding

            backdrop = nuke.createNode("BackdropNode")
            backdrop["xpos"].setValue(min_x)
            backdrop["ypos"].setValue(min_y)
            backdrop["bdwidth"].setValue(max_x - min_x)
            backdrop["bdheight"].setValue(max_y - min_y)

            # Prioritize input text first, then preset label
            label_text = (self.label_input.text().strip() or 
                          self.label_text or 
                          "Backdrop")
            backdrop["label"].setValue(label_text)

            if self.backdrop_color:
                backdrop["tile_color"].setValue(self.backdrop_color)

            # Set label text size
            backdrop["note_font_size"].setValue(self.font_size)

            # Set label text color to white
            backdrop["note_font_color"].setValue(0xFFFFFFFF)

            self.close()  # Close the UI after creating the backdrop

        except Exception as e:
            nuke.message(f"Error creating backdrop: {str(e)}")

    def update_padding(self, value):
        """Update backdrop padding value"""
        self.padding = value

    def update_font_size(self, value):
        """Update backdrop font size value."""
        self.font_size = value

    def set_color_and_create(self, color_value):
        """Sets the backdrop tile color and creates backdrop"""
        self.backdrop_color = color_value
        self.create_backdrop()


def launch_backdrop_creator():
    if nuke.GUI:
        dialog = BackdropCreator()
        dialog.exec_()


# menubar = nuke.menu("Nuke")
#v_commands = menubar.addMenu("V_commands")
#v_commands.addCommand("Create Backdrop", lambda: launch_backdrop_creator(), "ctrl+alt+B")