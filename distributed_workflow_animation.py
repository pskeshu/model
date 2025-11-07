#!/usr/bin/env python3
"""
Distributed Scientific Workflow Animation

Visualizes a network of microscopes, HPC resources, and other scientific
facilities communicating in a distributed workflow system.
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
import numpy as np
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
from enum import Enum
import random


class NodeType(Enum):
    """Types of nodes in the distributed workflow."""
    MICROSCOPE = "microscope"
    HPC = "hpc"
    STORAGE = "storage"
    ANALYSIS = "analysis"
    FACILITY_HUB = "facility_hub"


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
                     has_analysis: bool = True):
        """Add a complete facility with its resources."""

        facility_nodes = []

        # Add facility hub
        hub_id = f"{facility_name}_hub"
        self.graph.add_node(hub_id)
        self.node_types[hub_id] = NodeType.FACILITY_HUB
        facility_nodes.append(hub_id)

        # Add microscopes
        for i in range(num_microscopes):
            microscope_id = f"{facility_name}_microscope_{i+1}"
            self.graph.add_node(microscope_id)
            self.node_types[microscope_id] = NodeType.MICROSCOPE
            self.graph.add_edge(hub_id, microscope_id)
            facility_nodes.append(microscope_id)

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

        # Setup figure
        self.fig, self.ax = plt.subplots(figsize=(16, 12))
        self.fig.patch.set_facecolor('#1a1a1a')
        self.ax.set_facecolor('#1a1a1a')

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

            if storage in self.graph and hpc in self.graph:
                sequences.extend([
                    {'nodes': [mic], 'edges': [], 'title': 'Microscope acquiring data'},
                    {'nodes': [mic, storage], 'edges': [(mic, f"{facility}_hub"), (f"{facility}_hub", storage)],
                     'title': 'Transferring to storage'},
                    {'nodes': [storage, hpc], 'edges': [(storage, f"{facility}_hub"), (f"{facility}_hub", hpc)],
                     'title': 'HPC processing data'},
                ])

        # Workflow 2: Cross-facility collaboration
        if len(hubs) >= 2:
            hub1, hub2 = random.sample(hubs, 2)
            facility1 = hub1.replace('_hub', '')
            facility2 = hub2.replace('_hub', '')

            mic1 = f"{facility1}_microscope_1"
            mic2 = f"{facility2}_microscope_1"

            if mic1 in self.graph and mic2 in self.graph:
                sequences.extend([
                    {'nodes': [mic1], 'edges': [], 'title': f'Data from {facility1}'},
                    {'nodes': [mic1, hub1], 'edges': [(mic1, hub1)], 'title': 'Sending to facility hub'},
                    {'nodes': [hub1, hub2], 'edges': [(hub1, hub2)], 'title': 'Cross-facility transfer'},
                    {'nodes': [hub2, mic2], 'edges': [(hub2, mic2)], 'title': f'Coordinating with {facility2}'},
                ])

        # Workflow 3: Distributed HPC processing
        if len(hpcs) >= 2:
            hpc1, hpc2 = random.sample(hpcs, 2)
            sequences.extend([
                {'nodes': [hpc1], 'edges': [], 'title': 'HPC 1 processing'},
                {'nodes': [hpc1, hpc2], 'edges': [], 'title': 'Distributed computation'},
            ])

        # Add some pause frames
        sequences.append({'nodes': [], 'edges': [], 'title': 'Workflow complete'})

        return sequences

    def draw_network(self, active_nodes: Set[str], active_edges: Set[Tuple], title: str = ''):
        """Draw the network with highlighted active nodes and edges."""
        self.ax.clear()
        self.ax.set_facecolor('#1a1a1a')
        self.ax.axis('off')

        # Draw edges (inactive)
        inactive_edges = [(u, v) for u, v in self.graph.edges() if (u, v) not in active_edges and (v, u) not in active_edges]
        nx.draw_networkx_edges(self.graph, self.pos, edgelist=inactive_edges,
                              edge_color='#444444', width=1.5, alpha=0.3, ax=self.ax)

        # Draw active edges with glow effect
        if active_edges:
            nx.draw_networkx_edges(self.graph, self.pos, edgelist=list(active_edges),
                                  edge_color='#FFD700', width=4, alpha=0.9, ax=self.ax)

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
                                      node_size=style.size, alpha=0.4, ax=self.ax)

            # Draw active nodes with glow
            if active:
                # Outer glow
                nx.draw_networkx_nodes(self.graph, self.pos, nodelist=active,
                                      node_color='#FFFFFF', node_shape=style.shape,
                                      node_size=style.size * 1.5, alpha=0.3, ax=self.ax)
                # Main node
                nx.draw_networkx_nodes(self.graph, self.pos, nodelist=active,
                                      node_color=style.color, node_shape=style.shape,
                                      node_size=style.size, alpha=1.0, ax=self.ax,
                                      edgecolors='#FFFFFF', linewidths=3)

        # Draw labels for active nodes
        if active_nodes:
            active_labels = {n: n.split('_')[-1] if '_' in n else n for n in active_nodes}
            nx.draw_networkx_labels(self.graph, self.pos, labels=active_labels,
                                   font_size=8, font_color='white', ax=self.ax)

        # Add title
        if title:
            self.ax.text(0.5, 0.98, title, transform=self.ax.transAxes,
                        fontsize=16, color='white', ha='center', va='top',
                        bbox=dict(boxstyle='round', facecolor='#333333', alpha=0.8))

        # Add legend
        legend_elements = []
        for node_type, style in NODE_STYLES.items():
            legend_elements.append(plt.scatter([], [], c=style.color, marker=style.shape,
                                              s=100, label=style.label, edgecolors='white'))

        self.ax.legend(handles=legend_elements, loc='upper left',
                      framealpha=0.8, facecolor='#333333', edgecolor='white',
                      labelcolor='white', fontsize=10)

        # Add frame counter
        self.ax.text(0.02, 0.02, f'Frame: {self.current_frame}',
                    transform=self.ax.transAxes, fontsize=10,
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
            self.workflow_sequences = self.create_workflow_sequence()
            step = self.workflow_sequences[0]

        self.draw_network(set(step['nodes']), set(step['edges']), step['title'])

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

        plt.tight_layout()
        plt.show()

        return anim


def create_example_network():
    """Create an example distributed workflow network."""
    workflow = DistributedWorkflowGraph()

    # Add multiple facilities
    workflow.add_facility("MIT", num_microscopes=4, has_hpc=True, has_storage=True, has_analysis=True)
    workflow.add_facility("Stanford", num_microscopes=3, has_hpc=True, has_storage=True, has_analysis=True)
    workflow.add_facility("Berkeley", num_microscopes=2, has_hpc=True, has_storage=True, has_analysis=False)
    workflow.add_facility("Janelia", num_microscopes=5, has_hpc=True, has_storage=True, has_analysis=True)
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
    animator.run(frames=200, interval=800, save_gif=False)


if __name__ == "__main__":
    main()
