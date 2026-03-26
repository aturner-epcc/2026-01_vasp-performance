timestamp=$(date '+%s')
scriptfile="vaspsub.slurm"

cat $1 | while read line
do
   if [[ "$line" != \#* ]]
   then
     read nodes cpn nthread ngpu ncore nrep < <(echo $line)
     stride=$(( 288 / cpn ))
     echo "#!/bin/bash" > ${scriptfile}
     echo "#SBATCH --job-name=VASP${nodes}${cpn}${ncore}${kpar}" >> ${scriptfile}
     echo "#SBATCH --nodes=$nodes" >> ${scriptfile}
     echo "#SBATCH --ntasks-per-node=${cpn}" >> ${scriptfile}
     echo "#SBATCH --cpus-per-task=${stride}" >> ${scriptfile}
     echo "#SBATCH --gpus-per-node=${ngpu}" >> ${scriptfile}
     cat preamble.txt >> ${scriptfile}
     echo "ncore=${ncore}" >> ${scriptfile}
     echo "cpn=${cpn}" >> ${scriptfile}
     echo "threads=${nthread}" >> ${scriptfile}
     echo "ngpu=${ngpu}" >> ${scriptfile}
     cat postamble.txt >> ${scriptfile}
     echo
     for i in $(seq 1 $nrep)
     do
       echo "Submitting $i of $nrep : $nodes $cpn $ncore $kpar"
       sbatch ${scriptfile}
     done
   fi
done
