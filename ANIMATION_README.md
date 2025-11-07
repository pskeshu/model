# Distributed Scientific Workflow Animation

This animation visualizes a distributed network of scientific resources including microscopes, HPC clusters, storage systems, and analysis nodes across multiple facilities, with a real-time action log showing current, upcoming, and completed workflow steps.

## Features

- **Multiple Node Types:**
  - 🔬 **Microscopes** (green circles): Data acquisition instruments
  - 💻 **HPC Clusters** (blue squares): High-performance computing resources
  - 💾 **Storage** (orange diamonds): Data storage systems
  - 📊 **Analysis** (purple triangles): Analysis processing nodes
  - 🏢 **Facility Hubs** (red hexagons): Central coordination points

- **Distributed Workflows:**
  - Local data processing within facilities
  - Cross-facility collaboration and data sharing
  - Distributed HPC computation
  - Real-time visualization of active nodes and data flows

- **Visual Effects:**
  - Nodes "light up" when active with glow effects
  - Active connections highlighted in gold
  - Smooth animations showing data flow through the network

- **Action Log Panel:**
  - **Current Action**: Shows what's happening right now with detailed descriptions
  - **Upcoming Actions**: Preview of the next 5 workflow steps
  - **Completed Actions**: History of recently completed tasks
  - Color-coded action types (ACQUIRE, TRANSFER, COMPUTE, ANALYZE, etc.)
  - Real-time updates synchronized with network visualization

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install matplotlib networkx numpy
```

## Usage

### Basic Usage

Run the animation with default settings:

```bash
python distributed_workflow_animation.py
```

This will display an interactive window showing the animated workflow. Close the window to exit.

### Save as GIF

To save the animation as a GIF file, modify the `main()` function:

```python
# Change this line in main():
animator.run(frames=200, interval=800, save_gif=True)
```

Then run:

```bash
python distributed_workflow_animation.py
```

## Customization

### Adding Your Own Facilities

Edit the `create_example_network()` function:

```python
def create_example_network():
    workflow = DistributedWorkflowGraph()

    # Add your facilities
    workflow.add_facility("YourLab",
                         num_microscopes=3,
                         has_hpc=True,
                         has_storage=True,
                         has_analysis=True)

    # Connect to other facilities
    workflow.connect_facilities("YourLab", "MIT")

    return workflow
```

### Adjusting Animation Parameters

In the `main()` function:

```python
animator.run(
    frames=200,      # Number of animation frames
    interval=800,    # Milliseconds between frames
    save_gif=False   # Set to True to save as GIF
)
```

### Creating Custom Workflows

Override the `create_workflow_sequence()` method to define your own workflow patterns:

```python
def create_workflow_sequence(self) -> List[Dict]:
    sequences = []

    # Your custom workflow
    sequences.append({
        'nodes': ['MIT_microscope_1', 'MIT_storage'],
        'edges': [('MIT_microscope_1', 'MIT_hub'), ('MIT_hub', 'MIT_storage')],
        'title': 'Acquiring and storing data'
    })

    return sequences
```

## Architecture

The animation consists of three main components:

1. **DistributedWorkflowGraph**: Manages the network topology
   - Adds facilities with their resources
   - Creates connections between facilities
   - Calculates optimal layout

2. **WorkflowAnimator**: Handles visualization and animation
   - Renders the network graph
   - Animates node activation and data flows
   - Manages visual effects

3. **Workflow Sequences**: Define the patterns of activity
   - Local processing workflows
   - Cross-facility collaboration
   - Distributed computation patterns

## Example Network Topology

The default network includes:

- **MIT**: 4 microscopes, HPC, storage, analysis
- **Stanford**: 3 microscopes, HPC, storage, analysis
- **Berkeley**: 2 microscopes, HPC, storage
- **Janelia**: 5 microscopes, HPC, storage, analysis
- **EMBL**: 3 microscopes, storage, analysis

Connected in a mesh topology allowing flexible data routing between facilities.

## Use Cases

This visualization is useful for:

- Demonstrating distributed scientific computing concepts
- Planning facility resource allocation
- Visualizing data flow in collaborative research
- Presenting infrastructure capabilities
- Teaching distributed systems architecture

## Technical Details

- Built with NetworkX for graph management
- Matplotlib for rendering and animation
- Spring layout algorithm for automatic node positioning
- Frame-based animation with configurable timing
- Support for GIF export using Pillow

## Future Enhancements

Potential additions:
- Real-time data integration from actual systems
- Interactive node selection and workflow control
- 3D visualization for larger networks
- Performance metrics overlay
- Web-based version using D3.js
- Load balancing visualization
- Fault tolerance scenarios
