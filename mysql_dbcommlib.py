import MySQLdb, MySQLdb.cursors
import numpy, pylab
import time, datetime
import os, sys

sys.path.append(os.path.expanduser("C:/Users/Public/Documents/PythonCode/PythonCodeSecureFiles"))
from url import url

class dbcomm():
    def __init__(self, url=url, user='',password='',db='hte_echemdrop_proto'):
        self.db=MySQLdb.connect(url, user, password, db, cursorclass = MySQLdb.cursors.SSCursor)
        self.cursor=self.db.cursor()

    def execute_getsinglerow(self, query):
        self.cursor.execute(query)
        for row in self.cursor:break#assumes only 1 row
        for xrow in self.cursor:continue
        return row

    def dbstrcvt(self, val, cvtstr=None):
        if not isinstance(val, str):
            if not cvtstr is None:
                val= cvtstr %val
            else:
                val=`val`
        return val
        
    def getnumrecords(self, filterfield, filterval, valcvtcstr=None):
        filterval=self.dbstrcvt(filterval, valcvtcstr)
        query = 'select count(*) from data where %s = %s' %(filterfield, filterval)
        row=self.execute_getsinglerow(query)
        return row[0]

    def getallrecordids(self, filterfield, filterval, valcvtcstr=None):
        filterval=self.dbstrcvt(filterval, valcvtcstr)
        data_ids=[]
        if filterfield is None:
            query = 'select id from data'
        else:
            query = 'select id from data where %s = %s' %(filterfield, filterval)
        self.cursor.execute(query)
        for row in self.cursor:
            data_ids.append(row[0])
        return data_ids
    
    def getallplateids(self, filterfield, filterval, valcvtcstr=None):
        filterval=self.dbstrcvt(filterval, valcvtcstr)
        data_ids=[]
        if filterfield is None:
            query = 'select plate_id from data'
        else:
            query = 'select plate_id from data where %s = %s' %(filterfield, filterval)
        self.cursor.execute(query)
        for row in self.cursor:
            data_ids.append(row[0])
        return data_ids

    def getrecordids_created(self, plateid, dt0, dt1):
        data_ids=[]
        query = 'select id from data where plate_id = %d and created_at >= "%s" and created_at < "%s"' % (plateid, str(dt0),str(dt1)) 
        self.cursor.execute(query)
        for row in self.cursor:
            data_ids.append(row[0])
        return data_ids
        
    def getrowdict_fields(self, filterfield, filterval, fields, recordnum=0, valcvtcstr=None):
        #print recordnum
        filterval=self.dbstrcvt(filterval, valcvtcstr)
        query='select %s from data where %s = %s limit %d, 1;'% (', '.join(fields), filterfield, filterval, recordnum)
        row=self.execute_getsinglerow(query)
        d=dict([tup for tup in zip(fields,row)])
        return d
    
    def getdlist_fields(self, filterfield, filterval, fields, recnums=None, valcvtcstr=None):
        filterval=self.dbstrcvt(filterval, valcvtcstr)
        dlist=[]
        if recnums is None:
            recnums=self.getallrecordids(filterfield, filterval)
        for data_id in recnums:
            query = 'select %s from data where id = %d;' % (', '.join(fields), data_id)
            self.cursor.execute(query)
            for row in self.cursor:
                dlist.append(dict([tup for tup in zip(fields,row)]))
        return dlist

    def getarrd_scalarfields(self, filterfield, filterval, fields, recnums=None, valcvtcstr=None):
        filterval=self.dbstrcvt(filterval, valcvtcstr)
        arrd=dict([(f, []) for f in fields])
        if recnums is None:
            recnums=self.getallrecordids(filterfield, filterval)
        for data_id in recnums:
            query = 'select %s from data where id = %d;' % (', '.join(fields), data_id)
            self.cursor.execute(query)
            garbage=[arrd[f].append(v) for row in self.cursor for f, v in zip(fields,row)]
        for k, v in arrd.iteritems():
            arrd[k]=numpy.array(v)
        return arrd
        
    def getdatapath_id(self, id):
        d=self.getrowdict_fields('id', id, ['plate_id','dc_data__t_v_a_c_i'], valcvtcstr='%d')
        p=os.path.join(os.path.join('J:/hte_echemdrop_proto/data','%d' %d['plate_id']),d['dc_data__t_v_a_c_i'])
        return p

    """ Closes both the connection and the crusor. Closing only the the db
        connection can lead to errors. """
    def close(self):
        self.cursor.close()
        self.db.close()
        


#t=time.time()
#
#dbc=dbcomm(user='',password='',db='hte_echemdrop_proto')
#fields=['id', 'sample_no','created_at', 'experiment_no', 'technique_name', 'dc_data__t_v_a_c_i']
#plate_id=401
#ids=dbc.getallrecordids('plate_id', plate_id, valcvtcstr='%d')
#d=dbc.getarrd_scalarfields('plate_id', plate_id, fields, valcvtcstr='%d')
#
#print 'ready to read files ', time.time()-t
#t=time.time()
#
#print 'Readine the sample_no'
#t=time.time()
#for id in d['id'][:10]:
#    dbc.getrowdict_fields('id', id, ['sample_no'], recordnum=0, valcvtcstr='%d')
#    print id, time.time()-t
#    t=time.time()
#print 'READING 10 bytes each file'
#l10=[]
#
#for fn in d['dc_data__t_v_a_c_i'][:10]:
#    p=os.path.join(os.path.join('J:/hte_echemdrop_proto/data','%d' %plate_id),fn)
#    print p, time.time()-t
#    t=time.time()
#    try:
#        f=open(p, mode='r')
#    except:
#        try:
#            print 'error'
#            f=open(p, mode='r')
#        except:
#            print 'error'
#            f=open(p, mode='r')
#    l10+=[f.read(10)]
#    f.close()
#
#print 'READING each file'
#l=[]
#
#for fn in d['dc_data__t_v_a_c_i'][:10]:
#    p=os.path.join(os.path.join('J:/hte_echemdrop_proto/data','%d' %plate_id),fn)
#    print p, time.time()-t
#    t=time.time()
#    try:
#        f=open(p, mode='r')
#    except:
#        try:
#            print 'error'
#            f=open(p, mode='r')
#        except:
#            print 'error'
#            f=open(p, mode='r')
#    l+=[f.read()]
#    f.close()
#dbc.db.close()
