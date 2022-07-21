FROM continuumio/miniconda3
WORKDIR /scripts

# put the envinroment.yaml file in the container
COPY environment.yml /tmp/environment.yml

# create the environment
RUN conda update -n base -c defaults conda
RUN conda env create -f /tmp/environment.yml

# pull the environment name out of the environment.yml
RUN echo "conda activate download_env" > /root/.bashrc
ENV PATH /opt/conda/envs/download_env/bin:$PATH

# copy the necessary scripts into the container
COPY README.md helpfile updatehelpfile.sh download_cmems_physics.py download_cmems_biogeochemistry.py download_era5.py /scripts/
# run the sed command to deal with windows users to get rid of ^M in updatehelpfile.sh
RUN ./updatehelpfile.sh

# tell the container to use bash
CMD ["cat", "helpfile"]
