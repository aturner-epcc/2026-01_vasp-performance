module load craype-network-ofi
module load PrgEnv-nvidia 
module load cudatoolkit/24.11_12.6
module load cray-mpich
module load craype-accel-nvidia90
module load craype-arm-grace
module load cray-fftw

export MPICH_GPU_SUPPORT_ENABLED=1

cp makefile.include.isambardai makefile.include
# make veryclean
make all

