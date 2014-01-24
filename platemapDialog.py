# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 15:18:08 2014

@author: Solrisa
"""

from platemap_ui import *

class platemapDialog(QDialog):
    def __init__(self, parent=None, title='', folderpath=None):
        super(platemapDialog, self).__init__(parent)
        self.parent=parent
#        self.echem30=echem30axesWidget()
#        self.echem30.show()

        
        self.plotw_stack=plotwidget(self)
        self.plotw_stack.axes.set_xlabel('')
        self.plotw_stack.axes.set_ylabel('')
        self.plotw_stack.axes.set_aspect(1)

        
        self.plotw_plate=plotwidget(self)

        self.plotw_plate.axes.set_aspect(1)
        
        self.plotw_plate.fig.subplots_adjust(left=0, right=1)

        QObject.connect(self.plotw_plate, SIGNAL("genericclickonplot"), self.plateclickprocess)


        
        self.fileLineEdit=QLineEdit()        
        self.fileLineEdit.setText('')
        fileLineEditLabel=QLabel()
        fileLineEditLabel.setText('File:\n')
        fileLineEditlayout=QVBoxLayout()

        self.codesLineEdit=QLineEdit()        
        self.codesLineEdit.setText('0,10,20,30,40,50')
        codesLineEditLabel=QLabel()
        codesLineEditLabel.setText('only show these codes:\n')
        codesLineEditlayout=QVBoxLayout()

        ternstackComboBoxLabel=QLabel()
        ternstackComboBoxLabel.setText('Pseudo-tern\nstack wrt:')
        self.ternstackComboBox=QComboBox()
        self.ternstackComboBox.clear()
        for i, l in enumerate(['D', 'A', 'B', 'C']):
                self.ternstackComboBox.insertItem(i, l)
        self.ternstackComboBox.setCurrentIndex(0)
        QObject.connect(self.ternstackComboBox,SIGNAL("activated(QString)"),self.setupcomppermute)
        self.setupcomppermute(replot=False)
        compLineEditLabel=QLabel()
        compLineEditLabel.setText('Composition:\n use the order in the data files\n(as in a,b,c,d)')
        self.compLineEdit=QLineEdit()
        self.compLineEdit.setText('0.5,0.4,0.1,0.0')
        
        
        xyLineEditLabel=QLabel()
        xyLineEditLabel.setText('x,y position:')
        self.xyLineEdit=QLineEdit()
        self.xyLineEdit.setText('5.45, 6.33')
        
        sampleLineEditLabel=QLabel()
        sampleLineEditLabel.setText('Sample No(s).:')
        self.sampleLineEdit=QLineEdit()
        self.sampleLineEdit.setText('254')


        addFile=QPushButton()
        addFile.setText("select\nfile")
        QObject.connect(addFile, SIGNAL("pressed()"), self.openAddFile)
        
        addComp=QPushButton()
        addComp.setText("add")
        QObject.connect(addComp, SIGNAL("pressed()"), self.addValuesComp)
        
        remComp=QPushButton()
        remComp.setText("remove")
        QObject.connect(remComp, SIGNAL("pressed()"), self.remValuesComp)
        
        addxy=QPushButton()
        addxy.setText("add")
        QObject.connect(addxy, SIGNAL("pressed()"), self.addValuesXY)
        
        remxy=QPushButton()
        remxy.setText("remove")
        QObject.connect(remxy, SIGNAL("pressed()"), self.remValuesXY)

        addSample=QPushButton()
        addSample.setText("add")
        QObject.connect(addSample, SIGNAL("pressed()"), self.addValuesSample)

        
        remSample=QPushButton()
        remSample.setText("remove")
        QObject.connect(remSample, SIGNAL("pressed()"), self.remValuesSample)

        savesampleButton=QPushButton()
        savesampleButton.setText("save select\nsample IDs")
        QObject.connect(savesampleButton, SIGNAL("pressed()"), self.writesamplelist)
        


        self.ctrlgriditems=[\
        (fileLineEditLabel, self.fileLineEdit, 0, 0),\
        (codesLineEditLabel, self.codesLineEdit, 1, 0),\
        (compLineEditLabel, self.compLineEdit, 2, 0), \
        (xyLineEditLabel, self.xyLineEdit, 3, 0),\
        (sampleLineEditLabel, self.sampleLineEdit, 4, 0),\
        ]
        
        mainlayout=QGridLayout()
        ctrllayout=QGridLayout()
        for labw, spw, i, j in self.ctrlgriditems:
            templayout=QHBoxLayout()
            templayout.addWidget(labw)
            templayout.addWidget(spw)
            ctrllayout.addLayout(templayout, i, j)
        
        ctrllayout.addWidget(addFile, 0, 1)
        #ctrllayout.addWidget(savesampleButton, 0, 2) don't have save yet, just copy text
        ctrllayout.addWidget(ternstackComboBoxLabel, 1, 1)
        ctrllayout.addWidget(self.ternstackComboBox, 1, 2)
        ctrllayout.addWidget(addComp, 2, 1)
        ctrllayout.addWidget(remComp, 2, 2)
        ctrllayout.addWidget(addxy, 3, 1)
        ctrllayout.addWidget(remxy, 3, 2)
        ctrllayout.addWidget(addSample, 4, 1)
        ctrllayout.addWidget(remSample, 4, 2)

        
        self.browser = QTextBrowser()
#        self.lineedit = self.addValuesComp
#        self.lineedit = QLineEdit("Type an expression and press Enter")
#        self.lineedit.selectAll()
#        self.connect(self.lineedit, SIGNAL("returnPressed()"),self.updateUi)


        
        mainlayout.addLayout(ctrllayout, 0, 0, 1, 2)

        mainlayout.addWidget(self.browser, 0, 2)
        #mainlayout.addWidget(self.lineedit, 1,2,1,1)

        mainlayout.addWidget(self.plotw_plate, 2, 1)
        mainlayout.addWidget(self.plotw_stack, 2, 2)        
        
        pylab.figure()
        self.quat=QuaternaryPlot(pylab.gca())
        
        self.setLayout(mainlayout)
        self.resize(1600, 750)
        
        self.linefields=[('%d', 'Sample'), ('%.2f', 'x'), ('%.2f', 'y'), ('%.2f', 'A'), ('%.2f', 'B'), ('%.2f', 'C'), ('%.2f', 'D'), ('%d', 'code')]
        
        
    def extractlist_dlistkey(self, k):
        return [d[k] for d in self.platemapdlist]
        
    def plot(self): #self.platemapselectinds


        self.plotw_plate.axes.cla()
        
        s_plate=20
        
        #xy plot
        self.plotw_plate.axes.scatter(self.x, self.y, c=self.col, s=s_plate, marker='s', edgecolor='none')
        
        for i in self.platemapselectinds:
            circ = pylab.Circle((self.x[i], self.y[i]), radius=1, edgecolor='r', facecolor='none')
            self.plotw_plate.axes.add_patch(circ)
        
        self.plotw_plate.axes.set_xlim(min(self.x)-3, max(self.x)+3)
        self.plotw_plate.axes.set_ylim(min(self.y)-3, max(self.y)+3)
        
        self.plotw_plate.fig.canvas.draw()
        
        #comp plot
        #self.plotw_stack.fig.clf()
        fom=['k']*len(self.comp)
        for i in self.platemapselectinds:
            fom[i]='r'
        fom=numpy.array(fom)
        permcomp=self.comp[:, self.comppermuteinds]
        self.stackplotfcn(permcomp, fom, self.plotw_stack_stpl, s=8)
        
        
        self.plotw_stack.fig.canvas.draw()
        #browser text
        headline='\t'.join([k for fmtstr, k in self.linefields])
        selectsamplesstr='\n'.join([headline]+self.selectsamplelines)
        
        self.browser.setText(selectsamplesstr)

    

    def plateclickprocess(self, coords_button):
        if len(self.x)==0:
            return
        critdist=2.
        xc, yc, button=coords_button

        dist=((self.x-xc)**2+(self.y-yc)**2)**.5
        if min(dist)<critdist:
            self.selectind=numpy.argmin(dist)
            self.plotselect()

        if button==3:#right click
            self.addtoselectsamples()
        elif button==2:#center click
            self.remfromselectsamples()
            
    def plotselect(self):
        self.compLineEdit.setText(','.join(['%.2f' %n for n in self.comp[self.selectind]]))

        self.xyLineEdit.setText(','.join(['%.2f' %n for n in [self.x[self.selectind], self.y[self.selectind]]]))

        self.sampleLineEdit.setText('%d' %self.platemapdlist[self.selectind]['Sample'])

    def sampleline_ind(self):
        d=self.platemapdlist[self.selectind]
        return '\t'.join([fmtstr %d[k] for fmtstr, k in self.linefields])
        
    def addtoselectsamples(self):# self.selectind
        if self.selectind in self.platemapselectinds:
            return
        self.platemapselectinds+=[self.selectind]
        self.selectsamplelines+=[self.sampleline_ind()]
        self.plot()#would be nice to only have to plot overlay of selected samples
    
    def setupcomppermute(self, replot=True):
        i=self.ternstackComboBox.currentIndex()
        self.ellabels=['A', 'B', 'C', 'D', 'A', 'B', 'C'][i:i+4]
        self.comppermuteinds=[0, 1, 2, 3, 0, 1, 2][i:i+4]
        print '**********', self.comppermuteinds
        print replot
        if replot:
            self.stackedplotsetup()
            self.plot()
            print 'updated'
    
    def remfromselectsamples(self):# self.selectind
        if not self.selectind in self.platemapselectinds:
            return
        i=self.platemapselectinds.index(self.selectind)
        self.platemapselectinds.pop(i)
        self.selectsamplelines.pop(i)
        self.plot()#would be nice to only have to plot overlay of selected samples
    
    def stackedplotsetup(self):
        a=numpy.sort(self.comp[:,0])
        adiff=(a[1:]-a[:-1])
        adiff=(adiff[adiff>.001]).mean()
        nints=(1./adiff).round()
        intervopts=[5, 10, 20, 30]
        intervchoice=intervopts[numpy.argmin((nints-numpy.array(intervopts))**2)]
        #print 'difference in A channel,  number of a intervals per 100% and stacked plot choice are:',  adiff, nints, intervchoice
        if intervchoice==5:
            makefcn=make5ternaxes
            self.stackplotfcn=scatter_5axes
        elif intervchoice==10:
            makefcn=make10ternaxes
            self.stackplotfcn=scatter_10axes
        elif intervchoice==20:
            makefcn=make20ternaxes
            self.stackplotfcn=scatter_20axes
        elif intervchoice==30:
            makefcn=make30ternaxes
            self.stackplotfcn=scatter_30axes
            
        self.plotw_stack.fig.clf()
        self.plotw_stack_axl, self.plotw_stack_stpl=makefcn(fig=self.plotw_stack.fig, ellabels=self.ellabels)
        print self.ellabels
        
    def openAddFile(self):
        p=mygetopenfile(parent=self, markstr='select platemap .txt')
        if p is None or p=='':
            return
        self.fileLineEdit.setText(p)

        self.platemapdlist=readsingleplatemaptxt(p)
        
        codesstr=str(self.codesLineEdit.text())
        self.filterbycodes=eval('['+codesstr+']')
        self.platemapdlist=[d for d in self.platemapdlist if d['code'] in self.filterbycodes]
        for d in self.platemapdlist:
            d['comp']=numpy.array([d[k] for k in ['A', 'B', 'C', 'D']])
            d['col']=self.quat.rgb_comp([d['comp']])[0]
            
        self.x=numpy.array(self.extractlist_dlistkey('x'))
        self.y=numpy.array(self.extractlist_dlistkey('y'))
        self.col=numpy.array(self.extractlist_dlistkey('col'))
        self.comp=numpy.array(self.extractlist_dlistkey('comp'))
        self.smplist=self.extractlist_dlistkey('Sample')
        
        self.stackedplotsetup()
        
        
        self.platemapselectinds=[]
        self.selectsamplelines=[]
        self.plot()
        
    def addValuesSample(self, remove=False):
        sampleNostr = str(self.sampleLineEdit.text())

        try:
            if ',' in sampleNostr:
                sampleNolist=eval('['+sampleNostr+']')
                inds=[self.smplist.index(n) for n in sampleNolist if n in self.smplist]
            else:
                sampleNo=int(eval(sampleNostr.strip()))
                inds=[self.smplist.index(sampleNo)]
        except:
            print 'error adding samples'
            return
        for i in inds:
            self.selectind=i
            if remove:
                self.remfromselectsamples()
            else:
                self.addtoselectsamples()
#            if a == sampleNo:
#                self.browser.append(line)
#        print sampleNo
#        return sampleNo
    
    def remValuesSample(self):
        self.addValuesSample(remove=True)
        
    def addValuesComp(self, remove=False):
        compstr = str(self.compLineEdit.text())
        try:
            abcd=numpy.array(eval('['+compstr.strip()+']'))
            if abcd.sum()<=0.:
                raise
            abcd/=abcd.sum()
            i=numpy.argmin(numpy.array([((comp-abcd)**2).sum() for comp in self.comp]))
        except:
            print 'error adding samples'
            return
        self.selectind=i
        if remove:
            self.remfromselectsamples()
        else:
            self.addtoselectsamples()
        
#        try:
#            s=unicode(self.compLineEdit.text())
#            self.browser.append("%s = <b>%s</b>" % (s, eval('['+s+']')))
#        except:
#            self.browser.append("<font color=red>%s is invalid!</font>" %s)
#            print 'Need to write a set of compositions'
    def remValuesComp(self):
        self.addValuesComp(remove=True)
#        try:
#            s=unicode(self.compLineEdit.text())
#            print "try"
#            self.browser.cut(s)
#        except:
#            print 'Need to write a set of x&y coordinates'
    def addValuesXY(self, remove=False):
        xystr = str(self.xyLineEdit.text())
        try:
            xy=numpy.array(eval('['+xystr.strip()+']'))
            i=numpy.argmin(numpy.array([((numpy.array([x, y])-xy)**2).sum() for x, y in zip(self.x, self.y)]))
        except:
            print 'error adding samples'
            return
        self.selectind=i
        if remove:
            self.remfromselectsamples()
        else:
            self.addtoselectsamples()
#        try:
#            xy=unicode(self.xyLineEdit.text())
#            self.browser.append("%s = <b>%s</b>" % (xy, eval('['+xy+']')))
#        except:
#            self.browser.append("<font color=red>%s is invalid!</font>" %s)
#            print 'Need to write a set of x&y coordinates'
            
    def remValuesXY(self):
        self.addValuesXY(remove=True)
#        try:
#            xy=unicode(self.xyLineEdit.text())
#            self.browser.clear(xy)
#        except:
#            print 'Need to write a set of x&y coordinates'
            
        
    def writesamplelist(self, p=None):#not implemented yet
        self.statusLineEdit.setText('writing file')
        idstr=str(self.selectsamplesLineEdit.text()).split(',')
        try:
            ids=[int(myeval(s.strip())) for s in idstr]
        except:
            print 'data conversion problem for this list of strings:', idstr
            return
        if len(ids)==0:
            print 'no data to save'
            return

        if p is None:
            p=mygetsavefile(parent=self, markstr='save spreadsheet string', filename=os.path.split(self.folderpath)[1]+'_'+explab+'.txt' )
        elif os.path.isdir(p):
            p=os.path.join(p, os.path.split(self.folderpath)[1]+'_'+explab+'.txt')
            print p
        if not p:
            print 'save aborted'
            return
        ids=list(set(ids))
        ids.sort()
        savestr='\n'.join([`n` for n in ids])
        
        f=open(p, mode='w')
        f.write(savestr)
        f.close()
        

class MainMenu(QMainWindow):
    def __init__(self, previousmm, execute=True, **kwargs):#, TreeWidg):
        super(MainMenu, self).__init__(None)
        #self.setupUi(self)
        self.setWindowTitle('PlateMap Visualization')
        self.di=platemapDialog(self, **kwargs)
        if execute:
            self.di.exec_()

def readsingleplatemaptxt(p, returnfiducials=False):
    f=open(p, mode='r')
    ls=f.readlines()
    f.close()
    if returnfiducials:
        s=ls[0].partition('=')[2].partition('mm')[0].strip()
        if not ',' in s[s.find('('):s.find(')')]: #needed because sometimes x,y in fiducials is comma delim and sometimes not
            print 'WARNING: commas inserted into fiducials line to adhere to format.'
            print s
            s=s.replace('(   ', '(  ',).replace('(  ', '( ',).replace('( ', '(',).replace('   )', '  )',).replace(',  ', ',',).replace(', ', ',',).replace('  )', ' )',).replace(' )', ')',).replace('   ', ',',).replace('  ', ',',).replace(' ', ',',)
            print s
        fid=eval('[%s]' %s)
        fid=numpy.array(fid)
    for count, l in enumerate(ls):
        if not l.startswith('%'):
            break
    keys=ls[count-1][1:].split(',')
    keys=[(k.partition('(')[0]).strip() for k in keys]
    dlist=[]
    for l in ls[count:]:
        sl=l.split(',')
        d=dict([(k, myeval(s.strip())) for k, s in zip(keys, sl)])
        dlist+=[d]
    if returnfiducials:
        return dlist, fid
    return dlist
