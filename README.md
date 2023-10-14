Bugs:
    CPU Monitoring might be having errors... as 80% seems unlikely.

Backlog:
    Requirements.txt
    Implement Flask Migration 
    Implement a Real DB insteaad of sqlitedb
    
Documentation:

    Env Activiting
        source myenv/bin/activate

    Sh scripting prepping
        cd /home/workspace

        chmod +x setup_service.sh
        chmod +x push_new_code.sh

    Update the code running as a service on the  raspberry

        sudo ./push_new_code.sh

    Check the logs of the service

        sudo journalctl -u py_monitor.service | tail -20

    Run the scripts
        sudo ./setup_service.sh

