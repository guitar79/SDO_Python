# Print software information
# print('Source : https://github.com/seungwonpark/SunSpotTracker')
# Based on python 2.7.12 by Seungwon Park
# change to python 3.6 by guitar79@gs.hs.kr

# get data from https://sdo.gsfc.nasa.gov/assets/img/browse/
# file name structure : 20170228_231038_1024_MHII.jpg
# conda install beautifulsoup

from glob import glob
from datetime import datetime
import os
import urllib.request
import SDO_utilities

log_dir = "logs/"
log_file = "{}{}.log".format(log_dir, os.path.basename(__file__)[:-3])
err_log_file = "{}{}_err.log".format(log_dir, os.path.basename(__file__)[:-3])
print ("log_file: {}".format(log_file))
print ("err_log_file: {}".format(err_log_file))

# some variables for downloading (site, file, perid and time gap, etc.)
site = 'https://sdo.gsfc.nasa.gov/assets/img/browse/'

#this tpye of image will be added
img_sizes = [4096, 3072, 2048, 1024, 512]
chls = ['HMII', 'HMIB', 'HMIBC', 'HMIIC', 'HMIIF',
        '4500', '0335', '1600', '1700', '0211', '0193'
        '0131', '0171', '0304', '0094'
        '211193171', '211193171n', '211193171rg']

for dir in chls :
    #dir = chls[0]
    base_dr = "../4096_{}".format(dir)
    fullnames = SDO_utilities.getFullnameListOfallFiles(base_dr)
    SDO_filelists = sorted(glob(os.path.join('../SDO_filelists/SDO_filelist_*.txt')))
    for SDO_filelist in SDO_filelists:
        #read_filename = 'SDO_filelist_20120101_20120201.txt'
        read_filename = SDO_filelist
        read_file = open(read_filename,'r')
        raw_lists = read_file.read()
        url_lists = raw_lists.split('\n')
        #print(url_lists) #debug
        
        read_filename_element1 = read_filename.split('.')
        #print(read_filename_element1) #debug
        #break
        read_filename_element2 = read_filename_element1[-2].split('_')
        download_date = read_filename_element2[-1] 
        #print(download_date) #debug
        
        #convert download date to datetime.date type
        DT_download_date = datetime.date(datetime.strptime(download_date, '%Y%m%d')) 
        
        #print(DT_download_date) #debug
        
    #%%    
        print ('*'*80)
        
    
    for url_list in url_lists[1:]:
        try : 
            #'https://sdo.gsfc.nasa.gov/assets/img/browse/2010/05/19/20100519_091114_1024_0193.jpg',
            SDO_url_element = url_list.split('/')
            SDO_filename = SDO_url_element[-1]
            SDO_filename_element = SDO_filename.split('_')
            #print(filename) #debug
            
            save_folder = "../SDO_images/{}/{}/{}/{}/".format(SDO_filename_element[0][:4], 
                                                           SDO_filename_element[0],
                                                           SDO_filename_element[-1][:4],
                                                           SDO_filename_element[-2])
            #print(save_folder) #debug
            
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)
                print ('='*80)
                print (save_folder, 'is created')
                
                             
            try : 
                print ('Trying {}'.format(SDO_filename))
                if os.path.exists('{}{}'.format(save_folder, SDO_filename)):
                    print ('#'*40)
                    print ('{} is exist'.format(SDO_filename))
                else :
                    print ('*'*60)
                    print ('Downloading {}'.format(SDO_filename))
                    urllib.request.urlretrieve(url_list, '{}{}'.format(save_folder, SDO_filename))
                        
            except Exception as err : 
                with open('./log/download_error_{0}.log'.format(read_filename_element1[-2][-21:]), "a") as download_errorlog :
                    download_errorlog.write("{0}: {1}, {2}\n".format(datetime.now(), err, url_list))
                    print ('#'*40)
                    print (err, url_list)
            
        except Exception as err : 
            with open('./log/download_error_{0}.log'.format(read_filename_element1[-2][-21:]), "a") as download_errorlog :
                download_errorlog.write("{0}: {1}, {2}\n".format(datetime.now(), err, SDO_filelist))
            print ('#'*40)
            print(err, SDO_filelist)