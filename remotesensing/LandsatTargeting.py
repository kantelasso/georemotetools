# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 15:21:34 2020

@author: Lancine KANTE
"""
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pandas.plotting import scatter_matrix
import seaborn as sns
from scipy import stats
#import pylab
#from pan(das.tools.plotting import scatter_matrix


wdir='C:/Correction/LC08_20180122/Vegetation/VegTarget/' # working directory
# Target Endmemer reflectance data
edf=pd.read_csv(wdir+'EndmemberAnaClass.csv')

# Target population reflectance data
d1=pd.read_csv(wdir+'AnaDark.csv')
d1=pd.read_csv(wdir+'ManguierDark.csv')
#d1=pd.read_csv(wdir+'AnaDarkTargetDetection.csv')
d1['Color']="Dark"
d2=pd.read_csv(wdir+'AnaLight.csv')
d2=pd.read_csv(wdir+'ManguierLight.csv')
#d2=pd.read_csv(wdir+'AnaLightTargetDetection.csv')
d2['Color']="Light"
d3=pd.read_csv(wdir+'AnaTrans.csv')
#d3=pd.read_csv(wdir+'AnaTransTargetDetection.csv')
d3['Color']="Trans"
d=pd.concat([d1,d2,d3])
d=d.iloc[:,6:]

d.describe().round(3)

scatter_matrix(d)
d.plot.kde('B5',by='Color')
d.boxplot(by='Color')
d.boxplot('B1',by='Color')
d.boxplot('B2',by='Color')
d.boxplot('B3',by='Color')
d.boxplot('B6',by='Color')

d.plot.scatter('B1','B2',by='Color',c=['r','g','b'])
d.plot.scatter('B2','B3',by='Color',c=['r','g','b'])
d.plot.scatter('B5','B6',by='Color',c=['r','g','b'])

d.plot.scatter('B4','B5',by='Color',c=['r','g','b'])


i=0
for i in range(7):
    sns.distplot(d.iloc[:,i],bins=25)
i=0
for i in range(7):
    sns.violinplot(d.iloc[:,:i])



# Function that detemine bins for histogram
def nbins(d):
    bw=((4*d.std()**5)/(3*len(d)))**0.2 # bins width for histogram
    bins=((max(d)-min(d))/bw) # bins for histogram
    if 200>len(d):
        bins=10
    elif 250<len(d):
        bins=25
    elif 1000<len(d):
        bins=bins*10
    return int(bins)

def normality(d,category=None,plot=False):
    if None==category:
        dd=d
    else:
        dd=d[d.Color==category]
    #delete string column
    dd=dd.drop(columns='Color')
    # Fetch all columns to test normality of data
    for col in dd.columns:
        df=dd.loc[:,col] # Band 1 of image
        mu,sigma=df.mean(),df.std()
        # Generate the random variable following the pdf
        dfnorm=np.random.normal(mu,sigma,len(df))
        # Check data normality
        if df.mean().round(4)==df.median().round(4):
            print '\n Columns %s follow a normal distribution'%(col)
            print 'Its Mean %1.4f equal %1.4f Median'%(df.mean(),df.median())

            if True==plot: # Plot histogram if data follow normal distribution
                fig=plt.figure()
                fig.add_subplot(121) #
                stats.probplot(df,dist='norm',plot=plt,rvalue=True)
                fig.add_subplot(122) #
                sns.distplot(df,bins=int(nbins(df)),norm_hist=True)
                sns.distplot(dfnorm,bins=int(nbins(df)),hist_kws={"alpha":0.25})
            # --- Print mode, median and mean --- #
        else:
            print "\n Column %s don't follow a normal distribition"%(col)
            print '    mode: %1.4f'%(max(df.mode()))
            print '  median: %1.4f'%(df.median())
            print '    mean: %1.4f'%(df.mean())
    return

# **** 3D vusialisation **** #
def band3dplot(bx,by,bz):
    '''3D Scatter plot for 3 band of image, like landsat8 OLI image
    To compare them and make good decision
    '''
    mpl.rcParams['font.size'] = 12
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for t, c, m, in [('Dark','k', 'o') # For dark
                    ,('Light','r', 'o') # For light
                    ,('Trans','g', 'o',) # For trans
                    ]:
        # Take one class in data according to his color
        df=d[d.Color==t]
        a, b, z = bx, by, bz
        xs = np.array(df.loc[:,a])
        ys = np.array(df.loc[:,b])
        zs = np.array(df.loc[:,z])
        ax.scatter(xs, ys, zs, c=c, marker=m,s=10)

        # Take a endmember off previous class to plot
        ed=edf[edf.Color==t]
        xs = np.array(ed.loc[:,a])
        ys = np.array(ed.loc[:,b])
        zs = np.array(ed.loc[:,z])
        ax.scatter(xs, ys, zs, c=c, marker=m,s=200)

    ax.set_xlabel(a)
    ax.set_ylabel(b)
    ax.set_zlabel(z)
    plt.title('3D plot of %s, %s and %s'%(a,b,z),{'fontsize':18})
    fig.tight_layout()
    #fig.legend()
    plt.show()
    return

##  *** Predicte the future visite of landsat satelite **
# Landsat 8
import numpy as np
import pandas as pd
import dateutil
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
#from pandas.io.data import DataReader
from dateutil.parser import parse

lanch_date='2013/02/11'
begin_date_world='2013/04/11'
begin_date='2013/04/14'

wdir='D:/Landsat/Data/'
gn=pd.read_csv(wdir+'Guinea_Landsat8oli.csv',converters={'Acquisition Date':parse})
col_name=pd.read_csv(wdir+'Landsat8oli_col_name.csv') # new simplify column name
gn.columns=col_name.columns # set simplify column name to database

# Start and stop time
time=gn.iloc[:,12:14] # get bad formating start time and stop time
time.columns=['sat','sot']
time.sat=time.sat.str.slice(9) # formating start time
time.sot=time.sot.str.slice(9) # formating stop time
time.sat.str.split(':')[:][1]

gn.iloc[:,12]=time.sat # reset start time to original database
gn.iloc[:,13]=time.sot # reset stop time to original database

times=pd.to_datetime(time.sat)
gn['sat']=times.dt.hour+times.dt.minute/60+times.dt.second/3600
times=pd.to_datetime(time.sot)
gn['sot']=times.dt.hour+times.dt.minute/60+times.dt.second/3600
gn.hist('sat',by='WRSPath',bins=50)
gn[(gn.WRSPath==199) & (gn.WRSRow==53)].sat.describe()

gn['month']=gn.loc[:,'ADate'].dt.month
gn['year']=gn.loc[:,'ADate'].dt.year
gn['dayofyear']=gn.iloc[:,2].dt.dayofyear
gn['week']=gn.iloc[:,2].dt.week

plt.scatter('ADate','SCC',s=5,marker='o',data=gn)
plt.scatter('week','SCC',s=5,marker='o',data=gn,alpha=0.5)
plt.scatter('dayofyear','SCC',s=5,marker='o',data=gn,alpha=0.5)

gn.boxplot('SCC',by='week',showmeans=True,notch=True)
gn.boxplot('SCC',by='month',showmeans=True,notch=True,whis=0.5)

gn.hist('SCC',by='month',bins=25,density=True)

gn16=gn[gn.iloc[:,2].dt.year<2017]
gn13=gn[gn.iloc[:,2].dt.year==2013]
gn13.plot('dayofyear','SCC',marker='o')
gn13.plot('ADate','SCC',marker='o')


# Plot different visite time by year
years = gn.ADate.dt.year.unique()
for y in years:
    gny = gn[gn.iloc[:,2].dt.year==y]
    plt.scatter(gny.dayofyear,gny.sat,s=10)
    plt.xlim=(0,366)
    plt.legend((years))


# *** --- Get the uncovery cloud days of year --- *** #
# SCC = Scene Cloud Covery of landsat 8 image
# -- Scatter plot dayofyear vs SCC -- #
def cloudcovery(data=gn):
    gn=data
    fig = plt.figure()
    ax = fig.add_subplot(121)
    plt.grid()
    #clouds = [100,50,25,10,5,1,0.1,0] # cloud amont in scene
    clouds = [100,10,1,0.1,0] # cloud amont in scene
    for i in range(len(clouds)-1):
        gnlc=gn[(gn.SCC<=clouds[i]) & (gn.SCC>clouds[i+1])]
        alpha = 1.0*(i+1)/len(clouds)
        plt.scatter('dayofyear','SCC',s=10*(i*2+1),marker='o',data=gnlc,alpha=alpha)
        plt.yscale('log') # Set Y axis Semi log
    plt.legend((clouds))
    plt.xlabel('Day of year')
    plt.ylabel('Cloud covery %')
    plt.xlim(0,366)
    plt.ylim(0,100)
    # Boxplot of cloud covery
    ax = fig.add_subplot(122)
    gn.boxplot('SCC',by='month',ax=ax)
    plt.ylim(0,100)
    return
# -- Histogram off SCC -- #
clouds = [100,10,1,0.1,0] # cloud amont in scene
for i in range(len(clouds)-1):
    gnlc=gn[(gn.SCC<=clouds[i]) & (gn.SCC>clouds[i+1])]
    alpha = 1.0*(i+1)/len(clouds)
    gnlc.dayofyear.hist(bins=nbins(gnlc.dayofyear),fill=False,histtype='step',density=True)
#    gnlc.dayofyear.hist(bins=nbins(gnlc.dayofyear),alpha=0.8/(i+1))
#    plt.legend((clouds))
    print 'Cloud: %1.1f to %1.1f percent %d days'%((clouds[i],clouds[i+1],len(gnlc)))

# Create dataframe index for landsat8 covery zone
#paths = [198,199,200,201,202,203,204]
#rows = [51,52,53,54,55]
paths, rows = gn.WRSPath.unique(), gn.WRSRow.unique()
pr=[]
for p in paths:
    for r in rows:
        gnlc=gn[(gn.WRSPath==p) & (gn.WRSRow==r)]
        print 'Path is %d, and Row is %d'%((p,r))
        gnlc.boxplot('SCC',by='month')
#        plt.scatter('dayofyear','SCC',s=10*(i*2+1),marker='o',data=gnlc,alpha=0.25)
#        gnlc.dayofyear.hist(bins=25,density=True,histtype='bar',grid=False)
        pr.append(p*100+r)
        plt.legend((pr))
        break

begin_dates=['23/04/2013','14/04/2013','21/04/2013',
             '12/04/2013','05/05/2013','18/03/2013','10/04/2013']
aq_times=[]
dt=pd.date_range(start='14/04/2013',end='2020',freq='16d')
dt=pd.DataFrame(dt)


# Create a function that get first visite for every area
ids = gn.LPID.unique()
ids.sort()
fvs=pd.DataFrame(columns=['LPID','FV'])
for i in range(len(ids)):
    gnlc=gn[gn.LPID==ids[i]]
    fv=gnlc.ADate.min()
    fvs=fvs.append({'LPID':ids[i],'FV':fv}, True)
    if 0==i:
        print "Please wait it's in progress... "
    elif len(ids)-1==i:
        print "Thank's it done. See your data "

#    print 'LPID:  %s, firt visite %s'%((ids[i],fv))
#    break

pathrows=gn.LPID.sort_values().unique()
iprs=[]
for pr in pathrows:
    ipr=lsa.rfvisite(pathrow=pr,data='world')
#    ipr=lsa.rfvisite(pathrow=pr,data='gn')
    try:
        iprs.append(ipr)
    except:
        continue

iprs=pd.Series(iprs)
iprn=iprs[iprs.notnull()]
iprn.index=range(len(iprn))

# Analyser les irreguliere par rapport a leur path ou row
rows=gn[gn.LPID.isin(iprs)].WRSRow
nrow=len(gn.WRSRow.unique())
paths=gn[gn.LPID.isin(iprs)].WRSPath
npath=len(gn.WRSPath.unique())
#gn.WRSPath.plot.hist(bins=len(gn.WRSPath.unique()))
fig=plt.figure()
plt.hist(gn.WRSRow,bins=nrow,color='b')
plt.hist(rows,bins=nrow,color='r',stacked=True)

fig=plt.figure()
x=gn[gn.LPID.isin(iprs)].CenterLongdec
y=gn[gn.LPID.isin(iprs)].CenterLatdec
plt.scatter(x=gn.CenterLongdec,y=gn.CenterLatdec,s=1,c='b',alpha=0.5)
plt.scatter(x=x,y=y,s=1.5,c='r',alpha=0.5)



#pchange=[]
#for i in ip:
#    unic,uix=lsa.rfvisite(pathrow=i,data='world')
#    print 'For %s There are %d change during flying'%((i,len(uix)))
#    pchange.append([i,len(uix)])
