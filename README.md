# AI Server Incident Assistant

An educational, production-focused AI engineering project that aims to help IT
support staff investigate server incidents and identify likely root causes.

The project starts as a small Python command-line application and will grow in
carefully tested milestones into a secure, evidence-based application. It is
designed to remain free to develop and run locally with open-source tools.

## Current capabilities

- Collects what happened during an incident
- Collects who was affected
- Collects when the incident occurred
- Rejects empty answers
- Displays an incident summary
- Supports repeated incident entry and a `quit` command

## Run locally

### Requirements

- Python 3

### Start the application

```bash
python3 chatbot.py
```

Enter `quit` when asked what happened to close the application.

## Project structure

```text
ai-chatbot/
├── chatbot.py     # Current command-line application
├── README.md      # Project documentation
└── .gitignore     # Files that Git must not track
```

## Roadmap

1. Incident intake
2. Validation and clean code
3. Persistent storage
4. Log and metric ingestion
5. Non-AI diagnostic baseline
6. Local AI integration
7. Evidence-based incident analysis
8. Backend API
9. Web interface
10. Security and access control
11. Testing, AI evaluations, and monitoring
12. Deployment and business pilot

## Project principles

- Solve a real operational problem
- Support conclusions with evidence
- Protect business and customer data
- Escalate uncertain conclusions to a person
- Measure reliability rather than relying on demos
- Keep paid services optional

## Status

This project is under active development for learning purposes. It is not yet
ready for use in a production environment.
# ai-server-incident-assistant
