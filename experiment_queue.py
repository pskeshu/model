#!/usr/bin/env python3
"""
Experiment Job Queue Management System

Manages imaging experiment requests from researchers worldwide,
enabling reviewers to approve/reject experiments for specific microscope systems.
"""

import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum
from pathlib import Path


class RequestStatus(Enum):
    """Status states for experiment requests"""
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class MicroscopeSystem(Enum):
    """Available microscope systems"""
    DISPIM = "DiSPIM"
    CONFOCAL = "confocal"
    WIDEFIELD = "widefield"
    LIGHT_SHEET = "light_sheet"
    TWO_PHOTON = "two_photon"
    SUPER_RESOLUTION = "super_resolution"


class Priority(Enum):
    """Priority levels for experiment requests"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class ExperimentRequest:
    """
    Represents a single experiment request with approval workflow.
    Extends Sample_Spec with request metadata and status tracking.
    """

    def __init__(
        self,
        sample_spec: Dict[str, Any],
        requester_name: str,
        requester_email: str,
        requester_institution: str,
        microscope_system: str,
        scientific_rationale: str,
        priority: str = "medium",
        request_id: Optional[str] = None,
        submission_date: Optional[str] = None,
        status: str = "submitted"
    ):
        self.request_id = request_id or str(uuid.uuid4())
        self.submission_date = submission_date or datetime.utcnow().isoformat()
        self.status = RequestStatus(status)

        # Requester information
        self.requester_name = requester_name
        self.requester_email = requester_email
        self.requester_institution = requester_institution

        # Experiment details
        self.sample_spec = sample_spec
        self.microscope_system = MicroscopeSystem(microscope_system)
        self.scientific_rationale = scientific_rationale
        self.priority = Priority(priority)

        # Approval workflow
        self.reviewer_name: Optional[str] = None
        self.reviewer_comments: Optional[str] = None
        self.review_date: Optional[str] = None

        # Execution tracking
        self.scheduled_date: Optional[str] = None
        self.completion_date: Optional[str] = None
        self.results_location: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert request to dictionary for serialization"""
        return {
            "request_id": self.request_id,
            "submission_date": self.submission_date,
            "status": self.status.value,
            "requester": {
                "name": self.requester_name,
                "email": self.requester_email,
                "institution": self.requester_institution
            },
            "experiment": {
                "sample_spec": self.sample_spec,
                "microscope_system": self.microscope_system.value,
                "scientific_rationale": self.scientific_rationale,
                "priority": self.priority.value
            },
            "review": {
                "reviewer_name": self.reviewer_name,
                "reviewer_comments": self.reviewer_comments,
                "review_date": self.review_date
            },
            "execution": {
                "scheduled_date": self.scheduled_date,
                "completion_date": self.completion_date,
                "results_location": self.results_location
            }
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ExperimentRequest':
        """Create ExperimentRequest from dictionary"""
        req = cls(
            sample_spec=data["experiment"]["sample_spec"],
            requester_name=data["requester"]["name"],
            requester_email=data["requester"]["email"],
            requester_institution=data["requester"]["institution"],
            microscope_system=data["experiment"]["microscope_system"],
            scientific_rationale=data["experiment"]["scientific_rationale"],
            priority=data["experiment"]["priority"],
            request_id=data["request_id"],
            submission_date=data["submission_date"],
            status=data["status"]
        )

        # Restore review information
        req.reviewer_name = data["review"]["reviewer_name"]
        req.reviewer_comments = data["review"]["reviewer_comments"]
        req.review_date = data["review"]["review_date"]

        # Restore execution information
        req.scheduled_date = data["execution"]["scheduled_date"]
        req.completion_date = data["execution"]["completion_date"]
        req.results_location = data["execution"]["results_location"]

        return req


class JobQueue:
    """
    Manages the queue of experiment requests with approval workflow.
    Provides methods for submission, review, and status tracking.
    """

    def __init__(self, storage_path: str = "experiment_queue.json"):
        self.storage_path = Path(storage_path)
        self.requests: Dict[str, ExperimentRequest] = {}
        self._load()

    def _load(self):
        """Load requests from persistent storage"""
        if self.storage_path.exists():
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                for req_data in data.get("requests", []):
                    req = ExperimentRequest.from_dict(req_data)
                    self.requests[req.request_id] = req

    def _save(self):
        """Save requests to persistent storage"""
        data = {
            "last_updated": datetime.utcnow().isoformat(),
            "requests": [req.to_dict() for req in self.requests.values()]
        }
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)

    def submit_request(
        self,
        sample_spec: Dict[str, Any],
        requester_name: str,
        requester_email: str,
        requester_institution: str,
        microscope_system: str,
        scientific_rationale: str,
        priority: str = "medium"
    ) -> str:
        """
        Submit a new experiment request to the queue.

        Returns:
            request_id: Unique identifier for the submitted request
        """
        request = ExperimentRequest(
            sample_spec=sample_spec,
            requester_name=requester_name,
            requester_email=requester_email,
            requester_institution=requester_institution,
            microscope_system=microscope_system,
            scientific_rationale=scientific_rationale,
            priority=priority
        )

        self.requests[request.request_id] = request
        self._save()

        return request.request_id

    def get_request(self, request_id: str) -> Optional[ExperimentRequest]:
        """Retrieve a specific request by ID"""
        return self.requests.get(request_id)

    def list_requests(
        self,
        status: Optional[str] = None,
        microscope_system: Optional[str] = None,
        priority: Optional[str] = None,
        requester_email: Optional[str] = None
    ) -> List[ExperimentRequest]:
        """
        List requests with optional filtering.

        Args:
            status: Filter by request status
            microscope_system: Filter by microscope system
            priority: Filter by priority level
            requester_email: Filter by requester email

        Returns:
            List of matching experiment requests
        """
        results = list(self.requests.values())

        if status:
            status_enum = RequestStatus(status)
            results = [r for r in results if r.status == status_enum]

        if microscope_system:
            system_enum = MicroscopeSystem(microscope_system)
            results = [r for r in results if r.microscope_system == system_enum]

        if priority:
            priority_enum = Priority(priority)
            results = [r for r in results if r.priority == priority_enum]

        if requester_email:
            results = [r for r in results if r.requester_email == requester_email]

        # Sort by priority (urgent first) and submission date
        priority_order = {"urgent": 0, "high": 1, "medium": 2, "low": 3}
        results.sort(
            key=lambda r: (priority_order[r.priority.value], r.submission_date)
        )

        return results

    def approve_request(
        self,
        request_id: str,
        reviewer_name: str,
        reviewer_comments: str = "",
        scheduled_date: Optional[str] = None
    ) -> bool:
        """
        Approve an experiment request.

        Args:
            request_id: ID of the request to approve
            reviewer_name: Name of the person approving
            reviewer_comments: Optional comments from reviewer
            scheduled_date: Optional scheduled execution date

        Returns:
            True if successful, False if request not found
        """
        request = self.requests.get(request_id)
        if not request:
            return False

        request.status = RequestStatus.APPROVED
        request.reviewer_name = reviewer_name
        request.reviewer_comments = reviewer_comments
        request.review_date = datetime.utcnow().isoformat()
        request.scheduled_date = scheduled_date

        self._save()
        return True

    def reject_request(
        self,
        request_id: str,
        reviewer_name: str,
        reviewer_comments: str
    ) -> bool:
        """
        Reject an experiment request.

        Args:
            request_id: ID of the request to reject
            reviewer_name: Name of the person rejecting
            reviewer_comments: Reason for rejection

        Returns:
            True if successful, False if request not found
        """
        request = self.requests.get(request_id)
        if not request:
            return False

        request.status = RequestStatus.REJECTED
        request.reviewer_name = reviewer_name
        request.reviewer_comments = reviewer_comments
        request.review_date = datetime.utcnow().isoformat()

        self._save()
        return True

    def update_status(
        self,
        request_id: str,
        new_status: str,
        results_location: Optional[str] = None
    ) -> bool:
        """
        Update the status of an experiment request.

        Args:
            request_id: ID of the request to update
            new_status: New status value
            results_location: Optional path to results (for completed experiments)

        Returns:
            True if successful, False if request not found
        """
        request = self.requests.get(request_id)
        if not request:
            return False

        request.status = RequestStatus(new_status)

        if new_status == "in_progress":
            # Experiment has started
            pass
        elif new_status == "completed":
            request.completion_date = datetime.utcnow().isoformat()
            if results_location:
                request.results_location = results_location

        self._save()
        return True

    def get_pending_for_review(self, microscope_system: Optional[str] = None) -> List[ExperimentRequest]:
        """
        Get all requests pending review/approval.

        Args:
            microscope_system: Optional filter for specific microscope system

        Returns:
            List of requests awaiting review
        """
        return self.list_requests(
            status="submitted",
            microscope_system=microscope_system
        )

    def get_approved_queue(self, microscope_system: Optional[str] = None) -> List[ExperimentRequest]:
        """
        Get all approved requests waiting to be executed.

        Args:
            microscope_system: Optional filter for specific microscope system

        Returns:
            List of approved requests
        """
        return self.list_requests(
            status="approved",
            microscope_system=microscope_system
        )

    def get_stats(self) -> Dict[str, Any]:
        """
        Get queue statistics.

        Returns:
            Dictionary with queue statistics
        """
        stats = {
            "total_requests": len(self.requests),
            "by_status": {},
            "by_microscope": {},
            "by_priority": {}
        }

        for request in self.requests.values():
            # Count by status
            status_key = request.status.value
            stats["by_status"][status_key] = stats["by_status"].get(status_key, 0) + 1

            # Count by microscope
            microscope_key = request.microscope_system.value
            stats["by_microscope"][microscope_key] = stats["by_microscope"].get(microscope_key, 0) + 1

            # Count by priority
            priority_key = request.priority.value
            stats["by_priority"][priority_key] = stats["by_priority"].get(priority_key, 0) + 1

        return stats


def main():
    """Example usage of the job queue system"""
    print("=== Experiment Job Queue System ===\n")

    # Initialize queue
    queue = JobQueue("experiment_queue.json")

    # Example 1: Submit a DiSPIM experiment request
    print("1. Submitting a DiSPIM experiment request...")

    sample_spec = {
        "sample_id": "dispim_zebrafish_001",
        "schema_version": "1.0.0",
        "biological_context": {
            "cell_line": "zebrafish_embryo",
            "developmental_stage": "24hpf",
            "specimen_type": "whole_organism"
        },
        "imaging_parameters": {
            "microscope_type": "light_sheet",
            "objective_magnification": 20,
            "channels": [
                {"name": "GFP", "excitation": 488, "emission": 519},
                {"name": "mCherry", "excitation": 561, "emission": 610}
            ],
            "time_lapse": {
                "enabled": True,
                "interval": 120,  # 2 minutes
                "duration": 43200  # 12 hours
            }
        }
    }

    request_id = queue.submit_request(
        sample_spec=sample_spec,
        requester_name="Dr. Sarah Johnson",
        requester_email="sjohnson@university.edu",
        requester_institution="University of Biology",
        microscope_system="DiSPIM",
        scientific_rationale="Study neural crest cell migration during zebrafish development. "
                            "DiSPIM provides the necessary speed and resolution for tracking "
                            "individual cell movements over extended time periods.",
        priority="high"
    )

    print(f"   Request submitted with ID: {request_id}\n")

    # Example 2: List pending requests for DiSPIM
    print("2. Listing pending DiSPIM requests for Ryan to review...")
    pending = queue.get_pending_for_review(microscope_system="DiSPIM")

    for req in pending:
        print(f"   Request ID: {req.request_id}")
        print(f"   Requester: {req.requester_name} ({req.requester_institution})")
        print(f"   Priority: {req.priority.value}")
        print(f"   Sample: {req.sample_spec.get('sample_id', 'N/A')}")
        print(f"   Rationale: {req.scientific_rationale[:100]}...")
        print()

    # Example 3: Ryan approves the request
    print("3. Ryan approves the DiSPIM experiment...")
    success = queue.approve_request(
        request_id=request_id,
        reviewer_name="Ryan",
        reviewer_comments="Excellent use case for DiSPIM. Approved for next week's imaging session.",
        scheduled_date="2025-11-17T09:00:00"
    )

    if success:
        print("   ✓ Request approved\n")

    # Example 4: Check approved queue
    print("4. Checking approved DiSPIM experiments...")
    approved = queue.get_approved_queue(microscope_system="DiSPIM")

    for req in approved:
        print(f"   Request ID: {req.request_id}")
        print(f"   Scheduled: {req.scheduled_date}")
        print(f"   Reviewer: {req.reviewer_name}")
        print(f"   Comments: {req.reviewer_comments}")
        print()

    # Example 5: Update status when experiment starts
    print("5. Experiment execution workflow...")
    queue.update_status(request_id, "in_progress")
    print("   ✓ Experiment marked as in_progress")

    # Simulate experiment completion
    queue.update_status(
        request_id,
        "completed",
        results_location="/data/dispim/zebrafish_001_results/"
    )
    print("   ✓ Experiment completed\n")

    # Example 6: View queue statistics
    print("6. Queue statistics:")
    stats = queue.get_stats()
    print(f"   Total requests: {stats['total_requests']}")
    print(f"   By status: {stats['by_status']}")
    print(f"   By microscope: {stats['by_microscope']}")
    print(f"   By priority: {stats['by_priority']}")


if __name__ == "__main__":
    main()
