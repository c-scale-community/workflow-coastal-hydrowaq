FROM continuumio/miniconda3
MAINTAINER Josefine Wilms <fine.wilms@deltares.nl>

WORKDIR /app

# Create the environment:
ADD environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "coastserv", "/bin/bash", "-c"]

COPY coastserv /app/coastserv/

COPY test_tide.py .
COPY test_boundary.py .

ENTRYPOINT ["conda", "run", "-n", "coastserv", "python"]
CMD ["test_boundary.py"]
