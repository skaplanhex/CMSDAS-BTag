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
from array import array
from ROOT import *
print "loading FWLite libraries... ",
from DataFormats.FWLite import Events, Handle
print "done."

def main():

    # if you want to run in batch mode
    #ROOT.gROOT.SetBatch()
    # maximum number of events. -1 run over all
    maxNevents = -1

    # Operating point
    bTagger = "combinedSecondaryVertexBJetTags" #"simpleSecondaryVertexHighEffBJetTags" "simpleSecondaryVertexHighEffBJetTags" "trackCountingHighEffBJetTags"
    tagAcronym = "CSV" # "SSVHE" "TCHE"
    operating_point = 0.679 # CSV (Medium) 1.74 #3.3 #1.74 #1.7 # TCHEL (Loose)
    OPAcronym = "CSVM" #"SSVHEM" # TCHEL"
    
    outfilename = "bTaggingMC_CSVM_ttbar.root"
#    outfilename = "bTaggingMC_CSVM_qcd.root"
    outputroot = TFile( outfilename, "RECREATE")
        
    prefixFnal = 'dcache:/pnfs/cms/WAX/11'
    prefixCern = 'rfio:/castor/cern.ch/cms'
    prefixPisa = '/gpfs/gpfsddn/cms/user/cmsdas/2012/btag/'
    prefixNaf = 'file:/nfs/dust/test/cmsdas/school86'
    prefix = prefixFnal

    # PAT ntuples from ttbar events
    files = [
        '/store/results/B2G/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/USER/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/0000/FEFD8AA1-5525-E211-B8C9-002618943915.root',
            ]

    # PAT ntuples from QCD
    filesQCD = [
    '/store/results/B2G/QCD_Pt_20_MuEnrichedPt_15_TuneZ2star_8TeV_pythia6/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/QCD_Pt_20_MuEnrichedPt_15_TuneZ2star_8TeV_pythia6/USER/StoreResults-Summer12_DR53X-PU_S10_START53_V7A-v1_TLBSM_53x_v2-c04f3b4fa74c8266c913b71e0c74901d/0000/FEF98E84-9629-E211-B812-00261894395A.root',
                ]
        
    fullpath_files = []
    
    for afile in files:
        fullpath_files.append( prefix+afile )
    
    events = Events ( fullpath_files)

    #handleJets = Handle ("vector<reco::PFJet>")
    handleJets = Handle ("vector<pat::Jet>")
    labelJets =  ("goodPatJetsPFlow")

    histogram = {}

    histogram["jet_pt"] = TH1F("jet_pt","Jet p_{T} [GeV/c]", 50, 0, 200)
    histogram["jet_pt_b"] = TH1F("jet_pt_b","Jet p_{T} [GeV/c]", 50, 0, 200)
    histogram["jet_pt_c"] = TH1F("jet_pt_c","Jet p_{T} [GeV/c]", 50, 0, 200)
    histogram["jet_pt_udsg"] = TH1F("jet_pt_udsg","Jet p_{T} [GeV/c]", 50, 0, 200)
    histogram["jet_pt_"+OPAcronym] = TH1F("jet_pt_"+OPAcronym,"Jet p_{T} [GeV/c]", 50, 0, 200)
    histogram["jet_pt_"+OPAcronym+"_b"] = TH1F("jet_pt_"+OPAcronym+"_b","Jet p_{T} [GeV/c]", 50, 0, 200)
    histogram["jet_pt_"+OPAcronym+"_c"] = TH1F("jet_pt_"+OPAcronym+"_c","Jet p_{T} [GeV/c]", 50, 0, 200)
    histogram["jet_pt_"+OPAcronym+"_udsg"] = TH1F("jet_pt_"+OPAcronym+"_udsg","Jet p_{T} [GeV/c]", 50, 0, 200)
    histogram["discriminator_"+tagAcronym] = TH1F("discriminator_"+tagAcronym, "Discriminator "+tagAcronym, 1500, -20, 20)
    histogram["discriminator_"+tagAcronym+"_b"] = TH1F("discriminator_"+tagAcronym+"_b","Discriminator "+tagAcronym+" b-jets",1500, -20, 20)
    histogram["discriminator_"+tagAcronym+"_c"] = TH1F("discriminator_"+tagAcronym+"_c","Discriminator "+tagAcronym+" c-jets",1500, -20, 20)
    histogram["discriminator_"+tagAcronym+"_udsg"] = TH1F("discriminator_"+tagAcronym+"_udsg","Discriminator "+tagAcronym+" udsg-jets",1500, -20, 20)
    histogram["Ntaggedjets_"+OPAcronym] = TH1F("Ntaggedjets_"+OPAcronym,"Number of tagged jets",5,0,5)
    
    for ih in histogram.keys():
        histogram[ih].Sumw2()
        histogram[ih].SetXTitle( histogram[ih].GetTitle() )
    
    # loop over events
    i = 0 # event counter
    
    for event in events:
        i = i + 1
        if i%100 == 0:
            print  "processing entry # " + str(i) + " from Run "+ str(event.eventAuxiliary().id().run()) + " lumi "+str(event.eventAuxiliary().id().luminosityBlock())

        # check if maximum number of events was asked
        if maxNevents > 0 and maxNevents == i:
            print "Maximum number of events read "+str(maxNevents) 
            break
        
        event.getByLabel (labelJets, handleJets)
        # get the product
        jets = handleJets.product()

        Ntaggedjets = 0
        
        for ajet in jets:

            if ajet.pt() < 30 or math.fabs( ajet.eta() ) > 2.4: continue
	    
            histogram["jet_pt"].Fill( ajet.pt() )

            disc = ajet.bDiscriminator( bTagger );
            flavor = math.fabs( ajet.partonFlavour() )
	    
	    histogram["discriminator_"+tagAcronym].Fill( disc )
	    if flavor == 5:
	       histogram["discriminator_"+tagAcronym+"_b"].Fill( disc )
	       histogram["jet_pt_b"].Fill( ajet.pt() )
	       
	    if flavor == 4:
	       histogram["discriminator_"+tagAcronym+"_c"].Fill( disc )
	       histogram["jet_pt_c"].Fill( ajet.pt() )
	       
	    if flavor == 21 or ( flavor>0 and flavor<4):
	       histogram["discriminator_"+tagAcronym+"_udsg"].Fill( disc )
	       histogram["jet_pt_udsg"].Fill( ajet.pt() )
	       
            if disc > operating_point:
                Ntaggedjets += 1
                
                histogram["jet_pt_"+OPAcronym].Fill( ajet.pt() )
                if flavor == 5:
                    histogram["jet_pt_"+OPAcronym+"_b"].Fill( ajet.pt() )
                if flavor == 4:
                    histogram["jet_pt_"+OPAcronym+"_c"].Fill( ajet.pt() )
                if flavor == 21 or ( flavor>0 and flavor<4):
                    histogram["jet_pt_"+OPAcronym+"_udsg"].Fill( ajet.pt() )
                                                                            
        # close jet loop
        histogram["Ntaggedjets_"+OPAcronym].Fill(Ntaggedjets)
        
    # close loop over entries    
    outputroot.cd()

    # write histograms to file
    for key in histogram.keys():
        histogram[key].Write()

    outputroot.Close()

if __name__ == '__main__':
    main()
