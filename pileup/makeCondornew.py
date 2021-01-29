
import os

def getArgs() :
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","--verbose",default=0,type=int,help="Print level.")
    defDS = '/VBFHToTauTau_M125_13TeV_powheg_pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM '
    parser.add_argument("--dataSet",default=defDS,help="Data set name.") 
    parser.add_argument("--nickName",default='MCpileup',help="Data set nick name.") 
    parser.add_argument("-m","--mode",default='anaXRD',help="Mode (script to run).")
    parser.add_argument("-y","--year",default=2017,type=str,help="Data taking period, 2016, 2017 or 2018")
    parser.add_argument("-c","--concatenate",default=1,type=int,help="On how many files to run on each job")
    parser.add_argument("-s","--selection",default='ZH',type=str,help="select ZH or AZH")
    return parser.parse_args()

def beginBatchScript(baseFileName) :
    outLines = ['#!/bin/tcsh\n']
    outLines.append("source /cvmfs/cms.cern.ch/cmsset_default.csh\n")
    outLines.append("setenv SCRAM_ARCH slc6_amd64_gcc700\n")
    outLines.append("eval `scramv1 project CMSSW CMSSW_10_2_16_patch1`\n")
    outLines.append("cd CMSSW_10_2_16_patch1/src\n")
    outLines.append("eval `scramv1 runtime -csh`\n")
    outLines.append("echo ${_CONDOR_SCRATCH_DIR}\n")
    outLines.append("cd ${_CONDOR_SCRATCH_DIR}\n")
    return outLines

def getFileName(line) :
    tmp = line.split()[0].strip(',')
    fileName = tmp.strip()
    return fileName


args = getArgs()
era = str(args.year)

# sample query 
# dasgoclient --query="file dataset=/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8*/*/NANOAOD*" --limit=0   

query = '"file dataset={0:s}"'.format(args.dataSet)

if "USER" in str(args.dataSet) : query = '"file dataset={0:s}"'.format(args.dataSet+" instance=prod/phys03")

command = "dasgoclient --query={0:s} --limit=0  > fileList.txt".format(query)
print("Running in {0:s} mode.  Command={1:s}".format(args.mode,command))
os.system(command)
    
files = open('fileList.txt','r').readlines()
if len(files) < 1 :
    print("***In makeCondor.py: Empty fileList.txt")
    exit()

scriptList = [] 
file=[]
dataset=[]

mjobs=args.concatenate


for nFiles, file in enumerate(files) :
    fileName=getFileName(file)
    dataset.append(fileName)


counter=0

for nFile in range(0, len(dataset),mjobs) :
    #print("nFile={0:d} file[:80]={1:s}".format(nFile,file[:80]))

    scriptName = "{0:s}_{1:03d}.csh".format(args.nickName,nFile+1)
    print("scriptName={0:s}".format(scriptName))
    outLines = beginBatchScript(scriptName)


    fileName = getFileName(file)
    server = 'cms-xrd-global.cern.ch'
    if 'lpcsusyhiggs' in fileName : server = 'cmsxrootd.fnal.gov'

    maxx = mjobs
    if counter+mjobs > len(dataset) : 
        #print 'should include', nFile, -nFile-mjobs + len(dataset)+1, 'from ', len(dataset), counter
        maxx = len(dataset)-counter
        #for j in range(0,mjobs) :
    for j in range(0,maxx) :
        #print 'shoud see', nFile+maxx, maxx, len(dataset)
        fileloop=dataset[nFile:nFile+maxx][j]
        outLines.append("xrdcp root://{1:s}/{0:s} inFile.root\n".format(fileloop,server))
        outFileName = "{0:s}_{1:03d}.root".format(args.nickName,nFile+j+1)
        outLines.append("python makePileUpHisto.py -f inFile.root -o {0:s} -y {1:s}\n".format(outFileName, args.year))
        outLines.append("mv inFile.csv {0:s}\n".format(outFileName.replace(".root",".csv")))
        outLines.append("rm inFile.root\n".format(nFile+1))


    outLines.append("rm *.pyc\nrm *.so\nrm *.pcm\nrm *cc.d\n")
    open(scriptName,'w').writelines(outLines)
    scriptList.append(scriptName)
    counter += mjobs
            

# now that .csh files have been generated make a list of corresponding .jdl files

#dir = '/uscms_data/d3/alkaloge/ZH/CMSSW_10_2_9/src/MC/'


dir = '/uscms_data/d3/alkaloge/ZH/CMSSW_10_2_9/src/pileup/'
funcsDir = '/uscms_data/d3/alkaloge/ZH/CMSSW_10_2_9/src/funcs/'

#dir = os.getcwd()+"/../../../pileup/"
dir = os.getcwd()+"/../"
funcsDir = os.getcwd()+"/../../funcs/"

for file in scriptList :
    base = file[:-4] 
    outLines = ['universe = vanilla\n']
    outLines.append('Executable = {0:s}\n'.format(file))
    outLines.append('Output = {0:s}.out\n'.format(base))
    outLines.append('Error = {0:s}.err\n'.format(base))
    outLines.append('Log = {0:s}.log\n'.format(base))
    outLines.append('transfer_input_files = {0:s}makePileUpHisto.py, {0:s}data_pileup_{1:s}.root,'.format(dir,args.year))
    outLines.append('{0:s}tauFun.py, {0:s}generalFunctions.py \n '.format(funcsDir))
    outLines.append('should_transfer_files = YES\n')
    outLines.append('when_to_transfer_output = ON_EXIT\n')
    outLines.append('x509userproxy = $ENV(X509_USER_PROXY)\n')
    outLines.append('Queue 1\n')
    open('{0:s}.jdl'.format(base),'w').writelines(outLines)


