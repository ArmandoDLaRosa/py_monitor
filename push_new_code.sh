#!/bin/bash

# Define service name
SERVICE_NAME="py_monitor.service"

# Stop the service
echo "Stopping ${SERVICE_NAME}..."
sudo systemctl stop ${SERVICE_NAME}

# Restart the service
echo "Starting ${SERVICE_NAME}..."
sudo systemctl start ${SERVICE_NAME}

# Check service status
echo "Checking service status..."
sudo systemctl status ${SERVICE_NAME}

echo "Showing the last 20 lines of logs for ${SERVICE_NAME}..."
sudo journalctl -u ${SERVICE_NAME} | tail -20
