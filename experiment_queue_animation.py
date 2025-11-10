#!/usr/bin/env python3
"""
Global Experiment Queue Animation

Visualizes the worldwide experiment submission and review workflow,
showing researchers from different countries submitting imaging requests,
reviewers (like Ryan) approving experiments, and the execution pipeline.
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
import networkx as nx
import numpy as np
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
from enum import Enum
import random
from datetime import datetime
import argparse


class NodeType(Enum):
    """Types of nodes in the experiment queue system."""
    RESEARCHER = "researcher"
    QUEUE_HUB = "queue_hub"
    REVIEWER = "reviewer"
    MICROSCOPE = "microscope"
    EXECUTION = "execution"
    RESULTS = "results"


@dataclass
class NodeStyle:
    """Visual styling for different node types."""
    color: str
    shape: str
    size: int
    label: str


# Define visual styles for each node type
NODE_STYLES = {
    NodeType.RESEARCHER: NodeStyle(
        color='#00BCD4',  # Cyan
        shape='o',
        size=1000,
        label='Researcher'
    ),
    NodeType.QUEUE_HUB: NodeStyle(
        color='#F44336',  # Red
        shape='h',  # Hexagon
        size=1800,
        label='Global Queue'
    ),
    NodeType.REVIEWER: NodeStyle(
        color='#9C27B0',  # Purple
        shape='s',  # Square
        size=1400,
        label='Reviewer'
    ),
    NodeType.MICROSCOPE: NodeStyle(
        color='#4CAF50',  # Green
        shape='D',  # Diamond
        size=1200,
        label='Microscope'
    ),
    NodeType.EXECUTION: NodeStyle(
        color='#FF9800',  # Orange
        shape='^',  # Triangle
        size=1000,
        label='Execution'
    ),
    NodeType.RESULTS: NodeStyle(
        color='#2196F3',  # Blue
        shape='v',  # Triangle down
        size=900,
        label='Results'
    ),
}


# Sample researchers from around the world
RESEARCHERS = [
    {"name": "Dr. Sarah\n(USA)", "institution": "Stanford", "specialty": "DiSPIM"},
    {"name": "Dr. Chen\n(China)", "institution": "Tsinghua", "specialty": "Confocal"},
    {"name": "Dr. Schmidt\n(Germany)", "institution": "MPI", "specialty": "DiSPIM"},
    {"name": "Dr. Patel\n(India)", "institution": "IISc", "specialty": "Widefield"},
    {"name": "Dr. Silva\n(Brazil)", "institution": "USP", "specialty": "Confocal"},
]


# Sample experiments
EXPERIMENT_TYPES = [
    {"name": "Zebrafish Development", "microscope": "DiSPIM", "priority": "high", "duration": "12h"},
    {"name": "Protein Localization", "microscope": "Confocal", "priority": "medium", "duration": "6h"},
    {"name": "Cell Migration", "microscope": "DiSPIM", "priority": "urgent", "duration": "24h"},
    {"name": "Drug Screening", "microscope": "Widefield", "priority": "low", "duration": "4h"},
    {"name": "Neural Imaging", "microscope": "DiSPIM", "priority": "high", "duration": "18h"},
]


class ExperimentQueueGraph:
    """Creates and manages the experiment queue network graph."""

    def __init__(self):
        self.graph = nx.Graph()
        self.node_types: Dict[str, NodeType] = {}
        self.pos = {}

        self._build_network()
        self._compute_layout()

    def _build_network(self):
        """Build the network topology."""

        # Add global queue hub (center)
        self.graph.add_node("Global_Queue")
        self.node_types["Global_Queue"] = NodeType.QUEUE_HUB

        # Add researchers (arranged in circle around queue)
        for i, researcher in enumerate(RESEARCHERS):
            node_id = f"Researcher_{i}"
            self.graph.add_node(node_id, **researcher)
            self.node_types[node_id] = NodeType.RESEARCHER
            self.graph.add_edge(node_id, "Global_Queue")

        # Add reviewers (between queue and microscopes)
        reviewers = [
            {"name": "Ryan\n(DiSPIM)", "microscope": "DiSPIM"},
            {"name": "Team\n(Confocal)", "microscope": "Confocal"},
            {"name": "Team\n(Widefield)", "microscope": "Widefield"},
        ]

        for i, reviewer in enumerate(reviewers):
            node_id = f"Reviewer_{reviewer['microscope']}"
            self.graph.add_node(node_id, **reviewer)
            self.node_types[node_id] = NodeType.REVIEWER
            self.graph.add_edge("Global_Queue", node_id)

        # Add microscope systems
        microscopes = ["DiSPIM", "Confocal", "Widefield"]
        for microscope in microscopes:
            node_id = f"Microscope_{microscope}"
            self.graph.add_node(node_id, name=microscope)
            self.node_types[node_id] = NodeType.MICROSCOPE
            self.graph.add_edge(f"Reviewer_{microscope}", node_id)

            # Add execution node for each microscope
            exec_id = f"Execution_{microscope}"
            self.graph.add_node(exec_id, name=f"Execute")
            self.node_types[exec_id] = NodeType.EXECUTION
            self.graph.add_edge(node_id, exec_id)

            # Add results node
            results_id = f"Results_{microscope}"
            self.graph.add_node(results_id, name=f"Results")
            self.node_types[results_id] = NodeType.RESULTS
            self.graph.add_edge(exec_id, results_id)

    def _compute_layout(self):
        """Compute node positions for visualization."""
        # Manual layout for clarity

        # Center: Global Queue
        self.pos["Global_Queue"] = (0, 0)

        # Researchers in a circle around the queue
        num_researchers = len(RESEARCHERS)
        radius = 3.5
        for i in range(num_researchers):
            angle = 2 * np.pi * i / num_researchers + np.pi / 2
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            self.pos[f"Researcher_{i}"] = (x, y)

        # Reviewers, microscopes, execution, and results in layers
        microscopes = ["DiSPIM", "Confocal", "Widefield"]

        for i, microscope in enumerate(microscopes):
            # Angle for this microscope system
            angle = 2 * np.pi * i / len(microscopes) - np.pi / 6

            # Reviewer closer to queue
            reviewer_r = 1.8
            self.pos[f"Reviewer_{microscope}"] = (
                reviewer_r * np.cos(angle),
                reviewer_r * np.sin(angle)
            )

            # Microscope further out
            micro_r = 3.0
            self.pos[f"Microscope_{microscope}"] = (
                micro_r * np.cos(angle),
                micro_r * np.sin(angle)
            )

            # Execution even further
            exec_r = 4.2
            self.pos[f"Execution_{microscope}"] = (
                exec_r * np.cos(angle),
                exec_r * np.sin(angle)
            )

            # Results at the edge
            results_r = 5.0
            self.pos[f"Results_{microscope}"] = (
                results_r * np.cos(angle),
                results_r * np.sin(angle)
            )


class ExperimentQueueAnimation:
    """Animates the experiment queue workflow."""

    def __init__(self, figsize=(20, 11)):
        self.graph_manager = ExperimentQueueGraph()
        self.current_frame = 0
        self.workflow_sequences = []
        self.action_history = []
        self.max_history = 8

        # Set up figure with dark background
        plt.style.use('dark_background')
        self.fig = plt.figure(figsize=figsize, facecolor='#1a1a1a')

        # Create grid layout: 60% network, 40% log
        gs = gridspec.GridSpec(1, 2, width_ratios=[3, 2], figure=self.fig,
                              left=0.02, right=0.98, top=0.95, bottom=0.05,
                              wspace=0.05)

        self.ax_network = self.fig.add_subplot(gs[0])
        self.ax_log = self.fig.add_subplot(gs[1])

        # Style the axes
        for ax in [self.ax_network, self.ax_log]:
            ax.set_facecolor('#0a0a0a')
            for spine in ax.spines.values():
                spine.set_edgecolor('#333333')
                spine.set_linewidth(2)

    def create_workflow_sequence(self) -> List[Dict]:
        """Create a sequence of workflow steps for one experiment."""

        # Pick a random researcher and experiment
        researcher_idx = random.randint(0, len(RESEARCHERS) - 1)
        researcher = RESEARCHERS[researcher_idx]
        experiment = random.choice(EXPERIMENT_TYPES)

        researcher_id = f"Researcher_{researcher_idx}"
        microscope = experiment["microscope"]
        reviewer_id = f"Reviewer_{microscope}"
        microscope_id = f"Microscope_{microscope}"
        execution_id = f"Execution_{microscope}"
        results_id = f"Results_{microscope}"

        priority_color = {
            "urgent": "🔴",
            "high": "🟠",
            "medium": "🟡",
            "low": "🟢"
        }

        priority_emoji = priority_color.get(experiment["priority"], "⚪")

        sequence = [
            {
                "title": f"1. Researcher Submits Experiment",
                "nodes": [researcher_id],
                "edges": [],
                "description": f"{researcher['name']} at {researcher['institution']}",
                "action": f"Submits: {experiment['name']}",
                "details": f"Microscope: {microscope} | Priority: {priority_emoji} {experiment['priority'].upper()}",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            },
            {
                "title": f"2. Request Sent to Global Queue",
                "nodes": [researcher_id, "Global_Queue"],
                "edges": [(researcher_id, "Global_Queue")],
                "description": "Experiment request transmitted",
                "action": f"📤 Uploading sample_spec and metadata",
                "details": f"Request ID: EXP-{random.randint(1000, 9999)}",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            },
            {
                "title": f"3. Queue Routes to Reviewer",
                "nodes": ["Global_Queue", reviewer_id],
                "edges": [("Global_Queue", reviewer_id)],
                "description": f"Routing to {microscope} reviewer",
                "action": f"📧 Notification sent to reviewer",
                "details": f"Queue position: {random.randint(1, 5)}",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            },
            {
                "title": f"4. Reviewer Evaluates Request",
                "nodes": [reviewer_id],
                "edges": [],
                "description": f"{'Ryan' if microscope == 'DiSPIM' else 'Imaging Team'} reviews",
                "action": f"🔍 Evaluating scientific rationale",
                "details": f"Checking: {microscope} availability",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            },
            {
                "title": f"5. ✅ Experiment Approved",
                "nodes": [reviewer_id, microscope_id],
                "edges": [(reviewer_id, microscope_id)],
                "description": "Experiment approved for execution",
                "action": f"✅ Approved by {'Ryan' if microscope == 'DiSPIM' else 'Team'}",
                "details": f"Scheduled: Tomorrow 9:00 AM | Duration: {experiment['duration']}",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            },
            {
                "title": f"6. Microscope Preparation",
                "nodes": [microscope_id, execution_id],
                "edges": [(microscope_id, execution_id)],
                "description": f"Setting up {microscope}",
                "action": f"🔧 Configuring imaging parameters",
                "details": "Loading sample, calibrating optics",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            },
            {
                "title": f"7. Experiment Execution",
                "nodes": [execution_id],
                "edges": [],
                "description": f"Acquiring {experiment['duration']} of data",
                "action": f"📸 Imaging in progress...",
                "details": f"Type: {experiment['name']}",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            },
            {
                "title": f"8. Processing Results",
                "nodes": [execution_id, results_id],
                "edges": [(execution_id, results_id)],
                "description": "Processing and storing data",
                "action": f"💾 Saving to results database",
                "details": f"Data size: {random.randint(5, 50)} GB",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            },
            {
                "title": f"9. Notifying Researcher",
                "nodes": [results_id, "Global_Queue", researcher_id],
                "edges": [(results_id, "Global_Queue"), ("Global_Queue", researcher_id)],
                "description": "Experiment complete!",
                "action": f"📬 Sending completion notification",
                "details": f"Results available for download",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            },
            {
                "title": f"✅ Workflow Complete",
                "nodes": [researcher_id],
                "edges": [],
                "description": f"{researcher['name']} can access results",
                "action": f"🎉 Experiment successful!",
                "details": "Ready for analysis",
                "timestamp": datetime.now().strftime("%H:%M:%S")
            },
        ]

        return sequence

    def draw_network(self, active_nodes: Set[str], active_edges: Set[Tuple],
                    title: str = ""):
        """Draw the network graph with highlighted active nodes/edges."""
        self.ax_network.clear()
        self.ax_network.axis('off')
        self.ax_network.set_xlim(-6, 6)
        self.ax_network.set_ylim(-6, 6)

        graph = self.graph_manager.graph
        pos = self.graph_manager.pos
        node_types = self.graph_manager.node_types

        # Draw all edges (dimmed)
        nx.draw_networkx_edges(
            graph, pos,
            edge_color='#333333',
            width=1.5,
            alpha=0.3,
            ax=self.ax_network
        )

        # Draw active edges (highlighted)
        if active_edges:
            nx.draw_networkx_edges(
                graph, pos,
                edgelist=list(active_edges),
                edge_color='#FFD700',
                width=4,
                alpha=0.9,
                arrows=True,
                arrowsize=20,
                arrowstyle='->',
                connectionstyle='arc3,rad=0.1',
                ax=self.ax_network
            )

        # Draw nodes by type
        for node_type, style in NODE_STYLES.items():
            nodes_of_type = [n for n, t in node_types.items() if t == node_type]

            if not nodes_of_type:
                continue

            # Separate active and inactive nodes
            active = [n for n in nodes_of_type if n in active_nodes]
            inactive = [n for n in nodes_of_type if n not in active_nodes]

            # Draw inactive nodes (dimmed)
            if inactive:
                nx.draw_networkx_nodes(
                    graph, pos,
                    nodelist=inactive,
                    node_color=style.color,
                    node_shape=style.shape,
                    node_size=style.size,
                    alpha=0.3,
                    edgecolors='#666666',
                    linewidths=1.5,
                    ax=self.ax_network
                )

            # Draw active nodes (highlighted)
            if active:
                nx.draw_networkx_nodes(
                    graph, pos,
                    nodelist=active,
                    node_color=style.color,
                    node_shape=style.shape,
                    node_size=style.size * 1.3,
                    alpha=0.95,
                    edgecolors='#FFD700',
                    linewidths=3,
                    ax=self.ax_network
                )

        # Draw labels for active and important nodes
        labels_to_draw = {}

        # Always show these important nodes
        important_nodes = ["Global_Queue"] + [f"Reviewer_{m}" for m in ["DiSPIM", "Confocal", "Widefield"]]

        for node_id in graph.nodes():
            if node_id in active_nodes or node_id in important_nodes:
                if node_id in pos:
                    x, y = pos[node_id]

                    # Get label text
                    if "name" in graph.nodes[node_id]:
                        label_text = graph.nodes[node_id]["name"]
                    elif node_id == "Global_Queue":
                        label_text = "Global\nQueue"
                    else:
                        label_text = node_id.split('_')[-1]

                    is_active = node_id in active_nodes
                    fontsize = 11 if is_active else 9
                    text_color = '#FFFFFF' if is_active else '#AAAAAA'

                    self.ax_network.text(x, y, label_text,
                                       fontsize=fontsize,
                                       fontweight='bold',
                                       color=text_color,
                                       ha='center', va='center',
                                       bbox=dict(boxstyle='round,pad=0.35',
                                               facecolor='#000000',
                                               edgecolor='#FFD700' if is_active else '#555555',
                                               alpha=0.9,
                                               linewidth=2 if is_active else 1),
                                       zorder=1000)

        # Add title
        if title:
            self.ax_network.text(0.5, 0.97, title,
                               transform=self.ax_network.transAxes,
                               fontsize=20, color='white', ha='center', va='top',
                               bbox=dict(boxstyle='round,pad=0.5',
                                       facecolor='#2a2a2a',
                                       edgecolor='#FFD700',
                                       alpha=0.9,
                                       linewidth=2),
                               fontweight='bold')

        # Add legend
        legend_elements = []
        for node_type, style in NODE_STYLES.items():
            legend_elements.append(
                plt.scatter([], [], c=style.color, marker=style.shape,
                          s=150, label=style.label, edgecolors='white',
                          linewidths=2, alpha=0.9)
            )

        self.ax_network.legend(handles=legend_elements, loc='upper left',
                             framealpha=0.95, facecolor='#1a1a1a',
                             edgecolor='#555555', labelcolor='white',
                             fontsize=10, ncol=2)

        # Add frame counter
        self.ax_network.text(0.02, 0.02, f'Frame: {self.current_frame}',
                           transform=self.ax_network.transAxes,
                           fontsize=10, color='#666666',
                           ha='left', va='bottom')

    def draw_action_log(self, current_step: Dict, upcoming_steps: List[Dict]):
        """Draw the action log panel."""
        self.ax_log.clear()
        self.ax_log.axis('off')
        self.ax_log.set_xlim(0, 1)
        self.ax_log.set_ylim(0, 1)

        # Title
        self.ax_log.text(0.5, 0.96, "Experiment Workflow Log",
                        fontsize=18, fontweight='bold', color='white',
                        ha='center', va='top',
                        bbox=dict(boxstyle='round,pad=0.5',
                                facecolor='#2a2a2a',
                                edgecolor='#FFD700',
                                linewidth=2))

        # Current action (highlighted)
        y_pos = 0.88

        # Current step box
        box_height = 0.18
        self.ax_log.add_patch(plt.Rectangle((0.05, y_pos - box_height), 0.9, box_height,
                                           facecolor='#1a4d2e',
                                           edgecolor='#4CAF50',
                                           linewidth=3, zorder=1))

        self.ax_log.text(0.08, y_pos - 0.02, "CURRENT",
                        fontsize=9, fontweight='bold', color='#4CAF50')

        self.ax_log.text(0.5, y_pos - 0.05, current_step.get('description', ''),
                        fontsize=13, fontweight='bold', color='white',
                        ha='center', va='top')

        self.ax_log.text(0.5, y_pos - 0.09, current_step.get('action', ''),
                        fontsize=11, color='#CCCCCC',
                        ha='center', va='top')

        self.ax_log.text(0.5, y_pos - 0.13, current_step.get('details', ''),
                        fontsize=9, color='#999999', style='italic',
                        ha='center', va='top')

        self.ax_log.text(0.92, y_pos - 0.02, current_step.get('timestamp', ''),
                        fontsize=8, color='#666666',
                        ha='right', va='top')

        # Divider
        y_pos -= box_height + 0.03
        self.ax_log.plot([0.1, 0.9], [y_pos, y_pos], color='#444444',
                        linewidth=1, linestyle='--')

        # Recent history
        y_pos -= 0.04
        self.ax_log.text(0.5, y_pos, "Recent History",
                        fontsize=12, fontweight='bold', color='#888888',
                        ha='center')

        y_pos -= 0.06
        for step in self.action_history[-4:]:  # Show last 4 steps
            self.ax_log.text(0.08, y_pos, "✓",
                           fontsize=10, color='#4CAF50')
            self.ax_log.text(0.13, y_pos, step.get('action', '')[:50],
                           fontsize=9, color='#AAAAAA',
                           va='center')
            y_pos -= 0.045

        # Upcoming steps
        if upcoming_steps:
            y_pos -= 0.03
            self.ax_log.plot([0.1, 0.9], [y_pos, y_pos], color='#444444',
                            linewidth=1, linestyle='--')

            y_pos -= 0.04
            self.ax_log.text(0.5, y_pos, "Next Steps",
                            fontsize=12, fontweight='bold', color='#888888',
                            ha='center')

            y_pos -= 0.06
            for i, step in enumerate(upcoming_steps[:3], 1):  # Show next 3
                self.ax_log.text(0.08, y_pos, f"{i}.",
                               fontsize=9, color='#666666')
                self.ax_log.text(0.13, y_pos, step.get('action', '')[:50],
                               fontsize=9, color='#777777',
                               va='center')
                y_pos -= 0.045

    def animate_frame(self, frame):
        """Animation update function."""
        self.current_frame = frame

        if not self.workflow_sequences:
            self.workflow_sequences = self.create_workflow_sequence()

        # Get current workflow step
        step_idx = frame % len(self.workflow_sequences)
        step = self.workflow_sequences[step_idx]

        # If we've completed a cycle, generate new workflow
        if step_idx == 0 and frame > 0:
            if self.workflow_sequences:
                self.action_history.extend(self.workflow_sequences)
                self.action_history = self.action_history[-self.max_history:]

            self.workflow_sequences = self.create_workflow_sequence()
            step = self.workflow_sequences[0]

        # Add previous step to history
        if step_idx > 0:
            prev_step = self.workflow_sequences[step_idx - 1]
            if not self.action_history or self.action_history[-1] != prev_step:
                self.action_history.append(prev_step)
                self.action_history = self.action_history[-self.max_history:]

        # Get upcoming steps
        upcoming = self.workflow_sequences[step_idx + 1:] if step_idx + 1 < len(self.workflow_sequences) else []

        # Draw both panels
        self.draw_network(set(step['nodes']), set(step['edges']), step.get('title', ''))
        self.draw_action_log(step, upcoming)

    def run(self, frames=200, interval=1500, save_gif=False, save_video=False,
            output_filename='experiment_queue_animation'):
        """Run the animation."""

        anim = animation.FuncAnimation(
            self.fig, self.animate_frame,
            frames=frames, interval=interval,
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
        description="Animate the global experiment queue workflow"
    )
    parser.add_argument('--frames', type=int, default=200,
                       help='Number of frames to animate (default: 200)')
    parser.add_argument('--interval', type=int, default=1500,
                       help='Interval between frames in ms (default: 1500)')
    parser.add_argument('--save-gif', action='store_true',
                       help='Save animation as GIF')
    parser.add_argument('--save-video', action='store_true',
                       help='Save animation as MP4 video')
    parser.add_argument('--output', type=str, default='experiment_queue_animation',
                       help='Output filename (without extension)')

    args = parser.parse_args()

    print("=" * 70)
    print("Global Experiment Queue Animation")
    print("=" * 70)
    print()
    print("This animation visualizes the worldwide experiment submission")
    print("and review workflow for imaging experiments.")
    print()
    print(f"Configuration:")
    print(f"  Frames: {args.frames}")
    print(f"  Interval: {args.interval}ms")
    print(f"  Save GIF: {args.save_gif}")
    print(f"  Save Video: {args.save_video}")
    print()

    animator = ExperimentQueueAnimation(figsize=(20, 11))
    animator.run(
        frames=args.frames,
        interval=args.interval,
        save_gif=args.save_gif,
        save_video=args.save_video,
        output_filename=args.output
    )


if __name__ == "__main__":
    main()
