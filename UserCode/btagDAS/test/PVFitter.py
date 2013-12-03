#! /usr/bin/env python

#import ROOT
from ROOT import *

import sys,os, math

from DataFormats.FWLite import Handle


# 3D fit
def Fit3D( pvStore ):

    errorScale_ = 0.9
    sigmaCut_ = 5.0
    
    fcn = FcnBeamSpotFitPV(pvStore)
    minuitx = TFitterMinuit()
    minuitx.SetMinuitFCN(fcn)
 
    # fit parameters: positions, widths, x-y correlations, tilts in xz and yz
    minuitx.SetParameter(0,"x",0.,0.02,-10.,10.)
    minuitx.SetParameter(1,"y",0.,0.02,-10.,10.)
    minuitx.SetParameter(2,"z",0.,0.20,-30.,30.)
    minuitx.SetParameter(3,"ex",0.015,0.01,0.,10.)
    minuitx.SetParameter(4,"corrxy",0.,0.02,-1.,1.)
    minuitx.SetParameter(5,"ey",0.015,0.01,0.,10.)
    minuitx.SetParameter(6,"dxdz",0.,0.0002,-0.1,0.1)
    minuitx.SetParameter(7,"dydz",0.,0.0002,-0.1,0.1)
    minuitx.SetParameter(8,"ez",1.,0.1,0.,30.)
    minuitx.SetParameter(9,"scale",errorScale_,errorScale_/10.,errorScale_/2.,errorScale_*2.)

    # first iteration without correlations
    ierr = 0
    minuitx.FixParameter(4)
    minuitx.FixParameter(6)
    minuitx.FixParameter(7)
    minuitx.FixParameter(9)
    minuitx.SetMaxIterations(100)
    #       minuitx.SetPrintLevel(3)
    minuitx.SetPrintLevel(0)
    minuitx.CreateMinimizer()
    ierr = minuitx.Minimize()
    if ierr == 1:
	print "3D beam spot fit failed in 1st iteration"
	return (False, fbeamspot)
    
    # refit with harder selection on vertices
    
    fcn.setLimits(minuitx.GetParameter(0)-sigmaCut_*minuitx.GetParameter(3),
		   minuitx.GetParameter(0)+sigmaCut_*minuitx.GetParameter(3),
		   minuitx.GetParameter(1)-sigmaCut_*minuitx.GetParameter(5),
		   minuitx.GetParameter(1)+sigmaCut_*minuitx.GetParameter(5),
		   minuitx.GetParameter(2)-sigmaCut_*minuitx.GetParameter(8),
		   minuitx.GetParameter(2)+sigmaCut_*minuitx.GetParameter(8));
    ierr = minuitx.Minimize();
    if ierr == 1:
	print "3D beam spot fit failed in 2nd iteration"
	return (False, fbeamspot)
    
    # refit with correlations
    
    minuitx.ReleaseParameter(4);
    minuitx.ReleaseParameter(6);
    minuitx.ReleaseParameter(7);
    ierr = minuitx.Minimize();
    if ierr == 1:
	print "3D beam spot fit failed in 3rd iteration"
	return (False, fbeamspot)

    # store results

    beamWidthX = minuitx.GetParameter(3);
    beamWidthY = minuitx.GetParameter(5);
    sigmaZ = minuitx.GetParameter(8);
    X = minuitx.GetParameter(0)
    Y = minuitx.GetParameter(1)
    Z = minuitx.GetParameter(2)
    dxdz = minuitx.GetParameter(6)
    dydz = minuitx.GetParameter(7)

    point = reco.BeamSpot.Point(X,Y,Z)
    
    beamWidthXerr = minuitx.GetParError(3);
    beamWidthYerr = minuitx.GetParError(5);
    sigmaZerr = minuitx.GetParError(8);
    Xerr = minuitx.GetParError(0)
    Yerr = minuitx.GetParError(1)
    Zerr = minuitx.GetParError(2)
    dxdzerr = minuitx.GetParError(6)
    dydzerr = minuitx.GetParError(7)

    matrix = reco.BeamSpot.CovarianceMatrix()
    
    matrix[0,0] = math.pow( minuitx.GetParError(0), 2)
    matrix[1,1] = math.pow( minuitx.GetParError(1), 2)
    matrix[2,2] = math.pow( minuitx.GetParError(2), 2)
    matrix[3,3] = sigmaZerr * sigmaZerr
    matrix[4,4] = math.pow( minuitx.GetParError(6), 2)
    matrix[5,5] = math.pow( minuitx.GetParError(7), 2)
    matrix[6,6] = beamWidthXerr * beamWidthXerr

    fbeamspot = reco.BeamSpot( point, sigmaZ, dxdz, dydz, beamWidthX, matrix)
    fbeamspot.setBeamWidthX( beamWidthX )
    fbeamspot.setBeamWidthY( beamWidthY )
                                    
    return (True, fbeamspot)






