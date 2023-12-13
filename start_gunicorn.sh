#!/bin/bash
cd /opt/human-features
exec /home/ubuntu/.local/bin/gunicorn --workers=1 --timeout=3600 --bind=0.0.0.0:8080 --access-logfile - --error-logfile - app:app
