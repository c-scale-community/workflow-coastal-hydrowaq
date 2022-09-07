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

    docker run -p 8888:8888 -v $(pwd):/home/jovyan/work dfmipynb

The above command will return output similar to the below:
```
[I 2022-09-07 13:34:03.166 ServerApp] jupyterlab | extension was successfully linked.
[W 2022-09-07 13:34:03.180 NotebookApp] 'ip' has moved from NotebookApp to ServerApp. This config will be passed to ServerApp. Be sure to update your config before our next release.
[W 2022-09-07 13:34:03.181 NotebookApp] 'port' has moved from NotebookApp to ServerApp. This config will be passed to ServerApp. Be sure to update your config before our next release.
[W 2022-09-07 13:34:03.181 NotebookApp] 'port' has moved from NotebookApp to ServerApp. This config will be passed to ServerApp. Be sure to update your config before our next release.
[I 2022-09-07 13:34:03.205 ServerApp] Writing Jupyter server cookie secret to /home/jovyan/.local/share/jupyter/runtime/jupyter_cookie_secret
[I 2022-09-07 13:34:03.817 ServerApp] nbclassic | extension was successfully linked.
[I 2022-09-07 13:34:03.859 ServerApp] nbclassic | extension was successfully loaded.
[I 2022-09-07 13:34:03.860 LabApp] JupyterLab extension loaded from /opt/conda/lib/python3.9/site-packages/jupyterlab
[I 2022-09-07 13:34:03.860 LabApp] JupyterLab application directory is /opt/conda/share/jupyter/lab
[I 2022-09-07 13:34:03.865 ServerApp] jupyterlab | extension was successfully loaded.
[I 2022-09-07 13:34:03.867 ServerApp] Serving notebooks from local directory: /home/jovyan
[I 2022-09-07 13:34:03.867 ServerApp] Jupyter Server 1.18.1 is running at:
[I 2022-09-07 13:34:03.867 ServerApp] http://8ca53708c6b0:8888/lab?token=...
[I 2022-09-07 13:34:03.867 ServerApp]  or http://127.0.0.1:8888/lab?token=...
[I 2022-09-07 13:34:03.867 ServerApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 2022-09-07 13:34:03.871 ServerApp] 
    
    To access the server, open this file in a browser:
        file:///home/jovyan/.local/share/jupyter/runtime/jpserver-7-open.html
    Or copy and paste one of these URLs:
        http://8ca53708c6b0:8888/lab?token=...
     or http://127.0.0.1:8888/lab?token=...
```

If you are running the above locally, copy and past the URL starting with `http://127.0.0.1:8888/lab?token=...` to your browser.

If you are running the above on a virtual machine in the cloud, replace `127.0.0.1` with the public IP of the virtual machine you are working on, and put that URL into your browser.
