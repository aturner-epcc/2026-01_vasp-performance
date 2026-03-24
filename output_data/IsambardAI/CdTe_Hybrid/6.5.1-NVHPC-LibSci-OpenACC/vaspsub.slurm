#!/bin/bash
#SBATCH --job-name=CdTe64418
#SBATCH --nodes=64
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=72
#SBATCH --gpus-per-node=4
#SBATCH --time=6:0:0
#SBATCH --exclusive
#SBATCH --hint=nomultithread

module load craype-network-ofi
module load PrgEnv-nvidia
module load cudatoolkit/24.11_12.6
module load cray-mpich
module load craype-accel-nvidia90
module load craype-arm-grace
module load cray-fftw

export MPICH_GPU_SUPPORT_ENABLED=1
export LD_PRELOAD=/opt/cray/pe/mpich/8.1.32/gtl/lib/libmpi_gtl_cuda.so

VASP_EXE=/projects/u6cb/software/VASP/vasp.6.5.1/bin/vasp_ncl

ncore=1
kpar=8
cpn=4
threads=72
ngpu=4
nodes=$SLURM_JOB_NUM_NODES
casename="CdTe"
srunopts="--hint=nomultithread --distribution=block:block"

uuid=$(uuidgen)
rundir=${casename}_${uuid}

mkdir ${rundir}

cp input/KPOINTS ${rundir}/
cp input/POSCAR ${rundir}/
cp input/POTCAR ${rundir}/
cp input/INCAR.base ${rundir}/INCAR
echo "NCORE=${ncore}" >> ${rundir}/INCAR
echo "KPAR=${kpar}" >> ${rundir}/INCAR

cd ${rundir}

cores=$(( nodes * cpn ))
timestamp=$(date '+%Y%m%d%H%M')
resfile="${casename}_${nodes}nodes_${cores}cores_${threads}threads_${ncore}NCORE_${kpar}KPAR_${timestamp}.OUTCAR"
TMPDIR=$PWD

export OMP_NUM_THREADS=${threads}
export OMP_PLACES=cores
rm WAVECAR

nvidia-smi dmon -o DT -s p -d 30 > ../dmon-${SLURM_JOB_ID}.out &
dmon_id=$!

srun --hint=nomultithread --distribution=block:block $VASP_EXE

kill $dmon_id
sleep 30

mv OUTCAR ../${resfile}
cd ..
echo "++++ Slurm JobID = ${SLURM_JOB_ID}" >> $resfile
cat slurm-${SLURM_JOB_ID}.out >> $resfile
rm -r ${rundir}
echo "++++ Power data" >> $resfile
cat dmon-${SLURM_JOB_ID}.out >> $resfile

