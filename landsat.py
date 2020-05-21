# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 15:21:34 2020
Update on Fri Apr 24 13:44:11 2020
@author: Lancine KANTE
@email: kantemou@gmail.com
"""
# import required packages
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from stats_l8_image import nbins


class Landsat8(object):
    """Python module that explore landsat 8 image information, the caracteristic of
    your area interest like image quality, the cloud covery and its period. It can
    tell you when landsat8 will revisite your area of interest in the future.
    """
    def __init__(self):
        self.lanch_date='2013/02/11'
        self.begin_date_world='2013/03/08'
        self.zone=None
        self.flyear = None
        self.frv = None
        self.lvisite = None
        self.wdir = './data/'
        self.gn = self.import_data('world')
        return

    ##  *** Predicte the future visite of landsat satelite **
    def import_data(self,zone='gn',flyear='last'):

        if zone == self.zone and self.flyear == flyear:
            gn=self.gn
        else:
            if 'world'==zone or 'gn'==self.zone:
                if 'all' == flyear:
                    base = 'LANDSAT_8_World_2013_2020.csv'
                elif 'last' == flyear:
                    base = 'LANDSAT_8_World_01-04-2020.csv'
            elif 'gn'==zone or 'world'==self.zone:
                base = 'Guinea_Landsat8oli.csv'
            else:
                base = 'Guinea_Landsat8oli.csv'
#            gn=pd.read_csv(wdir+base,converters={'ADate':parse},dayfirst=True)

            gn=pd.read_csv(self.wdir+base)
            gn.ADate=pd.to_datetime(gn.ADate,dayfirst=True)
            # Set Path and Row as ID of each scene
            gn.LPID=gn.LPID.str.strip('_')

            self.gn = gn
            self.zone = zone
        return gn

    ## *** Find the most and less periode cloud covery ** ##
    def distcloud(self,zone='gn'):
        """Cloud distribution in year per month
        """
#        gn=self.import_data(zone)
        gn=self.gn
        fig = plt.figure()
        ax = fig.add_subplot(121)
#        plt.grid()
        clouds = [100,10,1,0.1,0] # cloud amont in scene
        for i in range(len(clouds)-1):
            gnlc=gn[(gn.SCC<=clouds[i]) & (gn.SCC>clouds[i+1])]
            alpha = 1.0*(i+1)/len(clouds)
            plt.scatter(gnlc.ADate.dt.dayofyear,'SCC',s=10*(i*2+1),marker='o',data=gnlc,alpha=alpha)
            plt.yscale('log') # Set Y axis Semi log
        plt.xlabel('Day of year')
        plt.ylabel('Cloud covery')
#        plt.xlim(1,366)
#        plt.ylim(1,100)
        # Boxplot of cloud covery
        ax = fig.add_subplot(122)
        gn.boxplot('SCC',by=gn.ADate.dt.month,ax=ax)
        plt.ylim(0,100)
        plt.legend((clouds))
        return


    def cloudcovery(self,pathrow=None,zone='gn',period='month',tplot='boxplot'):
        """Plot cloud covery per period
        Parameters: period, tplot
        period: default 'month', it can take 'dayofyea', 'week', 'month'
        tplot: default 'boxplot', it can take 'scatter', 'hist' and 'boxplot'
        """
        # Create periodic variable like, year, month, week, and day
#        gn=self.import_data(zone)
        gn=self.gn
        gn['year']=gn.loc[:,'ADate'].dt.year
        gn['month']=gn.loc[:,'ADate'].dt.month
        gn['week']=gn.loc[:,'ADate'].dt.week
        gn['dayofyear']=gn.loc[:,'ADate'].dt.dayofyear

        if None!=pathrow:
            gn=gn[pathrow==gn.LPID]

        if 'scatter'==tplot:
            plt.scatter(period,'SCC',s=5,marker='o',data=gn,alpha=0.5)
        elif 'boxplot'==tplot:
            gn.boxplot('SCC',by=period,showmeans=True,notch=True)
        elif 'hist'==tplot:
            gn.hist('SCC',by=period,bins=nbins(gn['SCC']),density=True)
        else:
            print "We don't take account this type of graphe or period"
        return

    def vtime(self,pathrow=None,paths=False,zone='gn'):
        """Function that plot the visite time
        """
        # Plot different visite time by year
        if type(None)==type(self.gn):
            gn=self.import_data(zone)
        else:
            gn=self.gn
        if type(pathrow)==list and False==paths:
            gn=gn[gn.LPID.isin(pathrow)]
        elif type(pathrow)==str:
            gn=gn[pathrow==gn.LPID]
        if True==paths:
            self.get_pathrow(zone)
            gn=self.gn
            gn=gn[gn.Path.isin(pathrow)]
        #Get Start and stop time
        gn.loc[:,'StartTime'] = gn.StartTime.str.slice(9)# get bad formating start time
        gn.loc[:,'StartTime']=pd.to_timedelta(gn.StartTime,unit='ns')
        gn['sat']=gn.StartTime.dt.components.hours+gn.StartTime.dt.components.minutes/60+gn.StartTime.dt.components.seconds/3600
        years = gn.ADate.dt.year.sort_values().unique()
        plt.Figure()
        for y in years:
            gny = gn[gn.loc[:,'ADate'].dt.year==y]
            plt.scatter(gny.ADate.dt.dayofyear,gny.sat,s=10)
            plt.legend((years))
        return

    def lesscloud(self,zone='gn'):
        # -- Histogram off SCC -- #
#        gn=self.import_data(zone)
        gn=self.gn
        clouds = [100,10,1,0.1,0] # cloud amont in scene
        for i in range(len(clouds)-1):
            gnlc=gn[(gn.SCC<=clouds[i]) & (gn.SCC>clouds[i+1])]
            gnlc.ADate.dt.dayofyear.hist(bins=nbins(gnlc.ADate.dt.dayofyear),fill=False,
                                histtype='step',density=True,linewidth=i+1)
            plt.legend((clouds))
            print 'Cloud: %1.1f to %1.1f percent %d days'%((clouds[i],clouds[i+1],len(gnlc)))

    def revisite(self,pathrow='199053',enddate='06/2020',zone='gn', history=True, Next=True):
        """Compare real visite and planed visite date of landsat image
        It can tell you the last and next visite date
        @createdate:09 May 2020
        """
#        gn=self.import_data(zone)
        gn=self.gn
        if 0==len(gn[gn.LPID==pathrow]):
            print "Pathrow %s does not exit."%(pathrow)
            print "Please try an other one."
            return
        # Determine real visite date
        real_visite=gn[gn.LPID==pathrow].ADate
        real_visite=real_visite.sort_values()
        real_visite.index=real_visite
        real_visite=real_visite[real_visite<=enddate]
        # First visite according to images
        fvisite=self.rfvisite(pathrow=pathrow,zone=zone)
        # Determine planed visite date
        planed_visite=pd.date_range(start=fvisite,end=enddate,freq='16d')
        planed_visite=pd.DataFrame(planed_visite,columns=['PlanedDate'])
        planed_visite.index=planed_visite.PlanedDate
        rvisite=pd.concat([real_visite,planed_visite],axis=1)
        rvisite['Diff']=rvisite.ADate-rvisite.PlanedDate

        if True==history:
            diff=len(rvisite[~rvisite.Diff.notna()])
            print 'Between %s to %s in scene %s'%((fvisite,enddate,pathrow))
            print 'There are %d missing image'%(diff)
        if True==Next:
            today=datetime.date.today()
            enddate=str('%d/%d'%((today.month+1,today.year)))
            today=str('%d/%d/%d'%((today.day,today.month,today.year)))
            today=pd.to_datetime(today,dayfirst=True)
            rvisite['Delta']=rvisite.PlanedDate-today
#            print rvisite.Delta.sort_values(ascending=False)[0:3]
            near_visite=rvisite.sort_values(by='Delta',ascending=False)[0:3]
            last_visite=near_visite[near_visite.Delta.dt.days<0].sort_values(by='Delta',ascending=False)
            last_visite=last_visite.iloc[0,:].PlanedDate
            print 'The last visite was on %s the %s %s %d'%(
                    (last_visite.day_name(),last_visite.day,last_visite.month_name(),last_visite.year))
            next_visite=near_visite[near_visite.Delta.dt.days>=0].sort_values(by='Delta',ascending=True)
            if 0==next_visite.iloc[0,:].Delta.days:
                print 'Great! Today you can download a new image'
            elif 1==next_visite.iloc[0,:].Delta.days:
                print 'Great! Tomorrow you can download a new image'
            else:
                print 'Great! about %d days, you can download a new image'%(next_visite.iloc[0,:].Delta.days)
            next_visite=next_visite.iloc[0,:].PlanedDate
            print 'The next visite will be on %s the %s %s %d'%(
                    (next_visite.day_name(),next_visite.day,next_visite.month_name(),next_visite.year))
            # Estimate cloud covery of the next visite
            nxday=gn[(gn.LPID==pathrow) & (gn.ADate.dt.month==next_visite.month) & (gn.ADate.dt.day==next_visite.day)].loc[:,['ADate','SCC']]
            print nxday
            next_visite=str('%d/%d/%d'%((next_visite.day,next_visite.month,next_visite.year)))
            next_visite=pd.to_datetime(today,dayfirst=True)
            cloud=gn[(gn.LPID==pathrow) & (gn.ADate.dt.month==next_visite.month)].loc[:,['ADate','SCC']]
            print 'In this month the cloud covery is: min:%1.2f, mean:%1.2f, max:%1.2f'%(
                    (cloud.SCC.min(),cloud.SCC.mean(),cloud.SCC.max()))
            print cloud
#            self.cloudcovery(pathrow=pathrow,tplot='boxplot',period='month')
        return near_visite
#        return rvisite

    def fvisite(self,path=None,row=None,pathrow=None,zone='gn'):
        """Get the first visite of landsat 8 for all or a specific scene
        @createdate:09 May 2020
        """
#        gn=self.import_data(zone)
        gn=self.gn
        if type(pathrow)==list:
            gn=gn[gn.LPID.isin(pathrow)]
            ids = gn.LPID.sort_values().unique()
            fvs=pd.DataFrame(columns=['LPID','FV'])
            for i in ids:
                fv=gn[gn.LPID==i].ADate.min()
                fvs=fvs.append({'LPID':i,'FV':fv}, True)
                if 0==i and 2<=len(ids): # Show progress text for multiple scene
                    print "Please wait it's in progress... "
                elif len(ids)-1==i and 2<=len(ids):
                    print "Thank's it done. See your data "
        elif type(pathrow)==str:
            gn=gn[pathrow==gn.LPID]
            fvs=gn[pathrow==gn.LPID].ADate.min()
            fvs=str(fvs.date())
        else:
            print "Scene %s does'nt exit, Please try a other one"%(pathrow)
            return
        return fvs

    def rfvisite(self,pathrow=None,zone='gn',rfv_id=True,fvr=True,irfvs=False):
        """
        Get regular first visite of landsat 8 at scene
        @createdate: 10 May 2020
        fvr: first visite regular, default True
        rfv_id: reference of regular first visite, default True
        irfvs: irregular first visites, default False
        """
#        gn=self.import_data(zone)
        gn=self.gn
        rv=gn[gn.LPID==pathrow].ADate.sort_values(ascending=True)
        try:
            fv=self.fvisite(pathrow=pathrow,zone=zone)
        except:
            return
        pv=pd.date_range(start=fv,end='2014',freq='16d')
        pv=pd.DataFrame(pv,columns=['PlanedDate'])
        rv.index=range(len(rv))
        pv.index=range(len(pv))
        irv=pd.concat([rv,pv],axis=1)
        irv['Diff']=irv.ADate-irv.PlanedDate
        if 0==len(irv[(abs(irv.Diff.dt.days)>0) & (abs(irv.Diff.dt.days)<16)]):
            print 'Scene: %s, regular images at begin %s '%((pathrow,fv))
            if True==fvr:
                return fv
        else:
            if True==rfv_id:
                return pathrow
            else:
                irv=irv.sort_values(by='ADate')
                # drop the duplicated value and conserve the first one
                ix=irv.Diff.drop_duplicates().index
                unic=irv.iloc[ix,:]
                unic=unic[~unic.Diff.isna()]
                ix=unic.index # original index of dataframe
                ix=range(len(ix)) #  reindex for iteration
                unic.index=ix
                uix=[] # usefull index, that not meet landsat planed visite
                for i in range(len(unic.Diff)-1):
                    der=unic.Diff.dt.days[i+1]-unic.Diff.dt.days[i]
                    mod=der%16
                    if 0!=mod: # Take seconds regular visite dates
                        uix.append(i+1)
                print 'Irregular images from %s to %s'%((fv,str(unic.loc[uix[-1],'ADate'].date())))
                print '   Scene: %s is Regular since %s'%((pathrow,str(unic.loc[uix[-1],'ADate'].date())))
                if True==irfvs:
                    print unic.iloc[uix,:]
                return str(unic.loc[uix[-1],'ADate'].date())

    def get_irvisite(self,zone='gn',plot=False):
        """
        Get irregular visite scene of landsat
        @createdate: 12 May 2020
        """
#        gn=self.import_data(zone)
        gn=self.gn
        pathrows=gn.LPID.sort_values().unique()
        iprs=[]
        for pathrow in pathrows:
            fv=self.fvisite(pathrow=pathrow,data=zone)
            rfv=self.rfvisite(pathrow=pathrow,data=zone,fvr=True,rfv_id=False)
            try:
                iprs.append([pathrow,fv,rfv])
            except:
                continue
        iprs=pd.DataFrame(iprs,columns=['LPID','FV','RFV'])
        iprs=iprs[iprs.notnull()]
        iprs.index=range(len(iprs))
        # Add underscore after and before LPID to maintain string type
        iprs['ID']='_'+iprs.LPID+'_'
        iprs.to_csv(self.wdir+'FRV_2013_04-2020_1.csv')

        if True==plot or 'world'==zone:
            x=gn[gn.LPID.isin(iprs[iprs.FV!=iprs.RFV].LPID)].CenterLongdec
            y=gn[gn.LPID.isin(iprs[iprs.FV!=iprs.RFV].LPID)].CenterLatdec
            plt.Figure()
            plt.scatter(x=gn.CenterLongdec,y=gn.CenterLatdec,s=1,c='b',alpha=0.2)
            plt.scatter(x=x,y=y,s=1.5,c='r',alpha=0.3)
        return iprs

    def get_nvisite(self,flyear='last'):
        """ Get the paths from wich landsat 8 will pass today
        """
        if  None!=self.frv:
            fvr=self.frv
        else:
            if 'all'==flyear:
                fvr=pd.read_csv(self.wdir+'FRV_2013_04-2020.csv',index_col=0)
                fvr.LPID=fvr.ID.str.strip('_')
                fvr.drop(columns='ID',inplace=True)
                fvr.FV=pd.to_datetime(fvr.FV,dayfirst=True)
                fvr.RFV=pd.to_datetime(fvr.RFV,dayfirst=True)
            elif 'last'==flyear:
                fvr=pd.read_csv(self.wdir+'L8_Last_visite_04-2020.csv',index_col=0)
                fvr['RFV']=pd.to_datetime(fvr.LPV,dayfirst=True)
        paths=fvr.PATH.sort_values().unique()
        last_rvisites = []
        today_paths = []
        for path in paths:
            d=fvr[path==fvr.PATH]
            lfv=str(d.RFV.sort_values(ascending=False).dt.date.max())

            today=datetime.date.today()
            enddate=str('%d/%d'%((today.month+1,today.year)))
            today=str('%d/%d/%d'%((today.day,today.month,today.year)))
            today=pd.to_datetime(today,dayfirst=True)

            planed_visite=pd.date_range(start=lfv,end=enddate,freq='16d')
            planed_visite=pd.DataFrame(planed_visite,columns=['PlanedDate'])
            planed_visite['Diff_to_now']=planed_visite.PlanedDate-today
            planed_visite.sort_values('Diff_to_now',ascending=False,inplace=True)
            last_rvisites.append([path,lfv,str(planed_visite.iloc[0,0].date())])
            if 0!=len(planed_visite[0==planed_visite.Diff_to_now.dt.days]):
                today_paths.append(path)
        if 'all'==flyear:
            last_rvisites=pd.DataFrame(last_rvisites,columns=['Path','LRFV','LPV'])
            last_rvisites.to_csv(self.wdir+'L8_Last_visite.csv')
        self.get_pathrow('world')
        return today_paths

    def get_pathrow(self,zone):
        if type(None)==type(self.gn):
            gn=self.import_data('world')
        else:
            gn=self.gn
        gn.loc[:,'Path'], gn.loc[:,'Row'] =gn.LPID.str.slice(0,3), gn.LPID.str.slice(3,6)
        gn.Path=pd.Series(gn.Path,index=gn.index,dtype='int64')
        gn.Row=pd.Series(gn.Row,index=gn.index,dtype='int64')
        self.gn=gn
        return
