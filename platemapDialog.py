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
        self.plotillumkey=None

        self.techniquedictlist=[]
        
        self.plotw_select=plotwidget(self)
        self.plotw_select.axes.set_xlabel('')
        self.plotw_select.axes.set_ylabel('')
        self.plotw_select.axes.set_aspect(1)
        
        self.plotw_plate=plotwidget(self)
        self.plotw_plate.axes.set_xlabel('')
        self.plotw_plate.axes.set_ylabel('')
        self.plotw_plate.axes.set_aspect(1)
        
        self.plotw_tern=plotwidget(self)
        self.plotw_tern.axes.set_xlabel('')
        self.plotw_tern.axes.set_ylabel('')
        self.plotw_tern.axes.set_aspect(1)
        
##        self.plotw_quat=plotwidget(self, projection3d=True)
#        self.plotw_quat.axes.set_xlabel('')
#        self.plotw_quat.axes.set_ylabel('')
        #self.plotw_quat.axes.set_aspect(1)
        
##        self.plotw_aux=plotwidget(self)
#        self.plotw_aux.axes.set_xlabel('')
#        self.plotw_aux.axes.set_ylabel('')
        #self.plotw_aux.axes.set_aspect(1)
        
        axrect=[0.82, 0.1, 0.04, 0.8]
        
        
        self.plotw_plate.fig.subplots_adjust(left=0, right=axrect[0]-.01)
        self.cbax_plate=self.plotw_plate.fig.add_axes(axrect)
        
#        self.plotw_tern.fig.subplots_adjust(left=0, right=axrect[0]-.01)
#        self.cbax_tern=self.plotw_tern.fig.add_axes(axrect)
        
##        self.plotw_quat.fig.subplots_adjust(left=0, right=axrect[0]-.01)
##        self.cbax_quat=self.plotw_quat.fig.add_axes(axrect)
        
##        self.plotw_select.fig.subplots_adjust(left=.2)
##        self.plotw_aux.fig.subplots_adjust(left=.2)

##        QObject.connect(self.plotw_plate, SIGNAL("genericclickonplot"), self.plateclickprocess)
        
#in options, always make an option that does not require user input at index 0
        CVops=[\
        ['Imax', ['I(A)'], []], \
        ['Imin', ['I(A)'], []], \
        ['E_Ithresh', ['I(A)','Ewe(V)'], [['Ithresh(A)', float, '1e-5'], ['Num consec points', int, '20'], ['0 for below, 1 for above', int, '1'], ['Thresh not reached value', float, '1']]], \
        ['Eh in I=Io Exp(E/Eh)', ['I(A)', 'Ewe(V)'], []], \
        ['Io in I=Io Exp(E/Eh)', ['I(A)', 'Ewe(V)'], []], \
        ['Iphoto_max', ['Illum', 'I(A)', 'Ewe(V)', 't(s)'], [['frac of Illum segment start', float, '0.4'], ['frac of Illum segment end', float, '0.95'], ['frac of Dark segment start', float, '0.4'], ['frac of Dark segment end', float, '0.95'], ['Illum signal key', str, 'Ach(V)'], ['Illum signal time shift (s)', float, '0.'], ['Illum Threshold', float, '0.8'], ['Illum Invert', int, '1'], ['num illum cycles', int, '99'], ['0 from beginning, 1 from end', int, '1']]], \
        ['Iphoto_min', ['Illum', 'I(A)', 'Ewe(V)', 't(s)'], [['frac of Illum segment start', float, '0.4'], ['frac of Illum segment end', float, '0.95'], ['frac of Dark segment start', float, '0.4'], ['frac of Dark segment end', float, '0.95'], ['Illum signal key', str, 'Ach(V)'], ['Illum signal time shift (s)', float, '0.'], ['Illum Threshold', float, '0.8'], ['Illum Invert', int, '1'], ['num illum cycles', int, '99'], ['0 from beginning, 1 from end', int, '1']]], \
        ['None', ['I(A)', 'Ewe(V)'], []], \
        ]
        
        OCVops=[\
        ['Efin', ['Ewe(V)'], []], \
        ['Eave', ['Ewe(V)', 't(s)'], [['Interval(s)', float, '2.'], ['Num StdDev outlier', float, '2.'], ['Num Pts in Window', int, '999999'], ['0 from beginning, 1 from end', int, '1']]], \
        ['Ess', ['Ewe(V)'], [['Weight Exponent for NumPts', float, '1.'], ['NumPts test interval', int, '10']]], \
        ['Ephoto', ['Illum', 'Ewe(V)', 'I(A)', 't(s)'], [['frac of Illum segment start', float, '0.4'], ['frac of Illum segment end', float, '0.95'], ['frac of Dark segment start', float, '0.4'], ['frac of Dark segment end', float, '0.95'], ['Illum signal key', str, 'Ach(V)'], ['Illum signal time shift (s)', float, '0.'], ['Illum Threshold', float, '0.8'], ['Illum Invert', int, '1'], ['num illum cycles', int, '99'], ['0 from beginning, 1 from end', int, '1']]], \
        ]
        
        CPops=[\
        ['Efin', ['Ewe(V)'], []], \
        ['Eave', ['Ewe(V)', 't(s)'],  [['Interval(s)', float, '2.'], ['Num StdDev outlier', float, '2.'], ['Num Pts in Window', int, '999999'], ['0 from beginning, 1 from end', int, '1']]], \
        ['Ess', ['Ewe(V)'], [['Weight Exponent for NumPts', float, '1.'], ['NumPts test interval', int, '10']]], \
        ['Ephoto', ['Illum', 'Ewe(V)', 'I(A)', 't(s)'], [['frac of Illum segment start', float, '0.4'], ['frac of Illum segment end', float, '0.95'], ['frac of Dark segment start', float, '0.4'], ['frac of Dark segment end', float, '0.95'], ['Illum signal key', str, 'Ach(V)'], ['Illum signal time shift (s)', float, '0.'], ['Illum Threshold', float, '0.8'], ['Illum Invert', int, '1'], ['num illum cycles', int, '99'], ['0 from beginning, 1 from end', int, '1']]], \
        ]
        
        CAops=[\
        ['Ifin', ['I(A)'], []], \
        ['Iave', ['I(A)', 't(s)'],  [['Interval(s)', float, '2.'], ['Num StdDev outlier', float, '2.'], ['Num Pts in Window', int, '999999'], ['0 from beginning, 1 from end', int, '1']]], \
        ['Iss', ['I(A)'], [['Weight Exponent for NumPts', float, '1.'], ['NumPts test interval', int, '10']]], \
        ['Iphoto', ['Illum', 'I(A)', 'Ewe(V)', 't(s)'], [['frac of Illum segment start', float, '0.4'], ['frac of Illum segment end', float, '0.95'], ['frac of Dark segment start', float, '0.4'], ['frac of Dark segment end', float, '0.95'], ['Illum signal key', str, 'Ach(V)'], ['Illum signal time shift (s)', float, '0.'], ['Illum Threshold', float, '0.8'], ['Illum Invert', int, '1'], ['num illum cycles', int, '99'], ['0 from beginning, 1 from end', int, '1']]], \
        ]
        
        Bubbleops=[\
        ['slopefin', ['Maxslope'], []], \
        ['Intfin', ['Intensity'], []], \
        ]
        
        
        self.expmnt_calc_options=[['OCV', OCVops], ['CP', CPops], ['CA', CAops], ['CV', CVops], ['Bubble', Bubbleops]]
        self.expmnt_calc_lastusedvals=[[[] for calcopt in opslist] for opname, opslist in self.expmnt_calc_options]
        expmntComboBoxLabel=QLabel()
        expmntComboBoxLabel.setText('Technique type:')
        self.expmntComboBox=QComboBox()
        for i, tup in enumerate(self.expmnt_calc_options):
            self.expmntComboBox.insertItem(i, tup[0])
        self.expmntComboBox.setCurrentIndex(0)
        
#        calcoptionComboBoxLabel=QLabel()
#        calcoptionComboBoxLabel.setText('FOM:')
#        self.calcoptionComboBox=QComboBox()

        ternskipComboBoxLabel=QLabel()
        ternskipComboBoxLabel.setText('Exclude for ternary:')
        self.ternskipComboBox=QComboBox()
        for i, l in enumerate(['A', 'B', 'C', 'D']):
            self.ternskipComboBox.insertItem(i, l)
        self.ternskipComboBox.setCurrentIndex(i)
        
        #QObject.connect(self.expmntComboBox,SIGNAL("activated(QString)"),self.fillcalcoptions)
        #QObject.connect(self.calcoptionComboBox,SIGNAL("activated(QString)"),self.getcalcparams)
        
        self.xplotchoiceComboBox=QComboBox()
        self.yplotchoiceComboBox=QComboBox()
        self.plotkeys=['t(s)', 'I(A)', 'Ewe(V)', 'Ece(V)', 'Ewe-E0(V)', 'I*Is(A)']
        #keys=['Intensity', 'Fit', 'Maxslope']
        for i, nam in enumerate(self.plotkeys):
            self.xplotchoiceComboBox.insertItem(i, nam)
            self.yplotchoiceComboBox.insertItem(i, nam)
        self.xplotchoiceComboBox.setCurrentIndex(0)
        self.yplotchoiceComboBox.setCurrentIndex(1)
        
        xplotchoiceComboBoxLabel=QLabel()
        xplotchoiceComboBoxLabel.setText('x-axis')
        yplotchoiceComboBoxLabel=QLabel()
        yplotchoiceComboBoxLabel.setText('y-axis')
        
#        self.legendselectLineEdit=QLineEdit()
#        self.legendselectLineEdit.setText('4')
#        templab=QLabel()
#        templab.setText("'select' plot\nlegend loc (int)")
#        legendlayout=QVBoxLayout()
#        legendlayout.addWidget(templab)
#        legendlayout.addWidget(self.legendselectLineEdit)
        
        self.fileLineEdit=QLineEdit()        
        self.fileLineEdit.setText('/Users/Solrisa/Documents/platevisualizer_ui/Plate28.rtf')
        fileLineEditLabel=QLabel()
        fileLineEditLabel.setText('File:\n')
        fileLineEditlayout=QVBoxLayout()
        fileLineEditlayout.addWidget(fileLineEditLabel)
        fileLineEditlayout.addWidget(self.fileLineEdit)

        
        expmntLineEditLabel=QLabel()
        expmntLineEditLabel.setText('Composition:\n use the order in the data files\n(as in a,b,c,d)')
        self.expmntLineEdit=QLineEdit()
        self.expmntLineEdit.setText('0.5,0.4,0.1')
        
#        expmntLineEditButton=QPushButton()
#        expmntLineEditLabel.setText('Composition:\n use the order in the data files\n(as in a,b,c,d)')    
        
        xyLineEditLabel=QLabel()
        xyLineEditLabel.setText('x,y position:')
        self.xyLineEdit=QLineEdit()
        self.xyLineEdit.setText('i.e. 5.45, 6.33')
        
        sampleLineEditLabel=QLabel()
        sampleLineEditLabel.setText('Sample #:')
        self.sampleLineEdit=QLineEdit()
        self.sampleLineEdit.setText('i.e. 254')


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
#        QObject.connect(addSample, SIGNAL("pressed()"), mygetopenfile)
        
        remSample=QPushButton()
        remSample.setText("remove")

        folderButton=QPushButton()
        folderButton.setText("select\nfolder")
        #QObject.connect(folderButton, SIGNAL("pressed()"), self.selectfolder)
        
        plotButton=QPushButton()
        plotButton.setText("update\nfigures")
        #QObject.connect(plotButton, SIGNAL("pressed()"), self.calcandplot)
        
        updateButton=QPushButton()
        updateButton.setText("update\ndata")
        #QObject.connect(updateButton, SIGNAL("pressed()"), self.calcandplotwithupdate)
        
        saveButton=QPushButton()
        saveButton.setText("save FOM\nspreadhseet")
        QObject.connect(saveButton, SIGNAL("pressed()"), self.writefile)
        
        savesampleButton=QPushButton()
        savesampleButton.setText("save select\nsample IDs")
        QObject.connect(savesampleButton, SIGNAL("pressed()"), self.writesamplelist)
        
        self.infoLabel=QLabel()
        self.infodef='Q=10,15,40,80 1/nm -> \nd=0.63,0.42,0.16,0.079 nm\n'
        
        self.revcmapCheckBox=QCheckBox()
        self.revcmapCheckBox.setText('reverse cmap?')
        
        templab=QLabel()
        templab.setText('min,max colorbar')
        
        self.vminmaxLineEdit=QLineEdit()
        
        vminmaxlayout=QVBoxLayout()
        vminmaxlayout.addWidget(templab)
        vminmaxlayout.addWidget(self.vminmaxLineEdit)

        templab=QLabel()
        templab.setText('below,above range colors:\nEnter a char,0-1 gray,tuple,\n"None" for ignore')
        
        self.aboverangecolLineEdit=QLineEdit()
        self.aboverangecolLineEdit.setText('k')
        self.belowrangecolLineEdit=QLineEdit()
        self.belowrangecolLineEdit.setText('0.9')
        
        outrangecollayout=QGridLayout()
        outrangecollayout.addWidget(templab, 0, 0, 2, 1)
        outrangecollayout.addWidget(self.belowrangecolLineEdit, 0, 1)
        outrangecollayout.addWidget(self.aboverangecolLineEdit, 1, 1)
        
        self.statusLineEdit=QLineEdit()
        self.statusLineEdit.setReadOnly(True)
        
        templab=QLabel()
        templab.setText('DAQ time')
        self.daqtimeLineEdit=QLineEdit()
        daqtimelayout=QVBoxLayout()
        daqtimelayout.addWidget(templab)
        daqtimelayout.addWidget(self.daqtimeLineEdit)
        
        stackedtern10Button=QPushButton()
        stackedtern10Button.setText("Create stacked\ntern at 10%")
        QObject.connect(stackedtern10Button, SIGNAL("pressed()"), self.stackedtern10window)
        
        stackedtern30Button=QPushButton()
        stackedtern30Button.setText("Create stacked\ntern at 3.33%")
        QObject.connect(stackedtern30Button, SIGNAL("pressed()"), self.stackedtern30window)
        
        templab=QLabel()
        templab.setText('E0=Equil.Pot.(V):')
        self.E0SpinBox=QDoubleSpinBox()
        self.E0SpinBox.setDecimals(3)
        E0layout=QHBoxLayout()
        E0layout.addWidget(templab)
        E0layout.addWidget(self.E0SpinBox)
        
        templab=QLabel()
        templab.setText('Is=I scaling:')
        self.IsSpinBox=QDoubleSpinBox()
        self.IsSpinBox.setMaximum(1000.)
        self.IsSpinBox.setMinimum(-1000.)
        self.IsSpinBox.setValue(1.)
        Islayout=QHBoxLayout()
        Islayout.addWidget(templab)
        Islayout.addWidget(self.IsSpinBox)
        
        self.overlayselectCheckBox=QCheckBox()
        self.overlayselectCheckBox.setText("overlay on\n'select' plot")
        self.legendselectLineEdit=QLineEdit()
        self.legendselectLineEdit.setText('4')
        templab=QLabel()
        templab.setText("'select' plot\nlegend loc (int)")
        legendlayout=QVBoxLayout()
        legendlayout.addWidget(templab)
        legendlayout.addWidget(self.legendselectLineEdit)
        
        
        
        selectbuttonlayout=QHBoxLayout()
        selectbuttonlab=QLabel()
        selectbuttonlab.setText("Select samples by mouse right-click\n  OR filter FOM in this range:")
        #selectbuttonlayout.addWidget(templab, 0, 0, 1, 3)
        
        selectbelowButton=QPushButton()
        selectbelowButton.setText("(-INF,min)")
        QObject.connect(selectbelowButton, SIGNAL("pressed()"), self.selectbelow)
        selectbuttonlayout.addWidget(selectbelowButton)#, 1, 0)
        
        selectbetweenButton=QPushButton()
        selectbetweenButton.setText("[min,max)")
        QObject.connect(selectbetweenButton, SIGNAL("pressed()"), self.selectbetween)
        selectbuttonlayout.addWidget(selectbetweenButton)#, 1, 1)
        
        selectaboveButton=QPushButton()
        selectaboveButton.setText("[max,INF)")
        QObject.connect(selectaboveButton, SIGNAL("pressed()"), self.selectabove)
        selectbuttonlayout.addWidget(selectaboveButton)#, 1, 2)
    
        
        selectsamplelab=QLabel()
        selectsamplelab.setText("sample IDs selected for export")
        #selectsamplelayout=QVBoxLayout()
        #selectsamplelayout.addWidget(templab)
        self.selectsamplesLineEdit=QLineEdit()
        #selectsamplelayout.addWidget(self.selectsamplesLineEdit)

        self.ctrlgriditems=[\
#        (expmntComboBoxLabel, self.expmntComboBox, 0, 0), \
#        (calcoptionComboBoxLabel, self.calcoptionComboBox, 0, 1), \
        (fileLineEditLabel, self.fileLineEdit, 0, 0),\
        (expmntLineEditLabel, self.expmntLineEdit, 1, 0), \
        (xyLineEditLabel, self.xyLineEdit, 2, 0),\
        (sampleLineEditLabel, self.sampleLineEdit, 3, 0),\
#        (xplotchoiceComboBoxLabel, self.xplotchoiceComboBox, 1, 0), \
#        (yplotchoiceComboBoxLabel, self.yplotchoiceComboBox, 1, 1), \
#        (ternskipComboBoxLabel, self.ternskipComboBox, 1, 2), \
        ]
        
        mainlayout=QGridLayout()
        ctrllayout=QGridLayout()
        for labw, spw, i, j in self.ctrlgriditems:
            templayout=QHBoxLayout()
            templayout.addWidget(labw)
            templayout.addWidget(spw)
            ctrllayout.addLayout(templayout, i, j)
        
        ctrllayout.addWidget(addFile, 0, 1)
        ctrllayout.addWidget(addComp, 1, 1)
        ctrllayout.addWidget(remComp, 1, 2)
        ctrllayout.addWidget(addxy, 2, 1)
        ctrllayout.addWidget(remxy, 2, 2)
        ctrllayout.addWidget(addSample, 3, 1)
        ctrllayout.addWidget(remSample, 3, 2)
#        ctrllayout.addWidget(plotButton, 0, 1)
#        ctrllayout.addLayout(savebuttonlayout, 0, 0, 1, 4)
#        #        ctrllayout.addWidget(self.revcmapCheckBox, i+2, 0)
#
#        ctrllayout.addLayout(vminmaxlayout, i+2, 1)
#        ctrllayout.addLayout(outrangecollayout, i+2, 2)
#        
##        ctrllayout.addWidget(self.statusLineEdit, i+3, 0)
#        ctrllayout.addWidget(self.overlayselectCheckBox, i+3, 1)
#        ctrllayout.addLayout(legendlayout, i+3, 2)
#        
#        ctrllayout.addLayout(daqtimelayout, i+4, 0)
#        ctrllayout.addWidget(stackedtern10Button, i+4, 1)
###        ctrllayout.addWidget(stackedtern30Button, i+4, 2)
#        
#        ctrllayout.addLayout(E0layout, i+5, 0, 1, 2)
#        ctrllayout.addLayout(Islayout, i+5, 2, 1, 2)
#        
#        ctrllayout.addWidget(selectbuttonlab, i+6, 0)
#        #ctrllayout.addLayout(selectsamplelayout, i+6, 1, 1, 2)
#        ctrllayout.addWidget(selectsamplelab, i+6, 1, 1, 2)
#        
#        ctrllayout.addLayout(selectbuttonlayout, i+7, 0)
#        ctrllayout.addWidget(self.selectsamplesLineEdit, i+7, 1, 1, 2)
        
        self.browser = QTextBrowser()
#        self.lineedit = self.addValuesComp
        self.lineedit = QLineEdit("Type an expression and press Enter")
        self.lineedit.selectAll()
        self.connect(self.lineedit, SIGNAL("returnPressed()"),self.updateUi)

                
        
        mainlayout.addLayout(ctrllayout, 0, 0, 1, 2)
#        mainlayout.addWidget(self.plotw_aux, 0, 2)
#        mainlayout.addWidget(self.plotw_plate, 0, 2, 1, 2)
        mainlayout.addWidget(self.browser, 0, 2)
        mainlayout.addWidget(self.lineedit, 1,2,1,1)
#        mainlayout.addWidget(self.browser, 0, 2, 1, 1)
#        mainlayout.addWidget(self.lineedit, 0, 3, 1, 1)
#        mainlayout.addWidget(self.plotw_select, 1, 0)
#        mainlayout.addWidget(self.plotw_quat, 1, 0,1,1)
#        mainlayout.addWidget(stackedtern30Button, 1, 1, 1, 3)
#        mainlayout.addWidget(self.plotw_tern, 1, 1, 1, 3)
        
        
        self.setLayout(mainlayout)
        
        
        self.statusLineEdit.setText('idle')
        self.plate_id=None
        self.resize(1600, 750)
        
    def updateUi(self):
        print "test2"
        try:
            text = unicode(self.lineedit.text())
            self.browser.append("%s = <b>%s</b>" % (text, eval(text)))
        except:
            self.browser.append("<font color=red>%s is invalid!</font>" %text)
    def plot(self):
        self.statusLineEdit.setText('plotting')
        s=25
        
        self.plotw_tern.axes.cla()
        self.plotw_quat.axes.cla()
        self.plotw_plate.axes.cla()
        self.plotw_aux.axes.cla()
        self.cbax_quat.cla()
        self.cbax_tern.cla()
        self.cbax_plate.cla()
        
        if len(self.techniquedictlist)==0:
            self.statusLineEdit.setText('idle')
            return
#        m=self.plotw_tern.axes.scatter(self.detx, self.detz, c=self.dsp, s=s, edgecolors='none')
#        cb=self.plotw_tern.fig.colorbar(m, cax=self.cbax_tern)
#        cb.set_label('d-spacing (nm)')
        
        getarr=lambda k:getarrfromkey(self.techniquedictlist, k)
        fom=getarr('FOM')
        sample=getarr('Sample')
        
        if self.revcmapCheckBox.isChecked():
            cmap=cm.jet_r
        else:
            cmap=cm.jet
        
        clip=True
        skipoutofrange=[False, False]
        self.vmin=fom.min()
        self.vmax=fom.max()
        vstr=str(self.vminmaxLineEdit.text()).strip()
        if ',' in vstr:
            a, b, c=vstr.partition(',')
            try:
                a=myeval(a.strip())
                c=myeval(c.strip())
                self.vmin=a
                self.vmax=c
                for count, (fcn, le) in enumerate(zip([cmap.set_under, cmap.set_over], [self.belowrangecolLineEdit, self.aboverangecolLineEdit])):
                    vstr=str(le.text()).strip()
                    vstr=vstr.replace('"', '').replace("'", "")
                    print '^^^', vstr, 'none' in vstr or 'None' in vstr
                    if 'none' in vstr or 'None' in vstr:
                        skipoutofrange[count]=True
                        continue
                    if len(vstr)==0:
                        continue
                    c=col_string(vstr)
                    try:
                        fcn(c)
                        clip=False
                    except:
                        print 'color entry not understood:', vstr
                
            except:
                pass
        
        norm=colors.Normalize(vmin=self.vmin, vmax=self.vmax, clip=clip)
        print 'fom min, max, mean, std:', fom.min(), fom.max(), fom.mean(), fom.std()
        
        comps=getarr('compositions')
        x=getarr('x')
        y=getarr('y')
        print 'skipoutofrange', skipoutofrange
        print len(fom)
        if skipoutofrange[0]:
            inds=numpy.where(fom>=self.vmin)
            fom=fom[inds]
            comps=comps[inds]
            x=x[inds]
            y=y[inds]
        print len(fom)
        if skipoutofrange[1]:
            inds=numpy.where(fom<=self.vmax)
            fom=fom[inds]
            comps=comps[inds]
            x=x[inds]
            y=y[inds]
        print len(fom)
        
        
        if numpy.any(fom>self.vmax):
            if numpy.any(fom<self.vmin):
                extend='both'
            else:
                extend='max'
        elif numpy.any(fom<self.vmin): 
            extend='min'
        else:
            extend='neither'
        print 'extend ', extend
#        m=self.plotw_plate.axes.scatter(x, y, c=fom, s=s, marker='s', cmap=cmap, norm=norm)
#        cb=self.plotw_plate.fig.colorbar(m, cax=self.cbax_plate, extend=extend, format=autocolorbarformat((fom.min(), fom.max())))
        #cb.set_label('|Q| (1/nm)')
        
        
        comps=numpy.array([c[:4]/c[:4].sum() for c in comps])
        i=self.ternskipComboBox.currentIndex()
        inds=[j for j in range(4) if j!=i][:3]
        terncomps=numpy.array([c[inds]/c[inds].sum() for c in comps])
        reordercomps=comps[:, inds+[i]]
        self.ellabels=self.techniquedictlist[0]['elements']
        reorderlabels=[self.ellabels[j] for j in inds+[i]]
        
        
        quat=QuaternaryPlot(self.plotw_quat.axes, ellabels=self.ellabels, offset=0)
        quat.label()
        quat.scatter(comps, c=fom, s=s, cmap=cmap, vmin=self.vmin, vmax=self.vmax)
        cb=self.plotw_quat.fig.colorbar(quat.mappable, cax=self.cbax_quat, extend=extend, format=autocolorbarformat((fom.min(), fom.max())))
        
#        fomlabel=''.join((str(self.expmntLineEdit.text()), str(self.calcoptionComboBox.currentText())))
#        self.stackedternplotdict=dict([('comps', reordercomps), ('fom', fom), ('cmap', cmap), ('norm', norm), ('ellabels', reorderlabels), ('fomlabel', fomlabel)])
        
        tern=TernaryPlot(self.plotw_tern.axes, ellabels=reorderlabels[:3], offset=0)
        tern.label()
        tern.scatter(terncomps, c=fom, s=s, cmap=cmap, vmin=self.vmin, vmax=self.vmax)
        cb=self.plotw_tern.fig.colorbar(tern.mappable, cax=self.cbax_tern, extend=extend, format=autocolorbarformat((fom.min(), fom.max())))
        
#        mapsvg('Plate 28.txt', 'Plate28-svgwrite.svg', ml=(65, 256, 321, 512, 577, 768, 833, 1024, 1089, 1280, 1345, 1536, 1601, 1792), allch=True)        
        
        self.plotw_aux.axes.plot(fom, 'g.-')
        self.plotw_aux.axes.set_xlabel('sorted by experiment time')
        self.plotw_aux.axes.set_ylabel('FOM')
        autotickformat(self.plotw_aux.axes, x=0, y=1)
        
        self.plotw_quat.axes.mouse_init()
        self.plotw_quat.axes.set_axis_off()
        self.plotw_tern.fig.canvas.draw()
        self.plotw_quat.fig.canvas.draw()
        self.plotw_plate.fig.canvas.draw()
        self.plotw_aux.fig.canvas.draw()
        
        self.selectind=-1
        self.plotselect()
        self.statusLineEdit.setText('idle')

    def stackedtern10window(self):
        d=self.stackedternplotdict
        self.echem10=echem10axesWidget(parent=self.parent, ellabels=d['ellabels'])
        self.echem10.plot(d, cb=True)
        
        #scatter_10axes(d['comps'], d['fom'], self.echem10.stpl, s=18, edgecolors='none', cmap=d['cmap'], norm=d['norm'])
        self.echem10.exec_()
        
    def stackedtern30window(self):
        d=self.stackedternplotdict
        self.echem30=echem30axesWidget(parent=None, ellabels=d['ellabels'])
        self.echem30.plot(d, cb=True)

        #scatter_30axes(d['comps'], d['fom'], self.echem30.stpl, s=18, edgecolors='none', cmap=d['cmap'], norm=d['norm'])
        #self.echem30.show()
        self.echem30.exec_()

    def plotselect(self):
        overlaybool=self.overlayselectCheckBox.isChecked()
        if not overlaybool:
            self.plotw_select.axes.cla()
        d=self.techniquedictlist[self.selectind]
        
        xk=str(self.xplotchoiceComboBox.currentText())
        yk=str(self.yplotchoiceComboBox.currentText())
        
        xshift=0.
        xmult=1.
        yshift=0.
        ymult=1.
        if '-E0' in xk:
            xshift=-1.*self.E0SpinBox.value()
            xk=xk.replace('-E0', '')
        if '*Is' in xk:
            xmult=self.IsSpinBox.value()
            xk=xk.replace('*Is', '')
        if '-E0' in yk:
            yshift=-1.*self.E0SpinBox.value()
            yk=yk.replace('-E0', '')
        if '*Is' in yk:
            ymult=self.IsSpinBox.value()
            yk=yk.replace('*Is', '')
            
        if not xk in d.keys():
            print 'cannot plot the selected x-y graph because %s not found' %xk
            return
        if not yk in d.keys():
            print 'cannot plot the selected x-y graph because %s not found' %yk
            return
        x=d[xk]*xmult+xshift
        y=d[yk]*ymult+yshift
        lab=''.join(['%s%d' %(el, c*100.) for el, c in zip(d['elements'], d['compositions'])])+'\n'
        if 'FOM' in d.keys():
            lab+='%d,%.2e' %(d['Sample'], d['FOM'])
        else:
            lab+='%d' %d['Sample']
        self.plotw_select.axes.plot(x, y, '.-', label=lab)

        autotickformat(self.plotw_select.axes, x=0, y=1)

        if (not self.plotillumkey is None) and self.plotillumkey in d.keys() and not overlaybool:
            illuminds=numpy.where(d[self.plotillumkey])[0]
            self.plotw_select.axes.plot(x[illuminds], y[illuminds], 'y.')
        self.plotw_select.axes.set_xlabel(xk)
        self.plotw_select.axes.set_ylabel(yk)
        legtext=unicode(self.legendselectLineEdit.text())
        if len(legtext)>0:
            legloc=myeval(legtext)
            if isinstance(legloc, int) and legloc>=0:
                self.plotw_select.axes.legend(loc=legloc)
        self.plotw_select.fig.canvas.draw()
        t=d['mtime']-2082844800.
        print '^^^^^^^^', t
        if not isinstance(t, str):
            try:
                t=time.ctime(t)
            except:
                t='error'
        print t
        self.daqtimeLineEdit.setText(t)

    def plateclickprocess(self, coords_button):
        if len(self.techniquedictlist)==0:
            return
        critdist=3.
        xc, yc, button=coords_button
        x=getarrfromkey(self.techniquedictlist, 'x')
        y=getarrfromkey(self.techniquedictlist, 'y')
        dist=((x-xc)**2+(y-yc)**2)**.5
        if min(dist)<critdist:
            self.selectind=numpy.argmin(dist)
            self.plotselect()
        if button==3:
            self.addtoselectsamples([self.techniquedictlist[self.selectind]['Sample']])
    def selectbelow(self):
        try:
            vmin, vmax=(self.vmin, self.vmax)
        except:
            print 'NEED TO PERFORM A PLOT TO DEFINE THE MIN,MAX RANGE BEFORE SELECTING SAMPLES'
        idlist=[]
        for d in self.techniquedictlist:
            if d['FOM']<vmin:
                idlist+=[d['Sample']]
        if len(idlist)>0:
            self.addtoselectsamples(idlist)
            
    def selectbetween(self):
        try:
            vmin, vmax=(self.vmin, self.vmax)
        except:
            print 'NEED TO PERFORM A PLOT TO DEFINE THE MIN,MAX RANGE BEFORE SELECTING SAMPLES'
        idlist=[]
        for d in self.techniquedictlist:
            if d['FOM']>=vmin and d['FOM']<vmax:
                idlist+=[d['Sample']]
        if len(idlist)>0:
            self.addtoselectsamples(idlist)
            
    def selectabove(self):
        try:
            vmin, vmax=(self.vmin, self.vmax)
        except:
            print 'NEED TO PERFORM A PLOT TO DEFINE THE MIN,MAX RANGE BEFORE SELECTING SAMPLES'
        idlist=[]
        for d in self.techniquedictlist:
            if d['FOM']>=vmax:
                idlist+=[d['Sample']]
        if len(idlist)>0:
            self.addtoselectsamples(idlist)
            
    def addtoselectsamples(self, idlist):
        instr=str(self.selectsamplesLineEdit.text()).strip().split(',')
        instr+=[`n` for n in idlist if len(`n`)>0]
        s=','.join(instr).strip().strip(',').strip()
        self.selectsamplesLineEdit.setText(s)

        #John explains how to evaluate lineedit: eval('['+s+']')
    def openAddFile(self):
        file = open(self.fileLineEdit.text(), mode='r')
        for line in file:
            self.browser.append(line)
    def addValuesComp(self):
        try:
            s=unicode(self.expmntLineEdit.text())
            self.browser.append("%s = <b>%s</b>" % (s, eval('['+s+']')))
        except:
            self.browser.append("<font color=red>%s is invalid!</font>" %s)
            print 'Need to write a set of compositions'

    def addValuesXY(self):
        try:
            xy=unicode(self.xyLineEdit.text())
            self.browser.append("%s = <b>%s</b>" % (xy, eval('['+xy+']')))
        except:
            self.browser.append("<font color=red>%s is invalid!</font>" %s)
            print 'Need to write a set of x&y coordinates'

    def remValuesComp(self):
        try:
            s=unicode(self.expmntLineEdit.text())
            print "try"
            self.browser.cut(s)
        except:
            print 'Need to write a set of x&y coordinates'
            
    def remValuesXY(self):
        try:
            xy=unicode(self.xyLineEdit.text())
            self.browser.clear(xy)
        except:
            print 'Need to write a set of x&y coordinates'
#        idlist=[]
#        for d in self.techniquedictlist:
#            if d['FOM']>=vmin and d['FOM']<vmax:
#                idlist+=[d['Sample']]
#        if len(idlist)>0:
#            self.addtoselectsamples(idlist)
            
        
    def writesamplelist(self, p=None, explab='selectsamples'):
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
        
        self.statusLineEdit.setText('idle')
        
    def writefile(self, p=None, explab=None, savedlist=False):
        self.statusLineEdit.setText('writing file')
        if len(self.techniquedictlist)==0:
            print 'no data to save'
            return
#        if explab is None:
#            explab=''.join((str(self.expmntLineEdit.text()), str(self.calcoptionComboBox.currentText())))
        if p is None:
            p=mygetsavefile(parent=self, markstr='save spreadsheet string', filename=os.path.split(self.folderpath)[1]+'_'+explab+'.txt' )
        elif os.path.isdir(p):
            p=os.path.join(p, os.path.split(self.folderpath)[1]+'_'+explab+'.txt')
            print p
        if not p:
            print 'save aborted'
            return
            
        labels=['Sample', 'x(mm)', 'y(mm)']
        labels+=self.techniquedictlist[0]['elements']
        labels+=[explab]
        kv_fmt=[('Sample', '%d'), ('x', '%.2f'), ('y', '%.2f'), ('compositions', '%.4f'), ('FOM', '%.6e')]
        arr=[]
        for d in self.techniquedictlist:
            arr2=[]
            for k, fmt in kv_fmt:
                v=d[k]
                if isinstance(v, numpy.ndarray) or isinstance(v, list):
                    for subv in v:
                        arr2+=[fmt %subv]
                else:
                    arr2+=[fmt %v]
            arr+=['\t'.join(arr2)]
        s='\t'.join(labels)+'\n'
        s+='\n'.join(arr)
        
        f=open(p, mode='w')
        f.write(s)
        f.close()
        
        if savedlist:
            f=open(p[:-4]+'_dlist.pck', mode='w')
            pickle.dump(self.techniquedictlist, f)
            f.close()
        
        self.statusLineEdit.setText('idle')

class MainMenu(QMainWindow):
    def __init__(self, previousmm, execute=True, **kwargs):#, TreeWidg):
        super(MainMenu, self).__init__(None)
        #self.setupUi(self)
        self.setWindowTitle('PlateMap Visualization')
        self.di=platemapDialog(self, **kwargs)
        if execute:
            self.di.exec_()