#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc6_amd64_gcc700
eval scramv1 project CMSSW CMSSW_10_2_16_patch1
cd CMSSW_10_2_16_patch1/src
eval scramv1 runtime -sh
export X509_USER_PROXY=$1
voms-proxy-info -all
voms-proxy-info -all -file $1
echo ${_CONDOR_SCRATCH_DIR}
cd ${_CONDOR_SCRATCH_DIR}
cp MCsamples_*csv MCsamples.csv
cp cuts_HAA.yaml cuts.yaml
xrdcp root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAODv6/SUSYGluGluToHToAA_AToMuMu_AToTauTau_M-50_TuneCUETP8M1_13TeV_madgraph_pythia8/NANOAODSIM/PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/70000/F85FB322-4E03-7844-9EAD-F62D51FB6E73.root inFile.root
python HAA.py -f inFile.root -o HToAAToMuMuTauTau_M50_000.root --nickName HToAAToMuMuTauTau_M50 -y 2016 -s HAA -w 1 -g 1
rm inFile.root
xrdcp root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAODv6/SUSYGluGluToHToAA_AToMuMu_AToTauTau_M-50_TuneCUETP8M1_13TeV_madgraph_pythia8/NANOAODSIM/PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/70000/9178DF55-C774-854A-A93A-CD20D46A9C47.root inFile.root
python HAA.py -f inFile.root -o HToAAToMuMuTauTau_M50_001.root --nickName HToAAToMuMuTauTau_M50 -y 2016 -s HAA -w 1 -g 1
rm inFile.root
hadd -f -k all_HToAAToMuMuTauTau_M50_001.root *ntup *weights
rm *.pyc
rm *.so
rm *.pcm
rm *cc.d
rm *.ntup *.weights *.so
rm *.pcm
rm *cc.d
