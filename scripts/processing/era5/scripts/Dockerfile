FROM continuumio/miniconda3

WORKDIR /app

# Create the environment:
ADD environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "coastserv", "/bin/bash", "-c"]

#COPY coastserv /app/coastserv/

COPY era_maps_allVars.py .
COPY ERA5_convert2_FM_and_merge_allVars.py .

ENTRYPOINT ["conda", "run", "-n", "coastserv", "python"]
CMD ["ERA5_convert2_FM_and_merge_allVars.py"]
