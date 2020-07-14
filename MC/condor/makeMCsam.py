
# generate a runMC.csh script that creates the .csh and .jdl files
# to process MC data 

import os

def getArgs() :
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--inFile",default='MCsamples_2016.csv',help="Input file name.") 
    parser.add_argument("-y","--year",default=2016,type=int,help="Data taking period, 2016, 2017 or 2018")
    parser.add_argument("-s","--selection",default='HAA',type=str,help="Select ZH,AZH or HAA")
    parser.add_argument("--csv",default="MCsamples_2016.csv",help="CSV file for samples")
    parser.add_argument("-g","--genmatch",default=0,type=int,help="genmatch")
    parser.add_argument("-p","--proxypath",default="/afs/cern.ch/user/s/shigginb/private/x509up",type=str,help="Full path to proxy certificate file (for condor)")
    parser.add_argument("-l","--language",default="bash",type=str,help="Language for scripts to run (only bash or tcsh is supported for now.)")
    parser.add_argument("-m","--makeCondor",default="../../makeCondorsam.py",type=str,help="makeCondor script to call")
    return parser.parse_args()

args = getArgs() 
era=str(args.year)
outLines = []
cwd = os.getcwd()
for line in open(args.inFile,'r').readlines() :
    nickname = line.split(',')[0]
    #print("\n\n\n line.split(',')={0:s}".format(str(line.split(','))))
    dataset = line.split(',')[6].replace(' ','_').strip()
    if len(dataset) < 2 : continue
    #print("\n***line.split()={0:s}".format(str(line.split(','))))
    print("nickname={0:s} \n dataset={1:s}".format(nickname,dataset))

    mode = 'anaXRD'
    
    outLines.append("mkdir -p {0:s}/{1:s}_{2:s}\ncd {0:s}/{1:s}_{2:s}\n".format(args.selection,nickname,era))
    outLines.append("python ../../{9:s} --dataSet {0:s} --nickName {1:s} --csv {2:s} --mode {3:s} --year {4:s} -c 5 -s {5:s} -g {6:d} -p {7:s} -l {8:s}\n".format(dataset,nickname, args.csv, mode,era, args.selection, args.genmatch, args.proxypath, args.language, args.makeCondor))
    outLines.append("cd {0:s}\n".format(cwd))

fOut='runMC_{0:s}_{1:s}.sh'.format(str(args.year),args.selection)
open(fOut,'w').writelines(outLines)



    
    
