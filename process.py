#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 12:41:35 2018
funtion, contact the raw_data_download.py,classify_by_boat.py
check_reformat_data.py and match_tele_raw.py
finally: output the plot and statistics every week

Mar 3,2020 Mingchao
    1.append emolt_no_telemetry every week
    2.the telemetry data have wrong lat and lon,but raw data have right lat and lon,we will compare them and put right raw data in emolt_no_telemetry
@author: leizhao
"""

import raw_tele_modules as rdm
from datetime import datetime,timedelta
import os
import pandas as pd
import upload_modules as up

def week_start_end(dtime,interval=0):
    '''input a time, 
    if the interval is 0, return this week monday 0:00:00 and next week monday 0:00:00
    if the interval is 1,return  last week monday 0:00:00 and this week monday 0:00:00'''
    delta=dtime-datetime(2003,1,1,0,0)-timedelta(weeks=interval)    #datetime(2003,1,1,0,0) is wednesday 0:00:00
    count=int(delta/timedelta(weeks=1))
    start_time=datetime(2003,1,1,0,0)+timedelta(weeks=count)
    end_time=datetime(2003,1,1,0,0)+timedelta(weeks=count+1)   
    return start_time,end_time    #start_time and end_time is different week wednesday morning 0:00:00
def main():
    realpath=os.path.dirname(os.path.abspath(__file__))
    #parameterpath=realpath.replace('py','parameter')
    #HARDCODING
    output_path=realpath.replace('py','result')  #use to save the data 
    picture_save=output_path+'/stats/' #use to save the picture
    emolt='https://www.nefsc.noaa.gov/drifter/emolt.dat' #this is download from https://www.nefsc.noaa.gov/drifter/emolt.dat, 
    #telemetry_status=os.path.join(parameterpath,'telemetry_status.csv')
    #telemetry_status='/home/jmanning/Mingchao/parameter/telemetry_status.csv'
    telemetry_status='/home/jmanning/leizhao/programe/aqmain/parameter/telemetry_status.csv'
    emolt_raw_save='/home/jmanning/Mingchao/result'#output emolt_raw.csv
    emolt_raw_path='/home/jmanning/Mingchao/result/emolt_raw.csv'#input emolt_raw.csv 
    emolt_no_telemetry_save='/home/jmanning/Mingchao/result'#output emolt_no_telemetry.csv
    path='https://www.nefsc.noaa.gov/drifter/emolt.dat'#input emolt.dat
    lack_data_path='/home/jmanning/leizhao/programe/raw_data_match/result/lack_data.txt'
    # below hardcodes is the informations to upload local data to student drifter. 
    subdir=['stats']    
    mremote='/Raw_Data'
    remote_subdir=['stats']
    ###########################
    end_time=datetime.now()#input local time,in match_tele_raw will change to UTCtime
    #end_time=datetime.now()-timedelta(days=346)
    #start_time,end_time=week_start_end(end_time,interval=1)
    start_time=end_time-timedelta(weeks=1)
    #start_time=end_time-timedelta(days=1460)
    #start_time=end_time-timedelta(days=557)
    if not os.path.exists(picture_save):
        os.makedirs(picture_save)
    print('match telemetered and raw data!')
    #match the telementry data with raw data, calculate the numbers of successful matched and the differnces of two data. finally , use the picture to show the result.
    dict=rdm.match_tele_raw(os.path.join(output_path,'checked'),path_save=os.path.join(picture_save,'statistics'),telemetry_path=emolt,telemetry_status=telemetry_status,\
                        emolt_raw_save=emolt_raw_save,start_time=start_time,end_time=end_time,dpi=500,lack_data=lack_data_path)
    tele_df=rdm.read_telemetry(path)#get emolt.dat
    emolt_raw_df=pd.read_csv(emolt_raw_path,index_col=0)#get emolt_raw.csv
    #create a DataFrame for store emolt_no_telemetry
    emolt_no_telemetry_DF=pd.DataFrame(data=None,columns=['vessel','datet','lat','lon','depth','depth_range','hours','mean_temp','std_temp'])
    #compare with emolt_raw.csv and emolt.dat to get emolt_no_telemetry.csv
    #emolt_no_telemetry_result=rdm.emolt_no_telemetry_df(tele_df=tele_df,emolt_raw_df=emolt_raw_df,year_now=2019,emolt_no_telemetry_df=emolt_no_telemetry_DF)
    emolt_no_telemetry_result=rdm.emolt_no_telemetry_df(tele_df=tele_df,emolt_raw_df=emolt_raw_df,emolt_no_telemetry_df=emolt_no_telemetry_DF)
    #according to columns,drop_duplicates
    emolt_no_telemetry_result=emolt_no_telemetry_result.drop_duplicates(['vessel','datet'])
    #get the rest of emolt_raw_df,it's emolt_no_telemetry
    emolt_no_telemetry_result=rdm.subtract(df1=emolt_raw_df,df2=emolt_no_telemetry_result,columns=['vessel','datet','lat','lon','depth','depth_range','hours','mean_temp','std_temp'])
    #emolt_no_telemetry_result.index=range(len(emolt_no_telemetry_result))
    #count ['std_temp'] and ['mean_temp'] again,get number likes that 12.33
    for i in emolt_no_telemetry_result.index:
        emolt_no_telemetry_result['std_temp'][i]="{:.2f}".format(emolt_no_telemetry_result['std_temp'][i]/100)
        emolt_no_telemetry_result['mean_temp'][i]="{:.2f}".format(emolt_no_telemetry_result['mean_temp'][i]/100)
    #emolt_no_telemetry_result=emolt_no_telemetry_result.sort_values(by=['vessel','datet'])
    #emolt_no_telemetry_result.index=range(len(emolt_no_telemetry_result))
    #save emolt_no_telemetry.csv
    if not os.path.exists(emolt_no_telemetry_save):
        os.makedirs(emolt_no_telemetry_save)
    #append every week
    emolt_no_telemetry=pd.read_csv(os.path.join(emolt_no_telemetry_save,'emolt_no_telemetry.csv'))
    emolt_no_telemetry=emolt_no_telemetry.append(emolt_no_telemetry_result)
    emolt_no_telemetry=emolt_no_telemetry.sort_values(by=['vessel','datet'])
    emolt_no_telemetry.index=range(len(emolt_no_telemetry))
    emolt_no_telemetry.to_csv(os.path.join(emolt_no_telemetry_save,'emolt_no_telemetry.csv'))
    #emolt_no_telemetry_result.to_csv(os.path.join(emolt_no_telemetry_save,'emolt_no_telemetry.csv'))
    tele_dict=dict['tele_dict']
    raw_dict=dict['raw_dict']
    record_file_df=dict['record_file_df']
    index=tele_dict.keys()
    print('match telemetered and raw data finished!')
    print("start draw map")
    raw_d=pd.DataFrame(data=None,columns=['time','filename','mean_temp','mean_depth','mean_lat','mean_lon'])
    tele_d=pd.DataFrame(data=None,columns=['time','mean_temp','mean_depth','mean_lat','mean_lon'])
    for i in index:
        for j in range(len(record_file_df)): #find the location of data of this boat in record file
            if i.lower()==record_file_df['Boat'][j].lower():
                break
        if len(raw_dict[i])==0 and len(tele_dict[i])==0:
            continue
        else:
            raw_d=raw_d.append(raw_dict[i])
            tele_d=tele_d.append(tele_dict[i])
            rdm.draw_map(raw_dict[i],tele_dict[i],i,start_time,end_time,picture_save,dpi=300)
            rdm.draw_time_series_plot(raw_dict[i],tele_dict[i],i,start_time,end_time,picture_save,record_file_df.iloc[j],dpi=300)
    raw_d.index=range(len(raw_d))
    tele_d.index=range(len(tele_d))
    rdm.draw_map(raw_d,tele_d,'all_map',start_time,end_time,picture_save,dpi=300)

    for i in range(len(subdir)):
        local_dir=os.path.join(output_path,subdir[i])
        remote_dir=os.path.join(mremote,remote_subdir[i])
        up.sd2drf(local_dir,remote_dir,keepfolder=True)  # need to keep subdirectry
if __name__=='__main__':
    main()