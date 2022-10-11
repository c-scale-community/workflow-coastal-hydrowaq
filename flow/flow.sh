#!/usr/bash -l

# This script runs in the Cloud or local machine
# first make it executable: chmod +x flow.sh

# load GRNET-HPC (ARIS) framework
# functions can be used as commands
source ./env

# pre-process data
# do Cloud pre-processing
# create the directory and the necessary content
# in ./input

# send data to GRNET-HPC (ARIS)
send

# submit the job to GRNET-HPC (ARIS)
# and save the job id into the file ./job
# it assumes that send command has been applied
# so that the submit.sh script be in GRNET-HPC (ARIS) (in order to be submitted)
submit

# this loop will continue until the job is completed
# you could add your own functionality
# e.g.  Output can be RUNNING, RESIZING, SUSPENDED, COMPLETED
# for more info run "man sacct" in GRNET-HPC (ARIS)
until check | grep -q "COMPLETED"; do
   :
    echo 'Waiting until the submitted job is done'

    # wait for 60 seconds until next check
    # set value accordingly
    sleep 60
done

# running from this steps and beyond, it means
# that the job has finished

# retrieve data from GRNET-HPC (ARIS)
retrieve

# post-process data
# do Cloud post-processing


# delete data from GRNET-HPC (ARIS)
# also the local (cloud) job file
clean

# the commands: send, submit, check, retrieve
# have been exported to this script via the sourcing of ./env file

