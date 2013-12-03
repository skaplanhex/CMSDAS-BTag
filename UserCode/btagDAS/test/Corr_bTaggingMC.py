#! /usr/bin/env python
#
# Simple script to extract the b-tagging discriminator and make
# MC efficiency plots.
#
# Francisco Yumiceva
# yumiceva@fnal.gov
#
# Fermilab, 2011
#
#____________________________________________________________

import sys
import math
import commands
from array import array
from ROOT import *
print "loading FWLite libraries... ",
from DataFormats.FWLite import Events, Handle
print "done."

def main():

    # if you want to run in batch mode
    #ROOT.gROOT.SetBatch()
    # maximum number of events. -1 run over all
    maxNevents = 500

    # Operating point
    bTagger = "simpleSecondaryVertexHighEffBJetTags" #"simpleSecondaryVertexHighEffBJetTags" "trackCountingHighEffBJetTags"
    tagAcronym = "SSVHE" #"TCHE"
    operating_point = 1.74 #3.3 #1.74 #1.7 # TCHEL (Loose)
    OPAcronym = "SSVHEM" #TCHEL"
    
    outfilename = "Corr_bTaggingMC_ttbar.root"
    outputroot = TFile( outfilename, "RECREATE")
        
    prefixFnal = 'dcache:/pnfs/cms/WAX/11'
    prefixCern = 'rfio:/castor/cern.ch/cms'
    prefix = prefixFnal

    # btag DB
    executableDB = "getbtagPerformance"
    rootDBFile = "rootFile=performanceDB.root"
    payload  = "payload=SYSTEM8SSVHEM"
    commandDB_b = executableDB + " " +rootDBFile+ " " +payload+ " " + "type=SF" + " "
    commandDB_l = executableDB + " " +rootDBFile+ " payload=MISTAGSSVHEM " + "type=SF" + " "

    # PAT ntuples from ttbar events
    files = ['/store/user/skhalil/TTJets_TuneD6T_7TeV-madgraph-tauola/shyft_387_v1/1bcebbd0f1a486aa7aaef10a50ee94bd/shyft_386_mc_9_1_S2t.root',\
             '/store/user/skhalil/TTJets_TuneD6T_7TeV-madgraph-tauola/shyft_387_v1/1bcebbd0f1a486aa7aaef10a50ee94bd/shyft_386_mc_99_1_qTf.root',\
             '/store/user/skhalil/TTJets_TuneD6T_7TeV-madgraph-tauola/shyft_387_v1/1bcebbd0f1a486aa7aaef10a50ee94bd/shyft_386_mc_98_1_bsC.root',\
             '/store/user/skhalil/TTJets_TuneD6T_7TeV-madgraph-tauola/shyft_387_v1/1bcebbd0f1a486aa7aaef10a50ee94bd/shyft_386_mc_97_1_GRg.root',\
             '/store/user/skhalil/TTJets_TuneD6T_7TeV-madgraph-tauola/shyft_387_v1/1bcebbd0f1a486aa7aaef10a50ee94bd/shyft_386_mc_96_1_tWt.root',\
             '/store/user/skhalil/TTJets_TuneD6T_7TeV-madgraph-tauola/shyft_387_v1/1bcebbd0f1a486aa7aaef10a50ee94bd/shyft_386_mc_95_1_IoX.root',\
             '/store/user/skhalil/TTJets_TuneD6T_7TeV-madgraph-tauola/shyft_387_v1/1bcebbd0f1a486aa7aaef10a50ee94bd/shyft_386_mc_94_1_chT.root',\
             '/store/user/skhalil/TTJets_TuneD6T_7TeV-madgraph-tauola/shyft_387_v1/1bcebbd0f1a486aa7aaef10a50ee94bd/shyft_386_mc_93_1_XZg.root',\
             '/store/user/skhalil/TTJets_TuneD6T_7TeV-madgraph-tauola/shyft_387_v1/1bcebbd0f1a486aa7aaef10a50ee94bd/shyft_386_mc_92_1_vXS.root',\
             '/store/user/skhalil/TTJets_TuneD6T_7TeV-madgraph-tauola/shyft_387_v1/1bcebbd0f1a486aa7aaef10a50ee94bd/shyft_386_mc_91_1_94n.root'\
             ]

    # PAT ntuples from QCD
    filesQCD = ['/store/user/srappocc/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/shyft_387_v1/2f94777c47687658400e9bd1c4f72c89/shyft_386_mc_9_1_fbm.root',\
             '/store/user/srappocc/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/shyft_387_v1/2f94777c47687658400e9bd1c4f72c89/shyft_386_mc_99_1_iBR.root',\
             '/store/user/srappocc/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/shyft_387_v1/2f94777c47687658400e9bd1c4f72c89/shyft_386_mc_7_1_qAV.root',\
             '/store/user/srappocc/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/shyft_387_v1/2f94777c47687658400e9bd1c4f72c89/shyft_386_mc_79_1_84s.root',\
             '/store/user/srappocc/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/shyft_387_v1/2f94777c47687658400e9bd1c4f72c89/shyft_386_mc_78_1_EAU.root',\
             '/store/user/srappocc/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/shyft_387_v1/2f94777c47687658400e9bd1c4f72c89/shyft_386_mc_77_1_V0y.root',\
             '/store/user/srappocc/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/shyft_387_v1/2f94777c47687658400e9bd1c4f72c89/shyft_386_mc_76_1_Uwt.root',\
             #'/store/user/srappocc/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/shyft_387_v1/2f94777c47687658400e9bd1c4f72c89/shyft_386_mc_75_1_9we.root',\
             #'/store/user/srappocc/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/shyft_387_v1/2f94777c47687658400e9bd1c4f72c89/shyft_386_mc_74_1_ozk.root',\
             #'/store/user/srappocc/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/shyft_387_v1/2f94777c47687658400e9bd1c4f72c89/shyft_386_mc_73_1_ma1.root',\
             #'/store/user/srappocc/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/shyft_387_v1/2f94777c47687658400e9bd1c4f72c89/shyft_386_mc_72_1_9Ay.root',\
             #'/store/user/srappocc/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/shyft_387_v1/2f94777c47687658400e9bd1c4f72c89/shyft_386_mc_71_1_mtQ.root',\
             #'/store/user/srappocc/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/shyft_387_v1/2f94777c47687658400e9bd1c4f72c89/shyft_386_mc_70_1_oBc.root',\
             '/store/user/srappocc/QCD_Pt-20_MuEnrichedPt-15_TuneZ2_7TeV-pythia6/shyft_387_v1/2f94777c47687658400e9bd1c4f72c89/shyft_386_mc_6_1_uy9.root'\
             ]
    
    fullpath_files = []
    
    for afile in files:
        fullpath_files.append( prefix+afile )
    
    events = Events ( fullpath_files)

    #handleJets = Handle ("vector<reco::PFJet>")
    handleJets = Handle ("vector<pat::Jet>")
    labelJets =  ("selectedPatJetsPFlow")

    histogram = {}

    histogram["jet_pt_"+OPAcronym] = TH1F("jet_pt_"+OPAcronym,"Jet p_{T} [GeV/c]", 50, 0, 200)
    histogram["Corr_jet_pt_"+OPAcronym] = TH1F("Corr_jet_pt_"+OPAcronym,"Jet p_{T} [GeV/c]", 50, 0, 200)
    histogram["Ntaggedjets_"+OPAcronym] = TH1F("Ntaggedjets_"+OPAcronym,"Number of tagged jets",5,0,5)
    histogram["Corr_Ntaggedjets_"+OPAcronym] = TH1F("Corr_Ntaggedjets_"+OPAcronym,"Number of tagged jets",5,0,5)
    
    for ih in histogram.keys():
        histogram[ih].Sumw2()
        histogram[ih].SetXTitle( histogram[ih].GetTitle() )
    
    # loop over events
    i = 0 # event counter
    
    for event in events:
        i = i + 1
        #if i%100 == 0:
        print  "processing entry # " + str(i) + " from Run "+ str(event.eventAuxiliary().id().run()) + " lumi "+str(event.eventAuxiliary().id().luminosityBlock())

        # check if maximum number of events was asked
        if maxNevents > 0 and maxNevents == i:
            print "Maximum number of events read "+str(maxNevents) 
            break
        
        event.getByLabel (labelJets, handleJets)
        # get the product
        jets = handleJets.product()

        Ntaggedjets = 0
        Ntaggedjets_weight = 1
        
        for ajet in jets:

            #histogram["jet_pt"].Fill( ajet.pt() )
                        
            disc = ajet.bDiscriminator( bTagger );

            if disc <= operating_point: continue

            flavor = math.fabs( ajet.partonFlavour() )

            aSF = 1.
            aSFerr = 0.
            
            if flavor == 5:
                output = commands.getstatusoutput( commandDB_b+"flavor=b"+" "+"pt="+str(ajet.pt())+" "+"eta="+str(math.fabs(ajet.eta())) )
                aSF = float( output[1].split()[2] )
                aSFerr = float( output[1].split()[4] )
                
            if flavor == 4:
                # charm
                output = commands.getstatusoutput( commandDB_b+"flavor=b"+" "+"pt="+str(ajet.pt())+" "+"eta="+str(math.fabs(ajet.eta())) )
                aSF = float( output[1].split()[2] )
                aSFerr = float( output[1].split()[4] )
                
            if flavor == 21 or ( flavor>0 and flavor<4):
                output = commands.getstatusoutput( commandDB_l+"flavor=l"+" "+"pt="+str(ajet.pt())+" "+"eta="+str(math.fabs(ajet.eta())) )
                aSF = float( output[1].split()[2] )
                aSFerr = float( output[1].split()[4] )
                

            if aSF == -100:
                aSF = 0
                aSFerr = 0
                print "no SF for jet with pt,eta = "+str( ajet.pt()) +", "+str( ajet.eta() )
                
            Ntaggedjets += 1
            Ntaggedjets_weight = Ntaggedjets_weight*aSF
                
            histogram["jet_pt_"+OPAcronym].Fill( ajet.pt() )
            histogram["Corr_jet_pt_"+OPAcronym].Fill( ajet.pt() , aSF )
                
                    
        # close jet loop
        histogram["Ntaggedjets_"+OPAcronym].Fill(Ntaggedjets)
        histogram["Corr_Ntaggedjets_"+OPAcronym].Fill(Ntaggedjets, Ntaggedjets_weight)
        
    # close loop over entries    
    outputroot.cd()

    # write histograms to file
    for key in histogram.keys():
        histogram[key].Write()

    outputroot.Close()

if __name__ == '__main__':
    main()
