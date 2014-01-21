import time
import time
import os, os.path
import sys
import numpy
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import operator
import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
import numpy.ma as ma
import matplotlib.colors as colors
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import pylab
import pickle

from mapspread import *

PyCodePath=os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
print PyCodePath
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import ScalarFormatter
def myexpformat_4digs(x, pos):
    return '%.3e' %x
#    for ndigs in range(4):
#        lab=(('%.'+'%d' %ndigs+'e') %x).replace('e+0','e').replace('e+','e').replace('e0','').replace('e-0','e')
#        if eval(lab)==x:
#            return lab
#    return lab

ExpTickLabels=FuncFormatter(myexpformat_4digs)
RegTickLabels=matplotlib.ticker.ScalarFormatter()

def autotickformat(ax, x=False, y=False, ndec=3):
    for bl, xax, lims in zip([x, y], [ax.xaxis, ax.yaxis], [ax.get_xlim(), ax.get_ylim()]):
        if bl:
            try:
                doit=numpy.max(numpy.log10(numpy.abs(numpy.array(lims))))<(-ndec)
                doit=doit or numpy.min(numpy.log10(numpy.abs(numpy.array(lims))))>ndec
            except:
                print 'error on axis formatter for lims ', lims
                continue
            if doit:
                xax.set_major_formatter(ExpTickLabels)
            else:
                xax.set_major_formatter(RegTickLabels)

def autocolorbarformat(lims, ndec=3):
    try:
        doit=numpy.max(numpy.log10(numpy.abs(numpy.array(lims))))<(-ndec)
        doit=doit or numpy.min(numpy.log10(numpy.abs(numpy.array(lims))))>ndec
    except:
        print 'error on axis formatter for lims ', lims
        return
    if doit:
        return ExpTickLabels
    else:
        return RegTickLabels

wd=os.getcwd()


sys.path.append(os.path.join(PyCodePath,'PythonCompositionPlots'))
from myternaryutility import TernaryPlot
from myquaternaryutility import QuaternaryPlot
from quaternary_FOM_stackedtern5 import *
from quaternary_FOM_stackedtern10 import *
from quaternary_FOM_stackedtern20 import *
from quaternary_FOM_stackedtern30 import *

#sys.path.append(os.path.join(PyCodePath,'JCAPPyDBComm'))
#from mysql_dbcommlib import *
#
#sys.path.append(os.path.join(PyCodePath, 'PythonCodeSecureFiles'))
#from paths import *
#if os.path.isdir(EchemSavePath):
#    os.chdir(EchemSavePath)


    
class messageDialog(QDialog):
    def __init__(self, parent=None, title=''):
        super(messageDialog, self).__init__(parent)
        self.setWindowTitle(title)
        mainlayout=QGridLayout()
  
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        QObject.connect(self.buttonBox, SIGNAL("rejected()"), self.reject)
        mainlayout.addWidget(self.buttonBox, 0, 0)
         
        QObject.connect(self.buttonBox,SIGNAL("accepted()"),self.ExitRoutine)
    def ExitRoutine(self):
        return
        
def mygetopenfile(parent=None, xpath="%s" % os.getcwd(),markstr='', filename='' ):
    if parent is None:
        xapp = QApplication(sys.argv)
        xparent = QWidget()
        returnfn = unicode(QFileDialog.getOpenFileName(xparent,''.join(['Select file to open:', markstr]),os.path.join(xpath, filename).replace('\\','/')))
        xparent.destroy()
        xapp.quit()
        return returnfn
    return unicode(QFileDialog.getOpenFileName(parent,''.join(['Select file to open: ', markstr]),os.path.join(xpath, filename).replace('\\','/')))

def mygetopenfiles(parent=None, xpath="%s" % os.getcwd(),markstr='', filename='' ):
    if parent is None:
        xapp = QApplication(sys.argv)
        xparent = QWidget()
        returnfns=QFileDialog.getOpenFileNames(xparent,''.join(['Select file to open:', markstr]),os.path.join(xpath, filename).replace('\\','/'))
        xparent.destroy()
        xapp.quit()
    else:
        returnfns=QFileDialog.getOpenFileNames(parent,''.join(['Select file to open: ', markstr]),os.path.join(xpath, filename).replace('\\','/'))
    return [str(s) for s in returnfns]

def mygetsavefile(parent=None, xpath="%s" % os.getcwd(),markstr='', filename='' ):
    if parent is None:
        xapp = QApplication(sys.argv)
        xparent = QWidget()
        returnfn = unicode(QFileDialog.getSaveFileName(xparent,''.join(['Select file for save: ', markstr]),os.path.join(xpath, filename).replace('\\','/')))
        xparent.destroy()
        xapp.quit()
        return returnfn
    return unicode(QFileDialog.getSaveFileName(parent,''.join(['Select file for save: ', markstr]),os.path.join(xpath, filename).replace('\\','/')))

def mygetdir(parent=None, xpath="%s" % os.getcwd(),markstr='' ):
    if parent is None:
        xapp = QApplication(sys.argv)
        xparent = QWidget()
        returnfn = unicode(QFileDialog.getExistingDirectory(xparent,''.join(['Select directory:', markstr]), xpath))
        xparent.destroy()
        xapp.quit()
        return returnfn
    return unicode(QFileDialog.getExistingDirectory(parent,''.join(['Select directory:', markstr]), xpath))
    

def userinputcaller(parent, inputs=[('testnumber', int)], title='Enter values',  cancelallowed=True):
    problem=True
    while problem:
        idialog=userinputDialog(parent, inputs, title)
        idialog.exec_()
        problem=idialog.problem
        if not idialog.ok and cancelallowed:
            return None
        inputs=[(tup[0], tup[1], s) for tup, s  in zip(inputs, idialog.inputstrlist)]
        
    return idialog.ans

class userinputDialog(QDialog):
    def __init__(self, parent, inputs=[('testnumber', int, '')], title='Enter values'):
        super(userinputDialog, self).__init__(parent)
        self.setWindowTitle(title)
        mainlayout=QGridLayout()
        self.parent=parent
        self.inputs=inputs
        self.lelist=[]
        for i, tup in enumerate(self.inputs):
            lab=QLabel()
            lab.setText(tup[0])
            le=QLineEdit()
            if len(tup)>2:
                le.setText(tup[2])
            self.lelist+=[le]
            mainlayout.addWidget(lab, 0, i, 1, 1)
            mainlayout.addWidget(le, 1, i, 1, 1)    
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        mainlayout.addWidget(self.buttonBox, 2, 0, len(inputs), 1)
         
        QObject.connect(self.buttonBox,SIGNAL("accepted()"),self.ExitRoutine)
        
        self.setLayout(mainlayout)
        
        
        QMetaObject.connectSlotsByName(self)
        
        self.problem=False
        self.ok=False

    def ExitRoutine(self):
        self.ok=True
        self.problem=False
        self.ans=[]
        self.inputstrlist=[str(le.text()).strip() for le in self.lelist]
        for s, tup in zip(self.inputstrlist, self.inputs):
            if tup[1]==str:
                try:
                    self.ans+=[s]
                except:
                    self.problem=True
                    break
            else:
                try:
                    n=myeval(s)
                    self.ans+=[tup[1](n)]
                except:
                    self.problem=True
                    break
        if self.problem:
            idialog=messageDialog(self, 'problem with conversion of ' + tup[0])
            idialog.exec_()

#class selectdbsessionsDialog(QDialog):
#    def __init__(self, parent, ex_trange_techl, maxsessions=15, title='Select DB experiment sessions to analyze'):
#        super(selectdbsessionsDialog, self).__init__(parent)
#        self.setWindowTitle(title)
#        mainlayout=QVBoxLayout()
#        
#        self.cblist=[]
#        self.cbinds=[]
#        for count,  (ex, (t0, t1), techl) in enumerate(ex_trange_techl[:maxsessions]):
#            cb=QCheckBox()
#            cb.setText('exp %d: %s to %s, %s' %(ex, str(t0), str(t1), ','.join(techl)))
#            cb.setChecked(False)
#            mainlayout.addWidget(cb)
#            self.cblist+=[cb]
#            self.cbinds+=[[count]]
#        if len(ex_trange_techl)>maxsessions:
#            cb=QCheckBox()
#            ex, (t0, t1), techl=ex_trange_techl[maxsessions]
#            ex2, (t02, t12), techl2=ex_trange_techl[-1]
#            techl=list(set(techl+techl2))
#            cb.setText('exp %d-%d: %s to %s, %s' %(ex, ex2, str(t0), str(t12), ','.join(techl)))
#            cb.setChecked(True)
#            mainlayout.addWidget(cb)
#            self.cblist+=[cb]
#            self.cbinds+=[range(maxsessions, len(ex_trange_techl))]
#        cb.setChecked(True)
#        
#        self.buttonBox = QDialogButtonBox(self)
#        self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
#        self.buttonBox.setOrientation(Qt.Horizontal)
#        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
#        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
#        mainlayout.addWidget(self.buttonBox)
#         
#        QObject.connect(self.buttonBox,SIGNAL("accepted()"),self.ExitRoutine)
#        self.setLayout(mainlayout)
#        QMetaObject.connectSlotsByName(self)
#    def ExitRoutine(self):
#        self.selectinds=[]
#        for cb, l in zip(self.cblist, self.cbinds):
#            if cb.isChecked():
#                self.selectinds+=l
#                



class echem10axesWidget(QDialog):
    def __init__(self, parent=None, ellabels=['A', 'B', 'C', 'D']):
        super(echem10axesWidget, self).__init__(parent)
        
        mainlayout=QVBoxLayout()
        
        self.plotw=plotwidget(self)
        self.plotw.fig.clf()
        self.axl, self.stpl=make10ternaxes(fig=self.plotw.fig, ellabels=ellabels)
        
####        mainlayout.addWidget(self.plotw)
        
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        mainlayout.addWidget(self.buttonBox)
        
        self.setLayout(mainlayout)
    
#    def plot(self, d, cb=True):
#        if 'fomlabel' in d.keys():
#            cblabel=d['fomlabel']
#        else:
#            cblabel=''
#        scatter_10axes(d['comps'], d['fom'], self.stpl, s=18, edgecolors='none', cb=cb, cblabel=cblabel, cmap=d['cmap'], norm=d['norm'])

class echem30axesWidget(QDialog):
    def __init__(self, parent=None, ellabels=['A', 'B', 'C', 'D']):
        super(echem30axesWidget, self).__init__(parent)
        
        mainlayout=QVBoxLayout()
        
        self.plotw=plotwidget(self)
        self.plotw.fig.clf()
        self.axl, self.stpl=make30ternaxes(fig=self.plotw.fig, ellabels=ellabels)
        
        mainlayout.addWidget(self.plotw)
        
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        mainlayout.addWidget(self.buttonBox)
        
        self.setLayout(mainlayout)
    
#    def plot(self, d, cb=True):
#        if 'fomlabel' in d.keys():
#            cblabel=d['fomlabel']
#        else:
#            cblabel=''
#        scatter_30axes(d['comps'], d['fom'], self.stpl, s=18, edgecolors='none', cb=cb, cblabel=cblabel, cmap=d['cmap'], norm=d['norm'])
            

class messageDialog(QDialog):
    def __init__(self, parent=None, title=''):
        super(messageDialog, self).__init__(parent)
        self.setWindowTitle(title)
        mainlayout=QGridLayout()
  
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        QObject.connect(self.buttonBox, SIGNAL("rejected()"), self.reject)
##        mainlayout.addWidget(self.buttonBox, 0, 0)
    
        QObject.connect(self.buttonBox,SIGNAL("accepted()"),self.ExitRoutine)
    def ExitRoutine(self):
        return
        
class plotwidget(FigureCanvas):
    def __init__(self, parent, width=12, height=6, dpi=72, projection3d=False):

        #plotdata can be 2d array for image plot or list of 2 1d arrays for x-y plot or 2d array for image plot or list of lists of 2 1D arrays
        
        self.fig=Figure(figsize=(width, height), dpi=dpi)
        if projection3d:
            self.axes=self.fig.add_subplot(111, navigate=True, projection='3d')
        else:
            self.axes=self.fig.add_subplot(111, navigate=True)
        
        self.axes.hold(True)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        #self.parent=parent
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        #NavigationToolbar(self, parent)
        NavigationToolbar(self, self)
        
        self.mpl_connect('button_press_event', self.myclick)
        self.clicklist=[]
    
    def myclick(self, event):
        if not (event.xdata is None or event.ydata is None):
            arrayxy=[event.xdata, event.ydata]
            print 'clicked on image: array indeces ', arrayxy, ' using button', event.button
            self.clicklist+=[arrayxy]
            self.emit(SIGNAL("genericclickonplot"), [event.xdata, event.ydata, event.button])

