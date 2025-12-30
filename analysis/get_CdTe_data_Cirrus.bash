
datadirs="6.5.1-GCC-LibSci 6.5.1-GCC-MKL 6.5.1-GCC-OpenBLAS 6.5.1-Intel-MKL"

system="Cirrus"

for dir in $datadirs
do
   if [ -f ${dir}.csv ]
   then
      rm ${dir}.csv
   fi
   python 2026-01_vasp-performance/analysis/cdte_output_file.py CdTe_Hybrid/${dir} ${dir} ${system} ${dir}.csv
done


first=true
for dir in $datadirs
do
   if [ -v first ]
   then
      cat ${dir}.csv > CdTe_combined.csv
      unset first
   else
      tail -n +2 ${dir}.csv >> CdTe_combined.csv
   fi
done

