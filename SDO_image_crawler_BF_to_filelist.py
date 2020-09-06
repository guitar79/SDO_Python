# Print software information
# print('Source : https://github.com/seungwonpark/SunSpotTracker')
# Based on python 2.7.12 by Seungwon Park
# change to python 3.6 by guitar79@gs.hs.kr

# get data from https://sdo.gsfc.nasa.gov/assets/img/browse/
# file name structure : 20170228_231038_1024_MHII.jpg
# conda install beautifulsoup

from datetime import datetime, timedelta
from urllib.request import urlopen
from bs4 import BeautifulSoup
# some variables for downloading (site, file, perid and time gap, etc.)
site = 'https://sdo.gsfc.nasa.gov/assets/img/browse/'

#%%
def filename_to_hour(filename):
    fileinfo = filename.split('_')
    return datetime.strptime(fileinfo[0]+fileinfo[1], '%Y%m%d%H%M%S')

#%%
from dateutil.relativedelta import relativedelta
p_start_date = datetime(2012, 1, 1) #convert startdate to date type
p_end_date = datetime(2019, 12, 31)

date_No = 0
date1 = p_start_date
date2 = p_start_date
periods = []
while date2 < p_end_date : 
    date_No += 1
    date2 = date1 + relativedelta(months=1)
    date1_strf = date1.strftime('%Y%m%d')
    date2_strf = date2.strftime('%Y%m%d')
    date = (date1_strf, date2_strf, date_No)
    periods.append(date)
    date1 = date2

#%%
for period in periods:
    startdate = period[0] #start date
    enddate = period[1] #end date
            
    #variable for calculating date
    start_date = datetime.date(datetime.strptime(startdate, '%Y%m%d')) #convert startdate to date type
    end_date = datetime.date(datetime.strptime(enddate, '%Y%m%d')) #convert enddate to date type
    duration = (end_date - start_date).days #total days for downloading
     
    file_lists = ''
    download_file_time = datetime.today() #variable for comparing with downloading filename
    for i in range(duration):
        try : 
            download_date = start_date + timedelta(i)
            directory = download_date.strftime('%Y') + '/' + download_date.strftime('%m') + '/' + download_date.strftime('%d') + '/'
            url = site + directory
            print ('*'*80)
            print ('trying %s ' % url)
            # using BeutifulSoup for crowling
            soup = BeautifulSoup(urlopen(url), "html.parser")
            #print('soup : ', soup)
            pre_list = soup.find_all('pre')
            #print('pre_list', pre_list)
            file_list = pre_list[0].find_all('a')
            #print('file_list', file_list)
            # select file fot downloading
            for i in range(5, len(file_list)):
                filename = file_list[i].text
                file_lists += site + download_date.strftime('%Y/%m/%d/') + filename + '\n'
            
        except Exception as err : 
            with open('./log/crawler_errorlog_{0}_{1}.log'.format(period[0], period[1]), "a") as write_errorlog :
                write_errorlog.write("{0}: {1}, {2}\n".format(datetime.now(), err, url))
            print ('*'*80)
            print(err, url)
    
    with open("../SDO_filelists/SDO_filelist_{0}_{1}.txt".format(startdate, enddate), "w") as text_file:
        text_file.write(file_lists)