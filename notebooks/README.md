# notebooks
In this folder you will find Jupyter Notebooks and the files to build the docker container (`Dockerfile`and `environment.yaml`) to run the notebooks.

* 'visualise_delft3dfm.ipynb' \
    notebook with examples on how to visualise Delft3D FM output
* 'dev.ipynb' \
    development notebook for troubleshoot and bug fixes

## `docker build`

To build the docker image run

    docker build --tag hydro-nb .

## `docker run`

    docker run -p 8888:8888 -v v $(pwd):/home/jovyan/work hydro-nb

Copy-paste the output from the above command to your browser.
