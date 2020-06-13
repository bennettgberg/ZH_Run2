#!/usr/bin/env python

""" HAA.py: makes an nTuple for the H->aa->2l2tau analysis """

__author__ = "Dan Marlow, Alexis Kalogeropoulos, Gage DeZoort" 
__version__ = "GageDev_v1.1"

# import external modules 
import sys
import numpy as np
from ROOT import TObject, TFile, TTree, TH1, TH1D, TCanvas, TLorentzVector  
from math import sqrt, pi

# import from ZH_Run2/funcs/
sys.path.insert(1,'../funcs/')
sys.path.insert(1,'../SVFit/')
import tauFun
import generalFunctions as GF 
import outTuple
import time

def getArgs() :
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","--verbose",default=0,type=int,help="Print level.")
    parser.add_argument("-f","--inFileName",default='ZHtoTauTau_test.root',help="File to be analyzed.")
    parser.add_argument("-c","--category",default='none',help="Event category to analyze.")
    parser.add_argument("--nickName",default='',help="MC sample nickname") 
    parser.add_argument("-d","--dataType",default='MC',help="Data or MC") 
    parser.add_argument("-o","--outFileName",default='',help="File to be used for output.")
    parser.add_argument("-n","--nEvents",default=0,type=int,help="Number of events to process.")
    parser.add_argument("-m","--maxPrint",default=0,type=int,help="Maximum number of events to print.")
    parser.add_argument("--maxprint2",default=0,type=int,help="Maximum number of events to print.")
    parser.add_argument("-t","--testMode",default='',help="tau MVA selection")
    parser.add_argument("-y","--year",default=2016,type=int,help="Data taking period, 2016, 2017 or 2018")
    parser.add_argument("--csv",default="MCsamples_2016.csv",help="CSV file for samples")
    parser.add_argument("-s","--selection",default='HAA',help="is this for the ZH,AZH, or HAA analysis?")
    parser.add_argument("-u","--unique",default='none',help="CSV file containing list of unique events for sync studies.") 
    parser.add_argument("-w","--weights",default=False,type=int,help="to re-estimate Sum of Weights")
    parser.add_argument("-j","--doSystematics",type=str, default='false',help="do JME systematics")
    parser.add_argument("-g","--genMatch",default=0,type=int,help="Store 1st order Gen Matching for candidates")
    
    return parser.parse_args()

args = getArgs()
print("args={0:s}".format(str(args)))
maxPrint = args.maxPrint 

cutCounter = {}
cutCounterGenWeight = {}

cats = ['mmet','mmmt','mmtt','mmem']
#cats = ['mmmt']
#cats = ['tttt'] # quad tau final state later??
doJME  = args.doSystematics.lower() == 'true' or args.doSystematics.lower() == 'yes' or args.doSystematics == '1'

for cat in cats : 
    cutCounter[cat] = GF.cutCounter()
    cutCounterGenWeight[cat] = GF.cutCounter()

inFileName = args.inFileName
print("Opening {0:s} as input.  Event category {1:s}".format(inFileName,cat))

isAZH=False
if str(args.selection) == 'AZH' : isAZH = True
if isAZH : print 'You are running on the AZH mode !!!'

inFile = TFile.Open(inFileName)
inFile.cd()
inTree = inFile.Get("Events")
nentries = inTree.GetEntries()
nMax = nentries
print("nentries={0:d} nMax={1:d}".format(nentries,nMax))
if args.nEvents > 0 : nMax = min(args.nEvents-1,nentries)


MC = len(args.nickName) > 0 
if args.dataType == 'Data' or args.dataType == 'data' : MC = False
if args.dataType == 'MC' or args.dataType == 'mc' : MC = True

if MC :
    print "this is MC, will get PU etc", args.dataType
    PU = GF.pileUpWeight()
    PU.calculateWeights(args.nickName,args.year,args.csv)
else :
    CJ = ''#GF.checkJSON(filein='Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt')
    if args.year == 2016 : CJ = GF.checkJSON(filein='Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt')
    if args.year == 2017 : CJ = GF.checkJSON(filein='Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt')
    if args.year == 2018 : CJ = GF.checkJSON(filein='Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt')

varSystematics=['']
if doJME : varSystematics= ['', 'nom', 'jesTotalUp', 'jesTotalDown', 'jerUp', 'jerDown']
if not MC : 
    if doJME : varSystematics= ['', 'nom']

if not doJME  : varSystematics=['']

print 'systematics', doJME, varSystematics

era=str(args.year)

outFileName = GF.getOutFileName(args).replace(".root",".ntup")

if MC : 
    if "WJetsToLNu" in outFileName:
	hWxGenweightsArr = []
	for i in range(5):
	    hWxGenweightsArr.append(TH1D("W"+str(i)+"genWeights",\
		    "W"+str(i)+"genWeights",1,-0.5,0.5))
    elif "DYJetsToLL" in outFileName:
	hDYxGenweightsArr = []
	for i in range(5):
	    hDYxGenweightsArr.append(TH1D("DY"+str(i)+"genWeights",\
		    "DY"+str(i)+"genWeights",1,-0.5,0.5))


if args.weights > 0 :
    hWeight = TH1D("hWeights","hWeights",1,-0.5,0.5)
    hWeight.Sumw2()

    for count, e in enumerate(inTree) :
        hWeight.Fill(0, e.genWeight)
    

        if "WJetsToLNu" in outFileName :

            npartons = ord(e.LHE_Njets)
	    if  npartons <= 4: 	hWxGenweightsArr[npartons].Fill(0, e.genWeight)
        if "DYJetsToLL" in outFileName :
            npartons = ord(e.LHE_Njets)
	    if  npartons <= 4 : hDYxGenweightsArr[npartons].Fill(0, e.genWeight)

    fName = GF.getOutFileName(args).replace(".root",".weights")
    fW = TFile( fName, 'recreate' )
    print 'Will be saving the Weights in', fName
    fW.cd()

    if "WJetsToLNu" in outFileName :
        for i in range(len(hWxGenweightsArr)):
            hWxGenweightsArr[i].Write()
    elif "DYJetsToLL" in outFileName:
        for i in range(len(hDYxGenweightsArr)):
            hDYxGenweightsArr[i].Write()

    hWeight.Write()
    if args.weights == 2 : 
        fW.Close()
        sys.exit()

#############end weights

# read a CSV file containing a list of unique events to be studied 
unique = False 
if args.unique != 'none' :
    unique = True
    uniqueEvents = set()
    for line in open(args.unique,'r').readlines() : uniqueEvents.add(int(line.strip()))
    print("******* Analyzing only {0:d} events from {1:s} ******.".format(len(uniqueEvents),args.unique))
    
print("Opening {0:s} as output.".format(outFileName))
outTuple = outTuple.outTuple(outFileName, era)

if args.genMatch:
    genHistos = {}
    #bins = np.asarray([-1.5,-0.5,0.5,1.5])
    bins2 = np.asarray([-3.5,-1.5,-0.5,0.5,1.5,3.5])
    bins = np.asarray([-3.5,-1.5,-0.5,0.5,1.5,3.5])
    bins.sort()
    bins2.sort()
    algo=0
    for cat in cats:
        #for algo in range(0,2):
            genHistos[cat+":"+str(algo)] = [TH1D(str(cat)+"_"+str(algo)+"_1",str(cat)+"_"+str(algo)+"_1",len(bins)-1,bins),TH1D(str(cat)+"_"+str(algo)+"_2",str(cat)+"_"+str(algo)+"_2",len(bins)-1,bins),TH1D(str(cat)+"_"+str(algo)+"_3",str(cat)+"_"+str(algo)+"_3",len(bins)-1,bins),TH1D(str(cat)+"_"+str(algo)+"_4",str(cat)+"_"+str(algo)+"_4",len(bins)-1,bins)]

tStart = time.time()
countMod = 1000
isMC = True


#The event loop
for count, e in enumerate(inTree) :

    if args.maxprint2:
        GF.printMC(e)
        GF.printEvent(e)
    if count % countMod == 0 :
        print("Count={0:d}".format(count))
        if count >= 10000 : countMod = 10000
    if count == nMax : break    
    
    for cat in cats : 
        cutCounter[cat].count('All')
	if  MC :   cutCounterGenWeight[cat].countGenWeight('All', e.genWeight)

    isInJSON = False
    if not MC : isInJSON = CJ.checkJSON(e.luminosityBlock,e.run)
    if not isInJSON and not MC :
        #print("Event not in JSON: Run:{0:d} LS:{1:d}".format(e.run,e.luminosityBlock))
        continue

    for cat in cats: 
        cutCounter[cat].count('InJSON')
	if  MC :   cutCounterGenWeight[cat].countGenWeight('InJSON', e.genWeight)
    
    MetFilter = GF.checkMETFlags(e,args.year)
    if MetFilter : continue
    
    for cat in cats: 
        cutCounter[cat].count('METfilter') 
	if  MC :   cutCounterGenWeight[cat].countGenWeight('METfilter', e.genWeight)

    if unique :
        if e.event in uniqueEvents :
            for cat in cats: cutCounter[cat].count('Unique') 
        else :
            continue
    if not tauFun.goodTrigger(e, args.year) : continue
    
    for cat in cats:
        cutCounter[cat].count('Trigger')
    if  MC :   cutCounterGenWeight[cat].countGenWeight('Trigger', e.genWeight)

    if e.nMuon < 2 : continue 
    for cat in cats[4:] : 
        cutCounter[cat].count('LeptonCount')
    if  MC :   cutCounterGenWeight[cat].countGenWeight('LeptonCount', e.genWeight)


    goodElectronList = tauFun.makeGoodElectronList(e)
    goodMuonList = tauFun.makeGoodMuonList(e)
    goodElectronList, goodMuonList = tauFun.eliminateCloseLeptons(e, goodElectronList, goodMuonList)
    lepList=[] 
    
    if len(goodMuonList) < 2 : continue
    for cat in cats[4:] :
        cutCounter[cat].count('GoodLeptons')
    if  MC :   cutCounterGenWeight[cat].countGenWeight('GoodLeptons', e.genWeight)
        
    #Muon selection algorithm 
    pairList, lepList = tauFun.findLeadMuMu(goodMuonList, e)

    if len(lepList) != 2 : continue
    for cat in cats[4:] : 
        cutCounter[cat].count('LeptonPair')
    if  MC :   cutCounterGenWeight[cat].countGenWeight('LeptonPair', e.genWeight)

    LepP, LepM = pairList[0], pairList[1]
    M = (LepM + LepP).M()

    if not tauFun.mllCut(M) :
        if unique :
            print("Zmass Fail: : Event ID={0:d} cat={1:s} M={2:.2f}".format(e.event,cat,M))
            #GF.printEvent(e)
            #if MC : GF.printMC(e)
        continue ##cut valid for both AZH and ZH

    for cat in cats[4:]: 
        cutCounter[cat].count('FoundZ')
    if  MC :   cutCounterGenWeight[cat].countGenWeight('FoundZ', e.genWeight)

    #now to loop over the categories - all of them have a dimuon pair
    for cat in cats:
        if cat[2:] == 'tt' :
            tauList = tauFun.getTauList(cat, e, pairList=pairList)
            bestTauPair = tauFun.getBestTauPairPt(cat, e, tauList )
                                
        elif cat[2:] == 'et' :
            bestTauPair = tauFun.getBestETauPairPt(e,cat=cat,pairList=pairList)
        elif cat[2:] == 'mt' :
            bestTauPair = tauFun.getBestMuTauPairPt(e,cat=cat,pairList=pairList)
        elif cat[2:] == 'em' :
            bestTauPair = tauFun.getBestEMuTauPairPt(e,cat=cat,pairList=pairList)
        else : continue
        
        if len(bestTauPair) > 1 :
            jt1, jt2 = bestTauPair[0], bestTauPair[1]
            #print "evt ",e.event," best pair pt sum",e.Muon_pt[bestTauPair[0]] + e.Tau_pt[bestTauPair[1]]

            #not done yet! figure efficiency in taus!!
            if bestTauPair and args.genMatch:
                genHistos[cat+":"+str(algo)][2].Fill(10.0)
                genHistos[cat+":"+str(algo)][3].Fill(10.0)
                #print "gen mu id ",e.GenPart_pdgId[e.Muon_genPartIdx[jt1]],"  gen mu mother id ",e.GenPart_pdgId[e.GenPart_genPartIdxMother[e.Muon_genPartIdx[jt1]]]
                tauIdx1 = e.Muon_genPartIdx[jt1]
                #print "tau id 1",tauIdx1
                tauIdx2 = e.Tau_genPartIdx[jt2]
                #print "tau id 2",tauIdx2
                motherIndex1 = 0.0
                motherIndex2 = 0.0
                motherIndex1  = tauFun.findAMother(e,36,tauIdx1)
                #print "final mother index of leg 1",motherIndex1
                motherIndex2  = tauFun.findAMother(e,36,tauIdx2)
                #print "final mother index of leg 2",motherIndex2
                #print jt2,tauIdx
                #print "gen tau id ",e.GenPart_pdgId[e.Tau_genPartIdx[jt2]],"  gen tau mother id ",e.GenPart_pdgId[e.GenPart_genPartIdxMother[e.Tau_genPartIdx[jt2]]]
                if tauIdx1>0 and abs(e.GenPart_pdgId[tauIdx1])==13 and (motherIndex1==motherIndex2):
                    genHistos[cat+":"+str(algo)][2].Fill(2.0)
                elif tauIdx1>0 and abs(e.GenPart_pdgId[tauIdx1])==13 and motherIndex1>0:
                    genHistos[cat+":"+str(algo)][2].Fill(1.0)
                elif tauIdx1>0 and abs(e.GenPart_pdgId[tauIdx1])==13 and motherIndex1==-1:
                    genHistos[cat+":"+str(algo)][2].Fill(-1.0)
                else:
                    genHistos[cat+":"+str(algo)][2].Fill(0.0)
                if tauIdx2>0 and (abs(e.GenPart_pdgId[tauIdx2])==15 or abs(e.GenPart_pdgId[tauIdx2])==17) and (motherIndex1==motherIndex2):
                    genHistos[cat+":"+str(algo)][3].Fill(2.0)
                elif tauIdx2>0 and (abs(e.GenPart_pdgId[tauIdx2])==15 or abs(e.GenPart_pdgId[tauIdx2])==17) and motherIndex2>0:
                    genHistos[cat+":"+str(algo)][3].Fill(1.0)
                elif tauIdx2>0 and (abs(e.GenPart_pdgId[tauIdx2])==15 or abs(e.GenPart_pdgId[tauIdx2])==17) and motherIndex2==-1:
                    genHistos[cat+":"+str(algo)][3].Fill(-1.0)
                else:
                    genHistos[cat+":"+str(algo)][3].Fill(0.0)


        else :
            continue
        cutCounter[cat].count("GoodTauPair")

        if  MC:   cutCounterGenWeight[cat].countGenWeight('GoodTauPair', e.genWeight)

        if MC :
            outTuple.setWeight(PU.getWeight(e.PV_npvs)) 
            outTuple.setWeightPU(PU.getWeight(e.Pileup_nPU)) 
            outTuple.setWeightPUtrue(PU.getWeight(e.Pileup_nTrueInt)) 
        else : 
                outTuple.setWeight(1.) 
                outTuple.setWeightPU(1.) ##
                outTuple.setWeightPUtrue(1.)


        SVFit = False
    
        if not MC : isMC = False
        algo=0
        outTuple.Fill(e,SVFit,cat,jt1,jt2,LepP,LepM,lepList,isMC,era, goodMuonList, algo, doJME, varSystematics) 


        if (pairList and lepList and args.genMatch and len(goodMuonList)>2): 

            daughter1 = e.Muon_genPartIdx[lepList[0]]
            daughter2 = e.Muon_genPartIdx[lepList[1]]
            #print daughter1,daughter2
                
            genHistos[cat+":"+str(algo)][0].Fill(10.0)
            genHistos[cat+":"+str(algo)][1].Fill(10.0)
            #print "event   ",e.event," the dimuon pair selected ", lepList," pt ",pairList[0].Pt()," eta ",pairList[0].Eta()," phi ",pairList[0].Phi()," pt ",pairList[1].Pt()," eta ",pairList[1].Eta()," phi ",pairList[1].Phi()
            motherIndex1 = 0.0
            motherIndex2 = 0.0
            motherIndex1  = tauFun.findAMother(e,36,daughter1)
            #print "final mother index of leg 1",motherIndex1
            motherIndex2  = tauFun.findAMother(e,36,daughter2)
            #print "final mother index of leg 2",motherIndex2

            #if abs(e.GenPart_pdgId[e.Muon_genPartIdx[lepList[0]]])==13 and abs(e.GenPart_pdgId[e.GenPart_genPartIdxMother[e.Muon_genPartIdx[lepList[0]]]])==36 and (e.GenPart_genPartIdxMother[e.Muon_genPartIdx[lepList[0]]]==e.GenPart_genPartIdxMother[e.Muon_genPartIdx[lepList[1]]]):
            if daughter1>0 and abs(e.GenPart_pdgId[daughter1])==13 and (motherIndex1==motherIndex2):
                genHistos[cat+":"+str(algo)][0].Fill(2.0)
            elif daughter1>0 and abs(e.GenPart_pdgId[daughter1])==13 and motherIndex1>0:
                genHistos[cat+":"+str(algo)][0].Fill(1.0)
            elif daughter1>0 and abs(e.GenPart_pdgId[daughter1])==13 and motherIndex1==-1:
                genHistos[cat+":"+str(algo)][0].Fill(-1.0)
            #print " 1 Muon Index ",e.daughter0]]," 1 Muon ID ",e.GenPart_pdgId[e.Muon_genPartIdx[lepList[0]]]," 1 Muon Mother Index ",e.GenPart_genPartIdxMother[e.Muon_genPartIdx[lepList[0]]]," 1 Muon Mother ID ",e.GenPart_pdgId[e.GenPart_genPartIdxMother[e.Muon_genPartIdx[lepList[0]]]]
            else:
                genHistos[cat+":"+str(algo)][0].Fill(0.0)
            #if abs(e.GenPart_pdgId[e.daughter1]]])==13 and abs(e.GenPart_pdgId[e.GenPart_genPartIdxMother[e.Muon_genPartIdx[lepList[1]]]])==36 and (e.GenPart_genPartIdxMother[e.Muon_genPartIdx[lepList[0]]]==e.GenPart_genPartIdxMother[e.Muon_genPartIdx[lepList[1]]]):
            if daughter2>0 and abs(e.GenPart_pdgId[daughter2])==13 and (motherIndex1==motherIndex2):
                genHistos[cat+":"+str(algo)][1].Fill(2.0)
            elif daughter2>0 and abs(e.GenPart_pdgId[daughter2])==13 and motherIndex2>0:
                genHistos[cat+":"+str(algo)][1].Fill(1.0)
            elif daughter2>0 and abs(e.GenPart_pdgId[daughter2])==13 and motherIndex2==-1:
                genHistos[cat+":"+str(algo)][1].Fill(-1.0)
            else:
                genHistos[cat+":"+str(algo)][1].Fill(0.0)

        if maxPrint > 0 :
            maxPrint -= 1
            print("\n\nGood Event={0:d} cat={1:s}  MCcat={2:s}".format(e.event,cat,GF.eventID(e)))
            print("goodMuonList={0:s} goodElectronList={1:s} Mll={2:.1f} bestTauPair={3:s}".format(
                str(goodMuonList),str(goodElectronList),M,str(bestTauPair)))
            print("Lep1.pt() = {0:.1f} Lep2.pt={1:.1f}".format(pairList[0].Pt(),pairList[1].Pt()))
            GF.printEvent(e)
            print("Event ID={0:s} cat={1:s}".format(GF.eventID(e),cat))
                

dT = time.time() - tStart
print("Run time={0:.2f} s  time/event={1:.1f} us".format(dT,1000000.*dT/count))

hLabels=[]
hLabels.append('All')
hLabels.append('inJSON')
hLabels.append('METfilter')
hLabels.append('Trigger')
hLabels.append('LeptonCount')
hLabels.append('GoodLeptons')
hLabels.append('LeptonPair')
hLabels.append('FoundZ')
hLabels.append('GoodTauPair')

hCutFlow=[]
hCutFlowW=[]
for icat,cat in enumerate(cats) :
    print('\nSummary for {0:s}'.format(cat))
    cutCounter[cat].printSummary()
    hName="hCutFlow_"+str(cat)
    hNameW="hCutFlowWeighted_"+str(cat)
    hCutFlow.append( TH1D(hName,hName,20,0.5,20.5))
    if MC  : hCutFlowW.append( TH1D(hNameW,hNameW,20,0.5,20.5))
    #if not MC : lcount=len(cutCounter[cat].getYield()) #lcount stands for how many different values you have
    #else : lcount=len(cutCounterGenWeight[cat].getYieldWeighted()) #lcount stands for how many different values you have
    lcount=len(hLabels)
    print lcount, cat, icat
    for i in range(len(hLabels)) :
        hCutFlow[icat].GetXaxis().SetBinLabel(i+1,hLabels[i])
        if MC : hCutFlowW[icat].GetXaxis().SetBinLabel(i+1,hLabels[i])

    for i in range(lcount) :
        #hCutFlow[cat].Fill(1, float(cutCounter[cat].getYield()[i]))
        yields = cutCounter[cat].getYield()[i]
        hCutFlow[icat].Fill(i+1, float(yields))

        if MC : 
	    yieldsW = cutCounterGenWeight[cat].getYieldWeighted()[i]
            hCutFlowW[icat].Fill(i+1, float(yieldsW))
        #print cutCounter[cat].getYield()[i], i, cutCounter[cat].getLabels()[i]

    
    hCutFlow[icat].Sumw2()
    if MC : hCutFlowW[icat].Sumw2()
    icat+=1

if not MC : CJ.printJSONsummary()


outTuple.writeTree()
