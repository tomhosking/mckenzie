#!/bin/bash

# SCRIPT=$(readlink -f "$0")
SCRIPTPATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

source "${SCRIPTPATH}/../config.sh"

timedout=0
canceled=0
errored=0

mckenzie_trap_timeout () {
    echo "McKenzie caught a timeout"
    timedout=1
    curl -s --data "jobid=$SLURM_JOB_ID&partition=$SLURM_JOB_PARTITION&status=timeout" http://${MCKENZIE_ENDPOINT}/hooks/update_job/
}


mckenzie_trap_err () {
    echo "McKenzie caught an error: $timedout $canceled $errored $@"
    errored=1
    if [ $timedout = 0 ] && [ $canceled = 0 ] ; then
        echo "Signalling"
        curl -s --data "jobid=$SLURM_JOB_ID&partition=$SLURM_JOB_PARTITION&status=error&msg=Line $1" http://${MCKENZIE_ENDPOINT}/hooks/update_job/
    fi
}
mckenzie_trap_cancel () {
    echo "McKenzie caught an cancel request: $timedout $canceled $errored $@ "
    canceled=1
    if [ $timedout = 0 ] && [ $errored = 0 ] ; then
        echo "Signalling"
        canceled=1
        curl -s --data "jobid=$SLURM_JOB_ID&partition=$SLURM_JOB_PARTITION&status=cancelled" http://${MCKENZIE_ENDPOINT}/hooks/update_job/
    fi
}

echo "Setting up error handling"

trap 'mckenzie_trap_timeout' USR1
trap 'mckenzie_trap_err ${LINENO}' ERR
trap 'mckenzie_trap_cancel' HUP INT QUIT PIPE SIGTERM SIGINT