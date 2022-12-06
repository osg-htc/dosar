# A few tips and tricks

### Objective
This exercise will teach you a few nifty commands to help you use Condor more easily.

## Tips for condor_q

Curious where your jobs are running? Use the `-run` option to see where jobs are running. (Idle jobs are not shown.) 
```
$ condor_q -run -nobatch

-- Submitter: frontal.cci.ucad.sn : <10.0.0.252:9645> : frontal.cci.ucad.sn
 ID      OWNER           SUBMITTED     RUN_TIME HOST(S)
  23.44  kagross         8/18 14:51   0+00:00:42 slot1@node2.cci.ucad.sn
  23.45  kagross         8/18 14:51   0+00:00:37 slot2@node2.cci.ucad.sn
  23.46  kagross         8/18 14:51   0+00:00:32 slot3@node2.cci.ucad.sn
  23.47  kagross         8/18 14:51   0+00:00:27 slot4@node2.cci.ucad.sn
  23.48  kagross         8/18 14:51   0+00:00:20 slot1@frontal.cci.ucad.sn
  23.49  kagross         8/18 14:51   0+00:00:14 slot2@frontal.cci.ucad.sn
```

`condor_q` can show you your job ClassAd. Recall back to the lecture and the discussion of ClassAds. For instance, you can look at the ClassAd for a single job:

```
$ condor_q -l 23.0

MaxHosts = 1
User = "kagross@frontal.cci.ucad.sn"
OnExitHold = false
CoreSize = 0
MachineAttrCpus0 = 1
WantRemoteSyscalls = false
MyType = "Job"
Rank = 0.0
CumulativeSuspensionTime = 0
MinHosts = 1
PeriodicHold = false
PeriodicRemove = false
Err = "simple.49.error"
ProcId = 49
EnteredCurrentStatus = 1408374244
UserLog = "/home/kagross/condor-test/s
... output trimmed ... 
```

There are some interesting parts you can check out. 

How many times has this job run? (It might be more than one if there were recoverable errors.)

```
$ condor_q -l 23.0 | grep JobRunCount
JobRunCount = 1
```

Where is the user log for this job? This is helpful when you assist someone else in debugging and they're not sure.

```
$ condor_q -l 23.0 | grep UserLog
UserLog = "/home/kagross/condor-test/simple.47.log"
```

What are the job's requirements? Condor automatically fills some in for you to make sure your job runs on a reasonable computer in our cluster, but you can override any of these. I've broken the output into multiple lines to explain it to you.

```
$ condor_q -l 23.0 | grep Requirements
Requirements =( TARGET.Arch == "X86_64" ) <em># Run on a 64-bit computer</em>
    && ( TARGET.OpSys == "LINUX" )  <em># Make sure you run on Linux</em>
    && ( TARGET.Disk >= RequestDisk ) <em># Make sure the default disk Condor is on has enough disk space.</em>
    && ( TARGET.Memory >= RequestMemory )  <em># Make sure the computer has enough memory</em>
    && ( TARGET.HasFileTransfer )  <em># Only run on a computer that can accept your files.</em>
```

What else can you find that's interesting in the ClassAd?

## Removing jobs

If you submit a job that you realize has a problem, you can remove it with `condor_rm`. For example: 

```
$ condor_q -nobatch

-- Submitter: osg-ss-submit.chtc.wisc.edu : <128.104.100.55:9618?sock=28867_10e4_2> : osg-ss-submit.chtc.wisc.edu
 ID      OWNER            SUBMITTED     RUN_TIME ST PRI SIZE CMD               
  29.0   roy             6/21 15:23   0+00:00:00 I  0   0.7  simple 60 10      

1 jobs; 0 completed, 0 removed, 2 idle, 0 running, 0 held, 0 suspended

$ condor_rm 29.0
Job 29.0 marked for removal

$ condor_q -nobatch

-- Submitter: osg-ss-submit.chtc.wisc.edu : <128.104.100.55:9618?sock=28867_10e4_2> : osg-ss-submit.chtc.wisc.edu
 ID      OWNER            SUBMITTED     RUN_TIME ST PRI SIZE CMD               

0 jobs; 0 completed, 0 removed, 1 idle, 0 running, 0 held, 0 suspended
```

A few tips:

   * You can remove all of your jobs with the `-all` option.
   * You can't remove other users jobs.
   * There are [fancy options to condor_rm](https://htcondor.readthedocs.io/en/v10_0/man-pages/condor_rm.html).  

## Historical information

You can see information about jobs that completed and are no longer in the queue with the <code>condor_history</code> command. It's rare that you want to see *all* the jobs, so try looking at jobs for just you:

```
$ condor_history YOUR_USER_ID
```

For example:
```
$ condor_history kagross
   9.9   kagross         7/31 12:44   0+00:00:03 C   7/31 12:44 /home/kagross/simple 9 9
   9.8   kagross         7/31 12:44   0+00:00:03 C   7/31 12:44 /home/kagross/simple 8 9
   9.11  kagross         7/31 12:44   0+00:00:03 C   7/31 12:44 /home/kagross/simple 11 9
   9.7   kagross         7/31 12:44   0+00:00:03 C   7/31 12:44 /home/kagross/simple 7 9
   9.5   kagross         7/31 12:44   0+00:00:02 C   7/31 12:44 /home/kagross/simple 5 9
   9.6   kagross         7/31 12:44   0+00:00:02 C   7/31 12:44 /home/kagross/simple 6 9
   9.3   kagross         7/31 12:44   0+00:00:02 C   7/31 12:44 /home/kagross/simple 3 9
   9.2   kagross         7/31 12:44   0+00:00:02 C   7/31 12:44 /home/kagross/simple 2 9
   9.1   kagross         7/31 12:44   0+00:00:03 C   7/31 12:44 /home/kagross/simple 1 9
   9.0   kagross         7/31 12:44   0+00:00:03 C   7/31 12:44 /home/kagross/simple 
   9.4   kagross         7/31 12:44   0+00:00:01 C   7/31 12:44 /home/kagross/simple 4 9
   8.0   kagross         7/31 12:42   0+00:00:07 C   7/31 12:42 /home/kagross/simple 4 10
...
```
