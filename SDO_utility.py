# Print software information
# print('Source : https://github.com/seungwonpark/SunSpotTracker')
# Based on python 2.7.12 by Seungwon Park
# change to python 3.6 by guitar79@gs.hs.kr

# get data from https://sdo.gsfc.nasa.gov/assets/img/browse/
# file name structure : 20170228_231038_1024_MHII.jpg
# conda install beautifulsoup

import os
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup

site = 'https://sdo.gsfc.nasa.gov/assets/img/browse/'
    
def write_log(log_file, log_str):
    with open(log_file, 'a') as log_f:
        log_f.write(log_str+'\n')
    return print (log_str)
#for checking time
cht_start_time = datetime.now()
def print_working_time():
    working_time = (datetime.now() - cht_start_time) #total days for downloading
    return print('working time ::: %s' % (working_time))

def filename_to_hour(filename):
    fileinfo = filename.split('_')
    return datetime.strptime(fileinfo[0]+fileinfo[1], '%Y%m%d%H%M%S')

def SDO_image_list_to_filelist_1day(save_dir_name, date):
    add_log = True
    if add_log == True :
        log_file = 'SDO_image_list_to_filelist.log'
        err_log_file = 'SDO_image_list_to_filelist_err.log'

    downloaddate = date[0] #start date

            
    #variable for calculating date
    download_date = datetime.date(datetime.strptime(downloaddate, '%Y%m%d')) #convert downloaddate to date type
    
    file_lists = '#this file is created by guitar79@naver.com\n'
     
    download_date = download_date
    if os.path.isfile("{0}SDO_filelist_{1}.txt"\
                      .format(save_dir_name, download_date.strftime('%Y%m%d'))) :
        write_log(log_file, "{2} ::: {0}SDO_filelist_{1}.txt is laready exist."\
                  .format(save_dir_name, download_date.strftime('%Y%m%d'), datetime.now()))
    else : 
        try : 
            
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
                
            with open("{0}SDO_filelist_{1}.txt".format(save_dir_name, download_date.strftime('%Y%m%d')), "w") as text_file:
                text_file.write(file_lists)
                write_log(log_file, "{2}: {0}SDO_filelist_{1}.txt is created".format(save_dir_name, download_date.strftime('%Y%m%d'), datetime.now()))
            
        except Exception as err : 
            write_log(err_log_file, "{2}: {0}, {1}\n".format(err, url, datetime.now()))

def SDO_image_downloader_from_filelist(SDO_filelist, targets, request_hour):
    import urllib.request
    add_log = True
    if add_log == True :
        log_file = 'SDO_image_download_from_filelist.log'
        err_log_file = 'SDO_image_download_from_filelist_err.log'
    # Open the file with read only permit
    f = open(SDO_filelist,'r')
    all_text = f.read()
    url_lists = all_text.split('\n')
    
    # close the file after reading the lines.
    f.close()

    
    
    for url_list in url_lists:    
    
        if url_list[:8] == 'https://' and url_list[-4:] == '.jpg':
            
            url_el = url_list.split('/')
            filename = url_el[-1]
            filename_el = filename.split('_')
            
            for target in targets : 
                save_dir_name = '../{0}/'.format(target)
                if not os.path.exists(save_dir_name):
                    os.makedirs(save_dir_name)
                    print ('*'*80)
                    print ('{0} is created.'.format(save_dir_name))
                
                if target == '{0}_{1}'.format(filename_el[-2], filename_el[-1]) \
                    and int(filename_to_hour(filename).strftime('%H')) in request_hour :
                
                    if os.path.exists('%s/%s' % (save_dir_name, filename)):
                        print ('*'*40)
                        print ('{0} is exist'.format(filename))
                    
                    else :
                    
                        try : 
                            print ('Trying %s' % filename)
                            urllib.request.urlretrieve(url_list, '{0}{1}'.format(save_dir_name, filename))
                            write_log(log_file, "{2}: {0}{1} is downloaded.".format(save_dir_name, filename, datetime.now()))
                            print ('Downloading' + filename)
                            
                        except Exception as err : 
                            write_log(err_log_file, "{2}: {0}, {1}\n".format(err, url_list, datetime.now()))
                            
                else:
                    print ('Skipping ' + filename)                
            
        
            
    
    