#! /usr/bin/env python

from ROOT import *

import sys
import os
import math

gROOT.SetStyle("Plain")

tagAcronym = "CSV" #"SSVHE" #"TCHE"
OPAcronym = "CSVM" #"SSVHEM" #"TCHEM"

inputfile = TFile("bTaggingMC_CSVM_ttbar.root")
outputfile = TFile("results_bTaggingMC_"+OPAcronym+"_ttbar.root", "RECREATE")

inputfile.cd()

histogram = {}

histogram["jet_pt"] = gDirectory.Get("jet_pt")
histogram["jet_pt_b"] = gDirectory.Get("jet_pt_b")
histogram["jet_pt_c"] = gDirectory.Get("jet_pt_c")
histogram["jet_pt_udsg"] = gDirectory.Get("jet_pt_udsg")
histogram["jet_pt_"+OPAcronym] = gDirectory.Get("jet_pt_"+OPAcronym)
histogram["jet_pt_"+OPAcronym+"_b"] = gDirectory.Get("jet_pt_"+OPAcronym+"_b")
histogram["jet_pt_"+OPAcronym+"_c"] = gDirectory.Get("jet_pt_"+OPAcronym+"_c")
histogram["jet_pt_"+OPAcronym+"_udsg"] = gDirectory.Get("jet_pt_"+OPAcronym+"_udsg")
histogram["discriminator_"+tagAcronym] = gDirectory.Get("discriminator_"+tagAcronym)
histogram["discriminator_"+tagAcronym+"_b"] = gDirectory.Get("discriminator_"+tagAcronym+"_b")
histogram["discriminator_"+tagAcronym+"_c"] = gDirectory.Get("discriminator_"+tagAcronym+"_c")
histogram["discriminator_"+tagAcronym+"_udsg"] = gDirectory.Get("discriminator_"+tagAcronym+"_udsg")

newhistogram = {}

newhistogram["eff_"+OPAcronym+"_b"] = histogram["jet_pt_"+OPAcronym+"_b"].Clone("eff_"+OPAcronym+"_b")
newhistogram["eff_"+OPAcronym+"_c"] = histogram["jet_pt_"+OPAcronym+"_c"].Clone("eff_"+OPAcronym+"_c")
newhistogram["eff_"+OPAcronym+"_udsg"] = histogram["jet_pt_"+OPAcronym+"_udsg"].Clone("eff_"+OPAcronym+"_udsg")

for ih in newhistogram.keys():
    newhistogram[ih].Reset()


newhistogram["eff_"+OPAcronym+"_b"].Divide( histogram["jet_pt_"+OPAcronym+"_b"], histogram["jet_pt_b"], 1., 1.,"B")
newhistogram["eff_"+OPAcronym+"_c"].Divide( histogram["jet_pt_"+OPAcronym+"_c"], histogram["jet_pt_c"], 1., 1.,"B")
newhistogram["eff_"+OPAcronym+"_udsg"].Divide( histogram["jet_pt_"+OPAcronym+"_udsg"], histogram["jet_pt_udsg"], 1., 1.,"B")


canvas = {}

canvas["discriminator"] = TCanvas("discriminator","discriminator",700,700)

histogram["discriminator_"+tagAcronym+"_c"].Add(histogram["discriminator_"+tagAcronym+"_udsg"])
histogram["discriminator_"+tagAcronym+"_b"].Add(histogram["discriminator_"+tagAcronym+"_c"])

histogram["discriminator_"+tagAcronym+"_udsg"].SetFillColor(ROOT.kRed)
histogram["discriminator_"+tagAcronym+"_c"].SetFillColor(ROOT.kYellow)
histogram["discriminator_"+tagAcronym+"_b"].SetFillColor(ROOT.kBlue)

histogram["discriminator_"+tagAcronym].Draw()
histogram["discriminator_"+tagAcronym+""].Draw("histogram same")
histogram["discriminator_"+tagAcronym+"_b"].Draw("histogram same")
histogram["discriminator_"+tagAcronym+"_c"].Draw("histogram same")
histogram["discriminator_"+tagAcronym+"_udsg"].Draw("histogram same")
gPad.SetLogy()

canvas["eff_"+OPAcronym+"_b"] = TCanvas("Eff_"+OPAcronym+"_b","Eff_"+OPAcronym+"_b",400,400)
newhistogram["eff_"+OPAcronym+"_b"].Draw("pe")
gPad.SetGrid()

canvas["eff_"+OPAcronym+"_c"] = TCanvas("Eff_"+OPAcronym+"_c","Eff_"+OPAcronym+"_c",400,400)
newhistogram["eff_"+OPAcronym+"_c"].Draw("p")
gPad.SetGrid()

canvas["eff_"+OPAcronym+"_udsg"] = TCanvas("Eff_"+OPAcronym+"_udsg","Eff_"+OPAcronym+"_udsg",400,400)
newhistogram["eff_"+OPAcronym+"_udsg"].Draw("p")
gPad.SetGrid()


outputfile.cd()
for key in newhistogram.keys():
    newhistogram[key].Write()
    
raw_input ("Enter to quit:")



