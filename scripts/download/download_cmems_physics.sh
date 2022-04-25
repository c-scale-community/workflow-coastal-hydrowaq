#!/bin/bash
Help()
{
  # Display Help
  echo "This script downloads the necessary hydrodynmic input data from
  Copernicus."
  echo
  echo "Syntax: download_cmems_physics.sh username password longitude_min
  longitude_max latitude_min latitude_max date_min date_max"
}

user="$1"
pwd="$2"
longitude_min=$3 #22.5
longitude_max=$4 #24.5
latitude_min=$5 #36.5
latitude_max=$6 #38.5
date_min=$7 #$(date --date="5 days ago" +"%Y-%m-%d")
date_max=$8 #$(date +"%Y-%m-%d")

motu="https://nrt.cmems-du.eu/motu-web/Motu"
service_id="GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS"
product_id="global-analysis-forecast-phy-001-024"
depth_min=0.493
depth_max=5727.918000000001
variables=("thetao" "bottomT" "so" "zos" "uo" "vo")
out_dir="/data/cmems"

for v in ${variables[*]}
do
out_name="${v}_${date_min}_${date_max}.nc"
echo ${v}
echo $out_name
python -m motuclient \
    --motu $motu \
    --service-id $service_id \
    --product-id $product_id \
    --longitude-min $longitude_min \
    --longitude-max $longitude_max \
    --latitude-min $latitude_min \
    --latitude-max $latitude_max \
    --date-min $date_min \
    --date-max $date_max \
    --depth-min $depth_min \
    --depth-max $depth_max \
    --variable $v \
    --out-dir $out_dir \
    --out-name $out_name \
    --user "$user" \
    --pwd "$pwd"
done
