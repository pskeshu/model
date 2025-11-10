#!/usr/bin/env python3
"""
Story Mode: Experiment Journey Visualization

Follows a single researcher's experiment through the global queue system,
showing the human story and scientific context at each stage.
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
import numpy as np
from datetime import datetime, timedelta
import argparse


class ExperimentStory:
    """Represents one researcher's experiment journey"""

    def __init__(self):
        # Researcher details
        self.researcher_name = "Dr. Sarah Johnson"
        self.institution = "Stanford University, USA"
        self.question = "How do neural crest cells migrate during brain development?"

        # Experiment details
        self.experiment_name = "Zebrafish Neural Development Imaging"
        self.sample = "Zebrafish embryo, 24hpf, GFP-labeled neurons"
        self.microscope = "DiSPIM"
        self.duration = "12 hours"
        self.imaging_params = "360 timepoints, 2-minute intervals, dual-view light-sheet"

        # Journey stages with times
        self.start_time = datetime.now().replace(hour=10, minute=30, second=0)

        self.stages = [
            {
                "name": "THE QUESTION",
                "time": self.start_time - timedelta(days=7),
                "duration": "7 days",
                "icon": "🔬",
                "color": "#00BCD4",
                "title": "The Scientific Question",
                "description": [
                    f'Dr. Sarah Johnson asks:',
                    f'"How do neural crest cells migrate during brain development?"',
                    '',
                    'The Challenge:',
                    '• Need to track individual cells over 12 hours',
                    '• Standard confocal too slow (miss critical movements)',
                    '• Phototoxicity kills cells in extended imaging',
                    '',
                    'The Solution:',
                    f'DiSPIM provides speed + resolution + minimal phototoxicity',
                ],
                "status": "Preparing sample and experimental design"
            },
            {
                "name": "SUBMISSION",
                "time": self.start_time,
                "duration": "2 minutes",
                "icon": "📤",
                "color": "#4CAF50",
                "title": "Submission to Global Queue",
                "description": [
                    f'Time: {self.start_time.strftime("%I:%M %p PST")}',
                    '',
                    'Submitting via REST API:',
                    '• Sample specification (sample_spec.json)',
                    '• Scientific rationale',
                    '• Priority: HIGH (live sample, time-sensitive)',
                    '',
                    f'Sample: {self.sample}',
                    f'Requested: {self.microscope}',
                    f'Duration: {self.duration} of continuous imaging',
                    '',
                    'Request ID: EXP-2847',
                    '✓ Submitted successfully',
                ],
                "status": "Awaiting review"
            },
            {
                "name": "QUEUE",
                "time": self.start_time + timedelta(minutes=2),
                "duration": "3 hours",
                "icon": "📋",
                "color": "#FF9800",
                "title": "In Review Queue",
                "description": [
                    f'Position in queue: #3',
                    '',
                    f'Ahead of this request:',
                    '  1. 🔴 URGENT: Live organoid (expires in 4h)',
                    '  2. 🟠 HIGH: Drug response time course',
                    '',
                    f'Behind this request: 5 experiments',
                    '',
                    'Notification sent to:',
                    '  → Ryan (DiSPIM specialist)',
                    '  → Email: "New HIGH priority DiSPIM request"',
                    '',
                    f'Estimated review time: 2-4 hours',
                    'Dr. Sarah receives email: "Request submitted successfully"',
                ],
                "status": "Waiting for Ryan's review"
            },
            {
                "name": "REVIEW",
                "time": self.start_time + timedelta(hours=3, minutes=45),
                "duration": "32 minutes",
                "icon": "👀",
                "color": "#9C27B0",
                "title": "Expert Review by Ryan",
                "description": [
                    f'Reviewer: Ryan (DiSPIM Specialist)',
                    f'Started: {(self.start_time + timedelta(hours=3, minutes=45)).strftime("%I:%M %p")}',
                    '',
                    'Evaluation checklist:',
                    '  ✓ Scientific rationale: Excellent',
                    '  ✓ DiSPIM suitability: Perfect fit',
                    '  ✓ Sample preparation: Appropriate',
                    '  ✓ Imaging parameters: Well-designed',
                    '  ✓ Duration feasible: 12 hours OK',
                    '  ✓ Urgency justified: Live sample, limited window',
                    '',
                    'Ryan\'s assessment:',
                    '"This is exactly what DiSPIM excels at. Neural crest',
                    'migration requires the speed and 3D coverage that only',
                    'dual-view light-sheet can provide. Approved."',
                ],
                "status": "Under expert review"
            },
            {
                "name": "APPROVED",
                "time": self.start_time + timedelta(hours=4, minutes=17),
                "duration": "Instant",
                "icon": "✅",
                "color": "#4CAF50",
                "title": "Experiment Approved!",
                "description": [
                    f'Time: {(self.start_time + timedelta(hours=4, minutes=17)).strftime("%I:%M %p PST")}',
                    '',
                    '✅ APPROVED by Ryan',
                    '',
                    'Reviewer comments:',
                    '"Perfect use case for DiSPIM. Your imaging parameters',
                    'look great. One suggestion: consider adding a 405nm',
                    'channel if you want to track nuclear morphology."',
                    '',
                    'Scheduled:',
                    f'  Date: Tomorrow',
                    f'  Time: 9:00 AM PST',
                    f'  Estimated completion: 9:00 PM PST',
                    '',
                    'Dr. Sarah notified:',
                    '  ✓ Email sent: "Your DiSPIM experiment is approved!"',
                    '  ✓ SMS sent: "Exp #2847 approved for tomorrow 9am"',
                ],
                "status": "Scheduled for execution"
            },
            {
                "name": "PREPARATION",
                "time": self.start_time + timedelta(days=1, hours=-1),
                "duration": "1 hour",
                "icon": "🔧",
                "color": "#2196F3",
                "title": "Microscope Preparation",
                "description": [
                    f'Time: 8:00 AM PST (Next Day)',
                    '',
                    'Lab technician preparing DiSPIM:',
                    '  ✓ Optical alignment check',
                    '  ✓ Temperature stabilization (28.5°C for zebrafish)',
                    '  ✓ Chamber cleaning and preparation',
                    '  ✓ Laser power calibration',
                    '  ✓ Camera synchronization test',
                    '',
                    'Sample mounting:',
                    '  ✓ Embryo embedded in low-melt agarose',
                    '  ✓ Positioned in dual-view chamber',
                    '  ✓ E3 medium perfusion system connected',
                    '  ✓ Focus and orientation optimized',
                    '',
                    'Parameters loaded from sample_spec:',
                    '  • 488nm laser (GFP excitation)',
                    '  • 2-minute intervals, 360 timepoints',
                    '  • Dual views for 3D reconstruction',
                ],
                "status": "Setting up experiment"
            },
            {
                "name": "EXECUTION",
                "time": self.start_time + timedelta(days=1),
                "duration": "12 hours",
                "icon": "📸",
                "color": "#F44336",
                "title": "Imaging in Progress",
                "description": [
                    f'Started: 9:00 AM PST',
                    f'Expected completion: 9:00 PM PST',
                    '',
                    'Live status: ████████░░░░░ 67% complete',
                    'Timepoints acquired: 240 / 360',
                    'Elapsed: 8h 00m | Remaining: 4h 00m',
                    '',
                    'Data being collected:',
                    '  • Dual-view light-sheet images',
                    '  • Z-stack at each timepoint (150 planes)',
                    '  • GFP fluorescence (neural crest cells)',
                    '  • Current data size: 32 GB',
                    '',
                    'Quality metrics:',
                    '  ✓ Sample health: Excellent',
                    '  ✓ Photobleaching: Minimal (<5%)',
                    '  ✓ Drift: Compensated automatically',
                    '  ✓ Signal-to-noise: High',
                    '',
                    'Dr. Sarah can monitor progress via web dashboard',
                ],
                "status": "Acquiring data - DO NOT DISTURB"
            },
            {
                "name": "PROCESSING",
                "time": self.start_time + timedelta(days=1, hours=12),
                "duration": "2 hours",
                "icon": "⚙️",
                "color": "#673AB7",
                "title": "Data Processing",
                "description": [
                    f'Imaging complete: 9:00 PM PST',
                    '',
                    'Automated processing pipeline:',
                    '  ⚙️  Dual-view fusion (merging views)',
                    '  ⚙️  Deconvolution (enhancing resolution)',
                    '  ⚙️  Drift correction',
                    '  ⚙️  Background subtraction',
                    '  ⚙️  Format conversion (raw → HDF5)',
                    '  ⚙️  Metadata embedding',
                    '',
                    'Generating previews:',
                    '  ✓ Maximum intensity projections',
                    '  ✓ Time-lapse movie (all timepoints)',
                    '  ✓ 3D renderings at key timepoints',
                    '  ✓ Thumbnail gallery',
                    '',
                    'Final data package:',
                    '  • Raw data: 45 GB',
                    '  • Processed data: 38 GB',
                    '  • Previews: 2.3 GB',
                ],
                "status": "Processing and quality control"
            },
            {
                "name": "DELIVERY",
                "time": self.start_time + timedelta(days=1, hours=14),
                "duration": "Instant",
                "icon": "📬",
                "color": "#4CAF50",
                "title": "Results Delivered",
                "description": [
                    f'Completed: 11:00 PM PST',
                    '',
                    'Dr. Sarah notified:',
                    '  ✓ Email: "Your DiSPIM experiment is complete!"',
                    '  ✓ SMS: "Data ready for download"',
                    '  ✓ Dashboard updated with preview images',
                    '',
                    'Data available at:',
                    '  • High-speed download: AWS S3',
                    '  • Preview via browser',
                    '  • Expiration: 30 days (then archived)',
                    '',
                    'Package includes:',
                    '  📁 Raw data (45 GB)',
                    '  📁 Processed data (38 GB)',
                    '  📁 Preview movies (2.3 GB)',
                    '  📄 Metadata and acquisition parameters',
                    '  📄 Processing log',
                    '  📄 Quality metrics report',
                ],
                "status": "Results available for download"
            },
            {
                "name": "DISCOVERY",
                "time": self.start_time + timedelta(days=8),
                "duration": "Ongoing",
                "icon": "🎉",
                "color": "#FFD700",
                "title": "Scientific Discovery",
                "description": [
                    f'Analysis reveals breakthrough finding:',
                    '',
                    '🔬 Key Discovery:',
                    'Neural crest cells migrate using a "scout" strategy:',
                    '  • Lead cells explore paths independently',
                    '  • Follower cells track leaders via contact',
                    '  • Migration speed varies with local cell density',
                    '  • Cells avoid previous paths (memory mechanism)',
                    '',
                    'This was IMPOSSIBLE to see without DiSPIM!',
                    '  → Previous imaging too slow (missed movements)',
                    '  → 2D imaging missed 3D path complexity',
                    '  → Phototoxicity disrupted natural behavior',
                    '',
                    'Impact:',
                    '  📝 Paper submitted to Nature',
                    '  🎤 Presented at Developmental Biology conference',
                    '  💰 Grant funded based on preliminary data',
                    '  🎓 Core data for PhD student\'s thesis',
                    '',
                    '"This experiment changed my research direction!" - Dr. Sarah',
                ],
                "status": "Science in action!"
            },
        ]

    def get_stage(self, frame):
        """Get the stage for the current frame"""
        stage_index = min(frame, len(self.stages) - 1)
        return self.stages[stage_index], stage_index


class StoryModeAnimation:
    """Creates story-mode timeline visualization"""

    def __init__(self, figsize=(20, 11)):
        self.story = ExperimentStory()
        self.current_frame = 0

        # Set up figure with dark background
        plt.style.use('dark_background')
        self.fig = plt.figure(figsize=figsize, facecolor='#0a0a0a')

        # Create main axis
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#0a0a0a')
        self.ax.axis('off')
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)

    def draw_timeline(self, current_stage_idx):
        """Draw the timeline at the bottom"""
        timeline_y = 0.08
        timeline_start_x = 0.1
        timeline_end_x = 0.9
        timeline_width = timeline_end_x - timeline_start_x

        num_stages = len(self.story.stages)
        stage_spacing = timeline_width / (num_stages - 1)

        # Draw timeline line
        self.ax.plot([timeline_start_x, timeline_end_x], [timeline_y, timeline_y],
                    color='#333333', linewidth=3, zorder=1)

        # Draw stage markers
        for i, stage in enumerate(self.story.stages):
            x = timeline_start_x + i * stage_spacing

            if i < current_stage_idx:
                # Completed stages
                color = '#4CAF50'
                size = 400
                alpha = 0.6
            elif i == current_stage_idx:
                # Current stage
                color = stage['color']
                size = 800
                alpha = 1.0
            else:
                # Future stages
                color = '#555555'
                size = 300
                alpha = 0.3

            # Stage circle
            circle = Circle((x, timeline_y), 0.015, color=color, alpha=alpha,
                          zorder=2, ec='white', linewidth=2 if i == current_stage_idx else 1)
            self.ax.add_patch(circle)

            # Stage label
            label_y = timeline_y - 0.04
            fontsize = 10 if i == current_stage_idx else 8
            fontweight = 'bold' if i == current_stage_idx else 'normal'
            label_color = 'white' if i <= current_stage_idx else '#666666'

            self.ax.text(x, label_y, stage['name'],
                        ha='center', va='top',
                        fontsize=fontsize, fontweight=fontweight,
                        color=label_color)

    def draw_stage_content(self, stage, stage_idx):
        """Draw the main content for the current stage"""

        # Stage header
        header_y = 0.93
        self.ax.text(0.5, header_y, f"{stage['icon']}  {stage['title']}",
                    ha='center', va='top',
                    fontsize=28, fontweight='bold', color=stage['color'])

        # Time and duration info
        time_y = 0.87
        time_str = stage['time'].strftime("%I:%M %p, %B %d")
        self.ax.text(0.5, time_y, f"Time: {time_str}  •  Duration: {stage['duration']}",
                    ha='center', va='top',
                    fontsize=12, color='#AAAAAA', style='italic')

        # Main content box
        box_y = 0.78
        box_height = 0.55
        box = FancyBboxPatch((0.08, box_y - box_height), 0.84, box_height,
                            boxstyle="round,pad=0.02",
                            facecolor='#1a1a1a',
                            edgecolor=stage['color'],
                            linewidth=3,
                            zorder=0)
        self.ax.add_patch(box)

        # Description text
        text_y = box_y - 0.03
        line_height = 0.035

        for line in stage['description']:
            if line == '':
                text_y -= line_height * 0.5  # Half space for empty lines
                continue

            # Check if it's a header (ends with :)
            if line.strip().endswith(':') and not line.startswith(' '):
                color = stage['color']
                weight = 'bold'
                size = 13
            # Check if it's a bullet point
            elif line.strip().startswith('•') or line.strip().startswith('✓'):
                color = '#CCCCCC'
                weight = 'normal'
                size = 11
            # Check if it's indented (sub-point)
            elif line.startswith('  '):
                color = '#AAAAAA'
                weight = 'normal'
                size = 10
            # Check if it's a quote
            elif '"' in line:
                color = '#FFD700'
                weight = 'normal'
                size = 12
                line = f'  {line}'  # Indent quotes
            else:
                color = 'white'
                weight = 'normal'
                size = 12

            self.ax.text(0.12, text_y, line,
                        ha='left', va='top',
                        fontsize=size, fontweight=weight, color=color,
                        family='monospace' if line.startswith('  ') else 'sans-serif')

            text_y -= line_height

        # Status indicator at bottom right
        status_y = 0.19
        self.ax.text(0.88, status_y, f"Status: {stage['status']}",
                    ha='right', va='center',
                    fontsize=10, color='#888888', style='italic',
                    bbox=dict(boxstyle='round,pad=0.5',
                            facecolor='#000000',
                            edgecolor='#444444',
                            alpha=0.8))

    def draw_progress_indicator(self, stage_idx):
        """Draw progress indicator"""
        total_stages = len(self.story.stages)
        progress_text = f"Stage {stage_idx + 1} of {total_stages}"

        self.ax.text(0.12, 0.19, progress_text,
                    ha='left', va='center',
                    fontsize=10, color='#888888',
                    bbox=dict(boxstyle='round,pad=0.5',
                            facecolor='#000000',
                            edgecolor='#444444',
                            alpha=0.8))

    def animate_frame(self, frame):
        """Animation update function"""
        self.current_frame = frame
        self.ax.clear()
        self.ax.axis('off')
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)

        # Get current stage
        stage, stage_idx = self.story.get_stage(frame)

        # Draw components
        self.draw_timeline(stage_idx)
        self.draw_stage_content(stage, stage_idx)
        self.draw_progress_indicator(stage_idx)

        # Title
        self.fig.suptitle(f"Experiment Journey: {self.story.researcher_name}",
                         fontsize=16, color='white', y=0.985, x=0.5)

    def run(self, interval=3000, save_gif=False, save_video=False,
           output_filename='story_mode_animation'):
        """Run the animation"""

        num_frames = len(self.story.stages)

        anim = animation.FuncAnimation(
            self.fig, self.animate_frame,
            frames=num_frames, interval=interval,
            repeat=True, blit=False
        )

        if save_gif:
            print(f"Saving animation as {output_filename}.gif...")
            anim.save(f'{output_filename}.gif', writer='pillow', fps=1000/interval)
            print(f"✓ Saved as {output_filename}.gif")

        if save_video:
            print(f"Saving animation as {output_filename}.mp4...")
            anim.save(f'{output_filename}.mp4', writer='ffmpeg', fps=1000/interval)
            print(f"✓ Saved as {output_filename}.mp4")

        if not save_gif and not save_video:
            plt.show()

        plt.close()


def main():
    parser = argparse.ArgumentParser(
        description="Story Mode: Follow one experiment's journey through the system"
    )
    parser.add_argument('--interval', type=int, default=3000,
                       help='Interval between frames in ms (default: 3000)')
    parser.add_argument('--save-gif', action='store_true',
                       help='Save animation as GIF')
    parser.add_argument('--save-video', action='store_true',
                       help='Save animation as MP4 video')
    parser.add_argument('--output', type=str, default='story_mode',
                       help='Output filename (without extension)')

    args = parser.parse_args()

    print("=" * 70)
    print("Story Mode: Dr. Sarah's Experiment Journey")
    print("=" * 70)
    print()
    print("Following one researcher's experiment from question to discovery")
    print()
    print(f"Configuration:")
    print(f"  Interval: {args.interval}ms")
    print(f"  Save GIF: {args.save_gif}")
    print(f"  Save Video: {args.save_video}")
    print()

    animator = StoryModeAnimation(figsize=(20, 11))
    animator.run(
        interval=args.interval,
        save_gif=args.save_gif,
        save_video=args.save_video,
        output_filename=args.output
    )


if __name__ == "__main__":
    main()
