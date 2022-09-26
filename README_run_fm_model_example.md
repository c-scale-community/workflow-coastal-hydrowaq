# Run the fm_model example in this repo

The below instructions are for running the workflow components for the example [fm_model](https://github.com/c-scale-community/use-case-hisea/tree/main/fm_model) included in this repo.

Once you've [set up your computing environment](https://github.com/c-scale-community/use-case-hisea/blob/main/README-setup_compute.md), follow the below steps in your operating system's command line interface.

## Setup the folder structure and clone the repo 

1. Navigate to the folder where you want to work, here we use the `$HOME` directory, which typically has the path `home/$USER`, where `$USER` is your username.

2. In `$HOME` create the directory `$HOME/data/download/` to which you will [download](https://github.com/c-scale-community/use-case-hisea/tree/main/scripts/download) the input data needed to run the model by typing:
		
		mkdir -p data/download/
   
3. In `$HOME` create the directory `$HOME/data/preprocout` where you can store the output from the [preprocessing](https://github.com/c-scale-community/use-case-hisea/tree/main/scripts/preprocessing) needed to run the model by typing:
		
	
		mkdir -p data/preprocout/
		
4. In `$HOME` create the directory `$HOME/data/postprocout` where you can store the output from the [postprocessing](https://github.com/c-scale-community/use-case-hisea/tree/main/scripts/postprocessing) by typing:
	
		mkdir -p data/postprocout/
		

5. In `$HOME` clone this repository by doing: 
		
		git clone https://github.com/c-scale-community/use-case-hisea.git
	
	This will create the folder `$HOME/use-case-hisea` containing all the files you need for the workflow. 
  
  Note that for private repos authentication will be required. The user will be prompted to enter the github username and the [personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).
	
	
## Build and pull the docker containers for the workflow
(Note: if you have permission denied error, add `sudo` before all commands) 

1. Navigate to `$HOME/use-case-hisea/scripts/download` and do: 
		
		docker build --tag download-input .
		
2. Navigate to `$HOME/use-case-hisea/scripts/preprocessing/era5` and do: 
		
		docker build --tag getera .
		
3. Navigate to `$HOME/use-case-hisea/scripts/preprocessing/tide_physical_chemical` and do: 
	
		docker build --tag preprocessing .
		
4. Navigate to `$HOME/use-case-hisea/scripts/postprocessing` and do:

		docker build --tag postprocess .
	
5. Pull docker image for Delft3D Flexible Mesh by doing: 
	
		docker login --username ... --password ...
	
		docker image pull deltares/delft3dfm:latest
	
6. Navigate to `$HOME/use-case-hisea/notebooks` and do:

		docker build --tag dfmipynb .

Check the created images:

	docker images

## Run the docker containers of the workflow one-by-one

Below are examples of the `docker run` commands for a 5-day simulation from 1-Apr-2022 to 5-Apr-2022 for a small model in Greece (the example [fm_model](https://github.com/c-scale-community/use-case-hisea/tree/main/fm_model) included in this repository).

1. Download ERA5 forcing data

		docker run -v /home/$USER/.cdsapirc:/root/.cdsapirc -v /home/$USER/data/download:/data download-input python download_era5.py --longitude_min 22.5 --longitude_max 24.5 --latitude_min 36.5 --latitude_max 38.5 --date_min '2022-04-01' --date_max '2022-04-05'
	
2. Download CMEMS physics data

		docker run -v /home/$USER/data/download:/data download-input python download_cmems_physics.py --username $CMEMS_USERNAME --password $CMEMS_PWD --longitude_min 22.5 --longitude_max 24.5 --latitude_min 36.5 --latitude_max 38.5 --date_min '2022-04-01' --date_max '2022-04-05'
	
3. Download CMEMS biogeochemistry data

		docker run -v /home/$USER/data/download:/data download-input python download_cmems_biogeochemistry.py --username $CMEMS_USERNAME --password $CMEMS_PWD --longitude_min 22.5 --longitude_max 24.5 --latitude_min 36.5 --latitude_max 38.5 --date_min '2022-04-01' --date_max '2022-04-05'
	
4. Preprocess CMEMS phyics and biogeochemistry data

		docker run -v /home/$USER/data/download/cmems:/data/input -v /home/$USER/use-case-hisea/fm_model:/data/model -v /home/$USER/data/preprocout:/data/output preprocessing boundary.py --interp true --simultaneous true --steric true --input /data/input --model /data/model --output /data/output
	
5. Preprocess tide data. For this step to work you must download FES2012 data. Copy your FES2012 tide data to `/home/$USER/data/download/fes2012`. Please go to https://www.aviso.altimetry.fr/es/data/products/auxiliary-products/global-tide-fes/description-fes2012.html for more details.

		docker run -v /home/$USER/data/download/fes2012:/data/input -v /home/$USER/use-case-hisea/fm_model:/data/model -v /home/$USER/data/preprocout:/data/output preprocessing tide.py --fespath /data/input --coords "22.5, 24.5, 36.5, 38.5" --pli south2.pli --pli east2.pli --output /data/output --model /data/model
		
6. Preprocess ERA5 data 

		docker run -v /home/$USER/data/download/era5:/data/input -v /home/$USER/data/preprocout:/data/output getera ERA5_convert2_FM_and_merge_allVars.py --input /data/input --output /data/output
		
7. Copy the output from preprocessing to your `fm_model/input` directory
	
		cp /home/$USER/data/preprocout/* /home/$USER/use-case-hisea/fm_model/input/.

8. Run Delft3D FM docker container (run the model). The `fm_model/` folder contains the `run_docker.sh` batch file in which you can set the number of cores and nodes (partitions).   

		docker run -v /home/$USER/use-case-hisea/fm_model:/data --shm-size=4gb --ulimit stack=-1 -t deltares/delft3dfm:latest

9. Post-process the model output. A single netcdf file (no partitions) will be created on a regular grid. You can define the output resolution (in the example: 500 x 400). Note that currently only the surface layer is extracted, this can be modified in the script.

		docker run -v /home/$USER/use-case-hisea/fm_model/DFM_OUTPUT_tttz_waq:/data/input -v /home/$USER/data/postprocout:/data/output postprocess tttz_waq_0000_map.nc 500 400

10. (*Note that this step doesn't depend on Step 9*) Set up JupyterHub to analyse your data in Jupyter Notebooks (An OpenStack VM requires that the VM security groups are configured to allow inbound connectivity - follow [these instructions](https://github.com/c-scale-community/use-case-hisea/tree/main/notebooks#getting-the-above-to-run-on-an-openstack-virtual-machine-in-the-cloud) to set that up)

		sudo docker run -p 8888:8888 -v /home/$USER/use-case-hisea/notebooks:/home/jovyan/work -v /home/$USER/use-case-hisea/fm_model/DFM_OUTPUT_tttz_waq:/home/jovyan/work/data_unstruct -v /home/$USER/data/postprocout:/home/jovyan/work/data_struct dfmipynb
		
	From the resultant output copy and paste the URL starting with `http://127.0.0.1:8888/lab?token=...` to your browser but replace `127.0.0.1` with the public IP of the virtual machine you are working on. This will give you access to the JupyerLab instance you've just launched.
