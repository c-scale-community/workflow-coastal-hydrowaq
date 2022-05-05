FROM continuumio/miniconda3

WORKDIR /app

# Create the environment:
ADD environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "coastserv", "/bin/bash", "-c"]

COPY coastserv /app/coastserv/

COPY tide.py .
COPY boundary.py .

ENTRYPOINT ["conda", "run", "-n", "coastserv", "python"]
CMD ["boundary.py"]
