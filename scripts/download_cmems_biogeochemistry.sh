#!/bin/bash

motu="https://nrt.cmems-du.eu/motu-web/Motu"
service_id="GLOBAL_ANALYSIS_FORECAST_BIO_001_028"
product_id="global-analysis-forecast-bio-001-028-daily"
longitude_min=22.5
longitude_max=24.5
latitude_min=36.5
latitude_max=38.5
date_min=$(date --date="5 days ago" +"%Y-%m-%d")
date_max=$(date +"%Y-%m-%d")
depth_min=0.493
depth_max=5727.918000000001
variables=("no3" "o2" "phyc" "po4" "si")
out_dir="/home/centos/hisea/data/cmems"
user=""
pwd=""

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