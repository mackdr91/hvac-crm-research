# Author: Domonick Mack
# Date: 2026-11-13
# Description: Dockerfile for running HVAC CRM research deliverable verification and local analysis environment.

FROM python:3.9-slim

WORKDIR /app

COPY . /app

CMD ["python3", "scripts/verify_deliverables.py"]
