# -*- coding: utf-8 -*-
"""
Created on Sun May 17 14:46:24 2020
@author: Lancine KANTE
"""

# Function that detemine number of bins for histogram
def nbins(d):
    try:
        bw=((4*d.std()**5)/(3*len(d)))**0.2 # bins width for histogram
        bins=int(round((max(d)-min(d))/bw))
        return bins
    except:
        print 'bins value not calculated, please check your data!'
    return

def normality(d,category=None,plot=False):
    """ This function cherk the normality of landsat image band of
    your target. You can specific the different category of the target
    as text
    """
    if None!=category:
        d=d[d.Color==category]
        d=d.drop(columns='Color') #delete string column
    # Fetch all columns to test data normality
    for col in d.columns:
        df=d.loc[:,col] # Band 1 of image
        # Check data normality manualy
        if df.mean().round(4)==df.median().round(4):
            print '\n Columns %s follow a normal distribution'%(col)
            print 'Its Mean %1.4f equal %1.4f Median'%(df.mean(),df.median())

            if False!=plot: # Plot histogram if data follow normal distribution
                mu,sigma=df.mean(),df.std()
                # Generate the random variable following the pdf
                dfnorm=np.random.normal(mu,sigma,len(df))
                fig=plt.figure()
                ax=fig.add_subplot(121) #
                stats.probplot(df,dist='norm',plot=plt,rvalue=True)
                ax=fig.add_subplot(122) #
                sns.distplot(df,bins=self.nbins(df),norm_hist=True,ax=ax)
                sns.distplot(dfnorm,bins=self.nbins(df),ax=ax,hist_kws={"alpha":0.25})
        else: # --- Print mode, median and mean --- #
            print "\n Column %s don't follow a normal distribition"%(col)
            print '    mode: %1.4f'%(max(df.mode()))
            print '  median: %1.4f'%(df.median())
            print '    mean: %1.4f'%(df.mean())
    return


# **** 3D vusialisation **** #
def band3dplot(self,bx,by,bz,data=None,endmember=None):
    '''3D Scatter plot for 3 band of image, like landsat8 OLI image
    To compare them and make good decision
    Paramaters: bx,by,bz
    '''
    mpl.rcParams['font.size'] = 12
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for t, c, m, in [('Dark','k', 'o') # For dark
                    ,('Light','r', 'o') # For light
                    ,('Trans','g', 'o',) # For trans
                    ]:
        # Take one class in data according to its color
        df=data[data.Color==t]
        a, b, z = bx, by, bz
        xs = np.array(df.loc[:,a])
        ys = np.array(df.loc[:,b])
        zs = np.array(df.loc[:,z])
        ax.scatter(xs, ys, zs, c=c, marker=m,s=10)

        if endmember:
        # Take a endmember of previous class to plot
            ed=endmember[endmember.Color==t]
            xs = np.array(ed.loc[:,a])
            ys = np.array(ed.loc[:,b])
            zs = np.array(ed.loc[:,z])
            ax.scatter(xs, ys, zs, c=c, marker=m,s=200)

    ax.set_xlabel(a)
    ax.set_ylabel(b)
    ax.set_zlabel(z)
    plt.title('3D plot of %s, %s and %s'%(a,b,z),{'fontsize':18})
#        fig.tight_layout()
#        plt.show()
    return
