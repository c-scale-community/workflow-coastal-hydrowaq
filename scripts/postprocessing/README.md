# Output2RegularGrid
A program for converting DFlowFM map output to a regular spaced grid.

# Docker container
- mount /data/input -> Output DFlowFM
- mount /data/output -> here the regular grid nc file is written

# nc2regularGrid_listComprehension.py
This script expects 3 paramaters:
- mapfile: 0th partition of your NetCDF map output
- xpoints: number of points you wish to include into your regular grid
- ypoints: number of points you wish to include into your regular grid

# Example Docker build

docker build -t postprocess .

# Example Docker run

docker run -v <path to fm output>:/data/input -v <path to regular grid output folder>:/data/output hisea tttz_waq_0000_map.nc 500 400
