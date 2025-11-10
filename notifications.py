#!/usr/bin/env python3
"""
Notification Service for Global Experiment Queue

Handles email notifications and alerts for experiment submissions,
approvals, rejections, and status updates to keep researchers
and reviewers informed worldwide.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List
from datetime import datetime
import json
from pathlib import Path


class NotificationService:
    """
    Manages notifications for the global experiment queue.
    Supports email notifications and can be extended for Slack, Teams, etc.
    """

    def __init__(self, config_path: str = "notification_config.json"):
        self.config = self._load_config(config_path)
        self.enabled = self.config.get("enabled", False)

        # Email configuration
        self.smtp_server = os.getenv("SMTP_SERVER", self.config.get("smtp_server"))
        self.smtp_port = int(os.getenv("SMTP_PORT", self.config.get("smtp_port", 587)))
        self.smtp_user = os.getenv("SMTP_USER", self.config.get("smtp_user"))
        self.smtp_password = os.getenv("SMTP_PASSWORD", self.config.get("smtp_password"))
        self.from_email = os.getenv("FROM_EMAIL", self.config.get("from_email", "experiments@lab.org"))

        # Reviewer configuration - map microscope systems to reviewers
        self.reviewers = self.config.get("reviewers", {
            "DiSPIM": ["ryan@lab.org"],
            "confocal": ["imaging-team@lab.org"],
            "widefield": ["imaging-team@lab.org"]
        })

    def _load_config(self, config_path: str) -> dict:
        """Load notification configuration"""
        path = Path(config_path)
        if path.exists():
            with open(path, 'r') as f:
                return json.load(f)
        else:
            # Create default config
            default_config = {
                "enabled": False,  # Disabled by default until configured
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "from_email": "experiments@lab.org",
                "reviewers": {
                    "DiSPIM": ["ryan@lab.org"],
                    "confocal": ["imaging-team@lab.org"],
                    "widefield": ["imaging-team@lab.org"],
                    "light_sheet": ["imaging-team@lab.org"],
                    "two_photon": ["imaging-team@lab.org"],
                    "super_resolution": ["imaging-team@lab.org"]
                },
                "email_templates": {
                    "new_submission_subject": "[Experiment Queue] New {priority} priority request for {microscope}",
                    "approval_subject": "[Experiment Queue] Your experiment has been approved",
                    "rejection_subject": "[Experiment Queue] Experiment request update",
                    "completion_subject": "[Experiment Queue] Your experiment is complete"
                }
            }

            # Save default config
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=2)

            print(f"Created default notification config at {config_path}")
            print("Please configure SMTP settings and enable notifications.")

            return default_config

    def _send_email(
        self,
        to_addresses: List[str],
        subject: str,
        body_text: str,
        body_html: Optional[str] = None
    ) -> bool:
        """
        Send an email notification.

        Args:
            to_addresses: List of recipient email addresses
            subject: Email subject
            body_text: Plain text body
            body_html: Optional HTML body

        Returns:
            True if sent successfully, False otherwise
        """
        if not self.enabled:
            print(f"[NOTIFICATION] (disabled) Would send email to {to_addresses}")
            print(f"   Subject: {subject}")
            print(f"   Body: {body_text[:100]}...")
            return True

        if not all([self.smtp_server, self.smtp_user, self.smtp_password]):
            print("[ERROR] SMTP not configured. Cannot send email.")
            return False

        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.from_email
            msg['To'] = ', '.join(to_addresses)
            msg['Subject'] = subject

            # Attach plain text and HTML parts
            msg.attach(MIMEText(body_text, 'plain'))
            if body_html:
                msg.attach(MIMEText(body_html, 'html'))

            # Send via SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)

            print(f"[NOTIFICATION] Email sent to {to_addresses}")
            return True

        except Exception as e:
            print(f"[ERROR] Failed to send email: {e}")
            return False

    def notify_new_submission(
        self,
        request_id: str,
        microscope_system: str,
        requester_name: str,
        priority: str
    ):
        """
        Notify reviewers of a new experiment submission.

        Args:
            request_id: ID of the submitted request
            microscope_system: Requested microscope system
            requester_name: Name of requester
            priority: Priority level
        """
        # Get reviewer emails for this microscope system
        reviewer_emails = self.reviewers.get(microscope_system, self.reviewers.get("default", []))

        if not reviewer_emails:
            print(f"[WARNING] No reviewers configured for {microscope_system}")
            return

        # Prepare email
        subject_template = self.config.get("email_templates", {}).get(
            "new_submission_subject",
            "[Experiment Queue] New {priority} priority request for {microscope}"
        )
        subject = subject_template.format(priority=priority.upper(), microscope=microscope_system)

        body_text = f"""
New Experiment Submission

Request ID: {request_id}
Microscope System: {microscope_system}
Requester: {requester_name}
Priority: {priority.upper()}
Submitted: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}

Please review this request at:
https://experiments.lab.org/review/{request_id}

---
Global Experiment Queue System
        """.strip()

        body_html = f"""
<html>
<body>
    <h2>New Experiment Submission</h2>
    <table>
        <tr><td><strong>Request ID:</strong></td><td>{request_id}</td></tr>
        <tr><td><strong>Microscope System:</strong></td><td>{microscope_system}</td></tr>
        <tr><td><strong>Requester:</strong></td><td>{requester_name}</td></tr>
        <tr><td><strong>Priority:</strong></td><td><span style="color: {'red' if priority == 'urgent' else 'orange' if priority == 'high' else 'black'}">{priority.upper()}</span></td></tr>
        <tr><td><strong>Submitted:</strong></td><td>{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</td></tr>
    </table>
    <p><a href="https://experiments.lab.org/review/{request_id}">Click here to review this request</a></p>
    <hr>
    <small>Global Experiment Queue System</small>
</body>
</html>
        """.strip()

        self._send_email(reviewer_emails, subject, body_text, body_html)

    def notify_approval(
        self,
        requester_email: str,
        request_id: str,
        reviewer_name: str,
        scheduled_date: Optional[str] = None
    ):
        """
        Notify requester that their experiment has been approved.

        Args:
            requester_email: Email of requester
            request_id: ID of the request
            reviewer_name: Name of reviewer who approved
            scheduled_date: Optional scheduled execution date
        """
        subject = self.config.get("email_templates", {}).get(
            "approval_subject",
            "[Experiment Queue] Your experiment has been approved"
        )

        schedule_info = f"\nScheduled for: {scheduled_date}" if scheduled_date else "\nScheduling: To be determined"

        body_text = f"""
Good news! Your experiment request has been approved.

Request ID: {request_id}
Reviewed by: {reviewer_name}
Status: APPROVED{schedule_info}

You can track your experiment status at:
https://experiments.lab.org/experiments/{request_id}

You will receive another notification when your experiment begins and when results are ready.

---
Global Experiment Queue System
        """.strip()

        body_html = f"""
<html>
<body>
    <h2 style="color: green;">✓ Experiment Approved</h2>
    <p>Good news! Your experiment request has been approved.</p>
    <table>
        <tr><td><strong>Request ID:</strong></td><td>{request_id}</td></tr>
        <tr><td><strong>Reviewed by:</strong></td><td>{reviewer_name}</td></tr>
        <tr><td><strong>Status:</strong></td><td><span style="color: green;">APPROVED</span></td></tr>
        {f'<tr><td><strong>Scheduled for:</strong></td><td>{scheduled_date}</td></tr>' if scheduled_date else '<tr><td><strong>Scheduling:</strong></td><td>To be determined</td></tr>'}
    </table>
    <p><a href="https://experiments.lab.org/experiments/{request_id}">Track your experiment status</a></p>
    <p>You will receive another notification when your experiment begins and when results are ready.</p>
    <hr>
    <small>Global Experiment Queue System</small>
</body>
</html>
        """.strip()

        self._send_email([requester_email], subject, body_text, body_html)

    def notify_rejection(
        self,
        requester_email: str,
        request_id: str,
        reviewer_name: str,
        reviewer_comments: str
    ):
        """
        Notify requester that their experiment was not approved.

        Args:
            requester_email: Email of requester
            request_id: ID of the request
            reviewer_name: Name of reviewer
            reviewer_comments: Explanation for rejection
        """
        subject = self.config.get("email_templates", {}).get(
            "rejection_subject",
            "[Experiment Queue] Experiment request update"
        )

        body_text = f"""
Your experiment request has been reviewed.

Request ID: {request_id}
Reviewed by: {reviewer_name}
Status: NOT APPROVED

Reviewer comments:
{reviewer_comments}

If you have questions or would like to submit a revised request, please contact {reviewer_name} or resubmit with additional information.

View your request at:
https://experiments.lab.org/experiments/{request_id}

---
Global Experiment Queue System
        """.strip()

        body_html = f"""
<html>
<body>
    <h2>Experiment Request Update</h2>
    <p>Your experiment request has been reviewed.</p>
    <table>
        <tr><td><strong>Request ID:</strong></td><td>{request_id}</td></tr>
        <tr><td><strong>Reviewed by:</strong></td><td>{reviewer_name}</td></tr>
        <tr><td><strong>Status:</strong></td><td>NOT APPROVED</td></tr>
    </table>
    <p><strong>Reviewer comments:</strong></p>
    <blockquote>{reviewer_comments}</blockquote>
    <p>If you have questions or would like to submit a revised request, please contact {reviewer_name} or resubmit with additional information.</p>
    <p><a href="https://experiments.lab.org/experiments/{request_id}">View your request</a></p>
    <hr>
    <small>Global Experiment Queue System</small>
</body>
</html>
        """.strip()

        self._send_email([requester_email], subject, body_text, body_html)

    def notify_completion(
        self,
        requester_email: str,
        request_id: str,
        results_location: Optional[str] = None
    ):
        """
        Notify requester that their experiment is complete.

        Args:
            requester_email: Email of requester
            request_id: ID of the request
            results_location: Path/URL to results
        """
        subject = self.config.get("email_templates", {}).get(
            "completion_subject",
            "[Experiment Queue] Your experiment is complete"
        )

        results_info = f"\nResults available at: {results_location}" if results_location else ""

        body_text = f"""
Your experiment has been completed!

Request ID: {request_id}
Status: COMPLETED
Completion time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}{results_info}

View full details and download your data at:
https://experiments.lab.org/experiments/{request_id}

Thank you for using the Global Experiment Queue System!

---
Global Experiment Queue System
        """.strip()

        body_html = f"""
<html>
<body>
    <h2 style="color: green;">✓ Experiment Complete</h2>
    <p>Your experiment has been completed!</p>
    <table>
        <tr><td><strong>Request ID:</strong></td><td>{request_id}</td></tr>
        <tr><td><strong>Status:</strong></td><td><span style="color: green;">COMPLETED</span></td></tr>
        <tr><td><strong>Completion time:</strong></td><td>{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</td></tr>
        {f'<tr><td><strong>Results:</strong></td><td><a href="{results_location}">{results_location}</a></td></tr>' if results_location else ''}
    </table>
    <p><a href="https://experiments.lab.org/experiments/{request_id}"><strong>View full details and download your data</strong></a></p>
    <p>Thank you for using the Global Experiment Queue System!</p>
    <hr>
    <small>Global Experiment Queue System</small>
</body>
</html>
        """.strip()

        self._send_email([requester_email], subject, body_text, body_html)


# Testing/demo mode
if __name__ == "__main__":
    print("=== Notification Service Test ===\n")

    # Initialize service
    service = NotificationService()

    print(f"Notification service initialized")
    print(f"Enabled: {service.enabled}")
    print(f"Reviewers configured: {list(service.reviewers.keys())}\n")

    # Test notifications (will be logged, not sent unless SMTP is configured)
    print("Testing notification functions...\n")

    service.notify_new_submission(
        request_id="test-123",
        microscope_system="DiSPIM",
        requester_name="Dr. Test User",
        priority="high"
    )

    service.notify_approval(
        requester_email="testuser@university.edu",
        request_id="test-123",
        reviewer_name="Ryan",
        scheduled_date="2025-11-17T09:00:00"
    )

    service.notify_completion(
        requester_email="testuser@university.edu",
        request_id="test-123",
        results_location="/data/results/test-123"
    )

    print("\nNotification tests complete.")
    print("To enable actual email sending, configure SMTP settings in notification_config.json")
