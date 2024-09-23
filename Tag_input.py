import nuke

# Function to generate a unique name based on existing nodes
def generate_unique_name(base_name):
    i = 1
    while nuke.exists(f"{base_name}{i}"):
        i += 1
    return f"{base_name}{i}"

# Function to create the 'Tag_input' NoOp node with a unique name
def create_tag_input_node():
    # Generate a unique name based on existing nodes
    unique_name = generate_unique_name("Tag_input")

    # Get the selected node's name, or set it to an empty string if none is selected
    try:
        sel_node = nuke.selectedNode()
        sel_node_name = sel_node['name'].value()
    except:
        sel_node_name = ' '  # If no node is selected, use a blank string

    # Create a NoOp node with the unique name and set properties
    n = nuke.nodes.NoOp(name=unique_name)
    n['tile_color'].setValue(11384831)  # Custom color
    n['label'].setValue('[value nc]')    # Display the connection name dynamically
    n['note_font'].setValue('Bitstream Vera Sans Bold')  # Font for the note

    # Add an EvalString knob to display the selected input's name
    conn_name_knob = nuke.EvalString_Knob('nc', 'Connection name', sel_node_name)
    conn_name_knob.setFlag(nuke.STARTLINE)
    n.addKnob(conn_name_knob)

    # Add a button to fetch and update the selected node's name
    get_name_knob = nuke.PyScript_Knob('get_name', 'Get name')
    get_name_knob.setValue('''
try:
    sel_node = nuke.selectedNode()
    current_node = nuke.thisNode()
    current_node['nc'].setValue(sel_node.name())
except:
    nuke.message("No node selected!")
''')
    get_name_knob.setFlag(nuke.STARTLINE)
    n.addKnob(get_name_knob)

    # Add a help text knob for user guidance
    help_text_knob = nuke.Text_Knob('help_text', '<--- Select parent node first')
    help_text_knob.clearFlag(nuke.STARTLINE)
    n.addKnob(help_text_knob)

    # Add a button to connect to the node specified in 'nc'
    connect_knob = nuke.PyScript_Knob('connect', 'Connect')
    connect_knob.setValue('''
tn = nuke.thisNode()
node_name = tn['nc'].value()
target_node = nuke.toNode(node_name) if node_name.strip() else None
if target_node:
    tn.setInput(0, target_node)
else:
    nuke.message("Node not found or invalid name!")
''')
    connect_knob.setFlag(nuke.STARTLINE)
    n.addKnob(connect_knob)

    # Add a button to zoom in on the connected node
    view_input_knob = nuke.PyScript_Knob('view_input_node', 'Jump to Input')
    view_input_knob.setValue('''
nc_name = nuke.thisNode()['nc'].value()
target_node = nuke.toNode(nc_name) if nc_name.strip() else None
if target_node:
    nuke.zoom(2, [target_node.xpos(), target_node.ypos()])
else:
    nuke.message("Target node not found or invalid!")
''')
    view_input_knob.setFlag(nuke.STARTLINE)
    n.addKnob(view_input_knob)

# Create the node when the script runs
#create_tag_input_node()
