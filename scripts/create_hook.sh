#!/bin/bash

SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
source "${SCRIPTPATH}/../config.sh"



HOSTNAME=$(hostname)


curl -s --data "jobid=$1&hostname=$SLURM_JOB_NODELIST&partition=$SLURM_JOB_PARTITION&status=submitted" http://${MCKENZIE_ENDPOINT}/hooks/create_job/