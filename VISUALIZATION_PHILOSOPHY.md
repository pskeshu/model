# Design Philosophy for Workflow Visualization

## The Problem with Current Design

The current network graph shows **system topology** but fails to communicate:
- **Why** this system matters
- **What** scientific questions are being answered
- **Who** benefits from this (human stories)
- **When** things happen (time and urgency)
- **How many** experiments are happening simultaneously
- **Impact** of the system on science

## Better Design Philosophy: Multi-Perspective Storytelling

### Core Principles

#### 1. **Story First, Structure Second**
People remember stories, not system diagrams. Start with:
- A researcher with a burning scientific question
- Their journey through the system
- The moment of discovery when results arrive
- **Then** show how the system enables this at global scale

#### 2. **Progressive Disclosure**
Don't show everything at once:
- **Level 1**: Single experiment journey (emotional hook)
- **Level 2**: Multiple experiments in queue (scale)
- **Level 3**: System architecture (understanding)
- **Level 4**: Global impact (inspiration)

#### 3. **Multiple Views for Multiple Audiences**

**For Researchers**: "Where is my experiment?"
- Timeline view showing their experiment's progress
- Estimated completion time
- Position in queue

**For Reviewers (Ryan)**: "What needs my attention?"
- Pending requests sorted by priority/urgency
- Quick preview of each experiment
- One-click approve/request-more-info

**For Administrators**: "Is the system healthy?"
- Queue depth over time
- Microscope utilization
- Bottlenecks and delays
- Success metrics

**For Funders/Stakeholders**: "What's the impact?"
- Number of researchers served
- Countries participating
- Experiments completed
- Scientific output (papers, discoveries)

#### 4. **Time is Central**
The current design ignores time. Better approach:
- **Horizontal timeline** as primary organizing principle
- Show experiments moving left-to-right through stages
- Clock/calendar showing 24/7 operation
- Waiting time vs. execution time clearly differentiated

#### 5. **Context Over Mechanics**
Don't just show "Experiment approved" - show:
- **What**: "Zebrafish neural development imaging"
- **Why**: "Understanding how brains form"
- **Impact**: "Could reveal birth defect mechanisms"
- **Urgency**: "Live sample - 48hr window"

## Proposed Visualizations

### Visualization 1: Story Mode
**Purpose**: Emotional connection, understanding the journey

```
┌─────────────────────────────────────────────────────────────┐
│  Following Dr. Sarah's Experiment: "How do neurons migrate?" │
└─────────────────────────────────────────────────────────────┘

[STAGE 1: The Question] ───────────────────────────────────►
   Dr. Sarah (Stanford):
   "I need to see how neural crest cells migrate in real-time.
    Standard confocal is too slow. DiSPIM can capture this!"

   Sample: Zebrafish embryo, 24hpf, GFP-labeled neurons
   Need: 12 hours of imaging, 2-minute intervals

[STAGE 2: Submission] ──────────────────────────────────────►
   ⏱️  10:30 AM PST - Request submitted
   📧 Ryan notified (DiSPIM specialist)
   🔄 Position in queue: #3 (2 urgent experiments ahead)

[STAGE 3: Review] ──────────────────────────────────────────►
   ⏱️  2:15 PM PST - Ryan begins review
   👀 Reviewing: Scientific rationale, sample viability, DiSPIM fit
   💭 Ryan: "Perfect use case - this is exactly what DiSPIM excels at"

[STAGE 4: Approved!] ───────────────────────────────────────►
   ⏱️  2:47 PM PST - ✅ APPROVED
   📅 Scheduled: Tomorrow 9:00 AM
   📧 Dr. Sarah notified

[STAGE 5: Execution] ───────────────────────────────────────►
   ⏱️  9:00 AM PST - Imaging begins
   🔬 DiSPIM acquiring 360 timepoints
   📊 Progress: ████████░░░░ 67% (8/12 hours)

[STAGE 6: Results] ─────────────────────────────────────────►
   ⏱️  9:00 PM PST - Imaging complete
   💾 Data processed: 45 GB
   📬 Dr. Sarah notified - downloading results

[STAGE 7: Discovery] ───────────────────────────────────────►
   🎉 Analysis reveals: Neural crest cells use "scout" strategy
   📝 Paper submitted to Nature
   🌍 Impact: New understanding of brain development
```

### Visualization 2: Timeline/Queue View
**Purpose**: Show system activity, queue dynamics

```
GLOBAL EXPERIMENT QUEUE - Live View
════════════════════════════════════════════════════════════

                    SUBMITTED    IN REVIEW    APPROVED    EXECUTING    COMPLETE
                        │            │           │            │            │
DiSPIM (Ryan)          ██           █          ███         ████           ████████
                        ↓            ↓           ↓            ↓            ↓
                    [3 pending] [1 active]  [5 waiting]  [2 running]  [47 done]

Confocal (Team)        ████          ██         ██          ███           ████████
                    [8 pending] [2 active]  [4 waiting]  [3 running]  [89 done]

Widefield (Team)       ██           █           █          ██            ████████
                    [2 pending] [1 active]  [1 waiting]  [2 running]  [156 done]

Time ─────────────────────────────────────────────────────────────────►
        Minutes          Hours         Hours       Hours/Days        Archive

ACTIVE RIGHT NOW:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔬 DiSPIM #1: Zebrafish development (Dr. Sarah, USA) ████████░░ 78% → 3h remaining
🔬 DiSPIM #2: Organoid imaging (Dr. Schmidt, Germany) ███░░░░░░░ 35% → 8h remaining
🔬 Confocal #1: Protein localization (Dr. Chen, China) ██████████ 98% → 10min remaining
...

PENDING REVIEW (Ryan's Queue):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 URGENT: Live sample (Dr. Patel, India) - Submitted 2h ago - Expires in 6h
🟠 HIGH: Time-sensitive (Dr. Silva, Brazil) - Submitted 5h ago
🟡 MEDIUM: Standard request (Dr. Johnson, UK) - Submitted 1d ago
```

### Visualization 3: Global Map View
**Purpose**: Show worldwide collaboration

```
╔═══════════════════════════════════════════════════════════════════╗
║         GLOBAL EXPERIMENT QUEUE - 24/7 WORLDWIDE ACCESS           ║
╚═══════════════════════════════════════════════════════════════════╝

                    [World Map with pins]

    🌍 Active Researchers (48)
    📍 USA: 15 active experiments
    📍 Europe: 12 active experiments
    📍 Asia: 14 active experiments
    📍 South America: 4 active experiments
    📍 Australia: 3 active experiments

    Live Activity Feed:
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    🇺🇸 10:30 AM PST → Dr. Sarah submits DiSPIM request
    🇨🇳 02:15 AM CST → Dr. Chen's confocal experiment completes
    🇩🇪 07:47 PM CET → Dr. Schmidt's request approved
    🇮🇳 06:30 AM IST → Dr. Patel's urgent request submitted
    🇧🇷 01:20 PM BRT → Dr. Silva downloading results

    Current Time Zones:
    PST: 10:30 AM | CET: 7:30 PM | CST: 2:30 AM | IST: 12:00 AM

    [Microscope Facility - USA]
    ├─ DiSPIM: ⚡ Executing (2 experiments running)
    ├─ Confocal: 🔄 Ready (3 approved, awaiting schedule)
    └─ Widefield: ✅ Available
```

### Visualization 4: Dashboard/Control Center
**Purpose**: Real-time operations monitoring

```
╔══════════════════════ EXPERIMENT CONTROL CENTER ═══════════════════════╗
║                                                                         ║
║  QUEUE HEALTH                  MICROSCOPE STATUS         PERFORMANCE   ║
║  ┌──────────────┐             ┌──────────────┐         ┌────────────┐ ║
║  │ Total: 37    │             │ DiSPIM       │         │ Avg Wait   │ ║
║  │ Pending: 13  │             │ ⚡ Active    │         │ 4.2 hours  │ ║
║  │ Review: 4    │             │ 2/3 capacity │         │            │ ║
║  │ Approved: 11 │             ├──────────────┤         │ Completion │ ║
║  │ Active: 7    │             │ Confocal     │         │ 96.3%      │ ║
║  │ Complete: 2  │             │ ⚡ Active    │         │            │ ║
║  └──────────────┘             │ 3/4 capacity │         │ Uptime     │ ║
║                                ├──────────────┤         │ 99.2%      │ ║
║  URGENT ITEMS                 │ Widefield    │         └────────────┘ ║
║  🔴 2 urgent                  │ ✅ Ready     │                         ║
║  🟠 5 high priority           │ 0/2 capacity │         TRENDS         ║
║                                └──────────────┘         ┌────────────┐ ║
║  ALERTS                                                 │  Requests  │ ║
║  ⚠️  DiSPIM queue at 85%      RYAN'S REVIEW QUEUE     │     ↗     │ ║
║  ⚠️  1 urgent expiring in 4h  ┌──────────────┐        │   Usage    │ ║
║                                │ 3 Pending    │        │     ─     │ ║
║  NEXT ACTIONS                 │              │        │  Success   │ ║
║  → Ryan: Review 3 DiSPIM      │ 🔴 1 urgent  │        │     ↗     │ ║
║  → Schedule 5 approved        │ 🟠 2 high    │        └────────────┘ ║
║  → Complete 2 experiments     └──────────────┘                       ║
╚═════════════════════════════════════════════════════════════════════════╝
```

### Visualization 5: Impact View
**Purpose**: Show outcomes and value

```
GLOBAL EXPERIMENT QUEUE - IMPACT REPORT
═══════════════════════════════════════════════════════════════

EXPERIMENTS ENABLED (Last 6 months)
├─ Total experiments: 342
├─ Researchers served: 127 (from 23 countries)
├─ Imaging hours: 4,856 hours
└─ Data generated: 18.4 TB

SCIENTIFIC OUTPUT
├─ Papers published: 14
├─ Preprints: 23
├─ Conference presentations: 47
├─ Grant applications: 31

EFFICIENCY GAINS
├─ Avg approval time: 4.2 hours (was: 2.3 days)
├─ Microscope utilization: 87% (was: 54%)
├─ Failed experiments: 3.7% (was: 12%)
└─ Researcher satisfaction: 4.8/5.0

BREAKTHROUGH DISCOVERIES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏆 Nature paper: Neural crest migration mechanism (Dr. Sarah)
🏆 Cell paper: Organoid development patterns (Dr. Schmidt)
🏆 Science paper: Protein trafficking dynamics (Dr. Chen)

TESTIMONIALS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"The queue system let me access DiSPIM from India -
 impossible before. This data became my PhD thesis."
 - Dr. Patel, IISc Bangalore

"Ryan's expert review saved me from a failed experiment.
 His suggestion to adjust imaging parameters was crucial."
 - Dr. Silva, USP Brazil
```

## Implementation Strategy

### Phase 1: Core Story Mode
Build the linear narrative view that follows one experiment through the system. This becomes the "explainer" for new users.

### Phase 2: Timeline/Queue View
Add the horizontal timeline showing multiple experiments at different stages. This is the "working view" for daily operations.

### Phase 3: Dashboard View
Create the control center view for real-time monitoring and decision making.

### Phase 4: Map View
Add geographic visualization for showing global reach.

### Phase 5: Impact View
Build metrics and outcomes tracking.

## Key Design Decisions

### 1. **Animation Speed**
- Story mode: 2-3 seconds per stage (slow, narrative)
- Queue view: 1 second per update (rhythmic, monitoring)
- Dashboard: Real-time (immediate feedback)

### 2. **Information Hierarchy**
- **Primary**: Current state, next action
- **Secondary**: Context, history
- **Tertiary**: System details, metrics

### 3. **Color Semantics**
- **Red**: Urgent, attention needed
- **Orange**: High priority, soon
- **Yellow**: Medium, normal
- **Green**: Complete, success
- **Blue**: In progress, active
- **Gray**: Waiting, queued

### 4. **Interaction Modes**
- **Passive**: Auto-playing animation (for presentations)
- **Interactive**: Click to drill down (for exploration)
- **Live**: Real-time updates (for operations)

## Questions to Answer

1. **For researchers**: "When will my experiment run?"
2. **For Ryan**: "What's most urgent right now?"
3. **For administrators**: "Is the system performing well?"
4. **For funders**: "What's the return on investment?"
5. **For scientists**: "How do I use this system?"

## Success Metrics

A visualization succeeds if:
- ✅ Someone unfamiliar understands the system in 30 seconds
- ✅ Researchers feel confident submitting experiments
- ✅ Reviewers can prioritize effectively
- ✅ Stakeholders see the value clearly
- ✅ The human story comes through, not just the technology

## Next Steps

1. **Prototype Story Mode** - Build single-experiment narrative
2. **User Testing** - Show to researchers, get feedback
3. **Iterate** - Refine based on what resonates
4. **Add Complexity** - Gradually add other views
5. **Polish** - Make it beautiful and compelling

---

**Bottom Line**: Workflow visualization should inspire, not just inform. It should make people excited about science, not just understand the system mechanics.
