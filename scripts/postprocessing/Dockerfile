FROM continuumio/miniconda3

# put the environment.yml into the container
COPY environment.yml /tmp/environment.yml

# create the conda environment
RUN conda update -n base -c defaults conda
RUN conda env create -f /tmp/environment.yml

# Pull the environment name out of the environment.yml
RUN echo "source activate env" > /root/.bashrc
ENV PATH /opt/conda/envs/env/bin:$PATH

COPY *.py /root/
ENTRYPOINT ["python", "/root/nc2regularGrid_listComprehension.py"]
CMD ["tttz_waq_0000_map.nc", "500", "400"]
