# usage: in PuTTY: './run_set.sh'
#!/bin/bash

# INPUT
runid=${PWD##*/}
version=latest_dimr
nodes=2
cores=4
mdu=tttz_waq.mdu
# END OF INPUT

module load dflowfm
run_dflowfm.sh -v $version --partition:ndomains=$((nodes*cores)):icgsolver=6 $mdu
submit_dflowfm.sh -m $mdu -n $nodes -c $cores -v $version -j $runid -q test --bloomspecies bloom.spe --processlibrary proc_def.dat
