#!/bin/bash

SCRIPTPATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source "${SCRIPTPATH}/../config.sh"

MCKENZIE_HOOK=~/mckenzie/scripts/hook.sh


while getopts ":i:p:" opt; do
  case $opt in
    i) JOB_ID="$OPTARG"
    ;;
    p) JOB_PARTITION="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done


STATUS_RES="$(sacct -j $JOB_ID -o jobid,state -nP)"


# ${MCKENZIE_HOOK} -i $jobId -p $partition -s $status