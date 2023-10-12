#!/bin/bash

# Define variables
APP_NAME="py_monitor"
APP_SCRIPT="/home/armando/Repos/py_monitor/app.py"
APP_DIR="/home/armando/Repos/py_monitor/"
USER="armando"
VENV_DIR="/home/armando/Repos/myenv" 

# Create systemd service file
SERVICE_FILE="/etc/systemd/system/${APP_NAME}.service"
cat <<EOF > "${SERVICE_FILE}"
[Unit]
Description=Your Flask Application

[Service]
ExecStart=${VENV_DIR}/bin/python ${APP_SCRIPT}
WorkingDirectory=${APP_DIR}
Restart=always
User=${USER}
Environment="PATH=${VENV_DIR}/bin:/usr/bin:/usr/local/bin"
Environment="FLASK_APP=${APP_SCRIPT}"
Environment="FLASK_ENV=production"

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
sudo systemctl enable ${APP_NAME}.service
sudo systemctl start ${APP_NAME}.service

echo "Service '${APP_NAME}' has been set up and started."

#sudo journalctl -u {APP_NAME}.service

