#!/bin/bash
cd /opt/human-features
gunicorn --workers=1 --timeout=3600 --bind=0.0.0.0:8080 app:app
