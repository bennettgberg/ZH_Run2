# output ntuple for H->tautau analysis for CMSSW_10_2_X

from ROOT import TLorentzVector, TH1
from math import sqrt, sin, cos, pi
import tauFun 
import ROOT
import os
import sys
import generalFunctions as GF


electronMass = 0.0005
muonMass  = 0.105
class outTuple() :
    
    def __init__(self,fileName, era):
        from array import array
        from ROOT import TFile, TTree

        # Tau Decay types
        self.kUndefinedDecayType, self.kTauToHadDecay,  self.kTauToElecDecay, self.kTauToMuDecay = 0, 1, 2, 3    
        ROOT.gInterpreter.ProcessLine(".include .")
        for baseName in ['MeasuredTauLepton','svFitAuxFunctions','FastMTT'] : 
            if os.path.isfile("{0:s}_cc.so".format(baseName)) :
                ROOT.gInterpreter.ProcessLine(".L {0:s}_cc.so".format(baseName))
            else :
                ROOT.gInterpreter.ProcessLine(".L {0:s}.cc++".format(baseName))   
                # .L is not just for .so files, also .cc
        

        self.f = TFile( fileName, 'recreate' )
        self.t = TTree( 'Events', 'Output tree' )

        self.entries          = 0 
        self.run              = array('l',[0])
        self.nElectron        = array('l',[0])
        self.nMuon            = array('l',[0])
        self.nTau            = array('l',[0])
        self.lumi             = array('l',[0])
        self.is_trig          = array('l',[0])
        self.is_trigH         = array('l',[0])
        self.is_trigZ         = array('l',[0])
        self.is_trigZH        = array('l',[0])
        self.evt              = array('l',[0])
        self.nPU              = array('l',[0])
        self.nPUEOOT              = array('l',[0])
        self.nPULOOT              = array('l',[0])
        self.nPUtrue              = array('f',[0])
        self.nPV              = array('l',[0])
        self.nPVGood              = array('l',[0])
        self.cat              = array('l',[0])
        self.weight           = array('f',[0])
        self.weightPU           = array('f',[0])
        self.weightPUtrue           = array('f',[0])
        self.LHEweight        = array('f',[0])
        self.Generator_weight = array('f',[0])
        self.LHE_Njets        = array('l',[0])
        self.electronTriggerWord  = array('l',[0])
        self.muonTriggerWord  = array('l',[0])         
        
        self.nGoodElectron    = array('l',[0])
        self.nGoodMuon        = array('l',[0])

        self.d0_1        = array('f',[0])
        self.dZ_1        = array('f',[0])
        self.d0_2        = array('f',[0])
        self.dZ_2        = array('f',[0])
        
        self.pt_3        = array('f',[0])
        self.pt_3_tr     = array('f',[0])
        self.GenPart_statusFlags_3     = array('l',[0])
        self.GenPart_status_3     = array('l',[0])
        self.phi_3       = array('f',[0])
        self.phi_3_tr    = array('f',[0])
        self.eta_3       = array('f',[0])
        self.eta_3_tr    = array('f',[0])
        self.m_3         = array('f',[0])
        self.q_3         = array('f',[0])
        self.d0_3        = array('f',[0])
        self.dZ_3        = array('f',[0])
        self.mt_3        = array('f',[0])
        self.pfmt_3      = array('f',[0])
        self.puppimt_3   = array('f',[0])
        self.iso_3       = array('f',[0])
        self.Electron_mvaFall17V2noIso_WP90_1 = array('f',[0])
        self.Electron_mvaFall17V2noIso_WP90_2 = array('f',[0])
        self.Electron_mvaFall17V2noIso_WP90_3 = array('f',[0])
        self.Electron_mvaFall17V2noIso_WP90_4 = array('f',[0])
        self.gen_match_1 = array('l',[0])
        self.gen_match_2 = array('l',[0])
        self.gen_match_3 = array('l',[0])
        self.tightId_3       = array('f',[0])
        self.mediumId_3       = array('f',[0])
        self.mediumPromptId_3       = array('f',[0])
        self.looseId_3       = array('f',[0])
        self.isGlobal_3       = array('f',[0])
        self.isTracker_3       = array('f',[0])
        self.ip3d_3       = array('f',[0])
        self.inTimeMuon_3       = array('f',[0])

        self.idDecayModeNewDMs_3 = array('f',[0])
        self.idDeepTau2017v2p1VSe_3 = array('f',[0])
        self.idDeepTau2017v2p1VSjet_3 = array('f',[0])
        self.idDeepTau2017v2p1VSmu_3 = array('f',[0])
        self.idMVAnewDM2017v2_3 = array('f',[0])
        self.rawMVAnewDM2017v2_3 = array('f',[0])


        self.trigweight_3  = array('f',[0])
        self.idisoweight_3 = array('f',[0])
        self.decayMode_3   = array('l',[0])

        self.pt_4        = array('f',[0])
        self.pt_4_tr     = array('f',[0])
        self.GenPart_statusFlags_4     = array('l',[0])
        self.GenPart_status_4     = array('l',[0])
        self.phi_4       = array('f',[0])
        self.phi_4_tr    = array('f',[0])
        self.eta_4       = array('f',[0])
        self.eta_4_tr    = array('f',[0])
        self.m_4         = array('f',[0])
        self.q_4         = array('f',[0])
        self.d0_4        = array('f',[0])
        self.dZ_4        = array('f',[0])
        self.mt_4        = array('f',[0])
        self.pfmt_4      = array('f',[0])
        self.puppimt_4   = array('f',[0])
        self.iso_4       = array('f',[0])
        self.gen_match_4 = array('l',[0])
        self.tightId_4       = array('f',[0])
        self.mediumId_4       = array('f',[0])
        self.mediumPromptId_4       = array('f',[0])
        self.looseId_4       = array('f',[0])
        self.isGlobal_4       = array('f',[0])
        self.isTracker_4       = array('f',[0])
        self.ip3d_4       = array('f',[0])
        self.inTimeMuon_4       = array('f',[0])


        self.idDecayModeNewDMs_4 = array('f',[0])
        self.idDeepTau2017v2p1VSe_4 = array('f',[0])
        self.idDeepTau2017v2p1VSjet_4 = array('f',[0])
        self.idDeepTau2017v2p1VSmu_4 = array('f',[0])
        self.idMVAnewDM2017v2_4 = array('f',[0])
        self.rawMVAnewDM2017v2_4 = array('f',[0])



        self.pt_5        = array('f',[0])
        self.phi_5       = array('f',[0])
        self.eta_5       = array('f',[0])
        self.m_5         = array('f',[0])
        self.q_5         = array('f',[0])
        self.d0_5        = array('f',[0])
        self.dZ_5      = array('f',[0])
        self.gen_match_5 = array('l',[0])
        self.decayMode_5 = array('l',[0])

        self.idDecayModeNewDMs_5 = array('f',[0])
        self.idDeepTau2017v2p1VSe_5 = array('f',[0])
        self.idDeepTau2017v2p1VSjet_5 = array('f',[0])
        self.idDeepTau2017v2p1VSmu_5 = array('f',[0])
        self.idMVAnewDM2017v2_5 = array('f',[0])
        self.rawMVAnewDM2017v2_5 = array('f',[0])

        self.trigweight_4  = array('f',[0])
        self.idisoweight_4 = array('f',[0])
        self.decayMode_4   = array('l',[0])

        # di-tau variables
        self.pt_tt  = array('f',[0])
        self.mt_tot = array('f',[0])
        self.m_vis  = array('f',[0])
        self.m_sv   = array('f',[0])
        self.mt_sv  = array('f',[0])
        self.H_DR  = array('f',[0])
        self.AMass   = array('f',[0])


        # di-lepton variables.   1 and 2 refer to plus and minus charge
        # ll_lmass is mass of decay lepton 
        self.H_LT       = array('f',[0])
        self.dRl1H       = array('f',[0])
        self.dRl2H       = array('f',[0])
        self.dRlH       = array('f',[0])
        self.dPhil1H       = array('f',[0])
        self.dPhil2H       = array('f',[0])
        self.dPhilH       = array('f',[0])
        self.mll       = array('f',[0])
        self.mll2       = array('f',[0])
        self.Z_Pt       = array('f',[0])
        self.Z_DR       = array('f',[0])
        self.Z_SS       = array('f',[0])
        self.pt_1      = array('f',[0])
        self.m_1_tr   = array('f',[0])
        self.pt_1_tr   = array('f',[0])
        self.GenPart_statusFlags_1   = array('l',[0])
        self.GenPart_status_1     = array('l',[0])
        self.phi_1     = array('f',[0])
        self.phi_1_tr  = array('f',[0])
        self.eta_1     = array('f',[0])
        self.eta_1_tr  = array('f',[0])
        self.pt_2      = array('f',[0])
        self.GenPart_statusFlags_2   = array('l',[0])
        self.GenPart_status_2     = array('l',[0])
        self.m_2_tr   = array('f',[0])
        self.pt_2_tr   = array('f',[0])
        self.phi_2     = array('f',[0])
        self.phi_2_tr  = array('f',[0])
        self.eta_2     = array('f',[0])
        self.eta_2_tr  = array('f',[0])
        self.iso_1       = array('f',[0])
        self.q_1       = array('f',[0])
        self.Muon_Id_1       = array('f',[0])
        self.Muon_Id_2       = array('f',[0])
        self.Muon_Id_3       = array('f',[0])
        self.isGlobal_1       = array('f',[0])
        self.isTracker_1       = array('f',[0])
        self.isTracker_2       = array('f',[0])
        self.isGlobal_2       = array('f',[0])
        self.tightId_1       = array('f',[0])
        self.mediumId_1       = array('f',[0])
        self.mediumPromptId_1       = array('f',[0])
        self.looseId_1       = array('f',[0])
        
        # MET variables
        self.met         = array('f',[0])
        self.metphi      = array('f',[0])
        self.puppimet    = array('f',[0])
        self.puppimetphi = array('f',[0])
        self.metcov00    = array('f',[0])
        self.metcov01    = array('f',[0])
        self.metcov10    = array('f',[0])
        self.metcov11    = array('f',[0])


        #systematics

        self.metpt_nom = array('f',[0])
        self.metphi_nom = array('f',[0])
        self.metpt_JER = array('f',[0])
        self.metphi_JER = array('f',[0])
        self.metpt_JERUp = array('f',[0])
        self.metphi_JERUp = array('f',[0])
        self.metpt_JERDown = array('f',[0])
        self.metphi_JERDown = array('f',[0])
        self.metpt_JESUp = array('f',[0])
        self.metphi_JESUp = array('f',[0])
        self.metpt_JESDown = array('f',[0])
        self.metphi_JESDown = array('f',[0])
        self.metpt_UnclUp = array('f',[0])
        self.metphi_UnclUp = array('f',[0])
        self.metpt_UnclDown = array('f',[0])
        self.metphi_UnclDown = array('f',[0])
        self.met_UnclX = array('f',[0])
        self.met_UnclY = array('f',[0])

        # trigger info
        self.isTrig_2   = array('f',[0])
        self.isTrig_1   = array('f',[0])
        self.isDoubleTrig   = array('f',[0])


        # jet variables
        #self.njetsold = array('f',[-1]*8)
        self.njets     = array('f',[0]*8)
        self.nbtag     = array('f',[0]*8)
        #self.nbtagold     = array('f',[-1]*8)
        self.nbtagT     = array('f',[0]*8)

        self.jpt_1     = array('f',[0]*8)
        self.jpt_1_tr  = array('f',[0]*8)
        self.jeta_1    = array('f',[0]*8)
        self.jeta_1_tr = array('f',[0]*8)
        self.jphi_1    = array('f',[0]*8)
        self.jphi_1_tr = array('f',[0]*8)
        self.jcsv_1    = array('f',[0]*8)
        self.jcsvfv_1    = array('f',[0]*8)
        self.jpt_2     = array('f',[0]*8)
        self.jpt_2_tr  = array('f',[0]*8)
        self.jeta_2    = array('f',[0]*8)
        self.jeta_2_tr = array('f',[0]*8)
        self.jphi_2    = array('f',[0]*8)
        self.jphi_2_tr = array('f',[0]*8)
        self.jcsv_2    = array('f',[0]*8)
        self.jcsvfv_2    = array('f',[0]*8)
        self.iso_2       = array('f',[0])
        self.q_2       = array('f',[0])
        self.tightId_2       = array('f',[0])
        self.mediumId_2       = array('f',[0])
        self.mediumPromptId_2       = array('f',[0])
        self.looseId_2       = array('f',[0])

        self.bpt_1     = array('f',[0]*8)
        self.bpt_1_tr  = array('f',[0]*8)
        self.beta_1    = array('f',[0]*8)
        self.beta_1_tr = array('f',[0]*8)
        self.bphi_1    = array('f',[0]*8)
        self.bphi_1_tr = array('f',[0]*8)
        self.bcsv_1    = array('f',[0]*8)
        self.bcsvfv_1    = array('f',[0]*8)
        self.bpt_2     = array('f',[0]*8)
        self.bpt_2_tr  = array('f',[0]*8)
        self.beta_2    = array('f',[0]*8)
        self.beta_2_tr = array('f',[0]*8)
        self.bphi_2    = array('f',[0]*8)
        self.bphi_2_tr = array('f',[0]*8)
        self.bcsv_2    = array('f',[0]*8)
        self.bcsvfv_2    = array('f',[0]*8)

      
        self.t.Branch('run',              self.run,               'run/l' )
        self.t.Branch('nElectron',              self.nElectron,               'nElectron/l' )
        self.t.Branch('nMuon',              self.nMuon,               'nMuon/l' )
        self.t.Branch('nTau',              self.nTau,               'nTau/l' )
        self.t.Branch('lumi',             self.lumi,              'lumi/I' )
        self.t.Branch('is_trig',          self.is_trig,           'is_trig/I' )
        self.t.Branch('is_trigH',         self.is_trigH,          'is_trigH/I' )
        self.t.Branch('is_trigZ',         self.is_trigZ,          'is_trigZ/I' )
        self.t.Branch('is_trigZH',        self.is_trigZH,         'is_trigZH/I' )
        self.t.Branch('evt',              self.evt,               'evt/I' )
        self.t.Branch('nPU',              self.nPU,               'nPU/I' )
        self.t.Branch('nPUEOOT',              self.nPUEOOT,               'nPUEOOT/I' )
        self.t.Branch('nPULOOT',              self.nPULOOT,               'nPULOOT/I' )
        self.t.Branch('nPUtrue',              self.nPUtrue,               'nPUtrue/F' )
        self.t.Branch('nPV',              self.nPV,               'nPV/I' )
        self.t.Branch('nPVGood',              self.nPVGood,               'nPVGood/I' )
        self.t.Branch('cat',              self.cat,               'cat/I' )
        self.t.Branch('weight',           self.weight,            'weight/F' )
        self.t.Branch('weightPU',           self.weightPU,            'weightPU/F' )
        self.t.Branch('weightPUtrue',           self.weightPUtrue,            'weightPUtrue/F' )
        self.t.Branch('LHEweight',        self.LHEweight,         'LHEweight/F' )
        self.t.Branch('LHE_Njets',        self.LHE_Njets,         'LHE_Njets/I' )
        self.t.Branch('Generator_weight', self.Generator_weight,  'Generator_weight/F' )
        self.t.Branch('electronTriggerWord',  self.electronTriggerWord, 'electronTriggerWord/I' )
        self.t.Branch('muonTriggerWord',      self.muonTriggerWord,  'muonTriggerWord/I' )
        
        self.t.Branch('nGoodElectron',    self.nGoodElectron,     'nGoodElectron/I' )
        self.t.Branch('nGoodMuon',        self.nGoodMuon,         'nGoodMuon/I' )
        
        self.t.Branch('GenPart_statusFlags_1',     self.GenPart_statusFlags_1,     'GenPart_statusFlags_1/I')
        self.t.Branch('GenPart_statusFlags_2',     self.GenPart_statusFlags_2,     'GenPart_statusFlags_2/I')
        self.t.Branch('GenPart_statusFlags_3',     self.GenPart_statusFlags_3,     'GenPart_statusFlags_3/I')
        self.t.Branch('GenPart_statusFlags_4',     self.GenPart_statusFlags_4,     'GenPart_statusFlags_4/I')
        self.t.Branch('GenPart_status_1',     self.GenPart_status_1,     'GenPart_status_1/I')
        self.t.Branch('GenPart_status_2',     self.GenPart_status_2,     'GenPart_status_2/I')
        self.t.Branch('GenPart_status_3',     self.GenPart_status_3,     'GenPart_status_3/I')
        self.t.Branch('GenPart_status_4',     self.GenPart_status_4,     'GenPart_status_4/I')
        self.t.Branch('pt_3',        self.pt_3,        'pt_3/F')
        self.t.Branch('pt_3_tr',     self.pt_3_tr,     'pt_3_tr/F')
        self.t.Branch('phi_3',       self.phi_3,       'phi_3/F')
        self.t.Branch('phi_3_tr',    self.phi_3_tr,    'phi_3_tr/F')
        self.t.Branch('eta_3',       self.eta_3,       'eta_3/F')
        self.t.Branch('eta_3_tr',    self.eta_3_tr,    'eta_3_tr/F')
        self.t.Branch('m_3',         self.m_3,         'm_3/F')
        self.t.Branch('q_3',         self.q_3,         'q_3/F')
        self.t.Branch('d0_3',        self.d0_3,        'd0_3/F')
        self.t.Branch('dZ_3',        self.dZ_3,        'dZ_3/F')
        self.t.Branch('mt_3',        self.mt_3,        'mt_3/F')
        self.t.Branch('pfmt_3',      self.pfmt_3,      'pfmt_3/F')
        self.t.Branch('puppimt_3',   self.puppimt_3,   'puppimt_3/F')
        self.t.Branch('iso_3',       self.iso_3,       'iso_3/F')
        self.t.Branch('Electron_mvaFall17V2noIso_WP90_1', self.Electron_mvaFall17V2noIso_WP90_1, 'Electron_mvaFall17V2noIso_WP90_1/F')
        self.t.Branch('Electron_mvaFall17V2noIso_WP90_2', self.Electron_mvaFall17V2noIso_WP90_2, 'Electron_mvaFall17V2noIso_WP90_2/F')
        self.t.Branch('Electron_mvaFall17V2noIso_WP90_3', self.Electron_mvaFall17V2noIso_WP90_3, 'Electron_mvaFall17V2noIso_WP90_3/F')
        self.t.Branch('Electron_mvaFall17V2noIso_WP90_4', self.Electron_mvaFall17V2noIso_WP90_4, 'Electron_mvaFall17V2noIso_WP90_4/F')
        self.t.Branch('gen_match_1', self.gen_match_1, 'gen_match_1/l')
        self.t.Branch('gen_match_2', self.gen_match_2, 'gen_match_2/l')
        self.t.Branch('gen_match_3', self.gen_match_3, 'gen_match_3/l')
        self.t.Branch('tightId_3', self.tightId_3, 'tightId_3/F')
        self.t.Branch('mediumId_3', self.mediumId_3, 'mediumId_3/F')
        self.t.Branch('mediumPromptId_3', self.mediumPromptId_3, 'mediumPromptId_3/F')
        self.t.Branch('looseId_3', self.looseId_3, 'looseId_3/F')
        self.t.Branch('isGlobal_3', self.isGlobal_3, 'isGlobal_3/F')
        self.t.Branch('isTracker_3', self.isTracker_3, 'isTracker_3/F')
        self.t.Branch('ip3d_3', self.ip3d_3, 'ip3d_3/F')
        self.t.Branch('inTimeMuon_3', self.inTimeMuon_3, 'inTimeMuon_3/F')


        self.t.Branch('idDecayModeNewDMs_3', self.idDecayModeNewDMs_3, 'idDecayModeNewDMs_3/F')
        self.t.Branch('idDeepTau2017v2p1VSe_3', self.idDeepTau2017v2p1VSe_3, 'idDeepTau2017v2p1VSe_3/F')
        self.t.Branch('idDeepTau2017v2p1VSjet_3', self.idDeepTau2017v2p1VSjet_3, 'idDeepTau2017v2p1VSjet_3/F')
        self.t.Branch('idDeepTau2017v2p1VSmu_3', self.idDeepTau2017v2p1VSmu_3, 'idDeepTau2017v2p1VSmu_3/F')
        self.t.Branch('idMVAnewDM2017v2_3', self.idMVAnewDM2017v2_3, 'idMVAnewDM2017v2_3/F')
        self.t.Branch('rawMVAnewDM2017v2_3', self.rawMVAnewDM2017v2_3, 'rawMVAnewDM2017v2_3/F')

        self.t.Branch('trigweight_3',  self.trigweight_3,  'trigweight_3/F')
        self.t.Branch('idisoweight_3', self.idisoweight_3, 'idisoweight_3/F')
        self.t.Branch('decayMode_3',   self.decayMode_3,   'decayMode_3/I')

        self.t.Branch('pt_4',        self.pt_4,        'pt_4/F')
        self.t.Branch('pt_4_tr',     self.pt_4_tr,        'pt_4_tr/F')
        self.t.Branch('phi_4',       self.phi_4,       'phi_4/F')
        self.t.Branch('phi_4_tr',    self.phi_4_tr,    'phi_4_tr/F')
        self.t.Branch('eta_4',       self.eta_4,       'eta_4/F')
        self.t.Branch('eta_4_tr',    self.eta_4_tr,    'eta_4_tr/F')
        self.t.Branch('m_4',         self.m_4,         'm_4/F')
        self.t.Branch('q_4',         self.q_4,         'q_4/F')
        self.t.Branch('d0_4',        self.d0_4,        'd0_4/F')
        self.t.Branch('dZ_4',        self.dZ_4,        'dZ_4/F')
        self.t.Branch('mt_4',        self.mt_4,        'mt_4/F')
        self.t.Branch('pfmt_4',      self.pfmt_4,      'pfmt_4/F')
        self.t.Branch('puppimt_4',   self.puppimt_4,   'puppimt_4/F')
        self.t.Branch('iso_4',       self.iso_4,       'iso_4/F')
        self.t.Branch('gen_match_4', self.gen_match_4, 'gen_match_4/l')
        self.t.Branch('tightId_4', self.tightId_4, 'tightId_4/F')
        self.t.Branch('mediumId_4', self.mediumId_4, 'mediumId_4/F')
        self.t.Branch('mediumPromptId_4', self.mediumPromptId_4, 'mediumPromptId_4/F')
        self.t.Branch('looseId_4', self.looseId_4, 'looseId_4/F')
        self.t.Branch('isGlobal_4', self.isGlobal_4, 'isGlobal_4/F')
        self.t.Branch('isTracker_4', self.isTracker_4, 'isTracker_4/F')
        self.t.Branch('ip3d_4', self.ip3d_4, 'ip3d_4/F')
        self.t.Branch('inTimeMuon_4', self.inTimeMuon_4, 'inTimeMuon_4/F')


        self.t.Branch('idDecayModeNewDMs_4', self.idDecayModeNewDMs_4, 'idDecayModeNewDMs_4/F')
        self.t.Branch('idDeepTau2017v2p1VSe_4', self.idDeepTau2017v2p1VSe_4, 'idDeepTau2017v2p1VSe_4/F')
        self.t.Branch('idDeepTau2017v2p1VSjet_4', self.idDeepTau2017v2p1VSjet_4, 'idDeepTau2017v2p1VSjet_4/F')
        self.t.Branch('idDeepTau2017v2p1VSmu_4', self.idDeepTau2017v2p1VSmu_4, 'idDeepTau2017v2p1VSmu_4/F')
        self.t.Branch('idMVAnewDM2017v2_4', self.idMVAnewDM2017v2_4, 'idMVAnewDM2017v2_4/F')
        self.t.Branch('rawMVAnewDM2017v2_4', self.rawMVAnewDM2017v2_4, 'rawMVAnewDM2017v2_4/F')

        self.t.Branch('trigweight_4',  self.trigweight_4,  'trigweight_4/F')
        self.t.Branch('idisoweight_4', self.idisoweight_4, 'idisoweight_4/F')
        self.t.Branch('decayMode_4',   self.decayMode_4,   'decayMode_4/I')


        self.t.Branch('pt_5',        self.pt_5,        'pt_5/F')
        self.t.Branch('phi_5',       self.phi_5,       'phi_5/F')
        self.t.Branch('eta_5',       self.eta_5,       'eta_5/F')
        self.t.Branch('m_5',         self.m_5,         'm_5/F')
        self.t.Branch('q_5',         self.q_5,         'q_5/F')
        self.t.Branch('dZ_5',        self.dZ_5,        'dZ_5/F')
        self.t.Branch('d0_5',        self.d0_5,        'd0_5/F')
        self.t.Branch('gen_match_5', self.gen_match_5, 'gen_match_5/l')
        self.t.Branch('decayMode_5',   self.decayMode_5,   'decayMode_5/I')


        self.t.Branch('idDecayModeNewDMs_5', self.idDecayModeNewDMs_5, 'idDecayModeNewDMs_5/F')
        self.t.Branch('idDeepTau2017v2p1VSe_5', self.idDeepTau2017v2p1VSe_5, 'idDeepTau2017v2p1VSe_5/F')
        self.t.Branch('idDeepTau2017v2p1VSjet_5', self.idDeepTau2017v2p1VSjet_5, 'idDeepTau2017v2p1VSjet_5/F')
        self.t.Branch('idDeepTau2017v2p1VSmu_5', self.idDeepTau2017v2p1VSmu_5, 'idDeepTau2017v2p1VSmu_5/F')
        self.t.Branch('idMVAnewDM2017v2_5', self.idMVAnewDM2017v2_5, 'idMVAnewDM2017v2_5/F')
        self.t.Branch('rawMVAnewDM2017v2_5', self.rawMVAnewDM2017v2_5, 'rawMVAnewDM2017v2_5/F')




        # di-tau variables
        self.t.Branch('pt_tt', self.pt_tt, 'pt_tt/F')
        self.t.Branch('mt_tot', self.mt_tot, 'mt_tot/F')
        self.t.Branch('m_vis', self.m_vis, 'm_vis/F')
        self.t.Branch('m_sv', self.m_sv, 'm_sv/F')
        self.t.Branch('mt_sv', self.mt_sv, 'mt_sv/F') 
        self.t.Branch('H_DR', self.H_DR, 'H_DR/F')
        self.t.Branch('AMass', self.AMass, 'AMass/F')

        # di-lepton variables. 
        self.t.Branch('H_LT',         self.H_LT,         'H_LT/F')   
        self.t.Branch('dRl1H',         self.dRl1H,         'dRl1H/F')   
        self.t.Branch('dRl2H',         self.dRl2H,         'dRl2H/F')   
        self.t.Branch('dRlH',         self.dRlH,         'dRlH/F')   
        self.t.Branch('dPhil1H',         self.dPhil1H,         'dPhil1H/F')   
        self.t.Branch('dPhil2H',         self.dPhil2H,         'dPhil2H/F')   
        self.t.Branch('dPhilH',         self.dPhilH,         'dPhilH/F')   

        self.t.Branch('mll',         self.mll,         'mll/F')   
        self.t.Branch('mll2',         self.mll2,         'mll2/F')   
        self.t.Branch('Z_Pt',       self.Z_Pt,       'Z_Pt/F')   
        self.t.Branch('Z_DR',       self.Z_DR,       'Z_DR/F')   
        self.t.Branch('Z_SS',       self.Z_SS,       'Z_SS/F')   
        self.t.Branch('pt_1',        self.pt_1,        'pt_1/F')
        self.t.Branch('m_1_tr',     self.m_1_tr,     'm_1_tr/F')
        self.t.Branch('pt_1_tr',     self.pt_1_tr,     'pt_1_tr/F')
        self.t.Branch('phi_1',       self.phi_1,       'phi_1/F')  
        self.t.Branch('phi_1_tr',    self.phi_1_tr,    'phi_1_tr/F')
        self.t.Branch('eta_1',       self.eta_1,       'eta_1/F')    
        self.t.Branch('eta_1_tr',    self.eta_1_tr,    'eta_1_tr/F')
        self.t.Branch('pt_2',        self.pt_2,        'pt_2/F')      
        self.t.Branch('m_2_tr',     self.m_2_tr,     'm_2_tr/F')
        self.t.Branch('pt_2_tr',     self.pt_2_tr,     'pt_2_tr/F')
        self.t.Branch('phi_2',       self.phi_2,       'phi_2/F')    
        self.t.Branch('phi_2_tr',    self.phi_2_tr,    'phi_2_tr/F')
        self.t.Branch('eta_2',       self.eta_2,       'eta_2/F')      
        self.t.Branch('eta_2_tr',    self.eta_2_tr,    'eta_2_tr/F')
        self.t.Branch('iso_1',       self.iso_1,       'iso_1/F')
        self.t.Branch('iso_2',       self.iso_2,       'iso_2/F')
        self.t.Branch('q_1',       self.q_1,       'q_1/F')
        self.t.Branch('q_2',       self.q_2,       'q_2/F')
        self.t.Branch('d0_1',        self.d0_1,        'd0_1/F')
        self.t.Branch('dZ_1',        self.dZ_1,        'dZ_1/F')
        self.t.Branch('d0_2',        self.d0_2,        'd0_2/F')
        self.t.Branch('dZ_2',        self.dZ_2,        'dZ_2/F')
        self.t.Branch('Muon_Id_1',       self.Muon_Id_1,       'Muon_Id_1/F')
        self.t.Branch('Muon_Id_2',       self.Muon_Id_2,       'Muon_Id_2/F')
        self.t.Branch('isGlobal_1',       self.isGlobal_1,       'isGlobal_1/F')
        self.t.Branch('isGlobal_2',       self.isGlobal_2,       'isGlobal_2/F')
        self.t.Branch('isTracker_1',       self.isTracker_1,       'isTracker_1/F')
        self.t.Branch('isTracker_2',       self.isTracker_2,       'isTracker_2/F')
        self.t.Branch('tightId_1', self.tightId_1, 'tightId_1/F')
        self.t.Branch('mediumId_1', self.mediumId_1, 'mediumId_1/F')
        self.t.Branch('mediumPromptId_1', self.mediumPromptId_1, 'mediumPromptId_1/F')
        self.t.Branch('looseId_1', self.looseId_1, 'looseId_1/F')
        self.t.Branch('tightId_2', self.tightId_2, 'tightId_2/F')
        self.t.Branch('mediumId_2', self.mediumId_2, 'mediumId_2/F')
        self.t.Branch('mediumPromptId_2', self.mediumPromptId_2, 'mediumPromptId_2/F')
        self.t.Branch('looseId_2', self.looseId_2, 'looseId_2/F')

        #systematics
        self.t.Branch('metpt_nom', self.metpt_nom, 'metpt_nom/F')
        self.t.Branch('metphi_nom', self.metphi_nom, 'metphi_nom/F')
        self.t.Branch('metpt_JER', self.metpt_JER, 'metpt_JER/F')
        self.t.Branch('metphi_JER', self.metphi_JER, 'metphi_JER/F')
        self.t.Branch('metpt_JERUp', self.metpt_JERUp, 'metpt_JERUp/F')
        self.t.Branch('metphi_JERUp', self.metphi_JERUp, 'metphi_JERUp/F')
        self.t.Branch('metpt_JERDown', self.metpt_JERDown, 'metpt_JERDown/F')
        self.t.Branch('metphi_JERDown', self.metphi_JERDown, 'metphi_JERDown/F')
        self.t.Branch('metpt_JESUp', self.metpt_JESUp, 'metpt_JESUp/F')
        self.t.Branch('metphi_JESUp', self.metphi_JESUp, 'metphi_JESUp/F')
        self.t.Branch('metpt_JESDown', self.metpt_JESDown, 'metpt_JESDown/F')
        self.t.Branch('metphi_JESDown', self.metphi_JESDown, 'metphi_JESDown/F')
        self.t.Branch('metpt_UnclUp', self.metpt_UnclUp, 'metpt_UnclUp/F')
        self.t.Branch('metphi_UnclUp', self.metphi_UnclUp, 'metphi_UnclUp/F')
        self.t.Branch('metpt_UnclDown', self.metpt_UnclDown, 'metpt_UnclDown/F')
        self.t.Branch('metphi_UnclDown', self.metphi_UnclDown, 'metphi_UnclDown/F')
        self.t.Branch('met_UnclX', self.met_UnclX, 'met_UnclX/F')
        self.t.Branch('met_UnclY', self.met_UnclY, 'met_UnclY/F')
        
        # MET variables
        self.t.Branch('met', self.met, 'met/F')
        self.t.Branch('metphi', self.metphi, 'metphi/F')
        self.t.Branch('puppimet', self.puppimet, 'puppimet/F')
        self.t.Branch('puppimetphi', self.puppimetphi, 'puppimetphi/F')
        self.t.Branch('metcov00', self.metcov00, 'metcov00/F')
        self.t.Branch('metcov01', self.metcov01, 'metcov01/F')
        self.t.Branch('metcov10', self.metcov10, 'metcov10/F')
        self.t.Branch('metcov11', self.metcov11, 'metcov11/F')

        # trigger sf
        self.t.Branch('isTrig_2',  self.isTrig_2, 'isTrig_2/F' )
        self.t.Branch('isTrig_1',  self.isTrig_1, 'isTrig_1/F' )
        self.t.Branch('isDoubleTrig',  self.isDoubleTrig, 'isDoubleTrig/F' )


        # jet variables
        #self.t.Branch('njetsold', self.njetsold, 'njetsold[8]/F') 
        #self.t.Branch('nbtagold', self.nbtagold, 'nbtagold[8]/F')
        self.t.Branch('njets', self.njets, 'njets[8]/F')
        self.t.Branch('nbtag', self.nbtag, 'nbtag[8]/F')
        self.t.Branch('nbtagT', self.nbtagT, 'nbtagT[8]/F')


        self.t.Branch('jpt_1',     self.jpt_1,     'jpt_1[8]/F' )
        self.t.Branch('jpt_2',     self.jpt_2,     'jpt_2[8]/F' )

        self.t.Branch('jpt_1_tr',  self.jpt_1_tr,  'jpt_1_tr[8]/F' )
        self.t.Branch('jeta_1',    self.jeta_1,    'jeta_1[8]/F' ) 
        self.t.Branch('jeta_1_tr', self.jeta_1_tr, 'jeta_1_tr[8]/F' )
        self.t.Branch('jphi_1',    self.jphi_1,    'jphi_1[8]/F' )
        self.t.Branch('jphi_1_tr', self.jphi_1_tr, 'jphi_1_tr[8]/F' )
        self.t.Branch('jcsv_1',    self.jcsv_1,    'jcsv_1[8]/F' )
        self.t.Branch('jcsvfv_1', self.jcsvfv_1, 'jcsvfv_1[8]/F' )
        self.t.Branch('jpt_2',     self.jpt_2,     'jpt_2[8]/F' )
        self.t.Branch('jpt_2_tr',  self.jpt_2_tr,  'jpt_2_tr[8]/F' )
        self.t.Branch('jeta_2',    self.jeta_2,    'jeta_2[8]/F' ) 
        self.t.Branch('jeta_2_tr', self.jeta_2_tr, 'jeta_2_tr[8]/F' )
        self.t.Branch('jphi_2',    self.jphi_2,    'jphi_2[8]/F' )
        self.t.Branch('jphi_2_tr', self.jphi_2_tr, 'jphi_2_tr[8]/F' )
        self.t.Branch('jcsv_2',    self.jcsv_2,    'jcsv_2[8]/F' )
        self.t.Branch('jcsvfv_2', self.jcsvfv_2, 'jcsvfv_2[8]/F' )

        self.t.Branch('bpt_1',     self.bpt_1,     'bpt_1[8]/F' )
        self.t.Branch('bpt_1_tr',  self.bpt_1_tr,  'bpt_1_tr[8]/F' )
        self.t.Branch('beta_1',    self.beta_1,    'beta_1[8]/F' ) 
        self.t.Branch('beta_1_tr', self.beta_1_tr, 'beta_1_tr[8]/F' )
        self.t.Branch('bphi_1',    self.bphi_1,    'bphi_1[8]/F' )
        self.t.Branch('bphi_1_tr', self.bphi_1_tr, 'bphi_1_tr[8]/F' )
        self.t.Branch('bcsv_1',    self.bcsv_1,    'bcsv_1[8]/F' )
        self.t.Branch('bcsvfv_1', self.bcsvfv_1, 'bcsvfv_1[8]/F' )
        self.t.Branch('bpt_2',     self.bpt_2,     'bpt_2[8]/F' )
        self.t.Branch('bpt_2_tr',  self.bpt_2_tr,  'bpt_2_tr[8]/F' )
        self.t.Branch('beta_2',    self.beta_2,    'beta_2[8]/F' )
        self.t.Branch('beta_2_tr', self.beta_2_tr, 'beta_2_tr[8]/F' )
        self.t.Branch('bphi_2',    self.bphi_2,    'bphi_2[8]/F' )
        self.t.Branch('bphi_2_tr', self.bphi_2_tr, 'bphi_2_tr[8]/F' )
        self.t.Branch('bcsv_2',    self.bcsv_2,    'bcsv_2[8]/F' )
        self.t.Branch('bcsvfv_2', self.bcsvfv_2, 'bcsvfv_2[8]/F' )

    def get_mt(self,METtype,entry,tau) :
        if METtype == 'MVAMet' :
            # temporary choice 
            dphi = tau.Phi() - entry.MET_phi
            return sqrt(2.*tau.Pt()*entry.MET_pt*(1. - cos(dphi)))
        elif METtype == 'PFMet' :
            dphi = tau.Phi() - entry.MET_phi
            return sqrt(2.*tau.Pt()*entry.MET_pt*(1. - cos(dphi)))
        elif METtype == 'PUPPIMet' :
            dphi = tau.Phi() - entry.PuppiMET_phi
            return sqrt(2.*tau.Pt()*entry.PuppiMET_pt*(1. - cos(dphi)))
        else :
            print("Invalid METtype={0:s} in outTuple.get_mt().   Exiting".format(METtype))

    def getPt_tt(self,entry,tau1,tau2) :
        ptMiss = TLorentzVector() 
        ptMiss.SetPtEtaPhiM(entry.MET_pt,0.,entry.MET_phi,0.)
        return (tau1+tau2+ptMiss).Pt()

    def getMt_tot(self,entry,tau1,tau2) :
        pt1, pt2, met = tau1.Pt(), tau2.Pt(), entry.MET_pt
        phi1, phi2, metphi = tau1.Phi(), tau2.Phi(), entry.MET_phi
        arg = 2.*(pt1*met*(1. - cos(phi1-metphi)) + pt2*met*(1. - cos(phi2-metphi)) + pt1*pt2*(1. - cos(phi2-phi1)))
        return sqrt(arg)

    def getDR(self,entry, v1,v2) :

        dPhi = min(abs(v2.Phi()-v1.Phi()),2.*pi-abs(v2.Phi()-v1.Phi()))
        DR = sqrt(dPhi**2 + (v2.Eta()-v1.Eta())**2)
	return DR

    def getDRnV(self,entry, eta1,phi1, eta2,phi2) :

        dPhi = min(abs(phi2-phi1),2.*pi-abs(phi2-phi1))
        DR = sqrt(dPhi**2 + (eta2-eta1)**2)
	return DR

    def getdPhi(self, entry, v1,v2) :
        dPhi = min(abs(v2.Phi()-v1.Phi()),2.*pi-abs(v2.Phi()-v1.Phi()))
        return dPhi

    def getM_vis(self,entry,tau1,tau2) :
        return (tau1+tau2).M()

    def getJets(self,entry,tau1,tau2,era) :
	nJet30, jetList, bJetList, bJetListFlav = 0, [], [], []
        phi2_1, eta2_1 = tau1.Phi(), tau1.Eta() 
        phi2_2, eta2_2 = tau2.Phi(), tau2.Eta() 
	bjet_discr = 0.6321
	bjet_discrFlav = 0.0614
	if str(era) == 2017 : bjet_discr = 0.4941
	if str(era) == 2018 : bjet_discr = 0.4184

        for j in range(entry.nJet) :
            if entry.Jet_jetId[j]  < 2  : continue  #require tigh jets
            if entry.Jet_pt[j]>20 and entry.Jet_pt[j] < 50 and entry.Jet_puId[j]  < 4  : continue #loose jetPU_iD
            if str(era) == '2017'  and entry.Jet_pt[j] > 20 and entry.Jet_pt[j] < 50 and abs(entry.Jet_eta[j]) > 2.65 and abs(entry.Jet_eta[j]) < 3.139 : continue  #remove noisy jets
            if entry.Jet_pt[j] < 20. : continue
            if abs(entry.Jet_eta[j]) > 4.7 : continue
            phi1, eta1 = entry.Jet_phi[j], entry.Jet_eta[j]
            dPhi = min(abs(phi2_1-phi1),2.*pi-abs(phi2_1-phi1))
            DR = sqrt(dPhi**2 + (eta2_1-eta1)**2)
            dPhi = min(abs(phi2_2-phi1),2.*pi-abs(phi2_2-phi1))
            DR = min(DR,sqrt(dPhi**2 + (eta2_2-eta1)**2))
            if DR < 0.5 : continue
            if entry.Jet_pt[j] > 30 :
		if abs(entry.Jet_eta[j]) < 2.4 and entry.Jet_btagDeepB[j] > bjet_discr : bJetList.append(j)
		if abs(entry.Jet_eta[j]) < 2.4 and entry.Jet_btagDeepFlavB[j] > bjet_discrFlav : bJetListFlav.append(j)
                jetList.append(j) 

        return jetList, bJetList,bJetListFlav



    def getJetsJMEMV(self,entry,LepList,era, syst) :
	jetList, bJetList, bJetListT, bJetListFlav = [], [], [], []
	#print 'will try', len(LepList)
	bjet_discr = 0.6321
	bjet_discrT = 0.8953
	bjet_discrFlav = 0.0614

	if str(era) == '2017' : 
	    bjet_discr = 0.4941
	    bjet_discrT = 0.8001
	if str(era) == '2018' : 
	    bjet_discr = 0.4184
	    bjet_discrT = 0.7527

	failJets=[]
        goodJets=[]
        jeList=[]
        bJetList=[]
        if syst !='' : syst="_"+syst
        for j in range(entry.nJet) :
            jpt = getattr(entry, "Jet_pt{0:s}".format(str(syst)), None)

            #print jpt[j],  entry.Jet_pt[j],  syst

            if entry.Jet_jetId[j]  < 2  : continue  #require tight jets
            if jpt[j] > 30 and jpt[j] < 50 and entry.Jet_puId[j]  < 4  : continue #loose jetPU_iD
            if str(era) == '2017'  and jpt[j] > 20 and jpt[j] < 50 and abs(entry.Jet_eta[j]) > 2.65 and abs(entry.Jet_eta[j]) < 3.139 : continue  #remove noisy jets
            if jpt[j] < 25. : continue
            if abs(entry.Jet_eta[j]) > 4.7 : continue

            #for iv, lepv in enumerate(LepList) : 
            for iv, lv  in  enumerate(LepList) :
		dr = self.getDRnV(entry, entry.Jet_eta[j], entry.Jet_phi[j], LepList[iv].Eta(), LepList[iv].Phi())
                if float(dr) > 0.5 : 
                    #print 'seems goodfor iv--->', iv, 'jet', j, entry.nJet, 'dr--', dr , LepList[iv].Eta(), LepList[iv].Phi(), LepList[iv].Pt()
                    if j not in goodJets : goodJets.append(j)
		if float(dr) < 0.5 : 
                    #print ' failed for lepton--->', iv, 'jet', j, 'njets', entry.nJet, 'dr--', dr , LepList[iv].Eta(), LepList[iv].Phi(), LepList[iv].Pt()
                    if j not in failJets : failJets.append(j)
                    #continue


        #print 'some info', goodJets, failJets
        for j in failJets : 
            if j in goodJets : goodJets.remove(j)


        for jj in goodJets : 
            
            if jpt[jj] > 25 : 
                #print 'will check now', jj, goodJets, entry.Jet_btagDeepB[jj], bjet_discr, jpt[jj], entry.Jet_btagDeepB[jj],  entry.Jet_pt[jj]
		if abs(entry.Jet_eta[jj]) < 2.4 and entry.Jet_btagDeepB[jj] > bjet_discr : bJetList.append(jj)
		if abs(entry.Jet_eta[jj]) < 2.4 and entry.Jet_btagDeepB[jj] > bjet_discrT : bJetListT.append(jj)
		if abs(entry.Jet_eta[jj]) < 2.4 and entry.Jet_btagDeepFlavB[jj] > bjet_discrFlav : bJetListFlav.append(jj)

                jetList.append(jj) 

        return jetList, bJetList,bJetListT,bJetListFlav



    def runSVFit(self, entry, channel, jt1, jt2, tau1, tau2 ) :
                      
        measuredMETx = entry.MET_pt*cos(entry.MET_phi)
        measuredMETy = entry.MET_pt*sin(entry.MET_phi)

        #define MET covariance
        covMET = ROOT.TMatrixD(2,2)
        covMET[0][0] = entry.MET_covXX
        covMET[1][0] = entry.MET_covXY
        covMET[0][1] = entry.MET_covXY
        covMET[1][1] = entry.MET_covYY
        #covMET[0][0] = 787.352
        #covMET[1][0] = -178.63
        #covMET[0][1] = -178.63
        #covMET[1][1] = 179.545

        #self.kUndefinedDecayType, self.kTauToHadDecay,  self.kTauToElecDecay, self.kTauToMuDecay = 0, 1, 2, 3

        if channel == 'et' :
            measTau1 = ROOT.MeasuredTauLepton(self.kTauToElecDecay, tau1.Pt(), tau1.Eta(), tau1.Phi(), 0.000511) 
        elif channel == 'mt' :
            measTau1 = ROOT.MeasuredTauLepton(self.kTauToMuDecay, tau1.Pt(), tau1.Eta(), tau1.Phi(), 0.106) 
        elif channel == 'tt' :
            measTau1 = ROOT.MeasuredTauLepton(self.kTauToHadDecay, tau1.Pt(), tau1.Eta(), tau1.Phi(), entry.Tau_mass[jt1])
                        
	if channel != 'em' :
            measTau2 = ROOT.MeasuredTauLepton(self.kTauToHadDecay, tau2.Pt(), tau2.Eta(), tau2.Phi(), entry.Tau_mass[jt2])

	if channel == 'em' :
            measTau1 = ROOT.MeasuredTauLepton(self.kTauToElecDecay, tau1.Pt(), tau1.Eta(), tau1.Phi(), 0.000511)
            measTau2 = ROOT.MeasuredTauLepton(self.kTauToMuDecay, tau2.Pt(), tau2.Eta(), tau2.Phi(), 0.106)

        VectorOfTaus = ROOT.std.vector('MeasuredTauLepton')
        instance = VectorOfTaus()
        instance.push_back(measTau1)
        instance.push_back(measTau2)

        FMTT = ROOT.FastMTT()
        FMTT.run(instance, measuredMETx, measuredMETy, covMET)
        ttP4 = FMTT.getBestP4()
        return ttP4.M(), ttP4.Mt() 
    
    def Fill(self, entry, SVFit, cat, jt1, jt2, LepP, LepM, lepList, isMC, era, doUncertainties=False , sysVariations=[]) :
        ''' - jt1 and jt2 point to the selected tau candidates according to the table below.
            - if e.g., channel = 'et', the jt1 points to the electron list and jt2 points to the tau list.
            - LepP and LepM are TLorentz vectors for the positive and negative members of the dilepton pair
        '''

        is_trig_1, is_trig_2, is_Dtrig_1 = 0., 0., 0.
        TrigListLep = []
        TrigListTau = []
        hltListLep  = []

        #channel_ll = 'mm' or 'ee'
        channel_ll = cat[:-2]

	TrigListLep, hltListLep  = GF.findSingleLeptTrigger(lepList, entry, channel_ll, era)

	TrigListLep = list(dict.fromkeys(TrigListLep))


	TrigListLepD, hltListLepD  = GF.findDoubleLeptTrigger(lepList, entry, channel_ll, era)

	TrigListLepD = list(dict.fromkeys(TrigListLepD))

	#if len(TrigListLepD) > 0 : print TrigListLepD, hltListLepD, TrigListLep, hltListLep
	if len(TrigListLepD) == 2 : 
	    if lepList[0] == TrigListLepD[0] :
	        is_Dtrig_1 = 1 #that means that the leading lepton 
	    else : 
	        is_Dtrig_1 = -1


        if len(TrigListLep) == 1 :

	    if lepList[0] == TrigListLep[0] :
	        is_trig_1 = 1.
	    else:
	        is_trig_1 = -1. #that means that the subleading fired the trigger


        if len(TrigListLep) == 2 :
            if 'BothLept' in hltListLep :
	        is_trig_1 = 1.
	        is_trig_2 = 1.


        #if len(TrigListLep) ==1 : print 'TrigerList ===========>', TrigListLep, lepList, hltListLep, channel_ll, 'istrig_1', is_trig_1, 'istrig_2', is_trig_2, 'lenTrigList', len(TrigListLep),  'lenLept', len(lepList), 'lepList_0', lepList[0], 'TrigList_0', TrigListLep[0], hltListLep
        

        # channel = 'mt', 'et', 'tt', or 'em'
        channel = cat[-2:]
        if jt1 > -1 and jt2 > -1 : self.cat[0]  = tauFun.catToNumber(cat)
        
        self.entries += 1

        self.run[0]  = entry.run
        self.nElectron[0]  = entry.nElectron
        self.nMuon[0]  = entry.nMuon
        self.nTau[0]  = entry.nTau
        self.lumi[0] = entry.luminosityBlock 
        self.evt[0]  = entry.event
        self.iso_1[0]  = -99
        self.iso_2[0]  = -99
        self.q_1[0]  = -99
        self.q_2[0]  = -99
        self.isGlobal_1[0]  = -99
        self.isGlobal_2[0]  = -99


        self.tightId_1[0]       = -1 
        self.mediumId_1[0]       = -1 
        self.mediumPromptId_1[0]   = -1
        self.looseId_1[0]       = -1
        self.isGlobal_1[0]      = -1
        self.isTracker_1[0]     = -1

        self.tightId_2[0]       = -1 
        self.mediumId_2[0]       = -1 
        self.mediumPromptId_2[0]   = -1
        self.looseId_2[0]       = -1
        self.isGlobal_2[0]      = -1
        self.isTracker_2[0]     = -1

        self.decayMode_3[0]        = -1
        self.idDecayModeNewDMs_3[0]= -1
        self.idDeepTau2017v2p1VSe_3[0] = -1
        self.idDeepTau2017v2p1VSjet_3[0] = -1
        self.idDeepTau2017v2p1VSmu_3[0] = -1
        self.idMVAnewDM2017v2_3[0] = -1
        self.rawMVAnewDM2017v2_3[0] = -1
        self.mediumId_3[0]       = -1 
        self.mediumPromptId_3[0]   = -1
        self.looseId_3[0]       = -1
        self.isGlobal_3[0]      = -1
        self.isTracker_3[0]     = -1
        self.ip3d_3[0]          = -1
        self.inTimeMuon_3[0]    = -1

        self.decayMode_4[0]      = -1
        self.idDecayModeNewDMs_4[0] = -1
        self.idDeepTau2017v2p1VSe_4[0] = -1
        self.idDeepTau2017v2p1VSjet_4[0] = -1
        self.idDeepTau2017v2p1VSmu_4[0] = -1
        self.idMVAnewDM2017v2_4[0] = -1
        self.rawMVAnewDM2017v2_4[0] = -1
        self.mediumId_4[0]       = -1 
        self.mediumPromptId_4[0]   = -1
        self.looseId_4[0]       = -1
        self.isGlobal_4[0]      = -1
        self.isTracker_4[0]     = -1
        self.ip3d_4[0]          = -1
        self.inTimeMuon_4[0]    = -1
	self.GenPart_statusFlags_1[0]    = -1
	self.GenPart_status_1[0]    = -1
	self.GenPart_statusFlags_2[0]    = -1
	self.GenPart_status_2[0]    = -1
	self.GenPart_statusFlags_3[0]    = -1
	self.GenPart_status_3[0]    = -1
	self.GenPart_statusFlags_4[0]    = -1
	self.GenPart_status_4[0]    = -1
        self.gen_match_1[0] = -1
        self.gen_match_2[0] = -1
        self.gen_match_3[0] = -1
        self.gen_match_4[0] = -1
        self.gen_match_5[0] = -1

        goodElectronList = tauFun.makeGoodElectronList(entry)
        goodMuonList = tauFun.makeGoodMuonList(entry)
        
        self.nGoodElectron[0] = len(goodElectronList)
        self.nGoodMuon[0]     = len(goodMuonList)
        

        try :
            self.weight[0]           = entry.genWeight
            self.LHEweight[0]        = entry.LHEWeight_originalXWGTUP
            self.Generator_weight[0] = entry.Generator_weight
            self.LHE_Njets[0]        = ord(entry.LHE_Njets) 
	    self.nPU[0]  = entry.Pileup_nPU
	    self.nPUEOOT[0]  = entry.Pileup_sumEOOT
	    self.nPULOOT[0]  = entry.Pileup_sumLOOT
	    self.nPUtrue[0]  = entry.Pileup_nTrueInt
	    self.nPV[0]  = entry.PV_npvs
	    self.nPVGood[0]  = entry.PV_npvsGood
                        
        except AttributeError :
            self.weight[0]           = 1. 
            self.weightPU[0]         = -1
            self.weightPUtrue[0]     = -1
            self.LHEweight[0]        = 1. 
            self.Generator_weight[0] = 1.
            self.LHE_Njets[0] = -1
	    self.nPU[0]  = -1
	    self.nPUEOOT[0]  = -1
	    self.nPULOOT[0]  = -1
	    self.nPUtrue[0]  = -1
	    self.nPV[0]  = -1
	    self.nPVGood[0]  = -1

        # pack trigger bits into integer word

        e = entry
	bits=[]

        try : bits.append(e.HLT_Ele35_WPTight_Gsf)
        except AttributeError : bits.append(False)
        try : bits.append(e.HLT_Ele32_WPTight_Gsf)
        except AttributeError : bits.append(False)
        try : bits.append(e.HLT_Ele27_eta2p1_WPTight_Gsf)
        except AttributeError : bits.append(False) 
        try : bits.append(e.HLT_Ele25_eta2p1_WPTight_Gsf)
        except AttributeError : bits.append(False)

        try : bits.append(e.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL)
        except AttributeError : bits.append(False)
        try : bits.append(e.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ)
        except AttributeError : bits.append(False) 

        self.electronTriggerWord[0] = 0
        for i, bit in enumerate(bits) :
            if bit : self.electronTriggerWord[0] += 2**i

        bits=[]
        try : bits.append(e.HLT_IsoMu27)
        except AttributeError : bits.append(False) 
        try : bits.append(e.HLT_IsoMu24)
        except AttributeError : bits.append(False) 
        try : bits.append(e.HLT_IsoTkMu24)
        except AttributeError : bits.append(False)
        for i in range(5) : bits.append(False)         # pad rest of this byte 
        
        try : bits.append(e.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ)
        except AttributeError : bits.append(False) 
        try : bits.append(e.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8)
        except AttributeError : bits.append(False)
        try : bits.append(e.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8)
        except AttributeError : bits.append(False)
        try : bits.append(e.HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ)
        except AttributeError : bits.append(False) 
        try : bits.append(e.HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_Mass8)
        except AttributeError : bits.append(False) 

        self.muonTriggerWord[0] = 0
        for i, bit in enumerate(bits) :
            if bit : self.muonTriggerWord[0] += 2**i


        if jt1>-1 or jt2 >-1 :

	    tauMass = 1.7768 
	    tau1, tau2 = TLorentzVector(), TLorentzVector()

	    # Fill variables for Leg3, where 3->tau(ele) and 4->tau(had)
	    if channel == 'et' :
		self.pt_3[0]   = entry.Electron_pt[jt1]
		self.phi_3[0]  = entry.Electron_phi[jt1]
		self.eta_3[0]  = entry.Electron_eta[jt1]
		self.m_3[0]    = entry.Electron_mass[jt1]
		self.q_3[0]    = entry.Electron_charge[jt1]
		self.d0_3[0]   = entry.Electron_dxy[jt1]
		self.dZ_3[0]   = entry.Electron_dz[jt1]
		self.iso_3[0]  = entry.Electron_pfRelIso03_all[jt1]
		self.Electron_mvaFall17V2noIso_WP90_3[0]  = entry.Electron_mvaFall17V2noIso_WP90[jt1]

		
		# Fill genMatch variables for tau(ele)
		if isMC:
		    idx_genEle = entry.Electron_genPartIdx[jt1]

		    # if idx_genMu = -1, no match was found
		    if idx_genEle >= 0:
			idx_genEle_mom      = entry.GenPart_genPartIdxMother[idx_genEle]
			self.pt_3_tr[0]     = entry.GenPart_pt[idx_genEle]
			self.phi_3_tr[0]    = entry.GenPart_phi[idx_genEle]
			self.eta_3_tr[0]    = entry.GenPart_eta[idx_genEle]
			self.GenPart_statusFlags_3[0]    = entry.GenPart_statusFlags[idx_genEle]
			self.GenPart_status_3[0]    = entry.GenPart_status[idx_genEle]

		    try: self.gen_match_3[0] = ord(entry.Electron_genPartFlav[jt1])
		    except AttributeError: self.gen_match_3[0] = -1
		
		tau1.SetPtEtaPhiM(entry.Electron_pt[jt1],entry.Electron_eta[jt1], entry.Electron_phi[jt1], tauMass)
		tau2.SetPtEtaPhiM(entry.Tau_pt[jt2],entry.Tau_eta[jt2],entry.Tau_phi[jt2],tauMass)
		
		tauListE=[jt1]
	       

	    # Fill variables for Leg3 and Leg4, where 3->tau(ele) and 4->tau(mu)
	    elif channel == 'em' :
		self.pt_3[0]   = entry.Electron_pt[jt1]
		self.phi_3[0]  = entry.Electron_phi[jt1]
		self.eta_3[0]  = entry.Electron_eta[jt1]
		self.m_3[0]    = entry.Electron_mass[jt1]
		self.q_3[0]    = entry.Electron_charge[jt1]
		self.d0_3[0]   = entry.Electron_dxy[jt1]
		self.dZ_3[0]   = entry.Electron_dz[jt1]
		self.iso_3[0]  = entry.Electron_pfRelIso03_all[jt1]
		self.Electron_mvaFall17V2noIso_WP90_3[0]  = entry.Electron_mvaFall17V2noIso_WP90[jt1]
		
		if isMC:
		    try : self.gen_match_3[0] = ord(entry.Electron_genPartFlav[jt1])
		    except AttributeError : self.gen_match_3[0] = -1
		
		tau1.SetPtEtaPhiM(entry.Electron_pt[jt1], entry.Electron_eta[jt1], entry.Electron_phi[jt1], tauMass)
													    #???
		# fill genMatch for tau(ele)
		if isMC:
		    idx_genEle = entry.Electron_genPartIdx[jt1]

		    # if idx_genEle = -1, no match was found
		    if idx_genEle >= 0:
			idx_genEle_mom      = entry.GenPart_genPartIdxMother[idx_genEle]
			self.pt_3_tr[0]     = entry.GenPart_pt[idx_genEle]
			self.phi_3_tr[0]    = entry.GenPart_phi[idx_genEle]
			self.eta_3_tr[0]    = entry.GenPart_eta[idx_genEle]
			self.GenPart_statusFlags_3[0]    = entry.GenPart_statusFlags[idx_genEle]
			self.GenPart_status_3[0]    = entry.GenPart_status[idx_genEle]

		self.pt_4[0]     = entry.Muon_pt[jt2]
		self.phi_4[0]    = entry.Muon_phi[jt2]
		self.eta_4[0]    = entry.Muon_eta[jt2]
		self.m_4[0]      = entry.Muon_mass[jt2]
		self.q_4[0]      = entry.Muon_charge[jt2]
		self.d0_4[0]     = entry.Muon_dxy[jt2]
		self.dZ_4[0]     = entry.Muon_dz[jt2]
		self.iso_4[0]    = entry.Muon_pfRelIso04_all[jt2]
		self.tightId_4[0]      = entry.Muon_tightId[jt2]
		self.mediumId_4[0]      = entry.Muon_mediumId[jt2]
		self.mediumPromptId_4[0]   = entry.Muon_mediumPromptId[jt2]
		self.looseId_4[0]       = entry.Muon_looseId[jt2]
		self.isGlobal_4[0]      = entry.Muon_isGlobal[jt2]
		self.isTracker_4[0]     = entry.Muon_isTracker[jt2]
		self.ip3d_4[0]       = entry.Muon_ip3d[jt2]
		self.inTimeMuon_4[0]    = entry.Muon_inTimeMuon[jt2]
		if isMC:
		    try : self.gen_match_4[0] = ord(entry.Muon_genPartFlav[jt2]) 
		    except AttributeError : self.gen_match_4[0] = -1
		
		tau2.SetPtEtaPhiM(entry.Muon_pt[jt2], entry.Muon_eta[jt2], entry.Muon_phi[jt2], tauMass) 

		# fill genMatch for tau(mu)
		if isMC:
		    idx_genMu = entry.Muon_genPartIdx[jt2]
		    
		    # if idx_genMu = -1, no match was found
		    if idx_genMu >= 0:
			idx_genMu_mom       = entry.GenPart_genPartIdxMother[idx_genMu]
			self.pt_4_tr[0]     = entry.GenPart_pt[idx_genMu]
			self.phi_4_tr[0]    = entry.GenPart_phi[idx_genMu]
			self.eta_4_tr[0]    = entry.GenPart_eta[idx_genMu]
			self.GenPart_statusFlags_4[0]    = entry.GenPart_statusFlags[idx_genMu]
			self.GenPart_status_4[0]    = entry.GenPart_status[idx_genMu]


	    # Fill variables for Leg3, where 3->tau(mu) and 4->tau(had)
	    elif channel == 'mt' :
		self.pt_3[0]     = entry.Muon_pt[jt1]
		self.phi_3[0]    = entry.Muon_phi[jt1]
		self.eta_3[0]    = entry.Muon_eta[jt1]
		self.m_3[0]      = entry.Muon_mass[jt1]
		self.q_3[0]      = entry.Muon_charge[jt1]
		self.d0_3[0]     = entry.Muon_dxy[jt1]
		self.dZ_3[0]     = entry.Muon_dz[jt1]
		self.iso_3[0]    = entry.Muon_pfRelIso04_all[jt1]
		self.tightId_3[0]      = entry.Muon_tightId[jt1]
		self.mediumId_3[0]       = entry.Muon_mediumId[jt1]
		self.mediumPromptId_3[0]   = entry.Muon_mediumPromptId[jt1]
		self.looseId_3[0]       = entry.Muon_looseId[jt1]
		self.isGlobal_3[0]      = entry.Muon_isGlobal[jt1]
		self.isTracker_3[0]     = entry.Muon_isTracker[jt1]
		self.ip3d_3[0]       = entry.Muon_ip3d[jt1]
		self.inTimeMuon_3[0]    = entry.Muon_inTimeMuon[jt1]
		
		if isMC:
		    try : self.gen_match_3[0] = ord(entry.Muon_genPartFlav[jt1])
		    except AttributeError : self.gen_match_1[0] = -1
		
		tau1.SetPtEtaPhiM(entry.Muon_pt[jt1], entry.Muon_eta[jt1], entry.Muon_phi[jt1], tauMass)
		tau2.SetPtEtaPhiM(entry.Tau_pt[jt2],  entry.Tau_eta[jt2],  entry.Tau_phi[jt2],  tauMass) 
		
		# fill genMatch for tau(mu)
		if isMC:
		    idx_genMu = entry.Muon_genPartIdx[jt1]
		    
		    # if idx_genMu = -1, no match was found
		    if idx_genMu >= 0:
			idx_genMu_mom       = entry.GenPart_genPartIdxMother[idx_genMu]
			self.pt_3_tr[0]     = entry.GenPart_pt[idx_genMu]
			self.phi_3_tr[0]    = entry.GenPart_phi[idx_genMu]
			self.eta_3_tr[0]    = entry.GenPart_eta[idx_genMu]
			self.GenPart_statusFlags_3[0]    = entry.GenPart_statusFlags[idx_genMu]
			self.GenPart_status_3[0]    = entry.GenPart_status[idx_genMu]
	    
	    # Fill variables for Leg3 and Leg4, where 3->tau(had) and 4->tau(had)
	    elif channel == 'tt' :
		self.pt_3[0]     = entry.Tau_pt[jt1]
		self.phi_3[0]    = entry.Tau_phi[jt1]
		self.eta_3[0]    = entry.Tau_eta[jt1]
		self.m_3[0]      = entry.Tau_mass[jt1]
		self.q_3[0]      = entry.Tau_charge[jt1]
		self.d0_3[0]     = entry.Tau_dxy[jt1]
		self.dZ_3[0]     = entry.Tau_dz[jt1]
     

		self.idDecayModeNewDMs_3[0] = entry.Tau_idDecayModeNewDMs[jt1]
		self.idDeepTau2017v2p1VSe_3[0] = ord(entry.Tau_idDeepTau2017v2p1VSe[jt1])
		self.idDeepTau2017v2p1VSjet_3[0] = ord(entry.Tau_idDeepTau2017v2p1VSjet[jt1])
		self.idDeepTau2017v2p1VSmu_3[0] = ord(entry.Tau_idDeepTau2017v2p1VSmu[jt1])
		self.idMVAnewDM2017v2_3[0] = ord(entry.Tau_idMVAnewDM2017v2[jt1])
		self.rawMVAnewDM2017v2_3[0] = entry.Tau_rawMVAnewDM2017v2[jt1]

	
		# genMatch the hadronic tau candidate
		if isMC:
		    idx_t1_gen = GF.genMatchTau(entry, jt1, 'had')
		    if idx_t1_gen >= 0:
			self.pt_3_tr[0]  = entry.GenVisTau_pt[idx_t1_gen]
			self.phi_3_tr[0] = entry.GenVisTau_phi[idx_t1_gen]
			self.eta_3_tr[0] = entry.GenVisTau_eta[idx_t1_gen]
			self.GenPart_statusFlags_3[0]    = entry.GenPart_statusFlags[idx_t1_gen]
			self.GenPart_status_3[0]    = entry.GenPart_status[idx_t1_gen]
		    else:
			self.pt_3_tr[0]  = 1.2*entry.Tau_pt[jt1]
			self.phi_3_tr[0] = 1.2*entry.Tau_phi[jt1]
			self.eta_3_tr[0] = 1.2*entry.Tau_eta[jt1]

		    try : self.gen_match_3[0] = ord(entry.Tau_genPartFlav[jt1])
		    except AttributeError : self.gen_match_3[0] = -1

		try : self.decayMode_3[0] = int(entry.Tau_decayMode[jt1])
		except AttributeError : self.decayMode_3[0] = -1

		tau1.SetPtEtaPhiM(entry.Tau_pt[jt1], entry.Tau_eta[jt1], entry.Tau_phi[jt1], tauMass)
		tau2.SetPtEtaPhiM(entry.Tau_pt[jt2], entry.Tau_eta[jt2], entry.Tau_phi[jt2], tauMass)
		
	    else :
		print("Invalid channel={0:s} in outTuple(). Exiting.".format(channel))
		exit()
		
	    self.mt_3[0]      = self.get_mt('MVAMet',   entry,tau1)
	    self.pfmt_3[0]    = self.get_mt('PFMet',    entry,tau1)
	    self.puppimt_3[0] = self.get_mt('PUPPIMet', entry,tau1)

	    self.trigweight_3[0]  = -999.   
	    self.idisoweight_3[0] = -999.   
	    
	    # Fill variables for Leg4, where 4->tau(had)
	    if channel != 'em':
		self.pt_4[0]  = entry.Tau_pt[jt2]
		self.phi_4[0] = entry.Tau_phi[jt2]
		self.eta_4[0] = entry.Tau_eta[jt2]
		self.m_4[0]   = entry.Tau_mass[jt2]
		self.q_4[0]   = entry.Tau_charge[jt2]
		self.d0_4[0]  = entry.Tau_dxy[jt2]
		self.dZ_4[0]  = entry.Tau_dz[jt2]

		self.idDecayModeNewDMs_4[0] = entry.Tau_idDecayModeNewDMs[jt2]
		self.idDeepTau2017v2p1VSe_4[0] = ord(entry.Tau_idDeepTau2017v2p1VSe[jt2])
		self.idDeepTau2017v2p1VSjet_4[0] = ord(entry.Tau_idDeepTau2017v2p1VSjet[jt2])
		self.idDeepTau2017v2p1VSmu_4[0] = ord(entry.Tau_idDeepTau2017v2p1VSmu[jt2])
		self.idMVAnewDM2017v2_4[0] = ord(entry.Tau_idMVAnewDM2017v2[jt2])
		self.rawMVAnewDM2017v2_4[0] = entry.Tau_rawMVAnewDM2017v2[jt2]
		
		phi, pt = entry.Tau_phi[jt2], entry.Tau_pt[jt2]
		
		self.mt_4[0]      = self.get_mt('MVAMet',   entry, tau2) 
		self.pfmt_4[0]    = self.get_mt('PFMet',    entry, tau2)
		self.puppimt_4[0] = self.get_mt('PUPPIMet', entry, tau2) 


		# genMatch the hadronic tau candidate
		if isMC:
		    idx_t2_gen = GF.genMatchTau(entry, jt2, 'had')
		    if idx_t2_gen >= 0:
			self.pt_4_tr[0]  = entry.GenVisTau_pt[idx_t2_gen]
			self.phi_4_tr[0] = entry.GenVisTau_phi[idx_t2_gen]
			self.eta_4_tr[0] = entry.GenVisTau_eta[idx_t2_gen]
			self.GenPart_statusFlags_4[0]    = entry.GenPart_statusFlags[idx_t2_gen]
			self.GenPart_status_4[0]    = entry.GenPart_status[idx_t2_gen]
		    else:
			self.pt_4_tr[0]  = 1.2*entry.Tau_pt[jt2]
			self.phi_4_tr[0] = 1.2*entry.Tau_phi[jt2]
			self.eta_4_tr[0] = 1.2*entry.Tau_eta[jt2]

		    try : self.gen_match_4[0] = ord(entry.Tau_genPartFlav[jt2])
		    except AttributeError: self.gen_match_4[0] = -1

		try : self.decayMode_4[0] = int(entry.Tau_decayMode[jt2])
		except AttributeError: self.decayMode_4[0] = -1

		self.trigweight_4[0]  = -999.   # requires sf need help from Sam on these
		self.idisoweight_4[0] = -999.   # requires sf need help from Sam on these

	    # di-tau variables
	    self.pt_tt[0]  = self.getPt_tt( entry, tau1, tau2)
	    self.H_DR[0] = self.getDR(entry,tau1,tau2)
	    self.mt_tot[0] = self.getMt_tot(entry, tau1, tau2)
	    self.m_vis[0]  = self.getM_vis( entry, tau1, tau2)
		
	    if SVFit :
		fastMTTmass, fastMTTtransverseMass = self.runSVFit(entry, channel, jt1, jt2, tau1, tau2) 
	    else :
		fastMTTmass, fastMTTtransverseMass = -999., -999.
		
	    self.m_sv[0] = fastMTTmass 
	    self.mt_sv[0] = fastMTTtransverseMass  


        # Sort the di-lepton system by Pt
        Lep1, Lep2 = TLorentzVector(), TLorentzVector()
        if (LepP.Pt() > LepM.Pt()): 
            Lep1 = LepP
            Lep2 = LepM
        else:
            Lep1 = LepM
            Lep2 = LepP


        # di-lepton variables.   _p and _m refer to plus and minus charge
        if jt1>-1 and jt2>-1 : self.AMass[0]       = (Lep1 + Lep2 + tau1 + tau2).M() 
        self.mll[0]       = (Lep1 + Lep2).M()
        self.Z_DR[0]       = self.getDR(entry,Lep1,Lep2)
       
        self.H_LT[0]       = Lep1.Pt() + Lep2.Pt()
        self.dRl1H[0]  = self.getDR(entry,Lep1,tau1+tau2)
        self.dRl2H[0]  = self.getDR(entry,Lep2,tau1+tau2)
        self.dRlH[0]  = self.getDR(entry,Lep1+Lep2,tau1+tau2)

        self.dPhil1H[0]  = self.getdPhi(entry,Lep1,tau1+tau2)
        self.dPhil2H[0]  = self.getdPhi(entry,Lep2,tau1+tau2)
        self.dPhilH[0]  = self.getdPhi(entry,Lep1+Lep2,tau1+tau2)
           
        self.pt_1[0]   = Lep1.Pt()
        self.phi_1[0]  = Lep1.Phi()
        self.eta_1[0]  = Lep1.Eta()
        self.pt_2[0]   = Lep2.Pt()
        self.phi_2[0]  = Lep2.Phi()
        self.eta_2[0]  = Lep2.Eta()

	lep_index_1 = lepList[0]
	lep_index_2 = lepList[1]

	if (LepP.Pt() < LepM.Pt()):
	    lep_index_1 = lepList[1]
	    lep_index_2 = lepList[0]
	#relIso 
	if channel_ll == 'ee' : 
      
            self.iso_1[0]  = entry.Electron_pfRelIso03_all[lep_index_1]
            self.iso_2[0]  = entry.Electron_pfRelIso03_all[lep_index_2]
            self.q_1[0]  = entry.Electron_charge[lep_index_1]
            self.q_2[0]  = entry.Electron_charge[lep_index_2]
            self.d0_1[0]   = entry.Electron_dxy[lep_index_1]
            self.dZ_1[0]   = entry.Electron_dz[lep_index_1]
            self.d0_2[0]   = entry.Electron_dxy[lep_index_2]
            self.dZ_2[0]   = entry.Electron_dz[lep_index_2]
            self.Electron_mvaFall17V2noIso_WP90_1[0]  = entry.Electron_mvaFall17V2noIso_WP90[lep_index_1]
            self.Electron_mvaFall17V2noIso_WP90_2[0]  = entry.Electron_mvaFall17V2noIso_WP90[lep_index_2]


	if channel_ll == 'mm' : 
            self.iso_1[0]  = entry.Muon_pfRelIso04_all[lep_index_1]
	    self.iso_2[0]  = entry.Muon_pfRelIso04_all[lep_index_2]
	    self.q_1[0]  = entry.Muon_charge[lep_index_1]
	    self.q_2[0]  = entry.Muon_charge[lep_index_2]
	    self.d0_1[0]   = entry.Muon_dxy[lep_index_1]
	    self.dZ_1[0]   = entry.Muon_dz[lep_index_1]
	    self.d0_2[0]   = entry.Muon_dxy[lep_index_2]
	    self.dZ_2[0]   = entry.Muon_dz[lep_index_2]
	    self.looseId_1[0]   = entry.Muon_looseId[lep_index_1] 
	    self.looseId_2[0]   = entry.Muon_looseId[lep_index_2] 
            self.tightId_1[0]      = entry.Muon_tightId[lep_index_1]
            self.tightId_2[0]      = entry.Muon_tightId[lep_index_2]
	    self.mediumId_1[0]   = entry.Muon_mediumId[lep_index_1] 
	    self.mediumId_2[0]   = entry.Muon_mediumId[lep_index_2] 
	    self.mediumPromptId_1[0]   = entry.Muon_mediumPromptId[lep_index_1] 
	    self.mediumPromptId_2[0]   = entry.Muon_mediumPromptId[lep_index_2] 
	    self.isGlobal_1[0]   = entry.Muon_isGlobal[lep_index_1] 
	    self.isGlobal_2[0]   = entry.Muon_isGlobal[lep_index_2] 
	    self.isTracker_1[0]   = entry.Muon_isTracker[lep_index_1] 
	    self.isTracker_2[0]   = entry.Muon_isTracker[lep_index_2] 

        
        # genMatch the di-lepton variables
	if isMC :
	    idx_Lep1, idx_Lep2 = -1, -1
	    idx_Lep1_tr, idx_Lep2_tr = -1, -1
	    if (Lep1.M() > 0.05 and Lep2.M() > 0.05): # muon mass 
		idx_Lep1 = GF.getLepIdxFrom4Vec(entry, Lep1, 'm')
		idx_Lep2 = GF.getLepIdxFrom4Vec(entry, Lep2, 'm')
		try :
		    idx_Lep1_tr = entry.Muon_genPartIdx[idx_Lep1]
		    idx_Lep2_tr = entry.Muon_genPartIdx[idx_Lep2]
		except IndexError : pass 
		    
	    elif (Lep1.M() < 0.05 and Lep2.M() < 0.05): # electron mass
		idx_Lep1 = GF.getLepIdxFrom4Vec(entry, Lep1, 'e')
		idx_Lep2 = GF.getLepIdxFrom4Vec(entry, Lep2, 'e')
		try :
		    idx_Lep1_tr = entry.Electron_genPartIdx[idx_Lep1]
		    idx_Lep2_tr = entry.Electron_genPartIdx[idx_Lep2]
		except IndexError : pass 
		    
	    if idx_Lep1_tr >= 0 and idx_Lep2_tr >= 0:
		self.m_1_tr[0]  = entry.GenPart_mass[idx_Lep1_tr]
		self.pt_1_tr[0]  = entry.GenPart_pt[idx_Lep1_tr]
		self.m_2_tr[0]  = entry.GenPart_mass[idx_Lep2_tr]
		self.pt_2_tr[0]  = entry.GenPart_pt[idx_Lep2_tr]
		self.eta_1_tr[0] = entry.GenPart_eta[idx_Lep1_tr]
		self.eta_2_tr[0] = entry.GenPart_eta[idx_Lep2_tr]
		self.phi_1_tr[0] = entry.GenPart_phi[idx_Lep1_tr]
		self.phi_2_tr[0] = entry.GenPart_phi[idx_Lep2_tr]
		self.GenPart_statusFlags_1[0]    = entry.GenPart_statusFlags[idx_Lep1_tr]
		self.GenPart_status_1[0]    = entry.GenPart_status[idx_Lep1_tr]
		self.GenPart_statusFlags_2[0]    = entry.GenPart_statusFlags[idx_Lep2_tr]
		self.GenPart_status_2[0]    = entry.GenPart_status[idx_Lep2_tr]
        
        # MET variables
        self.met[0]         = entry.MET_pt    
        self.metphi[0]      = entry.MET_phi
        self.puppimet[0]    = entry.PuppiMET_pt
        self.puppimetphi[0] = entry.PuppiMET_phi
        
        self.metcov00[0] = entry.MET_covXX
        self.metcov01[0] = entry.MET_covXY
        self.metcov10[0] = entry.MET_covXY	
        self.metcov11[0] = entry.MET_covYY
	self.met_UnclX = entry.MET_MetUnclustEnUpDeltaX
	self.met_UnclY = entry.MET_MetUnclustEnUpDeltaY
        
        self.metpt_nom[0] = entry.MET_pt
        self.metphi_nom[0] =  entry.MET_phi
        if doUncertainties : 
            self.metpt_nom[0] = entry.MET_pt_nom
            self.metphi_nom[0] =  entry.MET_phi_nom
            if isMC : 
		self.metpt_JER[0] = entry.MET_pt_jer
		self.metphi_JER[0] = entry.MET_phi_jer
		self.metpt_JERUp[0] = entry.MET_pt_jerUp
		self.metphi_JERUp[0] = entry.MET_phi_jerUp
		self.metpt_JERDown[0] = entry.MET_pt_jerDown
		self.metphi_JERDown[0] = entry.MET_phi_jerDown
		self.metpt_JESUp[0] = entry.MET_pt_jesTotalUp
		self.metphi_JESUp[0] = entry.MET_phi_jesTotalUp
		self.metpt_JESDown[0] = entry.MET_pt_jesTotalDown
		self.metphi_JESDown[0] = entry.MET_phi_jesTotalDown
		self.metpt_UnclUp[0] = entry.MET_pt_unclustEnUp
		self.metphi_UnclUp[0] = entry.MET_phi_unclustEnUp
		self.metpt_UnclDown[0] = entry.MET_pt_unclustEnDown
		self.metphi_UnclDown[0] = entry.MET_phi_unclustEnDown

        # trig
	self.isTrig_1[0]   = is_trig_1
        self.isTrig_2[0]   = is_trig_2
	self.isDoubleTrig[0]   = is_Dtrig_1
        leplist=[]
        leplist.append(LepP)
        leplist.append(LepM)
	if jt1>-1 and jt2>-1 :  
	    leplist.append(tau1)
	    leplist.append(tau2)

        #if jt1>-1 and jt2>-1 :  
        #jetList, bJetList, bJetListFlav = self.getJets(entry,tau1,tau2,era) 
        #print 'old ', jetList, bJetList
	#else :  nJet30, jetList, bJetList, bJetListFlav = self.getJets(entry,LepP,LepM,era) 
        #self.nbtagold[0] = len(bJetList)
	#self.njetsold[0] = len(jetList)

	#print 'inside', sysVariations
	for ic, isys in enumerate(sysVariations):  
	    jetList, bJetList, bJetListT, bJetListFlav = self.getJetsJMEMV(entry,leplist,era,isys) 


	    self.njets[ic] = len(jetList)
	    self.nbtag[ic] = len(bJetList)
	    self.nbtagT[ic] = len(bJetListT)


	    if isys !='' and '_' not in isys: isys="_"+isys
	    self.jpt_1[ic], self.jeta_1[ic], self.jphi_1[ic], self.jcsv_1[ic], self.jcsvfv_1[ic]= -9.99, -9.99, -9.99, -9.99, -9.99 
	    if len(jetList) > 0 :
		jpt1 = getattr(entry, "Jet_pt{0:s}".format(str(isys)), None)
		jj1 = jetList[0]
		self.jpt_1[ic]  = jpt1[jj1]
		self.jeta_1[ic] = entry.Jet_eta[jj1]
		self.jphi_1[ic] = entry.Jet_phi[jj1]
		self.jcsv_1[ic] = entry.Jet_btagDeepB[jj1]
		self.jcsvfv_1[ic] = entry.Jet_btagDeepFlavB[jj1]
		
		# genMatch jet1
		if isMC:
		    idx_genJet = entry.Jet_genJetIdx[jj1]
		    if idx_genJet >= 0:
			try :
			    self.jpt_1_tr[ic]  = entry.GenJet_pt[idx_genJet]
			    self.jeta_1_tr[ic] = entry.GenJet_eta[idx_genJet]
			    self.jphi_1_tr[ic] = entry.GenJet_phi[idx_genJet]
			except IndexError : pass

	    self.jpt_2[ic], self.jeta_2[ic], self.jphi_2[ic], self.jcsv_2[ic],self.jcsvfv_2[ic] = -9.99, -9.99, -9.99, -9.99, -9.99
	    if len(jetList) > 1 :
		jpt2 = getattr(entry, "Jet_pt{0:s}".format(str(isys)), None)
		jj2 = jetList[1] 
		self.jpt_2[ic]  = jpt2[jj2]
		self.jeta_2[ic] = entry.Jet_eta[jj2]
		self.jphi_2[ic] = entry.Jet_phi[jj2]
		self.jcsv_2[ic] = entry.Jet_btagDeepB[jj2]
		self.jcsvfv_2[ic] = entry.Jet_btagDeepFlavB[jj2]
		
		# genMatch jet2
		if isMC:
		    idx_genJet = entry.Jet_genJetIdx[jj2]
		    if idx_genJet >= 0:
			try: 
			   self.jpt_2_tr[ic]  = entry.GenJet_pt[idx_genJet]
			   self.jeta_2_tr[ic] = entry.GenJet_eta[idx_genJet]
			   self.jphi_2_tr[ic] = entry.GenJet_phi[idx_genJet]
			except IndexError : pass 

	    self.bpt_1[ic], self.beta_1[ic], self.bphi_1[ic], self.bcsv_1[ic], self.bcsvfv_1[ic] = -9.99, -9.99, -9.99, -9.99, -9.99
	    if len(bJetList) > 0 :
		jpt1 = getattr(entry, "Jet_pt{0:s}".format(str(isys)), None)
		jbj1 = bJetList[0]
		self.bpt_1[ic] = jpt1[jbj1]
		self.beta_1[ic] = entry.Jet_eta[jbj1]
		self.bphi_1[ic] = entry.Jet_phi[jbj1]
		self.bcsv_1[ic] = entry.Jet_btagDeepB[jbj1] 
		self.bcsvfv_1[ic] = entry.Jet_btagDeepFlavB[jbj1]
		
	    self.bpt_2[ic], self.beta_2[ic], self.bphi_2[ic], self.bcsv_2[ic], self.bcsvfv_2[ic] = -9.99, -9.99, -9.99, -9.99, -9.99
	    if len(bJetList) > 1 :
		jpt2 = getattr(entry, "Jet_pt{0:s}".format(str(isys)), None)
		jbj2 = bJetList[1] 
		self.bpt_2[ic] = jpt2[jbj2]
		self.beta_2[ic] = entry.Jet_eta[jbj2]
		self.bphi_2[ic] = entry.Jet_phi[jbj2]
		self.bcsv_2[ic] = entry.Jet_btagDeepB[jbj2]
		self.bcsvfv_2[ic] = entry.Jet_btagDeepFlavB[jbj2]

		# genMatch bjet1
		if isMC:
		    idx_genJet = entry.Jet_genJetIdx[jbj2]
		    if idx_genJet >= 0:
			try :
			    self.bpt_2_tr[ic]  = entry.GenJet_pt[idx_genJet]
			    self.beta_2_tr[ic] = entry.GenJet_eta[idx_genJet]
			    self.bphi_2_tr[ic] = entry.GenJet_phi[idx_genJet]
			except IndexError : pass
        self.t.Fill()

	return

    def Fill3L(self, entry, cat, LepP, LepM, lepList, lepList_2, ElList, MuList, TauList, isMC, era, doUncertainties=False, sysVariations=[]) :
        ''' - jt1 point to the selected tau candidates according to the table below.
            - LepP and LepM are TLorentz vectors for the positive and negative members of the dilepton pair
        ''' 
        nelectrons = len(ElList)
        nmuons = len(MuList)
        ntaus = len(TauList)

        is_trig_1, is_trig_2, is_Dtrig_1 = 0,0,0
        TrigListLep = []
        TrigListTau = []
        hltListLep  = []

        #channel_ll = 'mm' or 'ee'
        channel_ll = cat[:2]

	TrigListLep, hltListLep  = GF.findSingleLeptTrigger(lepList, entry, channel_ll, era)

	TrigListLep = list(dict.fromkeys(TrigListLep))

	TrigListLepD, hltListLepD  = GF.findDoubleLeptTrigger(lepList, entry, channel_ll, era)

	TrigListLepD = list(dict.fromkeys(TrigListLepD))

	#if len(TrigListLepD) > 0 : print TrigListLepD, hltListLepD, TrigListLep, hltListLep
	if len(TrigListLepD) == 2 : 
	    if lepList[0] == TrigListLepD[0] :
	        is_Dtrig_1 = 1 #that means that the leading lepton 
	    else : 
	        is_Dtrig_1 = -1


        if len(TrigListLep) == 1 :

	    if lepList[0] == TrigListLep[0] :
	        is_trig_1 = 1.
	    else:
	        is_trig_1 = -1. #that means that the subleading fired the trigger


        if len(TrigListLep) == 2 :
            if 'BothLept' in hltListLep :
	        is_trig_1 = 1.
	        is_trig_2 = 1.

        '''
	TrigListLepD, hltListLepD  = GF.findDoubleLeptTrigger(lepList+lepList_2, entry, channel_ll, era)

	TrigListLepD = list(dict.fromkeys(TrigListLepD))


	if len(TrigListLepD) == 2 : 
	    if lepList[0] == TrigListLepD[0] :
	        is_Dtrig_1 = 1
	    else : 
	        is_Dtrig_1 = -1

        #if len(TrigListLep) == 1 :

	for i in TrigListLep :
	    is_trig_1 += 2**i
            #print 'trig_1', i, '2^i', 2**i, entry.event, is_trig_1

	for i in TrigListLepD : 
	    is_trig_2 += 2**i
            #print 'trig_2', i, '2^i', 2**i, entry.event, is_trig_2, '===============>', is_trig_1
	    #else:
	    #    is_trig_1 = -1. #that means that a subleading lepton fired the trigger


        #if len(TrigListLep) == 2 :
        #    if 'BothLept' in hltListLep :
	#        is_trig_1 = 1.
	#        is_trig_2 = 1.

        '''

        channel = cat[-2:]
        
        self.entries += 1

        self.run[0]  = entry.run
        self.nElectron[0]  = nelectrons
        self.nMuon[0]  = nmuons
        self.nTau[0]  = ntaus
        self.lumi[0] = entry.luminosityBlock 
        self.evt[0]  = entry.event
        self.iso_1[0]  = -99
        self.iso_2[0]  = -99
        self.q_1[0]  = -99
        self.q_2[0]  = -99
        self.isGlobal_1[0]  = -99
        self.isGlobal_2[0]  = -99

        self.tightId_1[0]       = -1 
        self.mediumId_1[0]       = -1 
        self.mediumPromptId_1[0]   = -1
        self.looseId_1[0]       = -1
        self.isGlobal_1[0]      = -1
        self.isTracker_1[0]     = -1

        self.tightId_2[0]       = -1 
        self.mediumId_2[0]       = -1 
        self.mediumPromptId_2[0]   = -1
        self.looseId_2[0]       = -1
        self.isGlobal_2[0]      = -1
        self.isTracker_2[0]     = -1

       
        self.decayMode_3[0]        = -1
        self.idDecayModeNewDMs_3[0]= -1
        self.idDeepTau2017v2p1VSe_3[0] = -1
        self.idDeepTau2017v2p1VSjet_3[0] = -1
        self.idDeepTau2017v2p1VSmu_3[0] = -1
        self.idMVAnewDM2017v2_3[0] = -1
        self.rawMVAnewDM2017v2_3[0] = -1
        self.mediumId_3[0]       = -1 
        self.mediumPromptId_3[0]   = -1
        self.looseId_3[0]       = -1
        self.isGlobal_3[0]      = -1
        self.isTracker_3[0]     = -1
        self.ip3d_3[0]          = -1
        self.inTimeMuon_3[0]    = -1

        self.decayMode_4[0]      = -1
        self.idDecayModeNewDMs_4[0] = -1
        self.idDeepTau2017v2p1VSe_4[0] = -1
        self.idDeepTau2017v2p1VSjet_4[0] = -1
        self.idDeepTau2017v2p1VSmu_4[0] = -1
        self.idMVAnewDM2017v2_4[0] = -1
        self.rawMVAnewDM2017v2_4[0] = -1
        self.mediumId_4[0]       = -1 
        self.mediumPromptId_4[0]   = -1
        self.looseId_4[0]       = -1
        self.isGlobal_4[0]      = -1
        self.isTracker_4[0]     = -1
        self.ip3d_4[0]          = -1
        self.inTimeMuon_4[0]    = -1
        self.gen_match_1[0] = -1
        self.gen_match_2[0] = -1
        self.gen_match_3[0] = -1
        self.gen_match_4[0] = -1
        self.gen_match_5[0] = -1

        self.decayMode_5[0]      = -1
        self.idDecayModeNewDMs_5[0] = -1
        self.idDeepTau2017v2p1VSe_5[0] = -1
        self.idDeepTau2017v2p1VSjet_5[0] = -1
        self.idDeepTau2017v2p1VSmu_5[0] = -1
        self.idMVAnewDM2017v2_5[0] = -1
        self.rawMVAnewDM2017v2_5[0] = -1

        goodElectronList = tauFun.makeGoodElectronList(entry)
        goodMuonList = tauFun.makeGoodMuonList(entry)
        
        self.nGoodElectron[0] =  nelectrons
        self.nGoodMuon[0]     = nmuons
        self.cat[0]  = tauFun.catToNumber3L(cat)
        

        try :
            self.weight[0]           = entry.genWeight
            self.LHEweight[0]        = entry.LHEWeight_originalXWGTUP
            self.Generator_weight[0] = entry.Generator_weight
            self.LHE_Njets[0]        = ord(entry.LHE_Njets) 
	    self.nPU[0]  = entry.Pileup_nPU
	    self.nPUEOOT[0]  = entry.Pileup_sumEOOT
	    self.nPULOOT[0]  = entry.Pileup_sumLOOT
	    self.nPUtrue[0]  = entry.Pileup_nTrueInt
	    self.nPV[0]  = entry.PV_npvs
	    self.nPVGood[0]  = entry.PV_npvsGood
                        
        except AttributeError :
            self.weight[0]           = 1. 
            self.weightPU[0]         = -1
            self.weightPUtrue[0]     = -1
            self.LHEweight[0]        = 1. 
            self.Generator_weight[0] = 1.
            self.LHE_Njets[0] = -1
	    self.nPU[0]  = -1
	    self.nPUEOOT[0]  = -1
	    self.nPULOOT[0]  = -1
	    self.nPUtrue[0]  = -1
	    self.nPV[0]  = -1
	    self.nPVGood[0]  = -1

        # pack trigger bits into integer word
        year = int(era)
        e = entry
	bits=[]

        try : bits.append(e.HLT_Ele35_WPTight_Gsf)
        except AttributeError : bits.append(False)
        try : bits.append(e.HLT_Ele32_WPTight_Gsf)
        except AttributeError : bits.append(False)
        try : bits.append(e.HLT_Ele27_eta2p1_WPTight_Gsf)
        except AttributeError : bits.append(False) 
        try : bits.append(e.HLT_Ele25_eta2p1_WPTight_Gsf)
        except AttributeError : bits.append(False)

        try : bits.append(e.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL)
        except AttributeError : bits.append(False)
        try : bits.append(e.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ)
        except AttributeError : bits.append(False) 

        self.electronTriggerWord[0] = 0
        for i, bit in enumerate(bits) :
            if bit : self.electronTriggerWord[0] += 2**i

        bits=[]
        try : bits.append(e.HLT_IsoMu27)
        except AttributeError : bits.append(False) 
        try : bits.append(e.HLT_IsoMu24)
        except AttributeError : bits.append(False) 
        try : bits.append(e.HLT_IsoTkMu24)
        except AttributeError : bits.append(False)
        for i in range(5) : bits.append(False)         # pad rest of this byte 
        
        try : bits.append(e.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ)
        except AttributeError : bits.append(False) 
        try : bits.append(e.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8)
        except AttributeError : bits.append(False)
        try : bits.append(e.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8)
        except AttributeError : bits.append(False)
        try : bits.append(e.HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ)
        except AttributeError : bits.append(False) 
        try : bits.append(e.HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_Mass8)
        except AttributeError : bits.append(False) 

        self.muonTriggerWord[0] = 0
        for i, bit in enumerate(bits) :
            if bit : self.muonTriggerWord[0] += 2**i


        # Sort the di-lepton system by Pt
        Lep1, Lep2 = TLorentzVector(), TLorentzVector()
	lep_index_1 = lepList[0]
	lep_index_2 = lepList[1]

        if (LepP.Pt() > LepM.Pt()): 
            Lep1 = LepP
            Lep2 = LepM
        else:
            Lep1 = LepM
            Lep2 = LepP
	    lep_index_1 = lepList[1]
	    lep_index_2 = lepList[0]

        # di-lepton variables.   _p and _m refer to plus and minus charge
        self.mll[0]       = (Lep1 + Lep2).M()
        self.Z_DR[0]       = self.getDR(entry,Lep1,Lep2)

        self.H_LT[0]       = Lep1.Pt() + Lep2.Pt()
           
        self.pt_1[0]   = Lep1.Pt()
        self.phi_1[0]  = Lep1.Phi()
        self.eta_1[0]  = Lep1.Eta()
        self.pt_2[0]   = Lep2.Pt()
        self.phi_2[0]  = Lep2.Phi()
        self.eta_2[0]  = Lep2.Eta()

	if channel_ll == 'ee' : 
      
            self.iso_1[0]  = entry.Electron_pfRelIso03_all[lep_index_1]
            self.iso_2[0]  = entry.Electron_pfRelIso03_all[lep_index_2]
            self.q_1[0]  = entry.Electron_charge[lep_index_1]
            self.q_2[0]  = entry.Electron_charge[lep_index_2]
            self.d0_1[0]   = entry.Electron_dxy[lep_index_1]
            self.dZ_1[0]   = entry.Electron_dz[lep_index_1]
            self.d0_2[0]   = entry.Electron_dxy[lep_index_2]
            self.dZ_2[0]   = entry.Electron_dz[lep_index_2]
            self.Electron_mvaFall17V2noIso_WP90_1[0]  = entry.Electron_mvaFall17V2noIso_WP90[lep_index_1]
            self.Electron_mvaFall17V2noIso_WP90_2[0]  = entry.Electron_mvaFall17V2noIso_WP90[lep_index_2]

	if channel_ll == 'mm' : 

            self.iso_1[0]  = entry.Muon_pfRelIso04_all[lep_index_1]
	    self.iso_2[0]  = entry.Muon_pfRelIso04_all[lep_index_2]
	    self.q_1[0]  = entry.Muon_charge[lep_index_1]
	    self.q_2[0]  = entry.Muon_charge[lep_index_2]
	    self.d0_1[0]   = entry.Muon_dxy[lep_index_1]
	    self.dZ_1[0]   = entry.Muon_dz[lep_index_1]
	    self.d0_2[0]   = entry.Muon_dxy[lep_index_2]
	    self.dZ_2[0]   = entry.Muon_dz[lep_index_2]
	    self.looseId_1[0]   = entry.Muon_looseId[lep_index_1] 
	    self.looseId_2[0]   = entry.Muon_looseId[lep_index_2] 
            self.tightId_1[0]      = entry.Muon_tightId[lep_index_1]
            self.tightId_2[0]      = entry.Muon_tightId[lep_index_2]
	    self.mediumId_1[0]   = entry.Muon_mediumId[lep_index_1] 
	    self.mediumId_2[0]   = entry.Muon_mediumId[lep_index_2] 
	    self.mediumPromptId_1[0]   = entry.Muon_mediumPromptId[lep_index_1] 
	    self.mediumPromptId_2[0]   = entry.Muon_mediumPromptId[lep_index_2] 
	    self.isGlobal_1[0]   = entry.Muon_isGlobal[lep_index_1] 
	    self.isGlobal_2[0]   = entry.Muon_isGlobal[lep_index_2] 
	    self.isTracker_1[0]   = entry.Muon_isTracker[lep_index_1] 
	    self.isTracker_2[0]   = entry.Muon_isTracker[lep_index_2] 


        #print ElList, MuList, TauList
        eL1, eL2= TLorentzVector(), TLorentzVector()  
        if nelectrons > 0 :
	    ie = ElList[0]

            if len(ElList)>1 :
                if entry.Electron_pt[ElList[0]] > entry.Electron_pt[ElList[1]] : 
		    ie = ElList[0] 
		    iee = ElList[1] 
		else : 
		    ie = ElList[1] 
		    iee = ElList[0] 

	    self.pt_3[0]   = entry.Electron_pt[ie]
	    self.phi_3[0]  = entry.Electron_phi[ie]
	    self.eta_3[0]  = entry.Electron_eta[ie]
	    self.m_3[0]    = entry.Electron_mass[ie]
	    self.q_3[0]    = entry.Electron_charge[ie]
	    self.d0_3[0]   = entry.Electron_dxy[ie]
	    self.dZ_3[0]   = entry.Electron_dz[ie]
	    self.iso_3[0]  = entry.Electron_pfRelIso03_all[ie]
	    self.Electron_mvaFall17V2noIso_WP90_3[0]  = entry.Electron_mvaFall17V2noIso_WP90[ie]
	    try : self.gen_match_3[0] = ord(entry.Electron_genPartFlav[ie])
	    except AttributeError : self.gen_match_3[0] = -1


            if len(ElList)>1 :
		self.pt_4[0]   = entry.Electron_pt[iee]
		self.phi_4[0]  = entry.Electron_phi[iee]
		self.eta_4[0]  = entry.Electron_eta[iee]
		self.m_4[0]    = entry.Electron_mass[iee]
		self.q_4[0]    = entry.Electron_charge[iee]
		self.d0_4[0]   = entry.Electron_dxy[iee]
		self.dZ_4[0]   = entry.Electron_dz[iee]
		self.iso_4[0]  = entry.Electron_pfRelIso03_all[iee]
		self.Electron_mvaFall17V2noIso_WP90_4[0]  = entry.Electron_mvaFall17V2noIso_WP90[iee]
		try : self.gen_match_4[0] = ord(entry.Electron_genPartFlav[iee])
		except AttributeError : self.gen_match_4[0] = -1

		eL1.SetPtEtaPhiM(entry.Electron_pt[ElList[0]],entry.Electron_eta[ElList[0]], entry.Electron_phi[ElList[0]], electronMass)
		eL2.SetPtEtaPhiM(entry.Electron_pt[ElList[1]],entry.Electron_eta[ElList[1]], entry.Electron_phi[ElList[1]], electronMass)
		self.mll2[0] = (eL1 + eL2).M()


        if nmuons > 0:
            
	    im = MuList[0]

            if len(MuList)>1 :
                if  entry.Muon_pt[MuList[0]] > entry.Muon_pt[MuList[1]] : 
		    im = MuList[0] 
		    imm = MuList[1] 
		else : 
		    im = MuList[1] 
		    imm = MuList[0] 

	    self.pt_3[0]     = entry.Muon_pt[im]
	    self.phi_3[0]    = entry.Muon_phi[im]
	    self.eta_3[0]    = entry.Muon_eta[im]
	    self.m_3[0]      = entry.Muon_mass[im]
	    self.q_3[0]      = entry.Muon_charge[im]
	    self.d0_3[0]     = entry.Muon_dxy[im]
	    self.dZ_3[0]     = entry.Muon_dz[im]
	    self.iso_3[0]    = entry.Muon_pfRelIso04_all[im]
	    self.tightId_3[0]   = entry.Muon_tightId[im] 
	    self.mediumId_3[0]      = entry.Muon_mediumId[im]
	    self.tightId_3[0]      = entry.Muon_tightId[im]
	    self.mediumPromptId_3[0]   = entry.Muon_mediumPromptId[im]
	    self.looseId_3[0]       = entry.Muon_looseId[im]
	    self.isGlobal_3[0]      = entry.Muon_isGlobal[im]
	    self.isTracker_3[0]     = entry.Muon_isTracker[im]
	    self.ip3d_3[0]       = entry.Muon_ip3d[im]
	    self.inTimeMuon_3[0]    = entry.Muon_inTimeMuon[im]
	    try : self.gen_match_3[0] = ord(entry.Muon_genPartFlav[im])
	    except AttributeError : self.gen_match_3[0] = -1


            if len(MuList)>1 :

		self.pt_4[0]     = entry.Muon_pt[imm]
		self.phi_4[0]    = entry.Muon_phi[imm]
		self.eta_4[0]    = entry.Muon_eta[imm]
		self.m_4[0]      = entry.Muon_mass[imm]
		self.q_4[0]      = entry.Muon_charge[imm]
		self.d0_4[0]     = entry.Muon_dxy[imm]
		self.dZ_4[0]     = entry.Muon_dz[imm]
		self.iso_4[0]    = entry.Muon_pfRelIso04_all[imm]
		self.tightId_4[0]   = entry.Muon_tightId[imm] 
		self.mediumId_4[0]      = entry.Muon_mediumId[imm]
		self.mediumPromptId_4[0]   = entry.Muon_mediumPromptId[imm]
		self.looseId_4[0]       = entry.Muon_looseId[imm]
		self.isGlobal_4[0]      = entry.Muon_isGlobal[imm]
		self.isTracker_4[0]     = entry.Muon_isTracker[imm]
		self.ip3d_4[0]       = entry.Muon_ip3d[imm]
		self.inTimeMuon_4[0]    = entry.Muon_inTimeMuon[imm]
		try : self.gen_match_4[0] = ord(entry.Muon_genPartFlav[imm])
		except AttributeError : self.gen_match_4[0] = -1
		eL1.SetPtEtaPhiM(entry.Muon_pt[MuList[0]],entry.Muon_eta[MuList[0]], entry.Muon_phi[MuList[0]], muonMass)
		eL2.SetPtEtaPhiM(entry.Muon_pt[MuList[1]],entry.Muon_eta[MuList[1]], entry.Muon_phi[MuList[1]], muonMass)
		self.mll2[0] = (eL1 + eL2).M()

        # genMatch the di-lepton variables
	if isMC :
	    idx_Lep1, idx_Lep2 = -1, -1
	    idx_Lep1_tr, idx_Lep2_tr = -1, -1
	    if (Lep1.M() > 0.05 and Lep2.M() > 0.05): # muon mass 
		idx_Lep1 = GF.getLepIdxFrom4Vec(entry, Lep1, 'm')
		idx_Lep2 = GF.getLepIdxFrom4Vec(entry, Lep2, 'm')
		try :
		    idx_Lep1_tr = entry.Muon_genPartIdx[idx_Lep1]
		    idx_Lep2_tr = entry.Muon_genPartIdx[idx_Lep2]
		except IndexError : pass 
		    
	    elif (Lep1.M() < 0.05 and Lep2.M() < 0.05): # electron mass
		idx_Lep1 = GF.getLepIdxFrom4Vec(entry, Lep1, 'e')
		idx_Lep2 = GF.getLepIdxFrom4Vec(entry, Lep2, 'e')
		try :
		    idx_Lep1_tr = entry.Electron_genPartIdx[idx_Lep1]
		    idx_Lep2_tr = entry.Electron_genPartIdx[idx_Lep2]
		except IndexError : pass 
		    
	    if idx_Lep1_tr >= 0 and idx_Lep2_tr >= 0:
		self.m_1_tr[0]  = entry.GenPart_mass[idx_Lep1_tr]
		self.pt_1_tr[0]  = entry.GenPart_pt[idx_Lep1_tr]
		self.m_2_tr[0]  = entry.GenPart_mass[idx_Lep2_tr]
		self.pt_2_tr[0]  = entry.GenPart_pt[idx_Lep2_tr]
		self.eta_1_tr[0] = entry.GenPart_eta[idx_Lep1_tr]
		self.eta_2_tr[0] = entry.GenPart_eta[idx_Lep2_tr]
		self.phi_1_tr[0] = entry.GenPart_phi[idx_Lep1_tr]
		self.phi_2_tr[0] = entry.GenPart_phi[idx_Lep2_tr]
		self.GenPart_statusFlags_1[0]    = entry.GenPart_statusFlags[idx_Lep1_tr]
		self.GenPart_status_1[0]    = entry.GenPart_status[idx_Lep1_tr]
		self.GenPart_statusFlags_2[0]    = entry.GenPart_statusFlags[idx_Lep2_tr]
		self.GenPart_status_2[0]    = entry.GenPart_status[idx_Lep2_tr]
        
        # MET variables
        self.met[0]         = entry.MET_pt    
        self.metphi[0]      = entry.MET_phi
        self.puppimet[0]    = entry.PuppiMET_pt
        self.puppimetphi[0] = entry.PuppiMET_phi
        
        self.metcov00[0] = entry.MET_covXX
        self.metcov01[0] = entry.MET_covXY
        self.metcov10[0] = entry.MET_covXY	
        self.metcov11[0] = entry.MET_covYY
	self.met_UnclX = entry.MET_MetUnclustEnUpDeltaX
	self.met_UnclY = entry.MET_MetUnclustEnUpDeltaY
        
        self.metpt_nom[0] = entry.MET_pt
        self.metphi_nom[0] =  entry.MET_phi
        if doUncertainties : 
            self.metpt_nom[0] = entry.MET_pt_nom
            self.metphi_nom[0] =  entry.MET_phi_nom
            if isMC : 
		self.metpt_JER[0] = entry.MET_pt_jer
		self.metphi_JER[0] = entry.MET_phi_jer
		self.metpt_JERUp[0] = entry.MET_pt_jerUp
		self.metphi_JERUp[0] = entry.MET_phi_jerUp
		self.metpt_JERDown[0] = entry.MET_pt_jerDown
		self.metphi_JERDown[0] = entry.MET_phi_jerDown
		self.metpt_JESUp[0] = entry.MET_pt_jesTotalUp
		self.metphi_JESUp[0] = entry.MET_phi_jesTotalUp
		self.metpt_JESDown[0] = entry.MET_pt_jesTotalDown
		self.metphi_JESDown[0] = entry.MET_phi_jesTotalDown
		self.metpt_UnclUp[0] = entry.MET_pt_unclustEnUp
		self.metphi_UnclUp[0] = entry.MET_phi_unclustEnUp
		self.metpt_UnclDown[0] = entry.MET_pt_unclustEnDown
		self.metphi_UnclDown[0] = entry.MET_phi_unclustEnDown


        # trig
	self.isTrig_1[0]   = is_trig_1
        self.isTrig_2[0]   = is_trig_2
	self.isDoubleTrig[0]   = is_Dtrig_1

        # jet variables
        leplist=[]
        leplist.append(LepP)
        leplist.append(LepM)
        if eL1.Pt()> 0 : leplist.append(eL1)
        if eL2.Pt()> 0 : leplist.append(eL2)

	for ic, isys in enumerate(sysVariations):  
	    #print 'passing in now ', ic, isys, sysVariations[ic]
	    jetList, bJetList, bJetListT, bJetListFlav = self.getJetsJMEMV(entry,leplist,era,isys) 

	    self.njets[ic] = len(jetList)
	    self.nbtag[ic] = len(bJetList)
	    self.nbtagT[ic] = len(bJetListT)

	    if isys !='' and '_' not in isys: isys="_"+isys
	    self.jpt_1[ic], self.jeta_1[ic], self.jphi_1[ic], self.jcsv_1[ic], self.jcsvfv_1[ic]= -9.99, -9.99, -9.99, -9.99, -9.99 
	    if len(jetList) > 0 :
		jpt1 = getattr(entry, "Jet_pt{0:s}".format(str(isys)), None)
		#print '============================ get syst now>', isys, jetList[0], len(jetList), jpt1, nJet30, len(bJetList), len(bJetListT)
		jj1 = jetList[0]
		self.jpt_1[ic]  = jpt1[jj1]
		self.jeta_1[ic] = entry.Jet_eta[jj1]
		self.jphi_1[ic] = entry.Jet_phi[jj1]
		self.jcsv_1[ic] = entry.Jet_btagDeepB[jj1]
		self.jcsvfv_1[ic] = entry.Jet_btagDeepFlavB[jj1]
		
		# genMatch jet1
		if isMC:
		    idx_genJet = entry.Jet_genJetIdx[jj1]
		    if idx_genJet >= 0:
			try :
			    self.jpt_1_tr[ic]  = entry.GenJet_pt[idx_genJet]
			    self.jeta_1_tr[ic] = entry.GenJet_eta[idx_genJet]
			    self.jphi_1_tr[ic] = entry.GenJet_phi[idx_genJet]
			except IndexError : pass

	    self.jpt_2[ic], self.jeta_2[ic], self.jphi_2[ic], self.jcsv_2[ic],self.jcsvfv_2[ic] = -9.99, -9.99, -9.99, -9.99, -9.99
	    if len(jetList) > 1 :
		jpt2 = getattr(entry, "Jet_pt{0:s}".format(str(isys)), None)
		jj2 = jetList[1] 
		self.jpt_2[ic]  = jpt2[jj2]
		self.jeta_2[ic] = entry.Jet_eta[jj2]
		self.jphi_2[ic] = entry.Jet_phi[jj2]
		self.jcsv_2[ic] = entry.Jet_btagDeepB[jj2]
		self.jcsvfv_2[ic] = entry.Jet_btagDeepFlavB[jj2]
		
		# genMatch jet2
		if isMC:
		    idx_genJet = entry.Jet_genJetIdx[jj2]
		    if idx_genJet >= 0:
			try: 
			   self.jpt_2_tr[ic]  = entry.GenJet_pt[idx_genJet]
			   self.jeta_2_tr[ic] = entry.GenJet_eta[idx_genJet]
			   self.jphi_2_tr[ic] = entry.GenJet_phi[idx_genJet]
			except IndexError : pass 

	    self.bpt_1[ic], self.beta_1[ic], self.bphi_1[ic], self.bcsv_1[ic], self.bcsvfv_1[ic] = -9.99, -9.99, -9.99, -9.99, -9.99
	    if len(bJetList) > 0 :
		jpt1 = getattr(entry, "Jet_pt{0:s}".format(str(isys)), None)
		jbj1 = bJetList[0]
		self.bpt_1[ic] = jpt1[jbj1]
		self.beta_1[ic] = entry.Jet_eta[jbj1]
		self.bphi_1[ic] = entry.Jet_phi[jbj1]
		self.bcsv_1[ic] = entry.Jet_btagDeepB[jbj1] 
		self.bcsvfv_1[ic] = entry.Jet_btagDeepFlavB[jbj1]
		
	    self.bpt_2[ic], self.beta_2[ic], self.bphi_2[ic], self.bcsv_2[ic], self.bcsvfv_2[ic] = -9.99, -9.99, -9.99, -9.99, -9.99
	    if len(bJetList) > 1 :
		jpt2 = getattr(entry, "Jet_pt{0:s}".format(str(isys)), None)
		jbj2 = bJetList[1] 
		self.bpt_2[ic] = jpt2[jbj2]
		self.beta_2[ic] = entry.Jet_eta[jbj2]
		self.bphi_2[ic] = entry.Jet_phi[jbj2]
		self.bcsv_2[ic] = entry.Jet_btagDeepB[jbj2]
		self.bcsvfv_2[ic] = entry.Jet_btagDeepFlavB[jbj2]

		# genMatch bjet1
		if isMC:
		    idx_genJet = entry.Jet_genJetIdx[jbj2]
		    if idx_genJet >= 0:
			try :
			    self.bpt_2_tr[ic]  = entry.GenJet_pt[idx_genJet]
			    self.beta_2_tr[ic] = entry.GenJet_eta[idx_genJet]
			    self.bphi_2_tr[ic] = entry.GenJet_phi[idx_genJet]
			except IndexError : pass
       
        if self.isTrig_1 !=0 : self.t.Fill()
        #self.t.Fill()
        return


    def setWeight(self,weight) :
        self.weight[0] = weight
        #print("outTuple.setWeight() weight={0:f}".format(weight))
        return
    def setWeightPU(self,weight) :
        self.weightPU[0] = weight
        #print("outTuple.setWeight() weight={0:f}".format(weight))
        return
    def setWeightPUtrue(self,weight) :
        self.weightPUtrue[0] = weight
        #print("outTuple.setWeight() weight={0:f}".format(weight))
        return

    def writeTree(self) :
        print("In outTuple.writeTree() entries={0:d}".format(self.entries)) 
        self.f.Write()
        self.f.Close()
        return

    


