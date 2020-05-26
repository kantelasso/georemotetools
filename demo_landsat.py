# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:54:43 2020
@author: hp
"""

# Import Run Module
#%run landsat.py
import landsat as lsat
lsa=lsat.Landsat8()
gn=lsa.import_data(zone='world',flyear='last')
#lsa.distcloud()
#lsa.cloudcovery()
#lsa.vtime('199053',zone='world')
today_path=lsa.get_nvisite()
lsa.vtime(today_path,paths=True,zone='world')
#lsa.lesscloud()
lsa.fvisite('199053',zone='world')
rv=lsa.revisite('199053',enddate='07/2020',zone='world')

lsa.fvisite(pathrow='199053',zone='world')
lsa.rfvisite(pathrow='199053',zone='world')
lsa.rfvisite(pathrow='199053',zone='world')
#ip=lsa.get_irvisite(zone='world')
#%run l8_realtime_fly.py
