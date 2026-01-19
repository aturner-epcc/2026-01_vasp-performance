module load /home/y07/shared/tursa-modules/setup-env
module load openmpi/4.1.5-nvhpc235-cuda12
module load nvhpc/23.5-nompi

export OMPI_CC=nvc
export OMPI_CXX=nvc++
export OMPI_FC=nvfortran

cp makefile.include.tursa_nvhpc makefile.include
make veryclean
make all
