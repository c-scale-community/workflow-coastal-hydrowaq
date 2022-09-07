# notebooks
In this folder you will find Jupyter Notebooks and the files to build the docker container (`Dockerfile`and `environment.yaml`) to run the notebooks.

* `visualise_delft3dfm.ipynb` \
    notebook with examples on how to visualise Delft3D FM output
* `dev.ipynb` \
    development notebook for troubleshooting and bug fixes

## `docker build`

To build the docker image run

    docker build --tag dfmipynb .

## `docker run`

    docker run -p 8888:8888 -v v $(pwd):/home/jovyan/work dfmipynb

Copy and past the URL starting with `http://127.0.0.1:8888/lab?token=...` to your browser

If you are running the above on a virtual machine in the cloud, replace `127.0.0.1` with the public IP of the virtual machine you are working on.
