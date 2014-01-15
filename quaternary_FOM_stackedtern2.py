import matplotlib.cm as cm
import numpy
import pylab
import h5py
import operator, copy, os


#pylab.rc('font',**{'family':'serif''serif':['Times New Roman']})
#pylab.rcParams['font.family']='serif'
#pylab.rcParams['font.serif']='Times New Roman'
pylab.rc('font', family='serif', serif='Times New Roman')
#os.chdir('C:/Users/Gregoire/Documents/PythonCode/ternaryplot')
from myternaryutility import TernaryPlot
from myquaternaryutility import QuaternaryPlot


def make10ternaxes(ellabels=['A', 'B', 'C', 'D']):

    ax_xc=[]
    ax_yc=[]
    xcdel=[.22, .19, .1, .04, .04, .05, .03, .03, .03, .03]
    ax_yc=[.5, .6, .36, .65, .49, .33, .67, .55, .445, .32]
    for i in range(10):
        if i==0:
            ax_xc+=[xcdel[i]]
        else:
            ax_xc+=[ax_xc[-1]+xcdel[i]]
        #ax_yc+=[.5+((i%2)*2.-1.)*((i>0)*.1+.072*i/10)]

    shape1=numpy.array([.35, 1.])
    fig=pylab.figure(figsize=(12, 8))

    axl=[]
    for i, xc, yc in zip(range(1, 11), ax_xc, ax_yc):
        w, l=shape1/i
        axl+=[fig.add_axes([xc-w/2, yc-l/2, w, l])]


    stpl=[]
    xpos=[.27]*10
    xpos[0:3]=[.35, .29, .28]
    xpos[-1]=.26
    for count, (ax, xp) in enumerate(zip(axl, xpos)):
        stp=TernaryPlot(ax, ellabels=ellabels[:3], offset=.03)
        stp.label(fontsize=17)#,fontdict={'fontname':'Times New Roman'})
        stpl+=[stp]
        
        
        if count<9:
            stp.ax.text(xp, .8, '%s$_{%.2f-%.2f}$' %(ellabels[3], (count*.1), ((count+1)*.1)-.01), ha='right', va='center', fontsize=17)
        else:
            stp.ax.text(xp, .8, '%s$_{%.2f-%d}$' %(ellabels[3], (count*.1), 1), ha='right', va='center', fontsize=17)
    return axl, stpl



def scatter_10axes(comps, fom, stpl, s=18, **kwargs):
    abc=comps[:, :3]
    abc[abc.sum(axis=1)==0.]=numpy.array([1., 1., 1.])/3.
    abc=numpy.array([c/c.sum() for c in abc])
    d=comps[:, 3]
    d30=numpy.round(d*30.)
    dlims=numpy.array([0., 1., 2., 3.])
    marks=[('o', 1., 1.), ('D', .9, .7),('s', .8, .5)]
    sl=s*numpy.array([2.3, 1., .55, .4, .4, .45, .4, .5, .8, 1., 1.5])
    for i, (stp, sv) in enumerate(zip(stpl, sl)):
        dl=dlims+(i*3.)
        if i==9:
            dl[-1]+=.01
        for a, b, (m, sf, al) in zip(dl, dl[1:], marks):
            inds=numpy.where((d30>=a) & (d30<b))[0]
            #print a, b, len(inds)
            if len(inds)>0:
                stp.scatter(abc[inds], c=fom[inds], marker=m, s=sv*sf, alpha=al, **kwargs)


