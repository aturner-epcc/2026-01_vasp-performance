module restore
module load PrgEnv-gnu
module load cray-fftw
module load cray-hdf5-parallel
module load libxc
module load wannier90
module remove cray-libsci
module load intel-mkl

echo $LOADEDMODULES > loadedmodules.txt
cp makefile.include.CirrusEX_GCC_MKL_omp makefile.include
make veryclean
make all
