#! /usr/bin/env python

class Item:

    def __init__(self):
        self.ptlow = 0.
        self.pthigh = 0.
        self.etalow = 0.
        self.etahigh = 0.
        self.value = 0.

class LOTable:

    def __init__(self):
        self.myItem = Item()
        self.thetable = []

    def LoadTable(self, filename):

        file = open(filename)

        for line in file:

            list = line.split()

            row = Item()
            row.ptlow = float(list[0])
            row.pthigh = float(list[1])
            row.etalow = float(list[2])
            row.etahigh = float(list[3])
            row.value = float(list[4])
            
            self.thetable.append( row )

        #print "read "+str(len(self.thetable)) +" lines"
        file.close()
        
    def GetValue( self, pt, eta):

        last_value = 0.
        #print str(pt)+" "+str(eta)
        
        for row in self.thetable:
            #print str(row.ptlow) + " " +str(row.value)
            last_value = row.value
            if row.ptlow <= pt and pt < row.pthigh and row.etalow <= eta and eta < row.etahigh:
                return row.value

        return last_value

