#
# read MC file root files and histogram by group 
#

import CMS_lumi
import tdrstyle
import ROOT
from ROOT import gSystem, gStyle, gROOT, kTRUE, TMatrixD
from ROOT import TFile, TTree, TH1D, TCanvas, TLorentzVector, TLegend, TAxis, THStack, TGraphAsymmErrors, vector, gInterpreter
gROOT.SetBatch(True) # don't pop up any plots
gStyle.SetOptStat(0) # don't show any stats
from math import sqrt, sin, cos, pi, tan, acos, atan2,log
#import math
import os
import os.path
import sys
sys.path.append('../modules/')
import ScaleFactor as SF
sys.path.append('../TauPOG')
from TauPOG.TauIDSFs.TauIDSFTool import TauIDSFTool
from TauPOG.TauIDSFs.TauIDSFTool import TauESTool
from TauPOG.TauIDSFs.TauIDSFTool import TauFESTool

def catToNumber(cat) :
    number = { 'eeet':1, 'eemt':2, 'eett':3, 'eeem':4, 'mmet':5, 'mmmt':6, 'mmtt':7, 'mmem':8, 'et':9, 'mt':10, 'tt':11 }
    return number[cat]

def numberToCat(number) :
    cat = { 1:'eeet', 2:'eemt', 3:'eett', 4:'eeem', 5:'mmet', 6:'mmmt', 7:'mmtt', 8:'mmem', 9:'et', 10:'mt', 11:'tt' }
    return cat[number]


def search(values, searchFor):
    for k in values:
        for v in values[k]:
            if searchFor in v:
                return True
    return False


def runSVFit(entry, channel) :
		  
    measuredMETx = entry.met*cos(entry.metphi)
    measuredMETy = entry.met*sin(entry.metphi)

    #define MET covariance
    covMET = TMatrixD(2,2)
    covMET[0][0] = entry.metcov00
    covMET[1][0] = entry.metcov10
    covMET[0][1] = entry.metcov01
    covMET[1][1] = entry.metcov11


    #self.kUndefinedDecayType, self.kTauToHadDecay,  self.kTauToElecDecay, self.kTauToMuDecay = 0, 1, 2, 3
    if channel == 'et' :
	measTau1 = ROOT.MeasuredTauLepton(kTauToElecDecay, entry.pt_3, entry.eta_3, entry.phi_3, 0.000511) 
    elif channel == 'mt' :
	measTau1 = ROOT.MeasuredTauLepton(kTauToMuDecay, entry.pt_3, entry.eta_3, entry.phi_3, 0.106) 
    elif channel == 'tt' :
	measTau1 = ROOT.MeasuredTauLepton(kTauToHadDecay, entry.pt_3, entry.eta_3, entry.phi_3, entry.m_3)
		    
    if channel != 'em' :
	measTau2 = ROOT.MeasuredTauLepton(kTauToHadDecay, entry.pt_4, entry.eta_4, entry.phi_4, entry.m_4)

    if channel == 'em' :
	measTau1 = ROOT.MeasuredTauLepton(kTauToElecDecay,  entry.pt_3, entry.eta_3, entry.phi_3, 0.000511)
	measTau2 = ROOT.MeasuredTauLepton(kTauToMuDecay, entry.pt_4, entry.eta_4, entry.phi_4, 0.106)

    VectorOfTaus = ROOT.std.vector('MeasuredTauLepton')
    instance = VectorOfTaus()
    instance.push_back(measTau1)
    instance.push_back(measTau2)

    FMTT = ROOT.FastMTT()
    FMTT.run(instance, measuredMETx, measuredMETy, covMET)
    ttP4 = FMTT.getBestP4()
    return ttP4.M(), ttP4.Mt() 


def getArgs() :
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","--verbose",default=0,type=int,help="Print level.")
    parser.add_argument("-f","--inFileName",default='./MCsamples_2017_small.csv',help="File to be analyzed.")
    parser.add_argument("-o","--outFileName",default='',help="File to be used for output.")
    parser.add_argument("-y","--year",default=2017,type=int,help="Year for data.")
    parser.add_argument("-l","--LTcut",default=0.,type=float,help="H_LTcut")
    parser.add_argument("-s","--sign",default='OS',help="Opposite or same sign (OS or SS).")
    parser.add_argument("-a","--analysis",default='ZH',help="Select ZH or AZH")
    parser.add_argument("--MConly",action='store_true',help="no data driven bkg") 
    parser.add_argument("--looseCuts",action='store_true',help="Loose cuts")
    parser.add_argument("-u", "--unBlind",default='no',help="Unblind signal region for OS")
    parser.add_argument("-r", "--redoFit",default='no',help="redo FastMTT and adjust MET after to Tau ES corrections")
    parser.add_argument("-w", "--workingPoint",type=int, default=16, help="working point for fakes 16 (M), 32(T), 64(VT), 128(VVT)")
    parser.add_argument("-b", "--bruteworkingPoint",type=int, default=16, help="make working point for fakes 16 (M), 32(T), 64(VT), 128(VVT)")
    parser.add_argument("-p", "--plotsScheme",type=bool, default=False, help="more categories for the plots")
    
    return parser.parse_args()

class dupeDetector() :
    
    def __init__(self):
        self.nCalls = 0 
        self.runEventList = []
        self.DuplicatedEvents = []

    def checkEvent(self,entry,cat) :
        self.nCalls += 1 
        runEvent = "{0:d}:{1:d}:{2:d}:{3:s}".format(entry.lumi,entry.run,entry.evt,cat)
        if runEvent in self.runEventList :
            #print("Event in list: runEventList={0:s}".format(str(self.runEventList)))
            self.DuplicatedEvents.append(runEvent)
	    #print 'duplicated event', entry.lumi,entry.run,entry.evt
            return True
        else :
            self.runEventList.append(runEvent)
            #print("New event: runEventList={0:s}".format(str(self.runEventList)))
            return False

        print 'print report', self.DuplicatedEvents

    def printSummary(self) :
        print("Duplicate Event Summary: Calls={0:d} Unique Events={1:d}".format(self.nCalls,len(self.runEventList)))
        return


def OverFlow(htest) :

    nb = htest.GetNbinsX()

    lastbincont = htest.GetBinContent(nb)
    overbincont = htest.GetBinContent(nb+1)
    lastbinerror = htest.GetBinError(nb)
    overbinerror = htest.GetBinError(nb+1)

    htest.SetBinContent(nb, 0)
    htest.SetBinContent(nb, lastbincont+overbincont)
    htest.SetBinContent(nb+1, 0.)
    htest.SetBinError(nb, sqrt(lastbinerror*lastbinerror + overbinerror*overbinerror))
    htest.SetBinError(nb+1, 0.)


    #return htest

def PtoEta( Px,  Py,  Pz) :

   P = sqrt(Px*Px+Py*Py+Pz*Pz);
   if P> 0 : 
       cosQ = Pz/P;
       Q = acos(cosQ);
       Eta = - log(tan(0.5*Q));
       return Eta
   else: return -99

def PtoPhi( Px,  Py) : return atan2(Py,Px)


def PtoPt( Px,  Py) : return sqrt(Px*Px+Py*Py)


def dPhiFrom2P( Px1,  Py1, Px2,  Py2) :
   prod = Px1*Px2 + Py1*Py2;
   mod1 = sqrt(Px1*Px1+Py1*Py1);
   mod2 = sqrt(Px2*Px2+Py2*Py2);
   cosDPhi = prod/(mod1*mod2);
   return acos(cosDPhi)


def DRobj(eta1,phi1,eta2,phi2) :
    dPhi = min(abs(phi2-phi1),2.*pi-abs(phi2-phi1))
    return sqrt(dPhi**2 + (eta2-eta1)**2)

def DPhiobj(phi1,phi2) :
    dPhi = min(abs(phi2-phi1),2.*pi-abs(phi2-phi1))
    return dPhi

def deltaEta(Px1, Py1, Pz1, Px2,  Py2,  Pz2):

  eta1 = PtoEta(Px1,Py1,Pz1)
  eta2 = PtoEta(Px2,Py2,Pz2)

  dEta = eta1 - eta2

  return dEta

def getFakeWeightsvspT(ic, pt1,pt2, WP, ist1, ist2) :
    
    if ic == 'et' : 
        p1 = 'e_et'
        p2 = 't_et'

    if ic == 'mt' : 
        p1 = 'm_mt'
        p2 = 't_mt'

    if ic == 'em' : 
        p1 = 'e_em'
        p2 = 'm_em'

    if ic == 'tt' : 
        p1 = 't1_tt'
        p2 = 't2_tt'

    filein = '../fakes/FakesResult_{0:s}_SS_{1:s}WP.root'.format(str(args.year),str(WP))
    fin = TFile.Open(filein,"READ")         
    h1 = fin.Get('{0:s}_vspT'.format(p1))
    h2 = fin.Get('{0:s}_vspT'.format(p2))
    xB1 = 1
    xB2 = 1
    if pt1 < 100 : xB1 = h1.FindBin(pt1)
    if pt1 > 100 : xB1 = h1.GetNbinsX()

    if pt2 < 100 : xB2 = h2.FindBin(pt2)
    if pt2 > 100 : xB2 = h2.GetNbinsX()

    f1 = h1.GetBinContent(xB1)
    f2 = h1.GetBinContent(xB2)
    #print '===========>', pt1, pt2, f1, f2, xB1, xB2
    w1, w2, w0 =0. ,0. ,0.
    '''
    if not ist1 and ist2 : w1 = float(f1/(1.-f1))
    if ist1 and not ist2 : w2 = float(f2/(1.-f2))
    if not ist1 and not ist2 : w0 = w1*w2
    '''
    w1 = float(f1/(1.-f1))
    w2 = float(f2/(1.-f2))
    w0 = w1*w2
    #print '================= now reading fake rate for data', pt1, pt2 ,' to be', f1, f2, 'actual fW1 etc', w1, w2, w0, 'is this false??? ', ist1, ist2
    return w1, w2, w0




def getFakeWeights(p1,p2, WP) :
    
    filein = '../fakes/FakesResult_{0:s}_SS_{1:s}WP.root'.format(str(args.year),str(WP))
    fin = TFile.Open(filein,"READ")         
    h1 = fin.Get('{0:s}'.format(p1))
    h2 = fin.Get('{0:s}'.format(p2))
    f1 = h1.GetSumOfWeights()
    f2 = h2.GetSumOfWeights()

    #print '================= now reading fake rate for', p1, p2 ,' to be', f1, f2, 'and for WP', WP

    w1 = f1/(1.-f1)
    w2 = f2/(1.-f2)
    w0 = w1*w2
    return w1, w2, w0


args = getArgs()
era=str(args.year)
#cats = { 1:'eeet', 2:'eemt', 3:'eett', 4:'mmet', 5:'mmmt', 6:'mmtt', 7:'et', 8:'mt', 9:'tt' }
cats = { 1:'eeet', 2:'eemt', 3:'eett', 4:'eeem', 5:'mmet', 6:'mmmt', 7:'mmtt', 8:'mmem'}
tightCuts = not args.looseCuts 
dataDriven = not args.MConly

unblind=False
if args.unBlind.lower() == 'true' or args.unBlind.lower == 'yes' : unblind = True


Pblumi = 1000.
tauID_w = 1.


# Tau Decay types
kUndefinedDecayType, kTauToHadDecay,  kTauToElecDecay, kTauToMuDecay = 0, 1, 2, 3   

gInterpreter.ProcessLine(".include .")
for baseName in ['../SVFit/MeasuredTauLepton','../SVFit/svFitAuxFunctions','../SVFit/FastMTT', '../HTT-utilities/RecoilCorrections/src/MEtSys', '../HTT-utilities/RecoilCorrections/src/RecoilCorrector'] : 
    if os.path.isfile("{0:s}_cc.so".format(baseName)) :
	gInterpreter.ProcessLine(".L {0:s}_cc.so".format(baseName))
    else :
	gInterpreter.ProcessLine(".L {0:s}.cc++".format(baseName))   
	# .L is not just for .so files, also .cc


print 'compiled it====================================================================='

weights= {''}
weights_muToTauFR={''}
weights_elToTauFR={''}
weights_mujToTauFR={''}
weights_eljToTauFR={''}
weights_muTotauES={''}
weights_elTotauES={''}


campaign = {2016:'2016Legacy', 2017:'2017ReReco', 2018:'2018ReReco'}



if era == '2016' : 
    weights = {'lumi':35.92, 'tauID_w' :0.87, 'tauES_DM0' : -0.6, 'tauES_DM1' : -0.5,'tauES_DM10' : 0.0, 'mutauES_DM0' : -0.2, 'mutauES_DM1' : 1.5, 'eltauES_DM0' : 0.0, 'eltauES_DM1' : 9.5}

    weights_mujToTauFR = {'DM1' : 0.85, 'lt0p4' : 1.21, '0p4to0p8' : 1.11, '0p8to1p2' : 1.20, '1p2to1p7' : 1.16, '1p7to2p3' : 2.25 }
    weights_muToTauFR = {'DM1' : 1.38, 'lt0p4' : 0.80, '0p4to0p8' : 0.81, '0p8to1p2' : 0.79, '1p2to1p7' : 0.68, '1p7to2p3' : 1.34 }
    weights_eljToTauFR = {'lt1p479_DM0' : 1.18, 'gt1p479_DM0' : 0.93, 'lt1p479_DM1' : 1.18, 'gt1p479_DM1' : 1.07 }
    weights_elToTauFR = {'lt1p479_DM0' : 0.80, 'gt1p479_DM0' : 0.72, 'lt1p479_DM1' : 1.14, 'gt1p479_DM1' : 0.64 }

    weights_muTotauES = {'DM0' : 0, 'DM1' : -0.5}
    weights_elTotauES = {'DM0' :-0.5, 'DM1' : 6}


    TriggerSF={'dir' : '../tools/ScaleFactors/TriggerEffs/', 'fileMuon' : 'Muon/SingleMuon_Run2016_IsoMu24orIsoMu27.root', 'fileElectron' : 'Electron/SingleElectron_Run2016_Ele25orEle27.root'}
    LeptonSF={'dir' : '../tools/ScaleFactors/LeptonEffs/', 'fileMuon0p2' : 'Muon/Muon_Run2016_IdIso_0p2.root', 'fileMuon0p15' : 'Muon/Muon_Run2016_IdIso_0p15.root', 'fileElectron0p1' : 'Electron/Electron_Run2016_IdIso_0p1.root',  'fileElectron0p15' : 'Electron/Electron_Run2016_IdIso_0p15.root'}
    TESSF={'dir' : 'TauPOG/TauIDSFs/data/', 'fileTES' : 'TauES_dm_2016Legacy.root'}



if era == '2017' : 
    weights = {'lumi':41.53, 'tauID_w' :0.89, 'tauES_DM0' : 0.7, 'tauES_DM1' : -0.2,'tauES_DM10' : 0.1, 'mutauES_DM0' : 0.0, 'mutauES_DM1' : 0.0, 'eltauES_DM0' : 0.3, 'eltauES_DM1' : 3.6}

    weights_mujToTauFR = {'DM1' : 0.77, 'lt0p4' : 1.23, '0p4to0p8' : 1.07, '0p8to1p2' : 1.21, '1p2to1p7' : 1.21, '1p7to2p3' : 2.74 }
    weights_muToTauFR = {'DM1' : 0.69, 'lt0p4' : 1.14, '0p4to0p8' : 1., '0p8to1p2' : 0.87, '1p2to1p7' : 0.52, '1p7to2p3' : 1.47 }
    weights_eljToTauFR = {'lt1p479_DM0' : 1.09, 'gt1p479_DM0' : 0.86, 'lt1p479_DM1' : 1.10, 'gt1p479_DM1' : 1.03 }
    weights_elToTauFR = {'lt1p479_DM0' : 0.98, 'gt1p479_DM0' : 0.80, 'lt1p479_DM1' : 1.07, 'gt1p479_DM1' : 0.64 }


    weights_muTotauES = {'DM0' : -0.2, 'DM1' : -0.8}
    weights_elTotauES = {'DM0' :-1.8, 'DM1' : 1.8}

    TriggerSF={'dir' : '../tools/ScaleFactors/TriggerEffs/', 'fileMuon' : 'Muon/SingleMuon_Run2017_IsoMu24orIsoMu27.root', 'fileElectron' : 'Electron/SingleElectron_Run2017_Ele32orEle35.root'}
    LeptonSF={'dir' : '../tools/ScaleFactors/LeptonEffs/', 'fileMuon0p2' : 'Muon/Muon_Run2017_IdIso_0p2.root', 'fileMuon0p15' : 'Muon/Muon_Run2017_IdIso_0p15.root', 'fileElectron0p1' : 'Electron/Electron_Run2017_IdIso_0p1.root',  'fileElectron0p15' : 'Electron/Electron_Run2017_IdIso_0p15.root'}
    TESSF={'dir' : 'TauPOG/TauIDSFs/data/', 'fileTES' : 'TauES_dm_2017ReReco.root'}

if era == '2018' : 
    weights = {'lumi':59.74, 'tauID_w' :0.90, 'tauES_DM0' : -1.3, 'tauES_DM1' : -0.5,'tauES_DM10' : -1.2, 'mutauES_DM0' : 0.0, 'mutauES_DM1' : 0.0, 'eltauES_DM0' : 0.0, 'eltauES_DM1' : 0.0}
    weights_mujToTauFR = {'DM1' : 0.79, 'lt0p4' : 1.11, '0p4to0p8' : 1.05, '0p8to1p2' : 1.18, '1p2to1p7' : 1.06, '1p7to2p3' : 1.79 }
    weights_muToTauFR = {'DM1' : 0.55, 'lt0p4' : 1.08, '0p4to0p8' : 0.78, '0p8to1p2' : 0.77, '1p2to1p7' : 0.75, '1p7to2p3' : 2.02 }
    weights_eljToTauFR = {'lt1p479_DM0' : 1.21, 'gt1p479_DM0' : 0.92, 'lt1p479_DM1' : 1.18, 'gt1p479_DM1' : 1.04 }
    weights_elToTauFR = {'lt1p479_DM0' : 1.09, 'gt1p479_DM0' : 0.80, 'lt1p479_DM1' : 0.85, 'gt1p479_DM1' : 0.49 }


    weights_muTotauES = {'DM0' : -0.2, 'DM1' : -1.}
    weights_elTotauES = {'DM0' :-3.2, 'DM1' : 2.6}

    TriggerSF={'dir' : '../tools/ScaleFactors/TriggerEffs/', 'fileMuon' : 'Muon/SingleMuon_Run2018_IsoMu24orIsoMu27.root', 'fileElectron' : 'Electron/SingleElectron_Run2018_Ele32orEle35.root'}
    LeptonSF={'dir' : '../tools/ScaleFactors/LeptonEffs/', 'fileMuon0p2' : 'Muon/Muon_Run2018_IdIso_0p2.root', 'fileMuon0p15' : 'Muon/Muon_Run2018_IdIso_0p15.root', 'fileElectron0p1' : 'Electron/Electron_Run2018_IdIso_0p1.root',  'fileElectron0p15' : 'Electron/Electron_Run2018_IdIso_0p15.root'}
    TESSF={'dir' : 'TauPOG/TauIDSFs/data/', 'fileTES' : 'TauES_dm_2018ReReco.root'}



if era == '2016' : recoilCorrector  = ROOT.RecoilCorrector("HTT-utilities/RecoilCorrections/data/Type1_PFMET_Run2016BtoH.root");
if era == '2017' : recoilCorrector  = ROOT.RecoilCorrector("HTT-utilities/RecoilCorrections/data/Type1_PFMET_2017.root");
if era == '2018' : recoilCorrector  = ROOT.RecoilCorrector("HTT-utilities/RecoilCorrections/data/TypeI-PFMet_Run2018.root");

# use this utility class to screen out duplicate events
DD = {}
for cat in cats.values() :
    DD[cat] = dupeDetector()

# dictionary where the group is the key
hMC = {}
hMCFM = {}

hm_sv_cat = {}
hm_sv_new = {}
hm_sv_new_FM = {}
hw_fm_new = {}
hmt_sv_new = {}
hmt_sv_new_FM = {}
hH_LT= {}
hH_LT_FM= {}
hCutFlow = {}
hCutFlowN = {}
hCutFlowFM = {}
hW = {}
hTriggerW= {}
hLeptonW= {}
hCutFlowPerGroup = {}
hCutFlowPerGroupFM = {}
WCounter = {}


isW = False
isDY = False
muonMass = 0.106
electronMass = 0.000511
		
MetV = TLorentzVector()
MetVcor = TLorentzVector()
tauV3 = TLorentzVector()
tauV4 = TLorentzVector()
tauV = TLorentzVector()
tauV3cor = TLorentzVector()
tauV4cor = TLorentzVector()
L1 = TLorentzVector()
L2 = TLorentzVector()
L1.SetXYZM(0,0,0,0)
L2.SetXYZM(0,0,0,0)
L1g = TLorentzVector()
L2g = TLorentzVector()
L1g.SetXYZM(0,0,0,0)
L2g.SetXYZM(0,0,0,0)
MetV.SetXYZM(0,0,0,0)
MetVcor.SetXYZM(0,0,0,0)
tauV3.SetXYZM(0,0,0,0)
tauV4.SetXYZM(0,0,0,0)
tauV3cor.SetXYZM(0,0,0,0)
tauV4cor.SetXYZM(0,0,0,0)
tauV.SetXYZM(0,0,0,0)

# dictionary where the nickName is the key
nickNames, xsec, totalWeight, sampleWeight = {}, {}, {}, {}

#groups = ['fakes','Signal','Other','Top','DY','WZ','ZZ','data']
#groups = ['Signal','Other','Top','DY','WZ','ZZ','data','fakes','f1','f2']
groups = ['fakes','f1', 'f2','bfl1', 'ljfl1', 'cfl1','jfl1','bfl2', 'ljfl2', 'cfl2','jfl2','jft1', 'jft2','Signal','Other','Top','DY','WZ','ZZ','data']
ngroups = ['fakes','f1', 'f2','bfl1', 'ljfl1', 'cfl1','jfl1','bfl2', 'ljfl2', 'cfl2','jfl2','jft1', 'jft2','Signal','Other','Top','DY','WZ','ZZ','data']
fgroups = ['bfl', 'ljfl',  'cfl','jfl', 'jft1', 'jft2']

groupss = ['Other','Top','DY','WZ','ZZ', 'Signal']

'''
groups = ['fakes','f1', 'f2', 'Signal','Other','Top','DY','WZ','ZZ','data']
ngroups = ['fakes','f1', 'f2','Signal','Other','Top','DY','WZ','ZZ','data']

for f in fgroups : 
    for g in groupss :
        groups.insert(0,g+'_'+f)
        ngroups.insert(0,g+'_'+f)
'''

for group in groups :
    nickNames[group] = []


# make a first pass to get the weights


WNJetsXsecs = [47297.3] # first entry: W0Jets xsec (not in file redirector)
DYNJetsXsecs = [4263.5] # first entry: DY0Jets xsec (not in file redirector)

WIncl_xsec = 61526.7
DYIcl_xsec = 6225.42

WJets_kfactor = 1.221
DY_kfactor = 1.1637

WxGenweightsArr = []
DYxGenweightsArr = []

print ' Will use the ' ,args.inFileName
for line in open(args.inFileName,'r').readlines() :
    vals = line.split(',')
    if '#' in vals[0] : continue
    if vals[0][0] == "W" and  "JetsToLNu" in vals[0][2:] :
        WNJetsXsecs.append(float(vals[2]))
        filein = '../MC/condor/{0:s}/{1:s}_{2:s}/{1:s}_{2:s}.root'.format(args.analysis,vals[0],era)
        fIn = TFile.Open(filein,"READ")
        WxGenweightsArr.append(fIn.Get("hWeights").GetSumOfWeights())


    if vals[0][:2] == "DY" and "JetsToLL" in vals[0][3:] and 'M10to50' not in vals[0]:
        DYNJetsXsecs.append(float(vals[2]))
        filein = '../MC/condor/{0:s}/{1:s}_{2:s}/{1:s}_{2:s}.root'.format(args.analysis,vals[0],era)
        fIn = TFile.Open(filein,"READ")
        DYxGenweightsArr.append(fIn.Get("hWeights").GetSumOfWeights())
        #DYxGenweightsArr.append(fIn.Get("DY"+str(i)+"genWeights").GetSumOfWeights())

WIncl_only = False
DYIncl_only = False


for line in open(args.inFileName,'r').readlines() :
    vals = line.split(',')
    if '#' in vals[0] : continue
    nickName = vals[0]
    group = vals[1]
    nickNames[group].append(nickName)
    xsec[nickName] = float(vals[2])
    #totalWeight[nickName] = float(vals[4])
    filein = '../MC/condor/{0:s}/{1:s}_{2:s}/{1:s}_{2:s}.root'.format(args.analysis,vals[0],era)
    fIn = TFile.Open(filein,"READ")
    totalWeight[nickName] = float(fIn.Get("hWeights").GetSumOfWeights())
    sampleWeight[nickName]= Pblumi*weights['lumi']*xsec[nickName]/totalWeight[nickName]
    

    print("group={0:10s} nickName={1:20s} xSec={2:10.3f} totalWeight={3:11.1f} sampleWeight={4:10.6f}".format(
        group,nickName,xsec[nickName],totalWeight[nickName],sampleWeight[nickName]))

    #print("{0:100s}  & {1:10.3f} & {2:11.1f} & {3:10.6f}\\\\\\hline".format(
    #     str(vals[6]),xsec[nickName],totalWeight[nickName],sampleWeight[nickName]))
   
if not search(nickNames, 'W1') and not search(nickNames, 'W2') and not search(nickNames, 'W3') and not search(nickNames, 'W4') : WIncl_only = True
if not search(nickNames, 'DY1') and not search(nickNames, 'DY2') and not search(nickNames, 'DY3') and not search(nickNames, 'DY4') : DYIncl_only = True


for i in range(1,5) :
    nn = 'DY{0:d}JetsToLL'.format(i)
    if search(nickNames, nn) :
        sampleWeight[nn] = Pblumi*weights['lumi']/(totalWeight['DYJetsToLL']/xsec['DYJetsToLL'] + DYxGenweightsArr[i-1]/(xsec[nn]*DY_kfactor))
        #print 'DY', totalWeight['DYJetsToLL']/xsec['DYJetsToLL'], DYxGenweightsArr[i-1], 'xsec', xsec[nn], 'weight ? ', sampleWeight[nn]

for i in range(1,4) :
    nn = 'W{0:d}JetsToLNu'.format(i)
    if search(nickNames, nn) : sampleWeight[nn] = Pblumi*weights['lumi']/(totalWeight['WJetsToLNu']/xsec['WJetsToLNu'] + WNJetsXsecs[i-1]/(xsec[nn]*WJets_kfactor))

#print '========================================',  sampleWeight['DY1JetsToLL'], sampleWeight['W1JetsToLNu'], WIncl_only,  DYIncl_only

# now add the data
#for eras in ['2017B','2017C','2017D','2017E','2017F'] :
for eras in [era] :
    #for dataset in ['SingleElectron','SingleMuon','DoubleEG','DoubleMuon'] :
    for dataset in ['data'] :
        #nickName = '{0:s}_Run{1:s}'.format(dataset,eras)
        nickName = '{0:s}_{1:s}'.format(dataset,eras)
        totalWeight[nickName] = 1.
        sampleWeight[nickName] = 1.
        nickNames['data'].append(nickName)
#####################################3


print("tightCuts={0}".format(tightCuts))
if tightCuts :
    outFileName = 'allGroups_{0:d}_{1:s}_LT{2:02d}.root'.format(args.year,args.sign,int(args.LTcut))
    if args.MConly :
        print("args.MConly is TRUE")
        outFileName = outFileName.replace('.root','_MC.root') 
else :
    outFileName = 'allGroups_{0:d}_{1:s}_LT{2:02d}_loose.root'.format(args.year,args.sign,int(args.LTcut))
    
if args.redoFit.lower() == 'no' : outFileName = 'allGroups_{0:d}_{1:s}_LT{2:02d}_{3:s}noSV'.format(args.year,args.sign,int(args.LTcut), str(args.workingPoint))


WP = args.workingPoint
WPSR= 16
if args.workingPoint == args.bruteworkingPoint : WPSR = WP
outFileName = outFileName +"_"+str(args.bruteworkingPoint)+"brute"


print("Opening {0:s} as output.".format(outFileName))
fOut = TFile( outFileName+".root", 'recreate' )

#fe, fm, ft_et, ft_mt, f1_tt, f2_tt   = 0.0456, 0.0935, 0.1391, 0.1284, 0.0715, 0.0609
# values with nbtag = 0 cut \

fe_et, ft_et, fm_mt, ft_mt, f1_tt, f2_tt, fe_em, fm_em  = 0.0073, 0.1327, 0.0434, 0.1087,0.1318, 0.1327, 0.0101, 0.0380
if era == '2017' : fe_et, ft_et, fm_mt, ft_mt, f1_tt, f2_tt, fe_em, fm_em  = 0.0082, 0.1236, 0.0581, 0.1083, 0.1146,0.1160,0.0081, 0.0346
if era == '2018' : fe_et, ft_et, fm_mt, ft_mt, f1_tt, f2_tt, fe_em, fm_em  = 0.0083,0.1199, 0.0598, 0.1105, 0.1178, 0.1121, 0.01009, 0.0440


#define the tightiD WP

'''
fW1, fW2, fW0 = {}, {}, {}
fW1['et'], fW2['et'], fW0['et'] = getFakeWeights('e_et','t_et', WP)
fW1['mt'], fW2['mt'], fW0['mt'] = getFakeWeights('m_mt','t_mt', WP)
fW1['tt'], fW2['tt'], fW0['tt'] = getFakeWeights('t1_tt','t2_tt', WP)
fW1['em'], fW2['em'], fW0['em'] = getFakeWeights('e_em','m_em', WP)
'''

global getsf,sf


plotSettings = { # [nBins,xMin,xMax,units]

        "weight":[20,-10,10,"","PUWeight"],
        "weightPUtrue":[20,-10,10,"","PUtrue"],
        "weightPUtrue":[20,-10,10,"","PU"],
        "nPV":[120,-0.5,119.5,"","nPV"],
        "nPU":[130,-0.5,129.5,"","nPU"],
        "nPUtrue":[130,-0.5,129.5,"","nPUtrue"],
        "Generator_weight":[20,-10,10,"","genWeight"],

        "pt_1":[8,0,160,"[Gev]","P_{T}(#tau_{1})"],
        "eta_1":[30,-3,3,"","#eta(l_{1})"],
        "phi_1":[30,-3,3,"","#phi(l_{1})"],
        "iso_1":[20,0,1,"","relIso(l_{1})"],
        "dZ_1":[10,-0.1,0.1,"[cm]","d_{z}(l_{1})"],
        "d0_1":[10,-0.1,0.1,"[cm]","d_{xy}(l_{1})"],
        "q_1":[3,-1.5,1.5,"","charge(l_{1})"],

        "pt_2":[8,0,160,"[Gev]","P_{T}(l_{2})"],
        "eta_2":[30,-3,3,"","#eta(l_{2})"],
        "phi_2":[30,-3,3,"","#phi(l_{2})"],
        "iso_2":[20,0,1,"","relIso(l_{2})"],
        "dZ_2":[10,-0.1,0.1,"[cm]","d_{z}(l_{2})"],
        "d0_2":[10,-0.1,0.1,"[cm]","d_{xy}(l_{2})"],
        "q_2":[3,-1.5,1.5,"","charge(l_{2})"],

	"iso_3":[20,0,1,"","relIso(l_{3})"],
        "pt_3":[8,0,160,"[Gev]","P_{T}(l_{3})"],
        "eta_3":[30,-3,3,"","#eta(l_{3})"],
        "phi_3":[30,-3,3,"","#phi(l_{3})"],
        "dZ_3":[10,-0.1,0.1,"[cm]","d_{z}(l_{3})"],
        "d0_3":[10,-0.1,0.1,"[cm]","d_{xy}(l_{3})"],

        "iso_4":[20,0,1,"","relIso(l_{4})"],
        "pt_4":[8,0,160,"[Gev]","P_{T}(l_{4})"],
        "eta_4":[30,-3,3,"","#eta(l_{4})"],
        "phi_4":[30,-3,3,"","#phi(l_{4})"],
        "dZ_4":[10,-0.1,0.1,"[cm]","d_{z}(l_{4})"],
        "d0_4":[10,-0.1,0.1,"[cm]","d_{xy}(l_{4})"],

        "njets":[10,-0.5,9.5,"","nJets"],
        #"Jet_pt":[100,0,500,"[GeV]","Jet P_{T}"], 
        #"Jet_eta":[30,-3,3,"","Jet #eta"],
        #"Jet_phi":[30,-3,3,"","Jet #phi"],
        #"Jet_ht":[100,0,800,"[GeV]","H_{T}"],

        "jpt_1":[10,0,200,"[GeV]","Jet^{1} P_{T}"], 
        "jeta_1":[30,-3,3,"","Jet^{1} #eta"],
        "jpt_2":[10,0,200,"[GeV]","Jet^{2} P_{T}"], 
        "jeta_2":[6,-3,3,"","Jet^{2} #eta"],

        "bpt_1":[10,0,200,"[GeV]","BJet^{1} P_{T}"], 
        "bpt_2":[10,0,200,"[GeV]","BJet^{2} P_{T}"], 

        "nbtag":[5,-0.5,4.5,"","nBTag"],
        #"nbtagLoose":[10,0,10,"","nBTag Loose"],
        #"nbtagTight":[5,0,5,"","nBTag Tight"],
        "beta_1":[30,-3,3,"","BJet^{1} #eta"],
        "beta_2":[30,-3,3,"","BJet^{2} #eta"],

        "met":[10,0,200,"[GeV]","#it{p}_{T}^{miss}"], 
        "met_phi":[30,-3,3,"","#it{p}_{T}^{miss} #phi"], 
        "puppi_phi":[30,-3,3,"","PUPPI#it{p}_{T}^{miss} #phi"], 
        "puppimet":[10,0,200,"[GeV]","#it{p}_{T}^{miss}"], 
        #"mt_tot":[100,0,1000,"[GeV]"], # sqrt(mt1^2 + mt2^2)
        #"mt_sum":[100,0,1000,"[GeV]"], # mt1 + mt2

        "mll":[40,50,130,"[Gev]","m(l^{+}l^{-})"],

        "m_vis":[15,50,200,"[Gev]","m(#tau#tau)"],
        "pt_tt":[10,0,200,"[GeV]","P_{T}(#tau#tau)"],
        "H_DR":[60,0,6,"","#Delta R(#tau#tau)"],
        "H_tot":[30,0,200,"[GeV]","m_{T}tot(#tau#tau)"],

        "mt_sv":[10,0,200,"[Gev]","m_{T}(#tau#tau)"],
        "m_sv":[10,0,200,"[Gev]","m(#tau#tau)(SV)"],
        "AMass":[50,50,550,"[Gev]","m_{Z+H}(SV)"],
        #"CutFlowWeighted":[15,0.5,15.5,"","cutflow"],
        #"CutFlow":[15,0.5,15.5,"","cutflow"]

        "Z_Pt":[10,0,200,"[Gev]","P_T(l_{1}l_{2})"],
        "Z_DR":[30,0,6,"[Gev]","#Delta R(l_{1}l_{2})"],



        "inTimeMuon_1":[3,-1.5,1.5,"","inTimeMuon_1"],
        "isGlobal_1":[3,-1.5,1.5,"","isGlobal_1"],
        "isTracker_1":[3,-1.5,1.5,"","isTracker_1"],
        "looseId_1":[3,-1.5,1.5,"","looseId_1"],
        "mediumId_1":[3,-1.5,1.5,"","mediumId_1"],
        "Electron_mvaFall17V2noIso_WP90_1":[3,-1.5,1.5,"","Electron_mvaFall17V2noIso_WP90_1"],
        "gen_match_1":[30,-0.5,29.5,"","gen_match_1"],


        "inTimeMuon_2":[3,-1.5,1.5,"","inTimeMuon_2"],
        "isGlobal_2":[3,-1.5,1.5,"","isGlobal_2"],
        "isTracker_2":[3,-1.5,1.5,"","isTracker_2"],
        "looseId_2":[3,-1.5,1.5,"","looseId_2"],
        "mediumId_2":[3,-1.5,1.5,"","mediumId_2"],
        "Electron_mvaFall17V2noIso_WP90_2":[3,-1.5,1.5,"","Electron_mvaFall17V2noIso_WP90_2"],
        "gen_match_2":[30,-0.5,29.5,"","gen_match_2"],



        "inTimeMuon_3":[3,-1.5,1.5,"","inTimeMuon_3"],
        "isGlobal_3":[3,-1.5,1.5,"","isGlobal_3"],
        "isTracker_3":[3,-1.5,1.5,"","isTracker_3"],
        "looseId_3":[3,-1.5,1.5,"","looseId_3"],
        "mediumId_3":[3,-1.5,1.5,"","mediumId_3"],
        "Electron_mvaFall17V2noIso_WP90_3":[3,-1.5,1.5,"","Electron_mvaFall17V2noIso_WP90_3"],
        "gen_match_3":[30,-0.5,29.5,"","gen_match_3"],



        "inTimeMuon_4":[3,-1.5,1.5,"","inTimeMuon_4"],
        "isGlobal_4":[3,-1.5,1.5,"","isGlobal_4"],
        "isTracker_4":[3,-1.5,1.5,"","isTracker_4"],
        "looseId_4":[3,-1.5,1.5,"","looseId_4"],
        "mediumId_4":[3,-1.5,1.5,"","mediumId_4"],
        "Electron_mvaFall17V2noIso_WP90_4":[3,-1.5,1.5,"","Electron_mvaFall17V2noIso_WP90_4"],
        "gen_match_4":[30,-0.5,29.5,"","gen_match_4"],

        "idDeepTau2017v2p1VSjet_3":[256,-0.5,255.5,"","#tau_deepiD_3"],
        "idDeepTau2017v2p1VSjet_4":[256,-0.5,255.5,"","#tau_deepiD_4"],
        "idDeepTau2017v2p1VSmu_3":[256,-0.5,255.5,"","#mu_deepiD_3"],
        "idDeepTau2017v2p1VSe_3":[256,-0.5,255.5,"","e_deepiD_3"],
        "idDeepTau2017v2p1VSmu_4":[256,-0.5,255.5,"","#mu_deepiD_4"],
        "idDeepTau2017v2p1VSe_4":[256,-0.5,255.5,"","e_deepiD_4"],

        }





canvasDict = {}
legendDict = {}
cols = len(cats.items()[0:8])
icut=10 ########last filled bin from first round of ntuples
hLabels=[]
rows, cols,nicks = (8, 25,100) 
#hLabels = [[0]*cols]*rows 

hLabels.append('All')
hLabels.append('inJSON')
hLabels.append('METfilter')
hLabels.append('Trigger')
hLabels.append('LeptonCount')
hLabels.append('GoogLeptons')
hLabels.append('LeptonPairs')
hLabels.append('foundZ')
hLabels.append('GoodTauPair')
#hLabels.append('TightTauPair') #bin 10

hLabels.append(str(args.sign)) #bin 11
hLabels.append('goodIso_Id')
hLabels.append('H_LT > '+str(args.LTcut))
hLabels.append('nbtag=0')
hLabels.append('TriggerSF')
hLabels.append('LeptonSF')
hLabels.append('TauID')

WCounter = [[[0 for k in xrange(cols)] for j in xrange(rows)] for i in xrange(nicks)]


for icat,cat in cats.items()[0:8] :
    for plotVar in plotSettings: # add an entry to the plotVar:hist dictionary
        canvasDict.update({plotVar:TCanvas("c_"+plotVar+"_"+cat,"c_"+plotVar+"_"+cat,10,20,1000,700)})
        legendDict.update({plotVar:TLegend(.45,.75,.90,.90)})
        title = plotVar+" ("+cat+")"
        title = "cutflow ("+cat+")"

########## initializing triggers
wpp = 'Medium'
if str(args.bruteworkingPoint=='64') : wpp = 'VTight'

tauSFTool = TauIDSFTool(campaign[args.year],'DeepTau2017v2p1VSjet',wpp)
testool = TauESTool(campaign[args.year])
festool = TauESTool(campaign[args.year])
sf_MuonTrig = SF.SFs()
sf_MuonTrig.ScaleFactor("{0:s}{1:s}".format(TriggerSF['dir'],TriggerSF['fileMuon']))
sf_EleTrig = SF.SFs()
sf_EleTrig.ScaleFactor("{0:s}{1:s}".format(TriggerSF['dir'],TriggerSF['fileElectron']))

sf_MuonId = SF.SFs()
sf_MuonId.ScaleFactor("{0:s}{1:s}".format(LeptonSF['dir'],LeptonSF['fileMuon0p2']))
sf_ElectronId = SF.SFs()
sf_ElectronId.ScaleFactor("{0:s}{1:s}".format(LeptonSF['dir'],LeptonSF['fileElectron0p15']))


#for icat, cat in cats.items()[0:8] :

for icat, cat in cats.items()[0:8] :
    hCutFlow[cat] = {}
    hCutFlowN[cat] = {}
    hCutFlowFM[cat] = {}
    hW[cat] = {}

for group in groups :
    for inick, nickName in enumerate(nickNames[group]) :
        if group == 'data':
	    inFileName = './data/{0:s}/{1:s}/{1:s}.root'.format(args.analysis,nickName)
        for icat, cat in cats.items()[0:8] :
	    #setting up the CutFlow histogram
	    hCutFlow[cat][nickName] = {}
	    hCutFlowN[cat][nickName] = {}
	    hCutFlowFM[cat][nickName] = {}
	    hW[cat][nickName] = {}
	    hW[cat][nickName] = TH1D("hW_"+nickName+"_"+cat,"weights",3,-0.5,2.5)
	    hCutFlowN[cat][nickName] = TH1D("hCutFlow_"+nickName+"_"+cat,"CutFlow",20,-0.5,19.5)
	    hCutFlowFM[cat][nickName] = TH1D("hCutFlowFM_"+nickName+"_"+cat,"CutFlow",20,-0.5,19.5)

	    if group != 'data' :
	        inFileName = '../MC/condor/{0:s}/{1:s}_{2:s}/{1:s}_{2:s}.root'.format(args.analysis,nickName,era)

	    inFile = TFile.Open(inFileName)
	    inFile.cd()

	    print '========================================> will use this one',inFileName, inick, nickName
	    if group != 'data' :
		hCutFlow[cat][nickName] = inFile.Get("hCutFlowWeighted_{0:s}".format(cat))
	    else :
		hCutFlow[cat][nickName] = inFile.Get("hCutFlow_{0:s}".format(cat))

	    for i in range(1,10) :
		WCounter[i-1][icat-1][inick] = float(hCutFlow[cat][nickName].GetBinContent(i))
                hCutFlowN[cat][nickName].SetBinContent(i,WCounter[i-1][icat-1][inick])
		print i, hCutFlow[cat][nickName].GetBinContent(i), hCutFlow[cat][nickName].GetXaxis().GetBinLabel(i), cat, ' <===>', WCounter[i-1][icat-1][inick], nickName

	    inFile.Close()

for group in groups :
    hMC[group] = {}
    hMCFM[group] = {}
    hm_sv_cat[group] = {}
    hm_sv_new[group] = {}
    hm_sv_new_FM[group] = {}
    hw_fm_new[group] = {}

    hTriggerW[group] = {}
    hLeptonW[group] = {}
    hmt_sv_new[group] = {}
    hmt_sv_new_FM[group] = {}
    hH_LT[group] = {}
    hH_LT_FM[group] = {}
    hCutFlowPerGroup[group] = {}
    hCutFlowPerGroupFM[group] = {}
    for icat, cat in cats.items()[0:8] :
        hMC[group][cat] = {}
        hMCFM[group][cat] = {}
        hName = 'h{0:s}_{1:s}'.format(group,cat)
        hm_sv_cat[group][cat] = TH1D(hName+'_m_sv_cat',hName+'_m_sv_cat',10,0,200)
        hm_sv_cat[group][cat].SetDefaultSumw2()
        hm_sv_new[group][cat] = TH1D(hName+'_m_sv_new',hName+'_m_sv_new',10,0,200)
        hm_sv_new[group][cat].SetDefaultSumw2()
        hm_sv_new_FM[group][cat] = TH1D(hName+'_m_sv_new_FM',hName+'_m_sv_new_FM',10,0,200)
        hm_sv_new_FM[group][cat].SetDefaultSumw2()
        hw_fm_new[group][cat] = TH1D(hName+'_w_fm_new',hName+'_w_fm_new',3,0.5,3.5)
        hw_fm_new[group][cat].SetDefaultSumw2()

        hH_LT[group][cat] = TH1D(hName+'_H_LT',hName+'_H_LT',10,0,200)
        hH_LT[group][cat].SetDefaultSumw2()
        hH_LT_FM[group][cat] = TH1D(hName+'_H_LT_FM',hName+'_H_LT',10,0,200)
        hH_LT_FM[group][cat].SetDefaultSumw2()
        hmt_sv_new[group][cat] = TH1D(hName+'_mt_sv_new',hName+'_mt_sv_new',10,0,200)
        hmt_sv_new[group][cat].SetDefaultSumw2()
        hmt_sv_new_FM[group][cat] = TH1D(hName+'_mt_sv_new_FM',hName+'_mt_sv_new_FM',10,0,200)
        hmt_sv_new_FM[group][cat].SetDefaultSumw2()
        hTriggerW[group][cat] = TH1D (hName+'_TriggerW',hName+'_TriggerW',75,0.75,1.50)
        hLeptonW[group][cat] = TH1D (hName+'_LeptonW',hName+'_LeptonW',40,0.8,1.2)
        hTriggerW[group][cat].SetDefaultSumw2()
        hLeptonW[group][cat].SetDefaultSumw2()

        hCutFlowPerGroup[group][cat] = {}
        hCutFlowPerGroupFM[group][cat] = {}
        hCutFlowPerGroup[group][cat] = TH1D("hCutFlowPerGroup_"+group+"_"+cat,"PerGroupCutFlow",20,-0.5,19.5)
        hCutFlowPerGroupFM[group][cat] = TH1D("hCutFlowPerGroupFM_"+group+"_"+cat,"PerGroupCutFlowFM",20,-0.5,19.5)

        for plotVar in plotSettings:
            hMC[group][cat][plotVar] = {}
            hMCFM[group][cat][plotVar] = {}
            nBins = plotSettings[plotVar][0]
            xMin = plotSettings[plotVar][1]
            xMax = plotSettings[plotVar][2]
            units = plotSettings[plotVar][3]
            lTitle = plotSettings[plotVar][4]
            hName = 'h{0:s}_{1:s}_{2:s}'.format(group,cat,plotVar)
            
            binwidth = (xMax - xMin)/nBins
            hMC[group][cat][plotVar] = TH1D(hName,hName,nBins,xMin,xMax)
            hMC[group][cat][plotVar].SetDefaultSumw2()
            hMC[group][cat][plotVar].GetXaxis().SetTitle(lTitle + ' ' + units)
            if 'GeV' in units : hMC[group][cat][plotVar].GetYaxis().SetTitle("Events / "+str(binwidth)+" {0:s}".format(units))
            if 'GeV' not in units : hMC[group][cat][plotVar].GetYaxis().SetTitle("Events / "+str(binwidth))

            hName = 'h{0:s}_{1:s}_{2:s}_FM'.format(group,cat,plotVar)
            hMCFM[group][cat][plotVar] = TH1D(hName,hName,nBins,xMin,xMax)
            hMCFM[group][cat][plotVar].SetDefaultSumw2()
            hMCFM[group][cat][plotVar].GetXaxis().SetTitle(lTitle + ' ' + units)
            if 'GeV' in units : hMCFM[group][cat][plotVar].GetYaxis().SetTitle("Events / "+str(binwidth)+" {0:s}".format(units))
            if 'GeV' not in units : hMCFM[group][cat][plotVar].GetYaxis().SetTitle("Events / "+str(binwidth))

            #print '=======', nBins, xMin, xMax, hMC[group][cat][plotVar].GetName(), hMC[group][cat][plotVar].GetTitle()

	print("\nInstantiating TH1D {0:s}".format(hName))
	print("      Nickname                 Entries    Wt/Evt  Ngood   Tot Wt")

    for inick, nickName in enumerate(nickNames[group]) :

        if 'DY' in nickName : isDY = True
	if 'JetsToLNu' in nickName : isW = True
        #print 'names are====================>', hMC[group][cat][plotVar].GetName()

        isData = False 
        inFileName = '../MC/condor/{0:s}/{1:s}_{2:s}/{1:s}_{2:s}.root'.format(args.analysis,nickName,era)
	#cf = os.path.isfile('{0:s}'.format(inFileName))
	#if not cf : continue
        if group == 'data' :
            isData = True
            inFileName = './data/{0:s}/{1:s}/{1:s}.root'.format(args.analysis,nickName)
	    print 'for data will use ',inFileName
        try :

            inFile = TFile.Open(inFileName)
            inFile.cd()
            inTree = inFile.Get("Events")
            nentries = inTree.GetEntries()
        except AttributeError :
            print("  Failure on file {0:s}".format(inFileName))
	    #continue
            exit()

        # resume here
        nEvents, totalWeight = 0, 0.
	sWeight = 0.
        DYJets = ('DYJetsToLL' in nickName and 'M10' not in nickName)
        WJets  = ('WJetsToLNu' in nickName)
        sWeight = sampleWeight[nickName]
	print '========================================> start looping on events now',inFileName, inick, nickName

        for i, e in enumerate(inTree) :
            iCut=icut
            hGroup = group
            trigw = 1.
	    weight=1.
            weightCF = 1.
	    weightFM=1.
            weightTID = 1.
	    ww = 1.
            lepton_sf = 1.
            cat = cats[e.cat]
            icat = catToNumber(cat)
            tight1 = True
            tight2 = True
            isfakemc1 = False
            isfakemc2 = False
	    #if ('ZZTo4' in inFileName or 'ZH' in inFileName) and  i > 2000 : continue
	    #if hGroup != 'data' and i > 200:continue

            #sampleWeight = lumi/(WIncl_totgenwt/WIncl_xsec + WxGenweightsArr[i]/(WNJetsXsecs[i]*WJets_kfactor))
            if e.isTrig_1 == 0 and e.isDoubleTrig==0 : continue  
	    if e.q_1*e.q_2 > 0 : continue
            if args.sign == 'SS':
               if e.q_3*e.q_4 < 0. : continue
            else :
                if e.q_3*e.q_4 > 0. : continue

            if WJets and not WIncl_only: 
                if e.LHE_Njets > 0 : sWeight = sampleWeight['W{0:d}JetsToLNu'.format(e.LHE_Njets)]
                elif e.LHE_Njets == 0 : sWeight = sampleWeight['WJetsToLNu']
                #print 'will now be using ',sWeight, e.LHE_Njets, nickName
            if DYJets and not DYIncl_only: 
                if e.LHE_Njets > 0 : sWeight = sampleWeight['DY{0:d}JetsToLL'.format(e.LHE_Njets)]
                elif e.LHE_Njets  : sWeight = sampleWeight['DYJetsToLL']
                #print 'will now be using ',sWeight, e.LHE_Njets, nickName

            if group != 'data' :
		# the pu weight is the e.weight in the ntuples
		#print 'weights', group, nickName, e.Generator_weight, e.weight, i
		weight = e.weightPUtrue * e.Generator_weight *sWeight 
		#ww = e.weightPUtrue * e.Generator_weight *sWeight 
		weightFM = e.weightPUtrue * e.Generator_weight *sWeight
            weightCF = weight

            #weight=1.

            #####sign
            iCut +=1
            WCounter[iCut-1][icat-1][inick] += weightCF
            hCutFlowN[cat][nickName].SetBinContent(iCut-1, hCutFlowN[cat][nickName].GetBinContent(iCut-1)+weight)
            hCutFlowFM[cat][nickName].SetBinContent(iCut-1, hCutFlowFM[cat][nickName].GetBinContent(iCut-1)+weightFM)


            ##############good ISO
	    if cat[:2] == 'mm' and  (e.iso_1 > 0.2 or e.iso_2 > 0.2) : continue
	    if cat[:2] == 'ee' and  (e.iso_1 > 0.15 or e.iso_2 > 0.15) : continue

	    if cat[2:] == 'em'  :
                if  (e.isGlobal_4 < 1 and e.isTracker_4 < 1) : continue
	    if cat[2:] == 'mt':
                if  (e.isGlobal_3 < 1 and e.isTracker_3 < 1) : continue

	    if cat[2:] == 'em' :
                if e.iso_4 > 0.20 or e.tightId_4 < 1 : tight2 = False

	    if cat[2:] == 'mt' :
                if e.iso_3 > 0.20 or e.tightId_3 < 1 : tight1 = False

	    if (cat[2:] == 'et' or cat[2:] == 'em') and e.Electron_mvaFall17V2noIso_WP90_3 < 1 or e.iso_3 > 0.15 : tight1 = False

	    #if abs(e.dZ_3) > 0.02 or abs(e.dZ_4) > 0.02 : continue
	    #if abs(e.d0_3) > 0.02 or abs(e.d0_4) > 0.02 : continue

            
	    if cat[2:] == 'tt' and e.idDeepTau2017v2p1VSjet_3 < WPSR-1  : tight1 = False
	    if cat[2:] == 'tt' and e.idDeepTau2017v2p1VSjet_4 < WPSR-1 : tight2 = False

	    if cat[2:] == 'mt' and e.idDeepTau2017v2p1VSjet_4 < WPSR-1 : tight2 = False
	    if cat[2:] == 'et' and e.idDeepTau2017v2p1VSjet_4 < WPSR-1 : tight2 = False

	    if cat[2:] == 'et' and e.Electron_mvaFall17V2noIso_WP90_3 < 1 : tight1 = False
            
            if group != 'data' :
                if not tight1 or not tight2 : continue

            #if group == 'data' :
            #    if DD[cat].checkEvent(e,cat) : continue 

            iCut +=1
            WCounter[iCut-1][icat-1][inick] += weightCF
            hCutFlowN[cat][nickName].SetBinContent(iCut-1, hCutFlowN[cat][nickName].GetBinContent(iCut-1)+weight)
            hCutFlowFM[cat][nickName].SetBinContent(iCut-1, hCutFlowFM[cat][nickName].GetBinContent(iCut-1)+weightFM)


            ########H_LT
            H_LT = e.pt_3 + e.pt_4
            if H_LT < args.LTcut : continue


            iCut +=1
            WCounter[iCut-1][icat-1][inick] += weightCF
            hCutFlowN[cat][nickName].SetBinContent(iCut-1, hCutFlowN[cat][nickName].GetBinContent(iCut-1)+weight)
            hCutFlowFM[cat][nickName].SetBinContent(iCut-1, hCutFlowFM[cat][nickName].GetBinContent(iCut-1)+weightFM)

            ######### nbtag
	    if e.nbtag > 0 : continue
	    #if e.mll > 100 or e.mll<80: continue



            iCut +=1
            WCounter[iCut-1][icat-1][inick] += weightCF
            hCutFlowN[cat][nickName].SetBinContent(iCut-1, hCutFlowN[cat][nickName].GetBinContent(iCut-1)+weight)
            hCutFlowFM[cat][nickName].SetBinContent(iCut-1, hCutFlowFM[cat][nickName].GetBinContent(iCut-1)+weightFM)

            ########### Trigger
            ################### Trigger SF
            #if e.isTrig_1 == 0 and e.isDoubleTrig==0: continue  


            #SingleLepton is fired but no DoubleLepton
            if e.isTrig_1 != 0: 

                #leading fired the trigger
		if e.isTrig_1 == 1 and e.isTrig_2 == 0: 
		    if cat[:2] == 'mm' and e.pt_1 < 29 : continue
		    if cat[:2] == 'ee' and era == '2016' and e.pt_1 < 29 : continue
		    if cat[:2] == 'ee' and era != '2016' and e.pt_1 < 37 : continue

		#subleading fired the trigger
		if e.isTrig_1 == -1 and e.isTrig_2 == 0: 
		#if e.isTrig_1 == -1 : 
		    if cat[:2] == 'mm' and e.pt_2 < 29 : continue
		    if cat[:2] == 'ee' and era == '2016' and e.pt_2 < 29 : continue
		    if cat[:2] == 'ee' and era != '2016' and e.pt_2 < 37 : continue

		# both fired the trigger _isTrig_2 = 1
		
		if e.isTrig_2 == 1 : 
		    if cat[:2] == 'mm' and e.pt_1 < 29 and e.pt_2 < 29: continue
		    if cat[:2] == 'ee' and era == '2016' and e.pt_1 <  29 and  e.pt_2 < 29 : continue
		    if cat[:2] == 'ee' and era != '2016' and e.pt_1 < 37 and e.pt_2 < 37 : continue
            
            if e.isDoubleTrig!=0 and e.isTrig_1 == 0 : #the DoubleLepton trigger was fired but not the SingleLepton

		if cat[:2] == 'mm' and (e.pt_1 < 19 or e.pt_2 < 10): continue
		if cat[:2] == 'ee' and (e.pt_1 < 25 or e.pt_2 < 14): continue

            if group == 'data' :
                if DD[cat].checkEvent(e,cat) : continue 

	    eff_trig_d_1, eff_trig_d_2 = 1.,1.
	    eff_trig_mc_1, eff_trig_mc_2 = 1.,1.

	    eff_id_d_1, eff_id_d_2, eff_id_d_3, eff_id_d_4 = 1.,1.,1.,1.
	    eff_id_mc_1, eff_id_mc_2, eff_id_mc_3, eff_id_mc_4 = 1.,1.,1.,1.

            if group != 'data' :
		#leading firing the trigger
		if e.isTrig_1 == 1 and e.isTrig_2 == 0 : 


		    if cat[:2] == 'mm' :                
			eff_trig_d_1 =  sf_MuonTrig.get_EfficiencyData(e.pt_1,e.eta_1)
			eff_trig_mc_1 =  sf_MuonTrig.get_EfficiencyMC(e.pt_1,e.eta_1)

		    if cat[:2] == 'ee' :                 
			eff_trig_d_1 =  sf_EleTrig.get_EfficiencyData(e.pt_1,e.eta_1)
			eff_trig_mc_1 =  sf_EleTrig.get_EfficiencyMC(e.pt_1,e.eta_1)
		    if eff_trig_mc_1 !=0 :		trigw = float(eff_trig_d_1/eff_trig_mc_1)
		    else : continue

		#subleading firing the trigger
		if e.isTrig_1 == -1 and e.isTrig_2 == 0: 
		    if cat[:2] == 'mm' :                 
			eff_trig_d_2 =  sf_MuonTrig.get_EfficiencyData(e.pt_2,e.eta_2)
			eff_trig_mc_2 =  sf_MuonTrig.get_EfficiencyMC(e.pt_2,e.eta_2)

		    if cat[:2] == 'ee' :                 
			eff_trig_d_2 =  sf_EleTrig.get_EfficiencyData(e.pt_2,e.eta_2)
			eff_trig_mc_2 =  sf_EleTrig.get_EfficiencyMC(e.pt_2,e.eta_2)

		    if eff_trig_mc_2 !=0 :		trigw = float(eff_trig_d_2/eff_trig_mc_2)
		    else : continue


		#both firing the trigger
		if e.isTrig_1 == 1 and e.isTrig_2 == 1 : 
		    if cat[:2] == 'mm' :                 
			eff_trig_d_1 =  sf_MuonTrig.get_EfficiencyData(e.pt_1,e.eta_1)
			eff_trig_mc_1 = sf_MuonTrig.get_EfficiencyMC(e.pt_1,e.eta_1)
			eff_trig_d_2 =  sf_MuonTrig.get_EfficiencyData(e.pt_2,e.eta_2)
			eff_trig_mc_2 = sf_MuonTrig.get_EfficiencyMC(e.pt_2,e.eta_2)

		    if cat[:2] == 'ee' :                 
			eff_trig_d_1 =  sf_EleTrig.get_EfficiencyData(e.pt_1,e.eta_1)
			eff_trig_mc_1 =  sf_EleTrig.get_EfficiencyMC(e.pt_1,e.eta_1)
			eff_trig_d_2 =  sf_EleTrig.get_EfficiencyData(e.pt_2,e.eta_2)
			eff_trig_mc_2 =  sf_EleTrig.get_EfficiencyMC(e.pt_2,e.eta_2)

		    if eff_trig_mc_1 != 0 and eff_trig_mc_2 == 0  : 	trigw = float(eff_trig_d_1/eff_trig_mc_1)
		    elif eff_trig_mc_1 == 0 and eff_trig_mc_2 != 0  : trigw = float(eff_trig_d_2/eff_trig_mc_2)
		    elif eff_trig_mc_1 == 0 and eff_trig_mc_2 == 0  : continue 
		    else : 	trigw = float(1- (1-eff_trig_d_1/eff_trig_mc_1) * (1-eff_trig_d_2/eff_trig_mc_2))

		if e.isDoubleTrig!=0 and e.isTrig_1 == 0 : trigw = 1
		weight *= trigw 
		weightFM *= trigw 

            iCut +=1
            WCounter[iCut-1][icat-1][inick] += weightCF
            hCutFlowN[cat][nickName].SetBinContent(iCut-1, hCutFlowN[cat][nickName].GetBinContent(iCut-1)+weight)
            hCutFlowFM[cat][nickName].SetBinContent(iCut-1, hCutFlowFM[cat][nickName].GetBinContent(iCut-1)+weightFM)

            if group != 'data' :
		#############3lepton SFs
		if cat[:2] == 'mm' :                 
			eff_id_d_1 =  sf_MuonId.get_EfficiencyData(e.pt_1,e.eta_1)
			eff_id_mc_1 = sf_MuonId.get_EfficiencyMC(e.pt_1,e.eta_1)

			eff_id_d_2 =  sf_MuonId.get_EfficiencyData(e.pt_2,e.eta_2)
			eff_id_mc_2 = sf_MuonId.get_EfficiencyMC(e.pt_2,e.eta_2)

		if cat[:2] == 'ee' :                 
			eff_id_d_1 =  sf_ElectronId.get_EfficiencyData(e.pt_1,e.eta_1)
			eff_id_mc_1 = sf_ElectronId.get_EfficiencyMC(e.pt_1,e.eta_1)

			eff_id_d_2 =  sf_ElectronId.get_EfficiencyData(e.pt_2,e.eta_2)
			eff_id_mc_2 = sf_ElectronId.get_EfficiencyMC(e.pt_2,e.eta_2)

		if cat[2:] == 'mt' :
			eff_id_d_3 =  sf_MuonId.get_EfficiencyData(e.pt_3,e.eta_3)
			eff_id_mc_3 = sf_MuonId.get_EfficiencyMC(e.pt_3,e.eta_3)

		if cat[2:] == 'et' :
			eff_id_d_3 =  sf_ElectronId.get_EfficiencyData(e.pt_3,e.eta_3)
			eff_id_mc_3 = sf_ElectronId.get_EfficiencyMC(e.pt_3,e.eta_3)

		if cat[2:] == 'em' :               
			eff_id_d_3 =  sf_ElectronId.get_EfficiencyData(e.pt_3,e.eta_3)
			eff_id_mc_3 = sf_ElectronId.get_EfficiencyMC(e.pt_3,e.eta_3)
			eff_id_d_4 =  sf_MuonId.get_EfficiencyData(e.pt_4,e.eta_4)
			eff_id_mc_4 = sf_MuonId.get_EfficiencyMC(e.pt_4,e.eta_4)

		lepton_sf = float (eff_id_d_1/eff_id_mc_1 * eff_id_d_2/eff_id_mc_2 * eff_id_d_3/eff_id_mc_3 * eff_id_d_4/eff_id_mc_4)

		weight *= lepton_sf
		weightFM *= lepton_sf

            iCut +=1
            WCounter[iCut-1][icat-1][inick] += weightCF
            hCutFlowN[cat][nickName].SetBinContent(iCut-1, hCutFlowN[cat][nickName].GetBinContent(iCut-1)+weight)
            hCutFlowFM[cat][nickName].SetBinContent(iCut-1, hCutFlowFM[cat][nickName].GetBinContent(iCut-1)+weightFM)

            ##########
            pfmet_tree = e.met
            puppimet_tree = e.puppimet
            fW1, fW2, fW0 = 0,0,0

	    #if group != 'data' :
            #    if  not tight1 or not tight2 : continue
	    
            #if hGroup == 'data' and not unblind and e.m_sv > 80. and e.m_sv < 140. : continue                 
            dataDriven = True
	    if group == 'data' :
		if dataDriven :
		    fW1, fW2, fW0 = getFakeWeightsvspT(cat[2:], e.pt_3, e.pt_4, WP, tight1, tight2)
		    if not tight1 and tight2 : 
                        ww = fW1          
                        hGroup = 'f1'
		    elif tight1 and not tight2 : 
                        ww = fW2
                        hGroup = 'f2'
		    elif not (tight1 or tight2) : 
                        ww = -fW0
                        hGroup = 'fakes'
		    else :
			hGroup = 'data'
		else :
		    hGroup = 'data'
		    #print("group = data  cat={0:s} tight1={1} tight2={2} ww={3:f}".format(cat,tight1,tight2,ww))
		    if not (tight1 and tight2) : continue 
	

	    else : 
		#print("Good MC event: group={0:s} nickName={1:s} cat={2:s} gen_match_1={3:d} gen_match_2={4:d}".format(
		#    group,nickName,cat,e.gen_match_1,e.gen_match_2))
		if dataDriven :   # include only events with MC matching
		    if cat[2:] == 'em'  :
			if e.gen_match_3 == 0 or e.gen_match_3 == 3 or e.gen_match_3 == 4 or e.gen_match_3 == 5 :
                            isfakemc1 = True
                            if  e.gen_match_3 == 0 : hGroup = 'jfl1'
                            if  e.gen_match_3 == 3 : hGroup = 'ljfl1'
                            if  e.gen_match_3 == 4 : hGroup = 'cfl1'
                            if  e.gen_match_3 == 5 : hGroup = 'bfl1'

			if e.gen_match_4 == 0 or e.gen_match_4 == 3 or e.gen_match_4 == 4 or e.gen_match_4 == 5 :
                            isfakemc2 = True
                            if  e.gen_match_4 == 0 : hGroup = 'jfl2'
                            if  e.gen_match_4 == 3 : hGroup = 'ljfl2'
                            if  e.gen_match_4 == 4 : hGroup = 'cfl2'
                            if  e.gen_match_4 == 5 : hGroup = 'bfl2'
			
		    if cat[2:] == 'et' or cat[2:] == 'mt' :
	                if  e.gen_match_3 == 0 or e.gen_match_3 == 3 or e.gen_match_3 == 4 or e.gen_match_3 == 5 :
                            isfakemc1 = True
                            if  e.gen_match_3 == 0 : hGroup = 'jfl1'
                            if  e.gen_match_3 == 3 : hGroup = 'ljfl1'
                            if  e.gen_match_3 == 4 : hGroup = 'cfl1'
                            if  e.gen_match_3 == 5 : hGroup = 'bfl1'

			if e.gen_match_4 == 0  :
                            isfakemc2 = True
                            hGroup = 'jft2'
			
		    if cat[2:] == 'tt' :
			if e.gen_match_3 == 0  :
                            isfakemc1 = True
                            hGroup = 'jft1'
			if e.gen_match_4 == 0  :
                            isfakemc2 = True
                            hGroup = 'jft2'
		    
            #if group != 'data' and cat[2:] != 'tt' : print 'some info', cat, e.iso_3, e.iso_4, group, hGroup, isfakemc1, isfakemc2

            weightFM=ww
           
            #if group != 'data' and group!='Signal' :
            #    if not isfakemc1 or not isfakemc2  : continue

            ########### tauID
            tauV3.SetPtEtaPhiM(e.pt_3, e.eta_3, e.phi_3, e.m_3)
            tauV4.SetPtEtaPhiM(e.pt_4, e.eta_4, e.phi_4, e.m_4)
            tauV3cor.SetPtEtaPhiM(e.pt_3, e.eta_3, e.phi_3, e.m_3)
            tauV4cor.SetPtEtaPhiM(e.pt_4, e.eta_4, e.phi_4, e.m_4)
	    MetV.SetPx(e.met * cos (e.metphi))
	    MetV.SetPy(e.met * sin (e.metphi))
	    MetVcor.SetPx(e.met * cos (e.metphi))
	    MetVcor.SetPy(e.met * sin (e.metphi))
	    met_x = e.met * cos(e.metphi)
	    met_y = e.met * sin(e.metphi)
	    metcor = e.met
	    

	    if cat[:2] == 'mm' :  
		L1g.SetPtEtaPhiM(e.pt_1_tr, e.eta_1_tr,e.phi_1_tr,muonMass)
		L2g.SetPtEtaPhiM(e.pt_2_tr, e.eta_2_tr,e.phi_2_tr,muonMass)

		L1.SetPtEtaPhiM(e.pt_1, e.eta_1,e.phi_1,muonMass)
		L2.SetPtEtaPhiM(e.pt_2, e.eta_2,e.phi_2,muonMass)
	    if cat[:2] == 'ee' :  
		L1g.SetPtEtaPhiM(e.pt_1_tr, e.eta_1_tr,e.phi_1_tr,electronMass)
		L2g.SetPtEtaPhiM(e.pt_2_tr, e.eta_2_tr,e.phi_2_tr,electronMass)

		L1.SetPtEtaPhiM(e.pt_1, e.eta_1,e.phi_1,electronMass)
		L2.SetPtEtaPhiM(e.pt_2, e.eta_2,e.phi_2,electronMass)

            if group != 'data' :


	        # recoils
		njetsforrecoil = e.njets
		if (isW)  : njetsforrecoil = e.njets + 1
                if isW or isDY :
		    boson = TLorentzVector()
		    if cat[:2] == 'mm' :  
			boson += L1g
			boson += L2g

		    if cat[:2] == 'ee' :  
			boson += L1g
			boson += L2g
                    mett = recoilCorrector.CorrectByMeanResolution( met_x, met_y, boson.Px(), boson.Py(), boson.Px(), boson.Py(), int(njetsforrecoil))
		    metcor = sqrt(mett[0]* mett[0] + mett[1]*mett[1])
		    met_x = mett[0]
		    met_y = mett[1]
		    MetVcor.SetPx(mett[0])
		    MetVcor.SetPy(mett[1])

            if group != 'data' and (cat[2:] == 'et' or cat[2:]  == 'mt' or  cat[2:] == 'tt') :

                # leptons faking taus // muon->tau
		if e.gen_match_4 == 2 or e.gen_match_4 == 4 :
		    if e.decayMode_4 == 1 :  
		        weight *= weights_muToTauFR['DM1']
			tauV4cor  *= (1 +  weights_muTotauES['DM1']*0.01)
			MetVcor +=  tauV4*(1 +  weights_muTotauES['DM1']*0.01)

		    if e.decayMode_4 == 0 :  
			if abs(e.eta_4) < 0.4                        : weightTID *= weights_muToTauFR['lt0p4'] *  weights_mujToTauFR['lt0p4']
			if abs(e.eta_4) > 0.4 and abs(e.eta_4 < 0.8) : weightTID *= weights_muToTauFR['0p4to0p8'] * weights_mujToTauFR['0p4to0p8']
			if abs(e.eta_4) > 0.8 and abs(e.eta_4 < 1.2) : weightTID *= weights_muToTauFR['0p8to1p2'] * weights_mujToTauFR['0p8to1p2']
			if abs(e.eta_4) > 1.2 and abs(e.eta_4 < 1.7) : weightTID *= weights_muToTauFR['1p2to1p7'] * weights_mujToTauFR['1p2to1p7']
			if abs(e.eta_4) > 1.7 and abs(e.eta_4 < 2.3) : weightTID *= weights_muToTauFR['1p7to2p3'] * weights_mujToTauFR['1p7to2p3']
			tauV4cor *= (1 +  weights_muTotauES['DM0']*0.01)
			MetVcor +=   tauV4*(1 +  weights_muTotauES['DM0']*0.01)



                # leptons faking taus // electron->tau
		if e.gen_match_4 == 1 or e.gen_match_4 == 3 :

		    if e.decayMode_4 == 0 :  
			if abs(e.eta_4) < 1.479     : weightTID *= weights_elToTauFR['lt1p479_DM0'] * weights_eljToTauFR['lt1p479_DM0']
			if abs(e.eta_4) > 1.479     : weightTID *= weights_elToTauFR['gt1p479_DM0'] * weights_eljToTauFR['gt1p479_DM0']
			tauV4cor  *= (1 +  weights_elTotauES['DM0']*0.01)
			MetVcor +=   tauV4*(1 +  weights_elTotauES['DM0']*0.01)

		    if e.decayMode_4 == 1 :  
			if abs(e.eta_4) < 1.479     : weightTID *= weights_elToTauFR['lt1p479_DM1'] * weights_eljToTauFR['lt1p479_DM1']
			if abs(e.eta_4) > 1.479     : weightTID *= weights_elToTauFR['gt1p479_DM1'] * weights_eljToTauFR['gt1p479_DM1']
			tauV4cor  *= (1 +  weights_elTotauES['DM1']*0.01)
			MetVcor +=   tauV4*(1 +  weights_elTotauES['DM1']*0.01)

		
                if  cat[2:] == 'tt' :
		    #muon faking _3 tau

		    if e.gen_match_3 == 2 or e.gen_match_3 == 4 :
			if e.decayMode_3 == 1 :  
			    weightTID *= weights_muToTauFR['DM1']
			    tauV3cor  *= (1 +  weights_muTotauES['DM1']*0.01)
			    MetVcor +=   tauV3*(1 +  weights_muTotauES['DM1']*0.01)

			if e.decayMode_3 == 0 :  
			    if abs(e.eta_3) < 0.4                        : weightTID *= weights_muToTauFR['lt0p4'] *  weights_mujToTauFR['lt0p4']
			    if abs(e.eta_3) > 0.4 and abs(e.eta_3 < 0.8) : weightTID *= weights_muToTauFR['0p4to0p8'] * weights_mujToTauFR['0p4to0p8']
			    if abs(e.eta_3) > 0.8 and abs(e.eta_3 < 1.2) : weightTID *= weights_muToTauFR['0p8to1p2'] * weights_mujToTauFR['0p8to1p2']
			    if abs(e.eta_3) > 1.2 and abs(e.eta_3 < 1.7) : weightTID *= weights_muToTauFR['1p2to1p7'] * weights_mujToTauFR['1p2to1p7']
			    if abs(e.eta_3) > 1.7 and abs(e.eta_3 < 2.3) : weightTID *= weights_muToTauFR['1p7to2p3'] * weights_mujToTauFR['1p7to2p3']

			    tauV3cor  *= (1 +  weights_muTotauES['DM0']*0.01)
			    MetVcor +=   tauV3*(1 +  weights_muTotauES['DM0']*0.01)


                    # electron faking _3 tau
		    if e.gen_match_3 == 1 or e.gen_match_3 == 3 :
		        #weightTID *= festool.getFES(e.eta_3,e.decayMode_3,e.gen_match_3)
			if e.decayMode_3 == 0 :  
			    if abs(e.eta_3) < 1.479     : weightTID *= weights_elToTauFR['lt1p479_DM0'] * weights_eljToTauFR['lt1p479_DM0']
			    if abs(e.eta_3) > 1.479     : weightTID *= weights_elToTauFR['gt1p479_DM0'] * weights_eljToTauFR['gt1p479_DM0']
			    tauV3cor  *= (1 +  weights_elTotauES['DM0']*0.01)
			    MetVcor +=   tauV3*(1 +  weights_elTotauES['DM0']*0.01)

			if e.decayMode_3 == 1 :  
			    if abs(e.eta_3) < 1.479     : weightTID *= weights_elToTauFR['lt1p479_DM1'] * weights_eljToTauFR['lt1p479_DM1']
			    if abs(e.eta_3) > 1.479     : weightTID *= weights_elToTauFR['gt1p479_DM1'] * weights_eljToTauFR['gt1p479_DM1']

			    tauV3cor  *= (1 +  weights_elTotauES['DM1']*0.01)
			    MetVcor +=   tauV3*(1 +  weights_elTotauES['DM1']*0.01)
		if cat[2:] == 'tt' and e.gen_match_3 == 5 : 
			weightTID *= tauSFTool.getSFvsPT(e.pt_3,e.gen_match_3)
			tauV3cor *= testool.getTES(e.pt_3, e.decayMode_3, e.gen_match_3)
			if e.decayMode_3 == 1 : 
			    e.m_3 =  0.1396  
			    tauV3cor.SetE(0.1396)
			MetVcor +=   tauV3 - tauV3cor

                if  cat[2:] == 'tt' or cat[2:] == 'mt' or cat[2:] == 'et' :
		    if e.gen_match_4 == 5 : 
			weightTID *= tauSFTool.getSFvsPT(e.pt_4,e.gen_match_4)
			tauV4cor *= testool.getTES(e.pt_4, e.decayMode_4, e.gen_match_4)
			if e.decayMode_4 == 1 : 
			    e.m_4 =  0.1396  
			    tauV4cor.SetE(0.1396)
			MetVcor+=   tauV4 - tauV4cor

                #if isW or isDY : print 'try', MetVcor.Pt(), MetV.Pt()
                '''   
                e.met = MetVcor.Pt()
                e.metphi = MetVcor.Phi()
		e.pt_3 = tauV3cor.Pt()
		e.phi_3 = tauV3cor.Phi()
		e.eta_3 = tauV3cor.Eta()
		e.m3_3 = tauV3cor.M()
		e.pt_4 = tauV4cor.Pt()
		e.phi_4 = tauV4cor.Phi()
		e.eta_4 = tauV4cor.Eta()
		e.m3_4 = tauV4cor.M()
                '''

                weight *= weightTID
                #weightFM *= weightTID * ww

            iCut +=1
            WCounter[iCut-1][icat-1][inick] += weightCF
            hCutFlowN[cat][nickName].SetBinContent(iCut-1, hCutFlowN[cat][nickName].GetBinContent(iCut-1)+weight)
            hCutFlowFM[cat][nickName].SetBinContent(iCut-1, hCutFlowFM[cat][nickName].GetBinContent(iCut-1)+weightFM)
            #####
            #if not tight1 or not tight2 : hGroup = 'fakes'

	    if not tight1 and tight2: hw_fm_new[hGroup][cat].Fill(1,fW1 )
	    if tight1 and not tight2 : hw_fm_new[hGroup][cat].Fill(2,fW2 )
	    if not tight1 and not tight2: hw_fm_new[hGroup][cat].Fill(3,fW0)
            #if group!='data' and group!='fakes' and group !='f1' and group !='f2' and (not tight1 or not tight2) : print weightFM , hGroup, cat, tight1, tight2, i, e.evt, nickName, fW1, fW2, fW0, e.gen_match_3, e.gen_match_4
           
            #print 'made thus far', leptons_sf
	    fastMTTmass, fastMTTtransverseMass = -1, -1
	    if args.redoFit.lower() == 'yes' or args.redoFit.lower() == 'true' : fastMTTmass, fastMTTtransverseMass = runSVFit(e, cat[2:]) 
	    #print 'new', fastMTTmass, 'old', e.m_sv, fastMTTtransverseMass, e.mt_sv, cat[2:]


	    for plotVar in plotSettings:
		#print plotVar
		val = getattr(e, plotVar, None)
		if val is not None: 
		    if hGroup != 'data' : 
		        if hGroup !='fakes' and hGroup !='f1' and hGroup != 'f2' : 
                            hMC[hGroup][cat][plotVar].Fill(val,weight)
		            if not isfakemc1 and not isfakemc2 and tight1 and tight2: hMCFM[hGroup][cat][plotVar].Fill(val,weight)

		        if hGroup =='fakes' or hGroup =='f1' or hGroup == 'f2' :  hMCFM[hGroup][cat][plotVar].Fill(val,ww)

		    else : 
		        if tight1 and tight2 : 
		            hMC[hGroup][cat][plotVar].Fill(val,1)
		            hMCFM[hGroup][cat][plotVar].Fill(val,1)

		    #print hGroup, cat, plotVar, val
            #custom made variables

            tauV = tauV3cor + tauV4cor

            

	    if hGroup != 'data' : 
		if hGroup !='fakes' and hGroup !='f1' and hGroup != 'f2' : 
	            hm_sv_new[hGroup][cat].Fill(fastMTTmass,weight )
	            hmt_sv_new[hGroup][cat].Fill(fastMTTtransverseMass,weight )
	            hH_LT[hGroup][cat].Fill(H_LT,weight )


		    if not isfakemc1 and not isfakemc2 and tight1 and tight2: 
	                hm_sv_new_FM[hGroup][cat].Fill(fastMTTmass,weight )
	                hH_LT_FM[hGroup][cat].Fill(H_LT,weight )

		if hGroup =='fakes' or hGroup =='f1' or hGroup == 'f2' :  
                    hMCFM[hGroup][cat][plotVar].Fill(val,ww)
		    hm_sv_new_FM[hGroup][cat].Fill(fastMTTmass,ww )
		    hH_LT_FM[hGroup][cat].Fill(H_LT,ww )

            if group != 'data' : 
	        hLeptonW[group][cat].Fill(lepton_sf)
                hTriggerW[group][cat].Fill(trigw)
                    

	    nEvents += 1

        
	print("{0:30s} {1:7d} {2:10.6f} {3:5d}".format(nickName,nentries,sampleWeight[nickName],nEvents))
        
        inFile.Close()

htest={}

fOut.cd()
for group in ngroups:
    for icat, cat in cats.items()[0:8] :
        
	for i in range(len(hLabels)) : 
	    hCutFlowPerGroup[group][cat].GetXaxis().SetBinLabel(i+1, hLabels[i])
	    hCutFlowPerGroupFM[group][cat].GetXaxis().SetBinLabel(i+1, hLabels[i])

	for inick,nickName in enumerate(nickNames[group]) :
	    #for i in range(1,  hCutFlowN[cat][nickName].GetNbinsX()) : 
		#hCutFlowN[cat][nickName].SetBinContent(i, WCounter[i-1][icat-1][inick])

		#if 'DY' in nickName : print 'content now', i, hCutFlowN[cat][nickName].GetBinContent(i), 'for cat and nickName', cat, nickName, hCutFlowPerGroup[group][cat].GetXaxis().GetBinLabel(i), 'weight is ', weight 
	        #for i in range(len(hLabels)) :

	    for i in range(len(hLabels)) : 
		hCutFlowN[cat][nickName].GetXaxis().SetBinLabel(i+1, hLabels[i])
		hCutFlowFM[cat][nickName].GetXaxis().SetBinLabel(i+1, hLabels[i])
		hCutFlowPerGroup[group][cat].GetXaxis().SetBinLabel(i+1, hLabels[i])
		hCutFlowPerGroupFM[group][cat].GetXaxis().SetBinLabel(i+1, hLabels[i])

            #if  'data' not in nickName: 
                #hCutFlowN[cat][nickName].Scale(weight)

	    hCutFlowPerGroup[group][cat].Add(hCutFlowN[cat][nickName])
	    hCutFlowPerGroupFM[group][cat].Add(hCutFlowFM[cat][nickName])

	    hCutFlowN[cat][nickName].Write()
	    hCutFlowFM[cat][nickName].Write()
	
	hCutFlowPerGroup[group][cat].Write()
	hCutFlowPerGroupFM[group][cat].Write()


        htest = TH1D("hCutFlowAllGroup_"+cat,"AllGroupCutFlow",20,-0.5,19.5)
        if 'data' not in group and 'Signal' not in group : htest.Add(hCutFlowPerGroup[group][cat])

        OverFlow(hm_sv_new[group][cat])
        OverFlow(hmt_sv_new[group][cat])
        OverFlow(hm_sv_new_FM[group][cat])
        OverFlow(hmt_sv_new_FM[group][cat])
        OverFlow(hH_LT[group][cat])
        OverFlow(hH_LT_FM[group][cat])
        OverFlow(hdPhi_l1H[group][cat])
        OverFlow(hdPhi_l2H[group][cat])
        OverFlow(hdPhi_lH[group][cat])
        OverFlow(hdR_l1H[group][cat])
        OverFlow(hdR_l2H[group][cat])
        OverFlow(hdR_lH[group][cat])
        OverFlow(hdEta_l1H[group][cat])
        OverFlow(hdEta_l2H[group][cat])
        OverFlow(hdEta_lH[group][cat])

        hm_sv_new[group][cat].Write()
        hmt_sv_new[group][cat].Write()
        hm_sv_new_FM[group][cat].Write()
        hmt_sv_new_FM[group][cat].Write()
	hw_fm_new[hGroup][cat].Write()
        hH_LT[group][cat].Write()
        hH_LT_FM[group][cat].Write()
        hLeptonW[group][cat].Write()
        hTriggerW[group][cat].Write()

        for plotVar in plotSettings:
            OverFlow(hMC[group][cat][plotVar])
	    #if 'gen_match' not in plotVar and 'CutFlow' not in plotVar and 'iso' not in plotVar: 
            #    hMC[group][cat][plotVar].Rebin(2)
            #    hMCFM[group][cat][plotVar].Rebin(2)
            hMC[group][cat][plotVar].Write()
            OverFlow(hMCFM[group][cat][plotVar])
            hMCFM[group][cat][plotVar].Write()
    htest.Write()

for cat in cats.values():
    print("Duplicate summary for {0:s}".format(cat))
    DD[cat].printSummary()
    


