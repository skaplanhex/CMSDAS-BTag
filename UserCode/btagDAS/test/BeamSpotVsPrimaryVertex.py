#! /usr/bin/env python
#
#
# Francisco Yumiceva
# yumiceva@fnal.gov
#
# Fermilab, 2010
#
#____________________________________________________________

import sys
import math
from array import array
from ROOT import *
print "loading FWLite libraries... ",
from DataFormats.FWLite import Events, Handle
print "done."

from PVFitter import Fit3D
gSystem.AddIncludePath(" -I$CMSSW_BASE/src/RecoVertex/BeamSpotProducer/interface")
#gSystem.AddIncludePath(" -I$CMSSW_BASE/src")

gROOT.ProcessLine(".L $CMSSW_BASE/src/RecoVertex/BeamSpotProducer/interface/BeamSpotFitPVData.h+")
#gROOT.ProcessLine(".L BSVectorDict.h+")
gROOT.ProcessLine(".L $CMSSW_BASE/src/RecoVertex/BeamSpotProducer/test/scripts/BSVectorDict.h+")
gROOT.ProcessLine(".L $CMSSW_BASE/src/RecoVertex/BeamSpotProducer/src/FcnBeamSpotFitPV.cc+")


def main():

    gROOT.SetStyle('Plain')

    outfilename = "BeamSpotVsPrimaryVertex_Data.root"
    outputroot = TFile( outfilename, "RECREATE")
        
    prefixFnal = 'dcache:/pnfs/cms/WAX/11'
    prefixCern = 'rfio:/castor/cern.ch/cms'
    prefixDesy = 'dcap://dcache-cms-dcap.desy.de/pnfs/desy.de/cms/tier2'
    prefix = prefixFnal


    N_maximum = 1000 # to run on all the events do -1
    
    # RECO or AOD files
    files = [
        '/store/data/Run2012C/BJetPlusX/AOD/PromptReco-v2/000/199/699/D428D9CC-EBD8-E111-97E7-BCAEC5364C42.root',
# The file immediately below no longer lives at FNAL! For users at FNAL, use the last file in the list for MC.
#         '/store/mc/Summer12_DR53X/QCD_Pt-50to80_MuEnrichedPt5_TuneZ2star_8TeV_pythia6/AODSIM/PU_S10_START53_V7A-v1/0000/9C43520A-26E7-E111-86DF-E0CB4E55363D.root'
#	'/store/user/skaplan/CMSDAS2014/QCD_MuEnriched_Events.root',
             ]
    
    fullpath_files = []
    
    for afile in files:
        fullpath_files.append( prefix+afile )
    
    events = Events ( fullpath_files)
    #print events.fileIndex
    #print events.secondaryFileIndex
    
    handleBSpot = Handle ("reco::BeamSpot")
    handlePV    = Handle ("vector<reco::Vertex>")
    
    labelBSpot = ("offlineBeamSpot")
    labelPV = ("offlinePrimaryVertices")

    histogram = {}

    histogram["N_PVs"] = TH1F("N_PVs","number of primary vertices",15,0,15)
    histogram["BSpot_x"] = TH1F("BSpot_x", "x [cm]", 150, -0.5, 0.5)
    histogram["PV_x"] = TH1F("PV_x","x [cm]", 150, -0.5, 0.5)
    histogram["delta_x"] = TH1F("delta_x","x_{bspot} - x_{PV}",150,-0.5,0.5)
    histogram["PVx_vs_PVy"] = TH2F("PVx_vs_PVy","PV x versus PV y",150,-0.5,0.5,150,-0.5,0.5)
    histogram["PVx_vs_PVy_vs_PVz"] = TH3F("PVx_vs_PVy_vs_PVz","X vs Y vs Z", 150,-0.5,0.5,150,-0.5,0.5,150,-9,9)
    
    # loop over events
    i = 0

    pvStore = vector(BeamSpotFitPVData)(0)
    
    for event in events:
        i = i + 1
        if i%10 == 0:
            print  "processing entry # " + str(i) + " from Run "+ str(event.eventAuxiliary().id().run()) + " lumi "+str(event.eventAuxiliary().id().luminosityBlock())

        if i==N_maximum: break
        
        ## Primary vertices
        event.getByLabel (labelPV, handlePV )
        PVs = handlePV.product()

        # loop over PVs
        thePV = PVs[0] # leading PV
        hasGoodPV = False
        for ipv in PVs:
            isfake = ipv.isFake()
            ndof = ipv.ndof()
            # this line crashes
            # apos = ipv.position()
            
            # check qualite
            if not hasGoodPV and not isfake and ipv.ndof()>4 and math.fabs(ipv.z()) < 24.:
            #and math.fabs(ipv.position().Rho())<2.0:
                hasGoodPV = True
                thePV = ipv
                pvdata = BeamSpotFitPVData()

                tmparray_pos = array('f')
                tmparray_posError = array('f')
                tmparray_posCorr = array('f')
                
                tmparray_pos.append( ipv.x() )
                tmparray_pos.append( ipv.y() )
                tmparray_pos.append( ipv.z() )
                tmparray_posError.append( ipv.xError() )
                tmparray_posError.append( ipv.yError() )
                tmparray_posError.append( ipv.zError() )
                tmparray_posCorr.append( ipv.covariance(0,1)/ipv.xError()/ipv.yError() )
                tmparray_posCorr.append( ipv.covariance(0,2)/ipv.xError()/ipv.zError() )
                tmparray_posCorr.append( ipv.covariance(1,2)/ipv.yError()/ipv.zError() )

                pvdata.position = tmparray_pos
                pvdata.posError = tmparray_posError
                pvdata.posCorr = tmparray_posCorr
                
                pvStore.push_back( pvdata )
                
        if not hasGoodPV: continue

        ## Beam spot
        event.getByLabel (labelBSpot, handleBSpot)
        spot = handleBSpot.product()

        #point = reco.BeamSpot.Point(1,1,1)
        #print point
        
        # fill histograms
        
        histogram["BSpot_x"].Fill( spot.x0() )
                                
        histogram["N_PVs"].Fill( len(PVs) )
        histogram["PV_x"].Fill( thePV.x() )
        histogram["PVx_vs_PVy"].Fill( thePV.x(), thePV.y() )
        histogram["PVx_vs_PVy_vs_PVz"].Fill( thePV.x(), thePV.y(), thePV.z() )
        histogram["delta_x"].Fill( spot.x0() - thePV.x() )
        
        
    # end loop over events

    results = Fit3D( pvStore ) # returns status, BeamSpot
    
    if results[0]:

        # get print function
        printFunc = getattr (results[1], 'print')
        ss = stringstream()
        printFunc(ss)
        print ss.str()
        
        #print "Results:"
        #print " X = " +str(results[1].x0() )
        #print "width X = " +str(results[1].BeamWidthX() )
                                
    outputroot.cd()

    
    for key in histogram.keys():
        histogram[key].Write()

    outputroot.Close()

if __name__ == '__main__':
    main()
