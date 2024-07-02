# Our Condor Installation

## Objective

This exercise should help you understand the basics of how Condor is installed, what Condor processes (a.k.a. daemons) are running, and what they do.

## Login to the Condor submit computer
Before you start, make sure you are logged into `https://notebook.ospool.osg-htc.org/hub/login` with your Gmail or GitHub account.

```
$ hostname
jupyter-...-40gmail-2ecom
```

## Looking at our Condor installation

How do you know what version of Condor you are using? Try <code>condor_version</code>: 

```
$ condor_version
$CondorVersion: 23.7.2 2024-05-16 BuildID: 733409 PackageID: 23.7.2-0.2 GitSHA: 585ec167 $
$CondorPlatform: X86_64-Ubuntu_22.04 $
```

Note that the "CondorPlatform" reports the type of computer we built it on, _not necessarily_ the computer we're running on. It was built on Ubuntu 22.04, but you might notice that we're running on Ubuntu 22.04.4, which is a slightly newer version.

### Extra Tip: The OS version

Do you know how to find the OS version? You can usually look in /etc/issue to find out:

```
$ cat /etc/issue
Ubuntu 22.04.4 LTS \n \l
```

Or you can run:

```
$ lsb_release -a
o No LSB modules are available.
Distributor ID: Ubuntu
Description:    Ubuntu 22.04.4 LTS
Release:        22.04
Codename:       jammy
```

Where is Condor installed? 

```
# Show the location of the condor_q binary
$ which condor_q
/usr/bin/condor_q
```

Condor has some configuration files that it needs to find. They are in the standard location, `/etc/condor`

```
$ ls /etc/condor
condor_config  condor_config.local  config.d  ganglia.d
```

Condor has some directories that it keeps records of jobs in. Remember that each submission computer keeps track of all jobs submitted to it. That's in the local directory: 

```
$ condor_config_val -v LOCAL_DIR
LOCAL_DIR = /home/jovyan/.condor/local
 # at: /etc/condor/condor_config.local, line 2
 # raw: LOCAL_DIR = $ENV(HOME)/.condor/local

$ s -CF /home/jovyan/.condor/local/
cred_dir/  execute/  lock/  log/  run/  spool/
```

The spool directory is where Condor keeps the jobs you submit, while the execute directory is where Condor keeps running jobs. Since this is a submission-only computer, it should be empty.

Check if Condor is running.  Your output will differ slightly, but you should see `condor_master` with the other Condor daemons listed under it:

```
$ ps auwx --forest | grep condor_ | grep -v grep
jovyan      17  0.0  0.0  23844  7240 ?        Ss   19:32   0:00 condor_master
jovyan      18  0.0  0.0   7620  2372 ?        S    19:32   0:00  \_ condor_procd -A /home/jovyan/.condor/local/run/procd_pipe -L /home/jovyan/
jovyan      19  0.0  0.0  18200  8284 ?        Ss   19:32   0:00  \_ condor_shared_port
jovyan      20  0.0  0.0  20180  9640 ?        Ss   19:32   0:00  \_ condor_collector
jovyan      21  0.0  0.0  20688 10028 ?        Ss   19:32   0:00  \_ condor_negotiator
jovyan      22  0.0  0.0  21320 10104 ?        Ss   19:32   0:00  \_ condor_schedd
jovyan      23  0.0  0.0  21136 10172 ?        Ss   19:32   0:00  \_ condor_startd
```

For this version of Condor there are these processes running: the condor_master, the condor_schedd, the condor_procd, the condor_collector, the condor_negotiator, and condor_shared_port. In general, you might see many different Condor processes. Here's a list of the processes:

   * *condor_master*: This program runs constantly and ensures that all other parts of Condor are running. If they hang or crash, it restarts them.
   * *condor_schedd*: If this program is running, it allows jobs to be submitted from this computer--that is, your computer is a "submit machine". This will advertise jobs to the central manager so that it knows about them. It will contact a condor_startd on other execute machines for each job that needs to be started.
   * *condor_procd:* This process helps Condor track process (from jobs) that it creates
   * *condor_collector:* This program is part of the Condor central manager. It collects information about all computers in the pool as well as which users want to run jobs. It is what normally responds to the condor_status command. At the school, it is running on a different computer, and you can figure out which one: 

Other daemons include:

   * *condor_negotiator:* This program is part of the Condor central manager. It decides what jobs should be run where. It is run on the same computer as the collector.
   * *condor_startd:* If this program is running, it allows jobs to be started up on this computer--that is, your computer is an "execute machine". This advertises your computer to the central manager so that it knows about this computer. It will start up the jobs that run.
   * *condor_shadow:* For each job that has been submitted from this computer, there is one condor_shadow running. It will watch over the job as it runs remotely. In some cases it will provide some assistance (see the standard universe later.) You may or may not see any condor_shadow processes running, depending on what is happening on the computer when you try it out. 
   * *condor_shared_port:* Used to assist Condor with networking by allowing multiple Condor processes to share a single network port. 


## condor_q

You can find out what jobs have been submitted on your computer with the condor_q command: 

```
$ condor_q -nobatch
-- Schedd: jovyan@jupyter-email-3ahorst-2eseverini-40gmail-2ecom : <127.0.0.1:9618?... @ 07/02/24 19:44:46
 ID      OWNER            SUBMITTED     RUN_TIME ST PRI SIZE CMD

Total for query: 0 jobs; 0 completed, 0 removed, 0 idle, 0 running, 0 held, 0 suspended 
Total for jovyan: 0 jobs; 0 completed, 0 removed, 0 idle, 0 running, 0 held, 0 suspended 
Total for all users: 0 jobs; 0 completed, 0 removed, 0 idle, 0 running, 0 held, 0 suspended

0 jobs; 0 completed, 0 removed, 0 idle, 0 running, 0 held, 0 suspended 
```

The output that you see will be different depending on what jobs are running. Notice what we can see from this:

   * *ID*: We can see each jobs cluster and process number. For the first job, the cluster is 60256 and the process is 0.
   * *OWNER*: We can see who owns the job.
   * *SUBMITTED*: We can see when the job was submitted
   * *RUN_TIME*: We can see how long the job has been running.
   * *ST*: We can see what the current state of the job is. I is idle, R is running.
   * *PRI*: We can see the priority of the job.
   * *SIZE*: We can see the memory consumption of the job.
   * *CMD*: We can see the program that is being executed. 

### Extra Tip

What else can you find out with condor_q? Try any one of:

   * `man condor_q`  (Will not work on this ospool training machine.)
   * `condor_q -help`
   * [condor_q from the online manual](https://htcondor.readthedocs.io/en/v10_0/man-pages/condor_q.html)

### Double bonus points

How do you use the `-constraint` or `-format` options to `condor_q`? When would you want them? When would you use the -l option? This might be an easier exercise to try once you submit some jobs.

## condor_status

You can find out what computers are in your Condor pool. (A pool is similar to a cluster, but it doesn't have the connotation that all computers are dedicated full-time to computation: some may be desktop computers owned by users.) To look, use condor_status:

```
$ condor_status
Name                                                 OpSys      Arch   State     Activity LoadAv Mem     ActvtyTime

slot1@jupyter-email-3ahorst-2eseverini-40gmail-2ecom LINUX      X86_64 Unclaimed Idle      0.000 257750  0+00:14:02

               Total Owner Claimed Unclaimed Matched Preempting  Drain Backfill BkIdle

  X86_64/LINUX     1     0       0         1       0          0      0        0      0

         Total     1     0       0         1       0          0      0        0      0
...
```

Let's look at exactly what you can see (this will look differently on different condor pools):

   * *Name*: The name of the computer. Sometimes this gets chopped off, like above.
   * *OpSys*: The operating system, though not at the granularity you may wish: It says "Linux" instead of which distribution and version of Linux.
   * *Arch*: The architecture, such as INTEL or PPC.
   * *State*: The state is often Claimed (when it is running a Condor job) or Unclaimed (when it is not running a Condor job). It can be in a few other states as well, such as Matched.
   * *Activity*: This is usually something like Busy or Idle. Sometimes you may see a computer that is Claimed, but no job has yet begun on the computer. Then it is Claimed/Idle. Hopefully this doesn't last very long.
   * *LoadAv*: The load average on the computer.
   * *Mem*: The computers memory in megabytes.
   * *ActvtyTime*: How long the computer has been doing what it's been doing. 

### Extra credit

What else can you find out with condor_status? Try any one of:

   * `man condor_status`
   * `condor_status -help`
   * [condor_status from the online manual](https://htcondor.readthedocs.io/en/v10_0/man-pages/condor_status.html)

Note in particular the options like `-master` and `-schedd`. When would these be useful? When would the `-l` option be useful? 

