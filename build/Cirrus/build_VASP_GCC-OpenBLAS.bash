module restore
module swap PrgEnv-cray PrgEnv-gnu
module load cray-fftw
module load cray-hdf5-parallel
module load libxc
module load wannier90
module remove cray-libsci


echo $LOADEDMODULES > loadedmodules.txt
cp makefile.include.CirrusEX_GCC_OpenBLAS_omp makefile.include
make veryclean
make all
