# Print software information
# print('Source : https://github.com/seungwonpark/SunSpotTracker')
# Based on python 2.7.12 by Seungwon Park
# change to python 3.6 by guitar79@gs.hs.kr

# get data from https://sdo.gsfc.nasa.gov/assets/img/browse/
# file name structure : 20170228_231038_1024_MHII.jpg
# conda install beautifulsoup

from datetime import datetime
import os
import urllib.request
import SDO_utilities
import csv

#this tpye of image will be added
img_sizes = [4096, 3072, 2048, 1024, 512]
chls = ['0131', '0171', '0193', '0211',
        '0304', '0094', '0335', '1600', '1700', '0211', '4500', 
        'HMIB', 'HMIBC', 'HMID', 'HMII', 'HMIIC', 'HMIIF']
        #'211193171', '211193171n', '211193171rg']
        
# some variables for downloading (site, file, perid and time gap, etc.)
                        
filelist_dir_name = '../SDO_list_groupby/'
download_filename = '4096_HMII.jpg.csv' 

save_dir_name = '../{0}/'.format(download_filename[:-4])
if not os.path.exists(save_dir_name):
    os.makedirs(save_dir_name)
    print ('*'*80)
    print ('{0} is created.'.format(save_dir_name))
else : 
    print ('*'*80)
    print ('{0} is already exist.'.format(save_dir_name))
    
add_log = True
if add_log == True :
    log_file = 'SDO_image_download_from_filelist_groupby.log'
    err_log_file = 'SDO_image_download_from_filelist_groupby_err.log'
    
# Open the file with read only permit
with open('{0}{1}'.format(filelist_dir_name, download_filename), 'r') as f:
  reader = csv.reader(f)
  url_lists = list(reader)
#print(your_list) 
#%%
for i in range(len(url_lists)):
    url_list = url_lists[i][1]
    if url_list[:8] == 'https://' and url_list[-4:] == '.jpg':

        url_el = url_list.split('/')
        filename = url_el[-1]
        filename_el = filename.split('_')
        
        if os.path.exists('%s/%s' % (save_dir_name, filename)):
            print ('*'*40)
            print ('{0} is exist'.format(filename))
        
        else :
        
            try : 
                print ('Trying %s' % filename)
                urllib.request.urlretrieve(url_list, '{0}{1}'.format(save_dir_name, filename))
                SDO_utilities.write_log(log_file, '{2}: {0}{1} is downloaded.'\
                      .format(save_dir_name, filename, datetime.now()))
                print ('Downloading {0}'.format(filename))
                
            except Exception as err : 
                SDO_utilities.write_log(err_log_file, "{2}: {0}, {1}\n".format(err, url_list, datetime.now()))
                
    else:
        print ('Skipping ' + url_list)