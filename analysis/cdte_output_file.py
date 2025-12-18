

import re
import os
import sys
import glob
import subprocess
import csv

def main():
    
    resdir = sys.argv[1]
    outfile = sys.argv[2]

    # Here we generate the list of files from a directory name
    searchstr = resdir + "/*.OUTCAR"
    filelist = glob.glob(searchstr)

    # Loop over files extracting the data as CSV
    first = True
    for file in filelist:
        print(file)
        if first:
            get_file_data(file, outfile, header=True)
            first = False
        else:
            get_file_data(file, outfile)

def get_file_data(filename, outfile, header=False):
    """Extract the details from output
    """
    infile = open(filename, 'r')
    resdict = {}
    loopvals = []
    trialvals = []

    # Defaults
    resdict['Threads'] = 1

    # Values from file name
    resdict['File'] = os.path.abspath(filename)
    tokens = filename.split('.')
    filestem = ''
    for token in tokens:
        if 'nodes' in token:
            filestem = token
    tokens = filestem.split('_')
    nodestring = None
    resdict['JobID'] = tokens[6]
    result = subprocess.run(['sacct', '-Xn', '--format=consumedenergyraw', '-j', resdict['JobID']], stdout=subprocess.PIPE)
    energy = str(result.stdout)
    resdict['Energy'] = int(energy.rstrip())
    for token in tokens:
        if 'nodes' in token:
            nodestring = token
    resdict['Nodes'] = int(nodestring.replace('nodes',''))

    # Values from the file contents
    for line in infile:
        if re.search('LOOP+:', line):
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
            resdict['Processes'] = int(tokens[1])
            resdict['Threads'] = int(tokens[4])
        elif re.search('mpi-ranks', line):
            line = line.strip()
            tokens = line.split()
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
               resdict['KPAR'] = int(tokens[6].strip())  
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

    # Append this result to the CSV file

    outstream = open(outfile, "a", newline="")
    w = csv.DictWriter(f, resdict.keys())
    if header:
        w.writeheader()
        w.writerow(resdict)
    else:
        w.writerow(resdict)

if __name__ == "__main__":
    main()