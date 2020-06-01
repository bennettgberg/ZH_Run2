
# generate a runMC.csh script that creates the .csh and .jdl files
# to process MC data 

import os

def getArgs() :
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--inFile",default='MCsamples_2016.csv',help="Input file name.") 
    parser.add_argument("-y","--year",default=2016,type=int,help="Data taking period, 2016, 2017 or 2018")
    parser.add_argument("-s","--selection",default='HAA',type=str,help="Select ZH,AZH or HAA")
    parser.add_argument("-g","--genmatch",default=0,type=int,help="genmatch")
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
    outLines.append("python ../../makeCondorsam.py --dataSet {0:s} --nickName {1:s} --mode {2:s} --year {3:s} -c 20 -s {4:s} -g {5:d} \n".format(dataset,nickname, mode,era, args.selection, args.genmatch))
    outLines.append("cd {0:s}\n".format(cwd))

fOut='runMC_{0:s}_{1:s}.sh'.format(str(args.year),args.selection)
open(fOut,'w').writelines(outLines)



    
    
