#########################
#Author: Sam Higginbotham
'''

* File Name : crab.py

* Purpose :

* Creation Date : 10-03-2020

* Last Modified :

'''
#########################
import os
from WMCore.Configuration import Configuration


config = Configuration()

config.section_('General')
config.General.requestName = ''
# if (args.workArea != ''):
#   config.General.workArea = args.workArea

config.section_('JobType')
config.JobType.pluginName = 'PrivateMC'
#config.JobType.psetName = os.environ['CMSSW_BASE']+'do_nothing_cfg.py'
config.JobType.psetName = 'do_nothing_cfg.py'
config.JobType.scriptExe = 'crab_HToAAToMuMuTauTau_M20_001.sh'
config.JobType.inputFiles = ['FrameworkJobReport.xml','/afs/cern.ch/work/s/shigginb/cmssw/HAA/ZH_Run2_10_2_9/src/ZH_Run2/MC/ZH.py','/afs/cern.ch/work/s/shigginb/cmssw/HAA/ZH_Run2_10_2_9/src/ZH_Run2/MC/MC_2016.root','/afs/cern.ch/work/s/shigginb/cmssw/HAA/ZH_Run2_10_2_9/src/ZH_Run2/MC/data_pileup_2016.root','/afs/cern.ch/work/s/shigginb/cmssw/HAA/ZH_Run2_10_2_9/src/ZH_Run2/MC/MCsamples_2016.csv','/afs/cern.ch/work/s/shigginb/cmssw/HAA/ZH_Run2_10_2_9/src/ZH_Run2/MC/cuts_HAA.yaml','/afs/cern.ch/work/s/shigginb/cmssw/HAA/ZH_Run2_10_2_9/src/ZH_Run2/funcs/tauFun.py','/afs/cern.ch/work/s/shigginb/cmssw/HAA/ZH_Run2_10_2_9/src/ZH_Run2/funcs/generalFunctions.py','/afs/cern.ch/work/s/shigginb/cmssw/HAA/ZH_Run2_10_2_9/src/ZH_Run2/funcs/outTuple.py','/afs/cern.ch/work/s/shigginb/cmssw/HAA/ZH_Run2_10_2_9/src/ZH_Run2/SVFit/FastMTT.h','/afs/cern.ch/work/s/shigginb/cmssw/HAA/ZH_Run2_10_2_9/src/ZH_Run2/SVFit/MeasuredTauLepton.h','/afs/cern.ch/work/s/shigginb/cmssw/HAA/ZH_Run2_10_2_9/src/ZH_Run2/SVFit/svFitAuxFunctions.h','/afs/cern.ch/work/s/shigginb/cmssw/HAA/ZH_Run2_10_2_9/src/ZH_Run2/SVFit/FastMTT.cc','/afs/cern.ch/work/s/shigginb/cmssw/HAA/ZH_Run2_10_2_9/src/ZH_Run2/SVFit/MeasuredTauLepton.cc','/afs/cern.ch/work/s/shigginb/cmssw/HAA/ZH_Run2_10_2_9/src/ZH_Run2/SVFit/svFitAuxFunctions.cc']
config.JobType.outputFiles = ['HToAAToMuMuTauTau_M20.root']
config.JobType.maxMemoryMB = 5000
config.JobType.allowUndistributedCMSSW = True
config.section_('Data')
config.Data.outputPrimaryDataset = 'CRAB_HAA'
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 1
config.Data.totalUnits = 2
config.Data.publication = False
config.Data.outputDatasetTag = ''

config.section_('User')

config.section_('Site')
config.Site.blacklist = ['T3_IT_Bologna','T3_US_UMiss']
config.Site.storageSite = 'T2_CH_CERNBOX'
