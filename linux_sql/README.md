# Introduction

The Linux Cluster Monitoring System is designed to collect hardware specifications and real-time resource usage metrics from multiple Linux machines. It targets system administrators and DevOps engineers who need visibility into system performance and capacity across a distributed environment.

The system follows a centralized architecture, where each node runs lightweight Bash scripts to extract CPU, memory, and disk usage metrics, and pushes the data to a PostgreSQL database for persistent storage and analysis. Docker is used to containerize the PostgreSQL instance, ensuring portability and consistent deployment, while Git manages version control and collaboration.

Three core scripts handle system operations: one initializes the database schema, one collects static host information, and another continuously captures dynamic resource usage. A cron job schedules periodic data collection at one-minute intervals, enabling near real-time monitoring and trend analysis.   

# Quick Start
### 1.  Start Postgres Container   
**Command:** ./psql_docker.sh create db_username db_password
### 2. Create Tables by running the ddl.sql script   
**Command:** psql -h localhost -U db_username -d host_agent -f ddl.sql
### 3. Collect hardware information/specification and write it into the DB through the host_info.sh script 
**Command:** bash ./host_info.sh psql_host psql_port db_name psql_user psql_password
### 4. Collect hardware usage data and write it into the DB through the host_usage.sh script  
**Command:** bash ./host_usage.sh psql_host psql_port db_name psql_user psql_password
### 5. Set up a crontab to automate hardware usage data extraction in per-minute intervals  
**Command:** crontab -e  
**Command:** * * * * * bash /home/username/dev/jrvs-user-folder/linux_sql/host_agent/scripts/host_usage.sh localhost 5432 host_agent postgres password > /tmp/host_usage.log

# Implementation
The system is implemented using a set of Bash scripts that collect hardware specifications and real-time resource usage from the host machine. The host_info.sh script extracts static system data such as CPU details and total memory, while host_usage.sh captures dynamic metrics like CPU usage, memory availability, and disk I/O at regular intervals. A PostgreSQL database, running inside a Docker container, is used to store this data in two structured tables: host_info and host_usage. Data insertion is handled through parameterized SQL commands executed via the psql CLI. To enable continuous monitoring, the host_usage.sh script is scheduled using crontab to run every minute, ensuring consistent and up-to-date system metrics for analysis.  

## Architecture

![Linux Cluster Diagram](assets/Linux%20Diagram.png)
## Scripts
- *psql_docker.sh:* Initializes the PostgreSQL container and creates the required database schema (host_info and host_usage tables). The script validates input arguments and prevents duplicate table creation by throwing errors if the schema already exists.  
**Usage:**./scripts/psql_docker.sh start|stop|create [db_username][db_password]
- *host_info.sh:* Extracts static hardware specifications (hostname, CPU, memory, etc.) from the host machine and inserts the data into the host_info table. This script is typically executed once per host during setup.  
**Usage:**bash scripts/host_usage.sh psql_host psql_port db_name psql_user psql_password
- *host_usage.sh:* Collects dynamic system metrics such as CPU utilization, memory usage, and disk I/O, and inserts them into the host_usage table. Designed to run periodically for time-series monitoring.  
**Usage:** bash scripts/host_usage.sh localhost 5432 host_agent postgres password
- *crontab:* Schedules the execution of host_usage.sh at a fixed interval (every minute) to ensure continuous data collection and near real-time monitoring.  
**Usage:** * * * * * bash /path/to/host_usage.sh localhost 5432 host_agent postgres password


## Database Modeling

`host_info`  
| Column Name      | Data Type | Description                     |  
| ---------------- | --------- | ------------------------------- |  
| id               | SERIAL    | Unique identifier for each host |  
| hostname         | VARCHAR   | Name of the host machine        |  
| cpu_number       | INT       | Number of CPUs available        |  
| cpu_architecture | VARCHAR   | CPU architecture                |  
| cpu_model        | VARCHAR   | CPU model                       |  
| cpu_mhz          | FLOAT     | CPU speed in MHz                |  
| l2_cache         | INT       | L2 cache size in kB                  |  
| total_mem        | INT       | Total memory in kB              |  
| timestamp        | TIMESTAMP | Time when data was recorded     |  


`host_usage`
| Column Name    | Data Type | Description                       |
| -------------- | --------- | --------------------------------- |
| timestamp      | TIMESTAMP | Time when data was recorded       |
| host_id        | INT       | Foreign key referencing host_id from host_info |
| memory_free    | INT       | Free memory in MB                 |
| cpu_idle       | INT       | CPU idle percentage               |
| cpu_kernel     | INT       | CPU usage in kernel mode  percentage        |
| disk_io        | INT       | Number of disk I/O operations               |
| disk_available | INT       | Available disk space in MB        |


# Test

The Bash scripts were tested in two stages: metric-extraction validation and database-integration validation.

For host_info.sh and host_usage.sh, each command used to extract system metrics (CPU, memory, disk, and hostname) was first tested independently in the terminal to verify correctness, formatting, and consistency of the output. 

Once verified, the scripts were executed, and SQL queries were used to confirm successful insertion into the PostgreSQL database. Validation included checking row counts, data types, and value accuracy using queries such as SELECT * FROM "tableName";.

For psql_docker.sh, the script was tested by initializing the PostgreSQL container and verifying that the required tables were created with the correct schema.

# Deployment

The system is deployed on a Linux environment, where Docker is used to provision a PostgreSQL container for persistent storage. The monitoring scripts run directly on each host machine and are scheduled using cron to execute at regular intervals.GitHub is used strictly for version control and code management.  

# Improvements
- I would add the units to the columns of the DB for better readability of the data. I will also standardize a unit to help maintain consistency across.

- I would add a visualization layer by adding a dashboard, which will show the latest data extracted, helping with getting easy and dynamic updates.

- I would introduce an archive table for older usage records. Since the monitoring script inserts data on a recurring schedule, the host_usage table will continue growing over time. Archiving older records would help keep the main table smaller and more efficient for current reporting, while still preserving historical data for long-term analysis.



