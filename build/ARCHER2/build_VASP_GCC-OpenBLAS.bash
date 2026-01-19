module restore
module load PrgEnv-gnu
module load cray-fftw
module load cray-hdf5-parallel
module remove cray-libsci
echo $LOADEDMODULES > loadedmodules.txt
cp makefile.include.ARCHER2_GCC_OpenBLAS_omp makefile.include
make veryclean
make all
