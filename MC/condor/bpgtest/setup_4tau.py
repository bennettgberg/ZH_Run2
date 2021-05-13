#python 2 idk where it's at

#this script will take in the sample names from the file "bpgSamples.csv", and set up a different directory for each of them.
#  (by calling makeCondorsam.py for each sample name/location).


import os
import sys

def main():
    
    #submit jobs within this script (T) or just do the setup (F)
    submit_now = True

    #always delete current directory if it already exists?
    always_del = False

    year = 2017
    
    #number of root files to run in a single job
    nroot = 1 # 1

    #name for parent directory for all the new directories
    parent = "4tau_{}".format(year)
        
    inname = "bpgSamples.csv"
    infile = open(inname, "r")

    for line in infile:
        words = line.split(',')
        
        sample = words[6].strip() 

        #make the new directory
        #nickname of the sample
        samp_name = words[0].strip()
        
        #True if the files will be stored in my personal eos space, false otherwise.
        my_eos = False
        if "_M-" in samp_name:
            my_eos = True
        
        isMC = True
        if "data" in samp_name: isMC = False

        new_name = "%s/%s"%(parent, samp_name)
        new_sample = True
        if os.path.exists(new_name):
            new_sample = False
        else:
            os.system("mkdir -p %s"%(new_name) )
        #also make a directory on eos for it.
        eos_path = "/eos/uscms/store/user/bgreenbe/haa_4tau_%d/%s"%(year, samp_name)
        #MUST delete all prior contents in the eos directory if it already exists.
        #(this part not yet tested!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!)
        if os.path.exists(eos_path):
            if not always_del:
                cont = raw_input("Directory %s already exists. Delete all contents? (Y to delete and continue, N to cancel.) "%(eos_path))
                if cont not in ["Y", "y", "Yes", "yes"]:
                    sys.exit()
                else:
                    always_del = True
            os.system("rm %s/*.root"%(eos_path))
        os.system("eos root://cmseos.fnal.gov mkdir /store/user/bgreenbe/haa_4tau_%d/%s"%(year, samp_name))
        #run the setup code
        os.system("cd %s ; python ../../../makeCondorsam.py --dataSet %s --nickName %s --csv bpgSamples.csv --mode anaXRD --year %d -c %d -s HAA -g 0 -p /uscms/homes/b/bgreenbe/x509up_u52949 -l tcsh -tttt 0 -myeos %d -d %s\n"%(new_name, sample, samp_name, year, nroot, 1 if my_eos else 0, "MC" if isMC else "Data"))
        #come back to get ready for the next one.
        os.system("cd /uscms/homes/b/bgreenbe/work/CMSSW_10_2_9/src/ZH_Run2/MC/condor/bpgtest")
        #cp the submit_jobs file to the directory.
        #os.system("cp %s/submit_jobs.py %s"%(parent, new_name))
        os.system("sed \'s/nfiles = 5/nfiles = %d/\' %s/submit_jobs.py > %s/submit_jobs.py"%(nroot, parent, new_name))
        os.system("cp %s/mv_files.sh %s"%(parent, new_name))
        print("Directory %s created."%(new_name))
        
        #try to cp fileList.txt to cern eos (if it's a signal sample).
        if my_eos:
            #get mass of the signal sample
            mass = samp_name.split('-')[-1]
            print("command: scp %s/fileList.txt bgreenbe@lxplus.cern.ch:/eos/user/b/bgreenbe/HAA_ntuples/ggha01a01To4tau_%d_%s/"%(new_name, year, mass))
            os.system("scp %s/fileList.txt bgreenbe@lxplus.cern.ch:/eos/user/b/bgreenbe/HAA_ntuples/ggha01a01To4tau_%d_%s/"%(new_name, year, mass))
            #create the directory in eos for these files to be moved to
            os.system("eos root://cmseos.fnal.gov mkdir /store/user/bgreenbe/haa_4tau_%d/signal_M-%s"%(year, mass))
            #add signal sample to nAODv7
            os.system("python /uscms/homes/b/bgreenbe/work/CMSSW_10_2_9/src/ZH_Run2/MC/addPUhisto.py -f /uscms/homes/b/bgreenbe/work/CMSSW_10_2_9/src/ZH_Run2/MC/MC_%d_nAODv7.root -ch ZZZ -n HToAATo4Tau_M-%s"%(year, mass))
        elif new_sample:
            os.system("python /uscms/homes/b/bgreenbe/work/CMSSW_10_2_9/src/ZH_Run2/MC/addPUhisto.py -f /uscms/homes/b/bgreenbe/work/CMSSW_10_2_9/src/ZH_Run2/MC/MC_%d_nAODv7.root -ch ZZZ -n %s"%(year, samp_name)) 

        #submit the jobs now (if we're supposed to)
        if submit_now:
            os.system("cd %s; python submit_jobs.py"%(new_name))
            
if __name__=="__main__":
    main()

