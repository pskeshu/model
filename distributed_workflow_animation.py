#!/usr/bin/env python3
"""
Distributed Scientific Workflow Animation

Visualizes a network of microscopes, HPC resources, and other scientific
facilities communicating in a distributed workflow system.
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


class NodeType(Enum):
    """Types of nodes in the distributed workflow."""
    MICROSCOPE = "microscope"
    HPC = "hpc"
    STORAGE = "storage"
    ANALYSIS = "analysis"
    FACILITY_HUB = "facility_hub"
    RESEARCHER = "researcher"


@dataclass
class NodeStyle:
    """Visual styling for different node types."""
    color: str
    shape: str
    size: int
    label: str


# Define visual styles for each node type
NODE_STYLES = {
    NodeType.MICROSCOPE: NodeStyle(
        color='#4CAF50',  # Green
        shape='o',         # Circle
        size=800,
        label='Microscope'
    ),
    NodeType.HPC: NodeStyle(
        color='#2196F3',  # Blue
        shape='s',         # Square
        size=1200,
        label='HPC Cluster'
    ),
    NodeType.STORAGE: NodeStyle(
        color='#FF9800',  # Orange
        shape='D',         # Diamond
        size=900,
        label='Storage'
    ),
    NodeType.ANALYSIS: NodeStyle(
        color='#9C27B0',  # Purple
        shape='^',         # Triangle
        size=800,
        label='Analysis'
    ),
    NodeType.FACILITY_HUB: NodeStyle(
        color='#F44336',  # Red
        shape='h',         # Hexagon
        size=1000,
        label='Facility Hub'
    ),
    NodeType.RESEARCHER: NodeStyle(
        color='#00BCD4',  # Cyan
        shape='*',         # Star
        size=1000,
        label='Researcher'
    ),
}


class DistributedWorkflowGraph:
    """Creates and manages the distributed workflow network graph."""

    def __init__(self):
        self.graph = nx.Graph()
        self.node_types: Dict[str, NodeType] = {}
        self.facilities: Dict[str, List[str]] = {}

    def add_facility(self, facility_name: str,
                     num_microscopes: int = 3,
                     has_hpc: bool = True,
                     has_storage: bool = True,
                     has_analysis: bool = True,
                     researchers: List[str] = None):
        """Add a complete facility with its resources."""

        facility_nodes = []

        # Add facility hub
        hub_id = f"{facility_name}_hub"
        self.graph.add_node(hub_id)
        self.node_types[hub_id] = NodeType.FACILITY_HUB
        facility_nodes.append(hub_id)

        # Add researchers if specified
        if researchers:
            for researcher_name in researchers:
                researcher_id = f"{facility_name}_{researcher_name}"
                self.graph.add_node(researcher_id)
                self.node_types[researcher_id] = NodeType.RESEARCHER
                self.graph.add_edge(hub_id, researcher_id)
                facility_nodes.append(researcher_id)

        # Add microscopes
        for i in range(num_microscopes):
            microscope_id = f"{facility_name}_microscope_{i+1}"
            self.graph.add_node(microscope_id)
            self.node_types[microscope_id] = NodeType.MICROSCOPE
            self.graph.add_edge(hub_id, microscope_id)
            facility_nodes.append(microscope_id)

            # Connect researchers to microscopes they work with
            if researchers:
                for researcher_name in researchers:
                    researcher_id = f"{facility_name}_{researcher_name}"
                    self.graph.add_edge(researcher_id, microscope_id)

        # Add HPC if available
        if has_hpc:
            hpc_id = f"{facility_name}_hpc"
            self.graph.add_node(hpc_id)
            self.node_types[hpc_id] = NodeType.HPC
            self.graph.add_edge(hub_id, hpc_id)
            facility_nodes.append(hpc_id)

        # Add storage if available
        if has_storage:
            storage_id = f"{facility_name}_storage"
            self.graph.add_node(storage_id)
            self.node_types[storage_id] = NodeType.STORAGE
            self.graph.add_edge(hub_id, storage_id)
            facility_nodes.append(storage_id)

        # Add analysis nodes if available
        if has_analysis:
            analysis_id = f"{facility_name}_analysis"
            self.graph.add_node(analysis_id)
            self.node_types[analysis_id] = NodeType.ANALYSIS
            self.graph.add_edge(hub_id, analysis_id)
            facility_nodes.append(analysis_id)

        self.facilities[facility_name] = facility_nodes

    def connect_facilities(self, facility1: str, facility2: str):
        """Create inter-facility connections."""
        hub1 = f"{facility1}_hub"
        hub2 = f"{facility2}_hub"
        if hub1 in self.graph and hub2 in self.graph:
            self.graph.add_edge(hub1, hub2)

    def get_layout(self) -> Dict:
        """Calculate node positions using a layout algorithm."""
        # Use spring layout with facility clustering
        return nx.spring_layout(self.graph, k=2, iterations=50, seed=42)


class WorkflowAnimator:
    """Animates the distributed workflow showing node activity."""

    def __init__(self, workflow_graph: DistributedWorkflowGraph):
        self.workflow_graph = workflow_graph
        self.graph = workflow_graph.graph
        self.node_types = workflow_graph.node_types
        self.pos = workflow_graph.get_layout()

        # Animation state
        self.active_nodes: Set[str] = set()
        self.active_edges: Set[Tuple[str, str]] = set()
        self.workflow_sequences = []
        self.current_frame = 0
        self.action_history = []
        self.max_history = 10

        # Setup figure with two panels
        self.fig = plt.figure(figsize=(20, 12))
        self.fig.patch.set_facecolor('#1a1a1a')

        # Create grid: network on left (75%), action log on right (25%)
        gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1], figure=self.fig)
        self.ax_network = self.fig.add_subplot(gs[0])
        self.ax_log = self.fig.add_subplot(gs[1])

        self.ax_network.set_facecolor('#1a1a1a')
        self.ax_log.set_facecolor('#0d0d0d')

    def create_workflow_sequence(self) -> List[Dict]:
        """
        Create a sequence of workflow steps showing distributed processing.

        Example workflow:
        1. Microscope captures data
        2. Data sent to storage
        3. HPC processes data
        4. Analysis node generates results
        5. Results shared across facilities
        """
        sequences = []

        # Get all nodes by type
        microscopes = [n for n, t in self.node_types.items() if t == NodeType.MICROSCOPE]
        hpcs = [n for n, t in self.node_types.items() if t == NodeType.HPC]
        storages = [n for n, t in self.node_types.items() if t == NodeType.STORAGE]
        analysis_nodes = [n for n, t in self.node_types.items() if t == NodeType.ANALYSIS]
        hubs = [n for n, t in self.node_types.items() if t == NodeType.FACILITY_HUB]

        # Workflow 1: Local microscope to HPC processing
        if microscopes and hpcs and storages:
            mic = random.choice(microscopes)
            facility = mic.split('_microscope_')[0]
            storage = f"{facility}_storage"
            hpc = f"{facility}_hpc"
            analysis = f"{facility}_analysis"

            if storage in self.graph and hpc in self.graph:
                sequences.extend([
                    {
                        'nodes': [mic],
                        'edges': [],
                        'title': f'{facility} - Data Acquisition',
                        'description': f'Microscope acquiring high-resolution images',
                        'action': 'ACQUIRE',
                        'details': '2048x2048 px, 16-bit, 4 channels'
                    },
                    {
                        'nodes': [mic, storage],
                        'edges': [(mic, f"{facility}_hub"), (f"{facility}_hub", storage)],
                        'title': f'{facility} - Data Transfer',
                        'description': f'Transferring 2.5 GB to storage',
                        'action': 'TRANSFER',
                        'details': f'{mic} → {storage}'
                    },
                    {
                        'nodes': [storage, hpc],
                        'edges': [(storage, f"{facility}_hub"), (f"{facility}_hub", hpc)],
                        'title': f'{facility} - HPC Processing',
                        'description': 'Running image segmentation pipeline',
                        'action': 'COMPUTE',
                        'details': 'Estimated time: 5 minutes'
                    },
                ])

                if analysis in self.graph:
                    sequences.append({
                        'nodes': [hpc, analysis],
                        'edges': [(hpc, f"{facility}_hub"), (f"{facility}_hub", analysis)],
                        'title': f'{facility} - Analysis',
                        'description': 'Extracting cellular features',
                        'action': 'ANALYZE',
                        'details': 'Cell count, morphology, intensity'
                    })

        # Workflow 2: Cross-facility collaboration
        if len(hubs) >= 2:
            hub1, hub2 = random.sample(hubs, 2)
            facility1 = hub1.replace('_hub', '')
            facility2 = hub2.replace('_hub', '')

            mic1 = f"{facility1}_microscope_1"
            storage2 = f"{facility2}_storage"

            if mic1 in self.graph and storage2 in self.graph:
                sequences.extend([
                    {
                        'nodes': [mic1],
                        'edges': [],
                        'title': f'Cross-Facility - Acquisition',
                        'description': f'{facility1} acquiring data for {facility2}',
                        'action': 'ACQUIRE',
                        'details': 'Coordinated experiment'
                    },
                    {
                        'nodes': [mic1, hub1],
                        'edges': [(mic1, hub1)],
                        'title': f'Local Hub - {facility1}',
                        'description': 'Data ready for inter-facility transfer',
                        'action': 'STAGE',
                        'details': 'Preparing for network transfer'
                    },
                    {
                        'nodes': [hub1, hub2],
                        'edges': [(hub1, hub2)],
                        'title': 'Inter-Facility Transfer',
                        'description': f'{facility1} → {facility2}',
                        'action': 'TRANSFER',
                        'details': 'Secure high-bandwidth link'
                    },
                    {
                        'nodes': [hub2, storage2],
                        'edges': [(hub2, storage2)],
                        'title': f'{facility2} - Receiving Data',
                        'description': 'Storing shared experimental data',
                        'action': 'STORE',
                        'details': f'Replication complete'
                    },
                ])

        # Workflow 3: Distributed HPC processing
        if len(hpcs) >= 2:
            hpc1, hpc2 = random.sample(hpcs, 2)
            facility1 = hpc1.replace('_hpc', '')
            facility2 = hpc2.replace('_hpc', '')

            sequences.extend([
                {
                    'nodes': [hpc1],
                    'edges': [],
                    'title': 'Distributed Computation - Part 1',
                    'description': f'{facility1} HPC processing dataset chunk 1',
                    'action': 'COMPUTE',
                    'details': '512 CPU cores active'
                },
                {
                    'nodes': [hpc1, hpc2],
                    'edges': [],
                    'title': 'Distributed Computation - Part 2',
                    'description': f'Parallel processing across {facility1} & {facility2}',
                    'action': 'COMPUTE',
                    'details': 'Combined 1024 cores'
                },
                {
                    'nodes': [hpc1, hpc2],
                    'edges': [],
                    'title': 'Synchronizing Results',
                    'description': 'Merging distributed computation results',
                    'action': 'SYNC',
                    'details': 'Aggregating outputs'
                },
            ])

        # Workflow 4: Active Learning Loop with Ryan (Human-in-the-loop)
        researchers = [n for n, t in self.node_types.items() if t == NodeType.RESEARCHER]
        ryan_nodes = [n for n in researchers if 'Ryan' in n or 'ryan' in n]

        if ryan_nodes and microscopes and storages and analysis_nodes:
            ryan = ryan_nodes[0]
            facility = ryan.split('_')[0]  # e.g., "Janelia_Ryan" -> "Janelia"

            # Find resources at Ryan's facility
            ryan_microscope = f"{facility}_microscope_1"
            ryan_storage = f"{facility}_storage"
            ryan_hub = f"{facility}_hub"

            # Find remote analysis (could be at another facility)
            remote_analysis = None
            for analysis in analysis_nodes:
                if not analysis.startswith(facility):
                    remote_analysis = analysis
                    break
            if not remote_analysis:
                remote_analysis = analysis_nodes[0] if analysis_nodes else None

            if ryan_microscope in self.graph and ryan_storage in self.graph and remote_analysis:
                remote_facility = remote_analysis.split('_')[0]
                remote_hub = f"{remote_facility}_hub"

                sequences.extend([
                    {
                        'nodes': [ryan],
                        'edges': [],
                        'title': 'Active Learning: Sample Preparation',
                        'description': 'Ryan preparing C. elegans sample at Janelia',
                        'action': 'PREPARE',
                        'details': 'Mounting worms on slide, optimizing conditions'
                    },
                    {
                        'nodes': [ryan, ryan_microscope],
                        'edges': [(ryan, ryan_microscope)],
                        'title': 'Active Learning: Sample Mounting',
                        'description': 'Ryan mounts C. elegans on microscope',
                        'action': 'MOUNT',
                        'details': 'Sample ready for imaging'
                    },
                    {
                        'nodes': [ryan_microscope],
                        'edges': [],
                        'title': 'Active Learning: Data Acquisition',
                        'description': 'Microscope imaging C. elegans neurons',
                        'action': 'ACQUIRE',
                        'details': 'Time-lapse: 100 frames, 10s intervals'
                    },
                    {
                        'nodes': [ryan_microscope, ryan_storage],
                        'edges': [(ryan_microscope, ryan_hub), (ryan_hub, ryan_storage)],
                        'title': 'Active Learning: Data Storage',
                        'description': 'Saving experimental data locally',
                        'action': 'STORE',
                        'details': '1.2 GB neuronal imaging data'
                    },
                    {
                        'nodes': [ryan_storage, remote_analysis],
                        'edges': [(ryan_storage, ryan_hub), (ryan_hub, remote_hub), (remote_hub, remote_analysis)],
                        'title': 'Active Learning: Remote Analysis',
                        'description': f'Sending data to {remote_facility} for analysis',
                        'action': 'TRANSFER',
                        'details': 'Cross-facility data transfer'
                    },
                    {
                        'nodes': [remote_analysis],
                        'edges': [],
                        'title': 'Active Learning: Feature Extraction',
                        'description': 'Analyzing neuronal activity patterns',
                        'action': 'ANALYZE',
                        'details': 'Detecting calcium transients, tracking neurons'
                    },
                    {
                        'nodes': [remote_analysis],
                        'edges': [],
                        'title': 'Active Learning: Hypothesis Generation',
                        'description': 'AI formulates new hypothesis from data',
                        'action': 'HYPOTHESIS',
                        'details': 'Hypothesis: Neuron AVA shows stress response'
                    },
                    {
                        'nodes': [remote_analysis, ryan],
                        'edges': [(remote_analysis, remote_hub), (remote_hub, ryan_hub), (ryan_hub, ryan)],
                        'title': 'Active Learning: Results to Ryan',
                        'description': 'Sending analysis results and hypothesis to Ryan',
                        'action': 'TRANSFER',
                        'details': 'Hypothesis + supporting data visualization'
                    },
                    {
                        'nodes': [ryan],
                        'edges': [],
                        'title': 'Active Learning: Human Feedback',
                        'description': 'Ryan reviews results and tweaks experiment',
                        'action': 'REVIEW',
                        'details': 'Decision: Test with stressor compound'
                    },
                    {
                        'nodes': [ryan, ryan_microscope],
                        'edges': [(ryan, ryan_microscope)],
                        'title': 'Active Learning: Iteration 2 - Sample Prep',
                        'description': 'Ryan prepares refined experiment based on AI insight',
                        'action': 'PREPARE',
                        'details': 'Adding stressor, mounting new sample'
                    },
                    {
                        'nodes': [ryan_microscope],
                        'edges': [],
                        'title': 'Active Learning: Iteration 2 - Imaging',
                        'description': 'Acquiring data for hypothesis validation',
                        'action': 'ACQUIRE',
                        'details': 'Testing AVA stress response hypothesis'
                    },
                ])

        # Add completion frame
        sequences.append({
            'nodes': [],
            'edges': [],
            'title': 'Workflow Complete',
            'description': 'All tasks completed successfully',
            'action': 'DONE',
            'details': 'Ready for next workflow'
        })

        return sequences

    def draw_action_log(self, current_step: Dict, upcoming_steps: List[Dict]):
        """Draw the action log panel showing current and upcoming actions."""
        self.ax_log.clear()
        self.ax_log.set_facecolor('#0d0d0d')
        self.ax_log.axis('off')

        y_position = 0.98

        # Title
        self.ax_log.text(0.5, y_position, 'WORKFLOW TIMELINE',
                        transform=self.ax_log.transAxes,
                        fontsize=14, fontweight='bold', color='#FFD700',
                        ha='center', va='top')
        y_position -= 0.05

        # Progress indicator
        total_steps = len(self.workflow_sequences) if self.workflow_sequences else 1
        current_step_num = (self.current_frame % total_steps) + 1
        progress_pct = (current_step_num / total_steps) * 100

        self.ax_log.text(0.5, y_position, f'Step {current_step_num} of {total_steps}',
                        transform=self.ax_log.transAxes,
                        fontsize=9, color='#AAAAAA',
                        ha='center', va='top')
        y_position -= 0.03

        # Progress bar
        bar_width = 0.8
        bar_start = 0.1
        bar_height = 0.015

        # Background bar
        self.ax_log.add_patch(plt.Rectangle((bar_start, y_position - bar_height),
                                            bar_width, bar_height,
                                            transform=self.ax_log.transAxes,
                                            facecolor='#2a2a2a', edgecolor='#444444',
                                            linewidth=1))
        # Progress fill
        self.ax_log.add_patch(plt.Rectangle((bar_start, y_position - bar_height),
                                            bar_width * (progress_pct / 100), bar_height,
                                            transform=self.ax_log.transAxes,
                                            facecolor='#FFD700', edgecolor='none'))

        y_position -= 0.05

        # Action type colors
        action_colors = {
            'ACQUIRE': '#4CAF50',
            'TRANSFER': '#2196F3',
            'COMPUTE': '#FF9800',
            'ANALYZE': '#9C27B0',
            'STORE': '#FF9800',
            'STAGE': '#FFD700',
            'SYNC': '#00BCD4',
            'DONE': '#888888',
            'PREPARE': '#00BCD4',
            'MOUNT': '#4CAF50',
            'HYPOTHESIS': '#E91E63',
            'REVIEW': '#9C27B0'
        }

        # === CURRENT ACTION (Prominent Card) ===
        card_top = y_position
        card_height = 0.18

        # Draw card background
        self.ax_log.add_patch(plt.Rectangle((0.05, card_top - card_height),
                                            0.9, card_height,
                                            transform=self.ax_log.transAxes,
                                            facecolor='#1a1a1a', edgecolor='#FFD700',
                                            linewidth=2, alpha=0.9))

        y_position -= 0.02

        action = current_step.get('action', 'UNKNOWN')
        action_color = action_colors.get(action, '#FFFFFF')

        # Action badge and title on same line
        self.ax_log.text(0.08, y_position, '● NOW',
                        transform=self.ax_log.transAxes,
                        fontsize=10, fontweight='bold', color='#FFD700',
                        ha='left', va='top')

        bbox_props = dict(boxstyle='round,pad=0.3', facecolor=action_color, alpha=1.0)
        self.ax_log.text(0.20, y_position, f' {action} ',
                        transform=self.ax_log.transAxes,
                        fontsize=8, fontweight='bold', color='white',
                        ha='left', va='top', bbox=bbox_props)
        y_position -= 0.045

        # Description
        description = current_step.get('description', '')
        words = description.split()
        lines = []
        current_line = []
        for word in words:
            current_line.append(word)
            if len(' '.join(current_line)) > 28:
                lines.append(' '.join(current_line[:-1]))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))

        for line in lines[:2]:  # Max 2 lines
            self.ax_log.text(0.08, y_position, line,
                            transform=self.ax_log.transAxes,
                            fontsize=10, color='#FFFFFF', fontweight='bold',
                            ha='left', va='top')
            y_position -= 0.035

        # Details
        details = current_step.get('details', '')
        self.ax_log.text(0.08, y_position, f'{details}',
                        transform=self.ax_log.transAxes,
                        fontsize=8, color='#AAAAAA', style='italic',
                        ha='left', va='top')

        y_position = card_top - card_height - 0.04

        # === UPCOMING TIMELINE ===
        self.ax_log.text(0.05, y_position, '▼ NEXT STEPS',
                        transform=self.ax_log.transAxes,
                        fontsize=10, fontweight='bold', color='#888888',
                        ha='left', va='top')
        y_position -= 0.04

        # Timeline line
        timeline_x = 0.08
        timeline_start_y = y_position

        # Show next 3 upcoming actions in timeline format
        for i, step in enumerate(upcoming_steps[:3]):
            if y_position < 0.40:
                break

            action = step.get('action', 'UNKNOWN')
            action_color = action_colors.get(action, '#666666')
            title = step.get('title', 'Unknown')

            # Truncate long titles
            if len(title) > 32:
                title = title[:29] + '...'

            # Timeline dot
            self.ax_log.plot([timeline_x], [y_position],
                           'o', markersize=6, color='#555555',
                           transform=self.ax_log.transAxes)

            # Action badge (compact)
            self.ax_log.text(0.12, y_position + 0.005, f'{action}',
                            transform=self.ax_log.transAxes,
                            fontsize=7, color=action_color, fontweight='bold',
                            ha='left', va='center')

            # Title
            self.ax_log.text(0.12, y_position - 0.015, title,
                            transform=self.ax_log.transAxes,
                            fontsize=7, color='#AAAAAA',
                            ha='left', va='top')
            y_position -= 0.06

        # Timeline line connecting dots
        if len(upcoming_steps) > 0:
            self.ax_log.plot([timeline_x, timeline_x],
                           [timeline_start_y, y_position + 0.03],
                           '-', linewidth=2, color='#333333',
                           transform=self.ax_log.transAxes)

        y_position -= 0.04

        # === COMPLETED HISTORY ===
        self.ax_log.plot([0.05, 0.95], [y_position, y_position],
                        transform=self.ax_log.transAxes,
                        color='#333333', linewidth=1)
        y_position -= 0.03

        self.ax_log.text(0.05, y_position, '▲ COMPLETED',
                        transform=self.ax_log.transAxes,
                        fontsize=10, fontweight='bold', color='#555555',
                        ha='left', va='top')
        y_position -= 0.04

        # Show recent history in reverse chronological order (most recent first)
        recent_history = self.action_history[-6:][::-1]  # Last 6, reversed

        history_timeline_x = 0.08
        for i, step in enumerate(recent_history):
            if y_position < 0.05:
                break

            action = step.get('action', 'UNKNOWN')
            action_color = action_colors.get(action, '#444444')
            title = step.get('title', 'Unknown')

            # Truncate long titles
            if len(title) > 32:
                title = title[:29] + '...'

            # Checkmark dot
            self.ax_log.plot([history_timeline_x], [y_position],
                           'o', markersize=4, color='#2a5a2a',
                           transform=self.ax_log.transAxes)

            # Compact display
            self.ax_log.text(0.12, y_position + 0.002, f'✓ {title}',
                            transform=self.ax_log.transAxes,
                            fontsize=7, color='#666666',
                            ha='left', va='center')
            y_position -= 0.035

    def draw_network(self, active_nodes: Set[str], active_edges: Set[Tuple], title: str = ''):
        """Draw the network with highlighted active nodes and edges."""
        self.ax_network.clear()
        self.ax_network.set_facecolor('#1a1a1a')
        self.ax_network.axis('off')

        # Draw edges (inactive)
        inactive_edges = [(u, v) for u, v in self.graph.edges() if (u, v) not in active_edges and (v, u) not in active_edges]
        nx.draw_networkx_edges(self.graph, self.pos, edgelist=inactive_edges,
                              edge_color='#444444', width=1.5, alpha=0.3, ax=self.ax_network)

        # Draw active edges with glow effect
        if active_edges:
            nx.draw_networkx_edges(self.graph, self.pos, edgelist=list(active_edges),
                                  edge_color='#FFD700', width=4, alpha=0.9, ax=self.ax_network)

        # Draw nodes by type
        for node_type, style in NODE_STYLES.items():
            # Get nodes of this type
            nodes_of_type = [n for n, t in self.node_types.items() if t == node_type]

            # Split into active and inactive
            inactive = [n for n in nodes_of_type if n not in active_nodes]
            active = [n for n in nodes_of_type if n in active_nodes]

            # Draw inactive nodes
            if inactive:
                nx.draw_networkx_nodes(self.graph, self.pos, nodelist=inactive,
                                      node_color=style.color, node_shape=style.shape,
                                      node_size=style.size, alpha=0.4, ax=self.ax_network)

            # Draw active nodes with glow
            if active:
                # Outer glow
                nx.draw_networkx_nodes(self.graph, self.pos, nodelist=active,
                                      node_color='#FFFFFF', node_shape=style.shape,
                                      node_size=style.size * 1.5, alpha=0.3, ax=self.ax_network)
                # Main node
                nx.draw_networkx_nodes(self.graph, self.pos, nodelist=active,
                                      node_color=style.color, node_shape=style.shape,
                                      node_size=style.size, alpha=1.0, ax=self.ax_network,
                                      edgecolors='#FFFFFF', linewidths=3)

        # Draw labels for active nodes
        if active_nodes:
            active_labels = {n: n.split('_')[-1] if '_' in n else n for n in active_nodes}
            nx.draw_networkx_labels(self.graph, self.pos, labels=active_labels,
                                   font_size=8, font_color='white', ax=self.ax_network)

        # Add title
        if title:
            self.ax_network.text(0.5, 0.98, title, transform=self.ax_network.transAxes,
                        fontsize=16, color='white', ha='center', va='top',
                        bbox=dict(boxstyle='round', facecolor='#333333', alpha=0.8))

        # Add legend
        legend_elements = []
        for node_type, style in NODE_STYLES.items():
            legend_elements.append(plt.scatter([], [], c=style.color, marker=style.shape,
                                              s=100, label=style.label, edgecolors='white'))

        self.ax_network.legend(handles=legend_elements, loc='upper left',
                      framealpha=0.8, facecolor='#333333', edgecolor='white',
                      labelcolor='white', fontsize=10)

        # Add frame counter
        self.ax_network.text(0.02, 0.02, f'Frame: {self.current_frame}',
                    transform=self.ax_network.transAxes, fontsize=10,
                    color='#888888', ha='left', va='bottom')

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
            # Add the completed workflow to history before generating new one
            if self.workflow_sequences:
                self.action_history.extend(self.workflow_sequences)
                # Keep only recent history
                self.action_history = self.action_history[-self.max_history:]

            self.workflow_sequences = self.create_workflow_sequence()
            step = self.workflow_sequences[0]

        # Add previous step to history if moving to new step
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

    def run(self, frames=200, interval=800, save_gif=False, filename='workflow_animation.gif'):
        """Run the animation."""
        anim = animation.FuncAnimation(self.fig, self.animate_frame,
                                      frames=frames, interval=interval,
                                      repeat=True)

        if save_gif:
            print(f"Saving animation to {filename}...")
            writer = animation.PillowWriter(fps=1000//interval)
            anim.save(filename, writer=writer)
            print(f"Animation saved!")

        plt.tight_layout(pad=1.0)
        plt.subplots_adjust(wspace=0.05)
        plt.show()

        return anim


def create_example_network():
    """Create an example distributed workflow network."""
    workflow = DistributedWorkflowGraph()

    # Add multiple facilities
    workflow.add_facility("MIT", num_microscopes=4, has_hpc=True, has_storage=True, has_analysis=True)
    workflow.add_facility("Stanford", num_microscopes=3, has_hpc=True, has_storage=True, has_analysis=True)
    workflow.add_facility("Berkeley", num_microscopes=2, has_hpc=True, has_storage=True, has_analysis=False)
    # Janelia with Ryan - C. elegans researcher
    workflow.add_facility("Janelia", num_microscopes=5, has_hpc=True, has_storage=True, has_analysis=True,
                         researchers=["Ryan"])
    workflow.add_facility("EMBL", num_microscopes=3, has_hpc=False, has_storage=True, has_analysis=True)

    # Connect facilities
    workflow.connect_facilities("MIT", "Stanford")
    workflow.connect_facilities("Stanford", "Berkeley")
    workflow.connect_facilities("Berkeley", "Janelia")
    workflow.connect_facilities("Janelia", "EMBL")
    workflow.connect_facilities("MIT", "Janelia")
    workflow.connect_facilities("Stanford", "EMBL")

    return workflow


def main():
    """Main entry point for the animation."""
    print("=== Distributed Scientific Workflow Animation ===\n")
    print("Creating network topology...")

    # Create the network
    workflow = create_example_network()

    print(f"Network created with {workflow.graph.number_of_nodes()} nodes "
          f"and {workflow.graph.number_of_edges()} edges")
    print(f"Facilities: {', '.join(workflow.facilities.keys())}\n")

    # Create animator
    animator = WorkflowAnimator(workflow)

    print("Starting animation...")
    print("Close the window to exit.\n")

    # Run animation (set save_gif=True to save as GIF)
    # interval: milliseconds between frames (1500ms = 1.5 seconds per step)
    animator.run(frames=200, interval=1500, save_gif=False)


if __name__ == "__main__":
    main()
