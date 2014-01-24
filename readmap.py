# DESCRIPTION:
# Function "mapsvg(f, s, ml, allch)" takes a text plate map with filename 'f' and optional marker list 'ml' of sample IDs then outputs an SVG with filename 's'. SVG canvas size is defined by dpx, dpy below.
# When called with a marker list, red circles will be drawn around the listed samples. The marker list is also enumerated A...Z (max 26 markers) with letters printed over the corresponding samples.
# Optional boolean 'allch' for drawing spots from all 8 printer channels.

# requires numpy and svgwrite modules
import numpy
#import svgwrite

## DEFINE plate size (mm)
dpx = 152.4
dpy = 101.6

# function for evaluating None, NaN, and strip leading zeros
def myeval(c):
    if c=='None':
        c=None
    elif c=='nan' or c=='NaN':
        c=numpy.nan
    else:
        temp=c.lstrip('0')
        if (temp=='' or temp=='.') and '0' in c:
            c=0
        else:
            c=eval(temp)
    return c

# read platemap.txt (csv format) and return list of dictionaries; get keys from last line before start of data (find first line that doesn't start with '%', choose one line up)
def readsingleplatemaptxt(p):
    f=open(p, mode='r')
    lsold=f.readlines()
    f.close()
    ls=[]
    for line in lsold:
		if not line.strip():
			continue
		else:
			ls.append(line)
    for count, l in enumerate(ls, start=0):
        if not l.startswith('%'):
			break
	keys=ls[count][1:].split(',')
    keys=[(k.partition('(')[0]).strip() for k in keys]
    dlist=[]
    for l in ls[count:]:
        sl=l.split(',')
        d=dict([(k, myeval(s.strip())) for k, s in zip(keys, sl)])
        dlist+=[d]
    return dlist

# convert CMYK colorspace (ABCD compositions) to RGB format
def cmyk_to_rgb(c,m,y,k,gs):
	r = int(255 * (1-c) * (1-k))
	g = int(255 * (1-m) * (1-k))
	b = int(255 * (1-y) * (1-k))
	if gs:
		gray = int(numpy.dot([r, g, b], [0.3, 0.59, 0.11]))
		return (gray, gray, gray)
	else:
		return (r, g, b)

# take plate txt "f", save to svg "s"
def mapsvg(f, s, ml=None, allch=False, gs=False):
	# read plate map into list of dictionaries
	d = readsingleplatemaptxt(f)

	# create svg file
#	svg_document = svgwrite.Drawing(filename = s,
#									size = (str(dpx) + 'mm', str(dpy) + 'mm'))
#
#	# check if we're drawing all 8 channels, then parse list and write samples into svg
#	for count, sample in enumerate(d, start=0):
#		if allch:
#			rgbstr = "rgb" + str(cmyk_to_rgb(d[count]['A'] + d[count]['E'], d[count]['B'] + d[count]['F'], d[count]['C'] + d[count]['G'], d[count]['D'] + d[count]['H'], gs))
#		else:
#			rgbstr = "rgb" + str(cmyk_to_rgb(d[count]['A'], d[count]['B'], d[count]['C'], d[count]['D'], gs))
#		svg_document.add(svg_document.rect(insert = tuple((str(d[count]['x']) + 'mm', str(dpy - d[count]['y']) + 'mm')),
#											size = tuple((str(d[count]['dx']) + 'mm', str(d[count]['dy']) + 'mm')),
#											stroke_width = "0",
#											fill = rgbstr))
#	
#	# circle selected sample_id's in red, add text
#	if ml and len(ml) <= 26:
#		abc = map(chr, range(65, 91))
#		for count, sid in enumerate(ml):
#			svg_document.add(svg_document.circle(center = tuple((str(d[sid-1]['x'] + d[sid-1]['dx']*0.5) + 'mm', str(dpy - d[sid-1]['y'] + d[sid-1]['dy']*0.5) + 'mm')),
#												r = str(0.75*d[sid-1]['dx']) + 'mm',
#												stroke_width = "1",
#												stroke = "red",
#												fill = "none"))
#			svg_document.add(svg_document.text(text = abc[count],
#												insert = tuple((str(d[sid-1]['x'] - 1) + 'mm', str(dpy - d[sid-1]['y'] + d[sid-1]['dy'] + 1) + 'mm')),
#												fill = "red",
#												style = "font-size:6px; font-family:Monospace; font-weight:bold"))
#	elif ml and len(ml) > 26:
#		print 'More markers than alphabet. Shorten marker list to 26 elements or less'
#
#	svg_document.save()
