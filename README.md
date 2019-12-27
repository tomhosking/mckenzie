# McKenzie 

<img src="https://github.com/tomhosking/mckenzie/raw/master/src/static/slurms.png" width="64">


A lightweight job tracker for the Slurm scheduler

Create a file `config.sh` in the root of the project, like this:

```
#!/bin/bash

export MCKENZIE_ENDPOINT=localhost:5002
```

Then run `python src/app.py`, then go to [http://localhost:5002/](http://localhost:5002/) to monitor your jobs.

Add the hooks to your job script like this:
```
/path/to/mckenzie/scripts/create_hook.sh $SLURM_JOB_ID
```