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
xrdcp root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAODv6/SUSYGluGluToHToAA_AToMuMu_AToTauTau_M-20_TuneCUETP8M1_13TeV_madgraph_pythia8/NANOAODSIM/PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/100000/67F359A7-7255-AA44-9B01-5B8138EC30F7.root inFile.root
python HAA.py -f inFile.root -o HToAAToMuMuTauTau_M20_000.root --nickName HToAAToMuMuTauTau_M20 -y 2016 -s HAA -w 1 -g 1
rm inFile.root
xrdcp root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAODv6/SUSYGluGluToHToAA_AToMuMu_AToTauTau_M-20_TuneCUETP8M1_13TeV_madgraph_pythia8/NANOAODSIM/PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/100000/C1DB1417-3E94-5C4B-B4FE-932B27437444.root inFile.root
python HAA.py -f inFile.root -o HToAAToMuMuTauTau_M20_001.root --nickName HToAAToMuMuTauTau_M20 -y 2016 -s HAA -w 1 -g 1
rm inFile.root
hadd -f -k all_HToAAToMuMuTauTau_M20_001.root *ntup *weights
rm *.pyc
rm *.so
rm *.pcm
rm *cc.d
rm *.ntup *.weights *.so
rm *.pcm
rm *cc.d
