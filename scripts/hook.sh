#!/bin/bash

# SCRIPT=$(readlink -f "$0")
SCRIPTPATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source "${SCRIPTPATH}/../config.sh"

newjob=0
configfile=""
outputfile=""

while getopts ":a:s:c:o:m:n:i:p:r:" opt; do
  case $opt in
    a) newjob=1
    ;;
    s) status="$OPTARG"
    ;;
    c) configfile="$OPTARG"
    ;;
    o) outputfile="$OPTARG"
    ;;
    r) resultsfile="$OPTARG"
    ;;
    m) metric="$OPTARG"
    ;;
    n) jobname="$OPTARG"
    ;;
    i) SLURM_JOB_ID="$OPTARG"
    ;;
    p) SLURM_JOB_PARTITION="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

if [ $newjob -eq 1 ]
then
    curl -s --data "jobid=$SLURM_JOB_ID&partition=$SLURM_JOB_PARTITION&status=submitted" http://${MCKENZIE_ENDPOINT}/hooks/update_job/
elif [ -v status ]
then
    curl -s --data "jobid=$SLURM_JOB_ID&partition=$SLURM_JOB_PARTITION&status=$status&hostname=$SLURM_JOB_NODELIST" http://${MCKENZIE_ENDPOINT}/hooks/update_job/
elif [ -v jobname ]
then
    curl -s --data "jobid=$SLURM_JOB_ID&partition=$SLURM_JOB_PARTITION&jobname=$jobname" http://${MCKENZIE_ENDPOINT}/hooks/update_job/
fi

if [ "$configfile" != "" ]
then
    curl -F jobid=$SLURM_JOB_ID -F partition=$SLURM_JOB_PARTITION -F configfile=@$configfile http://${MCKENZIE_ENDPOINT}/hooks/update_job/
fi


if [ "$outputfile" != "" ]
then
    curl -F jobid=$SLURM_JOB_ID -F partition=$SLURM_JOB_PARTITION -F outputfile=@$outputfile http://${MCKENZIE_ENDPOINT}/hooks/update_job/
fi

if [ "$resultsfile" != "" ]
then
    curl -F jobid=$SLURM_JOB_ID -F partition=$SLURM_JOB_PARTITION -F resultsfile=@$resultsfile http://${MCKENZIE_ENDPOINT}/hooks/update_job/
fi