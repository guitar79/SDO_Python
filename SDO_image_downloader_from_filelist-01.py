# Print software information
# print('Source : https://github.com/seungwonpark/SunSpotTracker')
# Based on python 2.7.12 by Seungwon Park
# change to python 3.6 by guitar79@gs.hs.kr

# get data from https://sdo.gsfc.nasa.gov/assets/img/browse/
# file name structure : 20170228_231038_1024_MHII.jpg
# conda install beautifulsoup

from glob import glob
from datetime import datetime
import pandas as pd
import os
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
chls = ['0131', '0171', '0193', '0211',
        '0304', '0094', '0335', '1600', '1700', '0211', '4500', 
        'HMIB', 'HMIBC', 'HMID', 'HMII', 'HMIIC', 'HMIIF']
        #'211193171', '211193171n', '211193171rg']

targets = []
for img_size in img_sizes :
    for chl in chls : 
        targets.append('{0}_{1}'.format(str(img_size), chl))

SDO_filelists = sorted(glob(os.path.join('{0}SDO_filelist_*.txt'.format(filelist_dir_name))))

for SDO_filelist in SDO_filelists:
    
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

    time_gap = 1 #time gap
    request_hour = range(0,24,time_gap) #make list
    
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
                    and int(SDO_utilities.filename_to_hour(filename).strftime('%H')) in request_hour :
                
                    if os.path.exists('%s/%s' % (save_dir_name, filename)):
                        print ('*'*40)
                        print ('{0} is exist'.format(filename))
                    
                    else :
                    
                        try : 
                            print ('Trying %s' % filename)
                            urllib.request.urlretrieve(url_list, '{0}{1}'.format(save_dir_name, filename))
                            SDO_utilities.write_log(log_file, "{2}: {0}{1} is downloaded.".format(save_dir_name, filename, datetime.now()))
                            print ('Downloading' + filename)
                            
                        except Exception as err : 
                            SDO_utilities.write_log(err_log_file, "{2}: {0}, {1}\n".format(err, url_list, datetime.now()))
                            
                else:
                    print ('Skipping ' + filename)