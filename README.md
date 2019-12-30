<h1>McKenzie <img src="https://github.com/tomhosking/mckenzie/raw/master/src/static/slurms.png" width="64" style="float:right; vertical-aign:middle;"></h1>


A lightweight job tracker for the Slurm scheduler

<img src="https://github.com/tomhosking/mckenzie/raw/master/src/static/screenshot.png">

## Setup

Create a file `config.sh` in the root of the project, like this:

```
#!/bin/bash

export MCKENZIE_ENDPOINT=localhost:5002
```

Then run `python src/app.py`, and go to [http://localhost:5002/](http://localhost:5002/) to monitor your jobs.

## Example usage

Set up the hook within your job script:
```
MCKENZIE_HOOK=/path/to/mckenzie/scripts/hook.sh
```

Use McKenzie error trapping:
```
source /mnt/ext/phd/mckenzie/scripts/error_trap.sh
```

Create a new job:
```
${MCKENZIE_HOOK} -a 1 -i $jobId -n $jobName
```

Set the status to 'warmup' and send the job config file to McKenzie:
```
${MCKENZIE_HOOK} -s warmup -c $1
```

Set the status to 'running' before starting the job, then 'complete' once it's done:
```
${MCKENZIE_HOOK} -s running
# ...do the job
${MCKENZIE_HOOK} -s complete
```

To update McKenzie from within a running job, look at the example code in `./lib/mckenzie.py`.

## Todo

  - [ ] Capture cancels for jobs that aren't running yet
  - [ ] Capture output files
  - [ ] Easy access to slurm logs
  - [ ] Pivot tables for hparams
  - [ ] Custom list orders/filters
  - [ ] Detail view