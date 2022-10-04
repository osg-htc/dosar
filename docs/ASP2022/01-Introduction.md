# High Throughput Computing and Condor Introduction

## Preliminaries

You will need your Gmail or GitHub credentials for this session. 

   * You might want to refer to the [online Condor 8.6 manual](https://htcondor.org/documentation/htcondor.html).<br>
   * You may enjoy browsing the [Condor web page](http://www.cs.wisc.edu/condor/).<br>

## Which Condor?
We will be using Condor 9.0.17, which is a recent production version of Condor.

Condor has two coexisting types of releases at any given time: Feature (development) and Long Term Support (stable). Condor 9.0.17 is considered a stable release, and you can know it is stable because the second digit (a 0 in this cases) is an even number. In a given stable series, all versions have the same features (for example 9.0.16 and 9.0.17 have the same set of features) and differ only in bug fixes.

## Where you will work

Today you will log into https://notebook.ospool.osg-htc.org/hub/login for all of your exercises:

Login on submission node using a web browser:

https://notebook.ospool.osg-htc.org/hub/login

Click on 'Sign in with CILogon'.
Select the Identity Provider Google (or GitHub).
Click 'Login'.
Log into your Google account.
Click the 'Server Option' 'Data Science'.
Click 'Start'. This will take some time.
In the 'Launcher' window, click on 'Terminal' (bottom left).

When you login to the machine you will be in your "home directory".  We recommend that you work in this directory as nobody else can modify the files here.

You can always return to your home directory by running the command

<pre><code>
$ <b>cd ~</b>
</code></pre>

## The Exercises

Throughout the Condor exercises, you will be given a fair amount of guidance. In several spots, there are suggestions for extra exercises to do "on your own" or as "challenges". Since you aren't being graded, there is no extra credit for doing them, but we encourage you to try them out. If you prefer, you can come back to the extra credit after you've completed the basic exercises. If you simply cruise through the exercises, you'll probably have free time--we encourage you to delve in more deeply.

For all of the exercises, we'll assume that you are logged into user-training.osgconnect.net. You should have received your name and password for user-training.osgconnect.net at the beginning of the Computation Infrastructures lecture.
