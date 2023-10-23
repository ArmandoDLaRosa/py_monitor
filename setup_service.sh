#!/bin/bash

# Define variables
APP_NAME="py_monitor"
APP_SCRIPT="/home/armando/Repos/py_monitor/app.py"
APP_DIR="/home/armando/Repos/py_monitor/"
USER="armando"
VENV_DIR="/home/armando/Repos/myenv"
CRON_FILE="/home/armando/Repos/py_monitor/crons/cron.txt" 
BACKUP_CRON="/home/armando/Repos/py_monitor/crons/crontab_backup.txt" 

# Create systemd service file for your Flask app
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

# Enable and start the service for your Flask app
sudo systemctl enable ${APP_NAME}.service
sudo systemctl start ${APP_NAME}.service

echo "Service '${APP_NAME}' has been set up and started."

# Ensure Redis is enabled and started
sudo systemctl enable redis-server.service
sudo systemctl start redis-server.service

echo "Service Redis has been set up and started."

# Start the MySQL server
sudo systemctl enable mysql.service
sudo systemctl start mysql.service

echo "Service MariaDB has been set up and started."

# Load environment variables from .env file
source .env

sudo mysql <<MYSQL_SCRIPT
CREATE DATABASE IF NOT EXISTS LCARS;
CREATE USER IF NOT EXISTS '$MARIADB_USER'@'localhost' IDENTIFIED BY '$MARIADB_PASSWORD';
GRANT ALL PRIVILEGES ON LCARS.* TO '$MARIADB_USER'@'localhost';
FLUSH PRIVILEGES;
MYSQL_SCRIPT

echo "MariaDB database and user have been created."

INNODB_BUFFER_POOL_SIZE="1024M"  
# This setting determines the size of the InnoDB buffer pool, which is an important memory area for caching data and indexes. 
# A larger value can improve read performance but may require more memory.

MAX_CONNECTIONS="50"             
# This setting specifies the maximum number of concurrent connections that the MySQL/MariaDB server can handle.
# It's important to set this value to a reasonable limit based on your server's resources and expected traffic.

MEMORY_SIZE="2048M"  
# This setting represents the amount of memory allocated to the entire MySQL/MariaDB process.
# You should adjust this value based on your server's total memory and other resource requirements.

THREAD_STACK="512K"
# This setting defines the stack size for each thread in the MySQL/MariaDB server.
# Adjusting this value can affect the memory usage per thread. Smaller values may conserve memory.


sudo sed -i "s/^\(innodb_buffer_pool_size\s*=\s*\).*\$/\1$INNODB_BUFFER_POOL_SIZE/" /etc/mysql/mariadb.conf.d/50-server.cnf
sudo sed -i "s/^\(max_connections\s*=\s*\).*\$/\1$MAX_CONNECTIONS/" /etc/mysql/mariadb.conf.d/50-server.cnf
sudo sed -i "s/^\(key_buffer_size\s*=\s*\).*\$/\1$MEMORY_SIZE/" /etc/mysql/mariadb.conf.d/50-server.cnf
sudo sed -i "s/^\(thread_stack\s*=\s*\).*\$/\1$THREAD_STACK/" /etc/mysql/mariadb.conf.d/50-server.cnf


CPU_CORES="0"  # Allow unlimited concurrency
CORES="4" # I've 4 CPU cores

sudo sed -i "s/^\(innodb_thread_concurrency\s*=\s*\).*\$/\1$CPU_CORES/" /etc/mysql/mariadb.conf.d/50-server.cnf
sudo sed -i "s/^\(innodb_read_io_threads\s*=\s*\).*\$/\1$CORES/" /etc/mysql/mariadb.conf.d/50-server.cnf
sudo sed -i "s/^\(innodb_write_io_threads\s*=\s*\).*\$/\1$CORES/" /etc/mysql/mariadb.conf.d/50-server.cnf


# Restart the MariaDB service to apply the changes
sudo systemctl restart mysql.service

echo "MariaDB conf file has been updated"

# Backup current crontab
crontab -l > "$BACKUP_CRON"

# Set crontab to the jobs defined in the file
crontab "$CRON_FILE"

echo "Current crontab has been backed up to '$BACKUP_CRON'."
echo "Cron jobs have been updated to match '$CRON_FILE'."

${VENV_DIR}/bin/python -m flask db init

echo "Migrations folder existence was verified"


