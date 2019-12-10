import tdrstyle
import CMS_lumi
from ROOT import gSystem, gStyle, gROOT, kTRUE
from ROOT import TCanvas, TH1D, TH1F, THStack, TFile, TPad, TLegend, TLatex, TLine, TAttMarker, TMarker
from ROOT import kBlack, kBlue, kMagenta, kOrange, kAzure, kRed
import array
import plotting


# cat = 'eeet', 'eemt', 'eett', 'mmet', 'mmmt', or 'mmtt'
# if cat = 'et', 'mt', or 'tt' plot Z->ee and Z->mumu combined
# if cat = 'all', plot combined ee+mm for each tau pair combination 

gROOT.SetBatch(kTRUE) # prevent displaying canvases


def getArgs() :
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","--verbose",default=0,type=int,help="Print level.")
    parser.add_argument("-f","--inFile",default='./allGroups_2017_OS_LT00.root',help="File to be analyzed.")
    #parser.add_argument("-y","--year",default=2017,type=int,help="Year for data.")
    #parser.add_argument("-l","--LTcut",default=0.,type=float,help="H_LTcut")
    #parser.add_argument("-s","--sign",default='OS',help="Opposite or same sign (OS or SS).")
    parser.add_argument("-c","--cat",default='all',help="Category")
    parser.add_argument("-w","--wait",default='wait',help="Wait for enter")
    parser.add_argument("-L","--setlog",default='yes',help="Set log scale")
    parser.add_argument("-u","--unBlind",default='yes',help="Unblind data")
    
    return parser.parse_args()



def applyStyle( h, fill, line, fillStyle) :
    h.SetFillColor(fill)
    h.SetLineColor(line)
    h.SetFillStyle(fillStyle)
    h.SetLineWidth(2)

def applySignalStyle(h) :
    h.SetLineWidth(3)
    h.SetFillColor(0)
    h.SetLineColor(kRed)
    h.SetLineStyle(2)
    h.SetMarkerSize(1.5);
    h.SetMarkerColor(kRed);



def applyDATAStyle(h) :
    #print("In applyDATAStyle: h={0:s} type(h)={1:s}".format(str(h),type(h)))
    h.SetMarkerStyle(20)
    h.SetMarkerSize(1.0)
    h.SetLineWidth(2)
    h.SetLineColor(kBlack)

def convertToDNDM( histo) :
    for i in range(1,histo.GetNbinsX(),1) :
	histo.SetBinContent(i,histo.GetBinContent(i)/histo.GetXaxis().GetBinWidth(i))
	histo.SetBinError(i,histo.GetBinError(i)/histo.GetXaxis().GetBinWidth(i))



groups = ['data','Rare','ZZ4L','Reducible','Signal']

plotSettings = { # [nBins,xMin,xMax,units]
        "pt_1":[100,0,500,"[Gev]","P_{T}(#tau_{1})"],
        "eta_1":[100,-4,4,"","#eta(l_{1})"],
        "phi_1":[100,-4,4,"","#phi(l_{1})"],
        "iso_1":[20,0,1,"","relIso(l_{1})"],
        "dz_1":[10,0,0.2,"[cm]","d_{z}(l_{1})"],
        "d0_1":[10,0,0.2,"[cm]","d_{xy}(l_{1})"],
        "q_1":[10,-5,5,"","charge(l_{1})"],

        "pt_2":[100,0,500,"[Gev]","P_{T}(l_{2})"],
        "eta_2":[100,-4,4,"","#eta(l_{2})"],
        "phi_2":[100,-4,4,"","#phi(l_{2})"],
        "iso_2":[20,0,1,"","relIso(l_{2})"],
        "dz_2":[10,0,0.2,"[cm]","d_{z}(l_{2})"],
        "d0_2":[10,0,0.2,"[cm]","d_{xy}(l_{2})"],
        "q_2":[10,-5,5,"","charge(l_{2})"],

        "njets":[10,-0.5,9.5,"","nJet"],
        #"Jet_pt":[100,0,500,"[GeV]","Jet P_{T}"], 
        #"Jet_eta":[64,-3.2,3.2,"","Jet #eta"],
        #"Jet_phi":[100,-4,4,"","Jet #phi"],
        #"Jet_ht":[100,0,800,"[GeV]","H_{T}"],

        "jpt_1":[100,0,500,"[GeV]","Jet^{1} P_{T}"], 
        "jeta_1":[64,-3.2,3.2,"","Jet^{1} #eta"],
        "jpt_2":[100,0,500,"[GeV]","Jet^{2} P_{T}"], 
        "jeta_2":[64,-3.2,3.2,"","Jet^{2} #eta"],

        "bpt_1":[100,0,500,"[GeV]","BJet^{1} P_{T}"], 
        "bpt_2":[100,0,500,"[GeV]","BJet^{2} P_{T}"], 

        #nbtag":[5,-0.5,4.5,"","nBTag"],
        #"nbtagLoose":[10,0,10,"","nBTag Loose"],
        #"nbtagTight":[5,0,5,"","nBTag Tight"],
        #"beta_1":[64,-3.2,3.2,"","BJet^{1} #eta"],
        #"beta_2":[64,-3.2,3.2,"","BJet^{2} #eta"],

        "met":[100,0,500,"[GeV]","#it{p}_{T}^{miss}"], 
        "met_phi":[100,-4,4,"","#it{p}_{T}^{miss} #phi"], 
        "puppi_phi":[100,-4,4,"","PUPPI#it{p}_{T}^{miss} #phi"], 
        "puppimet":[100,0,500,"[GeV]","#it{p}_{T}^{miss}"], 
        #"mt_tot":[100,0,1000,"[GeV]"], # sqrt(mt1^2 + mt2^2)
        #"mt_sum":[100,0,1000,"[GeV]"], # mt1 + mt2

        "m_vis":[40,50,130,"[Gev]","m(l^{+}l^{-})"],
        "ll_pt_p":[100,0,500,"[GeV]","P_{T}l^{-}"],
        "ll_phi_p":[100,-4,4,"","#phi(l_^{-})"],
        "ll_eta_p":[100,-4,4,"","#eta(l_^{-})"],
        "ll_pt_m":[100,0,500,"[GeV]","P_{T}l^{-}"],
        "ll_phi_m":[100,-4,4,"","#phi(l_^{-})"],
        "ll_eta_m":[100,-4,4,"","#eta(l_^{-})"],
        "ll_iso_1":[20,0,1,"","relIso(l_{1})"],
        "ll_iso_2":[20,0,1,"","relIso(l_{2})"],

        "H_vis":[100,0,500,"[Gev]","m(#tau#tau)"],
        "H_Pt":[100,0,500,"[GeV]","P_{T}(#tau#tau)"],
        "H_DR":[70,0,7,"","#Delta R(#tau#tau)"],
        "H_tot":[100,0,500,"[GeV]","m_{T}tot(#tau#tau)"],

        "TMass":[100,0,500,"[Gev]","m_{T}(#tau#tau)"],
        "Mass":[100,0,500,"[Gev]","m(#tau#tau)(SV)"],
        "AMass":[100,0,500,"[Gev]","m_{Z+H}(SV)"],
        #"CutFlowWeighted":[15,0.5,15.5,"","cutflow"],
        #"CutFlow":[15,0.5,15.5,"","cutflow"]

        "Z_Pt":[100,0,500,"[Gev]","P_T(l_{1}l_{2})"],
        "Z_DR":[100,0,500,"[Gev]","#Delta R(l_{1}l_{2})"]


}

def makeDiTauStack(outDir,inFile,rootDi,dndm = False, doRatio = False, year=2017, sign='OS', LTcut=0., cat='mmtt') :
    
    if args.unBlind.lower() == 'true' or args.unBlind.lower() == 'yes' : doRatio = True

    tdrstyle.setTDRStyle()

    writeExtraText = True       # if extra text
    extraText  = "Preliminary"  # default extra text is "Preliminary"
    lumi_sqrtS = "13 TeV"
    lumi_13TeV = cat+"   41.8 fb^{-1}, 2017"
    iPeriod = 5    # 1=7TeV, 2=8TeV, 3=7+8TeV, 7=7+8+13TeV 

    xR=0.65   #legend parameters
    xR=0.2    #legend parameters
    lg = TLegend(xR+0.45,0.55,xR+0.75,0.9)
    H = 600
    W = 600
    H_ref = 600
    W_ref = 600

    # references for T, B, L, R
    T = 0.08*H_ref
    B = 0.12*H_ref 
    L = 0.16*W_ref
    R = 0.04*W_ref

    #margins for inbetween the pads in a ratio plot
    B_ratio = 0.1*H_ref 
    T_ratio = 0.03*H_ref 

    #margin required for lebal on bottom of raito plot
    B_ratio_label = 0.3*H_ref 

    c = TCanvas('c1','c1',50,50,W,H)
    c.SetFillColor(0)
    c.SetBorderMode(0)
    c.SetFrameFillStyle(0)
    c.SetFrameBorderMode(0)

    if not doRatio :
       c.SetLeftMargin(L/W)
       c.SetRightMargin(R/W)
       c.SetTopMargin(T/H)
       c.SetBottomMargin(B/H)

    c.cd()
    setLog = False
    if args.setlog.lower() == 'yes' or args.setlog.lower() == 'true' : setLog = True 
    ratioPad = TPad("pad2","",0.0,0.0,1.0,0.29)
    plotPad = TPad("pad1","",0.0016,0.291,1.0,1.0)

    if doRatio :
	plotPad.SetTicks(0,0)
	plotPad.SetLeftMargin(L/W)
	plotPad.SetRightMargin(R/W)
	plotPad.SetTopMargin(T/H)
	plotPad.SetBottomMargin(B_ratio/H) 
	plotPad.SetFillColor(0)
	plotPad.SetBottomMargin(0.05)

	ratioPad.SetLeftMargin  (L/W)
	ratioPad.SetRightMargin (R/W)
	ratioPad.SetTopMargin   (T_ratio/H)
	ratioPad.SetTopMargin   (0.007)
	ratioPad.SetBottomMargin(B_ratio_label/H)
	ratioPad.SetGridy(1)
	ratioPad.SetFillColor(4000)

    else :
	plotPad = TPad("pad1","",0.0,0.03,1.0,1.0)
	plotPad.SetLeftMargin(L/W)
	plotPad.SetRightMargin(R/W)
	plotPad.SetTopMargin(T/H)
	plotPad.SetBottomMargin(B/H)
	
    if setLog : plotPad.SetLogy()
    c.cd()
    plotPad.Draw()
    if doRatio : ratioPad.Draw()
    plotPad.cd()
    print("In makeStack inFile={0:s}".format(inFile))
    f = TFile(inFile)


    histo = {}
    colors = {'data':0,'Reducible':kMagenta-10,'Rare':kBlue-8,'ZZ4L':kAzure-9,'Signal':kRed}
    for plotVar in plotSettings :
        histo[plotVar] ={}
        hsum ={}
        hs = THStack("hs","")
        f.cd()
        for group in groups :
            units = plotSettings[plotVar][3]
            labelX = plotSettings[plotVar][4]
            histo[plotVar][group] ={}
	    h_ = "h{0:s}_{1:s}_{2:s}".format(group,cat,plotVar)
            #print 'will try ', "h{0:s}_{1:s}_{2:s}".format(group,cat,plotVar)
            if 'CutFlow' in plotVar : 
	        if 'data' in group : h_ = "hCutFlow_{0:s}_data".format(cat)
	        else : h_ = "hCutFlow_{0:s}_{1:s}".format(cat,group)

            try : histo[plotVar][group] = f.Get(h_)
            except KeyError : continue
            #print histo[plotVar][group].GetName(), histo[plotVar][group].GetNbinsX()
            
            if dndm : convertToDNDM(histo[plotVar][group])
            if group == 'data' :
                try : applyDATAStyle(histo[plotVar][group])
                except KeyError : pass
            if group == 'Signal' :
                applySignalStyle(histo[plotVar][group])
            if group != 'data' and group != 'Signal' :
                applyStyle(histo[plotVar][group],colors[group],1,1001)
        
            if group != 'data' and group != 'Signal' : hs.Add(histo[plotVar][group]) 
            #if '_met' in plotVar : print '============', group, histo[plotVar][group].GetSumOfWeights()

        hMax = 10e+03+hs.GetMaximum()
	if not setLog : hMax = 300+hs.GetMaximum()
	hs.SetMinimum(0.)
        #if setLog : 
	#    hs.SetMaximum(10e+05*hs.GetMaximum())
        #else :     hs.SetMinimum(0.)
        hsum=hs.GetStack().Last()
	hsum.SetMinimum(0.)
	if setLog : hsum.SetMinimum(0.015)
        hsum.SetMaximum(hMax)
        if cat[:2] == 'ee': labelX = labelX.replace('l','e')
        if cat[:2] == 'mm' : labelX = labelX.replace('l','#mu')
        hsum.GetXaxis().SetTitleSize(0.045)
	if doRatio :
	    hsum.GetXaxis().SetLabelSize(0)
	    hsum.GetXaxis().SetTitle('')
	else :
	    if units!="" :
		hsum.GetXaxis().SetTitle(labelX+" "+units)
	    else :
		hsum.GetXaxis().SetTitle(labelX)

	try : hsum.GetYaxis().SetTitle("Events")
        except KeyError : pass

	if units !='' : 
	    binw = hsum.GetBinLowEdge(2) - hsum.GetBinLowEdge(1)
            un = units.replace('[','')
            un = un.replace(']','')
	    hsum.GetYaxis().SetTitle("Events / {0:.1f} {1:s}".format(binw,un))

	hsum.GetYaxis().SetTitleOffset(1.5)

	if dndm : hsum.GetYaxis().SetTitle("dN/d"+labelX)

	hsum.Draw("hist")
	hs.Draw("hist same")
	if doRatio : histo[plotVar]['data'].Draw("same ep hist")
	histo[plotVar]['Signal'].Draw("same e1 hist")

	if doRatio :
	    data2 = histo[plotVar]['data'].Clone("data")
	    mc = histo[plotVar]['Rare']
	    mc.Add(histo[plotVar]['Reducible'])
	    mc.Add(histo[plotVar]['ZZ4L'])
	    xmin = mc.GetXaxis().GetXmin()
	    xmax = mc.GetXaxis().GetXmax()
	    line = TLine(xmin,1.0,xmax,1.0)
	    line.SetLineWidth(1)
	    line.SetLineColor(kBlack)

	    #ratioPad.Draw()
	    ratioPad.cd()

	    data2.Divide(data2,mc)

	    data2.SetMarkerStyle(20)
	    data2.SetTitleSize(0.12,"Y")
	    data2.SetTitleOffset(0.40,"Y")
	    data2.SetTitleSize(0.12,"X")
	    data2.SetLabelSize(0.10,"X")
	    data2.SetLabelSize(0.08,"Y")
	    data2.GetYaxis().SetRangeUser(0.62,1.38)
	    data2.GetYaxis().SetNdivisions(305)
	    data2.GetYaxis().SetTitle("Obs/Exp   ")

	    if units!="" :
		data2.GetXaxis().SetTitle(labelX+" "+units)
	    else :
		data2.GetXaxis().SetTitle(labelX)

	    data2.Draw("P")
	    line.Draw()

	#c.cd()
	plotPad.cd()
	lg.Clear()
	for group in groups :
	    try :
		if group == 'data' : lg.AddEntry(histo[plotVar][group],group,"ple")
		elif group == 'Signal' : lg.AddEntry(histo[plotVar][group],group,"pl")
		else : lg.AddEntry(histo[plotVar][group],group,"f")
	    except KeyError :
		continue
	    
	lg.SetBorderSize(0)
	lg.SetFillColor(0)
	lg.SetFillStyle (0)
	lg.SetTextSize(0.04)
	lg.Draw("same")
        '''
	y_min, y_max = (plotting.GetPadYMin(plotPad), plotting.GetPadYMax(plotPad))
	if y_max == 0 : y_max = 100
	try :
	    plotting.FixBothRanges(plotPad, y_min if setLog else 0, 0.05 if setLog else 0, y_max, 0.25)
	    #plotting.FixTopRange(plotPad,plotting.GetPadYMax(plotPad), 0.15);
	    plotting.FixOverlay();
	except KeyError : pass
	'''

	lTex1 = TLatex(120.,0.97*hMax,'Preliminary {0:d}'.format(year))
	lTex1.SetTextSize(0.04) 
	#lTex1.Draw("same")
	signText = 'Same Sign'
	if sign == 'OS' : signText = 'Opposite Sign'
        
	lTex2 = TLatex(150., plotting.GetPadYMax(plotPad)+100,'{0:s}'.format(signText))
	#lTex2 = TLatex(150.,0.8*hMax,'{0:s}'.format(signText))
	#if setLog : lTex2 = TLatex(150.,hMax-10e+03,'{0:s}'.format(signText))
	lTex2.SetTextSize(0.04) 
	lTex2.Draw()
        CMS_lumi.CMS_lumi(c, iPeriod, 11)

	#plotting.FixBoxPadding(plotPad,plotPad, 0.01);


        plotPad.cd()
        plotPad.Update()
        plotPad.RedrawAxis()
        #frame = c.GetFrame()
        #frame.Draw()

	outFileBase = "Stack_{0:d}_{1:s}_{2:s}_{3:s}".format(year,cat,sign,plotVar) 
	if setLog : outFileBase = "Stack_{0:d}_{1:s}_{2:s}_{3:s}_log".format(year,cat,sign,plotVar) 
	c.SaveAs("./plots/{0:s}.png".format(outFileBase))
        #f.Close()
	#c.SaveAs("{0:s}.root".format(outFileBase))
    
    
if __name__ == '__main__':

#def makeDiTauStack(outDir,inFile,rootDir,s,labelX, units = "GeV",left=false,channel = "",
#                   json = "Golden",log = false,dndm=false, doRatio = false) :
    args = getArgs()
    inFileName = args.inFile
    year  = int(inFileName.split('_')[1])
    sign  = inFileName.split('_')[2]
    LTcut = float(inFileName.split('_')[3][2:4])

#   see comments on cat argument at top of file
    cats = { 1:'eeet', 2:'eemt', 3:'eett', 4:'eeem', 5:'mmet', 6:'mmmt', 7:'mmtt', 8:'mmem'}
    #cats = { 1:'eeet', 2:'mmmt'}
    #cats = { 1:'eeet'}
    #cats = { 1:'mmem'}

    if args.cat.lower() == 'all' :
        for cat in cats.values() :
            makeDiTauStack('.','{0:s}'.format(inFileName),'', False, False, year=year,sign=sign,LTcut=LTcut,cat=cat)
#def makeDiTauStack(outDir,inFile,rootDir,channel = "",  dndm = False, doRatio = False, year=2017, sign='OS', LTcut=0., cat='mmtt') :
        
   

