# Experiment Queue Animation - Quick Start Guide

## Overview

The `experiment_queue_animation.py` script creates an animated visualization of the global experiment queue workflow, showing:

- **Researchers** from around the world submitting experiments
- **Global Queue** routing requests to appropriate reviewers
- **Reviewers** (like Ryan for DiSPIM) approving experiments
- **Microscope Systems** executing imaging experiments
- **Results** being delivered back to researchers

The animation displays a network graph with active nodes/edges highlighted, alongside an action log showing the current step and workflow history.

## Installation

### Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `matplotlib` - For creating animations
- `networkx` - For network graph visualization
- `numpy` - For numerical operations

### Optional: For Video Export

To export animations as MP4 videos, install ffmpeg:

```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Then install Python wrapper
pip install ffmpeg-python
```

## Running the Animation

### Basic Usage (Live Display)

```bash
python experiment_queue_animation.py
```

This will open a window showing the animation in real-time. Press `Ctrl+C` to stop.

### Save as GIF

```bash
python experiment_queue_animation.py --save-gif --output my_animation
```

This creates `my_animation.gif` showing the workflow.

### Save as Video (MP4)

```bash
python experiment_queue_animation.py --save-video --output my_animation
```

This creates `my_animation.mp4` (requires ffmpeg).

### Customize Animation

```bash
python experiment_queue_animation.py \
  --frames 100 \
  --interval 1000 \
  --save-gif \
  --output demo
```

Parameters:
- `--frames N` - Number of frames to animate (default: 200)
- `--interval N` - Milliseconds between frames (default: 1500)
- `--save-gif` - Save as GIF file
- `--save-video` - Save as MP4 video
- `--output NAME` - Output filename without extension

## Animation Flow

The animation shows a complete experiment workflow:

### 1. Researcher Submits Experiment
- A researcher from USA/China/Germany/India/Brazil submits an imaging request
- Includes sample specifications and scientific rationale

### 2. Request Sent to Global Queue
- Sample_spec and metadata uploaded to central queue
- Request ID assigned

### 3. Queue Routes to Reviewer
- System identifies appropriate reviewer based on microscope type
- Ryan receives DiSPIM requests
- Imaging Team handles Confocal/Widefield

### 4. Reviewer Evaluates Request
- Reviews scientific rationale
- Checks microscope availability
- Evaluates experimental feasibility

### 5. Experiment Approved
- Reviewer approves with comments
- Experiment scheduled for execution
- Requester notified

### 6. Microscope Preparation
- Configure imaging parameters
- Load sample
- Calibrate optics

### 7. Experiment Execution
- Acquire imaging data (4-24 hours)
- Different types: zebrafish development, protein localization, cell migration, etc.

### 8. Processing Results
- Process and store acquired data
- Save to results database
- Prepare data for download

### 9. Notifying Researcher
- Send completion notification
- Provide results download link

### 10. Workflow Complete
- Researcher can access results
- Ready for analysis

## Visual Elements

### Network Graph (Left Panel)

Shows the distributed system topology:

- **Cyan Circles** - Researchers worldwide
- **Red Hexagon** - Global Queue hub (center)
- **Purple Squares** - Reviewers (Ryan, Imaging Team)
- **Green Diamonds** - Microscope systems (DiSPIM, Confocal, Widefield)
- **Orange Triangles** - Execution nodes
- **Blue Triangles** - Results storage

**Active elements** are highlighted with:
- Larger size (1.3x)
- Golden edge color
- Brighter colors
- Bold labels

**Data flow** shown as:
- Golden arrows between active nodes
- Animated progression through workflow

### Action Log (Right Panel)

Shows real-time workflow status:

- **Current Action** - Green-highlighted box with:
  - Description of current step
  - Action being performed
  - Additional details
  - Timestamp

- **Recent History** - Last 4 completed steps with checkmarks

- **Next Steps** - Upcoming 3 steps in workflow

## Example Output

When you run the animation, you'll see experiments flowing through the system:

```
Frame 0: Dr. Sarah (USA) submits zebrafish development experiment
Frame 3: Ryan reviews DiSPIM request
Frame 5: Experiment approved for tomorrow 9:00 AM
Frame 7: DiSPIM executes 12-hour imaging session
Frame 9: Results delivered to Dr. Sarah
Frame 10: New experiment begins...
```

Each complete workflow cycle takes 10 frames, then a new experiment begins.

## Tips for Best Results

### For Presentations

```bash
# Slower animation for presentations
python experiment_queue_animation.py --interval 2000 --frames 50 --save-gif
```

### For Documentation

```bash
# Fast preview
python experiment_queue_animation.py --interval 800 --frames 100 --save-video
```

### For Live Demos

```bash
# Just display, no saving
python experiment_queue_animation.py --interval 1500
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'matplotlib'"

Install dependencies:
```bash
pip install matplotlib networkx numpy
```

### Emoji Warnings

You may see warnings like:
```
UserWarning: Glyph 128992 missing from font(s) DejaVu Sans
```

This is normal - emojis might not render, but the animation works fine.

### Animation Too Fast/Slow

Adjust the `--interval` parameter:
- Slower: `--interval 2000` (2 seconds per frame)
- Faster: `--interval 500` (0.5 seconds per frame)

### GIF Too Large

Reduce frames:
```bash
python experiment_queue_animation.py --frames 30 --save-gif
```

Or use video format instead:
```bash
python experiment_queue_animation.py --frames 100 --save-video
```

## Understanding the Workflow

The animation demonstrates:

1. **Global Collaboration** - Researchers worldwide can submit experiments
2. **Centralized Queue** - Single entry point manages all requests
3. **Specialized Review** - Each microscope system has dedicated reviewers
4. **Approval Workflow** - Quality control before execution
5. **Automated Execution** - Experiments run on approved schedule
6. **Results Delivery** - Data automatically returned to requesters

This system enables:
- 24/7 experiment submission from any timezone
- Fair prioritization (urgent/high/medium/low)
- Expert review by specialized reviewers
- Efficient use of expensive microscope resources
- Complete tracking from submission to results

## Integration with API Server

The animation visualizes the same workflow implemented in:
- `experiment_queue.py` - Core queue management
- `api_server.py` - REST API endpoints
- `notifications.py` - Email notification system

You can run the animation alongside the API server to demonstrate the system in action.

## Customizing the Animation

To add your own institutions, experiments, or microscope systems, edit these sections in `experiment_queue_animation.py`:

```python
# Add researchers (line ~90)
RESEARCHERS = [
    {"name": "Your Name\n(Country)", "institution": "University", "specialty": "DiSPIM"},
]

# Add experiment types (line ~100)
EXPERIMENT_TYPES = [
    {"name": "Your Experiment", "microscope": "DiSPIM", "priority": "high", "duration": "12h"},
]
```

## Questions?

For more information about the experiment queue system, see:
- [EXPERIMENT_QUEUE.md](EXPERIMENT_QUEUE.md) - Complete system documentation
- [README.md](README.md) - Project overview
- [sample_spec.md](sample_spec.md) - Experiment specification format

---

**Pro Tip**: Run the animation during meetings or presentations to demonstrate the global experiment queue workflow visually!
