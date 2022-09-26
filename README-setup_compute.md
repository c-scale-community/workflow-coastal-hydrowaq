# Set up your computing environment

It is recommended to run the workflow in a Linux environment with [docker](https://www.docker.com/). This could be a virtual machine in the cloud, or your local computer. 

## Run in the cloud

The workflow components have been tested on the below C-SCALE federation's OpenStack cloud providers: 
* GRNET
* CESNET
* CloudFerro

Please see the [C-SCALE documentation for users](https://wiki.c-scale.eu/C-SCALE/c-scale-users/getting-started) on how to set up your computing environment on the C-SCALE federation.

Note the following dependencies.
* docker
* git

## Run locally

To run the workflow locally on a Linux or Apple Mac computer requires [docker desktop](https://www.docker.com/products/docker-desktop/). 

For Windows users running locally, it is recommended to 
1. [install the Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/install), 
2. upgrade to [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install#upgrade-version-from-wsl-1-to-wsl-2) 
3. [install the docker desktop WSL2 backend](https://docs.docker.com/desktop/windows/wsl/).
