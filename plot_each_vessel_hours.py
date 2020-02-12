#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 13:08:35 2020
Plot each vessels' raw data of hours
Input:each vessels' raw data of hours
Output:time series plot of temp and depth of each vessels' raw data of hours

@author: Mingchao
"""
import matplotlib.pyplot as plt
import os
import pandas as pd
import zlconversions as zl
import matplotlib.dates as dates
import datetime
import matplotlib
#Hardcodes
Hours_save='/home/jmanning/Mingchao/result/Hours_data/'


def plot(vessel_lists,Hours_save,new_df,dpi=300):
#def plot(vessel_lists,Hours_save,new_df,linewidth=2,linestyle='--',color='y',alpha=0.5,marker='d',markerfacecolor='y',dpi=300):
        name=vessel_lists[i].split('/')[6].split('_hours')[0]
        MIN_T=min(new_df['temp'])
        MAX_T=max(new_df['temp'])
        MIN_D=min(new_df['depth'])
        MAX_D=max(new_df['depth'])
        diff_temp=MAX_T-MIN_T
        diff_depth=MAX_D-MIN_D
        if diff_temp==0:
            textend_lim=0.1
        else:
            textend_lim=diff_temp/8.0
        if diff_depth==0:
            dextend_lim=0.1
        else:
            dextend_lim=diff_depth/8.0
        #fig=plt.figure()#11.69,8.27))
        fig=plt.figure(figsize=[11.69,8.27])
        size=min(fig.get_size_inches())        
        fig.suptitle(name,fontsize=3*size, fontweight='bold')
        #ax1=fig.add_axes()#[0.12, 0.52, 0.76,0.36])
        #ax2=fig.add_axes()#[0.12, 0.12, 0.76,0.36])
        ax1=fig.add_subplot(211)
        ax2=fig.add_subplot(212)
        ax1.set_title(new_df['time'][0]+' to '+new_df['time'][len(new_df)-1])
        #ax1.plot_date(new_df['time'],new_df['temp'],linewidth=linewidth,linestyle=linestyle,color=color,alpha=alpha,marker=marker,markerfacecolor=markerfacecolor)
        #ax1.plot_date(new_df['time'][0::60],new_df['temp'][0::60],linewidth=linewidth,linestyle=linestyle,color=color,alpha=alpha,marker=marker,markerfacecolor=markerfacecolor)
        ax1.plot(new_df['new_time'][0::60],new_df['temp'][0::60],color='b')
        #ax1.plot(new_df['time'],new_df['temp'],color='b')#[0::60] #every minutes
        ax1.legend(prop={'size': 1.5*size})
        ax1.set_ylabel('Celsius',fontsize=2*size)
        ax1.set_ylim(MIN_T-textend_lim,MAX_T+textend_lim)
        ax1.axes.get_xaxis().set_visible(False)
        #ax2.plot_date(new_df['time'],new_df['depth'],linewidth=linewidth,linestyle=linestyle,color='R',alpha=alpha,marker=marker,markerfacecolor='R')
        #ax2.plot_date(new_df['time'][0::60],new_df['depth'][0::60],linewidth=linewidth,linestyle=linestyle,color='R',alpha=alpha,marker=marker,markerfacecolor='R')
        #ax2.plot(new_df['time'][0::60],new_df['depth'][0::60],color='R')
        #new_df['new_time']=pd.to_datetime(new_df['new_time'])
        ax2.plot(new_df['new_time'][0::60],new_df['depth'][0::60],color='R')
        ax2.legend(prop={'size':1.5* size})
        ax2.set_ylabel('depth(m)',fontsize=2*size)
        ax2.set_ylim(MAX_D+dextend_lim,MIN_D-dextend_lim)
        #ax2.tick_params(labelsize=1.5*size)
        #plt.gca().xaxis.set_major_locator(plt.MaxNLocator(10))
        ax2.xaxis.set_major_locator(plt.MaxNLocator(10))
        #ax2.xaxis.set_major_locator(plt.AutoLocator())
        plt.gca().xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d'))
        #fig.autofmt_xdate()
        plt.gcf().autofmt_xdate()
        if not os.path.exists(os.path.join(Hours_save+vessel_lists[i].split('/')[6].split('_hours')[0]+'/')):
            os.makedirs(Hours_save+vessel_lists[i].split('/')[6].split('_hours')[0]+'/')
        plt.savefig(os.path.join(Hours_save+vessel_lists[i].split('/')[6].split('_hours')[0]+'/')+vessel_lists[i].split('/')[6].split('_hours')[0]+'_hours.ps',dpi=dpi,orientation='landscape')
        plt.savefig(os.path.join(Hours_save+vessel_lists[i].split('/')[6].split('_hours')[0]+'/')+vessel_lists[i].split('/')[6].split('_hours')[0]+'_hours.png',dpi=dpi,orientation='portait')
        plt.show()
        
#main
hours_lists=zl.list_all_files(Hours_save)
vessel_lists=[]#store the path of every vessel's file
#Loop every vessel's file and Plot
for file in hours_lists:
   if file[len(file)-9:]=='hours.csv':
     vessel_lists.append(file)                
     for i in range(len(vessel_lists)):
         vessel_df=pd.read_csv(vessel_lists[i])
         plot(vessel_lists=vessel_lists,Hours_save=Hours_save,new_df=vessel_df,dpi=300)           

                    