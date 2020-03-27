#!/bin/bash
set -e
ulimit -s unlimited
ulimit -c 0

function error_exit
{
  if [ $1 -ne 0 ]; then
    echo "Error with exit code ${1}"
    if [ -e FrameworkJobReport.xml ]
    then
      cat << EOF > FrameworkJobReport.xml.tmp
      <FrameworkJobReport>
      <FrameworkError ExitStatus="${1}" Type="" >
      Error with exit code ${1}
      </FrameworkError>
EOF
      tail -n+2 FrameworkJobReport.xml >> FrameworkJobReport.xml.tmp
      mv FrameworkJobReport.xml.tmp FrameworkJobReport.xml
    else
      cat << EOF > FrameworkJobReport.xml
      <FrameworkJobReport>
      <FrameworkError ExitStatus="${1}" Type="" >
      Error with exit code ${1}
      </FrameworkError>
      </FrameworkJobReport>
EOF
    fi
    exit 0
  fi
}

trap 'error_exit $?' ERR

cp MCsamples_*csv MCsamples.csv
cp cuts_HAA.yaml cuts.yaml
if [ $1 -eq 1 ]; then
xrdcp root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAODv6/SUSYGluGluToHToAA_AToMuMu_AToTauTau_M-20_TuneCUETP8M1_13TeV_madgraph_pythia8/NANOAODSIM/PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/100000/67F359A7-7255-AA44-9B01-5B8138EC30F7.root inFile.root
python ZH.py -f inFile.root -o HToAAToMuMuTauTau_M20_000.root --nickName HToAAToMuMuTauTau_M20 -y 2016 -s HAA -w 1
rm inFile.root
fi
if [ $1 -eq 2 ]; then
xrdcp root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAODv6/SUSYGluGluToHToAA_AToMuMu_AToTauTau_M-20_TuneCUETP8M1_13TeV_madgraph_pythia8/NANOAODSIM/PUMoriond17_Nano25Oct2019_102X_mcRun2_asymptotic_v7-v1/100000/C1DB1417-3E94-5C4B-B4FE-932B27437444.root inFile.root
python ZH.py -f inFile.root -o HToAAToMuMuTauTau_M20_001.root --nickName HToAAToMuMuTauTau_M20 -y 2016 -s HAA -w 1
rm inFile.root
fi
hadd -f -k HToAAToMuMuTauTau_M20.root *ntup *weights
