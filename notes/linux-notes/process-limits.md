# nproc limit exhausted on shared server 
Even can cause the failure of logging in

## Symptom
ssh drops immediately / fork: retry: Resource temporarily unavailable

## Cause
RLIMIT_NPROC counts per UID, and threads count too. (4096 --> 44096)
DataLoader workers × OMP threads multiply out.

## Diagnose
ps -L -u $USER --no-headers | wc -l
ps -u $USER -o pid,nlwp,etime,cmd --sort=-nlwp | head

## Fix
export OMP_NUM_THREADS=1
systemd-run --user --scope -p TasksMax=1500 python train.py

## Prevent
cron every 5 min logging task count
