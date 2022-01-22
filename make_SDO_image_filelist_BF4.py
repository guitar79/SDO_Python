# Print software information
# print('Source : https://github.com/seungwonpark/SunSpotTracker')
# Based on python 2.7.12 by Seungwon Park
# change to python 3.6 by guitar79@gs.hs.kr

# get data from https://sdo.gsfc.nasa.gov/assets/img/browse/
# file name structure : 20170228_231038_1024_MHII.jpg
# conda install beautifulsoup

import os
from datetime import datetime
import SDO_utilities

log_dir = "logs/"
log_file = "{}{}.log".format(log_dir, os.path.basename(__file__)[:-3])
err_log_file = "{}{}_err.log".format(log_dir, os.path.basename(__file__)[:-3])
print ("log_file: {}".format(log_file))
print ("err_log_file: {}".format(err_log_file))

# some variables for downloading (site, file, perid and time gap, etc.)
site = 'https://sdo.gsfc.nasa.gov/assets/img/browse/'
   
from dateutil.relativedelta import relativedelta
p_start_date = datetime(2010, 5, 1) #convert startdate to date type
p_end_date = datetime(2021, 12, 31)

dates = [p_start_date]
date1 = p_start_date
while date1 < p_end_date : 
    date1 += relativedelta(days=1)
    dates.append(date1)    

print(dates)

save_dir_name = '../SDO_filelists_by_date/'
if not os.path.exists('{0}'.format(save_dir_name)):
    os.makedirs('{0}'.format(save_dir_name))
    print ('*'*80)
    print ('{0} is created'.format(save_dir_name))
else :
    print ('*'*80)
    print ('{0} is exist'.format(save_dir_name))

n = 0            
for download_date in dates:
    #download_date = dates[0]
    n += 1
    print('#'*40,
            "\n{2:.01f}%  ({0}/{1}) {3}".format(n, len(dates), (n/len(dates))*100, os.path.basename(__file__)))
    print ("Starting...   download_date: {}".format(download_date))

    if os.path.isfile("{0}SDO_filelist_{1}.txt"\
                .format(save_dir_name, download_date.strftime('%Y%m%d'))) :
            print("{2} ::: {0}SDO_filelist_{1}.txt is laready exist."\
                .format(save_dir_name, download_date.strftime('%Y%m%d'), datetime.now()))
    else : 

        try : 
            file_lists = SDO_utilities.SDO_image_list_to_filelist_1day(save_dir_name, download_date)
            
            '''
            from bs4 import BeautifulSoup
            from urllib.request import urlopen
            file_lists = '#this file is created by guitar79@naver.com\n'
            
                #directory = download_date.strftime('%Y') + '/' + download_date.strftime('%m') + '/' + download_date.strftime('%d') + '/'
                directory = download_date.strftime('%Y/%m/%d/')
                url = site + directory
                print ('*'*80)
                print ('trying %s ' % url)
                
                # using BeutifulSoup for crowling
                soup = BeautifulSoup(urlopen(url), "html.parser")
                print('soup: {}'.format(soup))
                
                # 
                table_list = soup.find_all('table')
                print('table_list: {}'.format(table_list))
                
                #
                file_list = table_list[0].find_all('a')
                print('file_list', file_list)
                
                # select file fot downloading
                for i in range(5, len(file_list)):
                    filename = file_list[i].text
                    file_lists += site + download_date.strftime('%Y/%m/%d/') + filename + '\n'
            '''

            print("file_lists: {}".format(file_lists))

            with open("{0}SDO_filelist_{1}.txt".format(save_dir_name, download_date.strftime('%Y%m%d')), "w") as text_file:
                text_file.write(file_lists)
                SDO_utilities.write_log(log_file, "{2}: {0}SDO_filelist_{1}.txt is created".format(save_dir_name, download_date.strftime('%Y%m%d'), datetime.now()))
                    
        except Exception as err : 
            SDO_utilities.write_log(err_log_file, "{1}: {0}\n".format(err, datetime.now()))