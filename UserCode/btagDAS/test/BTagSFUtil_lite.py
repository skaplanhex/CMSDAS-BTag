
from ROOT import *


class BTagSFUtil:

    def __init__(self, seed=0):

        self.seed = seed
        self.rand = TRandom3(self.seed)

    def applySF( self, isBTagged, Btag_SF, Btag_eff):

        newBTag = isBTagged

        if Btag_SF == 1: return newBTag  #no correction needed

        #throw die
        coin = self.rand.Uniform(1.)

        if Btag_SF > 1:  #// use this if SF>1

            if not isBTagged:

                #//fraction of jets that need to be upgraded
                mistagPercent = (1.0 - Btag_SF) / (1.0 - (Btag_SF/Btag_eff) )

                #//upgrade to tagged
                if coin < mistagPercent: newBTag = True

        else:
                    
            #// use this if SF<1

            #//downgrade tagged to untagged
            if isBTagged and coin > Btag_SF: newBTag = False
                    
        return newBTag;

    def modifyBTagsWithSF( self, isBTagged, pdgIdPart, Btag_SF, Btag_eff, Bmistag_SF, Bmistag_eff):

        newBTag = isBTagged
        
        # b quarks and c quarks:
        if abs( pdgIdPart ) == 5 or  abs( pdgIdPart ) == 4:
            
            bctag_eff = Btag_eff;
            #if ( abs(pdgIdPart)==4 )  bctag_eff = Btag_eff/5.0; // take ctag eff as one 5th of Btag eff
            newBTag = self.applySF(isBTagged, Btag_SF, bctag_eff);
            
            # light quarks:
        elif abs( pdgIdPart )>0: #in data it is 0 (save computing time)

            newBTag = self.applySF(isBTagged, Bmistag_SF, Bmistag_eff)
            
        return newBTag

