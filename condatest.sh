#!/usr/bin/env bash -e

# set the conda installation folder
CONDA_DIR=~/conda-envs/use-case-hisea

# activate conda once
source ${CONDA_DIR}/etc/profile.d/conda.sh

# activate download env
conda activate download_env
which python
python --version

# activate preprocessing env
conda activate preprocessing
which python
python --version

# activate postprocessing env
conda activate postprocessing
which python
python --version
