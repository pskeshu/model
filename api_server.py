#!/usr/bin/env python3
"""
Global Experiment Queue API Server

RESTful API for worldwide biological scientists to submit and manage
imaging experiment requests. Supports multiple reviewers, institutions,
and microscope systems globally.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict, Any, Optional
import os
from experiment_queue import JobQueue, RequestStatus, MicroscopeSystem, Priority
from notifications import NotificationService
from datetime import datetime


app = Flask(__name__)
CORS(app)  # Enable cross-origin requests for global access

# Initialize global queue and notification service
queue = JobQueue(storage_path=os.getenv("QUEUE_STORAGE_PATH", "global_experiment_queue.json"))
notifications = NotificationService()


# ============================================================================
# Experiment Submission Endpoints
# ============================================================================

@app.route('/api/v1/experiments', methods=['POST'])
def submit_experiment():
    """
    Submit a new experiment request.

    POST /api/v1/experiments
    Body: {
        "sample_spec": {...},
        "requester": {
            "name": "Dr. Jane Smith",
            "email": "jsmith@university.edu",
            "institution": "University of Biology",
            "country": "USA"
        },
        "experiment": {
            "microscope_system": "DiSPIM",
            "scientific_rationale": "...",
            "priority": "medium"
        }
    }

    Returns: {
        "request_id": "uuid",
        "status": "submitted",
        "message": "Experiment request submitted successfully"
    }
    """
    try:
        data = request.json

        # Validate required fields
        required_fields = ['sample_spec', 'requester', 'experiment']
        if not all(field in data for field in required_fields):
            return jsonify({
                "error": "Missing required fields",
                "required": required_fields
            }), 400

        # Submit to queue
        request_id = queue.submit_request(
            sample_spec=data['sample_spec'],
            requester_name=data['requester']['name'],
            requester_email=data['requester']['email'],
            requester_institution=data['requester']['institution'],
            microscope_system=data['experiment']['microscope_system'],
            scientific_rationale=data['experiment']['scientific_rationale'],
            priority=data['experiment'].get('priority', 'medium')
        )

        # Notify reviewers of new submission
        notifications.notify_new_submission(
            request_id=request_id,
            microscope_system=data['experiment']['microscope_system'],
            requester_name=data['requester']['name'],
            priority=data['experiment'].get('priority', 'medium')
        )

        return jsonify({
            "request_id": request_id,
            "status": "submitted",
            "message": "Experiment request submitted successfully. You will be notified when reviewed."
        }), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@app.route('/api/v1/experiments/<request_id>', methods=['GET'])
def get_experiment(request_id: str):
    """
    Get details of a specific experiment request.

    GET /api/v1/experiments/{request_id}

    Returns: Full experiment request details
    """
    req = queue.get_request(request_id)

    if not req:
        return jsonify({"error": "Request not found"}), 404

    return jsonify(req.to_dict()), 200


@app.route('/api/v1/experiments', methods=['GET'])
def list_experiments():
    """
    List experiment requests with optional filtering.

    GET /api/v1/experiments?status=submitted&microscope=DiSPIM&priority=high

    Query parameters:
        - status: Filter by status (submitted, approved, rejected, etc.)
        - microscope: Filter by microscope system
        - priority: Filter by priority level
        - requester: Filter by requester email

    Returns: List of matching experiment requests
    """
    try:
        filters = {
            'status': request.args.get('status'),
            'microscope_system': request.args.get('microscope'),
            'priority': request.args.get('priority'),
            'requester_email': request.args.get('requester')
        }

        # Remove None values
        filters = {k: v for k, v in filters.items() if v is not None}

        results = queue.list_requests(**filters)

        return jsonify({
            "count": len(results),
            "experiments": [req.to_dict() for req in results]
        }), 200

    except ValueError as e:
        return jsonify({"error": f"Invalid filter value: {str(e)}"}), 400


# ============================================================================
# Reviewer Endpoints
# ============================================================================

@app.route('/api/v1/review/pending', methods=['GET'])
def get_pending_reviews():
    """
    Get all experiments pending review.

    GET /api/v1/review/pending?microscope=DiSPIM

    Query parameters:
        - microscope: Optional filter for specific microscope system

    Returns: List of experiments awaiting review
    """
    microscope = request.args.get('microscope')
    pending = queue.get_pending_for_review(microscope_system=microscope)

    return jsonify({
        "count": len(pending),
        "pending_reviews": [req.to_dict() for req in pending]
    }), 200


@app.route('/api/v1/review/<request_id>/approve', methods=['POST'])
def approve_experiment(request_id: str):
    """
    Approve an experiment request.

    POST /api/v1/review/{request_id}/approve
    Body: {
        "reviewer_name": "Ryan",
        "reviewer_comments": "Approved for DiSPIM",
        "scheduled_date": "2025-11-17T09:00:00"  (optional)
    }

    Returns: Success message
    """
    try:
        data = request.json

        if not data or 'reviewer_name' not in data:
            return jsonify({"error": "reviewer_name is required"}), 400

        success = queue.approve_request(
            request_id=request_id,
            reviewer_name=data['reviewer_name'],
            reviewer_comments=data.get('reviewer_comments', ''),
            scheduled_date=data.get('scheduled_date')
        )

        if not success:
            return jsonify({"error": "Request not found"}), 404

        # Notify requester of approval
        req = queue.get_request(request_id)
        if req:
            notifications.notify_approval(
                requester_email=req.requester_email,
                request_id=request_id,
                reviewer_name=data['reviewer_name'],
                scheduled_date=data.get('scheduled_date')
            )

        return jsonify({
            "message": "Experiment approved successfully",
            "request_id": request_id,
            "status": "approved"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/v1/review/<request_id>/reject', methods=['POST'])
def reject_experiment(request_id: str):
    """
    Reject an experiment request.

    POST /api/v1/review/{request_id}/reject
    Body: {
        "reviewer_name": "Ryan",
        "reviewer_comments": "Insufficient justification for DiSPIM usage"
    }

    Returns: Success message
    """
    try:
        data = request.json

        if not data or 'reviewer_name' not in data or 'reviewer_comments' not in data:
            return jsonify({
                "error": "reviewer_name and reviewer_comments are required"
            }), 400

        success = queue.reject_request(
            request_id=request_id,
            reviewer_name=data['reviewer_name'],
            reviewer_comments=data['reviewer_comments']
        )

        if not success:
            return jsonify({"error": "Request not found"}), 404

        # Notify requester of rejection
        req = queue.get_request(request_id)
        if req:
            notifications.notify_rejection(
                requester_email=req.requester_email,
                request_id=request_id,
                reviewer_name=data['reviewer_name'],
                reviewer_comments=data['reviewer_comments']
            )

        return jsonify({
            "message": "Experiment rejected",
            "request_id": request_id,
            "status": "rejected"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================================
# Execution Status Endpoints
# ============================================================================

@app.route('/api/v1/experiments/<request_id>/status', methods=['PUT'])
def update_experiment_status(request_id: str):
    """
    Update experiment execution status.

    PUT /api/v1/experiments/{request_id}/status
    Body: {
        "status": "in_progress" | "completed" | "cancelled",
        "results_location": "/path/to/results"  (optional, for completed)
    }

    Returns: Success message
    """
    try:
        data = request.json

        if not data or 'status' not in data:
            return jsonify({"error": "status is required"}), 400

        success = queue.update_status(
            request_id=request_id,
            new_status=data['status'],
            results_location=data.get('results_location')
        )

        if not success:
            return jsonify({"error": "Request not found"}), 404

        # Notify requester of status change
        req = queue.get_request(request_id)
        if req and data['status'] == 'completed':
            notifications.notify_completion(
                requester_email=req.requester_email,
                request_id=request_id,
                results_location=data.get('results_location')
            )

        return jsonify({
            "message": f"Status updated to {data['status']}",
            "request_id": request_id,
            "status": data['status']
        }), 200

    except ValueError as e:
        return jsonify({"error": f"Invalid status value: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/v1/queue/approved', methods=['GET'])
def get_approved_queue():
    """
    Get approved experiments waiting for execution.

    GET /api/v1/queue/approved?microscope=DiSPIM

    Query parameters:
        - microscope: Optional filter for specific microscope system

    Returns: List of approved experiments
    """
    microscope = request.args.get('microscope')
    approved = queue.get_approved_queue(microscope_system=microscope)

    return jsonify({
        "count": len(approved),
        "approved_experiments": [req.to_dict() for req in approved]
    }), 200


# ============================================================================
# Statistics and Monitoring
# ============================================================================

@app.route('/api/v1/stats', methods=['GET'])
def get_statistics():
    """
    Get global queue statistics.

    GET /api/v1/stats

    Returns: Statistics about queue usage
    """
    stats = queue.get_stats()

    return jsonify({
        "timestamp": datetime.utcnow().isoformat(),
        "statistics": stats
    }), 200


@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "queue_size": len(queue.requests)
    }), 200


# ============================================================================
# Microscope System Information
# ============================================================================

@app.route('/api/v1/microscopes', methods=['GET'])
def list_microscope_systems():
    """
    List available microscope systems.

    GET /api/v1/microscopes

    Returns: List of available microscope systems with descriptions
    """
    systems = {
        "DiSPIM": {
            "name": "Dual-view Inverted Selective Plane Illumination Microscopy",
            "description": "Advanced light-sheet microscopy for fast 3D imaging",
            "capabilities": ["high_speed", "3d_imaging", "live_cell", "minimal_phototoxicity"],
            "typical_applications": [
                "Developmental biology",
                "Neural imaging",
                "Cell migration tracking",
                "Organoid imaging"
            ],
            "reviewer": "Ryan"
        },
        "confocal": {
            "name": "Confocal Microscopy",
            "description": "Standard confocal for high-resolution fluorescence imaging",
            "capabilities": ["high_resolution", "3d_imaging", "multi_channel"],
            "typical_applications": [
                "Protein localization",
                "Co-localization studies",
                "Fixed cell imaging"
            ]
        },
        "widefield": {
            "name": "Widefield Fluorescence Microscopy",
            "description": "Standard fluorescence microscopy for general imaging",
            "capabilities": ["fast_acquisition", "large_field_of_view"],
            "typical_applications": [
                "General cell imaging",
                "Screening assays",
                "Time-lapse imaging"
            ]
        }
    }

    return jsonify({"microscope_systems": systems}), 200


# ============================================================================
# Server Configuration
# ============================================================================

if __name__ == '__main__':
    # Development server - in production, use proper WSGI server (gunicorn, uwsgi)
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'

    print(f"""
    ╔══════════════════════════════════════════════════════════════╗
    ║  Global Experiment Queue API Server                          ║
    ║  Running on http://0.0.0.0:{port}                            ║
    ║                                                              ║
    ║  Endpoints:                                                  ║
    ║  - POST   /api/v1/experiments          Submit experiment    ║
    ║  - GET    /api/v1/experiments          List experiments     ║
    ║  - GET    /api/v1/review/pending       Pending reviews      ║
    ║  - POST   /api/v1/review/:id/approve   Approve request      ║
    ║  - POST   /api/v1/review/:id/reject    Reject request       ║
    ║  - GET    /api/v1/stats                Queue statistics     ║
    ║                                                              ║
    ║  For production deployment, use:                            ║
    ║  gunicorn -w 4 -b 0.0.0.0:{port} api_server:app            ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

    app.run(host='0.0.0.0', port=port, debug=debug)
