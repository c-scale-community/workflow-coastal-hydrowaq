FROM jupyter/minimal-notebook:lab-3.2.5

USER root

# put the environment.yaml file int the container
COPY environment.yaml /tmp/environment.yaml

# create the environment
RUN conda update -n base -c defaults conda
RUN conda env create -f /tmp/environment.yaml

# activate the environment
RUN echo ". /opt/conda/etc/profile.d/conda.sh \
	  conda activate dfm_tools_env" >> /home/jovyan/.bashrc && \
    echo ". /opt/conda/etc/profile.d/conda.sh \
	  conda activate dfm_tools_env" >> /root/.bashrc

#ENV PATH /opt/conda/envs/dfm_tools_env/bin:$PATH

RUN jupyter labextension install jupyter-matplotlib

# edit config
#RUN echo "c.NotebookApp.iopub_data_rate_limit = 10000000" >> /home/jovyan/.jupyter/jupyter_notebook_config.py \
 #&& echo "c.NotebookApp.iopub_msg_rate_limit = 100000" >> /home/jovyan/.jupyter/jupyter_notebook_config.py
#RUN chmod 777 /home/jovyan/.config

USER ${NB_UID}

CMD ["jupyter", "lab", "--port=8888", "--no-browser", "--ip=0.0.0.0"]
