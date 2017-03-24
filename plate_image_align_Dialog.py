import matplotlib.image as mpimg

from platemap_ui import *

class plateimagealignDialog(QDialog):
    def __init__(self, parent=None, title='', folderpath=None):
        super(plateimagealignDialog, self).__init__(parent)
        self.parent=parent
#        self.echem30=echem30axesWidget()
#        self.echem30.show()

        
        self.plotw_motimage=plotwidget(self)
        self.plotw_motimage.axes.set_xlabel('motor x')
        self.plotw_motimage.axes.set_ylabel('motor y')
        self.plotw_motimage.axes.set_aspect(1)

        
        self.plotw_plate=plotwidget(self)

        self.plotw_plate.axes.set_aspect(1)
        
        self.plotw_plate.fig.subplots_adjust(left=0, right=1)

        QObject.connect(self.plotw_plate, SIGNAL("genericclickonplot"), self.plateclickprocess)
        QObject.connect(self.plotw_motimage, SIGNAL("genericclickonplot"), self.motimageclickprocess)

        
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
#        ctrllayout.addWidget(ternstackComboBoxLabel, 1, 1)
#        ctrllayout.addWidget(self.ternstackComboBox, 1, 2)
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
        mainlayout.addWidget(self.plotw_motimage, 2, 2)        
        
        pylab.figure()
        self.quat=QuaternaryPlot(pylab.gca())
        
        self.setLayout(mainlayout)
        self.resize(1600, 750)
        
        self.linefields=[('%d', 'Sample'), ('%.3f', 'motx'), ('%.3f', 'moty'), ('%.2f', 'x'), ('%.2f', 'y'), ('%.2f', 'A'), ('%.2f', 'B'), ('%.2f', 'C'), ('%.2f', 'D'), ('%d', 'code')]
        self.clearcalibpoints()
        
        p=mygetopenfile(parent=self, markstr='select image of samples with x,y motors horizontal,vertical')
        self.image=mpimg.imread(p)
        self.plotw_motimage.axes.imshow(self.image, origin='lower', interpolation='none', aspect=1)
        self.plotw_motimage.fig.canvas.draw()
        self.manual_motimage_scale()
    
    def manual_motimage_scale(self):
        idialog=messageDialog(self, 'right click and enter x value then \nrepeat for 2nd x and 2 y values.\nThis is all in motor coordinates in mm \nto set the scale of the image.')
        idialog.exec_()
        self.remaining_clicks_for_scale=4
    
    def process_motimage_scale_click(self, xc, yc):
        key=['first_x', 'second_x', 'first_y', 'second_y'][self.remaining_clicks_for_scale-1]
        motorval=userinputcaller(self, inputs=[(key, float)], title='Enter mm value of motor position you clicked',  cancelallowed=False)[0]
        if self.remaining_clicks_for_scale==4:
            self.temp_pixelval_motorval=(xc, motorval)
            self.motimage_extent=[]
        elif self.remaining_clicks_for_scale==3:
            #TODO
            #here the pixels clicked are self.temp_pixelval_motorval[0] and xc and the motor values those refere to are self.first_motx_pixelx[1] and motorval. calculate the linear transofmration from there
            #calculate motx_left corresponding to pixel 0. calculate motx_right corresponding to pixel self.image.shape[0]-1
            self.motimage_extent+=[motx_left, motx_right]
        elif self.remaining_clicks_for_scale==2:
            self.temp_pixelval_motorval=(yc, motorval)
        elif self.remaining_clicks_for_scale==1:
            #TODO
            #here the pixels clicked are self.temp_pixelval_motorval[0] and yc and the motor values those refere to are self.first_motx_pixelx[1] and motorval. calculate the linear transofmration from there
            #calculate moty_bottom corresponding to pixel 0. calculate motx_top corresponding to pixel self.image.shape[1]-1
            self.motimage_extent+=[moty_bottom, motx_top]
            self.plotw_motimage.axes.cla()
            self.plotw_motimage.axes.imshow(self.image, origin='lower', interpolation='none', aspect=1, extent=self.motimage_extent)
            self.plotw_motimage.fig.canvas.draw()
        self.remaining_clicks_for_scale-=1
        
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
        #self.plotw_motimage.fig.clf()
        fom=['k']*len(self.comp)
        for i in self.platemapselectinds:
            fom[i]='r'
        fom=numpy.array(fom)

        
        
        self.plotw_motimage.fig.canvas.draw()
        #browser text
        headline='\t'.join([k for fmtstr, k in self.linefields])
        selectsamplesstr='\n'.join([headline]+self.selectsamplelines)
        
        self.browser.setText(selectsamplesstr)

    

    def plateclickprocess(self, coords_button_ax):
        if len(self.x)==0:
            return
        critdist=2.
        xc, yc, button, ax=coords_button_ax

        dist=((self.x-xc)**2+(self.y-yc)**2)**.5
        if min(dist)<critdist:
            self.selectind=numpy.argmin(dist)
            self.plotselect()

        if button==3:#right click
            self.addtoselectsamples()
        elif button==2:#center click
            self.remfromselectsamples()

    def motimageclickprocess(self, coords_button_ax):
        xc, yc, button, ax=coords_button_ax
        if button==3:
            if self.remaining_clicks_for_scale>0:
                self.process_motimage_scale_click(self, xc, yc)
            else:
                #Here the user needs to specify a sample (for example by clicking on the platemap) and then right click the plate image
                self.calib__dlist+=[dict({}, \
                    x=self.x[self.selectind], y=self.y[self.selectind], sample_no=self.platemapdlist[self.selectind]['Sample'], ind=self.selectind, \
                    motx=xc, moty=yc\
                                                 )]
                if len(self.calib__dlist)>=3:
                    self.update_xmotor_interpolator()
                    
    def clearcalibpoints(self):
        self.calib__dlist=[]
        self.calc_motx_from_pmxy=lambda pmx, pmy: pmx
        self.calc_moty_from_pmxy=lambda pmx, pmy: pmy
    def update_xmotor_interpolator(self):
        #TODO: self.calib__dlist is a list and every value has motor x,y and platemap x,y values to build 2 interp2d functions needed below
        
        self.calc_motx_from_pmxy=lambda pmx, pmy: pmx#TODO: replace pmx here with the interpolator function, and similarly for pmy below
        self.calc_moty_from_pmxy=lambda pmx, pmy: pmy
        
    def plotselect(self):
        self.compLineEdit.setText(','.join(['%.2f' %n for n in self.comp[self.selectind]]))

        self.xyLineEdit.setText(','.join(['%.2f' %n for n in [self.x[self.selectind], self.y[self.selectind]]]))

        self.sampleLineEdit.setText('%d' %self.platemapdlist[self.selectind]['Sample'])

    def sampleline_ind(self):
        d=self.platemapdlist[self.selectind]
        d['motx']=self.calc_motx_from_pmxy(d['x'], d['y'])
        d['moty']=self.calc_moty_from_pmxy(d['x'], d['y'])
        return '\t'.join([fmtstr %d[k] for fmtstr, k in self.linefields])
        
    def addtoselectsamples(self):# self.selectind
        if self.selectind in self.platemapselectinds:
            return
        self.platemapselectinds+=[self.selectind]
        self.selectsamplelines+=[self.sampleline_ind()]
        self.plot()#would be nice to only have to plot overlay of selected samples
    
    
    def remfromselectsamples(self):# self.selectind
        if not self.selectind in self.platemapselectinds:
            return
        i=self.platemapselectinds.index(self.selectind)
        self.platemapselectinds.pop(i)
        self.selectsamplelines.pop(i)
        self.plot()#would be nice to only have to plot overlay of selected samples

        
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
        self.setWindowTitle('PlateMap Align to Image')
        self.di=plateimagealignDialog(self, **kwargs)
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
