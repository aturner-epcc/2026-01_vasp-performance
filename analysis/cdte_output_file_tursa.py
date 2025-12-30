

import re
import os
import sys
import glob
import subprocess
import csv

def main():
    
    resdir = sys.argv[1]
    test_label = sys.argv[2]
    system_name = sys.argv[3]
    outfile = sys.argv[4]

    # Here we generate the list of files from a directory name
    print(resdir)
    searchstr = resdir + "/*.OUTCAR"
    filelist = glob.glob(searchstr)

    # Loop over files extracting the data as CSV
    first = True
    for file in filelist:
        print(file)
        if first:
            get_file_data(file, test_label, system_name, outfile, header=True)
            first = False
        else:
            get_file_data(file, test_label, system_name, outfile)

def get_file_data(filename, test_label, system_name, outfile, header=False):
    """Extract the details from output
    """
    infile = open(filename, 'r')
    resdict = {}

    # Defaults
    resdict['Threads'] = 1
    resdict['Label'] = test_label
    resdict['System'] = system_name

    # Values from file name
    resdict['File'] = os.path.abspath(filename)
    tokens = filename.split('.')
    filestem = ''
    for token in tokens:
        if 'nodes' in token:
            filestem = token
    tokens = filestem.split('_')
    nodestring = None
    resdict['JobID'] = tokens[6].replace('i','')
    result = subprocess.run(['sacct', '-Xn', '--format=consumedenergyraw', '-j', resdict['JobID']], stdout=subprocess.PIPE)
    energy = result.stdout.decode('UTF-8')
    resdict['Energy'] = int(energy.rstrip())
    for token in tokens:
        if 'nodes' in token:
            nodestring = token
    resdict['Nodes'] = int(nodestring.replace('nodes',''))

    # Values from the file contents
    inpower = False
    totpower = 0.0
    npower = 0
    for line in infile:
        if inpower:
            if re.search('#', line):
                pass
            else:
                line = line.strip()
                tokens = line.split()
                power = float(tokens[3])
                if power > 120.0:
                    totpower += power
                    npower += 1
        else:
            if re.search('++++ Power data', line):
                inpower = True
            elif re.search('Offloading initialized'):
                line = line.strip()
                tokens = line.split()
                resdict['GPUs'] = int(tokens[3])
            elif re.search('LOOP+:', line):
                line = line.strip()
                tokens = line.split()
                resdict['LOOP+ Time'] = float(tokens[6])
            elif re.search('running on ', line):
                line = line.strip()
                tokens = line.split()
                resdict['Processes'] = int(tokens[2])
            elif re.search('threads', line):
                line = line.strip()
                tokens = line.split()
                if "****" not in tokens[1]:
                resdict['Processes'] = int(tokens[1])
                resdict['Threads'] = int(tokens[4])
            elif re.search('mpi-ranks', line):
                line = line.strip()
                tokens = line.split()
                if "****" not in tokens[1]:
                resdict['Processes'] = int(tokens[1])
            elif re.search('Each process may', line):
                line = line.strip()
                tokens = line.split()
                resdict['Threads'] = int(tokens[6])
            elif re.search('executed on', line):
                line = line.strip()
                tokens = line.split()
                resdict['Date'] = f"{tokens[4].strip()} {tokens[5].strip()}"
            elif re.search('distr:', line):
                if not 'NCORE' in resdict:
                line = line.strip()
                tokens = line.split()
                resdict['NCORE'] = int(tokens[5].strip())
                resdict['NPAR'] = int(tokens[7].strip())
            elif re.search('distrk:', line):
                if not 'KPAR' in resdict:
                line = line.strip()
                tokens = line.split()
                kpar = int(tokens[6].strip())
                procperk = int(tokens[4].strip())
                resdict['KPAR'] = kpar
                resdict['Processes'] = procperk * kpar
            elif re.search('NBANDS=', line):
                line = line.strip()
                tokens = line.split()
                resdict['Bands'] = int(tokens[14].strip())
            elif re.search('Elapsed', line):
                line = line.strip()
                tokens = line.split()
                resdict['Runtime'] = float(tokens[3].strip())    
    infile.close()

    # Computed values
    resdict['Processes'] = resdict.get('Processes', 1)
    resdict['Cores'] = resdict['Processes'] * resdict['Threads']
    

    # Append this result to the CSV file if the run completed successfully
    if 'Runtime' in resdict.keys():
        # Compute energy based on mean power draw
        meanpower = totpower / npower
        print(f'Mean power = {meanpower:.3f}')
        resdict['Energy'] = meanpower * resdict['Runtime']
        # Write data
        outstream = open(outfile, "a", newline="")
        if header:
            headerline = "System,Label,File,JobID,Date,Nodes,Cores,Processes,Threads,GPUs,Energy,KPAR,NCORE,NPAR,Bands,LOOP+ Time,Runtime\n"
            outstream.write(headerline)
            rowlist = [
                    resdict['System'],
                    resdict['Label'],
                    resdict['File'],
                    resdict['JobID'],
                    resdict['Date'],
                    resdict['Nodes'],
                    resdict['Cores'],
                    resdict['Processes'],
                    resdict['Threads'],
                    resdict['GPUs'],
                    resdict['Energy'],
                    resdict['KPAR'],
                    resdict['NCORE'],
                    resdict['NPAR'],
                    resdict['Bands'],
                    resdict['LOOP+ Time'],
                    resdict['Runtime'],
                    ]
            rowline = ','.join(str(x) for x in rowlist)
            outstream.write(rowline + "\n")
        else:
            rowlist = [
                    resdict['System'],
                    resdict['Label'],
                    resdict['File'],
                    resdict['JobID'],
                    resdict['Date'],
                    resdict['Nodes'],
                    resdict['Cores'],
                    resdict['Processes'],
                    resdict['Threads'],
                    resdict['GPUs'],
                    resdict['Energy'],
                    resdict['KPAR'],
                    resdict['NCORE'],
                    resdict['NPAR'],
                    resdict['Bands'],
                    resdict['LOOP+ Time'],
                    resdict['Runtime'],
                    ]
            rowline = ','.join(str(x) for x in rowlist)
            outstream.write(rowline + "\n")

if __name__ == "__main__":
    main()
