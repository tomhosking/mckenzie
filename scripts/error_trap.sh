#!/bin/bash

# SCRIPT=$(readlink -f "$0")
SCRIPTPATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo $SCRIPTPATH
source "${SCRIPTPATH}/../config.sh"

timedout=0

mckenzie_trap_timeout () {
    echo "McKenzie caught a timeout"
    timedout=1
    curl -s --data "jobid=$SLURM_JOB_ID&status=timeout" http://${MCKENZIE_ENDPOINT}/hooks/update_job/
}


mckenzie_trap_err () {
    if [ timedout -ne 1 ]
    then
        echo "McKenzie caught an error: $@"
        curl -s --data "jobid=$SLURM_JOB_ID&status=error" http://${MCKENZIE_ENDPOINT}/hooks/update_job/
    fi
}
mckenzie_trap_cancel () {
    echo "McKenzie caught an cancel request: $@"
    curl -s --data "jobid=$SLURM_JOB_ID&status=canceled" http://${MCKENZIE_ENDPOINT}/hooks/update_job/
    
}

echo "Setting up error handling"

trap 'mckenzie_trap_timeout' USR1
trap 'mckenzie_trap_err' ERR
trap 'mckenzie_trap_cancel' EXIT HUP INT QUIT PIPE TERM SIGTERM SIGINT