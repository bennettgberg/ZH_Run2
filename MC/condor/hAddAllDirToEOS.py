import sys
import glob
import os

files = glob.glob('*_2016')
#files = glob.glob('*_2016')
print("files={0:s}".format(str(files)))
for file in files :
    print("file={0:s} isDir={1}".format(file,os.path.isdir(file)))
    if not os.path.isdir(file) : continue
    os.chdir(file) 
    print("cwd={0:s}".format(os.getcwd()))
    #cmd = "python  ../hadnano2.py {0:s}.root *.ntup *.weights".format(file)
    #cmd = "hadd -f {0:s}.root *.ntup *.weights".format(file)
    cmd = "hadd -f {0:s}.root all*.root".format(file)
    print("cmd={0:s}".format(cmd))
    os.system(cmd) 
    #mv = "mv {0:s}.root /eos/user/s/shigginb/HAA_ntuples/March_2020/.".format(file)
    mv = "mv {0:s}.root /eos/user/s/shigginb/HAA_ntuples/SignalOnly/.".format(file)
    os.system(mv)
    os.chdir('..')


