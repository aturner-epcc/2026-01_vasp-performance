
datadirs="6.5.1-GCC-MKL-OpenACC"

system="Tursa"

for dir in $datadirs
do
   if [ -f ${dir}.csv ]
   then
      rm ${dir}.csv
   fi
   python 2026-01_vasp-performance/analysis/tio2_output_file.py TiO2_MCC/${dir} ${dir} ${system} ${dir}.csv
done


first=true
for dir in $datadirs
do
   if [ -v first ]
   then
      cat ${dir}.csv > TiO2_combined_Tursa.csv
      unset first
   else
      tail -n +2 ${dir}.csv >> TiO2_combined_Tursa.csv
   fi
done

