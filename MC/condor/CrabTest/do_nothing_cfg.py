#########################
#Author: Sam Higginbotham
'''

* File Name : do_nothing_cfg.py

* Purpose :

* Creation Date : 10-03-2020

* Last Modified :

'''
#########################
import FWCore.ParameterSet.Config as cms
process = cms.Process("MAIN")

process.source = cms.Source("EmptySource")
