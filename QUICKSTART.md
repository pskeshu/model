# Quick Start Guide

## Running the Animation

### 1. Install Dependencies

```bash
pip install matplotlib networkx numpy
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

### 2. Run the Animation

```bash
python distributed_workflow_animation.py
```

This will open an interactive window showing:
- **Left panel**: Network graph with nodes lighting up during activity
- **Right panel**: Action log showing current, upcoming, and completed tasks

### 3. Understanding the Display

#### Network Panel (Left)
- **Green circles** = Microscopes acquiring data
- **Blue squares** = HPC clusters processing
- **Orange diamonds** = Storage systems
- **Purple triangles** = Analysis nodes
- **Red hexagons** = Facility coordination hubs
- **Cyan stars** = Researchers (e.g., Ryan at Janelia)
- **Gold lines** = Active data connections

#### Action Log Panel (Right)

**▶ CURRENT ACTION**
Shows the active workflow step with:
- Color-coded badge indicating action type
- Detailed description of what's happening
- Technical details (data size, compute resources, etc.)

**⏭ UPCOMING**
Lists the next 5 workflow steps so you can see what's coming

**✓ COMPLETED**
Scrolling history of recently finished tasks

### 4. Action Types

The animation uses different action types, each with its own color:

- **ACQUIRE** (Green) - Microscope data acquisition
- **TRANSFER** (Blue) - Data transfer between nodes
- **COMPUTE** (Orange) - HPC processing
- **ANALYZE** (Purple) - Data analysis
- **STORE** (Orange) - Storage operations
- **STAGE** (Gold) - Preparing for transfer
- **SYNC** (Cyan) - Synchronizing distributed results
- **PREPARE** (Cyan) - Sample preparation by researcher
- **MOUNT** (Green) - Mounting sample on microscope
- **HYPOTHESIS** (Pink) - AI hypothesis generation
- **REVIEW** (Purple) - Human review and feedback
- **DONE** (Gray) - Workflow complete

## Example Workflows

The animation demonstrates four types of distributed workflows:

### 1. Local Processing
```
Microscope → Storage → HPC → Analysis
```
Data acquired locally, processed on facility HPC, analyzed locally

### 2. Cross-Facility Collaboration
```
Facility A Microscope → Hub A → Hub B → Facility B Storage
```
Data acquired at one facility, transferred to another for storage/processing

### 3. Distributed Computation
```
HPC Cluster 1 + HPC Cluster 2 (parallel) → Sync Results
```
Large computation split across multiple HPC resources

### 4. Active Learning Loop (Human-in-the-Loop)
```
Ryan prepares C. elegans sample → Microscope acquires data →
Remote analysis → AI generates hypothesis → Results to Ryan →
Ryan reviews and tweaks → Second iteration
```
Demonstrates the complete active learning discovery cycle where:
- Ryan (researcher at Janelia) mounts C. elegans samples
- Data is acquired and analyzed (possibly at remote facility)
- AI formulates hypotheses from the data
- Ryan receives results and refines the experiment
- Iterative cycle continues for scientific discovery

This workflow showcases the human-AI collaboration in the discovery process!

## Customization

### Change Animation Speed

Edit `main()` function:
```python
animator.run(
    frames=200,
    interval=800,  # Change this (milliseconds between frames)
    save_gif=False
)
```

### Add Your Own Facilities

Edit `create_example_network()`:
```python
workflow.add_facility("YourLab",
                     num_microscopes=4,
                     has_hpc=True,
                     has_storage=True,
                     has_analysis=True)
```

### Save as Video or GIF

To save as MP4 video:
```python
animator.run(
    frames=200,
    interval=1500,
    save_video=True,
    filename='my_workflow'
)
```
This creates `my_workflow.mp4`

To save as animated GIF:
```python
animator.run(
    frames=200,
    interval=1500,
    save_gif=True,
    filename='my_workflow'
)
```
This creates `my_workflow.gif`

**Note**: Video export requires FFmpeg to be installed:
- **macOS**: `brew install ffmpeg`
- **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
- **Windows**: Download from https://ffmpeg.org/download.html

## Troubleshooting

**Problem**: `ModuleNotFoundError: No module named 'matplotlib'`
**Solution**: Install dependencies with `pip install -r requirements.txt`

**Problem**: Animation window is too small/large
**Solution**: Edit `figsize=(20, 12)` in `WorkflowAnimator.__init__()`

**Problem**: Action log text is cut off
**Solution**: Adjust `width_ratios=[3, 1]` in GridSpec setup to give more space to the log panel

## Use Cases

This animation is perfect for:
- Conference presentations about distributed computing
- Grant proposals showing infrastructure capabilities
- Team meetings to explain workflow architecture
- Educational demonstrations of distributed systems
- Planning facility resource allocation
- Visualizing data flow in collaborative research

## Performance Tips

For smoother animation:
1. Reduce number of facilities in `create_example_network()`
2. Increase `interval` parameter (slower but smoother)
3. Reduce `num_microscopes` per facility
4. Close other graphics-intensive applications

## Next Steps

See [ANIMATION_README.md](ANIMATION_README.md) for detailed documentation on:
- Custom workflow sequences
- Advanced customization
- Architecture details
- API reference
