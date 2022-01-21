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
import SDO_utilities

# some variables for downloading (site, file, perid and time gap, etc.)
site = 'https://sdo.gsfc.nasa.gov/assets/img/browse/'

#this tpye of image will be added
targets = ['2048_HMII.jpg','1024_HMII.jpg', '1024_0304.jpg', '1024_4500.jpg', 
           '1024_HMIIB.jpg', '1024_HMIIC.jpg', '1024_0171.jpg', '1024_0131.jpg'] 

targets = ['4096_HMII.jpg', '2048_HMII.jpg', '1024_HMII.jpg'] 

time_gap = 1 #time gap
request_hour = range(0,24,time_gap) #make list
    
filelist_dir_name = '../SDO_lists/'
save_dir_name = '../SDO_list_groupby/'
if not os.path.exists(save_dir_name):
    os.makedirs(save_dir_name)
    print ('*'*80)
    print ('{0} is created.'.format(save_dir_name))
                    
SDO_filelists = sorted(glob(os.path.join('{0}SDO_filelist_*.txt'
                                         .format(filelist_dir_name))))

url_lists = []
for SDO_filelist in SDO_filelists:    
    # Open the file with read only permit
    f = open(SDO_filelist,'r')
    lines = f.readlines()
    for line in lines:
        url_lists.append(line)
    # close the file after reading the lines.
    f.close()

add_log = True
if add_log == True :
    log_file = 'group_by_image_SDO_filelist.log'
    err_log_file = 'group_by_image_SDO_filelist.log'
        
for target in targets :
    
    results = '''#this file is created from all filelist
#time gap is in {0}.
#target file is {1}
#contact guitar79@naver.com
'''.format(request_hour, target)

    for url_list in url_lists:
        try : 
            url_list = url_list.rstrip()
            if url_list[:8] == 'https://' and url_list[-4:] == '.jpg':
        
                url_el = url_list.split('/')
                filename = url_el[-1]
                filename_el = filename.split('_')
                                
                if target == '{0}_{1}'.format(filename_el[-2], filename_el[-1]) \
                    and int(SDO_utilities.filename_to_hour(filename).strftime('%H')) in request_hour :

                    print ('adding %s' % filename)
                    results += '{0}\n'.format(url_list)
                    SDO_utilities.write_log(log_file, '{1}: {0} is added.'\
                          .format(filename, datetime.now()))
                else:
                    print ('Skipping ' + filename)
                    
        except Exception as err : 
            SDO_utilities.write_log(err_log_file, '{2}: {0}, {1}'\
                  .format(err, url_list, datetime.now()))
                
    with open('{0}{1}.txt'.format(save_dir_name, target), 'w') as f:
        #write
    	f.write(results)
    SDO_utilities.write_log(log_file, '{2} : {0}{1}.txt is created'\
          .format(save_dir_name, target, datetime.now()))
                    