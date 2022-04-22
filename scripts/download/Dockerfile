FROM continuumio/miniconda3
WORKDIR /scripts

# put the envinroment.yaml file in the container
COPY environment.yml /tmp/environment.yml

# create the enfironment
RUN conda update -n base -c defaults conda
RUN conda env create -f /tmp/environment.yml

# pull the environment name out of the environment.yml
RUN echo "conda activate download_env" > /root/.bashrc
ENV PATH /opt/conda/envs/download_env/bin:$PATH

# copy the necessary scripts into the container
COPY README.md download_cmems_biogeochemistry.sh download_cmems_physics.sh download_era5.py /scripts/.

# tell the container to use bash
ENTRYPOINT ["bash", "-c"]
