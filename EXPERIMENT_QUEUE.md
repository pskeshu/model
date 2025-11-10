# Global Experiment Queue System

A worldwide job queue system for managing imaging experiment requests across multiple microscope systems. Enables biological scientists from anywhere in the world to submit experiment requests, and allows facility managers/reviewers to approve and schedule experiments.

## Overview

The Global Experiment Queue System addresses the challenge of coordinating imaging experiments across:
- **Multiple researchers** worldwide
- **Various microscope systems** (DiSPIM, confocal, widefield, etc.)
- **Different sample types** and treatments
- **Limited equipment availability** requiring approval workflows

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Global Researchers                        │
│  (Submit experiments from anywhere in the world)            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    REST API Server                           │
│  • Experiment submission endpoints                          │
│  • Review/approval endpoints                                │
│  • Status tracking                                          │
│  • Queue management                                         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   Job Queue System                           │
│  • Persistent storage (JSON/Database)                       │
│  • Priority management                                      │
│  • Status workflow (submitted → approved → completed)       │
│  • Multi-microscope support                                 │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│               Notification Service                           │
│  • Email alerts for reviewers                               │
│  • Status updates for requesters                            │
│  • Completion notifications                                 │
└─────────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│             Reviewers (Ryan, etc.)                           │
│  • Approve/reject requests                                  │
│  • Schedule experiments                                     │
│  • Manage microscope availability                           │
└─────────────────────────────────────────────────────────────┘
```

## Key Features

### For Researchers (Requesters)
- **Submit experiments** from anywhere in the world via REST API
- **Track experiment status** in real-time
- **Receive notifications** when experiments are reviewed, approved, or completed
- **Specify detailed sample specifications** using Sample_Spec schema
- **Set priority levels** for urgent experiments

### For Reviewers (Ryan, Facility Managers)
- **View pending requests** filtered by microscope system
- **Approve or reject** experiments with comments
- **Schedule experiments** for specific dates/times
- **Monitor queue statistics** across all systems
- **Receive alerts** for new high-priority submissions

### System Features
- **Multi-microscope support**: DiSPIM, confocal, widefield, light-sheet, etc.
- **Priority queue management**: Urgent, high, medium, low priorities
- **Persistent storage**: All requests saved to disk (JSON) or database
- **RESTful API**: Easy integration with lab management systems
- **Email notifications**: Keep all parties informed
- **Status tracking**: From submission through completion
- **Extensible**: Easy to add new microscope systems or workflows

## Workflow

### 1. Experiment Submission
```
Researcher → API → Queue → Notification → Reviewer
```

A researcher anywhere in the world submits an experiment request with:
- Sample specification (using Sample_Spec schema)
- Requested microscope system
- Scientific rationale
- Priority level

### 2. Review Process
```
Reviewer receives notification → Reviews request → Approves/Rejects
```

The reviewer (e.g., Ryan for DiSPIM) receives an email notification and can:
- View detailed experiment specifications
- Approve with scheduling information
- Reject with explanation
- Request modifications

### 3. Execution
```
Approved → Scheduled → In Progress → Completed → Results Available
```

Once approved:
- Experiment is added to execution queue
- Status updated to "in_progress" when started
- Requester notified when completed
- Results location provided

## Request States

```
SUBMITTED ──────► UNDER_REVIEW ──────► APPROVED ──────► IN_PROGRESS ──────► COMPLETED
                        │
                        └──────────► REJECTED
                        │
                        └──────────► CANCELLED
```

- **SUBMITTED**: Initial state when request is created
- **UNDER_REVIEW**: Reviewer is actively evaluating
- **APPROVED**: Approved for execution, waiting to be scheduled/started
- **REJECTED**: Not approved, with explanation from reviewer
- **IN_PROGRESS**: Experiment is currently running
- **COMPLETED**: Experiment finished, results available
- **CANCELLED**: Requester or reviewer cancelled the request

## API Endpoints

### Experiment Submission

#### Submit New Experiment
```http
POST /api/v1/experiments
Content-Type: application/json

{
  "sample_spec": {
    "sample_id": "zebrafish_001",
    "biological_context": {...},
    "imaging_parameters": {...}
  },
  "requester": {
    "name": "Dr. Jane Smith",
    "email": "jsmith@university.edu",
    "institution": "University of Biology",
    "country": "USA"
  },
  "experiment": {
    "microscope_system": "DiSPIM",
    "scientific_rationale": "Study neural crest cell migration...",
    "priority": "high"
  }
}
```

**Response:**
```json
{
  "request_id": "abc-123-def-456",
  "status": "submitted",
  "message": "Experiment request submitted successfully"
}
```

#### Get Experiment Details
```http
GET /api/v1/experiments/{request_id}
```

#### List All Experiments
```http
GET /api/v1/experiments?status=approved&microscope=DiSPIM&priority=high
```

### Review Endpoints

#### Get Pending Reviews
```http
GET /api/v1/review/pending?microscope=DiSPIM
```

**Response:**
```json
{
  "count": 3,
  "pending_reviews": [
    {
      "request_id": "abc-123",
      "requester": {...},
      "experiment": {...},
      "priority": "high"
    }
  ]
}
```

#### Approve Experiment
```http
POST /api/v1/review/{request_id}/approve
Content-Type: application/json

{
  "reviewer_name": "Ryan",
  "reviewer_comments": "Excellent use case for DiSPIM",
  "scheduled_date": "2025-11-17T09:00:00"
}
```

#### Reject Experiment
```http
POST /api/v1/review/{request_id}/reject
Content-Type: application/json

{
  "reviewer_name": "Ryan",
  "reviewer_comments": "Insufficient justification for DiSPIM usage. Standard confocal would be more appropriate."
}
```

### Status Tracking

#### Update Experiment Status
```http
PUT /api/v1/experiments/{request_id}/status
Content-Type: application/json

{
  "status": "in_progress"
}
```

#### Get Approved Queue
```http
GET /api/v1/queue/approved?microscope=DiSPIM
```

### Statistics

#### Get Queue Statistics
```http
GET /api/v1/stats
```

**Response:**
```json
{
  "timestamp": "2025-11-10T12:00:00Z",
  "statistics": {
    "total_requests": 45,
    "by_status": {
      "submitted": 5,
      "approved": 12,
      "in_progress": 3,
      "completed": 20,
      "rejected": 5
    },
    "by_microscope": {
      "DiSPIM": 15,
      "confocal": 20,
      "widefield": 10
    },
    "by_priority": {
      "urgent": 2,
      "high": 10,
      "medium": 25,
      "low": 8
    }
  }
}
```

## Microscope Systems

The system supports multiple microscope types:

| System | Description | Typical Use Cases | Reviewer |
|--------|-------------|-------------------|----------|
| **DiSPIM** | Dual-view Inverted Selective Plane Illumination | Fast 3D imaging, developmental biology, minimal phototoxicity | Ryan |
| **Confocal** | Standard confocal microscopy | High-resolution fluorescence, protein localization | Imaging Team |
| **Widefield** | Standard fluorescence microscopy | General cell imaging, screening assays | Imaging Team |
| **Light Sheet** | Advanced light-sheet microscopy | Large samples, live imaging | Imaging Team |
| **Two Photon** | Two-photon microscopy | Deep tissue imaging | Imaging Team |
| **Super Resolution** | STED, STORM, PALM | Nanoscale imaging | Imaging Team |

## Priority Levels

- **URGENT**: Time-sensitive experiments (e.g., live samples with limited viability)
- **HIGH**: Important experiments with tight deadlines
- **MEDIUM**: Standard experiments (default)
- **LOW**: Exploratory experiments, flexible timing

Requests are sorted first by priority, then by submission date.

## Use Cases

### Use Case 1: International Collaboration
**Scenario**: A researcher in Europe wants to use the DiSPIM in the US lab.

1. Researcher submits experiment via API with complete Sample_Spec
2. Ryan receives email notification about high-priority DiSPIM request
3. Ryan reviews scientific rationale and sample details
4. Ryan approves and schedules for next week
5. Researcher receives approval notification with scheduling info
6. Lab staff executes experiment when scheduled
7. Researcher receives completion notification with data access

### Use Case 2: Multi-Microscope Comparison
**Scenario**: A researcher wants to compare imaging quality across systems.

1. Researcher submits multiple requests for same sample on different microscopes
2. Each microscope's reviewer evaluates appropriateness
3. Approved experiments scheduled across different systems
4. Researcher tracks all experiments via dashboard
5. Comparative analysis performed on results

### Use Case 3: Urgent Live Sample
**Scenario**: Time-sensitive experiment with limited sample viability.

1. Researcher submits with "urgent" priority
2. Reviewer immediately notified
3. Fast-track approval process
4. Experiment executed within hours
5. Real-time status updates

## Deployment

### Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure notifications (optional)
# Edit notification_config.json with SMTP settings

# Run API server
python api_server.py

# Or with gunicorn for production
gunicorn -w 4 -b 0.0.0.0:5000 api_server:app
```

### Production Deployment

#### Option 1: Cloud Deployment (AWS, GCP, Azure)
- Deploy API server on cloud instance
- Use managed database (PostgreSQL RDS, Cloud SQL)
- Configure email service (SES, SendGrid)
- Set up load balancer for high availability
- Enable HTTPS with SSL certificate

#### Option 2: On-Premise Deployment
- Deploy on lab server
- Use local database or file storage
- Configure SMTP relay
- Secure with firewall and VPN

#### Environment Variables
```bash
export QUEUE_STORAGE_PATH=/path/to/queue.json
export SMTP_SERVER=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USER=your_email@gmail.com
export SMTP_PASSWORD=your_app_password
export FROM_EMAIL=experiments@lab.org
export PORT=5000
export DEBUG=False
```

### Database Backend (Optional)

For production with high volume, replace JSON storage with PostgreSQL:

```python
# In experiment_queue.py, modify JobQueue class to use SQLAlchemy
# Example:
from sqlalchemy import create_engine, Column, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class ExperimentRequestDB(Base):
    __tablename__ = 'experiment_requests'
    request_id = Column(String, primary_key=True)
    data = Column(JSON)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

# Connect to PostgreSQL
engine = create_engine('postgresql://user:password@localhost/experiment_queue')
Session = sessionmaker(bind=engine)
```

## Security Considerations

### Authentication
- Add API key authentication for submitters
- JWT tokens for session management
- Role-based access control (RBAC)

### Authorization
- Reviewers can only approve their assigned microscope systems
- Requesters can only view their own experiments
- Admin users have full access

### Data Protection
- HTTPS for all API communication
- Encrypt sensitive data in database
- Rate limiting to prevent abuse
- Input validation to prevent injection attacks

## Monitoring and Maintenance

### Health Checks
```http
GET /api/v1/health
```

Returns system status and queue size.

### Logging
- Request/response logging
- Error tracking (Sentry, CloudWatch)
- Performance monitoring
- Queue depth alerts

### Metrics to Monitor
- Requests per day
- Average approval time
- Experiment completion rate
- System response time
- Error rates

## Client Integration

### Python Client Example
```python
import requests

# Submit experiment
response = requests.post('https://experiments.lab.org/api/v1/experiments', json={
    "sample_spec": {...},
    "requester": {
        "name": "Dr. Jane Smith",
        "email": "jsmith@university.edu",
        "institution": "University of Biology"
    },
    "experiment": {
        "microscope_system": "DiSPIM",
        "scientific_rationale": "...",
        "priority": "high"
    }
})

request_id = response.json()['request_id']
print(f"Submitted: {request_id}")

# Check status
status = requests.get(f'https://experiments.lab.org/api/v1/experiments/{request_id}')
print(status.json())
```

### cURL Examples
```bash
# Submit experiment
curl -X POST https://experiments.lab.org/api/v1/experiments \
  -H "Content-Type: application/json" \
  -d @experiment_request.json

# Get pending reviews for DiSPIM
curl https://experiments.lab.org/api/v1/review/pending?microscope=DiSPIM

# Approve experiment
curl -X POST https://experiments.lab.org/api/v1/review/{request_id}/approve \
  -H "Content-Type: application/json" \
  -d '{
    "reviewer_name": "Ryan",
    "reviewer_comments": "Approved",
    "scheduled_date": "2025-11-17T09:00:00"
  }'
```

## Future Enhancements

### Phase 1 (Current)
- ✅ Core job queue system
- ✅ REST API
- ✅ Email notifications
- ✅ Multi-microscope support

### Phase 2
- [ ] Web dashboard for visualization
- [ ] Real-time notifications (WebSocket)
- [ ] Advanced scheduling (time slots, calendars)
- [ ] Resource allocation optimization
- [ ] Integration with lab automation systems

### Phase 3
- [ ] Machine learning for experiment prioritization
- [ ] Automatic sample spec validation
- [ ] Predictive scheduling
- [ ] Cost estimation and billing
- [ ] Mobile app

## Support and Documentation

### Getting Help
- GitHub Issues: Report bugs or request features
- Email: support@experiments.lab.org
- Documentation: https://docs.experiments.lab.org

### Contributing
Contributions welcome! See CONTRIBUTING.md for guidelines.

## License

[Specify your license here]

---

## Quick Start for Ryan (DiSPIM Reviewer)

### View Pending DiSPIM Requests
```bash
curl https://experiments.lab.org/api/v1/review/pending?microscope=DiSPIM
```

### Approve a Request
```bash
curl -X POST https://experiments.lab.org/api/v1/review/{request_id}/approve \
  -H "Content-Type: application/json" \
  -d '{
    "reviewer_name": "Ryan",
    "reviewer_comments": "Approved for DiSPIM",
    "scheduled_date": "2025-11-17T09:00:00"
  }'
```

### Check Queue Statistics
```bash
curl https://experiments.lab.org/api/v1/stats
```

You'll also receive email notifications for all new DiSPIM submissions!
