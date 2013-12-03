#! /usr/bin/env python
#  Simple example to make an Efficiency vs Mistag plot from the discriminator histogram
#
#  A. Rizzi 2012
#____________________________________________________________

import sys
import math
from array import array
from ROOT import *

def makeEffVsMistagTGraph(inputfilename):

    file = TFile(inputfilename)
    histo_b = file.Get("discriminator_CSV_b")
    histo_udsg = file.Get("discriminator_CSV_udsg")
    
    b_eff = array('f')
    udsg_eff = array('f')
    tot_b= histo_b.GetEntries()
    tot_udsg= histo_udsg.GetEntries()

    print "Total number of jets: "
    print tot_b," b-jets "
    print tot_udsg," light jets "

    b_abovecut = 0
    udsg_abovecut =   0 

    for i in xrange(1501,-1,-1)  :   # from 1501 to 0, in steps of "-1"
      b_abovecut += histo_b.GetBinContent(i)
      udsg_abovecut += histo_udsg.GetBinContent(i)
      b_eff.append(b_abovecut/tot_b)
      udsg_eff.append(udsg_abovecut/tot_udsg)
    
    return TGraph(1500, b_eff, udsg_eff)

def main():
    c = TCanvas()
    c.SetLogy(1)
    c.SetGridy(1)
    c.SetGridx(1)
    g =  makeEffVsMistagTGraph("bTaggingMC_CSVM_ttbar.root")
    g.SetLineColor(2)	
#    g_qcd =  makeEffVsMistagTGraph("bTaggingMC_CSVM_qcd.root")
    g.Draw("ALP")
#    g_qcd.Draw("LP")
    g.GetXaxis().SetTitle("b efficiency")
    g.GetYaxis().SetTitle("udsg mistag rate")
    c.SaveAs("output_qcd.png")
    sys.stdin.readline()

if __name__ == '__main__':
    main()
