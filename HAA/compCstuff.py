#########################
#Author: Sam Higginbotham
'''

* File Name : compCstuff.py

* Purpose :

* Creation Date : 26-05-2020

* Last Modified :

'''
#########################
import os
from ROOT import gInterpreter

gInterpreter.ProcessLine(".include .")
for baseName in ['../SVFit/MeasuredTauLepton','../SVFit/svFitAuxFunctions','../SVFit/FastMTT', '../HTT-utilities/RecoilCorrections/src/MEtSys', '../HTT-utilities/RecoilCorrections/src/RecoilCorrector'] : 
    if os.path.isfile("{0:s}_cc.so".format(baseName)) :
        gInterpreter.ProcessLine(".L {0:s}_cc.so".format(baseName))
    else :
        gInterpreter.ProcessLine(".L {0:s}.cc++".format(baseName))   
