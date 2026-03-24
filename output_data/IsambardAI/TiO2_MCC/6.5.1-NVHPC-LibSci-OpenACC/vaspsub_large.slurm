#!/bin/bash
#SBATCH --job-name=VASP241
#SBATCH --nodes=4
#SBATCH --tasks-per-node=32
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:4
#SBATCH --time=2:0:0
#SBATCH --partition=gpu
#SBATCH --qos=standard
#SBATCH --account=z01
#SBATCH --gpu-freq=1410

module load openmpi/4.1.5-nvhpc235-cuda12
module load nvhpc/23.5-nompi

MKLROOT=/home/z01/z01/dc-turn1/software/VASP/intel-mkl-2025.3.0/mkl/2025.3
export LD_LIBRARY_PATH=$MKLROOT/lib/intel64:$LD_LIBRARY_PATH

VASP_EXE=/home/z01/z01/dc-turn1/software/VASP/vasp.6.5.1/bin/vasp_gam

ncore=1
cpn=4
threads=8
ngpu=4
nodes=$SLURM_JOB_NUM_NODES
casename="TiO2"
srunopts="--hint=nomultithread --distribution=block:block"

uuid=$(uuidgen)
rundir=${casename}_${uuid}

mkdir ${rundir}

cp input/KPOINTS ${rundir}/
cp input/POSCAR ${rundir}/
cp input/POTCAR ${rundir}/
cp input/INCAR.base ${rundir}/INCAR
echo "NCORE=${ncore}" >> ${rundir}/INCAR

cd ${rundir}

cores=$(( nodes * cpn ))
timestamp=$(date '+%Y%m%d%H%M')
resfile="${casename}_${nodes}nodes_${cores}cores_${threads}threads_${ncore}NCORE_${timestamp}.OUTCAR"
TMPDIR=$PWD

export OMP_NUM_THREADS=${threads}
export OMP_PLACES=cores
rm WAVECAR

nvidia-smi dmon -o DT -s p -d 30 > ../dmon-${SLURM_JOB_ID}.out &
dmon_id=$!

srun --nodes=$nodes --tasks-per-node=$cpn --cpus-per-task=$threads \
     --gres=gpu:$ngpu --hint=nomultithread --distribution=block:block \
     gpu_launch.sh $VASP_EXE

kill $dmon_id
sleep 30

mv OUTCAR ../${resfile}
cd ..
echo "++++ Slurm JobID = ${SLURM_JOB_ID}" >> $resfile
cat slurm-${SLURM_JOB_ID}.out >> $resfile
rm -r ${rundir}
echo "++++ Power data" >> $resfile
cat dmon-${SLURM_JOB_ID}.out >> $resfile

