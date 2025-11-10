#!/usr/bin/env python3
"""
Example client script for submitting experiments to the global queue.

This script demonstrates how researchers worldwide can submit imaging
experiments to the global experiment queue system.
"""

import requests
import json
from typing import Dict, Any, Optional
import sys


class ExperimentClient:
    """
    Client for interacting with the Global Experiment Queue API.
    """

    def __init__(self, api_base_url: str = "http://localhost:5000/api/v1"):
        self.api_base_url = api_base_url

    def submit_experiment(
        self,
        sample_spec: Dict[str, Any],
        requester_name: str,
        requester_email: str,
        requester_institution: str,
        microscope_system: str,
        scientific_rationale: str,
        priority: str = "medium"
    ) -> Optional[str]:
        """
        Submit an experiment request to the queue.

        Returns:
            request_id if successful, None otherwise
        """
        payload = {
            "sample_spec": sample_spec,
            "requester": {
                "name": requester_name,
                "email": requester_email,
                "institution": requester_institution
            },
            "experiment": {
                "microscope_system": microscope_system,
                "scientific_rationale": scientific_rationale,
                "priority": priority
            }
        }

        try:
            response = requests.post(
                f"{self.api_base_url}/experiments",
                json=payload,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 201:
                result = response.json()
                return result["request_id"]
            else:
                print(f"Error: {response.status_code}")
                print(response.json())
                return None

        except requests.exceptions.RequestException as e:
            print(f"Failed to submit experiment: {e}")
            return None

    def get_experiment_status(self, request_id: str) -> Optional[Dict[str, Any]]:
        """Get the current status of an experiment request"""
        try:
            response = requests.get(f"{self.api_base_url}/experiments/{request_id}")

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.status_code}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Failed to get status: {e}")
            return None

    def list_my_experiments(self, requester_email: str) -> Optional[list]:
        """List all experiments submitted by a requester"""
        try:
            response = requests.get(
                f"{self.api_base_url}/experiments",
                params={"requester": requester_email}
            )

            if response.status_code == 200:
                result = response.json()
                return result["experiments"]
            else:
                print(f"Error: {response.status_code}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Failed to list experiments: {e}")
            return None


def example_dispim_zebrafish():
    """
    Example 1: Submit a DiSPIM experiment for zebrafish developmental imaging.
    """
    print("=== Example 1: DiSPIM Zebrafish Developmental Imaging ===\n")

    # Initialize client
    client = ExperimentClient(api_base_url="http://localhost:5000/api/v1")

    # Define sample specification
    sample_spec = {
        "sample_id": "zebrafish_neural_crest_001",
        "schema_version": "1.0.0",
        "biological_context": {
            "cell_line": "zebrafish_embryo",
            "developmental_stage": "24hpf",
            "specimen_type": "whole_organism"
        },
        "culture_conditions": {
            "media_type": "E3_medium",
            "temperature_celsius": 28.5
        },
        "treatments": {
            "compounds": [],
            "physical_perturbations": []
        },
        "imaging_parameters": {
            "microscope_type": "light_sheet",
            "objective_magnification": 20,
            "numerical_aperture": 1.0,
            "channels": [
                {
                    "name": "GFP",
                    "excitation": 488,
                    "emission": 519,
                    "exposure_time": 50,
                    "intensity": 15
                },
                {
                    "name": "mCherry",
                    "excitation": 561,
                    "emission": 610,
                    "exposure_time": 100,
                    "intensity": 20
                }
            ],
            "z_stack": {
                "enabled": True,
                "step_size": 1.0,
                "num_planes": 200
            },
            "time_lapse": {
                "enabled": True,
                "interval": 120,  # 2 minutes
                "duration": 43200  # 12 hours
            }
        }
    }

    # Submit experiment
    request_id = client.submit_experiment(
        sample_spec=sample_spec,
        requester_name="Dr. Sarah Johnson",
        requester_email="sjohnson@university.edu",
        requester_institution="European Institute of Developmental Biology",
        microscope_system="DiSPIM",
        scientific_rationale=(
            "Study neural crest cell migration during zebrafish embryonic development. "
            "DiSPIM provides the necessary temporal resolution (2-minute intervals) and "
            "volumetric coverage (200 z-planes) to track individual cell movements over "
            "extended time periods (12 hours) while minimizing phototoxicity. "
            "The dual-view geometry is essential for accurate 3D tracking throughout the "
            "entire embryo without gaps in coverage."
        ),
        priority="high"
    )

    if request_id:
        print(f"✓ Experiment submitted successfully!")
        print(f"  Request ID: {request_id}")
        print(f"  Status: SUBMITTED")
        print(f"  You will receive an email when Ryan reviews your DiSPIM request.\n")
        return request_id
    else:
        print("✗ Failed to submit experiment\n")
        return None


def example_confocal_protein_localization():
    """
    Example 2: Submit a confocal microscopy experiment for protein localization.
    """
    print("=== Example 2: Confocal Protein Localization Study ===\n")

    client = ExperimentClient(api_base_url="http://localhost:5000/api/v1")

    sample_spec = {
        "sample_id": "hela_p53_localization_001",
        "schema_version": "1.0.0",
        "biological_context": {
            "cell_line": "HeLa",
            "passage_number": 15,
            "cell_density": 75000,
            "culture_age": 24
        },
        "culture_conditions": {
            "media_type": "DMEM",
            "media_supplements": ["10% FBS", "1% Pen/Strep"],
            "co2_percentage": 5,
            "temperature_celsius": 37
        },
        "treatments": {
            "compounds": [
                {
                    "name": "doxorubicin",
                    "concentration": 1,
                    "units": "µM",
                    "duration": 6,
                    "time_units": "hours"
                }
            ],
            "physical_perturbations": []
        },
        "sample_preparation": {
            "fixation_method": "paraformaldehyde",
            "fixation_duration": 15,
            "permeabilization": True,
            "blocking_agent": "5% goat_serum"
        },
        "staining_protocol": {
            "primary_antibodies": [
                {
                    "target": "p53",
                    "clone": "DO-1",
                    "concentration": 1,
                    "incubation_time": 60,
                    "temperature": 4
                }
            ],
            "secondary_antibodies": [
                {
                    "fluorophore": "Alexa488",
                    "concentration": 2,
                    "incubation_time": 45
                }
            ],
            "nuclear_stain": "DAPI"
        },
        "imaging_parameters": {
            "microscope_type": "confocal",
            "objective_magnification": 63,
            "numerical_aperture": 1.4,
            "channels": [
                {
                    "name": "DAPI",
                    "excitation": 405,
                    "emission": 450,
                    "exposure_time": 200,
                    "intensity": 2
                },
                {
                    "name": "Alexa488",
                    "excitation": 488,
                    "emission": 519,
                    "exposure_time": 500,
                    "intensity": 5
                }
            ],
            "z_stack": {
                "enabled": True,
                "step_size": 0.3,
                "num_planes": 30
            }
        }
    }

    request_id = client.submit_experiment(
        sample_spec=sample_spec,
        requester_name="Dr. Michael Chen",
        requester_email="mchen@researchlab.org",
        requester_institution="Institute of Cancer Research, Singapore",
        microscope_system="confocal",
        scientific_rationale=(
            "Investigate subcellular localization of p53 in response to DNA damage. "
            "High-resolution confocal imaging is required to distinguish nuclear vs. "
            "cytoplasmic localization and to identify potential aggregation patterns. "
            "Z-stack acquisition (30 planes, 0.3µm steps) ensures complete cellular "
            "coverage for accurate quantification of p53 distribution."
        ),
        priority="medium"
    )

    if request_id:
        print(f"✓ Experiment submitted successfully!")
        print(f"  Request ID: {request_id}")
        print(f"  Status: SUBMITTED\n")
        return request_id
    else:
        print("✗ Failed to submit experiment\n")
        return None


def check_experiment_status(client: ExperimentClient, request_id: str):
    """
    Example 3: Check the status of a submitted experiment.
    """
    print(f"=== Checking Status of Experiment {request_id} ===\n")

    status = client.get_experiment_status(request_id)

    if status:
        print(f"Request ID: {status['request_id']}")
        print(f"Status: {status['status'].upper()}")
        print(f"Submitted: {status['submission_date']}")
        print(f"Requester: {status['requester']['name']}")
        print(f"Institution: {status['requester']['institution']}")
        print(f"Microscope: {status['experiment']['microscope_system']}")
        print(f"Priority: {status['experiment']['priority'].upper()}")

        if status['status'] in ['approved', 'in_progress', 'completed']:
            print(f"\nReview Information:")
            print(f"  Reviewer: {status['review']['reviewer_name']}")
            print(f"  Comments: {status['review']['reviewer_comments']}")
            if status['execution']['scheduled_date']:
                print(f"  Scheduled: {status['execution']['scheduled_date']}")

        if status['status'] == 'completed':
            print(f"\nResults:")
            print(f"  Completed: {status['execution']['completion_date']}")
            print(f"  Location: {status['execution']['results_location']}")

        print()


def list_my_experiments(client: ExperimentClient, email: str):
    """
    Example 4: List all experiments submitted by a researcher.
    """
    print(f"=== Experiments for {email} ===\n")

    experiments = client.list_my_experiments(email)

    if experiments:
        print(f"Total experiments: {len(experiments)}\n")

        for exp in experiments:
            print(f"Request ID: {exp['request_id']}")
            print(f"  Status: {exp['status'].upper()}")
            print(f"  Microscope: {exp['experiment']['microscope_system']}")
            print(f"  Priority: {exp['experiment']['priority']}")
            print(f"  Submitted: {exp['submission_date']}")
            print()


def main():
    """
    Run example workflow: submit experiments and check status.
    """
    print("=" * 70)
    print("Global Experiment Queue - Client Examples")
    print("=" * 70)
    print()

    # Example 1: Submit DiSPIM experiment
    request_id_1 = example_dispim_zebrafish()

    # Example 2: Submit confocal experiment
    request_id_2 = example_confocal_protein_localization()

    # Example 3: Check status of first experiment
    if request_id_1:
        client = ExperimentClient(api_base_url="http://localhost:5000/api/v1")
        check_experiment_status(client, request_id_1)

        # Example 4: List all experiments for this researcher
        list_my_experiments(client, "sjohnson@university.edu")

    print("=" * 70)
    print("\nNext steps:")
    print("1. Reviewers will receive email notifications")
    print("2. You'll be notified when your experiments are reviewed")
    print("3. Check status anytime using the request ID")
    print("4. Access results when experiments are completed")
    print()


if __name__ == "__main__":
    # Check if API server is running
    try:
        response = requests.get("http://localhost:5000/api/v1/health")
        if response.status_code == 200:
            print("✓ API server is running\n")
            main()
        else:
            print("✗ API server returned unexpected status")
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("✗ Error: API server is not running")
        print("\nPlease start the server first:")
        print("  python api_server.py")
        print("\nOr if using gunicorn:")
        print("  gunicorn -w 4 -b 0.0.0.0:5000 api_server:app")
        sys.exit(1)
