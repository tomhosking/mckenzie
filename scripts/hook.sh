#!/bin/bash

# SCRIPT=$(readlink -f "$0")
SCRIPTPATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source "${SCRIPTPATH}/../config.sh"

newjob=0
configfile=""
outputfile=""

while getopts ":a:s:c:o:m:n:i:" opt; do
  case $opt in
    a) newjob=1
    ;;
    s) status="$OPTARG"
    ;;
    c) configfile="$OPTARG"
    ;;
    o) outputfile="$OPTARG"
    ;;
    m) metric="$OPTARG"
    ;;
    n) jobname="$OPTARG"
    ;;
    i) SLURM_JOB_ID="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

if [ $newjob -eq 1 ]
then
    curl -s --data "jobid=$SLURM_JOB_ID&status=submitted" http://${MCKENZIE_ENDPOINT}/hooks/update_job/
elif [ -v status ]
then
    curl -s --data "jobid=$SLURM_JOB_ID&status=$status&hostname=$SLURM_JOB_NODELIST&partition=$SLURM_JOB_PARTITION" http://${MCKENZIE_ENDPOINT}/hooks/update_job/
elif [ -v jobname ]
then
    curl -s --data "jobid=$SLURM_JOB_ID&jobname=$jobname" http://${MCKENZIE_ENDPOINT}/hooks/update_job/
fi

if [ "$configfile" != "" ]
then
    echo "TODO! upload config file $configfile"
fi


if [ "$outputfile" != "" ]
then
    echo "TODO! upload results file $outputfile"
fi