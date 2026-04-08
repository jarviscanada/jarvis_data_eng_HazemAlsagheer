
psql_host=$1
psql_port=$2
db_name=$3
psql_user=$4
psql_password=$5

if [ "$#" -ne 5 ]; then
	echo "Illegal number of parameters"
	exit 1
fi

vmstat_mb=$(vmstat --unit M)
hostname=$(hostname -f)

cpu_number=$(lscpu | grep "CPU(s)"| awk '{print $2}' | head -n1 | xargs)
cpu_architecture=$(lscpu | grep "Architecture" | awk -F: '{print $2}' | head -n1 | xargs)
cpu_model=$(lscpu | grep "Model name:"| awk -F: '{print $2}' | head -n1 | xargs)
cpu_mhz=$(cat /proc/cpuinfo | grep 'cpu MHz' | awk '{print $4}' | head -n1 | xargs)
l2_cache=$(lscpu | grep "L2"| awk '{print $3}' | head -n1 | xargs)
timestamp=$(date +"%Y-%m-%d %H:%M:%S" | xargs)
total_mem=$(cat /proc/meminfo | grep "MemTotal" | awk '{print $2}' | xargs)


insert_stmt="INSERT INTO host_info( hostname, cpu_number, cpu_architecture, cpu_model, cpu_mhz, l2_cache, timestamp, total_mem) VALUES ('$hostname', '$cpu_number', '$cpu_architecture', '$cpu_model', '$cpu_mhz','$l2_cache', '$timestamp', '$total_mem')";

export PGPASSWORD=$psql_password

psql -h $psql_host -p $psql_port -d $db_name -U $psql_user -c "$insert_stmt"

exit $?



